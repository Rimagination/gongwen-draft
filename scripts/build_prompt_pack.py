#!/usr/bin/env python3
"""Build a compact offline prompt pack from gongwen-draft references."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFERENCES = [
    "references/core-rules.md",
    "references/material-workflow.md",
    "references/policy-research.md",
    "references/writing-method.md",
    "references/language-polishing.md",
    "references/punctuation-style.md",
    "references/review-checklist.md",
    "references/format-output.md",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def extract_doc_section(doc_type: str | None) -> str:
    text = read(ROOT / "references" / "document-types.md")
    if not doc_type:
        return text

    pattern = re.compile(
        rf"(?ms)^##\s+{re.escape(doc_type)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)"
    )
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"Unknown or unsupported doc type: {doc_type}")

    routing = text.split("## 通知", 1)[0].strip()
    return f"{routing}\n\n## {doc_type}\n{match.group('body').strip()}"


def build_prompt(doc_type: str | None, task: str | None, material: str | None) -> str:
    parts = [
        "# gongwen-draft Offline Prompt Pack",
        "Use the following rules to draft, revise, review, or format Chinese official documents and formal materials. Treat all missing facts as placeholders; never invent authority, data, signatures, document numbers, or policy basis.",
        "## Skill Entry",
        read(ROOT / "SKILL.md"),
        "## Document Type Rules",
        extract_doc_section(doc_type),
    ]

    for rel in DEFAULT_REFERENCES:
        path = ROOT / rel
        parts.extend([f"## {rel}", read(path)])

    if task:
        parts.extend(["## User Task", task.strip()])
    if material:
        parts.extend(["## User Materials", material.strip()])

    return "\n\n".join(parts).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc-type", help="Limit document-type rules to one type, for example 通知")
    parser.add_argument("--task", help="Task instruction to append")
    parser.add_argument("--material-file", help="Optional UTF-8 material file to append")
    parser.add_argument("-o", "--output", required=True, help="Output markdown file")
    args = parser.parse_args()

    material = None
    if args.material_file:
        material = read(Path(args.material_file))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_prompt(args.doc_type, args.task, material), encoding="utf-8")
    print(f"OK: wrote offline prompt pack to {output}")


if __name__ == "__main__":
    main()
