# skillet repo conventions

## Contents

- Layout
- Where a new skill goes
- Versioning
- The leak gate
- Marketplace regeneration
- Installing and reloading

## Layout

```
skillet/
├── .claude-plugin/marketplace.json   # generated — never hand-edit
├── plugins/
│   └── <plugin>/
│       ├── .claude-plugin/plugin.json
│       └── skills/
│           └── <skill>/
│               ├── SKILL.md
│               └── references/*.md   # one level deep, flat
└── scripts/
    ├── build_marketplace.py
    └── check_leaks.py
```

Skills are invoked as `/<plugin>:<skill>` — so plugin names are a namespace the
user reads every time. Keep them short and domain-shaped (`explain`, `pydocs-zhtw`),
never a synonym of the skill inside them.

## Where a new skill goes

Into the existing plugin whose domain, vocabulary, and tooling it shares. Create a
new plugin only when it shares none of the three. Two skills in one plugin is
normal; a plugin holding one skill forever is a smell that it belongs elsewhere.

## Versioning

Each `plugins/<plugin>/.claude-plugin/plugin.json` carries its own semver.

| Change | Bump |
|---|---|
| Wording, examples, reference edits | patch |
| New skill, new capability, new reference file | minor |
| Rename, removal, breaking change to invocation | major |

The marketplace itself is not versioned; it is generated.

## The leak gate

`scripts/check_leaks.py` runs against staged changes and exits non-zero on anything
that looks like it came from private work.

Two rule sets:

1. **Generic patterns, committed.** Cloud account ids and ARNs, access-key shapes,
   private IP ranges, internal TLDs, ticket keys (an uppercase project prefix
   followed by digits), bearer tokens,
   and private-key headers. These describe *shapes*, not any organization.

2. **A personal blocklist, deliberately not in this repo.** One regex per line at
   `~/.config/skillet/blocklist.txt`, overridable with `$SKILLET_BLOCKLIST`. This
   holds the employer-specific strings — company and product names, internal repo
   and service names, colleague names, internal hostnames, warehouse tables.

Keeping set 2 outside the repo is the point: a public repo that ships a list of
company keywords has leaked the list. A missing blocklist file is a hard failure,
not a warning — the gate refuses to certify what it cannot check.

A `#` comments out the rest of a blocklist line only when it is followed by a
space or the end of the line, so `#channel-name` and `docs#anchor` stay part of
the pattern. The gate also rejects any pattern broad enough to match ordinary
prose, because that is what a half-truncated regex looks like and it would flag
every line while certifying nothing.

```bash
# create it
mkdir -p ~/.config/skillet
$EDITOR ~/.config/skillet/blocklist.txt   # one case-insensitive regex per line
```

## Marketplace regeneration

`.claude-plugin/marketplace.json` is derived from every `plugins/*/.claude-plugin/plugin.json`.

```bash
python3 scripts/build_marketplace.py          # rewrite it
python3 scripts/build_marketplace.py --check   # verify it is current, exit 1 if stale
```

Never hand-edit the generated file. If a field is wrong, fix the plugin's own
`plugin.json` and regenerate.

## Installing and reloading

```bash
claude plugin marketplace add mattwang44/skillet
claude plugin install skillsmith@skillet
claude plugin install pydocs-zhtw@skillet
claude plugin install explain@skillet
```

While iterating locally, point the marketplace at the working tree instead so edits
take effect without pushing:

```bash
claude plugin marketplace add ~/Developer/skillet
claude plugin marketplace update skillet   # after each change
```
