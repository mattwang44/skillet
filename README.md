# skillet

My personal Claude Code marketplace. The skills I actually use, iterated in public.

```bash
claude plugin marketplace add mattwang44/skillet
claude plugin install skillsmith@skillet
```

## Why this exists

I use Claude Code all day — Python backend work, infra, and side projects — and I
kept accumulating skills in three places: a work marketplace I can't publish, a
translation project's repo, and scratch files. This is where the general ones live
so I can keep sharpening them.

Three rules keep it useful rather than just large:

1. **Nothing employer-specific.** This repo is public and must not know anything
   about any employer — no internal names, tickets, hosts, or tables. A gate in
   `scripts/check_leaks.py` enforces it, backed by a personal blocklist kept
   outside the repo on purpose.
2. **Skills earn their place by failing first.** Nothing gets added or edited
   without a concrete moment where an agent did the wrong thing. See the Iron Law
   in `curating-skills`.
3. **Short beats thorough.** `eli5` is four lines and works. The model is already
   smart; the only tokens worth spending are on what it doesn't already know.

It's built for one user, so it optimizes for iteration speed over generality. Take
anything you find useful.

## Plugins

| Plugin | Skill | What it's for |
|---|---|---|
| `skillsmith` | `curating-skills` | The single door for changing anything in this repo |
| `pydocs-zhtw` | `translating-python-docs` | Translating CPython docs into Traditional Chinese for [python-docs-zh-tw](https://github.com/python/python-docs-zh-tw) |
| `explain` | `eli5` | Any topic as an HTML picture explainer with big visuals and few words |

```bash
claude plugin install pydocs-zhtw@skillet
claude plugin install explain@skillet
```

### skillsmith / curating-skills

The meta-skill. Every change to this repo goes through it, and it refuses to let me
edit a `SKILL.md` until I've written down what actually went wrong. It routes
new-vs-edit-vs-split-vs-delete, picks the *form* of the fix from the *shape* of the
failure, verifies in a fresh context rather than my contaminated one, and runs the
leak gate before anything is committed.

The discipline is the point. Without it a personal skill collection becomes a pile
of plausible-sounding markdown that nobody, including me, trusts.

### pydocs-zhtw / translating-python-docs

I translate the Python official docs into Traditional Chinese. The upstream repo
has skills already, but they split translate / check-terminology / validate across
three files I had to remember to chain, and mixed reST mechanics with prose
judgment.

This is one entry point covering the whole loop, and it treats validation as a
numbered step with real commands ([`poglossary`](https://github.com/mattwang44/poglossary),
`make lint`, `make wrap`) rather than a closing suggestion — which is what let
zh_CN wording reach review before.

### explain / eli5

A near-verbatim mirror of [@trq212's `eli5`](https://github.com/anthropics/claude-plugins-community/tree/main/eli5),
MIT, credited in `CREDITS.md`. Kept as-is because it's the taste benchmark for
this repo.

## Local development

```bash
git clone https://github.com/mattwang44/skillet ~/Developer/skillet
claude plugin marketplace add ~/Developer/skillet   # iterate without pushing
claude plugin marketplace update skillet            # after each change
```

```bash
python3 scripts/build_marketplace.py --check   # marketplace.json is generated, not written
python3 scripts/check_leaks.py --all           # needs ~/.config/skillet/blocklist.txt
```

Set up the leak gate's personal blocklist once:

```bash
mkdir -p ~/.config/skillet
$EDITOR ~/.config/skillet/blocklist.txt   # one case-insensitive regex per line
```

## License

MIT.
