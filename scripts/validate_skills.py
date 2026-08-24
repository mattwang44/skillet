#!/usr/bin/env python3
"""Check every SKILL.md against this repo's authoring rules.

Enforced (exit 1):
  - frontmatter present, with non-empty name and description
  - name matches the containing directory
  - name is lowercase letters, digits, hyphens
  - description within 1024 characters
  - body under 500 lines
  - every referenced references/*.md exists
  - no reference file links to another reference file (must stay one level deep)

Advisory (printed, exit 0):
  - description not starting with "Use when"
  - description that reads like a workflow summary
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MD_LINK = re.compile(r"\]\((?!https?://)([^)]+\.md)\)")
BACKTICK_REF = re.compile(r"`(references/[\w./-]+\.md)`")
WORKFLOW_WORDS = re.compile(r"\b(then|first|next|step \d|after that)\b", re.IGNORECASE)

MAX_BODY_LINES = 500
MAX_DESCRIPTION = 1024


def parse_frontmatter(text: str) -> tuple[dict[str, str], int]:
    """Return (fields, body start line). Only scalar keys are needed here."""
    if not text.startswith("---\n"):
        return {}, 0
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, 0
    fields, key = {}, None
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if match:
            key, value = match.group(1), match.group(2).strip()
            fields[key] = value.strip("'\"")
        elif key and line.startswith((" ", "\t")):
            fields[key] = f"{fields[key]} {line.strip()}".strip()
    return fields, text[: end + 5].count("\n")


def check_skill(skill_md: Path, errors: list[str], notes: list[str]) -> None:
    rel = skill_md.relative_to(REPO)
    text = skill_md.read_text(encoding="utf-8")
    fields, body_start = parse_frontmatter(text)

    if not fields:
        errors.append(f"{rel}: missing or malformed YAML frontmatter")
        return

    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        errors.append(f"{rel}: frontmatter has no name")
    elif not NAME_RE.match(name):
        errors.append(f"{rel}: name {name!r} must be lowercase letters, digits and hyphens")
    elif name != skill_md.parent.name:
        errors.append(f"{rel}: name {name!r} does not match directory {skill_md.parent.name!r}")

    if not description:
        errors.append(f"{rel}: frontmatter has no description")
    else:
        if len(description) > MAX_DESCRIPTION:
            errors.append(f"{rel}: description is {len(description)} chars (max {MAX_DESCRIPTION})")
        if not description.startswith("Use when"):
            notes.append(f"{rel}: description does not start with 'Use when'")
        if WORKFLOW_WORDS.search(description):
            notes.append(
                f"{rel}: description reads like a workflow summary — agents will follow it "
                "instead of the body"
            )

    body_lines = len(text.splitlines()) - body_start
    if body_lines > MAX_BODY_LINES:
        errors.append(f"{rel}: body is {body_lines} lines (max {MAX_BODY_LINES}) — move detail into references/")

    linked = set(MD_LINK.findall(text)) | set(BACKTICK_REF.findall(text))
    for target in linked:
        if not (skill_md.parent / target).is_file():
            errors.append(f"{rel}: references missing file {target}")

    for ref in sorted((skill_md.parent / "references").glob("*.md")):
        ref_text = ref.read_text(encoding="utf-8")
        nested = set(MD_LINK.findall(ref_text)) | set(BACKTICK_REF.findall(ref_text))
        if nested:
            errors.append(
                f"{rel.parent / 'references' / ref.name}: links to {sorted(nested)} — "
                "references must stay one level deep from SKILL.md"
            )
        if len(ref_text.splitlines()) > 100 and "## Contents" not in ref_text:
            notes.append(f"{rel.parent / 'references' / ref.name}: over 100 lines without a Contents section")


def main() -> int:
    skills = sorted(REPO.glob("plugins/*/skills/*/SKILL.md"))
    if not skills:
        print("no skills found", file=sys.stderr)
        return 1

    errors: list[str] = []
    notes: list[str] = []
    for skill in skills:
        check_skill(skill, errors, notes)

    for note in notes:
        print(f"note: {note}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    print(f"\nvalidate_skills: {len(skills)} skills, {len(errors)} errors, {len(notes)} notes")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
