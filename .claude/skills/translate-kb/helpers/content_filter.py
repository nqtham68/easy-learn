"""Detect low-content markdown files to skip translation.

A file is "low-content" if either:
  - Stripped prose has fewer than MIN_WORDS words, OR
  - Among non-blank, non-heading body lines, more than MAX_LINK_RATIO are
    pure link-only lines (bulleted or bare).

Stripping removes: frontmatter, fenced code, inline code, images, HTML
comments, headings, link URLs (keeping link text).
"""

from __future__ import annotations

import re
from pathlib import Path

import frontmatter

MIN_WORDS = 20
MAX_LINK_RATIO = 0.8

FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
LINK_ONLY_LINE_RE = re.compile(
    r"^\s*(?:[-*+]\s+)?\[[^\]]+\]\([^)]+\)\s*[-:].*$|^\s*(?:[-*+]\s+)?\[[^\]]+\]\([^)]+\)\s*$"
)


def strip_to_prose(body: str) -> str:
    body = FENCE_RE.sub(" ", body)
    body = HTML_COMMENT_RE.sub(" ", body)
    body = IMAGE_RE.sub(" ", body)
    body = INLINE_CODE_RE.sub(" ", body)
    body = LINK_RE.sub(r"\1", body)
    out_lines = []
    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        out_lines.append(s)
    return " ".join(out_lines)


def link_line_ratio(body: str) -> float:
    body = FENCE_RE.sub("", body)
    lines = [
        ln for ln in body.splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    if not lines:
        return 0.0
    link_lines = sum(1 for ln in lines if LINK_ONLY_LINE_RE.match(ln))
    return link_lines / len(lines)


def classify(raw_path: Path) -> tuple[bool, str]:
    """Return (is_low_content, reason). reason is empty if not low-content."""
    post = frontmatter.load(raw_path)
    body = post.content
    prose = strip_to_prose(body)
    words = prose.split()
    word_count = len(words)
    if word_count < MIN_WORDS:
        return True, f"prose<{MIN_WORDS}words ({word_count})"
    ratio = link_line_ratio(body)
    if ratio > MAX_LINK_RATIO:
        return True, f"link-list ({ratio:.0%} link lines)"
    return False, ""


def write_stub(raw_path: Path, vi_path: Path, reason: str) -> None:
    post = frontmatter.load(raw_path)
    post.metadata["translated"] = "skipped"
    post.metadata["skip_reason"] = reason
    vi_path.parent.mkdir(parents=True, exist_ok=True)
    vi_path.write_text(frontmatter.dumps(post), encoding="utf-8")
