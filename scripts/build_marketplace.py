#!/usr/bin/env python3
"""Regenerate .claude-plugin/marketplace.json from every plugin's own manifest.

The marketplace file is derived, never hand-edited: each plugin owns its name,
description, version and keywords in plugins/<name>/.claude-plugin/plugin.json,
and this script is the only thing that assembles them.

    python3 scripts/build_marketplace.py           # rewrite
    python3 scripts/build_marketplace.py --check    # exit 1 if stale
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO / "plugins"
MARKETPLACE = REPO / ".claude-plugin" / "marketplace.json"

OWNER = {"name": "mattwang44"}
DESCRIPTION = "Matt's personal Claude Code marketplace: the skills he actually uses, iterated in public."


def load_plugin(manifest: Path) -> dict:
    data = json.loads(manifest.read_text(encoding="utf-8"))
    plugin_dir = manifest.parent.parent
    missing = [key for key in ("name", "version", "description") if not data.get(key)]
    if missing:
        raise SystemExit(f"{manifest}: missing required field(s): {', '.join(missing)}")
    if data["name"] != plugin_dir.name:
        raise SystemExit(
            f"{manifest}: name {data['name']!r} does not match directory {plugin_dir.name!r}"
        )

    entry = {
        "name": data["name"],
        "description": data["description"],
        "source": f"./plugins/{plugin_dir.name}",
        "version": data["version"],
    }
    if data.get("keywords"):
        entry["tags"] = data["keywords"]
    return entry


def build() -> dict:
    manifests = sorted(PLUGINS_DIR.glob("*/.claude-plugin/plugin.json"))
    if not manifests:
        raise SystemExit(f"no plugin manifests found under {PLUGINS_DIR}")
    return {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": "skillet",
        "owner": OWNER,
        "metadata": {"description": DESCRIPTION, "pluginRoot": "./plugins"},
        "plugins": [load_plugin(m) for m in manifests],
    }


def main() -> int:
    generated = json.dumps(build(), indent=2, ensure_ascii=False) + "\n"

    if "--check" in sys.argv:
        current = MARKETPLACE.read_text(encoding="utf-8") if MARKETPLACE.exists() else ""
        if current != generated:
            print("marketplace.json is stale — run: python3 scripts/build_marketplace.py")
            return 1
        print("marketplace.json is up to date")
        return 0

    MARKETPLACE.parent.mkdir(parents=True, exist_ok=True)
    MARKETPLACE.write_text(generated, encoding="utf-8")
    count = len(json.loads(generated)["plugins"])
    print(f"wrote {MARKETPLACE.relative_to(REPO)} ({count} plugins)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
