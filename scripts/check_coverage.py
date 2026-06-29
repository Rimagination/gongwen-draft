#!/usr/bin/env python3
"""Validate document-type coverage across gongwen-draft resources."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LEGAL_DOC_TYPES = [
    "决议",
    "决定",
    "命令",
    "令",
    "公报",
    "公告",
    "通告",
    "意见",
    "通知",
    "通报",
    "报告",
    "请示",
    "批复",
    "议案",
    "函",
    "纪要",
]

LEGAL_DOC_CATEGORIES = [
    "决议",
    "决定",
    "命令（令）",
    "公报",
    "公告",
    "通告",
    "意见",
    "通知",
    "通报",
    "报告",
    "请示",
    "批复",
    "议案",
    "函",
    "纪要",
]

FORMAL_MATERIAL_TYPES = [
    "工作总结",
    "工作方案",
    "调研报告",
    "汇报材料",
    "简报",
    "情况专报",
    "讲话稿",
    "回复函",
]


def load_doc_types() -> set[str]:
    module_path = ROOT / "scripts" / "check_sections.py"
    spec = importlib.util.spec_from_file_location("check_sections", module_path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(module.DOC_TYPES)


def markdown_headings(text: str) -> set[str]:
    return set(re.findall(r"(?m)^##\s+(.+?)\s*$", text))


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    lint_types = load_doc_types()
    expected_lint_types = set(LEGAL_DOC_TYPES + FORMAL_MATERIAL_TYPES)
    missing_lint = sorted(expected_lint_types - lint_types)
    extra_lint = sorted(lint_types - expected_lint_types)
    if missing_lint:
        fail(f"check_sections.DOC_TYPES missing: {', '.join(missing_lint)}")
    if extra_lint:
        fail(f"check_sections.DOC_TYPES has unclassified values: {', '.join(extra_lint)}")

    doc_types_text = (ROOT / "references" / "document-types.md").read_text(encoding="utf-8")
    headings = markdown_headings(doc_types_text)
    missing_headings = sorted((set(LEGAL_DOC_CATEGORIES) | set(FORMAL_MATERIAL_TYPES)) - headings)
    if missing_headings:
        fail(f"document-types.md missing sections: {', '.join(missing_headings)}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "法定公文（15 种，完整支持）" not in readme:
        fail("README must state 15 statutory document types.")
    if "扩展政务材料（8 类" not in readme:
        fail("README must state 8 extended formal-material categories.")
    if "后续将逐步补充专用模板" in readme:
        fail("README still claims extended templates are incomplete.")

    print("OK: document-type coverage is complete and consistent.")


if __name__ == "__main__":
    main()
