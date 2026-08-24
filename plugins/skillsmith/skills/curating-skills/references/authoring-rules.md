# Skill authoring rules

Distilled from Anthropic's official skill-authoring guidance and the superpowers
`writing-skills` skill, plus what has actually held up in this repo.

## Contents

- The frontmatter contract
- The body contract
- Length and progressive disclosure
- Degrees of freedom
- Matching form to failure
- Content rules
- Feedback loops
- Anti-patterns

## The frontmatter contract

Only two fields are required. Everything else is optional and usually noise.

```yaml
---
name: hyphenated-lowercase-name
description: Use when <triggering conditions, symptoms, situations>.
---
```

- `name`: letters, numbers, hyphens only. Prefer gerunds for processes
  (`curating-skills`, `translating-python-docs`) and the bare noun for a
  single-shot output (`eli5`).
- `description`: third person, starts with "Use when", **triggering conditions
  only**. Under 500 characters where possible; 1024 is the hard cap.

**The description must never summarize the workflow.** This is the single most
expensive mistake in skill authoring. A description that describes the process
becomes a shortcut the agent takes *instead of* reading the body. A documented case:
a skill whose flowchart specified two review passes had a description mentioning
"code review between tasks" — agents did one review. Removing the process summary
from the description, changing nothing else, produced two.

```yaml
# Bad — summarizes the workflow, becomes the shortcut
description: Use when executing plans - dispatches a subagent per task with code review between

# Bad — first person
description: I can help you translate PO files

# Bad — too abstract to match against
description: For translation work

# Good — triggers only
description: Use when translating untranslated or fuzzy entries in a .po file of the CPython docs
```

Include the words a future agent would actually be thinking: error messages,
symptoms, tool names, file extensions, the user's own phrasing.

## The body contract

Assume the model is already very smart. Only add what it does not already have.
Challenge every paragraph: *does the agent really need this? does it justify its
token cost?*

A body generally contains, in this order:

1. One or two sentences of what this is and the core principle
2. When to use / when not to use, if the boundary is non-obvious
3. The workflow, or the pattern, or the reference table — whichever the skill is
4. Common mistakes
5. Pointers to `references/` files

Not every skill needs all five. `eli5` needs one line and an `$ARGUMENTS` slot.

## Length and progressive disclosure

- SKILL.md body: **under 500 lines**.
- Skills that load in most conversations: under 200 words.
- Everything heavier goes to `references/*.md`, linked **directly from SKILL.md**.

**References must be exactly one level deep.** Agents preview files reached through
a chain of references with `head -100` rather than reading them whole, so a
reference-inside-a-reference is silently truncated. If `a.md` needs `b.md`, link
both from SKILL.md.

Reference files over 100 lines start with a table of contents, so a partial read
still reveals the full scope of what is inside.

Organize `references/` by domain, not by sequence: `terminology.md` and
`rest-and-po.md`, never `part1.md` and `part2.md`.

## Degrees of freedom

Match specificity to how fragile the task is.

| Task | Give the agent |
|---|---|
| Many valid approaches, depends on context | Prose heuristics, principles |
| A preferred pattern with acceptable variation | Pseudocode, or a script with parameters |
| Fragile, order-dependent, consistency-critical | An exact command, and "do not modify it" |

The analogy: an open field gets a direction, a narrow bridge gets guardrails.

## Matching form to failure

Repeated from SKILL.md because it is the rule people skip:

| Failure | Form |
|---|---|
| Rule skipped under pressure | Prohibition + rationalization table + red flags |
| Output has wrong shape | Positive recipe naming the parts, in order |
| Required element omitted | REQUIRED slot in a template |
| Should be conditional | Conditional on an observable predicate |

Prohibitions measurably backfire on shaping problems. In head-to-head tests on
dispatch-prompt guidance, the "don't do X" arm produced *more* of the unwanted
content than the recipe arm, and trended worse than giving no guidance at all. A
recipe leaves nothing to negotiate with.

Never append a nuance clause to a rule that works. Adding one "unless it matters"
to a winning recipe degraded it from consistent to noisy across reps.

## Content rules

- **No time-sensitive information.** No "before August 2026, do X". If old behavior
  needs recording, put it in a collapsed `<details>` block titled "Old patterns".
- **One term per concept.** Pick "argument" or "parameter" and never drift.
- **One excellent example beats five mediocre ones.** Do not port the same example
  into five languages.
- **Give a default with an escape hatch, not a menu.** "Use pdfplumber; for scanned
  PDFs use pdf2image with pytesseract" — not "you could use any of these six".
- **Forward slashes in every path**, on every platform.
- Concrete over abstract. Real commands, real file names, real output.

## Feedback loops

A skill that ends in "check your work" produces worse results than one that ends in
a command whose exit code decides. Where a validator exists, name it, make running
it a numbered step, and state what to do when it fails:

```
1. Make the change
2. Run: <validator command>
3. If it fails: read the error, fix, return to step 2
4. Only proceed when it passes
```

If no validator exists and the task is quality-critical, the reference document
itself is the validator: "review against the checklist in X, note each issue with
its section, revise, re-check."

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Narrative ("in the session on 2026-08-24 we found…") | Not reusable; the reader is solving a different instance |
| Flowchart of linear steps | Cannot be copy-pasted; a numbered list is strictly better |
| Generic labels (`step1`, `helper2`) | Labels should carry meaning |
| Documenting every flag of a CLI | Point at `--help`; it cannot go stale |
| Restating what a cross-referenced skill says | Say `REQUIRED: use <skill>` and stop |
| `@path/to/file` links | Force-loads the file immediately and burns context |
