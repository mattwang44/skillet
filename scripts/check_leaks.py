#!/usr/bin/env python3
"""Refuse to let private work reach a public repo.

Two rule sets:

  Generic   Committed here. They describe *shapes* - credentials, cloud
            identifiers, private hosts, ticket keys - so they reveal nothing
            about any organization.

  Personal  Deliberately NOT in this repo. One case-insensitive regex per line
            in ~/.config/skillet/blocklist.txt (override with $SKILLET_BLOCKLIST).
            This is where employer, product, service, and colleague names live.
            A public repo that ships a list of company keywords has already
            leaked the list.

A missing personal blocklist is a hard failure, not a warning: the gate will not
certify what it cannot check. Use --generic-only where a personal list cannot
exist by design, such as CI.

    python3 scripts/check_leaks.py --staged        # staged diff (pre-commit)
    python3 scripts/check_leaks.py --all           # every tracked file
    python3 scripts/check_leaks.py --generic-only  # skip the personal blocklist
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_BLOCKLIST = Path.home() / ".config" / "skillet" / "blocklist.txt"

# Standards and public identifiers shaped like a ticket key (uppercase prefix,
# hyphen, digits) that are legitimate to mention in public documentation.
TICKET_KEY_ALLOWLIST = {
    "ISO", "RFC", "PEP", "UTF", "ASCII", "CVE", "CWE", "SHA", "AES", "RSA",
    "HTTP", "HTTPS", "TLS", "SSL", "IEEE", "ANSI", "GPL", "LGPL", "BSD", "MIT",
    "JSON", "YAML", "HTML", "CSS", "XML", "PNG", "JPEG", "GIF", "PDF", "UUID",
}

# Emails that are legitimately Matt's public identity.
EMAIL_ALLOWLIST = re.compile(
    r"@(gmail\.com|users\.noreply\.github\.com|python\.org|example\.com|example\.org)$",
    re.IGNORECASE,
)

GENERIC_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("AWS ARN", re.compile(r"\barn:aws[a-z-]*:", re.IGNORECASE)),
    ("cloud account id", re.compile(r"(?<![\w.])\d{12}(?![\w.])")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{16,}")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("generic API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("private IPv4", re.compile(
        r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b")),
    ("internal hostname", re.compile(r"\b[\w-]+\.(?:internal|corp|intranet|lan)\b", re.IGNORECASE)),
    ("Slack workspace", re.compile(r"\b[\w-]+\.slack\.com\b", re.IGNORECASE)),
    ("Jira/Confluence site", re.compile(r"\b[\w-]+\.atlassian\.net\b", re.IGNORECASE)),
    ("Snowflake account", re.compile(r"\b[\w-]+\.snowflakecomputing\.com\b", re.IGNORECASE)),
    ("Sentry DSN", re.compile(r"https://[0-9a-f]{16,}@[\w.-]*sentry[\w.-]*/", re.IGNORECASE)),
    ("database URL with password", re.compile(
        r"\b(?:postgres|postgresql|mysql|mongodb|redis|amqp)(?:\+\w+)?://[^\s:/@]+:[^\s@]+@")),
]

TICKET_KEY = re.compile(r"\b([A-Z][A-Z0-9]{1,9})-\d{3,6}\b")
EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")


def load_blocklist(generic_only: bool) -> list[tuple[str, re.Pattern[str]]]:
    if generic_only:
        return []
    path = Path(os.environ.get("SKILLET_BLOCKLIST", DEFAULT_BLOCKLIST)).expanduser()
    if not path.is_file():
        print(f"ERROR: personal blocklist not found at {path}", file=sys.stderr)
        print("", file=sys.stderr)
        print("This gate will not certify what it cannot check. Create it:", file=sys.stderr)
        print(f"  mkdir -p {path.parent}", file=sys.stderr)
        print(f"  $EDITOR {path}      # one case-insensitive regex per line, # for comments",
              file=sys.stderr)
        print("", file=sys.stderr)
        print("Or pass --generic-only where a personal list cannot exist (CI).", file=sys.stderr)
        raise SystemExit(2)

    rules = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        try:
            rules.append((f"blocklist:{line}", re.compile(line, re.IGNORECASE)))
        except re.error as exc:
            raise SystemExit(f"{path}:{lineno}: invalid regex {line!r}: {exc}")
    if not rules:
        raise SystemExit(f"{path}: blocklist is empty; add at least one pattern")
    return rules


def scan_line(text: str, rules: list[tuple[str, re.Pattern[str]]]) -> list[str]:
    hits = [label for label, pattern in rules if pattern.search(text)]
    for match in TICKET_KEY.finditer(text):
        if match.group(1) not in TICKET_KEY_ALLOWLIST:
            hits.append(f"ticket key ({match.group(0)})")
    for match in EMAIL.finditer(text):
        if not EMAIL_ALLOWLIST.search(match.group(0)):
            hits.append(f"non-public email ({match.group(0)})")
    return hits


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout


def added_lines() -> list[tuple[str, int, str]]:
    """Lines added in the staged diff, as (path, line number, text)."""
    out, path, lineno = [], "<unknown>", 0
    for line in git("diff", "--cached", "--unified=0").splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
        elif line.startswith("@@"):
            match = re.search(r"\+(\d+)", line)
            lineno = int(match.group(1)) if match else 0
        elif line.startswith("+") and not line.startswith("+++"):
            out.append((path, lineno, line[1:]))
            lineno += 1
    return out


def all_lines() -> list[tuple[str, int, str]]:
    out = []
    for name in git("ls-files").splitlines():
        file = REPO / name
        try:
            text = file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binary or unreadable: nothing to scan
        out.extend((name, i, line) for i, line in enumerate(text.splitlines(), 1))
    return out


def main() -> int:
    args = set(sys.argv[1:])
    rules = GENERIC_RULES + load_blocklist("--generic-only" in args)
    lines = all_lines() if "--all" in args else added_lines()

    findings = [
        (path, lineno, hit, text.strip()[:120])
        for path, lineno, text in lines
        for hit in scan_line(text, rules)
    ]

    if not findings:
        scope = "tracked files" if "--all" in args else "staged changes"
        print(f"check_leaks: clean ({len(lines)} lines of {scope})")
        return 0

    print(f"check_leaks: {len(findings)} finding(s) — DO NOT COMMIT\n", file=sys.stderr)
    for path, lineno, hit, text in findings:
        print(f"  {path}:{lineno}: {hit}\n    {text}", file=sys.stderr)
    print("\nFix the content. To override a genuine false positive, say which"
          "\npattern and why out loud first — never silently.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
