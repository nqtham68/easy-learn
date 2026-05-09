# web-easy-learn

Crawl tài liệu kỹ thuật tiếng Anh, dịch sang tiếng Việt theo định dạng song ngữ, gom nhiều bộ docs vào **một site MkDocs duy nhất** và publish lên GitHub Pages.

```
sites/<name>.yaml ─► python cli.py crawl|fetch ─► output/<name>/raw/**/*.md
                                                        │
                                                        ▼  /translate-kb (Claude Code)
                                              output/<name>/vi/**/*.md
                                                        │
                                                        ▼  python cli.py sync
                                              docs-site/docs/<name>/**/*.md
                                                        │
                                                        ▼  python cli.py serve|build  (CI: GitHub Actions)
                                                 GitHub Pages
```

**Tất cả thao tác (trừ translate) đi qua một entrypoint duy nhất là `cli.py`.** Translate chạy trong Claude Code qua slash command `/translate-kb`.

Xem toàn bộ subcommand:
```powershell
.\.venv\Scripts\python.exe cli.py --help
```

---

## Setup (1 lần)

```powershell
cd d:\Projects\web-easy-learn

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .

# Cho docs-site (preview local + build):
pip install mkdocs-material mkdocs-awesome-nav

# Cho crawl HTML (nếu cần Playwright):
pip install -e ".[js]"
playwright install chromium
```

Mở project bằng VS Code có Claude Code extension. Restart Claude Code session sau khi clone để load các agent trong `.claude/agents/`.

---

## Phase 1 — Lấy markdown gốc

Có 2 cách. **Ưu tiên 1B (git) nếu site có repo công khai** — chất lượng cao hơn nhiều.

### 1A. Crawl HTML

```powershell
.\.venv\Scripts\python.exe cli.py crawl sites\<name>.yaml
```

Config mẫu: [sites/nats-docs.yaml](sites/nats-docs.yaml).

### 1B. Fetch từ git (recommend)

```powershell
.\.venv\Scripts\python.exe cli.py fetch sites\<name>.yaml
```

Config mẫu: [sites/nats-docs-git.yaml](sites/nats-docs-git.yaml). Yêu cầu block `source:` với `type: git`.

**Output cả hai:** `output/<name>/raw/**/*.md` với frontmatter `translated: false`.

---

## Phase 2 — Translate

Skill `/translate-kb` chạy trong Claude Code. Workflow tự động hoá:
- Discover file pending (skip file đã `translated: true`)
- **Pre-filter content** (auto-skip page rỗng/toàn link, ghi `translated: skipped`)
- Protect code blocks (byte-equal preservation)
- Spawn translator subagent song song theo batch
- (Optional) Review pass cho N file đầu
- Restore code blocks + validate + atomic write
- **Linkify bare URLs** (auto, wrap URL trần thành `<a href>`)
- **Rewrite upstream links** (auto, đổi `https://docs.nats.io/...` thành relative path local)

### Quy trình 4 bước cho site mới

**Bước 1 — Smoke test 3 file đầu, có review:**

```
/translate-kb output/<name>/raw --max-files 3 --review-first 3
```

Mở 3 file vừa dịch trong `output/<name>/vi/`, đọc kỹ. Nếu chưa OK, chỉnh [.claude/agents/translator.md](.claude/agents/translator.md) (glossary / style / examples), xoá 3 file VN, chạy lại.

**Bước 2 — Mở rộng QA: 10 file, review 3:**

```
/translate-kb output/<name>/raw --max-files 10 --review-first 3
```

**Bước 3 — Dịch hết, không review:**

```
/translate-kb output/<name>/raw --auto
```

`--auto` = im lặng giữa batch, chỉ in tổng kết cuối. Resume-safe: tự skip file đã xong.

**Bước 4 — Retry file fail:** chỉ cần chạy lại lệnh Bước 3.

### Tham số `/translate-kb`

| Cờ | Mặc định | Mô tả |
|---|---|---|
| `<raw-folder>` | bắt buộc | `output/<name>/raw` |
| `--max-files N` | unlimited | Giới hạn số file dịch trong run này |
| `--batch-size N` | 3 | Số translator subagent song song mỗi batch (max 5–6) |
| `--review-first N` | 0 | Review N file đầu bằng `translation-reviewer` |
| `--auto` | false | Im lặng giữa các batch |
| `--no-filter` | false | Bỏ qua content filter (dịch luôn cả page rỗng) |

### Theo dõi tiến độ

```powershell
# File VN đã có:
Get-ChildItem output\<name>\vi -Recurse -Filter *.md `
  | Where-Object { $_.Name -notmatch '\.(tmp-|blocks\.)' } `
  | Measure-Object | Select-Object -Expand Count

# File pending:
.\.venv\Scripts\python.exe cli.py discover output\<name>\raw 2>&1 | Select-String "pending"
```

### Tinh chỉnh chất lượng

| Vấn đề | Cách sửa |
|---|---|
| Văn phong cứng / dịch word-by-word | Thêm "bad vs good" example vào `Worked Example` của [translator.md](.claude/agents/translator.md) |
| Thuật ngữ không nhất quán | Bổ sung term vào Glossary trong [translator.md](.claude/agents/translator.md) |
| Inline gloss quá nhiều/ít | Chỉnh quy tắc "3–5 core terms" trong [translator.md](.claude/agents/translator.md) |
| Chất lượng tổng thể chưa đủ | Tăng `--review-first` |
| Chậm | Tăng `--batch-size` |

---

## Phase 3 — Preview docs site local

Tổng hợp tất cả `output/*/vi/` thành một MkDocs site:

```powershell
# Sync các bộ vi/ vào docs-site/docs/<project>/
.\.venv\Scripts\python.exe cli.py sync

# Chạy dev server (auto-reload khi đổi file trong docs-site/docs/)
.\.venv\Scripts\python.exe cli.py serve
```

Mở `http://localhost:8001` (PC) hoặc `http://<LAN-IP>:8001` (điện thoại cùng WiFi). Material theme có dark mode, search VN+EN, navigation tabs cho từng bộ docs.

Đổi port: `python cli.py serve --addr 0.0.0.0:9000`. Build static cho test trước khi push CI: `python cli.py build`.

**Lưu ý:** mkdocs serve watch `docs-site/docs/`, không watch `output/*/vi/`. Khi sửa file trong `output/<name>/vi/`, chạy lại `python cli.py sync` để đẩy vào.

Tuỳ chỉnh tên hiển thị các bộ docs: chỉnh `PROJECT_TITLES` trong [docs-site/scripts/sync_projects.py](docs-site/scripts/sync_projects.py).

---

## Phase 4 — Publish lên GitHub Pages

Repo gốc commit cả `output/*/vi/` + `docs-site/`. CI tự sync và build.

### Lần đầu

1. **Khởi tạo git** (nếu chưa):
   ```powershell
   cd d:\Projects\web-easy-learn
   git init -b main
   git add .
   git commit -m "init"
   ```

2. **Tạo repo trên GitHub** (private hoặc public), push:
   ```powershell
   git remote add origin https://github.com/<user>/<repo>.git
   git push -u origin main
   ```

3. **Bật GitHub Pages**: Repo → Settings → Pages → **Source: GitHub Actions**.

4. Workflow [docs-site/.github/workflows/deploy-docs.yml](docs-site/.github/workflows/deploy-docs.yml) tự chạy khi push lên `main`. URL kết quả: `https://<user>.github.io/<repo>/`.

### Mỗi lần dịch thêm

```powershell
git add output/<name>/vi
git commit -m "feat(<name>): translate <X> more files"
git push
```

CI tự build lại trong 1–2 phút.

### Cấu hình `.gitignore`

Đã setup sẵn — chỉ commit:
- ✅ `output/<name>/vi/` (sản phẩm dịch)
- ✅ `docs-site/mkdocs.yml`, `docs-site/scripts/`, `docs-site/.github/`
- ❌ `output/<name>/raw/` (upstream, không phải work product)
- ❌ `docs-site/docs/`, `docs-site/site/` (sinh tự động bởi CI)

---

## Cấu trúc project

```
web-easy-learn/
├── cli.py                                       # Unified entrypoint (Typer)
├── crawler.py                                   # Phase 1A logic
├── git_fetch.py                                 # Phase 1B logic
├── sites/<name>.yaml                            # Config crawler per site
├── output/<name>/
│   ├── raw/**/*.md                              # Phase 1 — gitignored
│   └── vi/**/*.md                               # Phase 2 — committed
├── docs-site/                                   # Phase 3 + 4 — unified docs site
│   ├── mkdocs.yml
│   ├── docs/                                    # gitignored, CI sinh
│   ├── scripts/sync_projects.py
│   └── .github/workflows/deploy-docs.yml
├── .claude/
│   ├── agents/
│   │   ├── translator.md                        # Glossary + style guide
│   │   └── translation-reviewer.md
│   ├── skills/translate-kb/
│   │   ├── SKILL.md                             # Workflow spec
│   │   ├── helpers/                             # Gọi qua cli.py
│   │   │   ├── protect_code.py                  # Code-block protect/restore
│   │   │   ├── cli_protect.py                   # Wrapper cho /translate-kb
│   │   │   ├── discover.py                      # List pending files
│   │   │   ├── content_filter.py                # Auto-skip low-content pages
│   │   │   ├── linkify_urls.py                  # Wrap bare URLs
│   │   │   ├── rewrite_links.py                 # Upstream URL → local relative
│   │   │   └── rewrite_all_links.py             # Bulk runner
│   │   └── examples/bilingual-format.md
│   └── settings.json                            # Permissions allowlist
└── pyproject.toml
```

---

## Troubleshooting

| Lỗi | Cách xử lý |
|---|---|
| `Agent type 'translation-reviewer' not found` | Restart Claude Code session để load agent mới |
| `UnicodeEncodeError: 'charmap' codec can't encode '→'` | Đảm bảo `PYTHONIOENCODING=utf-8` (skill tự set) |
| Skill báo "Nothing to translate" nhưng folder rỗng | Frontmatter raw bị parse lỗi: chạy `discover.py` thủ công |
| File VN còn sót `<<<__WEBEZ_*__>>>` | Restore step fail. Xoá file → chạy lại |
| Bị hỏi quyền liên tục cho lệnh Bash | Check [.claude/settings.json](.claude/settings.json) có allowlist các helper |
| Page hiển thị broken sau bảng / link không clickable | `python cli.py linkify output/<name>/vi` |
| Link sang trang khác trong cùng site bị 404 | `python cli.py rewrite-links output/<name>/raw output/<name>/vi` |
| mkdocs serve không reload sau sync | mkdocs watch `docs-site/docs/`, không watch `output/`. Chạy lại `sync_projects.py`, đôi khi cần kill+restart server |

---

## Tham khảo

- [.claude/skills/translate-kb/SKILL.md](.claude/skills/translate-kb/SKILL.md) — spec workflow đầy đủ
- [.claude/agents/translator.md](.claude/agents/translator.md) — glossary + style guide
- [.claude/agents/translation-reviewer.md](.claude/agents/translation-reviewer.md) — spec reviewer
- [CLAUDE.md](CLAUDE.md) — working rules cho Claude Code trong project này
