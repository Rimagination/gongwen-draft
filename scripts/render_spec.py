#!/usr/bin/env python3
"""Render a structured gongwen JSON spec into controlled Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FRONT_KEYS = [
    "red_head",
    "font_profile",
    "page_number_position",
    "show_first_page_number",
    "copy_number",
    "secret_level",
    "urgency",
    "issuer_mark",
    "doc_number",
    "issue_person",
    "recipients",
    "signer",
    "date",
    "issuer_font",
    "title_font",
    "body_font",
    "h1_font",
    "h2_font",
    "h3_font",
    "footer_font",
]


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def text(value: Any) -> str:
    return str(value).strip()


def write_front_matter(lines: list[str], meta: dict[str, Any]) -> None:
    if not meta:
        return

    lines.append("---")
    for key in FRONT_KEYS:
        value = meta.get(key)
        if value in (None, ""):
            continue
        if isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {text(value)}")

    attachments = as_list(meta.get("attachments"))
    if attachments:
        lines.append("attachments:")
        for item in attachments:
            item_text = text(item)
            if item_text:
                lines.append(f"  - {item_text}")
    lines.append("---")


def emit_paragraphs(lines: list[str], paragraphs: Any) -> None:
    for item in as_list(paragraphs):
        paragraph = text(item)
        if paragraph:
            lines.append(paragraph)


def emit_sections(lines: list[str], sections: Any, *, inherited_level: int = 1) -> None:
    for section in as_list(sections):
        if not isinstance(section, dict):
            emit_paragraphs(lines, section)
            continue

        level = int(section.get("level") or inherited_level)
        level = min(max(level, 1), 4)
        heading = text(section.get("heading") or section.get("title") or "")
        if heading:
            lines.append(f"{'#' * (level + 1)} {heading}")

        emit_paragraphs(lines, section.get("paragraphs"))
        emit_sections(lines, section.get("children"), inherited_level=level + 1)


def normalize_spec(spec: dict[str, Any]) -> str:
    meta = dict(spec.get("meta") or {})
    for key in ("recipients", "signer", "date", "attachments"):
        if key in spec and key not in meta:
            meta[key] = spec[key]

    lines: list[str] = []
    write_front_matter(lines, meta)

    title = text(spec.get("title") or meta.get("title") or "")
    if title:
        lines.append(f"# {title}")

    emit_paragraphs(lines, spec.get("lead") or spec.get("intro") or spec.get("paragraphs"))
    emit_sections(lines, spec.get("sections"))
    emit_paragraphs(lines, spec.get("closing"))

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="UTF-8 JSON spec file")
    parser.add_argument("-o", "--output", help="Output controlled Markdown path")
    args = parser.parse_args()

    input_path = Path(args.input)
    spec = json.loads(input_path.read_text(encoding="utf-8-sig"))
    if not isinstance(spec, dict):
        raise SystemExit("JSON spec root must be an object.")

    markdown = normalize_spec(spec)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print(f"Generated: {output_path.resolve()}")
    else:
        print(markdown, end="")


if __name__ == "__main__":
    main()
