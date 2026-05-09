---
phase: 0
status: in_progress
priority: critical
effort: 0.5-1 day
results: spike-results.md
---

# Phase 0: Spike — Verify Foundational Assumptions

> **Progress:** Spike A ✅ PASS (1.86x parallel speedup), Spike C ✅ PASS (10/10), Spike B ⏳ pending user. See [spike-results.md](spike-results.md).

## Context

- Plan: [plan.md](plan.md)
- Added per Red Team Findings #5, #6, #7 — verify before committing implementation effort.

## Overview

Trước khi build, verify 3 giả định mà plan đang dựa vào. Nếu fail, redesign — tránh sunk cost fallacy.

## Spikes

### Spike A: Claude Code Subagent Parallelism (Finding #5)

**Hypothesis:** Spawn N Task subagents trong 1 message → song song thực sự (wall-clock < N×sequential).

**Test:**
1. Tạo 3 file dummy md ~500 lines
2. Spawn 3 Task calls cùng message, mỗi con sleep-then-write (giả lập translation latency)
3. Đo wall-clock vs spawn 3 sequential

**Pass criteria:** Parallel time ≤ 1.5× single task time (proves concurrent execution).

**If fail:** Redesign Phase 2 — drive `claude -p` CLI từ Python với asyncio (real OS-level parallelism), hoặc accept sequential.

### Spike B: NotebookLM Bilingual Format (Finding #6)

<!-- Updated: Validation Session 1 — target site = docs.nats.io/nats-concepts; fallback = VN-only -->

**Hypothesis:** Bilingual format blockquote `> 🇬🇧 *...*` + đoạn VN cho retrieval VN-clean.

**Test:**
1. Manual translate 5 trang từ `docs.nats.io/nats-concepts/*` sang bilingual format
2. Tạo 1 NotebookLM notebook, upload 5 file
3. Query bằng tiếng Việt: 3 câu hỏi cụ thể về NATS concepts
4. Inspect response: có lẫn EN không? Citations chính xác?

**Pass criteria:** Response chủ yếu VN, citations link đúng file, không phun nguyên đoạn EN.

**If fail:** **VN-only output** (validated decision). File `vi/*.md` thuần VN; EN giữ ở `raw/` reference qua `source_url`. Phase 2 conditional logic theo kết quả này.

### Spike C: selectolax → markdownify Code Preservation (Finding #7)

**Hypothesis:** Pipeline `selectolax extract → markdownify` giữ nguyên code blocks với language tag.

**Test:**
1. Tạo `tests/fixtures/code-blocks.html` chứa:
   - `<pre><code class="language-python">def x(): pass</code></pre>`
   - `<pre><code class="language-javascript">const x = 1;</code></pre>`
   - Inline `<code>print()</code>`
   - Bash code block
2. Run pipeline, assert output:
   - Triple backtick fence với `python`, `javascript`, `bash` tag
   - Inline backtick cho `<code>`
   - Body code byte-equal input

**Pass criteria:** All language tags preserved, code unchanged.

**If fail:** Switch to `html2text` hoặc viết custom converter. Pin chính xác markdownify version.

## Todo List

- [ ] Spike A: parallelism test → kết quả wall-clock
- [ ] Spike B: NotebookLM pilot 5 files → kết quả retrieval quality
- [ ] Spike C: code preservation fixture → kết quả pass/fail per language
- [ ] Document findings ở `plans/260505-1200-crawler-translator-kb/spike-results.md`
- [ ] Decide go/no-go cho từng phase based trên kết quả

## Success Criteria

- [ ] All 3 spikes có kết quả binary pass/fail rõ ràng
- [ ] `spike-results.md` ghi rõ next-action nếu fail
- [ ] Plan adjusted nếu cần TRƯỚC khi vào Phase 1

## Next Steps

→ Phase 1 (chỉ khi 3 spike đã pass hoặc đã có fallback design rõ).
