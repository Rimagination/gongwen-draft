# Font Policy

Use this reference before exporting Word `.docx` files.

## Strict Default

Default `font_profile` is `founder-gongwen`.

Required fonts:

- `方正小标宋简体`: issuer mark and title.
- `仿宋_GB2312`: body and lower headings.
- `黑体`: first-level headings.
- `楷体_GB2312`: second-level headings.
- `宋体`: page number footer. **Not bundled** — expected to be pre-installed via the operating system (ships with all Chinese editions of Windows as SimSun). On non-Chinese systems, install SimSun manually before export.

Do not silently replace these with Noto, Microsoft YaHei, SimSun, or other generic Chinese fonts. If the required fonts are missing, stop export and report exactly which fonts are missing.

## Configuration Modes

Use one of three modes:

1. Default公文字体 mode: use `founder-gongwen` and require the exact fonts listed above.
2. Unit template mode: use `font_profile: custom` only when the user provides exact unit-required font names.
3. Authorized asset mode: install or use font files placed under `assets/fonts` after verifying `catalog.toml`.

Do not guess custom font names from a screenshot or from visual similarity. Ask the user for the exact font names used by the unit template, or inspect an authorized template when provided.

## Official Channel

方正字库 official page for the公文写作字库:

- https://www.foundertype.com/index.php/FontInfo/get_font_office.html

The official page states that the公文写作字库 needs four fonts: 方正小标宋、黑体、仿宋、楷体. It provides a "下载字体包" entry, but obtaining the package may require account authorization/payment. Do not bypass authorization or download from unofficial font mirrors.

## Local Workflow

The skill may include local font assets under `assets/fonts` plus `assets/fonts/catalog.toml`.
The catalog records expected font names, hashes, source project, and redistribution cautions.
Before installing or publishing bundled fonts, verify the catalog:

```bash
python scripts/check_fonts.py --verify-assets
```

Before Word export, run:

```bash
python scripts/check_fonts.py --draft draft.md
```

If the user has placed authorized font files under `assets/fonts`, install matching fonts for the current Windows user:

```bash
python scripts/check_fonts.py --draft draft.md --install-assets
```

During export, use:

```bash
python scripts/generate_docx.py draft.md -o output.docx --doc-type 通知 --install-font-assets
```

The export script checks installed fonts before saving. Font assets are not treated as installed fonts until `--install-assets` / `--install-font-assets` has copied and registered matching files. A generated `.docx` is only reliable on machines that also have the required fonts installed, unless the user's authorized template embeds fonts under its own license terms.

Automated asset installation currently supports Windows current-user fonts. On macOS or Linux, install authorized fonts through the operating system, then run `python scripts/check_fonts.py --draft draft.md` again.

## User-Facing Font Setup

When the user asks how to configure fonts, explain it in plain language:

- Default export uses 方正小标宋简体、仿宋_GB2312、黑体、楷体_GB2312 and 宋体.
- If fonts are missing, export stops and reports the missing names.
- On Windows, authorized bundled assets can be installed for the current user.
- If the unit template requires different fonts, the user must provide exact font names and ensure they are installed or supplied as authorized assets.
- A Word file may look different on another machine unless that machine has the same fonts installed.

## Publication Boundary

Bundled font binaries are provided as assets for official-document draft formatting. Before using, mirroring, repackaging, or redistributing them, confirm the font license and organizational authorization requirements. If redistribution is not permitted in a downstream package, publish that package without font binaries and keep `catalog.toml` plus official/authorized acquisition instructions.

## Unit Template Overrides

If the user provides a unit template or authorized font policy that requires different exact font names, set explicit front matter:

```yaml
font_profile: custom
issuer_font: 方正小标宋简体
title_font: 方正小标宋简体
body_font: 仿宋_GB2312
h1_font: 黑体
h2_font: 楷体_GB2312
h3_font: 仿宋_GB2312
footer_font: 宋体
```

Only use custom values when the user confirms they are the unit's required fonts and they are installed or supplied as authorized assets.
