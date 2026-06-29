# Project Lessons

This file summarizes public projects inspected from the user's `gongwen-writing` GitHub search and nearby stronger projects. Use it as engineering guidance, not as authoritative writing source text.

## Inspected Projects

| Project | Useful pattern | Caution |
| --- | --- | --- |
| `HenryLau7/gongwen-writing` | Clear input handling: text/Word/PDF -> suggest文种 -> confirm -> draft/export; strong red-line warnings against fake official documents. | Very small; some workflow assumes external office tools. |
| `sunnydayplease668/gongwen-writing` | Reference-rich skill from extracted book/material rules; five anchors: purpose, audience, facts, structure, tone; good boundary language. | Source book/material authority must be checked before treating rules as normative. |
| `farmer-data/gongwen-writing` | Four-step定位法: 文种, 行文方向, 格式, 套语; good common-mistake framing and examples. | Some date-style notes conflict with GB/T 9704-2012 practice; use official/current rules first. |
| `wocessade/gongwen-writing-skill` | Pipeline thinking: G0 文种确认, G1 规划, G2 起草, G3 审查, G4 修订; staged lint/docx tooling. | Depends on a larger shared framework; keep `gongwen-draft` self-contained. |
| `Right-068/gongwen-writing-suite` | Fact ledger, boundary confirmation, three-round review, workflow/filing awareness, safety around sensitive materials. | Keep output concise; do not overburden simple tasks with full process ceremony. |
| `Likenttt/gongwen-writing-formatting` | Deliverable-first question, JSON spec -> deterministic Word/PDF generation, existence checks. | PDF support needs environment-specific tooling; `gongwen-draft` currently focuses on `.docx`. |
| `gzfutureai/mcp-server-moke-gongwen` | MCP framing: templates, compliance verification, contextual requirement analysis, style optimization. | Repository is README-only; treat as concept, not implementation. |
| `liaoxuyean/official-document-writer` | Compact command-style coverage of 15 document types, format elements, hierarchy numbering, common mistakes. | Mostly static rules, less source provenance and no scripts. |
| `zhaohui-yang/official-document-drafting` | Best engineering reference: doc-type specs, core guardrails, source/material workflow, examples, tests, scripts, output conventions. | Do not copy long prose; mirror the discipline and routing model. |
| `KaguraNanaga/official-document-writing-skill` | High-attention static skill with useful template/checklist coverage and readable GB/T 9704 summaries. | Static guidance alone is not enough; keep deterministic lint/export scripts in `gongwen-draft`. |
| `Aether-liusiqi/wenshu` | Compact 15+7 coverage, examples, language taboos, section checks, and docx export. | Avoid over-optimizing for "笔杆子" flourish; `gongwen-draft` should prefer restrained official clarity. |
| `hehecat/gongwen` | Real user-facing expectation: A4 preview, import, pagination, and DOCX export should feel visible and inspectable. | A full frontend/PWA is out of scope for this portable skill; borrow constants and verification habits only. |
| `linhut/document-ai-assistant` | Large app lessons: template management, font validation, preview/download error handling, document parsing, and style detection. | Do not import an Electron/backend stack into a skill; absorb validation and template ideas selectively. |
| `cycleuser/Skills@official-document-writer` | Quick command ergonomics and concise registry-style packaging. | Some rules are compact to the point of oversimplification; keep source hierarchy and scripts. |
| `luan-78-zao/official-document-writer-skill` | Useful idea: policy-source retrieval before writing source-sensitive请示/报告. | Mentions `GB/T 9704-2022`, conflicting with GB/T 9704-2012; treat as a cautionary example and lint this error. |

## Shared Strengths To Preserve

- Trigger on both `公文写作` and concrete文种 names, not just the English repository name.
- Confirm or infer文种 before drafting; correct common confusions such as 请示/报告, 通知/函, 公告/通告, 批复/复函.
- Use a fact ledger and placeholders instead of inventing facts.
- Separate drafting, review, formatting, export, and training tasks.
- Treat `.docx` generation as deterministic helper work after content is structurally clean.
- Include local linting for high-risk mistakes: report with approval requests, 请示报告混用, placeholders, Markdown artifacts, weak dates, vague terms.
- Keep output user-practical: give a usable draft first, then only the necessary assumptions and risks.

## Zhaohui Reference Practices To Adopt

- Maintain one source of truth for routing and workflow. Avoid duplicating conflicting rules across files.
- Distinguish `必备`, `常见`, `条件项`, `地方或系统样式`, and `项目自定义`; do not present local/unit customs as national requirements.
- Use `materials.md`-style thinking: separate source materials from generated drafts and note where facts came from.
- For network/current-policy tasks, verify official sources and dates before drafting.
- For offline tasks, rely only on user-provided or saved local materials; mark missing facts as `待核实`.
- Prefer complete structures for formal drafts, then let the user delete; do not drop主送、落款、日期 merely because facts are missing.
- Use default output directories and non-overwrite naming when producing files.
- Use controlled Markdown/JSON as the contract between drafting logic and formatting scripts.
- Treat font validation as a hard gate, not a best-effort warning.
- Hide first-page page numbers by default and make odd/even page placement configurable.
- Preserve quick command ergonomics without making them the only way to trigger the skill.

## Differentiators To Keep Improving

- Keep the user-facing README short and practical even as engineering depth grows.
- Treat all 15 statutory公文 and 8 common formal-material categories as first-class templates, not partial fallbacks.
- Use `scripts/check_type_consistency.py` as a release gate whenever document-type support changes.
- Use `scripts/prepare_dossier.py` to make messy素材 usable before drafting, instead of only relying on prompt instructions.
- Use `scripts/policy_research.py` and `scripts/check_citations.py` so source-sensitive drafts move through official-source research before writing.
- Use `scripts/check_language.py` to support润色 as a verifiable review surface, not just a style promise.
- Keep stricter punctuation and font gates than most static skills: fail loudly on missing fonts and flag English punctuation in Chinese prose.
- Provide an offline prompt-pack generator without requiring a large generated `dist/` tree in the portable skill package.
- Preserve explicit community citations while making official standards and user unit templates the higher authority.

## Rules Not To Adopt Blindly

- Do not require user confirmation at every step for simple drafting; ask only when missing facts would cause fabrication or wrong文种.
- Do not use ornate paired headings as a default. Operational clarity beats decoration.
- Do not claim a generated `.docx` is formally compliant enough to issue; unit templates and human review remain required.
- Do not mix mainland公文 rules with Taiwan, legal pleading, marketing, or literary-writing systems.
- Do not accept a project's stated standard year blindly; flag `GB/T 9704-2022` as suspicious unless a user provides a valid current source.
