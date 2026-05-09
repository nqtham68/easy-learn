"""Wrap bare URLs in markdown files so they become clickable.

Bare URLs (not already part of `[text](url)`, `<url>`, `href="url"`, an image,
or inside code) are wrapped in HTML `<a>` tags. HTML wrapping is required
because some bare URLs in this corpus appear inside literal `<p>...</p>`
blocks, where Markdown auto-link syntax (`<url>`) is not processed.

Usage:
  python linkify_urls.py <vi-root> [<file>...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Match a bare URL not preceded by `(`, `[`, `=`, `<`, `"`, `'`, `/` (avoids
# wrapping URLs already inside markdown/HTML constructs).
URL_RE = re.compile(
    r"(?<![\w(\[<=\"'/])"
    r"(https?://[^\s<>\"')]+[^\s<>\"'.,;:!?)\]])"
)
FENCE_RE = re.compile(r"(```.*?```)", re.DOTALL)
INLINE_CODE_RE = re.compile(r"(`[^`\n]+`)")
EXISTING_LINK_RE = re.compile(r"\[[^\]]*\]\([^)]*\)")


def linkify_segment(text: str) -> str:
    # Mask existing markdown links so URLs inside them are not double-wrapped.
    placeholders: list[str] = []

    def stash(m: re.Match[str]) -> str:
        placeholders.append(m.group(0))
        return f"\x00{len(placeholders) - 1}\x00"

    masked = EXISTING_LINK_RE.sub(stash, text)
    masked = URL_RE.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', masked)
    return re.sub(r"\x00(\d+)\x00", lambda m: placeholders[int(m.group(1))], masked)


def linkify(text: str) -> str:
    out: list[str] = []
    # Split by fenced code blocks first, then by inline code, leaving those
    # segments untouched.
    fence_parts = FENCE_RE.split(text)
    for i, fp in enumerate(fence_parts):
        if i % 2 == 1:
            out.append(fp)
            continue
        inline_parts = INLINE_CODE_RE.split(fp)
        for j, ip in enumerate(inline_parts):
            if j % 2 == 1:
                out.append(ip)
            else:
                out.append(linkify_segment(ip))
    return "".join(out)


FRONTMATTER_RE = re.compile(r"\A(---\r?\n.*?\r?\n---\r?\n)", re.DOTALL)
STRAY_HTML_TAG_RE = re.compile(r"^\s*</?(html|body)>\s*$", re.MULTILINE | re.IGNORECASE)


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if m:
        head, body = m.group(1), text[m.end():]
        body = STRAY_HTML_TAG_RE.sub("", body)
        new = head + linkify(body)
    else:
        body = STRAY_HTML_TAG_RE.sub("", text)
        new = linkify(body)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return 1
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2
    root = Path(argv[0]).resolve()
    files = [Path(p).resolve() for p in argv[1:]] or sorted(root.rglob("*.md"))
    changed = 0
    for f in files:
        changed += process_file(f)
    print(f"linkified: {changed}/{len(files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
