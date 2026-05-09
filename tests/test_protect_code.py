"""Unit tests for code block protection."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "translate-kb" / "helpers"))

from protect_code import has_sentinels, protect, restore


def test_no_code_blocks():
    md = "# Title\n\nJust prose, nothing technical."
    out, blocks = protect(md)
    assert blocks == {}
    assert out == md
    assert restore(out, blocks) == md


def test_python_fence():
    md = "Before\n\n```python\ndef hi():\n    return 42\n```\n\nAfter."
    out, blocks = protect(md)
    assert len(blocks) == 1
    assert "def hi():" not in out
    assert "<<<__WEBEZ_CB_0__>>>" in out
    assert restore(out, blocks) == md


def test_multiple_fences_different_languages():
    md = "```python\nx = 1\n```\n\nMid\n\n```bash\nls -la\n```\n\nEnd."
    out, blocks = protect(md)
    assert len(blocks) == 2
    assert "x = 1" not in out
    assert "ls -la" not in out
    assert restore(out, blocks) == md


def test_inline_code():
    md = "Use `npm install` then `parseInt(value, 10)` to parse."
    out, blocks = protect(md)
    assert len(blocks) == 2
    assert "npm install" not in out
    assert "parseInt" not in out
    assert restore(out, blocks) == md


def test_mixed_fence_and_inline():
    md = (
        "Use the `useState` hook:\n\n"
        "```jsx\nconst [x, setX] = useState(0);\n```\n\n"
        "Then call `setX(value)` to update."
    )
    out, blocks = protect(md)
    assert len(blocks) == 3
    assert "useState" not in out  # both inline + fence content
    assert "setX(value)" not in out
    assert restore(out, blocks) == md


def test_lost_sentinel_raises():
    md = "Code: `x`"
    out, blocks = protect(md)
    # simulate translator dropping the sentinel
    corrupted = out.replace("<<<__WEBEZ_IC_0__>>>", "đã mất")
    with pytest.raises(ValueError, match="sentinel lost"):
        restore(corrupted, blocks)


def test_has_sentinels_detects_leftover():
    assert has_sentinels("text with <<<__WEBEZ_CB_5__>>> remaining")
    assert not has_sentinels("clean text")


def test_byte_equal_preservation():
    """Critical: code body byte-equal pre vs post."""
    original_code = '```python\ndef f(x: int) -> str:\n    """doc"""\n    return f"value={x}"\n```'
    md = f"Wrapper text\n\n{original_code}\n\nMore text."
    out, blocks = protect(md)
    restored = restore(out, blocks)
    assert restored == md
    assert original_code in restored


def test_fence_with_no_language():
    md = "Plain block:\n\n```\nplain text\nno language\n```\n\nDone."
    out, blocks = protect(md)
    assert len(blocks) == 1
    assert "plain text" not in out
    assert restore(out, blocks) == md
