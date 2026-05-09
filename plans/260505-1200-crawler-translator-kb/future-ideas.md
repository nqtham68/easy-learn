---
type: future-ideas
note: Documented post-Red-Team but NOT scoped to current plan
---

# Future Ideas (Out of Plan)

Removed from plan per Red Team Findings (Scope Critic): YAGNI — chỉ build khi pain thực sự.

## Glossary System

**When to consider:** Sau Phase 2, scan thủ công 5-10 file VN, đếm số term inconsistent. Nếu >5 terms vary annoyingly across files → consider.

**Minimum design:** 5-10 line "preferred terms" trong subagent prompt. Không tạo file riêng, không subsystem.

## Incremental Re-crawl với Content Hash

**When to consider:** Sau khi maintain KB >6 tháng, thực sự cần re-crawl periodic và muốn tránh re-translate unchanged content.

**Minimum design:** SHA256 content_hash trong frontmatter raw + skill compare trước spawn. KHÔNG normalize whitespace (over-engineering); content khác = re-translate.

**Risk:** Manual VN edits bị overwrite. Cần `vn_edited:true` flag trong VN frontmatter để protect.

## Cross-File Search / Index

**When to consider:** KB >100 files VÀ NotebookLM không đủ.

**Minimum design:** ripgrep + small static index. Không build search engine.

## Multi-Language (other than VN)

**When to consider:** Nếu user thực sự cần. Hiện chỉ EN→VN.

---

**Trigger:** Mỗi mục trên CHỈ build khi có pain point đo lường được, document ở đây trước khi scope vào plan mới.
