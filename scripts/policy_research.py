#!/usr/bin/env python3
"""Create a policy-research plan and citation ledger for gongwen-draft."""

from __future__ import annotations

import argparse
from pathlib import Path

from citation_policy import classify_url, source_label


CORE_SOURCES = [
    ("中国政府网", "https://www.gov.cn/", "国务院文件、国务院公报、政策解读、国务院领导活动"),
    ("国家法律法规数据库", "https://flk.npc.gov.cn/", "法律、行政法规、监察法规、司法解释等"),
    ("全国人大网", "https://www.npc.gov.cn/", "法律、决定、授权发布的规范性内容"),
    ("国务院部门官网", "https://www.gov.cn/gwyzzjg/bumen/", "部委政策文件、通知公告、政策解读"),
    ("地方人民政府官网", "https://www.gov.cn/gwyzzjg/dfzfjg/index.htm", "地方现行政策、实施细则、通知公告"),
    ("共产党员网/求是网", "https://www.12371.cn/", "党内公开发布的重要论述、学习资料和讲话线索"),
]


def search_tasks(topic: str, departments: list[str]) -> list[str]:
    quoted = topic.strip()
    tasks = [
        f"site:gov.cn {quoted} 政策 文件 最新",
        f"site:gov.cn {quoted} 国务院 通知 决定 意见",
        f"site:flk.npc.gov.cn {quoted}",
        f"site:gov.cn {quoted} 政策解读",
        f"site:gov.cn {quoted} 领导讲话 会议",
    ]
    for item in departments:
        value = item.strip()
        if not value:
            continue
        if "." in value:
            tasks.append(f"site:{value} {quoted} 政策 文件 通知")
            tasks.append(f"site:{value} {quoted} 领导讲话 会议")
        else:
            tasks.append(f"{value} 官网 {quoted} 政策 文件 通知")
            tasks.append(f"{value} 官网 {quoted} 领导讲话 会议")
    return tasks


def classify_seed_urls(urls: list[str]) -> list[str]:
    rows: list[str] = []
    for url in urls:
        kind = classify_url(url)
        rows.append(f"| {url} | {source_label(kind)} | {'可进入台账' if kind == 'official' else '仅作线索或需剔除'} |")
    if not rows:
        rows.append("| [待补充] | [待核实] | [待处理] |")
    return rows


def build_policy_research(topic: str, departments: list[str] | None = None, urls: list[str] | None = None) -> str:
    departments = departments or []
    urls = urls or []
    parts = [
        "# gongwen-draft 政策研究台账",
        "## 主题",
        topic.strip(),
        "## 检索边界",
        "- 先查政策原文，再看解读、会议通稿和权威媒体报道。",
        "- 正文政策依据优先使用国务院、各部委、全国人大、地方政府等官方网站。",
        "- 人民日报、新华社、半月谈等权威媒体可作背景材料或线索；写入依据前应回到官方原文核验。",
        "- 找不到官方来源的政策、讲话、会议精神，一律标为待核实。",
        "## 优先来源",
        "| 来源 | 入口 | 用途 |",
        "| --- | --- | --- |",
    ]
    parts.extend(f"| {name} | {url} | {use} |" for name, url, use in CORE_SOURCES)

    parts.extend(
        [
            "## 检索任务",
            "| 序号 | 检索式或动作 | 处理要求 |",
            "| --- | --- | --- |",
        ]
    )
    for index, task in enumerate(search_tasks(topic, departments), start=1):
        parts.append(f"| R{index} | {task} | 打开官方原文，记录标题、机关、日期、URL和适用范围。 |")

    parts.extend(
        [
            "## 种子链接核验",
            "| URL | 分类 | 处理意见 |",
            "| --- | --- | --- |",
            *classify_seed_urls(urls),
            "## 可引用政策来源台账",
            "| 编号 | 文件或讲话标题 | 发布机关 | 文号 | 发布日期 | 来源URL | 来源等级 | 写入正文方式 | 核验状态 |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            "| C1 | [待补充] | [待补充] | [无/待补充] | [待补充] | [官方URL] | 政策原文/讲话原文/政策解读 | 作为依据/作为背景/仅作线索 | 待核实 |",
            "## 不进入正文依据的材料",
            "- 无法打开原文的转载材料。",
            "- 只有媒体转述、没有官方原文的政策表述。",
            "- 发布日期、发布机关或适用范围不明的材料。",
            "- 与当前政策冲突或可能已被废止、修改的旧文件。",
            "## 起草前结论",
            "- 可直接引用的依据：[待补充]",
            "- 只能作背景的材料：[待补充]",
            "- 仍需用户或人工确认的事项：[待补充]",
        ]
    )
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True, help="Policy topic to research")
    parser.add_argument("--department", action="append", default=[], help="主管部门名称或官网域名，可重复")
    parser.add_argument("--url", action="append", default=[], help="已有候选来源 URL，可重复")
    parser.add_argument("-o", "--output", required=True, help="Output markdown path")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        build_policy_research(args.topic, args.department, args.url),
        encoding="utf-8",
    )
    print(f"OK: wrote policy research ledger to {output}")


if __name__ == "__main__":
    main()
