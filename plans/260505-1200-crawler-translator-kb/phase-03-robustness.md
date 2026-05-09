---
phase: 3
status: as-needed
priority: low
effort: 1-3 days (only if needed)
depends_on: phase-01,phase-02
---

# Phase 3: As-Needed Enhancements (Demoted post-Red-Team)

## Context

- Plan: [plan.md](plan.md)
- **Status: AS-NEEDED, không build mặc định.** Chỉ làm khi 1 vấn đề cụ thể block tiến độ.
- **Revisions per Red Team:** #11, #12 — phase này từng là "build all", giờ là menu enhancement.

## Overview

Phase 1 đã có robots.txt, resume, sequential rate-limit (`time.sleep(1/rps)`). Phase này chỉ pick các enhancement khi gặp pain thật.

## Enhancement Menu (Pick On-Demand)

### E1: Async Fetcher (chỉ khi sequential quá chậm)

**Trigger:** Một site có >300 trang VÀ sequential crawl >15 phút.

**Design:**
- `httpx.AsyncClient` thay sync
- `asyncio.Semaphore(rate_limit_rps)` cap concurrency
- **Per-task immediate write** (Finding #11) — không gather-then-write. Mỗi task: `fetch → extract → write` complete rồi mới yield.

**Out:** Sequential vẫn là default. Async chỉ flag opt-in.

### E2: Tenacity Retry (chỉ khi gặp flaky site)

**Trigger:** Lỗi 5xx/timeout xuất hiện >5% requests trong 1 run.

**Design:** `@retry(stop=3, wait=exponential(1,10))` trên fetcher. Log retry attempts.

### E3: Playwright JS Render (chỉ khi cần crawl SPA cụ thể)

**Trigger:** Một target site config với `js_render:true` cần.

**Design:**
- Optional install: `pip install web-easy-learn[js]` group
- Lazy import; CLI first-run check chromium binary, print actionable error nếu thiếu
- Per-page `page.route()` block non-allowlisted hosts (Finding #9 SSRF)
- Pin Playwright version trong `pyproject.toml`, lockfile `uv.lock` với hashes

### E4: Section-aware Chunking cho file to (chỉ khi subagent overflow)

**Trigger:** Phase 2 fail trên file >30K chars.

**Design:** Skill split theo H2 trước khi spawn subagent; ráp lại sau.

### E5: TOC Builder (alphabet/nav-based, không BFS-order)

**Trigger:** User muốn 1 file index để đọc.

**Design:**
- Glob `output/{site}/raw/*.md`, parse frontmatter `title`+`source_url`
- Sort theo URL path (alphabet) HOẶC trích từ site `nav_selector` config nếu có
- Write `_toc.md` plain markdown list
- ❌ KHÔNG dùng BFS crawl-order (Finding: order ≠ pedagogical sequence)

## Out (Removed Entirely)

- ❌ Standalone `rate_limiter.py` module — inline trong fetcher (1 dòng)
- ❌ Standalone `robots.py` — đã xử lý Phase 1 inline
- ❌ Rich Progress bar custom — typer + rich đủ default
- ❌ Strict module split — Phase 1 đã collapse, Phase 3 không re-split

## Decision Process

Trước khi triển khai bất kỳ enhancement nào:
1. Document pain point cụ thể (số liệu: thời gian, % fail, etc.)
2. Pick ENHANCEMENT trong menu trên
3. Implement minimum (không bundling thêm)
4. Stop khi pain hết

## Success Criteria (Per Enhancement)

| Enhancement | Done When |
|---|---|
| E1 Async | 200-page site crawl <5 phút |
| E2 Retry | 0 unrecovered 5xx trong run thực tế |
| E3 Playwright | 1 target SPA crawl ra content giống browser |
| E4 Chunking | File 50K chars dịch không lỗi |
| E5 TOC | `_toc.md` link click được, sort hợp lý |

## Risks

- **Scope creep**: phase này chính là magnet cho gold-plating. Self-discipline: mỗi enhancement có trigger metric rõ ràng, không pre-emptive.

## Next Steps

→ Project complete sau Phase 1+2 cho most cases. Phase 3 reactive only.
