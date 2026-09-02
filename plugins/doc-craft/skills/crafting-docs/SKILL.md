---
name: crafting-docs
description: Use when writing or reviewing a formal engineering document — proposal, design doc, RFC, ADR, runbook, or how-to guide; when a draft keeps getting rejected as hard to read or hard to follow; when deciding which page a piece of content belongs on; or when a document must survive a strict owner review.
---

# crafting-docs

Rules for formal engineering documents, distilled from repeated owner-review
cycles (a full infrastructure proposal plus ~15 rejection rounds on a migration
runbook). Core principle: **place every piece of content by what the reader
does with it, and shape it for exactly that use** — a proposal argues, a
how-to executes, a record retrieves, a tutorial teaches.

## Language and platform layers

- Document written in Traditional Chinese → ALSO read `references/zh-tw.md`.
  Violations of that layer are the most-rejected class of edit.
- Creating or editing Confluence pages through the REST API → ALSO read
  `references/confluence-editing.md` before touching storage format.
- (No English-specific layer exists yet; the rules below are language-neutral.)

## 1. Document family — decide where content lives (Diátaxis)

For every block of content ask: *what does the reader DO with this?*

| Reader's use | Document | Shape |
|---|---|---|
| Understand and decide (why) | Proposal / main doc | 3–6 pages, one-sitting read, persuasive narrative |
| Follow along (task) | Runbook / how-to sub-page | Command-level steps, expected output, pre-written rollback |
| Look up (information) | Research-record sub-page | Evidence, matrices, measured data; searchable beats narrative |
| Learn (background) | Tutorial / explanation doc | Context, labs, self-tests; main doc routes jargon here |
| Long-term record | ADR (written after approval) | One page: decision, rationale, what was rejected, consequences incl. negative |

Linking discipline: at most one "deeper →" downward link per section of the
main doc; each sub-page opens with one upward link; link by absolute document
name, never relative role names ("parent page" — pages get moved).
"A junior must understand it, but no information may be lost" resolves as:
never delete information — move it to the document whose native purpose it is.

Family governance: adding, deleting, or moving a family member (sub-page)
requires owner approval first, and each membership change triggers a re-review
of the whole family layout. No "I'll just quickly add a page".

## 2. Proposal skeleton

metadata (named approvers / status / deadline) → glossary (≤10 entries, each
"definition; relevance to this case") → summary + explicit ask +
**reversibility statement** (rigor scales with irreversibility — tell approvers
where their attention belongs) → problem & deadline (numbers, not adjectives) →
constraints & principles (Goals/Non-Goals; state their SOURCE — derived from
the status quo, or worked backward from long-term direction; they are the
yardstick for later selection and acceptance) → options & alternatives (per-
option rejection reasons; gating conditions and exit mechanisms un-collapsed in
the body) → execution strategy (conceptual; details go to the runbook) →
schedule → risks (gating vs managed) → open questions → document index.

- If the problem section already proved "doing nothing is not viable", do NOT
  list "keep running as-is" as a candidate option (it forces the reader to
  re-litigate the problem section). Position stopgaps like "maintain a fork"
  as a temporary bridge under the exit mechanism.
- Open questions may only hold questions whose answer does not change the
  correctness of the chosen option; a question that could break a principle
  boundary is promoted to a gating precondition.

## 3. Writing rules (check one by one on review)

1. **Claim–evidence coupling**: every load-bearing claim carries its
   verification method in one sentence (what was scanned, when, how
   exhaustively). Summary confidence must not exceed the evidence section —
   hedge unverified claims to their gate number.
2. **Single source**: each number/list is written in exactly one place (main
   doc explains mechanism, runbook holds values). Duplication is drift's
   breeding ground; most review-round inconsistencies happen at duplicates.
3. **Code-name restraint**: at most 3 code systems per document (e.g. P1–P8
   principles, G1–G8 gates), each defined locally. Lists cited by other
   documents MUST be numbered.
4. **Gates and acceptance as binary tests**: action + pass condition + failure
   consequence. "Posture finalized" — satisfiable by any outcome — is
   unfalsifiable. Thresholds are approved together with the doc, never
   back-filled later.
5. **No self-praise**: delete "the honest version", "we won't force it" —
   let content demonstrate honesty instead of claiming it.
6. **Sentence craft**: a parenthesis holds at most one full clause, never
   nested, one per sentence; one sentence, one fact; argue in full sentences,
   bullets only for scope lists.
7. **Term management**: expand every abbreviation inline at first use;
   disambiguate collision-prone terms (a Kubernetes Service object vs the
   everyday word "service"). A glossary needing >10 entries means the body is
   too jargon-dense — fix the body.
8. **Rollback and coupling honesty**: before claiming "independently
   rollback-able", verify the architecture actually decouples it (shared
   Services/resources). Mark irreversible points explicitly and give them hold
   points. Rollback triggers are default-to-safe: breach → roll back first,
   discuss later.
9. **Engineer the discipline**: any critical rule that relies on humans
   remembering ("freeze applies during the window", "de-manage before
   uninstall") must be stated as an engineered control (CI lock, precheck) or
   at least name how it will become one.

## 4. How-to / runbook shape

The body of a how-to is an executable step sequence. Prose only marks where
the reader is; it never explains why (explanations live in collapsibles or an
explanation doc).

Per-paragraph test — apply to every paragraph:
- [OK] a command the reader runs as-is
- [OK] a pointer to the exact command in another document
- [Not OK] anything the reader must reason about before acting
  ("verify: end-to-end probe plus metrics look normal" — how, exactly?)
- [Not OK] "same command, just change two values" — still thinking

1. **Opening = 2–3 sentences of intent, then straight into steps.** Document
   roles are expressed by the page tree, not a role table; anything the tree
   cannot express ("canonical commands live on page X") gets one sentence.
   Execution status is a single sentence.
2. **Parameters as an assignment code block**: the first code block defines
   variables (one commented section per environment; uncomment to select,
   derivation commands included); every later command references `$VAR` —
   switching environments edits one place. If a parameter table survives, it
   holds parameters only; inventory data and reference values move to their
   point of use.
3. **Rollback lives inside the step**: embedded as the final action of each
   step's sequence, with complete paste-ready commands. Never a standalone
   rollback chapter that makes an incident responder cross-reference pages.
   Incident-time test: no page-flipping, no reading, paste directly.
4. **Teaching, mechanism, and design rationale go into collapsibles** (titled
   "read when stuck; not needed to operate") or an explanation doc. Helper
   content must never borrow "Step N" numbering — monitoring/interpretation
   guidance either merges into its step or stays unnumbered, otherwise it
   reads as a second competing step list.
5. **Checklist hygiene**: delete completed-checkbox sections wholesale (keep
   only live content). Coordination items (announcements, notifications,
   ticket confirmations) are not per-environment execution steps and do not
   belong in the checklist. An engineering TODO that is not yet a procedure
   does not deserve a checkbox. An item that restates another document becomes
   a pointer (transclusion with a single canonical source where the platform
   supports it).
6. **Schedule section**: one sentence listing the hard time constraints (only
   these shape the schedule), then the dated table. Completed phases collapse
   to one line. Reviewers want "N days before cutover, X must be done", not a
   calendar narrative.
7. **Doc-aging patrol** (mandatory after execution progresses): re-verify
   every "currently / as-is / final state" phrase; purge names of withdrawn
   commitments; re-check cited PR and version numbers. When compressing
   sentences, never drop the middle link of a causal chain — "A, therefore C"
   with B missing reads as pressure, not reasoning, and gets rejected.

## 5. Review flow (run after writing, before handing over)

1. **Self-challenge** per section: does this belong here? Would a junior
   understand it? Does the narrative flow problem → criteria → solution →
   validation → limitations? Is term density burying the point?
2. **Junior playtest**: 2–3 reader personas as fresh agents, given only the
   document's plain text and no other tools (backend dev who doesn't know
   infra / new-hire who knows the stack but not the org / frontend dev). Ask
   each for: a five-sentence restatement, a list of stuck points, quiz answers
   (what is being approved? what happens on failure? which step is most
   dangerous? how to roll back?), per-section comprehension %. When exporting
   plain text, keep link anchor text — stripping it manufactures false
   "missing link" findings.
3. **Expert panel** (no org context, cross-domain): academic reviewer
   (claim–evidence, falsifiability, hedging), technical writer (information
   architecture, duplicate-source drift, sentence craft, term binding),
   safety/systems engineer (role separation, hold points, default-to-safe,
   engineered vs administrative controls). The three lenses barely overlap.
4. **Verify before relaying agent findings**: fact-check any agent inference
   (especially about schedule or architecture) yourself before turning it into
   a question for a human. Unverified questions waste the owner's time.
5. After fixes, **re-run every affected check** (punctuation audit,
   cross-references, code-system numbering consistency).
