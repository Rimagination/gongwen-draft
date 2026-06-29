#!/usr/bin/env python3
"""Flag risky or weak official-document wording."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATTERNS = [
    ("WARN", r"显著成效|重大突破|全面完成|圆满完成|走在前列", "判断较强，需有事实、数据或正式评价支撑。"),
    ("INFO", r"高度重视|切实加强|扎实推进|形成合力|持续发力|不断提升", "表述偏泛，建议补充具体动作、责任或结果。"),
    ("INFO", r"尽快|及时|适时|近期|原则上", "时间或条件偏模糊，正式部署中宜明确期限或触发条件。"),
    ("WARN", r"必须无条件|一律|严禁|责令", "约束性较强，需确认发文权限和适用范围。"),
    ("WARN", r"给力|打call|破防|硬核|搞定|点赞|牛\b|yyds", "疑似口语或网络表达，不适合正式公文。"),
    ("INFO", r"不是[^。；；\n]{1,40}而是", "可直接写目的和要求，避免绕行表达。"),
]


def check_language(text: str) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    for severity, pattern, message in PATTERNS:
        for match in re.finditer(pattern, text, flags=re.I):
            start = max(0, match.start() - 18)
            end = min(len(text), match.end() + 18)
            sample = re.sub(r"\s+", " ", text[start:end]).strip()
            issues.append((severity, f"{message} 示例：{sample}"))
            break
    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Markdown or text draft")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if WARN issues are found")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8-sig")
    issues = check_language(text)
    if not issues:
        print("OK: no obvious language polish issue found.")
        return

    for severity, message in issues:
        print(f"[{severity}] {message}")

    if args.strict and any(severity == "WARN" for severity, _ in issues):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
