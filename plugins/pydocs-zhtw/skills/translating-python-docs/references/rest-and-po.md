# reST and PO mechanics

Everything a `msgstr` has to satisfy at once: it is a C string, a reStructuredText
fragment, and a line-wrapped gettext entry. Rules below are the ones review history
shows people actually get wrong.

## Contents

- msgid is immutable
- Escaping: why the separator is written `\\ `
- Choosing between `\\ ` and a plain space
- Separators around full-width punctuation
- Inline roles
- Cross-references with display text
- Hyperlinks
- Inline literals
- Literal blocks and `::`
- Code, comments, and doctests
- Multi-line msgstr and line width
- Flags: fuzzy and others

## msgid is immutable

`msgid` is upstream English, synchronised from CPython. Only `msgstr` and the
entry's flags are editable. An edited msgid diverges the catalogue from upstream and
gets the whole entry reverted in review. Automated tooling is the usual culprit —
if a diff shows a changed msgid, that is a bug, not a translation.

Lines beginning `#.`, `#:`, and `#|` are machine-generated too. Only `#` translator
notes and `#,` flags are yours.

## Escaping: why the separator is written `\\ `

A `msgstr` value is a C string, so gettext decodes escapes when reading it. For the
decoded string to contain `\ ` — reST's zero-width separator — the file must
contain `\\ `.

```
file contains:      msgstr "這對\\ :ref:`使用者定義泛型 <user-defined-generics>`\\ 也成立"
gettext decodes to: 這對\ :ref:`使用者定義泛型 <user-defined-generics>`\ 也成立
reST renders:       這對使用者定義泛型也成立        (no stray spaces)
```

Getting this wrong is invisible in the PO file and visible on the published page.

## Choosing between `\\ ` and a plain space

**The choice depends on what the role renders as, not on what surrounds it.**

Work out what the reader will see: for `` :role:`display <target>` `` that is the
display text; otherwise it is the target itself. Then:

| Renders as | Separator | Why |
|---|---|---|
| Latin | a normal half-width space | The rendered text is Latin, so ordinary CJK-Latin spacing applies. `\\ ` would suppress the space that belongs there. |
| Chinese | `\\ ` on both sides | Chinese needs no space, but reST still requires whitespace around inline markup. `\\ ` supplies it at zero width. |

```
並以 :func:`asyncio.set_event_loop` 將其重設          ← renders "asyncio.set_event_loop": Latin
如果 *file* 被省略或為 ``None``，此函式將印出            ← renders "None": Latin
必須是\\ :term:`可雜湊的 <hashable>`\\ 或不可變的        ← renders "可雜湊的": Chinese
這對\\ :ref:`使用者定義泛型 <user-defined-generics>`\\ 也是成立的
```

The same test applies to emphasis: `*future*` renders Latin and takes spaces;
`*任務*` renders Chinese and takes `\\ ` where a separator is needed at all.

Note that translating a role's display text changes the answer. Turning
`` :term:`hashable` `` into `` :term:`可雜湊的 <hashable>` `` flips it from spaces
to `\\ ` in the same edit.

## Separators around full-width punctuation

reST allows inline markup to be followed directly by closing and terminal
punctuation, but not by an opening bracket. Full-width punctuation inherits that
distinction:

| Neighbour | Separator | Example |
|---|---|---|
| `，` `。` `）` `；` `：` `！` `？` | none | ``印出到 :data:`sys.stdout`。`` |
| `（` `「` `『` `《` | `\\ ` | ``借自元組 *p*\\ （也就是說：…）`` |

A separator before `，` or `。` is the most common over-application; reviewers strip
it routinely.

## Inline roles

Roles are preserved exactly. Only a role's *display text* is ever translated.

```
msgid  "Avoids tests using :func:`type` or :func:`isinstance`."
msgstr "避免使用 :func:`type` 或 :func:`isinstance` 進行測試。"
```

Roles seen in these docs: `:mod:` `:func:` `:class:` `:meth:` `:attr:` `:data:`
`:exc:` `:term:` `:ref:` `:pep:` `:rfc:` `:keyword:` `:kbd:` `:mimetype:`
`:c:func:` `:c:data:` `:c:type:` `:c:member:` `:c:macro:`.

A leading `!` (`` :meth:`!__init__` ``) suppresses the link — keep it.

## Cross-references with display text

`:term:` and `:ref:` take `display <target>`. The target stays English; the display
text is translated. **A space is required before `<`** — omitting it is a frequent
correction.

```
msgid  "Returns a :term:`context manager`."
msgstr "回傳一個\\ :term:`情境管理器 <context manager>`。"
```

Never translate the part inside `<>`. That is the lookup key.

To gloss the term on first use, put the English inside the display text rather than
outside the role:

```
執行\\ :term:`協程 (coroutine) <coroutine>` *coro* 以及回傳結果
```

## Hyperlinks

The URL and reference name are preserved; only the label is translated. For a named
reference, convert it to the explicit form so the label can be Chinese:

```
msgid  "`Documentation bugs`_ on the Python issue tracker"
msgstr "Python issue tracker 上\\ `文件的錯誤 <Documentation bugs_>`_"
```

Inline URLs keep their target untouched:

```
msgstr "請造訪 `Python 網站 <https://python.org>`_。"
```

## Inline literals

Double backticks are code formatting and must survive translation. Replacing
`` ``False`` `` with `"False"` loses the code style and is caught in review. In the
PO file an escaped quote is `\"`, which is not a substitute for a literal.

## Literal blocks and `::`

`::` at the end of a paragraph does two things: render a colon, and mark the next
indented block as code. The code block itself never appears in the PO file — only
the paragraph introducing it.

**Match the msgid in both directions.**

```
msgid  "Here is a code example::"          msgstr "以下是個程式範例： ::"
msgid  "using the :func:`.round` on it:"   msgstr "對它使用 :func:`.round` 函式："
```

Adding `::` where the msgid has a plain colon introduces a literal block with
nothing to fill it, producing a build warning and a broken layout.

## Code, comments, and doctests

| In the msgid | In the msgstr |
|---|---|
| Identifiers, keywords, dunders, exception names | unchanged |
| Inline literals and code samples | unchanged |
| `#` comments inside example code | translated |
| Docstrings and strings a doctest displays | unchanged |
| Option and environment-variable names | unchanged |

## Multi-line msgstr and line width

Lines cap at 79 characters. Long values use the empty-first-line form:

```
msgstr ""
"命名空間的例子有：內建名稱的集合（包含如 :func:`abs` 的函式，和內建的例外"
"名稱）、一個模組中的全域名稱、和一個 function 呼叫中的區域名稱。"
```

Do not wrap by hand — `make wrap` (powrap) produces the canonical wrapping.
Wrapping never inserts whitespace: segments concatenate verbatim, so a break must
not fall where a space is semantically required.

## Flags: fuzzy and others

```
#, fuzzy
msgid "Original text"
msgstr "需要人工確認的翻譯"
```

`#, fuzzy` means "do not ship this". It is set automatically when upstream English
changes under an existing translation, and can be set by hand to mark uncertainty.

- Resolving a fuzzy entry means fixing the text **and deleting the flag**.
- `make fuzzy` lists them.
- With other flags on the line (`#, fuzzy, python-format`), remove only `fuzzy`.
