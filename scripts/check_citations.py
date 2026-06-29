#!/usr/bin/env python3
"""Check policy citations for official-source discipline."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from citation_policy import classify_url, source_label


URL_RE = re.compile(r"https?://[^\s<>()\[\]\"'，。；、）】]+")
DATE_RE = re.compile(r"(?:19|20)\d{2}年\d{1,2}月\d{1,2}日|(?:19|20)\d{2}-\d{1,2}-\d{1,2}")
ISSUER_RE = re.compile(
    r"国务院|全国人大|人民政府|委员会|办公厅|办公室|部|委|厅|局|署|院|最高人民法院|最高人民检察院|新华社|人民日报|半月谈"
)
POLICY_CLAIM_RE = re.compile(r"根据|依据|贯彻|落实|政策|法规|规章|规范性文件|领导讲话|会议精神|重要指示|重要批示")
CITATION_LEDGER_RE = re.compile(r"(?ms)^##\s+可引用政策来源台账\s*$\n(?P<body>.*?)(?=^##\s+|\Z)")


@dataclass(frozen=True)
class CitationIssue:
    severity: str
    message: str


def extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for match in URL_RE.finditer(text):
        url = match.group(0).rstrip(".。；;，,")
        if url not in seen:
            urls.append(url)
            seen.add(url)
    return urls


def line_containing(text: str, needle: str) -> str:
    for line in text.splitlines():
        if needle in line:
            return line.strip()
    return ""


def citation_scope(text: str) -> str:
    """Check the citation ledger section first when a policy ledger is present."""

    match = CITATION_LEDGER_RE.search(text)
    if match:
        return match.group("body")
    return text


def check_citations(
    text: str,
    *,
    require_citations: bool = False,
    allow_media: bool = False,
) -> list[CitationIssue]:
    issues: list[CitationIssue] = []
    scope = citation_scope(text)
    urls = extract_urls(scope)

    if "GB/T 9704-2022" in text:
        issues.append(
            CitationIssue(
                "error",
                "发现 GB/T 9704-2022 表述；当前项目按 GB/T 9704-2012 校验，除非用户提供新标准正式来源。",
            )
        )

    if require_citations and not urls:
        issues.append(CitationIssue("error", "要求校验政策引用，但未发现任何 URL 来源。"))
    elif not urls and POLICY_CLAIM_RE.search(text):
        issues.append(CitationIssue("warning", "文本含政策、依据或讲话类表述，但未发现可校验 URL。"))

    for url in urls:
        kind = classify_url(url)
        label = source_label(kind)
        line = line_containing(scope, url)

        if kind == "untrusted":
            issues.append(CitationIssue("error", f"{label}不能作为政策依据：{url}"))
        elif kind == "authoritative-media":
            severity = "warning" if allow_media else "error"
            issues.append(
                CitationIssue(
                    severity,
                    f"{label}只能作背景材料或权威报道线索，不能直接替代政策原文：{url}",
                )
            )

        if kind == "official":
            if "|" in line:
                if not DATE_RE.search(line):
                    issues.append(CitationIssue("warning", f"官方来源行缺少发布日期：{url}"))
                if not ISSUER_RE.search(line):
                    issues.append(CitationIssue("warning", f"官方来源行缺少发布机关：{url}"))
            else:
                issues.append(CitationIssue("warning", f"建议将官方来源放入台账表格并补齐标题、机关、日期：{url}"))

    return issues


def print_issues(issues: list[CitationIssue]) -> None:
    if not issues:
        print("OK: citation sources passed official-source checks.")
        return
    for issue in issues:
        prefix = "ERROR" if issue.severity == "error" else "WARN"
        print(f"{prefix}: {issue.message}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="Markdown draft or policy ledger to check")
    parser.add_argument("--require-citations", action="store_true", help="Fail when no URL citation is present")
    parser.add_argument(
        "--allow-media",
        action="store_true",
        help="Allow authoritative-media URLs as warnings for background use.",
    )
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8-sig")
    issues = check_citations(
        text,
        require_citations=args.require_citations,
        allow_media=args.allow_media,
    )
    print_issues(issues)
    if any(issue.severity == "error" for issue in issues):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
