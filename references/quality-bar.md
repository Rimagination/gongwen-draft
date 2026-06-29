# Quality Bar

Use this file to judge whether `gongwen-draft` is better than a generic公文写作 skill from a user's point of view.

## What A User Should Expect

1. It should choose the right文种 before writing.
   - The skill should actively catch 请示/报告, 通知/函, 公告/通告, 批复/复函, 纪要/会议记录 confusions.

2. It should protect the user from false authority.
   - It must not invent policies, document numbers, dates, leaders, meetings, approvals, seals, or statistics.
   - Missing facts should become placeholders or `待核实`, not confident prose.

3. It should be useful with messy materials.
   - The user may paste notes, meeting minutes, bullet points, WeChat article excerpts, or half-written drafts.
   - The skill should extract facts, build a structure, and ask only the few questions that matter.

4. It should separate facts from wording.
   - Maintain a mental or written fact ledger: confirmed facts, user judgments, to-verify items, and suggested wording.
   - Do not turn a plan into an achievement or a suggestion into a decision.

5. It should provide a usable draft quickly.
   - For ordinary tasks, give the draft first and keep caveats short.
   - For high-risk tasks, put risks before polish.

6. It should review like a competent办公室 colleague.
   - Findings should cover文种、行文方向、权限、事实、结构、执行性、语言、格式、保密.
   - Reviews should be actionable, not vague comments like "语言需进一步规范".

7. It should export files, not only write advice.
   - Markdown should be clean and controlled before `.docx` export.
   - JSON specs should be accepted for deterministic generation when a draft has many structured fields.
   - Generated files should be linted and saved outside the skill folder.
   - Generic红头版头 should be exportable from controlled front matter, while clearly remaining a draft aid rather than formal issuance.
   - Export must fail when exact required公文字体 are missing; do not silently substitute generic Chinese fonts.
   - Generated files should not overwrite earlier versions unless explicitly requested.

8. It should respect unit templates.
   - A user's current unit template beats generic GB/T-style defaults.
   - Generic defaults are only baselines for drafts and learning.

9. It should be source-aware.
   - Official rules and verified current sources outrank community skills, media articles, and training notes.
   - Community references should be cited when the skill design is described.

10. It should not make the user fight the tool.
    - Ask concise questions.
    - Avoid full ceremony for small tasks.
    - Preserve the user's facts and intent when revising.

## Better-Than-Community Targets

Compared with many lightweight community skills, `gongwen-draft` should add:

- Explicit community citations and source hierarchy.
- A fact-ledger discipline before drafting.
- High-risk linting as a first-class workflow step.
- Deterministic Markdown/JSON -> `.docx` generation, including generic红头版头 controls, strict font validation, first-page page-number handling, and non-overwrite versioning.
- Separate references for routing, document types, review, output, project lessons, and citations.
- A clear rule that official/current/user-provided sources outrank community guidance.

Compared with larger projects, `gongwen-draft` should stay:

- Portable as a skill folder.
- Easy to trigger from normal conversation.
- Small enough to maintain without a full app stack.
- Conservative enough for real机关材料 drafting support.
