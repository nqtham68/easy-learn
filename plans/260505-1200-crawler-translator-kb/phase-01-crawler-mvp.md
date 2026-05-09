---
phase: 1
status: completed
priority: high
effort: 2-3 days
actual_effort: ~2 hours (single session)
depends_on: phase-00
---

> **Completed 2026-05-05.** All 6 integration tests pass. crawler.py + cli.py + sites/nats-docs.yaml + tests/test_integration.py + tests/fixtures/site/ in place.

# Phase 1: Crawler MVP (Revised post-Red-Team)

## Context

- Brainstorm: [../reports/brainstorm-260505-web-crawler-translator.md](../reports/brainstorm-260505-web-crawler-translator.md)
- Plan: [plan.md](plan.md)
- Spike kết quả: phase-00 phải pass trước khi vào phase này.
- **Revisions per Red Team:** #1, #2, #4, #8, #9, #10, #13, #14, #15

## Overview

Build crawler **single-file (`crawler.py`) + cli.py**. Sequential, sync httpx, BFS với resume-on-restart, write atomically với HTML sanitization, SSRF guard, path traversal protection, secret scrub.

## Key Insights (post-Red-Team)

- **Over-modularization là YAGNI**: 1 file `crawler.py` ~150 lines đủ. Split sau khi thực sự cần.
- **Resume MUST work in Phase 1**: skip URL nếu file output đã tồn tại với frontmatter valid.
- **Security KHÔNG defer được**: SSRF, path traversal, HTML sanitize, secret scrub — bake vào MVP.
- **robots.txt vào Phase 1** (di chuyển từ Phase 3) với default-deny on parse error.

## Requirements

### Functional
- Đọc YAML site config qua `yaml.safe_load` (Finding #14)
- Validate config với pydantic schema; reject `start_urls` không phải `https`
- BFS từ start_urls, link discovery qua `link_selector`
- **Resume**: skip URL nếu `output/{site}/raw/<path>.md` đã tồn tại + frontmatter parse OK + `translated:false` (Finding #10)
- Fetch HTML qua httpx sync, **với SSRF guard** (Finding #9)
- robots.txt fetch + check trước fetch URL; default deny nếu parse fail (Finding #15)
- Sanitize HTML trước extract: bleach/nh3 strip `script`, `style`, `iframe`, `on*=`, `javascript:`, HTML comments (Finding #3)
- Extract content qua `content_selector`, exclude `exclude_selectors`
- Convert HTML→Markdown với markdownify (verified Phase 0)
- Atomic write: `.tmp` rồi `os.rename` (Finding #4)
- Frontmatter qua `python-frontmatter` lib (Finding #14)
- Strip query string + fragment khỏi `source_url` (Finding #15)
- `output/` vào `.gitignore` mặc định
- CLI: `python crawler.py crawl sites/<x>.yaml` + rich progress

### Non-functional
- **2 file Python**: `crawler.py` + `cli.py`. Không có `src/crawler/`, `src/writer/`, `src/config/` (Finding #13)
- Sequential fetch với `time.sleep(1.0/rps)` (Finding #12 — async không cần ở MVP)
- Errors: log + skip URL lỗi, không crash run

## Architecture

```
crawler.py (~200 lines):
  load_config(yaml_path) → SiteConfig (pydantic, safe_load)
  is_safe_url(url) → bool      # SSRF guard
  fetch(url, robots) → str | None
  sanitize_html(html) → str    # bleach
  extract(html, sel, excl) → str
  to_markdown(clean_html) → str
  safe_path(url, root) → Path  # path traversal + Windows-safe
  write_atomic(path, content, meta) → bool
  crawl(config) → CrawlReport  # BFS với resume

cli.py (~30 lines):
  typer command crawl <yaml>
```

## Site Config (YAML)
```yaml
name: react-docs
start_urls: [https://react.dev/learn]
allow_domains: [react.dev]
link_selector: "nav.sidebar a[href]"
content_selector: "article.main"
exclude_selectors: [".edit-page", "footer"]
max_depth: 3
max_pages: 500
rate_limit_rps: 1
respect_robots: true        # default true; --ignore-robots flag để override
```

## Frontmatter Output
```yaml
---
source_url: https://react.dev/learn  # query stripped
crawled_at: 2026-05-05T10:00:00Z
title: Quick Start
translated: false
---
```

❌ Không còn field `order` (Finding: BFS order ≠ reading order, drop unfounded claim)

## Related Code Files

**To create:**
- `pyproject.toml` — deps: `httpx`, `selectolax`, `markdownify`, `pyyaml`, `pydantic`, `python-frontmatter`, `bleach`, `pathvalidate`, `typer`, `rich`
- `crawler.py`
- `cli.py`
- `sites/nats-docs.yaml` (target validation: docs.nats.io/nats-concepts)
- `tests/fixtures/code-blocks.html` (từ Phase 0)
- `tests/test_integration.py` — chạy crawler trên fixture local
- `.gitignore` — thêm `output/`, `__pycache__/`, `.venv/`

## Implementation Steps

1. **Project scaffold**: `pyproject.toml` + `.gitignore` (`output/` included). `uv` hoặc `pip install -e .`.
2. **Config**: pydantic `SiteConfig`. `load_config(p)` dùng `yaml.safe_load`. Reject `start_urls` schema khác `https`.
3. **SSRF guard**: `is_safe_url(url)` — parse hostname, `socket.getaddrinfo`, reject IP private (`ipaddress.ip_address.is_private/is_loopback/is_link_local/is_multicast`), reject schemes ngoài `http`/`https`. Disable redirects qua `httpx.Client(follow_redirects=False)`; nếu cần follow, manual + re-check `is_safe_url`.
4. **robots.txt**: cache `RobotFileParser` per domain. Fetch fail/parse fail → return deny. CLI flag `--ignore-robots` để override (default off).
5. **Fetcher**: `httpx.Client(timeout=30, headers={"User-Agent": "..."})`. Retry policy ở Phase 3, Phase 1 chỉ try 1 lần.
6. **HTML sanitize**: `bleach.clean(html, tags=ALLOWED, attributes=ALLOWED_ATTRS, strip_comments=True)`. ALLOWED = standard markdown HTML (h1-6, p, code, pre, a, em, strong, ul, ol, li, blockquote, table v.v.). Strict — drop unknown.
7. **Extractor**: selectolax parse, drop `exclude_selectors` nodes, return `content_selector.html`.
8. **HTML→MD**: `markdownify.markdownify(clean_html, heading_style="ATX")`. Verify code preservation đã pass Phase 0; nếu cần custom callback cho `code_language`, viết tại đây.
9. **Path safety**: `safe_path(url, root)` —
   - Strip query/fragment
   - Sanitize Windows reserved names + length qua `pathvalidate.sanitize_filename`
   - `candidate = (root / parsed.netloc / parsed.path.lstrip('/')).with_suffix('.md')`
   - `assert candidate.resolve().is_relative_to(root.resolve())` else raise
10. **Atomic write**: write `path.with_suffix('.md.tmp')` → `os.replace(tmp, path)`. Frontmatter qua `python-frontmatter.dumps`.
11. **Resume check**: trước fetch, nếu `path` đã exist → load frontmatter, nếu valid → skip + count.
12. **BFS Discoverer**: queue + visited (URL normalized). Per URL: check `is_safe_url`, robots, allow_domains, depth/max_pages caps. Extract links bằng `link_selector`, normalize qua `urljoin`.
13. **CLI**: typer, rich.Progress.
14. **Test**: trên fixture local (4-5 file HTML trong `tests/fixtures/site/`), không hit network. Verify output structure + frontmatter + code blocks intact + resume skip.

## Todo List

- [ ] `pyproject.toml` + `.gitignore` với `output/`
- [ ] `crawler.py` skeleton (functions stubs)
- [ ] pydantic `SiteConfig` + `yaml.safe_load`
- [ ] `is_safe_url` + ipaddress check
- [ ] robots.txt với default-deny on error
- [ ] httpx fetcher + redirects=False
- [ ] HTML sanitize bleach
- [ ] extractor + html_to_md (use Phase 0 fixture)
- [ ] `safe_path` + pathvalidate + is_relative_to assert
- [ ] atomic write + python-frontmatter
- [ ] BFS với resume skip
- [ ] `cli.py` typer
- [ ] `sites/nats-docs.yaml` (start_urls: https://docs.nats.io/nats-concepts)
- [ ] `tests/test_integration.py` trên fixture local
- [ ] End-to-end run trên 1 site thật ~30 trang
- [ ] Compile check: `python crawler.py --help`

## Success Criteria

- [ ] `python crawler.py crawl sites/<x>.yaml` chạy không crash
- [ ] Re-run skip file đã có (proven by log "skipped 30/30")
- [ ] SSRF: config với `start_urls: [http://169.254.169.254]` → reject + log
- [ ] Path traversal: URL `/../../../etc/passwd` → reject (test fixture)
- [ ] robots.txt 503 → default deny + log warn (proven test)
- [ ] Sanitize: fixture HTML có `<script>alert(1)</script>` → output không chứa
- [ ] Code blocks Python/JS/Bash từ Phase 0 fixture preserved 100%
- [ ] `source_url` frontmatter không chứa query string
- [ ] `output/` trong `.gitignore`

## Risk Assessment

| Risk | Mitigation |
|---|---|
| bleach quá strict drop content cần thiết | Whitelist `<details>`, `<summary>`, `<table>`, etc; tune theo target site |
| python-frontmatter conflict với markdown body có `---` | Lib handle correctly (anchored top); tested in unit |
| Atomic rename fail trên Windows nếu target locked | Catch + retry 1 lần; log nếu fail vĩnh viễn |
| pathvalidate over-sanitize cần character | Test trên list URL thật của site target |

## Security Considerations

- SSRF guard mandatory; không bypass được dù personal use
- robots.txt default-deny on error
- HTML sanitize trước extract → defense in depth cho Phase 2 prompt injection
- `output/` luôn trong `.gitignore` — secret scrub nguyên tắc
- `source_url` strip query/fragment trước write
- User-agent rõ: `web-easy-learn/0.x (+contact-email)`

## Next Steps

→ Phase 2: dùng output Phase 1 để build translator skill.
