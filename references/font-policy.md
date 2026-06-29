# Font Policy

Use this reference before exporting Word `.docx` files.

## Strict Default

Default `font_profile` is `founder-gongwen`.

Required fonts:

- `方正小标宋简体`: issuer mark and title.
- `仿宋_GB2312`: body and lower headings.
- `黑体`: first-level headings.
- `楷体_GB2312`: second-level headings.
- `宋体`: page number footer.

Do not silently replace these with Noto, Microsoft YaHei, SimSun, or other generic Chinese fonts. If the required fonts are missing, stop export and report exactly which fonts are missing.

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

## Publication Boundary

Bundled font binaries are assets for local authorized use. Before publishing a public repository, release package, marketplace skill, or mirror that includes `assets/fonts/*.ttf`, confirm the font license permits redistribution. If redistribution is not confirmed, publish the skill without font binaries and keep `catalog.toml` plus official/authorized acquisition instructions.

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
