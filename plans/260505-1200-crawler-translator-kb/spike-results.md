---
type: spike-results
date: 2026-05-05
phase: 0
---

# Phase 0 Spike Results

## Spike A: Claude Code Subagent Parallelism

**Test method:** Spawn 3 `general-purpose` subagents in 1 message, mỗi con write start timestamp + `time.sleep(5)` + write end timestamp. Analyze overlap.

**Raw data:**
| Agent | Start (relative) | End (relative) | Duration |
|---|---|---|---|
| 1 | 0.00s | 5.00s | 5.00s |
| 2 | 2.06s | 7.06s | 5.00s |
| 3 | 3.06s | 8.06s | 5.00s |

**Metrics:**
- Wall-clock span: **8.06s**
- Sum of durations (sequential estimate): 15.00s
- Speedup: **1.86x** (53% of ideal 3x)
- Start-time spread: 3.06s

**Verdict: PASS với caveat**

✅ Subagents chạy concurrent (không sequential).
⚠️ Có stagger ~1-2s giữa start times — không phải fully simultaneous, nhưng đủ song song hữu ích.

**Implication for Phase 2:**
- Batch=3 vẫn đáng dùng (1.86x speedup)
- Không cần fallback `claude -p` CLI Python orchestration
- Document expectation: throughput ~50-60% of theoretical batch×N

## Spike C: selectolax + markdownify Code Preservation

**Test:** `tests/fixtures/code-blocks.html` qua `spikes/spike_c.py`. Verify language tags + body byte-equal.

**Initial run:** 7/10 PASS — language tags missing.
**Root cause:** markdownify default không đọc `class="language-xxx"` từ `<code>` con bên trong `<pre>`.
**Fix:** custom `code_language_callback` đọc child `<code>.class`.

**Final run: 10/10 PASS** ✅

| Check | Result |
|---|---|
| Python fence with `python` lang tag | PASS |
| JavaScript fence with `javascript` lang tag | PASS |
| Bash fence with `bash` lang tag | PASS |
| Python signature byte-equal | PASS |
| Python return statement intact | PASS |
| JS arrow function intact | PASS |
| Bash loop intact | PASS |
| Inline code 1 (`npm install`) | PASS |
| Inline code 2 (`parseInt(value, 10)`) | PASS |
| Plain block (no language) body intact | PASS |

**Verdict: PASS**

**Implication for Phase 1:**
- Use `markdownify(html, heading_style="ATX", code_language_callback=...)` với callback đọc `<pre> > <code>.class[language-*]`
- Pin `markdownify>=0.13` (current 0.13 verified)
- Reference implementation: [spikes/spike_c.py](../../spikes/spike_c.py)

## Spike B: NotebookLM Bilingual Format — PENDING USER

**Status:** Cần user manual (Claude không upload NotebookLM được).

**Instructions:** [../../spikes/spike_b_instructions.md](../../spikes/spike_b_instructions.md)

**Required:**
1. User dịch 5 trang NATS docs sang bilingual format
2. Upload lên NotebookLM
3. Test 3 query VN
4. Update section "Spike B Results" trong file này với PASS/FAIL

**Decision branch:**
- PASS → Phase 2 dùng bilingual format `> 🇬🇧 *...*` blockquote
- FAIL → Phase 2 fallback VN-only, EN giữ trong `raw/`

### Spike B Results
*(User fill in after manual test)*

- Files uploaded:
- Queries tested:
- VN-clean responses: X/3
- Verdict: PASS | FAIL
- Notes:

## Overall Phase 0 Status

| Spike | Status | Verdict |
|---|---|---|
| A — Parallelism | ✅ Done | PASS (1.86x speedup) |
| B — NotebookLM | ⏳ User pending | Unknown |
| C — Code preservation | ✅ Done | PASS (10/10) |

**Go/No-Go for Phase 1:** ✅ **GO** — Phase 1 có thể bắt đầu mà không phụ thuộc Spike B kết quả (Spike B chỉ ảnh hưởng Phase 2 format choice).

## Files Created

- [pyproject.toml](../../pyproject.toml) — deps
- [.gitignore](../../.gitignore)
- [tests/fixtures/code-blocks.html](../../tests/fixtures/code-blocks.html)
- [spikes/spike_c.py](../../spikes/spike_c.py)
- [spikes/spike_b_instructions.md](../../spikes/spike_b_instructions.md)
- This file: spike-results.md
