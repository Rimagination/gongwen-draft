# Punctuation Style

Use this reference when drafting, revising, or linting formal Chinese official-style documents.

## Sources

Primary standards:

- GB/T 15834-2011 `标点符号用法`: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=22EA6D162E4110E752259661E1A0D0A8
- GB/T 9704-2012 `党政机关公文格式`: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=F3CC9BEF482524C895FDA7A08BB4A70E

Practical public-document interpretation:

- 共产党员网《公文写作中这些标点，你用对了吗？》: https://www.12371.cn/2022/03/11/ARTI1646954732079542.shtml
- 共产党员网《复杂情况下的标点符号用法，都是你想问的》: https://www.12371.cn/2020/04/27/ARTI1587993655418449.shtml

## General Rule

Use Chinese full-width punctuation in Chinese prose: `，。；：？！、（）“”‘’《》〈〉〔〕——……·`.

Do not use English or half-width punctuation in Chinese sentences, except for necessary technical tokens such as URLs, email addresses, file paths, code identifiers, version numbers, chemical formulas, model numbers, foreign-name initials, or the GB/T 9704 hierarchy marker `1.`.

## Colon

Use the Chinese full-width colon `：`.

Use a colon when a prompt phrase clearly introduces following content:

- `现将有关事项通知如下：`
- `具体要求如下：`
- `附件：1. ××工作方案`
- `各有关单位：`
- `签发人：张三`

Do not use the English colon `:` in Chinese prose or public-document elements. YAML front matter and code blocks are technical exceptions.

Do not use a colon after `附件1` on the actual attachment page. Attachment page headings are `附件1`, `附件2`; attachment descriptions in the main document use `附件：`.

Do not overuse colons to connect long explanations. If the following content is a complete sentence rather than an introduced list/explanation, prefer comma, semicolon, or period.

## Quotation Marks

Use curved Chinese quotation marks:

- Outer quotation: `“……”`
- Nested quotation: `“……‘……’……”`

Do not use straight English quotes `"..."` or `'...'` in Chinese prose.

Use quotation marks for direct quotation, special terms, emphasized discussion objects, or shortened names inside explanatory parentheses:

- `（以下简称“专项行动”）`
- `“五四”以来的话剧`

For document names, book names, newspapers, journals, regulations, programs, and columns, use book-title marks `《》`, not quotation marks:

- `《党政机关公文格式》`
- `关于印发《××管理办法》的通知`

If the quoted content is an independent sentence, put the terminal punctuation inside the closing quotation mark. If the quoted content is only part of the sentence, put the sentence punctuation outside.

## Hierarchy Numbering

Follow GB/T 9704-2012 hierarchy markers:

- First level: `一、`
- Second level: `（一）`
- Third level: `1.`
- Fourth level: `（1）`

Do not write `（一）、`, `1、`, or `（1）、`.

When a heading is on a separate line, do not end it with `。`, `；`, `：`, `！`, or `？`. If a second-level heading is immediately followed by body text in the same paragraph, it may use a period before the body text: `（一）完善工作机制。各单位要……`

## Public-Document Hotspots

- 发文字号年份 uses six-angle brackets: `〔2026〕`; not `[2026]`, `（2026）`, or `〖2026〗`.
- 主送机关/抄送机关: same system and same level usually use `、`; different systems usually use `，`.
- 公文标题 generally does not use punctuation. Use `《》` only when a law, regulation, rule, newspaper, journal, book, or similarly named work/file must be marked.
- Ending formulas such as `特此通知。` and `特此公告。` should end with punctuation. `妥否，请批示。` uses comma, not question mark.
- Attachment descriptions use `附件：`; attachment names do not end with punctuation.
- Parallel quoted items or book-title-marked items usually do not use顿号 between them: `“定盘星”“指南针”“压舱石”`; `《红楼梦》《三国演义》`.

## Review Priority

Treat these as high-signal checks before exporting Word:

1. English/half-width punctuation in Chinese prose.
2. Wrong hierarchy markers.
3. Wrong发文字号 brackets.
4. Attachment colon errors.
5. Misplaced punctuation around quotes.
6. Misused顿号 between quoted or book-title-marked parallel items.
