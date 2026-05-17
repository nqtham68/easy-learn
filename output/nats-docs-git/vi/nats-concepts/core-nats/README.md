---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/core-nats
title: Core NATS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Core NATS

> 🇬🇧 *Core NATS is the foundational functionality in a NATS system. It operates on a publish-subscribe model using subject/topic-based addressing. This model offers two significant advantages: location independence and a default many-to-many (M:N) communication pattern. These fundamental concepts enable powerful and innovative solutions for common development patterns, such as microservices, without requiring additional technologies like load balancers, API gateways, or DNS configuration.*

Core NATS là nền tảng của hệ thống NATS, hoạt động theo mô hình publish-subscribe với cơ chế định địa chỉ dựa trên subject (chuỗi định danh message). Mô hình này mang lại hai lợi thế lớn: tính độc lập về vị trí và pattern giao tiếp nhiều-nhiều (M:N) mặc định. Những khái niệm cốt lõi này cho phép xây dựng các giải pháp mạnh mẽ cho các pattern phát triển phổ biến như microservices, mà không cần thêm load balancer, API gateway hay cấu hình DNS.

> 🇬🇧 *NATS systems can be enhanced with [JetStream](../jetstream), which adds persistence capabilities. While Core NATS provides best-effort, at-most-once message delivery, JetStream introduces at-least-once and exactly-once semantics.*

Hệ thống NATS có thể được mở rộng với [JetStream](../jetstream) để bổ sung khả năng lưu trữ bền vững. Core NATS đảm bảo giao nhận message (gói dữ liệu được gửi đi) theo kiểu best-effort, at-most-once, trong khi JetStream hỗ trợ ngữ nghĩa at-least-once và exactly-once.

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **message**: gói dữ liệu được gửi đi
- **subject**: chuỗi định danh message (giống topic)
- **topic**: chủ đề phân loại message