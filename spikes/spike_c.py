"""Spike C: verify selectolax + markdownify preserve code blocks with language tags.

Pass criteria (per phase-00-spike.md):
- Triple-backtick fences with python, javascript, bash language tags
- Inline backtick for <code> elements
- Code body byte-equal to input
"""

from __future__ import annotations

import sys
from pathlib import Path

from selectolax.parser import HTMLParser
from markdownify import markdownify

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "code-blocks.html"


def extract_content(html: str, content_selector: str = "article.main") -> str:
    tree = HTMLParser(html)
    node = tree.css_first(content_selector)
    if node is None:
        raise RuntimeError(f"selector {content_selector!r} matched nothing")
    return node.html


def _code_language(pre_el) -> str:
    """Callback receives <pre>; look at inner <code class='language-xxx'>."""
    code = pre_el.find("code") if pre_el else None
    if code is None:
        return ""
    cls = code.get("class") or []
    for c in cls:
        if c.startswith("language-"):
            return c[len("language-") :]
    return ""


def to_markdown(clean_html: str) -> str:
    return markdownify(
        clean_html,
        heading_style="ATX",
        code_language_callback=_code_language,
    )


def assert_contains(md: str, fragment: str, label: str) -> bool:
    ok = fragment in md
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}: {fragment!r}")
    return ok


def main() -> int:
    print(f"Reading fixture: {FIXTURE}")
    html = FIXTURE.read_text(encoding="utf-8")

    clean = extract_content(html)
    md = to_markdown(clean)

    print("\n=== Generated Markdown ===")
    print(md)
    print("=== End Markdown ===\n")

    print("=== Checks ===")
    checks: list[bool] = []

    # Language tags
    checks.append(assert_contains(md, "```python", "Python fence with lang tag"))
    checks.append(assert_contains(md, "```javascript", "JavaScript fence with lang tag"))
    checks.append(assert_contains(md, "```bash", "Bash fence with lang tag"))

    # Code body byte-equal (key fragments)
    checks.append(assert_contains(md, 'def greet(name: str) -> str:', "Python signature intact"))
    checks.append(assert_contains(md, 'return f"Hello, {name}!"', "Python return intact"))
    checks.append(assert_contains(md, "const fetchUser = async (id) =>", "JS arrow fn intact"))
    checks.append(assert_contains(md, "for f in *.md; do", "Bash loop intact"))

    # Inline code
    checks.append(assert_contains(md, "`npm install`", "Inline code 1"))
    checks.append(assert_contains(md, "`parseInt(value, 10)`", "Inline code 2"))

    # Plain block (no language tag)
    checks.append(assert_contains(md, "plain text code", "Plain block body"))

    passed = sum(checks)
    total = len(checks)
    print(f"\nResult: {passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
