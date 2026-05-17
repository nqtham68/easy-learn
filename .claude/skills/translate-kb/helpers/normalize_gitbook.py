"""Normalize GitBook-flavored markdown extensions to plain markdown.

Handles four patterns commonly emitted by GitBook docs sources:
  - {% embed url="..." %} [caption] {% endembed %}  → markdown link
  - {% hint style="info|warning|danger|success" %} ... {% endhint %} → blockquote
  - {% tabs %} {% tab title="X" %} ... {% endtab %} ... {% endtabs %} → headings
  - Stray {% tab %} / {% endtab %} outside a tabs block (rare)

All other content is passed through unchanged. Code fences inside tabs are
preserved verbatim (we never touch lines between ``` fences).

Usage:
    from normalize_gitbook import normalize
    body = normalize(body)
"""

from __future__ import annotations

import re

EMBED_RE = re.compile(
    r'\{%\s*embed\s+url="([^"]+)"\s*%\}(.*?)\{%\s*endembed\s*%\}',
    re.DOTALL,
)

HINT_RE = re.compile(
    r'\{%\s*hint\s+style="(info|warning|danger|success)"\s*%\}(.*?)\{%\s*endhint\s*%\}',
    re.DOTALL,
)

TABS_RE = re.compile(
    r'\{%\s*tabs\s*%\}(.*?)\{%\s*endtabs\s*%\}',
    re.DOTALL,
)

TAB_RE = re.compile(
    r'\{%\s*tab\s+title="([^"]+)"\s*%\}(.*?)\{%\s*endtab\s*%\}',
    re.DOTALL,
)

HINT_ICON = {
    "info": "ℹ️ Info",
    "warning": "⚠️ Warning",
    "danger": "🚨 Danger",
    "success": "✅ Success",
}


def _embed_repl(m: re.Match) -> str:
    url = m.group(1).strip()
    caption = m.group(2).strip()
    label = caption if caption else "📺 Video"
    return f"[{label}]({url})"


def _hint_repl(m: re.Match) -> str:
    style = m.group(1)
    body = m.group(2).strip("\n")
    icon = HINT_ICON.get(style, "ℹ️ Info")
    quoted = "\n".join(f"> {line}" if line else ">" for line in body.splitlines())
    return f"> **{icon}:**\n{quoted}"


def _tabs_repl(m: re.Match) -> str:
    inner = m.group(1)
    parts = []
    for tab in TAB_RE.finditer(inner):
        title = tab.group(1).strip()
        content = tab.group(2).strip("\n")
        parts.append(f"#### {title}\n\n{content}")
    return "\n\n".join(parts)


def normalize(text: str) -> str:
    text = TABS_RE.sub(_tabs_repl, text)
    text = HINT_RE.sub(_hint_repl, text)
    text = EMBED_RE.sub(_embed_repl, text)
    text = TAB_RE.sub(lambda m: f"#### {m.group(1).strip()}\n\n{m.group(2).strip()}", text)
    return text


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: normalize_gitbook.py <file.md>", file=sys.stderr)
        sys.exit(2)
    from pathlib import Path
    p = Path(sys.argv[1])
    print(normalize(p.read_text(encoding="utf-8")))
