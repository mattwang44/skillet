# Terminology

Counts in this file are how many times reviewers had to make that correction across
three years of PRs. They are a priority signal, not a complete list.

## Contents

- The lookup ladder
- Style rules
- Core terms
- Terms that stay in English
- Terms with more than one accepted rendering
- Forms reviewers strip
- Word senses that get taken wrongly
- Known conflicts between sources

## The lookup ladder

Terminology dominates review discussion. Walk this in order, stop at the first hit,
and do not invent a rendering.

1. **`poglossary.yml`** in the repo root — the only source CI enforces
2. **`glossary.po`**, or <https://docs.python.org/zh-tw/3/glossary.html>
3. **The file you are editing**, then the rest of the repo:
   `grep -rn "<term>" --include=*.po .`
4. **[術語列表 Wiki](https://github.com/python/python-docs-zh-tw/wiki/%E8%A1%93%E8%AA%9E%E5%88%97%E8%A1%A8)** — cited in 73 review comments
5. **[樂詞網 / 國家教育研究院](https://terms.naer.edu.tw/)** — cited in 24
6. **Nothing established → keep the English.**

Step 6 is the house answer, not a cop-out. Maintainers say it plainly:

> 任何相關翻譯都不通用
> 直接放原文我比較好受
> 太多東西能翻成模擬了，目前翻譯都是留原文的狀態

When keeping English for a term a reader may not know, gloss it at its **first
occurrence in the page**: 正規表示式 (regular expression).

Consistency inside a file outranks every table here. 222 review comments are some
form of "前面翻成 X，這邊也用 X".

## Style rules

| Rule | Count |
|---|---|
| 您 → 你. The project does not use the honorific. | 10 |
| Chinese-first, English in half-width parens: `協程 (coroutine)`, not the reverse | 42 |
| Gloss only at the term's first occurrence in the page, not later ones | — |
| No `，` before 和 / 或 in a short list: ``` ``'a'`` 或 ``'b'` ``` , not ``` ``'a'``，或 ``` | — |

## Core terms

| English | zh_TW |
|---|---|
| argument | 引數 |
| parameter | 參數 |
| attribute | 屬性 |
| class | 類別 |
| function | 函式 |
| method | 方法 |
| module | 模組 |
| package | 套件 |
| object | 物件 |
| type | 型別 |
| instance | 實例 |
| statement | 陳述式 |
| expression | 運算式 |
| exception | 例外 |
| raise | 引發 |
| return | 回傳 |
| protocol | 協定 |
| create | 建立 |
| import | 引入 |
| escape | 跳脫 |
| exit | 結束 |
| constructor | 建構函式 |
| delegate | 委派 |
| keyword-only | 僅限關鍵字 |
| interpreter | 直譯器 |
| iterate | 疊代 |
| iterator | 疊代器 |
| generator | 產生器 |
| decorator | 裝飾器 |
| descriptor | 描述器 |
| closure | 閉包 |
| callback | 回呼 |
| namespace | 命名空間 |
| sequence | 序列 |
| mapping | 對映 |
| slice | 切片 |
| loop | 迴圈 |
| operator | 運算子 |
| operand | 運算元 |
| element | 元素 |
| index | 索引 |
| newline | 換行字元 |
| annotate | 註釋 |
| comment | 註解 |
| mark | 標記 |
| evaluation | 計算 / 給值 / 求值 |
| bytecode | 位元組碼 |
| docstring | 說明字串 |
| metaclass | 元類別 |
| abstract base class | 抽象基底類別 |
| special method | 特殊方法 |
| extension module | 擴充模組 |
| file object | 檔案物件 |
| list comprehension | 串列綜合運算 |
| duck-typing | 鴨子型別 |
| deprecated | 已棄用 / 被棄用 |

`annotate` → 註釋 and `comment` → 註解 are deliberately different words. Do not
collapse them.

## Terms that stay in English

High-frequency names whose Chinese rendering makes Python writing harder to read:

`int` `float` `str` `bytes` `list` `tuple` `dict` `set` `iterator` `generator`
`iterable` `pickle` `lambda` `token` `tokenizer` `socket` `stub` `runtime`
`def` `async` `await` `None` `True` `False`, every other keyword, every dunder,
and every exception class name.

Also left alone: proper nouns (`CPU`, `Unicode`, `HTML`, `PSF`) and terms with no
settled Chinese form — `partial function` and `capturing group` are both live
examples where review concluded "keep the English".

`runtime` is worth calling out: 執行期 and 執行時 were both corrected back to
`runtime` in review.

## Terms with more than one accepted rendering

`poglossary.yml` maps these to a *list*, so more than one form passes. Match the
file you are editing rather than normalizing.

| English | Accepted |
|---|---|
| class | 類別, class |
| method | 方法, method（方法）, method |
| module | 模組, module |
| list | 串列, 清單, 列表, list |
| dictionary | 字典, dictionary, dict |
| type | 型別, 種類 |
| int | 整數, int |
| float | 浮點數, float |
| boolean | 布林, boolean |
| expression | 運算式, 表達式 (regular expression 用) |

Running text frequently keeps `class`, `method`, `module`, and `instance` in English
mid-sentence — 「一個 method 在它被連結後隨即被呼叫」. That is house style, not an
oversight.

## Forms reviewers strip

Ordered by how often each was corrected. Most are Mainland usage; a few are simply
not this project's choice.

| Corrected away | Use instead | Count |
|---|---|---|
| 函數 | 函式 | 15 |
| 異常 | 例外 | 13 |
| 調用 | 呼叫 | 13 |
| 返回 | 回傳 | 13 |
| 支持 | 支援 | 11 |
| 您 | 你 | 10 |
| 拋出 | 引發 | 10 |
| 創建 | 建立 | 8 |
| 協議 | 協定 | 8 |
| 參數 (where the source says *argument*) | 引數 | 8 |
| 迭代 | 疊代 | 8 |
| 傳回 | 回傳 | 7 |
| 語句 | 陳述式 | 6 |
| 匯入 | 引入 | 5 |
| 字符串 | 字串 | 5 |
| 客戶端 | 用戶端 | 5 |
| 類型 (where a Python type is meant) | 型別 | 5 |
| 默認 / 缺省 | 預設 | 5 |
| 對象 | 物件 | 4 |
| 建構器 | 建構函式 | 4 |
| 兼容 | 相容 | 3 |
| 指針 | 指標 | 3 |
| 緩存 | 快取 | 3 |
| 進程 | 行程 | 3 |
| 轉義 | 跳脫 | 3 |
| 委託 | 委派 | 2 |
| 數據 | 資料 | 2 |
| 模塊 | 模組 | 2 |
| 生成器 | 產生器 | 2 |
| 設置 | 設定 | 2 |
| 變量 | 變數 | 2 |
| 關鍵字專用 | 僅限關鍵字 | 2 |
| 信息 | 資訊 | 1 |
| 優化 | 最佳化 | 1 |
| 接口 | 介面 | 1 |
| 服務器 | 伺服器 | 1 |
| 退出 | 結束 | 1 |
| 線程 | 執行緒 | — |
| 網絡 | 網路 | — |
| 隊列 | 佇列 | — |
| 打印 | 印出 | — |
| 標識符 | 識別符 | — |
| 內存 | 記憶體 | — |
| 質量 | 品質 | — |
| 文件 (meaning *file*) | 檔案 | — |

`列表` is a deliberate exception: one of the accepted renderings of `list`. Do not
"correct" it.

`參數` is correct for *parameter* and wrong for *argument* — it is the most
corrected single term, so check which word the msgid uses.

## Word senses that get taken wrongly

77 review comments are about a word translated by its most common sense rather than
the one in play. Check any word that could plausibly be two things:

| Word | Wrong sense taken | Sense actually meant |
|---|---|---|
| introducing | 介紹 | 引入 — a PEP introduces syntax |
| integral | 整數 | 積分 |
| function | 函式 | 功能, in non-API prose |
| active | 啟用 | 活躍, as in active user |
| complex | 複雜 | 複數, as in complex number |
| line | 行 | 列, where the file already says 列 |
| print | 顯示 | 印出 — 顯示 reads as display/show |
| canonical | 標準 | depends on context; check |

## Known conflicts between sources

- **`import`** — the focused dictionary says 引入; `poglossary.example.yml` marks it
  `import  # no trans`. Follow the repo's own `poglossary.yml`, and keep `import`
  in English when it names the statement.
- **`type`** — 型別 for a Python type object, 類型 for a general category such as
  「presentation type」. Both appear legitimately.
- **`annotation`** — 註釋 by the rule above, but 標注 appears in the wild. Match the
  file.

When a conflict costs more than a minute, mark the entry `#, fuzzy` and move on.
