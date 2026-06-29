# Community Citations

Use this file when explaining what `gongwen-draft` learned from public community projects. These projects are cited for design influence and comparison, not as authoritative legal or formatting sources. Official rules, current user-provided materials, and verified government sources remain higher authority.

## Primary Engineering References

| Project | Link | What `gongwen-draft` learned |
| --- | --- | --- |
| `zhaohui-yang/official-document-drafting` | https://github.com/zhaohui-yang/official-document-drafting | The strongest reference for engineering discipline: doc-type routing, core guardrails, source/material workflow, examples, tests, output conventions, and `.docx` export. |
| `wzbwan/gongwen-format-skill` | https://github.com/wzbwan/gongwen-format-skill | Deterministic controlled Markdown/JSON to Word generation; avoid vague Markdown inference when producing formal files. |
| `KaguraNanaga/official-document-writing-skill` | https://github.com/KaguraNanaga/official-document-writing-skill | Template/checklist orientation and practical quality review flow. |
| `Aether-liusiqi/wenshu` | https://github.com/Aether-liusiqi/wenshu | Compact 15+7 document coverage, examples, structure checking, and language taboo awareness. |
| `luan-78-zao/official-document-writer-skill` | https://github.com/luan-78-zao/official-document-writer-skill | Source-sensitive policy retrieval before drafting请示/报告; also a cautionary example because `GB/T 9704-2022` appears inconsistent with current GB/T 9704-2012 usage. |

## `gongwen-writing` Search Result Projects

| Project | Link | What `gongwen-draft` learned |
| --- | --- | --- |
| `HenryLau7/gongwen-writing` | https://github.com/HenryLau7/gongwen-writing | Input handling flow: text/Word/PDF -> identify/suggest文种 -> draft/export; strong warning against fake official documents. |
| `sunnydayplease668/gongwen-writing` | https://github.com/sunnydayplease668/gongwen-writing | Five anchors for drafting and review: purpose, audience, facts, structure, tone; useful boundary framing for reference-derived rules. |
| `farmer-data/gongwen-writing` | https://github.com/farmer-data/gongwen-writing | Four-position routing: document type, writing direction, format, language patterns; common-mistake framing. |
| `wocessade/gongwen-writing-skill` | https://github.com/wocessade/gongwen-writing-skill | Staged pipeline thinking: confirm文种, plan, draft, review, revise; lint/docx tooling as part of the pipeline. |
| `Right-068/gongwen-writing-suite` | https://github.com/Right-068/gongwen-writing-suite | Fact ledger, boundary confirmation, three-round review, workflow/filing awareness, and sensitive-material safeguards. |
| `Likenttt/gongwen-writing-formatting` | https://github.com/Likenttt/gongwen-writing-formatting | Deliverable-first question and JSON-spec-like generation flow for deterministic files. |
| `gzfutureai/mcp-server-moke-gongwen` | https://github.com/gzfutureai/mcp-server-moke-gongwen | MCP framing for templates, compliance verification, contextual requirement analysis, and style optimization. |
| `liaoxuyean/official-document-writer` | https://github.com/liaoxuyean/official-document-writer | Concise command-style coverage of document types, format elements, hierarchy numbering, and common mistakes. |

## Adjacent Tooling References

| Project | Link | What `gongwen-draft` learned |
| --- | --- | --- |
| `hehecat/gongwen` | https://github.com/hehecat/gongwen | A4 preview, parsing, DOCX export, smart pagination, and real user-facing formatter expectations. |
| `linhut/document-ai-assistant` | https://github.com/linhut/document-ai-assistant | Larger app pattern: format detection, optimization, templates, tests, font validation, preview/download error handling, and local-first document handling. |
| `kairiclabs/gejian` | https://github.com/kairiclabs/gejian | Format checking as a product surface; start with a small set of high-signal rules and expand. |
| `cycleuser/Skills` official-document-writer | https://github.com/cycleuser/Skills/tree/main/skills/official-document-writer | Concise command-style skill packaging and quick command ergonomics. |

## Citation Rules

- Cite these projects when publishing README, release notes, marketplace descriptions, or comparison notes for `gongwen-draft`.
- Do not copy long rules, examples, or prose from these projects into user-facing drafts.
- When a community rule conflicts with an official source, user-provided unit template, or verified current government source, follow the higher-authority source.
- Preserve attribution even when an idea has been rewritten into local wording.
