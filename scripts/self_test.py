#!/usr/bin/env python3
"""Lightweight self-tests for gongwen-draft helper scripts."""

from __future__ import annotations

import tempfile
from pathlib import Path

from check_sections import check
from generate_docx import unique_output_path
from render_spec import normalize_spec


def test_render_spec() -> None:
    markdown = normalize_spec(
        {
            "meta": {"recipients": "各有关单位", "date": "2026年6月29日"},
            "title": "关于开展年度工作总结的通知",
            "lead": ["为全面总结年度工作成果，现就有关事项通知如下。"],
            "sections": [
                {
                    "level": 1,
                    "heading": "一、总体要求",
                    "paragraphs": ["正文自然段。"],
                    "children": [{"level": 2, "heading": "（一）突出重点", "paragraphs": ["正文自然段。"]}],
                }
            ],
        }
    )
    assert "recipients: 各有关单位" in markdown
    assert "# 关于开展年度工作总结的通知" in markdown
    assert "## 一、总体要求" in markdown
    assert "### （一）突出重点" in markdown


def test_high_risk_lint() -> None:
    issues = check(
        "报告",
        "---\ndoc_number: 某发[2026]第01号\n---\n# 关于有关工作的报告\n请予批准。\nGB/T 9704-2022\n",
    )
    messages = "\n".join(message for _, message in issues)
    assert "GB/T 9704-2022" in messages
    assert "报告中疑似夹带请示" in messages
    assert "六角括号" in messages
    assert "不加“第”字" in messages


def test_punctuation_lint() -> None:
    issues = check(
        "通知",
        "# 关于开展工作的通知。\n各有关单位:\n现将有关事项通知如下:\n## 一、总体要求。\n### （一）、完善机制\n1、明确责任\n附件1：工作方案\n",
    )
    messages = "\n".join(message for _, message in issues)
    assert "英文/半角标点" in messages
    assert "单独成行的标题" in messages
    assert "（一）、" in messages
    assert "1、" in messages
    assert "附件页题名" in messages


def test_unique_output_path() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir) / "output.docx"
        base.write_bytes(b"old")
        assert unique_output_path(base).name == "output-v02.docx"
        (Path(tmpdir) / "output-v02.docx").write_bytes(b"old")
        assert unique_output_path(base).name == "output-v03.docx"


def main() -> None:
    test_render_spec()
    test_high_risk_lint()
    test_punctuation_lint()
    test_unique_output_path()
    print("OK: gongwen-draft self-tests passed.")


if __name__ == "__main__":
    main()
