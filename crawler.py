"""Single-file crawler for web-easy-learn (Phase 1).

Honors Red-Team findings: yaml.safe_load, SSRF guard, robots.txt deny-on-error,
HTML sanitize, path traversal guard, atomic write, BFS resume.
"""

from __future__ import annotations

import ipaddress
import logging
import socket
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.robotparser import RobotFileParser

import bleach
import frontmatter
import httpx
import yaml
from markdownify import markdownify
from pathvalidate import sanitize_filename
from pydantic import BaseModel, Field, field_validator
from selectolax.parser import HTMLParser

log = logging.getLogger("crawler")

USER_AGENT = "web-easy-learn/0.1 (+https://github.com/web-easy-learn)"

ALLOWED_TAGS = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "br", "hr",
    "strong", "em", "code", "pre", "kbd", "var", "samp", "del", "ins", "sub", "sup",
    "a", "img",
    "ul", "ol", "li", "dl", "dt", "dd",
    "blockquote", "q", "cite",
    "table", "thead", "tbody", "tr", "th", "td",
    "div", "span", "section", "article", "main", "aside", "nav", "header", "footer",
    "details", "summary", "figure", "figcaption",
]
ALLOWED_ATTRS = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
    "code": ["class"],
    "pre": ["class"],
    "th": ["align"], "td": ["align"],
    "*": ["id"],
}


class SiteConfig(BaseModel):
    name: str
    start_urls: list[str]
    allow_domains: list[str]
    link_selector: str
    content_selector: str
    exclude_selectors: list[str] = Field(default_factory=list)
    max_depth: int = 3
    max_pages: int = 500
    rate_limit_rps: float = 1.0
    respect_robots: bool = True

    @field_validator("start_urls")
    @classmethod
    def _https_only(cls, urls: list[str]) -> list[str]:
        for u in urls:
            scheme = urlparse(u).scheme
            if scheme not in ("http", "https"):
                raise ValueError(f"start_url must be http/https, got {u!r}")
        return urls


def load_config(path: Path) -> SiteConfig:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return SiteConfig(**raw)


def is_safe_url(url: str) -> bool:
    """Reject schemes outside http(s) and IPs in private/loopback/link-local/multicast."""
    p = urlparse(url)
    if p.scheme not in ("http", "https"):
        return False
    host = p.hostname
    if not host:
        return False
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
            return False
    return True


class RobotsCache:
    def __init__(self, client: httpx.Client, respect: bool):
        self._client = client
        self._respect = respect
        self._cache: dict[str, RobotFileParser | None] = {}

    def can_fetch(self, url: str) -> bool:
        if not self._respect:
            return True
        p = urlparse(url)
        origin = f"{p.scheme}://{p.netloc}"
        if origin not in self._cache:
            rp = RobotFileParser()
            try:
                resp = self._client.get(f"{origin}/robots.txt", timeout=10)
                if resp.status_code >= 400:
                    self._cache[origin] = None  # deny on error
                    log.warning("robots.txt %s returned %d, deny-by-default", origin, resp.status_code)
                    return False
                rp.parse(resp.text.splitlines())
                self._cache[origin] = rp
            except Exception as e:
                self._cache[origin] = None
                log.warning("robots.txt %s fetch failed: %s — deny-by-default", origin, e)
                return False
        rp = self._cache[origin]
        if rp is None:
            return False
        return rp.can_fetch(USER_AGENT, url)


def extract_and_sanitize(html: str, content_selector: str, exclude_selectors: Iterable[str]) -> str:
    """Drop unwanted nodes (using raw HTML attributes), pick content, then sanitize.

    Order matters: bleach strips most attributes (aria-label, data-*, class) so
    exclude_selectors that key on those must run BEFORE sanitize.
    """
    tree = HTMLParser(html)
    # Drop dangerous tags entirely (bleach strip=True keeps inner text)
    for tag in ("script", "style", "noscript", "template"):
        for n in tree.css(tag):
            n.decompose()
    # Drop excluded selectors (raw attributes still available)
    for sel in exclude_selectors:
        for n in tree.css(sel):
            n.decompose()
    node = tree.css_first(content_selector)
    if node is None:
        return ""
    return bleach.clean(
        node.html or "",
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
        strip_comments=True,
    )


def _code_language(pre_el) -> str:
    code = pre_el.find("code") if pre_el else None
    if code is None:
        return ""
    cls = code.get("class") or []
    for c in cls:
        if c.startswith("language-"):
            return c[len("language-") :]
    return ""


def to_markdown(clean_html: str) -> str:
    return markdownify(clean_html, heading_style="ATX", code_language_callback=_code_language)


def safe_path(url: str, root: Path, site_name: str) -> Path:
    """Map URL to filesystem path under root/{site}/raw/, with traversal + Windows-safe guards."""
    p = urlparse(url)
    parts: list[str] = []
    for raw in p.path.strip("/").split("/"):
        if not raw or raw in ("..", "."):
            continue
        parts.append(sanitize_filename(raw, replacement_text="_"))
    if not parts:
        parts = ["index"]
    parts[-1] = parts[-1] + ".md"
    candidate = (root / site_name / "raw").joinpath(*parts)
    candidate_resolved = candidate.resolve()
    root_resolved = (root / site_name).resolve()
    if not str(candidate_resolved).startswith(str(root_resolved)):
        raise ValueError(f"path traversal attempt: {url}")
    return candidate


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8", newline="\n")
    tmp.replace(path)


def strip_url(url: str) -> str:
    """Remove fragment + query (Red Team #15: secret leak via source_url)."""
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}{p.path}"


def is_translated_already(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        post = frontmatter.load(path)
        return bool(post.metadata.get("source_url"))
    except Exception:
        return False


def discover_links(html: str, base_url: str, link_selector: str) -> list[str]:
    tree = HTMLParser(html)
    out: list[str] = []
    for a in tree.css(link_selector):
        href = a.attributes.get("href")
        if not href:
            continue
        absolute, _ = urldefrag(urljoin(base_url, href))
        out.append(absolute)
    return out


@dataclass
class CrawlReport:
    fetched: int = 0
    skipped: int = 0
    failed: int = 0
    written: int = 0


def crawl(config: SiteConfig, output_root: Path, ignore_robots: bool = False) -> CrawlReport:
    report = CrawlReport()
    sleep = 1.0 / config.rate_limit_rps

    with httpx.Client(
        timeout=30,
        headers={"User-Agent": USER_AGENT},
        follow_redirects=True,  # auto-follow; verify final hostname after
    ) as client:
        robots = RobotsCache(client, respect=config.respect_robots and not ignore_robots)

        queue: deque[tuple[str, int]] = deque((u, 0) for u in config.start_urls)
        visited: set[str] = set()

        while queue and (report.written + report.skipped) < config.max_pages:
            url, depth = queue.popleft()
            url = strip_url(url)
            if url in visited:
                continue
            visited.add(url)

            if depth > config.max_depth:
                continue
            if not is_safe_url(url):
                log.warning("unsafe url skipped: %s", url)
                report.failed += 1
                continue
            if urlparse(url).hostname not in config.allow_domains:
                continue
            if not robots.can_fetch(url):
                log.info("robots disallow: %s", url)
                report.skipped += 1
                continue

            target = safe_path(url, output_root, config.name)
            already = is_translated_already(target)

            try:
                resp = client.get(url)
                if resp.status_code >= 400:
                    log.warning("HTTP %d for %s", resp.status_code, url)
                    report.failed += 1
                    continue
                # Post-redirect domain check (SSRF defense)
                final_host = urlparse(str(resp.url)).hostname
                if final_host not in config.allow_domains:
                    log.warning("redirected off-domain: %s -> %s", url, resp.url)
                    report.failed += 1
                    continue
                # Use final URL as canonical (handles trailing-slash redirects)
                final_url = strip_url(str(resp.url))
                if final_url != url:
                    if final_url in visited:
                        continue
                    visited.add(final_url)
                    target = safe_path(final_url, output_root, config.name)
                    already = is_translated_already(target)
                    url = final_url
                html = resp.text
                if not already:
                    report.fetched += 1
            except Exception as e:
                log.warning("fetch failed %s: %s", url, e)
                report.failed += 1
                continue

            if already:
                log.info("resume skip: %s", target.name)
                report.skipped += 1
                # still discover links to keep BFS frontier consistent
                for link in discover_links(html, url, config.link_selector):
                    link = strip_url(link)
                    if link not in visited:
                        queue.append((link, depth + 1))
                continue

            inner = extract_and_sanitize(html, config.content_selector, config.exclude_selectors)
            if not inner.strip():
                log.warning("empty extraction: %s", url)
                report.failed += 1
            else:
                md_body = to_markdown(inner)
                inner_tree = HTMLParser(inner)
                title_node = (
                    inner_tree.css_first("h1")
                    or inner_tree.css_first("h2")
                    or inner_tree.css_first("h3")
                )
                title = title_node.text(strip=True) if title_node else urlparse(url).path.rstrip("/").rsplit("/", 1)[-1] or "index"
                post = frontmatter.Post(
                    md_body,
                    source_url=url,
                    crawled_at=datetime.now(timezone.utc).isoformat(),
                    title=title,
                    translated=False,
                )
                atomic_write(target, frontmatter.dumps(post))
                report.written += 1
                log.info("[%d] wrote %s", report.written, target.relative_to(output_root))

            # discover from raw HTML (not sanitized — links may be in stripped tags)
            for link in discover_links(html, url, config.link_selector):
                link = strip_url(link)
                if link not in visited:
                    queue.append((link, depth + 1))

            time.sleep(sleep)

    return report
