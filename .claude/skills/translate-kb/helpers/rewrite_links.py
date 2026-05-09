"""Rewrite upstream documentation URLs to relative local paths.

For each link of form `https://<host>/<path>` where the host matches a known
docs domain, look up the corresponding raw markdown file and replace with a
relative path from the current VN file to the target VN file.

Lookup precedence for `<path>`:
  1. raw/<path>.md
  2. raw/<path>/README.md
  3. raw/<path>/index.md

If no candidate exists, the link is left untouched.

Anchors (#section) and query strings (?x=y) are preserved.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

DOC_HOSTS = {"docs.nats.io"}

# [text](url) — capture group 2 is the URL (possibly with anchor/query)
LINK_RE = re.compile(r"(\[[^\]]*\]\()([^)\s]+)(\))")


def resolve_target(raw_root: Path, url_path: str) -> Path | None:
    rel = url_path.strip("/")
    if not rel:
        return None
    candidates = [
        raw_root / rel,
        raw_root / f"{rel}.md",
        raw_root / rel / "README.md",
        raw_root / rel / "index.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def rewrite_url(
    url: str,
    raw_root: Path,
    vi_root: Path,
    current_vi_file: Path,
) -> str:
    parts = urlsplit(url)
    if parts.scheme in ("http", "https"):
        if parts.netloc not in DOC_HOSTS:
            return url
        path = parts.path
    elif parts.scheme == "" and parts.netloc == "" and url.startswith("/"):
        # Site-root-relative link like /nats-concepts/foo
        path = parts.path
    else:
        return url
    target_raw = resolve_target(raw_root, path)
    if target_raw is None:
        return url
    import os

    rel_from_raw = target_raw.relative_to(raw_root)
    target_vi = vi_root / rel_from_raw
    relative = os.path.relpath(
        str(target_vi.resolve()), str(current_vi_file.parent.resolve())
    ).replace("\\", "/")
    if not relative.startswith((".", "/")):
        relative = "./" + relative
    suffix = ""
    if parts.query:
        suffix += "?" + parts.query
    if parts.fragment:
        suffix += "#" + parts.fragment
    return relative + suffix


def rewrite_file(
    vi_file: Path, raw_root: Path, vi_root: Path
) -> tuple[int, int]:
    """Rewrite links in vi_file in place. Returns (rewritten, total_links)."""
    text = vi_file.read_text(encoding="utf-8")
    rewritten = 0
    total = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal rewritten, total
        total += 1
        head, url, tail = m.group(1), m.group(2), m.group(3)
        new_url = rewrite_url(url, raw_root, vi_root, vi_file)
        if new_url != url:
            rewritten += 1
        return f"{head}{new_url}{tail}"

    new_text = LINK_RE.sub(repl, text)
    if new_text != text:
        vi_file.write_text(new_text, encoding="utf-8")
    return rewritten, total
