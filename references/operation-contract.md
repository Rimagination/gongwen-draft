# Operation Contract

Use this reference when turning a user request into a repeatable workflow, especially for file outputs.

## Quick Command Shapes

These are ergonomic command patterns, not a separate CLI:

- `/gongwen draft 通知 <topic>`: draft a notice.
- `/gongwen draft 请示 <topic>`: draft a request for approval.
- `/gongwen draft 报告 <topic>`: draft a report.
- `/gongwen review <draft>`: review type, authority, facts, structure, language, format, and confidentiality.
- `/gongwen collect <materials>`: build a material dossier and fact ledger before drafting.
- `/gongwen policy <topic>`: build a policy-research ledger before drafting.
- `/gongwen polish <draft>`: improve language while preserving facts and authority boundaries.
- `/gongwen export <draft.md>`: lint, check fonts, and export Word.
- `/gongwen format`: explain current formatting rules and required fonts.

Normal Chinese requests should work without these commands. Treat them as a compact user shorthand.

## Work Modes

### Quick Draft

Use when the user wants a usable text answer now. Ask only if missing facts would cause wrong文种, false authority, or invented facts. Otherwise draft with placeholders.

### Formal Draft

Use when the user asks for a serious公文 or Word file. Build a fact ledger, route the文种, preserve required elements, and run lint before export.

### Material Dossier

Use when the user provides multiple files, pasted notes, public excerpts, or a vague topic with raw materials. Prepare a source table, confirmed-looking facts, judgment/claim lines, and focused confirmation questions before drafting. Use `scripts/prepare_dossier.py` for local text files.

### Policy Research

Use when the draft depends on current policy, laws, department rules, official statistics,领导讲话, or meeting communiques. Build a policy ledger with `scripts/policy_research.py`, verify official sources manually or through browser/search tools, then run `scripts/check_citations.py --require-citations` before drafting.

### Review / Rewrite

Lead with risks and actionable fixes. Cover:

- 文种与行文方向
- 发文权限 and policy basis
- facts, names, numbers, dates, quotations
- structure and execution information
- language, hierarchy numbering, format, confidentiality

For language-only polishing, use the lightest mode from `references/language-polishing.md`: normalize, tighten, formalize, de-risk, or rebuild. Never polish by inventing facts or stronger conclusions.

### Export

Use controlled Markdown or JSON spec, then:

1. `scripts/render_spec.py spec.json -o draft.md` if input is JSON.
2. `scripts/check_citations.py draft.md` when the draft includes policy/current-source claims.
3. `scripts/check_sections.py <doc-type> draft.md`.
4. `scripts/check_fonts.py --draft draft.md`.
5. `scripts/generate_docx.py draft.md -o output.docx --doc-type <doc-type> --install-font-assets`.

## Source Modes

- Online/current-policy mode: verify current policies, standards, dates,领导讲话, and facts from official sources before writing them as facts. Keep a citation ledger and run the citation checker when sources are provided.
- Offline mode: use only user-provided materials and local references. Mark unverified claims as `待核实`.
- Mixed mode: facts from user materials remain user-supplied; official/current claims still require verification.

## Material Boundary

Keep business materials for a deliverable in the same working folder as the draft whenever possible:

- `task.md`: user's task and constraints.
- `materials.md`: confirmed source facts and excerpts.
- `dossier.md`: optional source table, fact ledger, claims, and confirmation questions for messy inputs.
- `draft.md`: controlled Markdown.
- `output.docx`: generated Word file.

Do not silently read unrelated directories for facts. If a file path is outside the deliverable folder, mention it and use only when the user supplied or authorized it.

## Versioning

Do not overwrite generated deliverables by default. If `output.docx` exists, create `output-v02.docx`, then `output-v03.docx`. Use `--overwrite` only on explicit user instruction.

## Community Influence

This contract absorbs:

- command ergonomics from `cycleuser/Skills@official-document-writer`;
- source/material discipline, non-overwrite outputs, and tests from `zhaohui-yang/official-document-drafting`;
- controlled Markdown/JSON discipline from `wzbwan/gongwen-format-skill` and `Likenttt/gongwen-writing-formatting`;
- compact review/checklist and language-style habits from `KaguraNanaga/official-document-writing-skill` and `Aether-liusiqi/wenshu`;
- policy-source caution from `luan-78-zao/official-document-writer-skill`, while requiring verification and warning about incorrect standard-year claims.
