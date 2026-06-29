# Engineering Workflow

Use this reference when deciding how to route a `gongwen-draft` task, when generating files, or when improving the skill.

## Design Position

`gongwen-draft` combines three layers:

1. Authority-first writing: local collected sources under `D:\微信推送\公文写作资料`, with official rules first and media/training articles second.
2. Modular skill workflow: route by task and document type, read only the relevant references, and keep `SKILL.md` concise.
3. Deterministic helpers: use scripts for repeated checks and `.docx` output instead of rewriting formatting code each time.

## Lessons From Inspected GitHub Projects

- `zhaohui-yang/official-document-drafting`: strong model for task routing, doc-type specs, offline prompts, examples, tests, and Word export. Borrow the architecture idea, not the text wholesale.
- `wzbwan/gongwen-format-skill`: strong model for controlled Markdown/JSON -> `.docx` generation. Keep inputs deterministic and avoid guessing general Markdown semantics.
- `Aether-liusiqi/wenshu`: useful compact references for 15 statutory document types plus common formal materials, with structure checking and language taboos.
- `KaguraNanaga/official-document-writing-skill`: useful quality checklist and template-library orientation.
- `hehecat/gongwen` and `linhut/document-ai-assistant`: useful UI/application references, but too large for a portable skill.
- `cycleuser/Skills@official-document-writer`: useful as a concise command-style reference.
- Screenshot `gongwen-writing` results: useful common patterns include four-position routing, fact ledgers, five anchors, task modes, local linting, and deliverable-first export questions. See `project-lessons.md`.

## Routing

Classify the request:

- `draft`: create a document from facts or notes.
- `revise`: rewrite an existing draft.
- `review`: diagnose risks, wrong文种, weak facts, or format issues.
- `format`: turn content into controlled Markdown or official layout.
- `export`: generate `.docx`.
- `training`: explain rules or teach writing method.

Then classify document family:

- 15 statutory公文: 决议、决定、命令/令、公报、公告、通告、意见、通知、通报、报告、请示、批复、议案、函、纪要.
- Common formal materials: 工作总结、工作方案、调研报告、讲话稿、汇报材料、简报、情况专报、回复函.

Use this four-position question set before drafting:

1. 文种: what document type best fits the purpose?
2. 方向: 上行、下行、平行、公开发布, or internal material?
3. 格式: content only, Markdown, `.docx`, PDF, or unit template?
4. 语言: formal issuance, internal report, speech, briefing, or training explanation?

## Default Draft Pipeline

1. Confirm or infer文种 from行文关系 and purpose.
2. Read `core-rules.md`, then read `document-types.md` for the selected structure.
3. Build a fact ledger with confirmed facts, user judgments, to-verify items, and suggested wording.
4. Gather or preserve placeholders for发文机关、主送机关、依据、事实、责任、时限、落款日期.
5. Draft in plain formal language, checking purpose, audience, facts, structure, and tone.
6. Run self-review with `review-checklist.md`.
7. If a file is requested, save Markdown outside the skill folder, lint it, then export.

## Export Pipeline

> This is a simplified minimum pipeline. The complete pre-export sequence (including citation checking and language lint) is documented in `SKILL.md` Lint And Export.

1. Produce controlled Markdown. See `format-output.md`.
2. Run:

```bash
python scripts/check_sections.py 通知 draft.md
python scripts/generate_docx.py draft.md -o output.docx --doc-type 通知
```

3. If lint finds high-risk issues, fix the Markdown first unless the user explicitly asks to preserve the draft.

## Naming

Use:

- Project/skill name: `gongwen-draft`
- Chinese display name: `公文 Draft`
- Suggested repository name: `gongwen-draft`

Do not rename generated files to generic `gongwen-writing` unless compatibility requires it.
