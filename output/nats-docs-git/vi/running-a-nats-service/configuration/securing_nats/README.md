---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats
title: Bảo mật NATS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Bảo mật NATS

> 🇬🇧 *The NATS server provides several forms of security:*

NATS server cung cấp nhiều lớp bảo mật:

> 🇬🇧 *Connections can be [_encrypted_ with TLS](./tls.md)*

* Kết nối có thể được [_mã hóa_ bằng TLS (mã hóa TLS)](./tls.md)

> 🇬🇧 *Client connections can require [_authentication_](./auth_intro)*

* Kết nối từ client có thể yêu cầu [_xác thực_](./auth_intro)

> 🇬🇧 *Clients can require [_authorization_](./authorization.md) for subjects they publish or subscribe to*

* Client có thể yêu cầu [_phân quyền_](./authorization.md) cho các subject (chuỗi định danh message) mà chúng publish hoặc subscribe

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **subject**: chuỗi định danh message (giống topic)
- **TLS**: mã hóa TLS