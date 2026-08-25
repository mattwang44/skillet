---
name: curating-skills
description: Use when adding, editing, splitting, renaming, or removing any skill in the skillet marketplace; when a session reveals that a skill gave wrong guidance, gave no guidance, or was ignored entirely; when a technique discovered in this session seems worth keeping; or before committing anything to the skillet repo.
---

# curating-skills

The only door into `mattwang44/skillet`. Every skill in that repo is added, changed,
split, or deleted through this workflow — never by opening a `SKILL.md` and typing.

`$ARGUMENTS` — optional description of what went wrong this session. If empty, infer
it from the conversation, then confirm it in Step 1 before touching anything.

## The Iron Law

**No skill change without an observed failure first.** A concrete moment where an
agent — in this session or a previous one — did the wrong thing, or where you did
something by hand that a skill should have handled.

This applies to edits exactly as much as to new skills.

**No exceptions:**
- Not for "I'm just fixing a typo in the description" — description changes alter
  which skills load. That is behavior. Observe it.
- Not for "I already know this is right"
- Not for "the skill is obviously missing this section"
- Not for "I'll write it now and test it later" — later never arrives, and an
  untested skill is worse than no skill because it displaces attention
- Not for "it's my own repo, I'll just try it"

An unobserved change is a guess. Guesses accumulate into a skill collection that
nobody trusts and everybody re-reads from scratch.

## Workflow

Copy this checklist into your response and tick items as you go:

```
- [ ] 1. State the observation (RED)
- [ ] 2. Classify the failure, pick the matching form
- [ ] 3. Route: new / edit / split / delete
- [ ] 4. Write the minimal change
- [ ] 5. Verify with a fresh agent (GREEN)
- [ ] 6. Leak gate
- [ ] 7. Bookkeeping and commit
```

### Step 1 — State the observation (RED)

Write it down in this exact shape before reading any skill file:

```
Trigger:    [what was asked]
Expected:   [what a good agent should have done]
Actual:     [what happened, quoted where possible]
Skill:      [which skill should have caught this, or "none exists"]
```

If you cannot fill in `Actual` with something that actually happened, **stop and say
so.** Offer to run the scenario first (Step 5's baseline mode) and come back.

### Step 2 — Classify the failure, pick the matching form

The shape of the fix is decided by the shape of the failure, not by taste:

| The failure was… | Write it as… | Do NOT write… |
|---|---|---|
| Knew the rule, skipped it under pressure | Prohibition + rationalization table + red flags | "prefer…", "consider…" |
| Complied, but output had the wrong shape | A positive recipe: name the parts of the output, in order | A list of "don't do X" |
| Left out a required element | A REQUIRED slot in a template the agent fills in | A prose reminder near the template |
| Should have depended on a condition | A conditional on an observable predicate | Unconditional rule + exemption clause |
| Agent simply never loaded the skill | Fix the `description` triggers — nothing else | More content in the body |

Two rules that override preference:
- **Never append a nuance clause.** "…unless it matters" reopens the negotiation and
  turns a stable rule into a noisy one.
- **Exemption clauses do not scope.** "This limit doesn't apply to code blocks" still
  suppresses code blocks. Restructure so the rule cannot reach the exempt part.

### Step 3 — Route

| Situation | Action |
|---|---|
| No skill covers this domain at all | New skill in the closest existing plugin |
| A skill exists but has a gap | Edit that skill |
| Skill is over 500 lines, or half of it loads for nothing | Split: move the cold half into `references/` |
| Two skills keep being invoked together | Merge, or make one declare the other REQUIRED |
| A skill has not fired in months, or you route around it | Delete it. A skill you distrust costs more than it saves |

New plugin only when the domain shares no tooling, no vocabulary, and no triggers
with any existing plugin. Prefer a new skill inside an existing plugin.

### Step 4 — Write the minimal change

Read `references/authoring-rules.md` before writing. The contract in one line: a
SKILL.md is *triggers in the frontmatter, and only what the model does not already
know in the body*.

Address the observation from Step 1 and nothing else. Do not add sections for cases
you imagined. The `eli5` skill in this repo is four lines long and works — that is
the bar.

### Step 5 — Verify with a fresh agent (GREEN)

Your own context is contaminated: you just wrote the skill, so of course it makes
sense to you. Verification only counts in a context that has never seen it.

```bash
# Baseline (RED) — reproduce the failure without the skill
claude -p "<the Step 1 trigger, verbatim>"

# With the skill (GREEN) — same trigger, skill content pasted in
claude -p "$(cat plugins/<plugin>/skills/<skill>/SKILL.md)

---
<the Step 1 trigger, verbatim>"
```

Dispatching a subagent works too, as long as it is given the trigger and nothing
about your intent. Never tell the verifying agent what you hope it will do.

Read the output yourself. Automated matching over-reports on both sides — template
echoes look like compliance and quoted counter-examples look like violations.

**Pass condition:** baseline reproduces the failure, and the GREEN run does not.
If the baseline does *not* fail, the skill has nothing to fix. Delete the change.

For anything that shapes behavior rather than supplying facts, run GREEN 5+ times.
Five different interpretations across five runs means the wording is not binding —
tighten the form from Step 2 rather than adding more words.

### Step 6 — Leak gate

This repo is public. It must not know anything about any employer.

```bash
python3 scripts/check_leaks.py --staged
```

The gate is not advisory. A non-zero exit means do not commit. If it flags something
you believe is a false positive, say which pattern and why, out loud, before
overriding — never silently.

If the gate reports a missing blocklist, that is also a hard stop. See
`references/repo-conventions.md` for how to create it.

### Step 7 — Bookkeeping and commit

```bash
python3 scripts/build_marketplace.py   # regenerate .claude-plugin/marketplace.json
git add -A && python3 scripts/check_leaks.py --staged
```

Bump the touched plugin's `version` in its `plugin.json`: patch for wording, minor
for a new skill or a new capability, major for a rename or removal.

Commit as `<type>(<plugin>): <what changed>`, and put the Step 1 observation in the
body — that is the record of *why*, and future-you will want it:

```
fix(pydocs-zhtw): terminology is settled in review, not by a checker

Observed: agent finished library/asyncio-task.po, ran the validators the
skill listed, and reported done with 「函數」still in three entries. The
skill described a checker that does not exist in python-docs-zh-tw --
upstream CI only runs `make all` -- so nothing ever read the wording.
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "It's my own repo, I don't need the ceremony" | The ceremony is the only thing separating a skill collection from a pile of notes. |
| "The failure is obvious, I don't need to write it down" | Obvious failures produce vague fixes. The written observation is what makes the fix minimal. |
| "I'll verify it next time I happen to use it" | You will not notice a skill quietly under-performing. You only notice it failing loudly. |
| "Adding a section can't make it worse" | It can. Every added line lowers the odds the agent reads the line that matters. |
| "It's just the description" | The description decides whether the skill loads at all. It is the highest-leverage line in the file. |
| "The leak gate is being paranoid" | The gate is cheap and the mistake is permanent. Public git history is not deletable. |
| "I'm mid-flow, I'll curate at the end of the session" | At the end of the session you will have lost the verbatim `Actual`. Capture it now, apply it later. |

## Red flags — stop and restart the workflow

- You have a `SKILL.md` open and have not written the Step 1 observation
- You are describing what the change will improve, in the future tense
- The `description` you just wrote contains the words "then", "and then", or a list
  of steps — that is a workflow summary, and agents will follow it *instead of*
  reading the body
- You are adding a third example of a pattern that already has two
- You are about to commit without running `check_leaks.py`
- The skill grew past 500 lines and you are looking for things to trim rather than
  things to move into `references/`

## References

- `references/authoring-rules.md` — what a good SKILL.md contains, and the frontmatter contract
- `references/repo-conventions.md` — skillet's layout, versioning, leak gate, and install commands
