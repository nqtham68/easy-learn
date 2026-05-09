"""E2E test for cli_protect.py wrapper script."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import frontmatter
import pytest

ROOT = Path(__file__).resolve().parent.parent
WRAPPER = ROOT / ".claude" / "skills" / "translate-kb" / "helpers" / "cli_protect.py"
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"

SAMPLE_RAW = """\
---
source_url: https://example.com/learn/intro
title: Quick Start
crawled_at: '2026-05-05T10:00:00Z'
translated: false
---

# Quick Start

This is the introduction paragraph.

```python
def hello():
    print("hi")
```

Use `npm install` then read more.
"""


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(PYTHON), str(WRAPPER), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def test_protect_then_restore_roundtrip(tmp_path):
    raw = tmp_path / "raw.md"
    raw.write_text(SAMPLE_RAW, encoding="utf-8")

    tmp_input = tmp_path / "tmp_input.md"
    blocks_json = tmp_path / "blocks.json"

    res = run("protect", str(raw), str(tmp_input), str(blocks_json))
    assert res.returncode == 0, res.stderr

    protected = tmp_input.read_text(encoding="utf-8")
    blocks = json.loads(blocks_json.read_text(encoding="utf-8"))

    # Protected content has sentinels, no original code
    assert "<<<__WEBEZ_CB_0__>>>" in protected
    assert "<<<__WEBEZ_IC_1__>>>" in protected
    assert "def hello()" not in protected
    assert "npm install" not in protected
    assert len(blocks) == 2

    # Simulate subagent: translates prose, marks translated:true, keeps tokens
    fake_translated = protected.replace(
        "# Quick Start", "# Bắt đầu nhanh"
    ).replace(
        "This is the introduction paragraph.",
        "Đây là đoạn giới thiệu.",
    ).replace(
        "Use", "Sử dụng"
    ).replace(
        " then read more.", " rồi đọc tiếp."
    )
    post = frontmatter.loads(fake_translated)
    post["title"] = "Bắt đầu nhanh"
    post["translated"] = True
    post["translated_at"] = "2026-05-05T11:00:00Z"

    sub_out = tmp_path / "sub_out.md"
    sub_out.write_text(frontmatter.dumps(post), encoding="utf-8")

    final = tmp_path / "vi" / "final.md"
    res = run("restore", str(sub_out), str(blocks_json), str(final))
    assert res.returncode == 0, res.stderr

    restored = final.read_text(encoding="utf-8")
    # Code byte-equal
    assert "```python\ndef hello():\n    print(\"hi\")\n```" in restored
    assert "`npm install`" in restored
    # No leftover sentinels
    assert "<<<__WEBEZ_" not in restored
    # Frontmatter updated
    rp = frontmatter.loads(restored)
    assert rp["translated"] is True
    assert rp["title"] == "Bắt đầu nhanh"


def test_restore_rejects_missing_translated_flag(tmp_path):
    """Restore must fail if subagent forgot to set translated:true."""
    raw = tmp_path / "raw.md"
    raw.write_text(SAMPLE_RAW, encoding="utf-8")
    tmp_input = tmp_path / "tmp_input.md"
    blocks_json = tmp_path / "blocks.json"
    run("protect", str(raw), str(tmp_input), str(blocks_json))

    # Subagent output without translated:true
    sub_out = tmp_path / "sub_out.md"
    sub_out.write_text(tmp_input.read_text(encoding="utf-8"), encoding="utf-8")  # unchanged
    final = tmp_path / "final.md"

    res = run("restore", str(sub_out), str(blocks_json), str(final))
    assert res.returncode != 0
    assert "translated != true" in res.stderr


def test_restore_rejects_lost_sentinel(tmp_path):
    """If subagent dropped a sentinel, restore must fail and not write."""
    raw = tmp_path / "raw.md"
    raw.write_text(SAMPLE_RAW, encoding="utf-8")
    tmp_input = tmp_path / "tmp_input.md"
    blocks_json = tmp_path / "blocks.json"
    run("protect", str(raw), str(tmp_input), str(blocks_json))

    content = tmp_input.read_text(encoding="utf-8")
    # Drop one sentinel
    corrupted = content.replace("<<<__WEBEZ_CB_0__>>>", "[code removed]")
    post = frontmatter.loads(corrupted)
    post["translated"] = True

    sub_out = tmp_path / "sub_out.md"
    sub_out.write_text(frontmatter.dumps(post), encoding="utf-8")
    final = tmp_path / "final.md"

    res = run("restore", str(sub_out), str(blocks_json), str(final))
    assert res.returncode != 0
    assert "sentinel lost" in res.stderr
    assert not final.exists()
