"""Deterministic code-block protection for translation pipeline.

Replace fenced (```...```) and inline (`...`) code with sentinel tokens BEFORE
sending markdown to LLM. After translation, restore byte-equal originals.

Per Red Team Finding #2: prevents LLM from translating/mutating code.
"""

from __future__ import annotations

import re

FENCE_RE = re.compile(r"```[^\n]*\n.*?\n```", re.DOTALL)
INLINE_RE = re.compile(r"`[^`\n]+`")
FENCE_TOKEN = "<<<__WEBEZ_CB_{i}__>>>"
INLINE_TOKEN = "<<<__WEBEZ_IC_{i}__>>>"


def protect(md: str) -> tuple[str, dict[str, str]]:
    """Return (protected_md, blocks). Order: fences first, then inline."""
    blocks: dict[str, str] = {}
    counter = [0]

    def fence_sub(m: re.Match[str]) -> str:
        key = FENCE_TOKEN.format(i=counter[0])
        counter[0] += 1
        blocks[key] = m.group(0)
        return key

    out = FENCE_RE.sub(fence_sub, md)

    def inline_sub(m: re.Match[str]) -> str:
        key = INLINE_TOKEN.format(i=counter[0])
        counter[0] += 1
        blocks[key] = m.group(0)
        return key

    out = INLINE_RE.sub(inline_sub, out)
    return out, blocks


def restore(md: str, blocks: dict[str, str]) -> str:
    """Replace sentinels with originals. Raise if any sentinel missing."""
    for key, original in blocks.items():
        if key not in md:
            raise ValueError(f"sentinel lost in translation: {key}")
        md = md.replace(key, original)
    return md


def has_sentinels(md: str) -> bool:
    """Detect leftover sentinels (validation step post-restore)."""
    return "<<<__WEBEZ_" in md
