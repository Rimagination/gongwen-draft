#!/usr/bin/env python3
"""Shared source classification rules for gongwen-draft citation checks."""

from __future__ import annotations

from urllib.parse import urlparse


OFFICIAL_EXACT_HOSTS = {
    "gov.cn",
    "www.gov.cn",
    "npc.gov.cn",
    "www.npc.gov.cn",
    "flk.npc.gov.cn",
    "cppcc.gov.cn",
    "www.cppcc.gov.cn",
    "ccdi.gov.cn",
    "www.ccdi.gov.cn",
    "12371.cn",
    "www.12371.cn",
    "qstheory.cn",
    "www.qstheory.cn",
    "dangjian.cn",
    "www.dangjian.cn",
}

OFFICIAL_SUFFIXES = (
    ".gov.cn",
    ".npc.gov.cn",
    ".cppcc.gov.cn",
    ".ccdi.gov.cn",
    ".12371.cn",
    ".qstheory.cn",
    ".dangjian.cn",
)

AUTHORITATIVE_MEDIA_EXACT_HOSTS = {
    "people.com.cn",
    "www.people.com.cn",
    "xinhuanet.com",
    "www.xinhuanet.com",
    "banyuetan.org",
    "www.banyuetan.org",
    "cctv.com",
    "www.cctv.com",
    "cctv.cn",
    "www.cctv.cn",
    "gmw.cn",
    "www.gmw.cn",
}

AUTHORITATIVE_MEDIA_SUFFIXES = (
    ".people.com.cn",
    ".xinhuanet.com",
    ".banyuetan.org",
    ".cctv.com",
    ".cctv.cn",
    ".gmw.cn",
)


def normalize_host(url: str) -> str:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower()
    if "@" in host:
        host = host.rsplit("@", 1)[1]
    if ":" in host:
        host = host.split(":", 1)[0]
    return host


def classify_url(url: str) -> str:
    """Return official, authoritative-media, or untrusted."""

    host = normalize_host(url)
    if not host:
        return "untrusted"
    if host in OFFICIAL_EXACT_HOSTS or host.endswith(OFFICIAL_SUFFIXES):
        return "official"
    if host in AUTHORITATIVE_MEDIA_EXACT_HOSTS or host.endswith(AUTHORITATIVE_MEDIA_SUFFIXES):
        return "authoritative-media"
    return "untrusted"


def source_label(kind: str) -> str:
    return {
        "official": "官方来源",
        "authoritative-media": "权威媒体",
        "untrusted": "非权威或未知来源",
    }.get(kind, "未知来源")
