---
name: translating-python-docs
description: Use when translating or reviewing .po files in the python/python-docs-zh-tw repository — filling empty msgstr entries, updating entries marked #, fuzzy, fixing sphinx-lint or powrap failures, or resolving zh_CN wording flagged in review. Also use when asked to translate CPython documentation into Traditional Chinese.
---

# translating-python-docs

Translate CPython documentation PO files into Traditional Chinese for
`python/python-docs-zh-tw`.

The hard part is not the Chinese. It is that a `msgstr` is simultaneously a C
string, a reStructuredText fragment, and a line-wrapped gettext entry — and
breaking any one of the three fails the build silently or produces a page that
renders with stray spaces. Get the mechanics right and the prose takes care of
itself.

## Before starting

```bash
poglossary --help          # pip install poglossary if missing
ls poglossary.yml          # the repo's enforced glossary; if absent, ask before proceeding
```

`make build` needs a sibling CPython checkout at `../cpython` and the venv at
`~/.venvs/python-docs-i18n/`. Translation and linting work without it; only the
HTML render step needs it.

## Workflow

```
- [ ] 1. Pick the work
- [ ] 2. Read the whole entry before translating any of it
- [ ] 3. Translate
- [ ] 4. Run the validators until clean
- [ ] 5. Commit
```

### Step 1 — Pick the work

```bash
make fuzzy      # entries previously translated, now stale — highest value, lowest effort
make progress   # where the gaps are
```

Prefer fuzzy entries over empty ones unless asked otherwise: the English changed
slightly and the existing Chinese usually needs one clause adjusted, not a rewrite.
**Remove the `#, fuzzy` flag once resolved** — leaving it means the entry still
does not ship.

### Step 2 — Read the whole entry first

Read the complete `msgid`, plus `msgctxt` and any translator comments, before
writing a character. Translations that read fine in isolation and wrongly in
context are the most common review finding, and the most expensive to fix.

Then classify:

| Content | Handling |
|---|---|
| Prose | Translate |
| Code, identifiers, `` ``literal`` `` | Leave byte-identical |
| reST directive or role | Preserve the syntax; translate only display text |
| Mixed | Translate around the preserved parts |

### Step 3 — Translate

The four mechanics that actually break. Everything else is in
`references/rest-and-po.md`.

**1. The zero-width separator is `\\ ` in the PO file — two backslashes.**

reST needs whitespace around inline roles, but Chinese takes no space. `\ ` is the
zero-width separator; the PO file stores it escaped:

```
msgid "As discussed in :ref:`tut-object`, shared data can be surprising."
msgstr "如同在\\ :ref:`tut-object`\\ 的討論，共享的資料可能令人意外。"
```

Needed on **both** sides when Chinese sits on both sides. Omit it and the rendered
page shows a stray space.

**2. A paragraph ending in `::` becomes `： ::`.**

`::` introduces a literal block *and* renders as a colon. Translating it to `：`
alone destroys the code block; keeping `::` alone loses the colon.

```
msgid "Here is a code example::"
msgstr "以下是個程式範例： ::"
```

**3. Punctuation and brackets follow the text inside them, not the sentence.**

Chinese text takes full-width `「」（）、，。：；！？`; English text keeps half-width
`(),.;:!?`. For brackets, the deciding factor is the bracket's *contents*:

```
list（串列）是 Python 中很常見的資料型別。      ← Chinese inside → full-width
在超文件標示語言 (HTML) 中應注意跳脫符號。      ← English inside → half-width, with spaces
```

**4. Space between CJK and Latin, but not against symbols or punctuation.**

```
使用 CPU 運算       ← correct
使用「CPU」運算      ← correct, no space against 「」
```

**Terminology.** `poglossary.yml` in the repo root is authoritative because it is
what CI enforces, and it accepts *lists* of valid renderings. Several core terms
legitimately stay in English in running text — `class`, `method`, `module`,
`instance`, `list`, `int` all appear untranslated throughout the existing
translation. Do not "fix" them. Match the surrounding file. Common terms and the
zh_CN forms that fail review are in `references/terminology.md`.

Unsure of a rendering? Gloss it on first occurrence in the page and keep the
original: 正規表示式 (regular expression). Still unsure? Leave `#, fuzzy`.

**Line width is 79 characters.** Do not hand-wrap — `make wrap` does it correctly
in Step 4.

### Step 4 — Run the validators until clean

Do not report a file as done before this loop passes. This is the step the old
workflow left as a suggestion, and it is why zh_CN terms reached review.

```bash
poglossary <file>.po poglossary.yml   # glossary violations
make lint                             # sphinx-lint: broken reST
make wrap                             # normalize to 79 chars — run last, it rewrites
```

On failure: read the message, fix the entry, rerun from `poglossary`. Only when all
three are clean is the file done.

If a `poglossary` hit is a genuine false positive — the English word appearing in a
sense the glossary does not cover — the fix is an `ignore.patterns` entry in
`poglossary.yml`, not silently rewording the translation to dodge the check.

Optional render check, when `../cpython` is available:

```bash
make build <file>.po
```

### Step 5 — Commit

One PO file per commit where practical; reviewers diff per file.

```
tutorial/classes.po: 翻譯 class 定義章節
```

## Common mistakes

| Mistake | Consequence |
|---|---|
| Single `\ ` instead of `\\ ` in the PO source | Backslash lost on decode; stray space on the page |
| `：` alone where the msgid had `::` | Literal block silently disappears |
| Hand-wrapping lines to 79 chars | `make wrap` reflows it differently; noisy diff |
| Translating inside `` ``literal`` `` or a role target | Broken cross-reference, build warning |
| Translating `class`/`method` when the file leaves them in English | Inconsistent with surrounding text |
| Leaving `#, fuzzy` on a finished entry | Entry does not ship |
| Reporting done without running `poglossary` | zh_CN terms reach review |

## References

- `references/rest-and-po.md` — full reST role, link, and gettext escaping patterns
- `references/terminology.md` — core term table, terms kept in English, zh_CN forms to avoid
