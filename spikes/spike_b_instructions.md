# Spike B: NotebookLM Bilingual Format — Manual Test

**Why manual:** Cần upload lên NotebookLM (web), Claude Code không thao tác được.

## Steps

### 1. Tạo 5 file bilingual mẫu
Pick 5 trang từ `https://docs.nats.io/nats-concepts/` (chọn các trang ngắn-vừa, có code).

Format mỗi file (`spikes/notebooklm-pilot/<page-slug>.md`):

```markdown
---
source_url: https://docs.nats.io/nats-concepts/<slug>
title: <Tiêu đề VN>
translated: true
---

# <Tiêu đề VN>

> 🇬🇧 *<Đoạn EN gốc 1>*

<Đoạn VN dịch 1>

> 🇬🇧 *<Đoạn EN gốc 2>*

<Đoạn VN dịch 2>

```code-block-if-any
giữ nguyên
```
```

Bạn có thể tự dịch hoặc dùng Claude/ChatGPT manual cho 5 file này — đây là 1 lần thôi.

### 2. Upload lên NotebookLM
- https://notebooklm.google.com → New notebook
- Add sources → upload 5 file `.md`
- Đặt tên notebook: `nats-concepts-pilot`

### 3. Test query (3 câu, tiếng Việt)
Đặt 3 câu hỏi cụ thể về NATS concepts đã có trong 5 file. Ví dụ:
1. "Subject là gì trong NATS?"
2. "JetStream khác gì Core NATS?"
3. "Cách publish/subscribe hoạt động ra sao?"

### 4. Đánh giá

Cho mỗi câu hỏi, ghi nhận:
- [ ] Response chủ yếu tiếng Việt? (target: >80% VN, không phun nguyên đoạn EN)
- [ ] Citation link đúng file?
- [ ] Có "lẫn EN" do `> 🇬🇧 *...*` blockquote không?

### 5. Verdict

**PASS** nếu cả 3 câu retrieval VN-clean → dùng bilingual format như spec.

**FAIL** nếu NotebookLM index cả EN block và phun ra → fallback **VN-only**:
- Translator skill drop blockquote EN
- File `vi/*.md` thuần Việt
- EN gốc giữ ở `output/{site}/raw/` reference qua `source_url` frontmatter

## Ghi kết quả vào

`plans/260505-1200-crawler-translator-kb/spike-results.md` (section "Spike B")

Format:
```markdown
### Spike B Results
- Files uploaded: 5
- Queries tested: 3
- VN-clean responses: X/3
- Verdict: PASS | FAIL
- Notes: <quan sát>
```
