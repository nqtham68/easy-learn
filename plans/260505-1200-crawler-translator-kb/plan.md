---
status: pending
created: 2026-05-05
updated: 2026-05-05
type: implementation-plan
red_team_reviewed: true
---

# Plan: Web Crawler + VN Translator Knowledge Base

## Context

- Brainstorm: [../reports/brainstorm-260505-web-crawler-translator.md](../reports/brainstorm-260505-web-crawler-translator.md)
- Red Team review: 4 lenses, 15 findings accepted (xem section cuối)
- Use case: cá nhân học tập, output markdown cho NotebookLM
- Architecture: hybrid — Python crawler (Stage 1) + Claude Code skill (Stage 2)

## Goals

1. Crawl website theo config YAML, output markdown EN sạch + safe
2. Skill `/translate-kb` dịch folder thành VN với code preservation deterministic
3. Resume file-based (VN file existence)
4. Security baseline: SSRF guard, path traversal, HTML sanitize, prompt injection defense

## Phases

| # | Phase | Status | Effort | Description |
|---|---|---|---|---|
| 0 | [Spike](phase-00-spike.md) | ✅ A+C done, B user-pending | 0.5-1d | Verify parallelism + NotebookLM + selectolax/markdownify |
| 1 | [Crawler MVP](phase-01-crawler-mvp.md) | ✅ completed | 2-3d | Single-file crawler, BFS resume, security baked in |
| 2 | [Translator Skill](phase-02-translator-skill.md) | ✅ completed | 2-3d | Skill + code-protect helper + hardened subagent prompt |
| 3 | [Enhancements](phase-03-robustness.md) | as-needed | 1-3d | Menu, chỉ pick khi gặp pain cụ thể |
| — | [Future ideas](future-ideas.md) | out-of-scope | — | Glossary, incremental, search — YAGNI |

**Total effort estimate:** 5-7 days (Phase 0+1+2). Phase 3 reactive.

## Key Dependencies

- Python 3.11+
- Claude Code CLI (subscription)
- Phase 0 → Phase 1 → Phase 2 sequential
- Phase 3 reactive, không block

## Success Criteria (Plan-level)

- [ ] Phase 0: 3 spike kết luận go/no-go có evidence
- [ ] Phase 1: crawl 1 site ~30-50 trang, resume + security tests pass
- [ ] Phase 2: 100% code blocks byte-equal, injection test không leak, resume skip works
- [ ] Output upload NotebookLM, query VN trả lời đúng (per Spike B kết quả)

## Out of Scope (YAGNI)

- Web UI, search engine, multi-language, glossary system, incremental re-crawl
- Standalone modules cho 5-line wrappers
- Async/Playwright/TOC nếu sequential đủ dùng

## Validation Log

### Session — 2026-05-05
**Questions asked:** 4 | **All answered**

| # | Question | Decision | Affects |
|---|---|---|---|
| 1 | First target site | `docs.nats.io/nats-concepts` (NATS docs) | Phase 0 Spike B + Phase 1 sample config |
| 2 | Spike B fallback | VN-only output if NotebookLM lẫn EN | Phase 2 conditional |
| 3 | Subagent approach | **Custom agent file** `.claude/agents/translator.md` (tools whitelist thực sự) | Phase 2 |
| 4 | Re-run default | Skip `translated:true`; user xóa VN file thủ công để re-translate | Phase 2 |

## Red Team Review

### Session — 2026-05-05
**Findings:** 15 (15 accepted, 0 rejected)
**Severity breakdown:** 4 Critical, 7 High, 4 Medium
**Reviewers:** Security Adversary, Failure Mode Analyst, Assumption Destroyer, Scope & Complexity Critic

| # | Finding | Severity | Disposition | Applied To |
|---|---------|----------|-------------|------------|
| 1 | Resume bug — raw frontmatter never updated | Critical | Accept | Phase 2 (filter on VN file) |
| 2 | Code preservation by prompt is wishful thinking | Critical | Accept | Phase 2 (deterministic protect/restore) |
| 3 | Prompt injection via crawled content + broad subagent tools | Critical | Accept | Phase 1 (HTML sanitize) + Phase 2 (hardened prompt, restricted tools) |
| 4 | Atomic write + integrity check missing | Critical | Accept | Phase 1 (`.tmp`+rename) + Phase 2 (validate before mark done) |
| 5 | Parallel subagent capability unverified | High | Accept | Phase 0 Spike A |
| 6 | NotebookLM bilingual format claim untested | High | Accept | Phase 0 Spike B; format pivot to blockquote |
| 7 | selectolax+markdownify integration unverified | High | Accept | Phase 0 Spike C; fixture test first |
| 8 | Path traversal + Windows reserved names | High | Accept | Phase 1 (`is_relative_to` + pathvalidate) |
| 9 | SSRF — fetcher + Playwright | High | Accept | Phase 1 (`is_safe_url` IP filter) + Phase 3 E3 |
| 10 | BFS crawl no resume — interrupt = full restart | High | Accept | Phase 1 (skip if file exists) |
| 11 | Async gather-then-write breaks resume | High | Accept | Phase 3 E1 (per-task immediate write) |
| 12 | Phase 3+4 gold-plating for personal use | High | Accept | Phase 3 demoted to as-needed; Phase 4 dropped → future-ideas.md |
| 13 | Phase 1 over-modularization (8 files for 300 lines) | Medium | Accept | Phase 1 collapsed to `crawler.py` + `cli.py` |
| 14 | yaml.load RCE + regex frontmatter parser | Medium | Accept | Phase 1 (`yaml.safe_load` + `python-frontmatter` lib) |
| 15 | robots.txt fail-open + secret leak via source_url | Medium | Accept | Phase 1 (default deny on parse error + strip query + `.gitignore`) |
