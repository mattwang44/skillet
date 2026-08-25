---
name: translating-python-docs
description: Use when translating or reviewing .po files in the python/python-docs-zh-tw repository — filling empty msgstr entries, updating entries marked #, fuzzy, fixing sphinx-lint or powrap failures, or resolving reviewer comments about terminology, spacing, or reST markup. Also use when asked to translate CPython documentation into Traditional Chinese.
---

# translating-python-docs

Translate CPython documentation PO files into Traditional Chinese for
`python/python-docs-zh-tw`.

Everything below is calibrated against three years of review history in that repo:
473 PRs, 2138 review threads, 1562 accepted before/after corrections. Where a rule
carries a count, that is how often reviewers actually had to fix it.

## Before starting

```bash
poglossary --help          # pip install poglossary if missing
ls poglossary.yml          # the repo's enforced glossary
```

`make build` needs a sibling CPython checkout at `../cpython` and the venv at
`~/.venvs/python-docs-i18n/`. Translation and linting work without it.

## Workflow

```
- [ ] 1. Pick the work
- [ ] 2. Read the whole entry, and the entries around it
- [ ] 3. Resolve every term through the lookup ladder
- [ ] 4. Translate
- [ ] 5. Run the validators until clean
- [ ] 6. Self-review against the checklist
- [ ] 7. Commit
```

### Step 1 — Pick the work

```bash
make fuzzy      # previously translated, now stale — highest value per effort
make progress
```

Resolving a fuzzy entry means fixing the text **and deleting the `#, fuzzy` flag**.
Leaving the flag means the entry still does not ship.

### Step 2 — Read the whole entry, and the entries around it

Read the complete `msgid`, plus `msgctxt` and translator comments, before writing a
character.

Then read how the **same file** already renders the terms you are about to use.
Consistency inside a page was the single most common review theme — 222 comments,
more than any mechanical rule. An established rendering in the file you are editing
beats a global preference:

> 前面的 `line` 都翻「列」的話這邊就翻列吧
> 下面的 parent 有翻譯，那這邊的 children 是否也應該翻譯？
> 同一篇文章 executor 也被翻譯成「執行器」，應該做出區別以免讓讀者誤解

```bash
grep -n "術語" <file>.po                                    # this file's existing usage
grep -rn "術語" --include=*.po . | head                     # the project's usage
```

### Step 3 — Resolve every term through the lookup ladder

Terminology disputes dominate review. Walk this ladder in order and stop at the
first hit — do not invent a rendering:

1. `poglossary.yml` in the repo root — the only source CI enforces
2. `glossary.po`, or <https://docs.python.org/zh-tw/3/glossary.html>
3. The same file, then the rest of the repo (`grep -rn --include=*.po`)
4. [術語列表 Wiki](https://github.com/python/python-docs-zh-tw/wiki/%E8%A1%93%E8%AA%9E%E5%88%97%E8%A1%A8) (73 comments cite it)
5. [樂詞網 / 國家教育研究院](https://terms.naer.edu.tw/) (24 comments cite it)
6. Nothing established → **keep the English.** This is the house answer, not a
   fallback: "任何相關翻譯都不通用" / "直接放原文我比較好受".

`references/terminology.md` holds the resolved table and the forms reviewers strip.

### Step 4 — Translate

Six mechanics account for most corrections. Full patterns in
`references/rest-and-po.md`.

**1. Never edit `msgid`.** It is upstream English. Only `msgstr` and the `#, fuzzy`
flag are yours. Agents get this wrong often enough that reviewers have a stock
phrase for it: *"revert the change to the original string (msgid)"*.

**2. The separator depends on what the role renders as, not on what surrounds it.**

This is the rule most often applied backwards. Look at what the *reader* sees — the
display text if the role is `` `display <target>` ``, otherwise the target:

| The role renders as | Use | Example |
|---|---|---|
| Latin (`asyncio.run`, `ParamSpec`, `None`) | a normal half-width space | ``並以 :func:`asyncio.set_event_loop` 將其`` |
| Chinese (`` `可雜湊的 <hashable>` ``) | `\\ ` on both sides | ``必須是\\ :term:`可雜湊的 <hashable>`\\ 或`` |

Latin renders as Latin, so ordinary CJK-Latin spacing applies and `\\ ` would
wrongly suppress the space. Chinese needs no space but reST still demands
whitespace, which is what `\\ ` supplies at zero width.

Across the corpus reviewers moved Latin-rendering roles from `\\ ` to a space
(43 → 11) and CJK-rendering roles from a space to `\\ ` (33 → 70).

**3. `::` must match the msgid, in both directions.**

If the msgid ends in `::`, the translation ends in `： ::` — full-width colon, one
space, then `::`. If the msgid ends in a plain colon, **do not add `::`**; it
introduces a literal block that has no code to follow it and warns at build time.
89 comments touch this.

```
msgid  "Here is a code example::"      msgstr "以下是個程式範例： ::"
msgid  "using the :func:`.round`:"     msgstr "使用 :func:`.round` 函式進行捨入："
```

**4. Space between CJK and Latin — including inside role targets.**

```
method 會基於數字        not  method會基於數字
關於 IP 版本的說明        not  關於IP 版本的說明
:ref:`捨棄 <whitespace>`  not  :ref:`捨棄<whitespace>`
```

No space against full-width punctuation: 使用「CPU」運算.

**5. Brackets follow their contents; gloss unfamiliar terms on first use.**

Chinese inside → full-width （）. English inside → half-width () with surrounding
spaces. When a term is uncommon or newly introduced, give the Chinese and keep the
English in half-width parentheses — **at the term's first occurrence in the page**,
not a later one (42 comments):

```
正規表示式 (regular expression)
點號參照 (dotted reference)
執行\\ :term:`協程 (coroutine) <coroutine>` *coro* 以及回傳結果
```

**6. Code stays; `#` comments in examples get translated.**

Preserve inline literals exactly — `` ``False`` `` never becomes `"False"`. Do not
translate identifiers, keywords, dunder names, exception classes, URLs, or role
targets inside `<>`. Comments inside example code **are** translated ("code comment
need translation"); docstrings that a doctest displays are not.

**Line width is 79 characters.** Never hand-wrap — `make wrap` does it in Step 5.

### Step 5 — Run the validators until clean

Do not report a file as done before this loop passes.

```bash
poglossary <file>.po poglossary.yml   # glossary violations
make lint                             # sphinx-lint: broken reST
make wrap                             # normalize to 79 chars — run last, it rewrites
```

On failure: read the message, fix the entry, rerun from `poglossary`.

A genuine false positive is fixed with an `ignore.patterns` entry in
`poglossary.yml`, never by rewording the translation to dodge the check.

### Step 6 — Self-review against the checklist

Reviewers catch the same things every time. Walk the list before asking anyone else
to:

```
- [ ] msgid untouched
- [ ] no clause dropped — every idea in the msgid appears in the msgstr (33 comments)
- [ ] each polysemous word checked against context (77 comments)
- [ ] terms match the rest of this file (222 comments)
- [ ] separators match what each role renders as
- [ ] `::` presence matches the msgid exactly
- [ ] uncommon terms glossed at first occurrence in the page
- [ ] #, fuzzy removed from anything finished
```

**The polysemy check has no shortcut.** Reviewers repeatedly caught words translated
by their most common sense rather than the one in play:

| Word | Wrong sense taken | Actual sense here |
|---|---|---|
| introducing | 介紹 | 引入（a PEP introduces syntax） |
| integral | 整數 | 積分 |
| function | 函式 | 功能, in non-API prose |
| active | 啟用 | 活躍 (active user) |
| complex | 複雜 | 複數 (complex number) |
| line | 行 | 列, where the file already says 列 |

When a word could plausibly be two things, say which one you picked and why in the
PR description. That is cheaper than a review round trip.

### Step 7 — Commit

One PO file per commit where practical.

```
tutorial/classes.po: 翻譯 class 定義章節
```

## Common mistakes

| Mistake | Consequence |
|---|---|
| `\\ ` around a role that renders Latin | Space suppressed where one is needed |
| Plain space around a role that renders Chinese | Stray space on the page |
| Adding `::` the msgid does not have | Empty literal block, build warning |
| `： ` where the msgid had `::` | Literal block silently disappears |
| Editing `msgid` | Diverges from upstream; reviewer reverts the whole entry |
| `"False"` instead of `` ``False`` `` | Loses code formatting |
| Inventing a rendering for an unlisted term | Review round trip; the answer was usually "keep the English" |
| Hand-wrapping to 79 chars | `make wrap` reflows differently; noisy diff |
| Leaving `#, fuzzy` on a finished entry | Entry does not ship |
| Reporting done without `poglossary` | zh_CN forms reach review |

## References

- `references/rest-and-po.md` — full reST role, link, and gettext escaping patterns
- `references/terminology.md` — resolved terms, the lookup ladder's outputs, forms reviewers strip
- `references/review-findings.md` — what three years of review history actually shows, and how these rules were derived
