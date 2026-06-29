#!/usr/bin/env python3
"""Prepare a lightweight material dossier for gongwen-draft."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DATE_RE = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日|\d{4}年\d{1,2}月|\d{4}年度?")
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:%|％|万元|亿元|人|户|项|个|件|次|天|月|年|日前|月底)")
ORG_RE = re.compile(r"[\u4e00-\u9fff]{2,}(?:委员会|人民政府|办公室|厅|局|办|中心|部门|单位|街道办事处|公司|学校)")
CLAIM_RE = re.compile(r"显著|重大|全面|圆满|首次|唯一|领先|突破|成效|建议|拟|计划|预计|争取|力争|待核实")


def clean_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(re.sub(r"\s+", " ", line))
    return lines


def pick_lines(lines: list[str], pattern: re.Pattern[str], limit: int = 30) -> list[str]:
    picked: list[str] = []
    seen: set[str] = set()
    for line in lines:
        if pattern.search(line) and line not in seen:
            picked.append(line)
            seen.add(line)
        if len(picked) >= limit:
            break
    return picked


def source_name(path: Path) -> str:
    return path.name if path.name else str(path)


def build_dossier(paths: list[Path], task: str | None = None) -> str:
    all_lines: list[tuple[str, str]] = []
    source_rows: list[str] = []

    for index, path in enumerate(paths, start=1):
        text = path.read_text(encoding="utf-8-sig")
        lines = clean_lines(text)
        label = f"S{index}"
        source_rows.append(f"| {label} | {source_name(path)} | 用户提供/本地文件 | {len(lines)} |")
        all_lines.extend((label, line) for line in lines)

    merged_lines = [f"{label}：{line}" for label, line in all_lines]
    fact_pattern = re.compile(
        f"(?:{DATE_RE.pattern})|(?:{NUMBER_RE.pattern})|(?:{ORG_RE.pattern})"
    )
    fact_lines = pick_lines(merged_lines, fact_pattern)
    claim_lines = pick_lines(merged_lines, CLAIM_RE)

    questions = [
        "发文机关、主送机关、成文日期是否已经确认？",
        "涉及政策依据、会议结论、领导讲话、统计数据的内容是否有正式来源？",
        "哪些内容属于已决定事项，哪些仍是拟办、建议或待审批事项？",
        "是否存在涉密、内部审议、个人敏感信息或不宜进入云端模型的内容？",
    ]

    parts = ["# gongwen-draft 素材台账"]
    if task:
        parts.extend(["## 任务", task.strip()])

    parts.extend(
        [
            "## 来源表",
            "| 编号 | 来源 | 类型 | 有效行数 |",
            "| --- | --- | --- | --- |",
            *source_rows,
            "## 可直接使用的事实线索",
        ]
    )
    parts.extend(f"- {line}" for line in fact_lines[:30])
    if not fact_lines:
        parts.append("- 未自动识别到日期、数字或机构名称，请人工补充关键事实。")

    parts.append("## 需要谨慎处理的判断或待核实表述")
    parts.extend(f"- {line}" for line in claim_lines[:30])
    if not claim_lines:
        parts.append("- 未自动识别到明显判断性或待核实表述。")

    parts.extend(["## 起草前确认问题", *[f"- {question}" for question in questions]])
    parts.append("## 使用提示")
    parts.append("- 起草时只把已核实内容写成确定事实；拟办、建议、预计、研判类内容应保留相应语气。")
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("materials", nargs="+", help="UTF-8 text/markdown material files")
    parser.add_argument("--task", help="Optional task summary")
    parser.add_argument("-o", "--output", required=True, help="Output dossier markdown path")
    args = parser.parse_args()

    paths = [Path(item) for item in args.materials]
    for path in paths:
        if not path.exists():
            raise SystemExit(f"Material file not found: {path}")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_dossier(paths, args.task), encoding="utf-8")
    print(f"OK: wrote material dossier to {output}")


if __name__ == "__main__":
    main()
