# Review findings

The observation record behind this skill. Every rule that carries a count traces
back to the measurement described here, so it can be re-derived and re-checked when
the project's conventions drift.

## Contents

- Corpus and method
- What reviewers actually changed
- The separator finding
- Terminology corrections
- Themes that only appear in prose comments
- What this evidence does not cover

## Corpus and method

All pull requests in `python/python-docs-zh-tw` created on or after 2023-08-25,
pulled through the GitHub GraphQL API:

- 473 PRs
- 2138 review threads
- 3041 comments, of which 2991 are substantive (bots and bare acknowledgements
  removed)

1562 of those comments contain a ` ```suggestion ` block whose diff hunk supplies
the original line. Those are objective before/after pairs: a reviewer's own
correction, accepted into the file. They are the primary evidence. Prose comments
are the secondary evidence, and are where the reasoning lives.

Corrections were classified by diffing each pair character-wise and tagging what
moved: separators, ASCII spaces, punctuation width, reST role content, and CJK
wording.

## What reviewers actually changed

| Change | Pairs |
|---|---|
| Wording or terminology | 1192 |
| Punctuation width or kind | 507 |
| Added a space | 452 |
| Removed a space | 171 |
| reST role content | 169 |
| Added a `\\ ` separator | 94 |
| Removed a `\\ ` separator | 90 |
| `::` literal-block colon | 37 |

The separator being removed almost as often as it is added was the finding that
changed this skill the most. Before this measurement the skill told the agent to
add a separator wherever Chinese abutted reST markup, which is exactly the error in
those 90 removals.

## The separator finding

Counting every role occurrence in the corpus, split by what the role renders as —
the display text where the role is `` `display <target>` ``, otherwise the target:

| Role renders | Separator | Before review | After review |
|---|---|---|---|
| Latin | `\\ ` before | 43 | 11 |
| Latin | space before | 329 | 479 |
| Latin | `\\ ` after | 22 | 15 |
| Latin | space after | 348 | 500 |
| Chinese | `\\ ` before | 33 | 70 |
| Chinese | space before | 23 | 20 |
| Chinese | `\\ ` after | 16 | 33 |
| Chinese | space after | 26 | 21 |

The movement is clean and bidirectional: reviewers push Latin-rendering roles toward
a plain space and Chinese-rendering roles toward `\\ `. The rule is therefore about
the rendered language of the role, not about what characters surround it in the
source.

## Terminology corrections

Measured as net frequency change across all pairs — a form appearing less often
after review than before was corrected away. This avoids the alignment errors that
token-level diffing produces on reflowed multi-line entries.

The resulting ranking is in the terminology reference. The headline results: 函數,
異常, 調用, and 返回 lead at 13–15 corrections each, and 參數 used where the source
says *argument* is the most corrected term that is not simply Mainland usage.

## Themes that only appear in prose comments

Suggestion blocks show what changed; prose comments show why, and surface whole
classes of problem that leave no mechanical trace:

| Theme | Comments |
|---|---|
| Consistency with the rest of the file or page | 222 |
| `::` handling | 89 |
| Word sense taken wrongly | 77 |
| Wiki 術語列表 cited as the authority | 73 |
| CJK-Latin spacing | 70 |
| glossary cited as the authority | 47 |
| Gloss the original at first occurrence | 42 |
| A project discussion cited as precedent | 41 |
| A clause or sentence dropped | 33 |
| 樂詞網 cited as the authority | 24 |
| msgid edited when it should not have been | 9 |

Consistency outranking every mechanical rule is the reason Step 2 of the workflow
reads the surrounding entries before translating anything.

## What this evidence does not cover

- **Review is a filter, not a census.** These are the mistakes that reached a
  reviewer and were caught. Mistakes nobody noticed are invisible here.
- **Reviewer mix.** A handful of maintainers account for most comments, so this
  measures their preferences as much as the project's written rules. Where the two
  disagreed, the written rule in `README.rst` was preferred.
- **Recency.** Conventions drift. A count from three years of history can be stale;
  the enforced source is always `poglossary.yml` plus `make lint`.
- **No baseline for the skill itself.** This measures human translators being
  corrected. It does not measure an agent using this skill and being corrected,
  which is the observation that should drive the next revision.
