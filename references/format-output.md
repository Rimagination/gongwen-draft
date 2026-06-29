# Format And Output

Use this reference when converting a draft to a controlled Markdown or `.docx` file.

## Controlled Markdown

Use one content unit per line. Avoid relying on general Markdown behavior.

```markdown
---
red_head: true
font_profile: founder-gongwen
page_number_position: outer
show_first_page_number: false
copy_number: 000001
secret_level: 机密★1年
urgency: 特急
issuer_mark: 某某单位文件
doc_number: 某发〔2026〕1号
issue_person: 张三
recipients: 各有关单位
signer: 某某单位
date: 2026年6月29日
---
# 关于开展年度工作总结的通知
为全面总结年度工作成果，现就有关事项通知如下。
## 一、总体要求
### （一）突出重点
正文自然段。
## 二、报送要求
正文自然段。
```

Supported front matter keys:

- `red_head`: optional boolean; defaults to `true` when版头字段 are supplied. Set `false` for a plain drafting header without red text/red line.
- `font_profile`: defaults to `founder-gongwen`, which requires exact公文字体 and fails export if they are missing.
- `page_number_position`: `outer` by default, using odd-page right and even-page left page numbers. Set `center` only for draft convenience or unit templates that require it.
- `show_first_page_number`: defaults to `false`; standard公文首页 usually does not show page number.
- Font overrides for authorized unit templates: `issuer_font`, `title_font`, `body_font`, `h1_font`, `h2_font`, `h3_font`, `footer_font`.
- `copy_number`: 份号, optional; only use user-supplied values or placeholders.
- `secret_level`: 密级和保密期限, optional; do not infer or invent.
- `urgency`: 紧急程度, optional; do not infer or invent.
- `issuer_mark`: 发文机关标志, optional.
- `doc_number`: 发文字号, optional; never invent it.
- `issue_person`: 版头中的签发人, optional and normally used for上行文. The `签发人：` label uses 3号仿宋体 and the name uses 3号楷体. Do not confuse this with正文末尾的发文机关署名.
- `recipients`: 主送机关, optional.
- `signer`: 正文末尾的发文机关署名, optional.
- `date`: 成文日期, optional.
- `attachments`: optional list; use simple `- 附件名称` lines.

## Heading Mapping

- `#`: document title.
- `##`: first-level heading, normally `一、`.
- `###`: second-level heading, normally `（一）`.
- `####` and deeper: lower-level heading/body emphasis.
- Other non-empty lines: body paragraphs.
- Standalone headings do not end with `。`, `；`, `：`, `！`, or `？`. If a second-level heading and body text are in the same paragraph, the heading phrase may end with `。` before body text.
- Do not rely on generic Markdown: avoid tables, bullet markers, block quotes, links, images, code spans, and bold markers for formal export.

## JSON Spec

For file generation, prefer a structured JSON spec when the draft is assembled from many facts, sections, or templates. Render it first:

```bash
python scripts/render_spec.py spec.json -o draft.md
```

Minimal shape:

```json
{
  "meta": {
    "red_head": true,
    "font_profile": "founder-gongwen",
    "issuer_mark": "某某单位文件",
    "doc_number": "某发〔2026〕1号",
    "issue_person": "张三",
    "recipients": "各有关单位",
    "signer": "某某单位",
    "date": "2026年6月29日"
  },
  "title": "关于开展年度工作总结的通知",
  "lead": ["为全面总结年度工作成果，现就有关事项通知如下。"],
  "sections": [
    {
      "level": 1,
      "heading": "一、总体要求",
      "paragraphs": ["正文自然段。"],
      "children": [
        {"level": 2, "heading": "（一）突出重点", "paragraphs": ["正文自然段。"]}
      ]
    }
  ]
}
```

The renderer does not invent numbering or facts. Section headings and paragraph text must already contain the intended wording.

## Word Export

Use `scripts/generate_docx.py` after drafting:

```bash
python scripts/check_fonts.py --draft draft.md
python scripts/generate_docx.py draft.md -o output.docx --doc-type 通知 --install-font-assets
```

The script applies common GB/T 9704-2012 style defaults:

- A4 page.
- Margins: top 37mm, bottom 35mm, left 28mm, right 26mm.
- Strict font guard: default output requires `方正小标宋简体`, `仿宋_GB2312`, `黑体`, `楷体_GB2312`, and `宋体`; export stops if required fonts are not installed.
- Optional generic版头: red发文机关标志, 发文字号/签发人 line, and red separator line when front matter supplies `issuer_mark`, `doc_number`, or `issue_person`.
- Title: 方正小标宋简体, size 2.
- Body: 仿宋_GB2312, size 3, fixed 28pt line spacing.
- First-level headings: 黑体, size 3.
- Second-level headings: 楷体_GB2312, size 3.
- Page number footer: `— 1 —` style Word field, hidden on the first page by default, odd pages right aligned and even pages left aligned.
- Existing output files are not overwritten by default; the script creates `-v02`, `-v03`, etc. Use `--overwrite` only when the user explicitly wants replacement.

Generated `.docx` is a drafting aid, not proof of formal issuance. Final files still require the user's current unit template, approval flow, seal/signature handling, and human review. Never imitate a real机关版头, 发文字号, 签发人, or印章 unless the user supplies authorized values and the task is explicitly draft preparation.
