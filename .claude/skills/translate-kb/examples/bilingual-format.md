---
source_url: https://docs.nats.io/nats-concepts/example
title: Khái niệm cơ bản
crawled_at: 2026-05-05T10:00:00Z
translated: true
translated_at: 2026-05-05T11:00:00Z
---

# Khái niệm cơ bản

> 🇬🇧 *NATS is a connective technology powering modern distributed systems.*

NATS là một công nghệ kết nối hỗ trợ các hệ thống phân tán hiện đại.

> 🇬🇧 *It uses a publish-subscribe model and supports multiple messaging patterns.*

Nó sử dụng mô hình publish-subscribe và hỗ trợ nhiều mẫu nhắn tin khác nhau.

## Subjects

> 🇬🇧 *Subjects are simple strings (the only requirement is they are ASCII text) that form a name hierarchy, optionally separated by dots.*

Subjects là các chuỗi đơn giản (yêu cầu duy nhất là chúng phải là văn bản ASCII) tạo thành một hệ thống phân cấp tên, tùy chọn được phân tách bởi dấu chấm.

```go
nc.Subscribe("orders.>", func(m *nats.Msg) {
    fmt.Printf("Received: %s\n", string(m.Data))
})
```

> 🇬🇧 *Use `nc.Subscribe` with a wildcard pattern to receive all messages under a subject hierarchy.*

Sử dụng `nc.Subscribe` với pattern wildcard để nhận tất cả message thuộc cùng một hệ thống phân cấp subject.
