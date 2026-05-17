# Review Feedback (learned from review passes)

## 1. Glossary Overrides
| Term | VN gloss | Reason | Source |
|---|---|---|---|

## 2. Style & Naturalness Rules

- Avoid glossing `pull consumer` as a compound — gloss the base term `consumer` on first occurrence and let `pull`/`push` prefix stand on its own. _Source: consumers.md_
- Prefer consistent short form "re-deliver / re-delivery" instead of mixed "tái giao nhận" and "re-deliver" within the same document. _Source: consumers.md_
- For blockquotes that list bullet points, translate bullet items inline under the same Vietnamese paragraph rather than duplicating the blockquote structure. _Source: consumers.md_
- When a sentence uses "chẳng hạn" to list items already covered by a colon-list, replace with a bare colon for conciseness. _Source: consumers.md_
- Avoid glossing informal metaphor words in parentheses (e.g., "island (đảo)") — if the word is not a glossary term, leave it bare in English. _Source: jetstream_leafnodes.md_
- Prefer active voice: "tránh được X" over "X sẽ được tránh khỏi" for natural-sounding passive-to-active conversion. _Source: jetstream_leafnodes.md_
- Drop redundant nested "để" in consequence phrases: "để có dữ liệu để truy xuất" → "để có dữ liệu truy xuất". _Source: jetstream_leafnodes.md_
- For NATS server config docs, preferred core term set is `config`, `cluster`, `stream`, `consumer`, `subject` — more topic-specific than generic `client`/`server`. _Source: running-a-nats-service/configuration/README.md_
- Place the inline gloss for the doc's primary concept in the first prose paragraph, not in a later aside or table. _Source: running-a-nats-service/configuration/README.md_
- For monitoring endpoint docs, preferred core term set is `endpoint`, `cluster`, `stream`, `consumer`, `metric` — not generic `server`/`port`. _Source: nats_admin/monitoring/README.md_
- Drop inline gloss annotations from `server` and `port` in monitoring docs — they are secondary/obvious terms; focus inline glosses on `endpoint` and topic-specific terms. _Source: nats_admin/monitoring/README.md_
- For NATS wire-protocol docs, preferred core term set is `subject`, `payload`, `publisher`, `subscriber`, `queue group` — not generic `client`/`server`. _Source: reference/nats-protocol/nats-protocol/README.md_
- In heading-based term definitions (e.g., "**Tên subject**"), place the inline gloss immediately after the term in the heading bold, not inside a separate parenthetical sentence. _Source: reference/nats-protocol/nats-protocol/README.md_
- For NSC/JWT identity management docs, preferred core term set is `credential`, `permission`, `subject`, `stream` — not generic `header`/`payload`/`subscriber`. _Source: using-nats/nats-tools/nsc/basics.md_
- For NSC stream export/import docs, preferred core term set is `stream`, `subject`, `subscriber`, `permission`, `token` — `message` is too generic to warrant an inline gloss slot. _Source: using-nats/nats-tools/nsc/streams.md_
- For NSC service export/import docs, preferred core term set is `service`, `subject`, `token`, `permission` — not generic `callback`/`request`/`response`. _Source: using-nats/nats-tools/nsc/services.md_
- For NATS benchmark docs, preferred core term set is `publisher`, `subscriber`, `stream`, `consumer`, `queue group` — all five are high-frequency in this doc type. _Source: natsbench.md_

## 3. Common Pitfalls to Avoid

- Translator added inline gloss to compound form "pull consumer (bên xử lý dữ liệu từ stream theo kiểu kéo)" — the extended gloss is non-standard; gloss only the base glossary term on first occurrence. _Source: consumers.md_
- Inline gloss for `subject` was missing on first occurrence even though it's a core term in NATS docs; add it when subject is central to the document. _Source: consumers.md_
- "tái giao nhận" is an acceptable literal translation but inconsistent with the English term "re-delivery" used in code contexts; prefer keeping "re-delivery" as English term in body text. _Source: consumers.md_
- Footer glossary was missing `subject` and `subscriber` even though both terms appeared in the body; always scan the full body for glossary terms before writing the footer. _Source: consumers.md_
- Do NOT gloss `client` or `server` inline — these are explicitly listed as "obvious" terms in the glossary spec and should only appear in the footer. _Source: jetstream_leafnodes.md_
- Inline gloss selection for JetStream docs should prioritize `stream`, `consumer`, `subject`, `cluster` over generic terms like `client`, `server`. _Source: jetstream_leafnodes.md_
- Footer `## Thuật ngữ trong bài` must include `API` when it appears repeatedly in the document body. _Source: jetstream_leafnodes.md_
- Do NOT add non-glossary translation annotations like "(đảo)" after "island" — only use VN gloss from the official glossary table. _Source: jetstream_leafnodes.md_
- Translator added phantom footer entries (`deploy`, `handler`, `middleware`, `schema`) for terms absent from the body text; verify each footer term actually appears in the body before including it. _Source: running-a-nats-service/configuration/README.md_
- Translator applied an ad-hoc inline gloss `(bên gọi)` to `client` mid-document outside the designated 3–5 core terms; inline glosses must only appear for the explicitly chosen core terms. _Source: running-a-nats-service/configuration/README.md_
- When translator omits all inline glosses entirely, reviewer must add 3–5 inline glosses on first prose occurrences of the most topic-relevant terms. _Source: running-a-nats-service/configuration/README.md_
- Translator glossed `server (máy chủ)` and `port (cổng kết nối)` inline in a monitoring doc where `endpoint`, `cluster`, `stream`, `consumer`, `metric` are the core terms; do not waste inline gloss slots on generic infrastructure terms. _Source: nats_admin/monitoring/README.md_
- In a monitoring doc, `stream` first-occurrence gloss belongs in the JetStream section note/table context, not forced into the intro paragraph where it does not naturally appear. _Source: nats_admin/monitoring/README.md_
- Translator glossed `client (bên gọi phía người dùng)` and `server (máy chủ)` inline in the first paragraph of a wire-protocol doc, using all inline gloss slots on generic terms; protocol-specific terms `subject`, `payload`, `publisher`, `subscriber`, `queue group` must be prioritized instead. _Source: reference/nats-protocol/nats-protocol/README.md_
- Footer included `broker` and `callback` which do not appear anywhere in the body of the protocol reference doc; always audit footer entries against body occurrences. _Source: reference/nats-protocol/nats-protocol/README.md_
- Translator glossed `header (phần metadata kèm theo)` and `payload (nội dung chính của message)` inline mid-document in an NSC/JWT doc where these are peripheral terms; do not apply inline glosses to terms that are not among the 3–5 chosen core terms for the document. _Source: using-nats/nats-tools/nsc/basics.md_
- Footer included `node` and `publisher` which do not appear as technical nouns in the NSC basics body; "publish" as a verb does not make "publisher" a footer-eligible term. _Source: using-nats/nats-tools/nsc/basics.md_
- Translator glossed `message (gói dữ liệu được gửi đi)` inline in an NSC stream export/import doc, wasting a core-term slot on a generic term; `stream` and `token` are more central to this document and should be glossed instead. _Source: using-nats/nats-tools/nsc/streams.md_
- Footer included `publisher`, `request`, `service` in the NSC streams doc where none appear as standalone technical nouns; `publisher` only appears in the glossary term `publish` (verb form), `request` is used conversationally, `service` is a brief mention — exclude them from the footer. _Source: using-nats/nats-tools/nsc/streams.md_
- Footer included `callback` in an NSC services doc where `callback` never appears in the body; phantom footer entries must be audited against actual body occurrences before writing the footer. _Source: using-nats/nats-tools/nsc/services.md_
- Translator wrote "Khóa công khai (public key)" annotating a non-glossary compound noun in Vietnamese; keep bare English form "public key" without a Vietnamese parenthetical annotation. _Source: using-nats/nats-tools/nsc/services.md_
- Footer included `async`, `producer`, `replica`, `sync`, `timeout` in a benchmark doc where none appeared as standalone English technical terms in the body prose; always verify each footer candidate against actual body text. _Source: natsbench.md_
