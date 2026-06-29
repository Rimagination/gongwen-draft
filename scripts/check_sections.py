#!/usr/bin/env python3
"""Heuristic checker for Chinese official document drafts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DOC_TYPES = {
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
    "工作总结",
    "工作方案",
    "调研报告",
    "讲话稿",
    "汇报材料",
    "简报",
    "情况专报",
    "回复函",
}

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

from front_matter import parse_front_matter, strip_front_matter
ASCII_PUNCT_NEAR_CJK_RE = re.compile(
    r"[\u3400-\u4dbf\u4e00-\u9fff][,:;!?()\[\]{}\"']|"
    r"[,:;!?()\[\]{}\"'][\u3400-\u4dbf\u4e00-\u9fff]|"
    r"[\u3400-\u4dbf\u4e00-\u9fff]\.(?=\s|$|[\u3400-\u4dbf\u4e00-\u9fff])"
)
TECH_TOKEN_RE = re.compile(
    r"`[^`]*`|https?://\S+|www\.\S+|[\w.+-]+@[\w.-]+\.\w+|[A-Za-z]:\\[^\s]+|/[^\s]+"
)



def title_from_text(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped
    return ""


def add(issues: list[tuple[str, str]], severity: str, message: str) -> None:
    issues.append((severity, message))


def strip_technical_tokens(line: str) -> str:
    return TECH_TOKEN_RE.sub("", line)


def punctuation_issues(body: str) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    ascii_examples: list[str] = []

    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue
        text = strip_technical_tokens(line.lstrip("#").strip())
        if CJK_RE.search(text) and ASCII_PUNCT_NEAR_CJK_RE.search(text):
            ascii_examples.append(line[:50])

    if ascii_examples:
        samples = "；".join(ascii_examples[:3])
        add(
            issues,
            "WARN",
            f"中文语境中疑似使用英文/半角标点，应改用中文全角标点；示例：{samples}",
        )

    if re.search(r"(?m)^\s*附件\s*:", body):
        add(issues, "WARN", "附件说明应使用中文冒号 `附件：`，不要写作 `附件:`。")
    if re.search(r"(?m)^\s*附件\s*[一二三四五六七八九十\d]+\s*[：:.．。]", body):
        add(issues, "WARN", "附件页题名一般写作 `附件1`、`附件2`，顺序号后不加冒号、点号或句号；正文附件说明用 `附件：`。")

    if re.search(r"(?m)^\s*#{0,6}\s*（[一二三四五六七八九十]+）、", body):
        add(issues, "WARN", "第二层级序号应写作 `（一）`，不要写作 `（一）、`。")
    if re.search(r"(?m)^\s*#{0,6}\s*\d+、", body):
        add(issues, "WARN", "第三层级序号应写作 `1.`，不要写作 `1、`。")
    if re.search(r"(?m)^\s*#{0,6}\s*（\d+）、", body):
        add(issues, "WARN", "第四层级序号应写作 `（1）`，不要写作 `（1）、`。")

    for raw in body.splitlines():
        line = raw.strip()
        if re.match(r"^#{1,6}\s+", line) and re.search(r"[。；：！？]$", line):
            add(issues, "INFO", f"单独成行的标题一般不加句末标点：{line[:50]}")
            break

    if re.search(r"[”》’][、，][“《‘]", body):
        add(issues, "INFO", "并列引号项或书名号项之间通常不加顿号，例如 `“定盘星”“指南针”`、`《红楼梦》《三国演义》`。")
    if re.search(r"妥否[？?]", body):
        add(issues, "WARN", "请示结语宜写作 `妥否，请批示。`，不要把“妥否”写成问号句。")

    return issues


def check(doc_type: str, text: str) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    meta, body = parse_front_matter(text)
    compact = re.sub(r"\s+", "", body)
    title = title_from_text(body)
    doc_number = meta.get("doc_number", "").strip()

    if doc_type and doc_type not in DOC_TYPES:
        add(issues, "WARN", f"未识别文种 `{doc_type}`，请确认是否为法定公文或常用事务文书。")
    if re.search(r"GB/T\s*9704[-—－]2022|GB/T9704[-—－]2022", text):
        add(issues, "HIGH", "出现 `GB/T 9704-2022`，现行常用依据应核对为 GB/T 9704-2012。")
    if "请示报告" in compact:
        add(issues, "HIGH", "出现“请示报告”混用表述，应明确使用“请示”或“报告”。")
    if doc_type and title and doc_type not in title and doc_type not in {"讲话稿", "汇报材料"}:
        add(issues, "WARN", f"标题中未明显包含文种 `{doc_type}`。")
    if doc_number:
        if re.search(r"[\[\]【】()（）]", doc_number) and not re.search(r"〔[^〕]+〕", doc_number):
            add(issues, "HIGH", "发文字号年份应使用六角括号 `〔〕`。")
        if "第" in doc_number:
            add(issues, "HIGH", "发文字号顺序号不加“第”字。")
        if re.search(r"〔\d{2}〕", doc_number) or re.search(r"〕0\d+号", doc_number):
            add(issues, "WARN", "发文字号年份应标全称，顺序号不编虚位。")
    if re.search(r"\[[^\]]+\]|〔[^〕]*(待|某|X|x|日期|机关)[^〕]*〕", text):
        add(issues, "WARN", "仍有占位符或待填信息，正式发文前需补齐。")

    issues.extend(punctuation_issues(body))

    if doc_type == "报告" and re.search(r"妥否|请批示|请批复|恳请.*批准|报请.*审批|请予批准", compact):
        add(issues, "HIGH", "报告中疑似夹带请示/审批请求，报告不得夹带请示事项。")
    if doc_type == "请示":
        if not re.search(r"妥否|请批示|请批复|以上请示", compact):
            add(issues, "WARN", "请示缺少常见请批结语。")
        if len(re.findall(r"请示事项|恳请|申请|请求", compact)) > 5:
            add(issues, "WARN", "请示中请求性表达较多，需确认是否符合一文一事。")
    if doc_type == "函" and re.search(r"命令|责令|必须无条件", compact):
        add(issues, "WARN", "函应保持平等商洽语气，当前文本可能偏命令式。")
    if doc_type == "批复" and not re.search(r"收悉|经研究|现批复如下|此复", compact):
        add(issues, "WARN", "批复缺少“收悉/经研究/现批复如下/此复”等常见结构。")

    if re.search(r"\*\*|__|^[-*]\s+", body, flags=re.M):
        add(issues, "INFO", "含 Markdown 强调或列表标记，导出正式公文前建议改为自然段和层级序号。")
    if re.search(r"一[、.]|二[、.]|三[、.]", body) and re.search(r"（1）|\\(1\\)", body):
        add(issues, "INFO", "请确认层级序号是否按“一、（一）1.（1）”连续使用。")
    if re.search(r"二〇|二零|[0-9]{4}[./-][0-9]{1,2}[./-][0-9]{1,2}", body):
        add(issues, "WARN", "日期格式疑似不符合常见公文写法，建议使用“2026年6月29日”。")
    if re.search(r"显著|全面圆满|重大突破|高度重视|尽快|原则上", compact):
        add(issues, "INFO", "存在容易空泛或需界定的词语，请核实是否有事实支撑或明确时限。")

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("doc_type", help="Document type, for example 通知 or 请示")
    parser.add_argument("input", help="Markdown or text draft")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if HIGH issues are found")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8-sig")
    issues = check(args.doc_type, text)
    if not issues:
        print("OK: no obvious high-risk issue found.")
        return

    for severity, message in issues:
        print(f"[{severity}] {message}")

    if args.strict and any(severity == "HIGH" for severity, _ in issues):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
