"""Integration test for crawler — serves fixture via local HTTP, runs crawl, asserts output."""

from __future__ import annotations

import http.server
import socketserver
import threading
import time
from pathlib import Path

import frontmatter
import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from crawler import SiteConfig, crawl, is_safe_url, safe_path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "site"


@pytest.fixture(scope="module")
def server():
    """Serve fixtures on localhost — note: is_safe_url rejects loopback so we patch."""
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(*a, directory=str(FIXTURE_DIR), **kw)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.2)
    yield port
    httpd.shutdown()


@pytest.fixture
def output_dir(tmp_path):
    return tmp_path / "output"


def test_safe_path_traversal_sanitized(tmp_path):
    """Red Team #8: ../ segments stripped; result stays under output root."""
    p = safe_path("https://x.com/../../../etc/passwd", tmp_path, "site")
    site_root = (tmp_path / "site").resolve()
    assert str(p.resolve()).startswith(str(site_root))
    assert ".." not in p.parts


def test_safe_path_normal(tmp_path):
    p = safe_path("https://example.com/learn/intro", tmp_path, "site")
    assert p.suffix == ".md"
    assert "learn" in p.parts
    assert "intro.md" == p.name


def test_is_safe_url_blocks_private():
    """Red Team #9: SSRF — private IPs rejected."""
    assert not is_safe_url("http://127.0.0.1/")
    assert not is_safe_url("http://169.254.169.254/")
    assert not is_safe_url("http://10.0.0.1/")
    assert not is_safe_url("file:///etc/passwd")


def test_is_safe_url_allows_public():
    assert is_safe_url("https://docs.nats.io/")


def test_crawl_e2e(server, output_dir, monkeypatch):
    """E2E: crawl fixture site, verify output structure + sanitization + frontmatter."""
    # Bypass SSRF guard for loopback fixture
    monkeypatch.setattr("crawler.is_safe_url", lambda url: True)

    port = server
    config = SiteConfig(
        name="fixture",
        start_urls=[f"http://127.0.0.1:{port}/index.html"],
        allow_domains=["127.0.0.1"],
        link_selector="main a[href]",
        content_selector="main",
        exclude_selectors=["nav", "script"],
        max_depth=2,
        max_pages=10,
        rate_limit_rps=10,  # fast for test
        respect_robots=False,
    )
    report = crawl(config, output_root=output_dir, ignore_robots=True)

    assert report.written >= 3, f"expected >=3 pages, got {report.written}"

    raw = output_dir / "fixture" / "raw"
    files = list(raw.rglob("*.md"))
    assert len(files) >= 3

    # Verify XSS sanitization
    index_md = next(p for p in files if "index" in p.name)
    content = index_md.read_text(encoding="utf-8")
    assert "alert(" not in content, "script tag must be sanitized"
    assert "javascript:" not in content, "javascript: URI must be filtered"

    # Verify frontmatter
    post = frontmatter.load(index_md)
    assert post.metadata["translated"] is False
    assert post.metadata["source_url"].startswith("http://127.0.0.1")
    assert "?" not in post.metadata["source_url"]  # query stripped
    assert post.metadata.get("title")

    # Verify code preservation (page-a)
    page_a = next(p for p in files if "page-a" in p.name)
    a_content = page_a.read_text(encoding="utf-8")
    assert "```python" in a_content
    assert 'def hello():' in a_content
    assert "`inline code`" in a_content


def test_resume_skip(server, output_dir, monkeypatch):
    """Red Team #10: resume — second run must skip existing files."""
    monkeypatch.setattr("crawler.is_safe_url", lambda url: True)

    port = server
    config = SiteConfig(
        name="fixture",
        start_urls=[f"http://127.0.0.1:{port}/index.html"],
        allow_domains=["127.0.0.1"],
        link_selector="main a[href]",
        content_selector="main",
        exclude_selectors=["nav", "script"],
        max_depth=2,
        max_pages=10,
        rate_limit_rps=10,
        respect_robots=False,
    )
    # First run
    r1 = crawl(config, output_root=output_dir, ignore_robots=True)
    assert r1.written >= 3

    # Second run — same output dir, must skip
    r2 = crawl(config, output_root=output_dir, ignore_robots=True)
    assert r2.skipped >= 3, f"expected resume skip, got skipped={r2.skipped}, written={r2.written}"
    assert r2.written == 0
