# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 blip-cmd and contributors
"""
Review-status front matter for book pages (see CONTENT_STANDARDS.md).

Front matter is a flat block of `key: value` lines between `---` fences at the
very top of a Markdown file. Values are plain strings; empty values are allowed.
"""

import re

FENCE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)

STATUSES = ("draft", "agent-verified", "reviewed", "gold")
VERIFIED_STATUSES = ("agent-verified", "reviewed", "gold")
AI_INVOLVEMENT = ("drafted", "assisted", "none")
REQUIRED_KEYS = ("status", "ai_involvement", "last_verified", "verified_against", "review_by", "reviewers")


def split_front_matter(text):
    """Return (meta_dict, body). Files without front matter return ({}, text)."""
    match = FENCE.match(text)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta, text[match.end():]


def strip_front_matter(text):
    return split_front_matter(text)[1]
