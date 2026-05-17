---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/lame_duck_mode
title: Chế Độ Lame Duck
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Chế Độ Lame Duck

> 🇬🇧 *In production we recommend that a server is shut down with ​lame duck mode​ as a graceful way to slowly evict clients. With large deployments this mitigates the "thundering herd" situation that will place CPU pressure on servers as TLS enabled clients reconnect.*

Trong môi trường production, nên tắt server bằng lame duck mode — một cách tắt duyên dáng, từ từ loại bỏ client (bên gọi phía người dùng) ra khỏi server. Với các deployment (triển khai) lớn, cách này giúp tránh hiện tượng "thundering herd" — tình huống nhiều client có TLS đồng loạt reconnect gây áp lực CPU lên server.

## Server

> 🇬🇧 *Lame duck mode is initiated by [signaling](./signals.md) the server:*

Lame duck mode được kích hoạt bằng cách [gửi signal](./signals.md) tới server:

```shell
nats-server --signal ldm
```

> 🇬🇧 *After entering lame duck mode, the server will stop accepting new connections, wait for a 10 second grace period, then begin to evict clients over a period of time configurable by the [lame_duck_duration](https://docs.nats.io/nats-server/configuration#runtime-configuration) configuration option. This period defaults to 2 minutes.*

Sau khi vào lame duck mode, server ngừng nhận kết nối mới, chờ 10 giây grace period, rồi bắt đầu lần lượt loại bỏ client trong một khoảng thời gian cấu hình qua tùy chọn [lame_duck_duration](https://docs.nats.io/nats-server/configuration#runtime-configuration). Mặc định khoảng thời gian này là 2 phút.

## Clients

> 🇬🇧 *When entering lame duck mode, the server will send a message to clients. Some maintainer supported clients will invoke an optional callback indicating that a server is entering lame duck mode. This is used for cases where an application can benefit from preparing for the short outage between the time it is evicted and automatically reconnected to another server.*

Khi server vào lame duck mode, server gửi một message (gói dữ liệu được gửi đi) tới các client. Một số client được maintainer hỗ trợ chính thức sẽ gọi một callback (hàm được gọi lại) tùy chọn để thông báo rằng server đang vào lame duck mode. Tính năng này hữu ích khi ứng dụng cần chuẩn bị trước cho khoảng thời gian gián đoạn ngắn — từ lúc bị loại bỏ đến khi tự động kết nối lại với server khác.

## Thuật ngữ trong bài

- **callback**: hàm được gọi lại
- **client**: bên gọi (phía người dùng)
- **deploy**: triển khai
- **message**: gói dữ liệu được gửi đi
- **server**: máy chủ
- **TLS**: mã hóa TLS