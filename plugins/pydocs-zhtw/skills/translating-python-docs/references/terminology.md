# Terminology

## Contents

- Precedence: which source wins
- Core terms
- Terms that stay in English
- Terms with more than one accepted rendering
- zh_CN forms that get flagged in review
- Known conflicts between sources

## Precedence: which source wins

When two sources disagree, use this order. Only the first is enforced by CI.

1. **`poglossary.yml`** in the repo root — what `poglossary` actually checks.
2. **`glossary.po`** — the translated official glossary; authoritative for any term
   that has a glossary entry.
3. **Surrounding file** — an established rendering in the file you are editing beats
   a table. Consistency within a page matters more than global uniformity.
4. **`focused_terminology_dictionary.csv`** / this file — a starting point.

This table is a head start, not a ruling. If `poglossary` disagrees with it,
`poglossary` is right and this file needs updating.

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
| return | 回傳 |
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
| condition | 條件 |
| prompt | 提示字元 |
| bytecode | 位元組碼 |
| docstring | 說明字串 |
| annotation | 註釋 |
| metaclass | 元類別 |
| abstract base class | 抽象基底類別 |
| special method | 特殊方法 |
| extension module | 擴充模組 |
| file object | 檔案物件 |
| list comprehension | 串列綜合運算 |
| duck-typing | 鴨子型別 |
| deprecated | 已棄用 / 被棄用 |
| lexical analyzer | 詞法分析器 |

## Terms that stay in English

High-frequency names whose Chinese rendering makes Python writing *harder* to read.
The glossary keeps these in English and annotates the common translation.

`int` `float` `str` `bytes` `list` `tuple` `dict` `set` `iterator` `generator`
`iterable` `pickle` `lambda` `token` `tokenizer` `def` `async` `await` `None`
`True` `False` and every other keyword, every dunder (`__init__`, `__iter__`, …),
and every exception class name (`ValueError`, `TypeError`, …).

Proper nouns are also left alone: `CPU`, `Unicode`, `HTML`, `PSF`.

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

Running text in this project frequently keeps `class`, `method`, `module`, and
`instance` in English mid-sentence — "一個 method 在它被連結後隨即被呼叫". That is
the house style, not an oversight.

## zh_CN forms that get flagged in review

The most common source of review churn. Left column is Mainland usage.

| zh_CN | zh_TW |
|---|---|
| 函數 | 函式 |
| 返回 | 回傳 |
| 對象 | 物件 |
| 類 | 類別 |
| 模塊 | 模組 |
| 字符串 | 字串 |
| 數組 | 陣列 |
| 變量 | 變數 |
| 調用 | 呼叫 |
| 語句 | 陳述式 |
| 表達式 | 運算式 (regex 例外) |
| 標識符 | 識別符 |
| 迭代 | 疊代 |
| 生成器 | 產生器 |
| 異常 | 例外 |
| 默認 / 缺省 | 預設 |
| 支持 | 支援 |
| 信息 | 資訊 |
| 數據 | 資料 |
| 數據庫 | 資料庫 |
| 文件 (meaning *file*) | 檔案 |
| 庫 | 函式庫 |
| 包 | 套件 |
| 內存 | 記憶體 |
| 進程 | 行程 |
| 線程 | 執行緒 |
| 網絡 | 網路 |
| 服務器 | 伺服器 |
| 客戶端 | 用戶端 |
| 接口 | 介面 |
| 指針 | 指標 |
| 隊列 | 佇列 |
| 棧 | 堆疊 |
| 哈希 | 雜湊 |
| 緩存 | 快取 |
| 打印 | 印出 |
| 循環 | 迴圈 |
| 兼容 | 相容 |
| 優化 | 最佳化 |
| 配置 | 設定 |
| 質量 | 品質 |

`列表` is a deliberate exception — it is one of the accepted renderings of `list`
in this project and must not be "corrected".

## Known conflicts between sources

- **`import`** — `focused_terminology_dictionary.csv` says 引入;
  `poglossary.example.yml` marks it `import  # no trans`. Follow the repo's own
  `poglossary.yml`, and keep `import` in English when it names the statement.
- **`annotation`** — 註釋 in the dictionary, but 註記 and 標註 both appear in the
  wild. Match the file.

When a conflict costs more than a minute, mark the entry `#, fuzzy` and move on.
