# skillet

My personal Claude Code marketplace. The skills I actually use, iterated in public.

```bash
claude plugin marketplace add mattwang44/skillet
```

## Plugins

| Plugin | Skill | What it's for |
|---|---|---|
| `skillsmith` | `curating-skills` | The single door for changing anything in this repo |
| `pydocs-zhtw` | `translating-python-docs` | Translating CPython docs into Traditional Chinese for [python-docs-zh-tw](https://github.com/python/python-docs-zh-tw) |
| `explain` | `eli5` | Any topic as an HTML picture explainer with big visuals and few words |
| `doc-craft` | `crafting-docs` | Writing and reviewing formal engineering docs (proposals, RFCs, runbooks, how-to guides), with a zh-TW language layer and Confluence API-editing traps |

```bash
claude plugin install skillsmith@skillet
claude plugin install pydocs-zhtw@skillet
claude plugin install explain@skillet
claude plugin install doc-craft@skillet
```

## Why this exists

Skills kept accumulating in places I can't publish or share. This is where the
general ones live so I can keep sharpening them. Three rules keep it useful rather
than just large:

1. **Nothing employer-specific.** `scripts/check_leaks.py` enforces it, backed by a
   personal blocklist kept outside the repo on purpose.
2. **Skills earn their place by failing first.** Nothing gets added or edited
   without a concrete moment where an agent did the wrong thing.
3. **Short beats thorough.** `eli5` is four lines and works.

Built for one user, so it optimizes for iteration speed over generality. Take
anything you find useful.

## Local development

```bash
git clone https://github.com/mattwang44/skillet ~/Developer/skillet
claude plugin marketplace add ~/Developer/skillet   # iterate without pushing
claude plugin marketplace update skillet            # after each change
```

```bash
python3 scripts/build_marketplace.py --check   # marketplace.json is generated, not written
python3 scripts/validate_skills.py
python3 scripts/check_leaks.py --all           # needs ~/.config/skillet/blocklist.txt
```

Set up the leak gate's personal blocklist once:

```bash
mkdir -p ~/.config/skillet
$EDITOR ~/.config/skillet/blocklist.txt   # one case-insensitive regex per line
```

## License

MIT. `eli5` is a near-verbatim mirror of [@trq212's skill](https://github.com/anthropics/claude-plugins-community/tree/main/eli5),
credited in `plugins/explain/skills/eli5/CREDITS.md`.
