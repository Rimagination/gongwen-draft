#!/usr/bin/env python3
"""Lightweight self-tests for gongwen-draft helper scripts."""

from __future__ import annotations

import tempfile
from pathlib import Path

from build_prompt_pack import build_prompt
from check_citations import check_citations
from check_language import check_language
from check_coverage import main as check_coverage_main
from check_sections import check
from generate_docx import unique_output_path
from policy_research import build_policy_research
from prepare_dossier import build_dossier
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


def test_prompt_pack() -> None:
    prompt = build_prompt("通知", "起草一份通知。", "会议决定：按时报送。")
    assert "# gongwen-draft Offline Prompt Pack" in prompt
    assert "## 通知" in prompt
    assert "会议决定：按时报送。" in prompt
    assert "## 请示" not in prompt


def test_coverage() -> None:
    check_coverage_main()


def test_material_dossier() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        material = Path(tmpdir) / "materials.md"
        material.write_text(
            "2026年6月30日，区水利局完成12项排查。计划取得显著成效。\n",
            encoding="utf-8",
        )
        dossier = build_dossier([material], "整理防汛情况专报")
        assert "区水利局" in dossier
        assert "12项" in dossier
        assert "显著成效" in dossier
        assert "待核实" in dossier


def test_language_lint() -> None:
    issues = check_language("我局高度重视该项工作，取得显著成效，大家纷纷点赞。")
    messages = "\n".join(message for _, message in issues)
    assert "事实、数据或正式评价" in messages
    assert "表述偏泛" in messages
    assert "口语或网络表达" in messages


def test_policy_research_pack() -> None:
    pack = build_policy_research(
        "公共数据授权运营",
        departments=["ndrc.gov.cn"],
        urls=["https://www.gov.cn/zhengce/content/2024-01/01/content_0000000.htm"],
    )
    assert "政策研究台账" in pack
    assert "site:gov.cn 公共数据授权运营 政策 文件 最新" in pack
    assert "site:ndrc.gov.cn 公共数据授权运营 政策 文件 通知" in pack
    assert "可引用政策来源台账" in pack
    assert any(issue.severity == "error" for issue in check_citations(pack, require_citations=True))


def test_citation_checker() -> None:
    valid = (
        "| C1 | 国务院关于某项工作的意见 | 国务院 | 国发〔2026〕1号 | "
        "2026年1月1日 | https://www.gov.cn/zhengce/content/2026-01/01/content_0000000.htm | 政策原文 | 作为依据 | 已核实 |\n"
    )
    assert not [issue for issue in check_citations(valid, require_citations=True) if issue.severity == "error"]

    invalid = "依据某文章： https://github.com/example/policy-note"
    issues = check_citations(invalid, require_citations=True)
    assert any(issue.severity == "error" and "不能作为政策依据" in issue.message for issue in issues)


def main() -> None:
    test_render_spec()
    test_high_risk_lint()
    test_punctuation_lint()
    test_unique_output_path()
    test_prompt_pack()
    test_coverage()
    test_material_dossier()
    test_language_lint()
    test_policy_research_pack()
    test_citation_checker()
    print("OK: gongwen-draft self-tests passed.")


if __name__ == "__main__":
    main()
