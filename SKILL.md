---
name: gongwen-draft
description: Draft, revise, polish, review, lint, and export Chinese党政机关公文 and政务材料 with authority-first guardrails, controlled Markdown/JSON specs, offline prompt-pack generation, strict official-document font checks, and optional Word .docx generation with generic red-head draft headers when authorized values are supplied. Use when the user asks for gongwen-draft, 公文, 公文写作, 公文起草, 机关文稿, 政务写作, 通知, 请示, 报告, 函, 纪要, 通报, 批复, 意见, 决定, 公告, 通告, 工作总结, 工作方案, 调研报告, 汇报材料, 简报, 情况专报, 讲话稿, 回复函, 材料改写, 公文润色, 格式审核, Word公文导出, 离线提示词, JSON公文规格, 红头版头, 发文机关标志, 发文字号, 签发人, or to turn notes into formal official-style Chinese documents.
---

# Gongwen Draft

Use this skill to produce practical,规范、准确、克制的中文公文和机关材料. The stable skill/repository name is `gongwen-draft`.

Treat the gathered local references as guidance, not as permission to invent facts, policies, authority, signatures, seals, dates, document numbers, or data.

## Quick Workflow

1. Identify the task: `draft`, `revise`, `review`, `format`, `template`, `extract`, `export`, or `training`.
2. Apply four-position routing: 文种 -> 行文方向 -> 格式/交付 -> 语言口径.
3. Build a fact ledger before final drafting: `已确认事实`, `用户判断`, `待核实`, `建议措辞`.
4. Check five anchors: purpose, audience, facts, structure, tone.
5. If key facts are missing, either ask 1-3 focused questions or produce a fillable skeleton with bracketed placeholders.
6. Draft with this order: define purpose -> choose文种 -> structure content -> write concise body -> self-review -> lint/export if requested.
7. For source-sensitive claims, cite or ask for the specific policy/source. Do not fabricate policy basis, statistics,领导讲话,会议精神, or official decisions.

## Load References As Needed

- For workflow routing, export behavior, and lessons absorbed from GitHub projects, read `references/engineering-workflow.md`.
- For quick command shapes, source modes, material boundaries, export sequencing, and versioning, read `references/operation-contract.md`.
- For the comparative learning summary of public `gongwen-writing` projects, read `references/project-lessons.md`.
- For explicit community project citations and what was learned from each, read `references/citations.md`.
- For the product quality bar and user expectations this skill should meet, read `references/quality-bar.md`.
- For legal/制度底线 and official document types, read `references/core-rules.md`.
- For concrete templates and section structures, read `references/document-types.md`.
- For writing method, style, revision strategy, and avoiding空心公文, read `references/writing-method.md`.
- For punctuation, colon, quotation marks, hierarchy markers, and avoiding English punctuation in Chinese prose, read `references/punctuation-style.md`.
- For reviewing an existing draft, read `references/review-checklist.md`.
- For strict公文字体 checks, official font channels, and authorized font assets, read `references/font-policy.md`.
- For controlled Markdown/JSON and Word output conventions, read `references/format-output.md`.
- For provenance of the local materials used to build this skill, read `references/source-index.md`.

## Drafting Standards

- Write from the institution's position, not the author's personality.
- Prefer facts, responsibilities, timelines, measures, and enforceable wording over slogans.
- Keep language accurate, plain, and actionable. Avoid empty排比, over-grand claims, vague adjectives, and unsupported成果.
- Use Chinese full-width punctuation in Chinese prose; follow `一、` -> `（一）` -> `1.` -> `（1）`, use `：` not `:`, and use `“”` / `‘’` not straight English quotes.
- Match文种 to行文关系: 上行 usually 请示/报告; 下行 usually 通知/通报/批复/意见; 平行 or non-subordinate usually 函.
- Keep one main matter per request when drafting请示. Do not mix report and request functions.
- Use placeholders like `[发文机关]`, `[日期]`, `[依据文件名称]` when facts are unknown.
- Preserve confidentiality: if user content appears涉密 or sensitive, warn and draft only with sanitized placeholders.
- Separate content drafting from formal issuance: do not add red headers, document numbers, signatories, seals, or approval language unless the user supplied authorized values or placeholders and the task is only preparing a draft.
- Prefer the user's current unit template over generic GB/T-style defaults when the user provides a template.

## Lint And Export

- Before exporting, form a clean Markdown draft. Avoid Markdown tables, bold markers, block quotes, and decorative bullets unless the user requested an informal reading draft.
- If using JSON spec, run `scripts/render_spec.py <spec.json> -o <draft.md>` before lint/export.
- For offline assistants or web chat tools that cannot install skills, run `scripts/build_prompt_pack.py --doc-type <doc-type> --task <task> -o <prompt.md>` and paste the generated prompt pack into the target tool.
- Run `scripts/check_sections.py <doc-type> <draft.md>` when reviewing or before file export.
- Run `scripts/check_fonts.py --verify-assets` after changing bundled fonts, then run `scripts/check_fonts.py --draft <draft.md>` before Word export. If authorized font files are in `assets/fonts`, use `--install-assets`.
- Run `scripts/generate_docx.py <draft.md> -o <output.docx> --doc-type <doc-type> --install-font-assets` when the user asks for Word output. The script creates `-vNN` files instead of overwriting unless `--overwrite` is explicit.
- Run `scripts/check_coverage.py` after changing document types, templates, README coverage language, or lint document-type lists.
- For generic红头版头 output, use controlled front matter such as `issuer_mark`, `doc_number`, and `issue_person`; never invent real机关名称、发文字号、签发人、印章 or approval status.
- Do not silently replace required公文字体 with generic fonts. If fonts are missing, stop and use official/authorized channels.
- If Python lacks `python-docx`, install or use the bundled workspace Python/libraries when available.
- Keep generated files outside the skill folder unless the user explicitly asks otherwise.
- If the user asks for a deliverable but not the format, ask whether they want Markdown, Word `.docx`, PDF, or both Word and PDF.
- Community projects inspired this workflow; cite them when explaining the design or publishing derivative project documentation.

## Output Patterns

When drafting from scratch, provide:

1. A finished draft in formal Chinese.
2. A short note listing assumptions/placeholders.
3. Optional review suggestions if the user asked for polish or compliance.

When reviewing or revising, provide:

1. Main issues by severity.
2. Revised draft or targeted edits.
3. A checklist of remaining facts the user must confirm.

When exporting, provide:

1. The generated file path.
2. Lint findings or a short "no high-risk issue found" note.
3. Placeholders or facts that still require human confirmation.

## Do Not

- Do not impersonate a real office, signatory, seal, or official approval.
- Do not invent legal basis, policy language, statistics, meeting outcomes, or document numbers.
- Do not quote long passages from reference articles. Summarize methods and cite source names where useful.
- Do not treat training articles or转载文章 as normative documents. Use official regulations and standards first.
- Do not copy another public project's long rules verbatim into outputs. Use inspected projects as engineering reference only.
- Do not remove community citations merely because a rule has been rewritten locally; provenance should remain visible.
