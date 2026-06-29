# Policy Research Workflow

Use this reference when a draft depends on current policy, laws, department rules,领导讲话, meeting communiques, or any statement that could become a false authority if outdated or unsourced.

## Goal

Draft only after finding and checking usable sources. The expected sequence is:

1. 先查：find current official sources.
2. 先核：record title, issuing body, document number, date, URL, scope, and citation status.
3. 再写：write only from verified sources and user-confirmed facts.

## Source Classes

### Can be used as policy basis

- 中国政府网、国务院公报、国务院部门官网.
- 国家法律法规数据库、全国人大网、政协网、纪检监察机关官网.
- 地方人民政府及其部门官网, when the document applies to the user's jurisdiction.
- 党内公开发布平台 such as 共产党员网、求是网、党建网, when the item is an official public release or verified学习材料.
- User-provided unit rules, meeting decisions, and approved templates, when the user confirms they are current and applicable.

### Can be used as background or discovery leads

- 人民日报、新华社、央视、光明日报、半月谈 and similar authoritative media.
- Government WeChat accounts, when they repost or explain official material.
- Training articles, public writing guides, and community projects.

These sources can improve wording or reveal a policy lead, but should not replace the official original document in正文依据.

### Do not use as policy basis

- Search snippets, copied excerpts without URLs, social-media reposts, SEO articles, courseware, forum posts, GitHub projects, and AI-generated summaries.
- Any source missing issuer, date, title, or stable URL.
- Old documents that may have been amended, repealed, or superseded.

## Research Procedure

1. Identify the policy-sensitive claims:
   - “根据……”
   - “依据……”
   - “贯彻落实……”
   - “按照……要求”
   - “领导讲话精神”
   - “会议精神”
   - statutory duties, funding rules, approval authority, penalties, standards, statistics, and mandatory deadlines.
2. Build a policy ledger with `scripts/policy_research.py --topic "<topic>" -o policy-ledger.md`.
3. Search official sources first. Use search engines only to locate official pages; open the original page before treating it as evidence.
4. Record each source in the ledger:
   - title
   - issuing body
   - document number, if any
   - publish date
   - URL
   - source class: policy original, law/regulation, official interpretation, leadership speech, meeting communique, background only
   - citation decision: cite as basis, mention as background, use as wording lead, reject
5. Run `scripts/check_citations.py policy-ledger.md --require-citations`.
6. Draft from the verified ledger. Do not pull additional policy claims from memory.
7. If official sources conflict, stop and surface the conflict instead of choosing silently.

## Leadership Speech Rules

- Use only official releases, official transcripts, or official news pages.
- Record speaker, occasion, date, publisher, URL, and whether the wording is a direct speech, meeting summary, or media report.
- Do not write “重要指示精神”“讲话精神” unless the source actually supports that formulation.
- If the source is a media report without official original text, mark it as background or待核实.

## Citation Ledger Shape

Use this table shape for serious drafts:

| 编号 | 文件或讲话标题 | 发布机关 | 文号 | 发布日期 | 来源URL | 来源等级 | 写入正文方式 | 核验状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | [标题] | [机关] | [文号或无] | [日期] | [官方URL] | 政策原文/法律法规/讲话原文/政策解读/背景材料 | 作为依据/作为背景/仅作线索/剔除 | 已核实/待核实 |

## Drafting Rules After Research

- A policy original can support “根据……”.
- An official interpretation can support understanding and wording, but should not replace the original document when the original is available.
- Authoritative media can support “据新华社报道”等背景句, not a formal制度依据.
- If no official basis is found, use placeholders such as `[政策依据待核实]` or ask the user to provide the applicable文件.
- Keep source wording short. Paraphrase policy requirements unless the exact phrase is necessary and supplied by a verified source.

## Citation Checker

Run:

- `scripts/check_citations.py <policy-ledger.md> --require-citations` for policy ledgers.
- `scripts/check_citations.py <draft.md>` before exporting high-stakes drafts.
- Add `--allow-media` only when the task explicitly permits authoritative media as background material.

The checker flags:

- non-official URLs used as policy basis;
- authoritative media used without explicit background treatment;
- official source rows missing publish date or issuer;
- policy-sensitive text with no URL;
- suspicious `GB/T 9704-2022` claims.
