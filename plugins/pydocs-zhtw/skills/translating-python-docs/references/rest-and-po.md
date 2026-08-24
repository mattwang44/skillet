# reST and PO mechanics

Everything the msgstr has to satisfy at once. Source of truth is `README.rst` in
python-docs-zh-tw (翻譯守則 / reST 語法注意事項) plus the existing translations.

## Contents

- Escaping: why `\\ ` has two backslashes
- Inline roles
- Cross-references with display text
- Hyperlinks
- Literal blocks and `::`
- Multi-line msgstr and line width
- Flags: fuzzy and others
- What never gets translated

## Escaping: why `\\ ` has two backslashes

A `msgstr` value is a C string. gettext decodes escape sequences when reading it,
so the file must contain `\\ ` for the decoded string to contain `\ `, which is
what reST sees as a zero-width separator.

```
file contains:      msgstr "如同在\\ :ref:`tut-object`\\ 的討論"
gettext decodes to: 如同在\ :ref:`tut-object`\ 的討論
reST renders:       如同在tut-object的討論      (no stray spaces)
```

Getting this wrong is invisible in the PO file and visible on the published page.

Place a separator on every side where Chinese abuts reST markup — before and after.

## Inline roles

Roles are preserved exactly. Only a role's *display text* is ever translated.

```
msgid  "Avoids tests using :func:`type` or :func:`isinstance`."
msgstr "避免使用 :func:`type` 或 :func:`isinstance` 進行測試。"
```

Note the half-width spaces around the roles here — the neighbours are Latin, so
normal CJK-Latin spacing applies and no `\\ ` is needed.

Roles seen in these docs: `:mod:` `:func:` `:class:` `:meth:` `:attr:` `:data:`
`:exc:` `:term:` `:ref:` `:pep:` `:kbd:` `:mimetype:` `:c:func:` `:c:data:`
`:c:type:` `:c:member:` `:c:macro:`.

A leading `!` (`:meth:`!__init__``) suppresses the link — keep it.

## Cross-references with display text

`:term:` and `:ref:` take `display <target>`. The target stays English; the display
text is translated.

```
msgid  "Returns a :term:`context manager`."
msgstr "回傳一個\\ :term:`情境管理器 <context manager>`。"
```

Never translate the part inside `<>`. That is the lookup key.

## Hyperlinks

The URL and the reference name are preserved; only the label is translated. For a
named reference, convert it to the explicit `label <target_>`_ form so the label can
be Chinese:

```
msgid  "`Documentation bugs`_ on the Python issue tracker"
msgstr "Python issue tracker 上\\ `文件的錯誤 <Documentation bugs_>`_"
```

Inline URLs keep their target untouched:

```
msgid  "Visit the `Python website <https://python.org>`_."
msgstr "請造訪 `Python 網站 <https://python.org>`_。"
```

## Literal blocks and `::`

`::` at the end of a paragraph means two things: render a colon, and treat the next
indented block as code. The code block itself is not in the PO file — only the
paragraph that introduces it.

```
msgid  "Here is a code example::"
msgstr "以下是個程式範例： ::"
```

Full-width colon, one half-width space, then `::`. Both parts are required.

## Multi-line msgstr and line width

Lines cap at 79 characters. Long values use the empty-first-line form:

```
msgstr ""
"命名空間的例子有：內建名稱的集合（包含如 :func:`abs` 的函式，和內建的例外"
"名稱）、一個模組中的全域名稱、和一個 function 呼叫中的區域名稱。"
```

Do not wrap by hand. `make wrap` (powrap) produces the canonical wrapping; hand
wrapping creates diff noise when it later reflows.

Wrapping never inserts whitespace — the segments are concatenated verbatim, so a
break must not fall where a space is semantically required.

## Flags: fuzzy and others

```
#, fuzzy
msgid "Original text"
msgstr "需要人工確認的翻譯"
```

`#, fuzzy` means "do not ship this". It is set automatically when the upstream
English changes under an existing translation, and can be set by hand to mark
uncertainty.

- Resolving a fuzzy entry means fixing the text **and deleting the flag**.
- `make fuzzy` lists them.
- Other flags on the same line (`#, fuzzy, python-format`) — remove only `fuzzy`.

Comment prefixes, for reference: `#.` extracted from source, `#:` source location,
`#,` flags, `#` translator's own note. Only `#` notes and `#,` flags are yours to
edit.

## What never gets translated

- Anything inside double backticks: `` ``int`` ``, `` ``zip(*[iter(x)]*n)`` ``
- Role targets and reference labels inside `<>`
- URLs
- Python keywords, dunder names, exception class names
- Option and environment-variable names
