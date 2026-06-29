#!/usr/bin/env python3
"""Shared YAML front-matter parser for gongwen-draft controlled Markdown."""

from __future__ import annotations

import re
from pathlib import Path


FRONT_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n?", re.S)


def parse_front_matter(text: str) -> tuple[dict[str, object], str]:
    """Parse YAML-like front matter from controlled Markdown.

    Returns (meta, rest) where *meta* maps keys to str or list[str] values
    and *rest* is the text after the closing ``---`` fence.
    """
    match = FRONT_RE.match(text)
    if not match:
        return {}, text

    meta: dict[str, object] = {}
    current_list: list[str] | None = None
    current_key: str | None = None

    for raw in match.group("body").splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.lstrip().startswith("- ") and current_list is not None:
            current_list.append(line.split("- ", 1)[1].strip())
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            current_key = key
            if value:
                meta[key] = value
                current_list = None
            else:
                current_list = []
                meta[key] = current_list
        elif current_key:
            meta[current_key] = line.strip()

    return meta, text[match.end():]


def meta_text(meta: dict[str, object], key: str) -> str:
    """Return a single string value for *key*, joining lists with ；."""
    value = meta.get(key, "")
    if isinstance(value, list):
        return "；".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def strip_front_matter(text: str) -> str:
    """Remove the front-matter block, returning only the body text."""
    return FRONT_RE.sub("", text, count=1)


def read_front_matter(path: Path) -> tuple[dict[str, object], str]:
    """Convenience: read a file and parse its front matter."""
    return parse_front_matter(path.read_text(encoding="utf-8-sig"))
