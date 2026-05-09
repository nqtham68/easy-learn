---
type: brainstorm-summary
date: 2026-05-05
topic: web-crawler-translator-knowledge-base
---

# Brainstorm: Web Crawler + VN Translator Knowledge Base

## 1. Problem Statement

Build công cụ cá nhân để:
- Crawl content từ websites (docs, blog, tutorial, wiki) với scope kiểm soát được
- Dịch sang tiếng Việt giữ độ chính xác kỹ thuật, **không dùng API key trả phí**
- Output markdown song ngữ để đọc trực tiếp + upload NotebookLM

## 2. Decisions (Locked-in)

| Aspect | Choice | Reason |
|---|---|---|
| Use case | Cá nhân học tập | Không cần web app, auth, hosting |
| Translation engine | **Claude Code skill (Sonnet)** | Tận dụng subscription, không tốn API cost |
| Architecture | **Hybrid: Python crawler + Claude Code skill** | Crawl deterministic dùng code, translate cần intelligence dùng skill |
| Skill mode | **Batch với subagents song song** | Main context clean, throughput cao hơn sequential |
| Resume | **File-based (frontmatter check)** | Đơn giản, không cần state DB |
| Output | Markdown song ngữ với `<details>` | NotebookLM-friendly, đối chiếu được |
| Crawl strategy | Config-per-site YAML | Predictable, debuggable |
| Organization | URL path mirror + ordered `_toc.md` | Vừa giữ structure, vừa đọc tuần tự |
| Stack crawler | Python | httpx + selectolax + markdownify |

## 3. Architecture

### 3.1 Two-Stage Pipeline

```
┌─────────────────────────────────────────┐
│ STAGE 1: Python Crawler (deterministic) │
└─────────────────────────────────────────┘
[site config YAML]
      ↓
[Discoverer] ← BFS link discovery, max_depth/pages, robots.txt
      ↓
[Fetcher]    ← httpx async + retry + rate limit
      ↓
[Extractor]  ← selectolax + content_selector
      ↓
[HTML→MD]    ← markdownify, preserve code blocks
      ↓
output/{site}/raw/{path}.md   ← markdown gốc EN, frontmatter: translated:false

┌─────────────────────────────────────────┐
│ STAGE 2: Claude Code Skill (intelligent)│
└─────────────────────────────────────────┘
User: /translate-kb output/react-docs

[Main skill agent]
      ↓ scan folder, filter translated:false
      ↓ spawn batch of N translator subagents (parallel)
      ↓
[translator subagent × N]   ← mỗi con: Read file → translate → Write
      ↓
output/{site}/vi/{path}.md   ← bilingual, frontmatter: translated:true
```

### 3.2 Tech Stack — Crawler (Python)
- `httpx[async]` — fetch
- `selectolax` — parse (nhanh hơn BS4 5-10×)
- `playwright` — fallback cho JS-heavy site (Phase 3)
- `markdownify` — HTML→MD
- `pyyaml` — config
- `typer` + `rich` — CLI/progress
- `tenacity` — fetch retry
- ❌ KHÔNG dùng `anthropic` SDK
- ❌ KHÔNG cần SQLite (file-based state)

### 3.3 Site Config Schema (YAML)
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
js_render: false
```

### 3.4 Raw Markdown Output (Stage 1)
```markdown
---
source_url: https://react.dev/learn
crawled_at: 2026-05-05T10:00:00Z
order: 12
title: Quick Start
translated: false
---

# Quick Start

React lets you build user interfaces out of components.

```js
function Hello() { return <h1>Hi</h1>; }
```
```

### 3.5 Bilingual Output (Stage 2)
```markdown
---
source_url: https://react.dev/learn
crawled_at: 2026-05-05T10:00:00Z
translated_at: 2026-05-05T11:00:00Z
order: 12
title: Bắt đầu nhanh
translated: true
---

# Bắt đầu nhanh

<details><summary>🇬🇧 Original</summary>

React lets you build user interfaces out of components.

</details>

React cho phép bạn xây dựng giao diện người dùng từ các components.

```js
function Hello() { return <h1>Hi</h1>; }
```
```

→ Code blocks giữ nguyên không động vào (subagent được instruct rõ).

### 3.6 Claude Code Skill Design

**Location:** `.claude/skills/translate-kb/SKILL.md`

**Skill prompt outline:**
```
Tên: translate-kb
Args: <folder-path> [--batch-size N] [--max-files M]

Workflow:
1. Scan folder, list .md files có frontmatter translated:false
2. Apply --max-files limit nếu có
3. Chia thành batches kích thước N (default 5)
4. Với mỗi batch: spawn N general-purpose subagents song song
   Mỗi subagent prompt:
     - Read file at {path}
     - Dịch sang tiếng Việt theo format song ngữ collapsible
     - GIỮ NGUYÊN code blocks (```...``` và `inline`)
     - GIỮ NGUYÊN markdown structure (headings, lists, links)
     - Update frontmatter: title (dịch), translated:true, translated_at
     - Write file ra path tương ứng vi/
5. Sau mỗi batch, report progress
6. Cuối: summarize số file done/skip/fail
```

**Glossary (optional, Phase 4):** file `.claude/skills/translate-kb/glossary.md` để consistent terminology (component → component, hook → hook, render → render…).

### 3.7 Why subagents?
- Main context không bị bùng nổ vì content file
- Parallel: 5 file/batch = 5× nhanh hơn sequential
- Mỗi subagent fail độc lập, không hỏng cả batch

## 4. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Subagent dịch nhầm code block | Skill prompt nhấn mạnh; thêm checklist "did you preserve code?" |
| Translate inconsistent terminology | Phase 4: glossary file shared cho subagents |
| Throughput chậm với 1000+ files | Batch size config được; user có thể chạy nhiều session |
| Site đổi structure → config hỏng | Crawler báo % extracted bất thường; raw output để check thủ công |
| Resume mid-batch crash | Frontmatter `translated:true` chỉ set sau khi Write thành công → re-run skip xong |
| Context limit subagent | 1 file/subagent đủ an toàn; file quá to skill có thể split theo H2 trước khi spawn |

## 5. Out of Scope (YAGNI)

- ❌ Web UI (đọc markdown trực tiếp)
- ❌ Search engine (NotebookLM lo)
- ❌ SQLite state DB (frontmatter đủ)
- ❌ API cost tracking (skill mode không cần)
- ❌ Auto-detect content selector
- ❌ Translate code comments
- ❌ Incremental re-crawl (Phase 4)
- ❌ Multi-language (chỉ EN→VN)

## 6. Project Structure

```
web-easy-learn/
├── .claude/
│   └── skills/
│       └── translate-kb/
│           ├── SKILL.md              # skill prompt + instructions
│           └── glossary.md           # (Phase 4) shared terminology
├── src/
│   ├── crawler/
│   │   ├── discoverer.py
│   │   ├── fetcher.py
│   │   ├── extractor.py
│   │   └── html_to_md.py
│   ├── writer/
│   │   ├── markdown_writer.py
│   │   └── toc_builder.py
│   ├── config/
│   │   └── site_config.py
│   └── cli.py                        # `crawl` command
├── sites/                            # YAML configs per site
│   └── react-docs.yaml
├── output/
│   └── {site}/
│       ├── raw/                      # Stage 1 output
│       └── vi/                       # Stage 2 output
├── tests/
└── pyproject.toml
```

## 7. Success Criteria

- [ ] Crawl 1 site target (e.g. react.dev/learn) → raw markdown đầy đủ
- [ ] Skill `/translate-kb` xử lý folder, spawn subagents, output bilingual
- [ ] 100% code blocks giữ nguyên syntax (manual check vài file đầu)
- [ ] Resume: re-run skill bỏ qua file `translated:true`
- [ ] Output upload NotebookLM được, query VN trả lời đúng
- [ ] Config 1 site mới ≤ 30 phút

## 8. Phasing

**Phase 1 — Crawler MVP (3-5 days):**
- httpx fetcher + selectolax extractor + markdownify
- YAML config loader
- BFS discoverer với max_depth/max_pages
- Output raw markdown với frontmatter
- Test trên 1 site nhỏ (~50 pages)

**Phase 2 — Translator Skill (2-3 days):**
- Tạo `.claude/skills/translate-kb/SKILL.md`
- Define subagent translation prompt
- Test batch=5 với 20 files
- Verify code preservation, bilingual format đúng

**Phase 3 — Robustness (3-5 days):**
- Async fetch, rate limit, tenacity retry
- robots.txt respect
- Playwright fallback cho JS site
- `_toc.md` ordered theo crawl order
- CLI progress UI (rich)

**Phase 4 — Polish (optional):**
- Glossary file cho terminology consistency
- Incremental re-crawl (so sánh content_hash)
- Multiple site batch run

## 9. Open Questions / Next Steps

1. Site đầu tiên target: bạn đã có URL cụ thể chưa? (ảnh hưởng config schema test)
2. Batch size mặc định: 5 OK? Hay muốn 3 (an toàn) / 10 (tốc độ)?
3. Tiếp tục `/ck:plan` để sinh phase files chi tiết?
