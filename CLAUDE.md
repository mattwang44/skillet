# skillet

Matt's personal, public Claude Code marketplace.

## The one rule

**Do not edit any file under `plugins/` directly.** Invoke
`/skillsmith:curating-skills` and follow it. It exists because untested skill edits
are how a skill collection rots, and it is the only path that runs the leak gate.

If `skillsmith` is not installed, read
`plugins/skillsmith/skills/curating-skills/SKILL.md` and follow it manually.

## This repo is public

It must not contain anything employer-specific: no company or product names, no
internal repo, service, host, or table names, no ticket keys, no colleague names,
no work email. Before any commit:

```bash
python3 scripts/check_leaks.py --staged
```

A non-zero exit means do not commit.

## Generated files

`.claude-plugin/marketplace.json` is generated. Edit `plugins/*/.claude-plugin/plugin.json`
and run `python3 scripts/build_marketplace.py`.
