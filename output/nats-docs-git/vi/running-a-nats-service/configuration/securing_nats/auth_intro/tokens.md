---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/tokens
title: Token Xác Thực
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Token Xác Thực

> 🇬🇧 *Token authentication is a string that if provided by a client, allows it to connect. It is the most straightforward authentication provided by the NATS server.*

Token authentication (chuỗi xác thực) là một chuỗi ký tự mà nếu client cung cấp khi kết nối, server sẽ cho phép truy cập. Đây là phương thức xác thực đơn giản nhất do NATS server cung cấp.

> 🇬🇧 *To use token authentication, you can specify an `authorization` section with the `token` property set:*

Để dùng token authentication, hãy khai báo section `authorization` với thuộc tính `token` trong config (cấu hình):

```text
authorization {
    token: "s3cr3t"
}
```

> 🇬🇧 *Token authentication can be used in the authorization section for clients and clusters.*

Token authentication có thể dùng trong section `authorization` cho cả client lẫn cluster.

> 🇬🇧 *Or start the server with the `--auth` flag:*

Hoặc khởi động server với flag `--auth`:

```shell
nats-server --auth s3cr3t
```

> 🇬🇧 *A client can easily connect by specifying the server URL:*

Client kết nối dễ dàng bằng cách chỉ định URL của server:

```shell
nats sub -s nats://s3cr3t@localhost:4222 ">"
```

## Token Bcrypted

> 🇬🇧 *Tokens can be bcrypted enabling an additional layer of security, as the clear-text version of the token would not be persisted on the server configuration file.*

Token có thể được mã hóa bằng bcrypt để tăng thêm một lớp bảo mật — phiên bản rõ của token sẽ không được lưu trong file config của server.

> 🇬🇧 *You can generate bcrypted tokens and passwords using the [`nats`](../../../../using-nats/nats-tools/nats_cli) tool:*

Dùng công cụ [`nats`](../../../../using-nats/nats-tools/nats_cli) để tạo token và password đã được bcrypt:

```shell
nats server passwd
```
```text
? Enter password [? for help] **********************
? Reenter password [? for help] **********************

$2a$11$PWIFAL8RsWyGI3jVZtO9Nu8.6jOxzxfZo7c/W0eLk017hjgUKWrhy
```

> 🇬🇧 *Here's a simple configuration file:*

Dưới đây là một file config đơn giản:

```text
authorization {
    token: "$2a$11$PWIFAL8RsWyGI3jVZtO9Nu8.6jOxzxfZo7c/W0eLk017hjgUKWrhy"
}
```

> 🇬🇧 *The client will still require the clear-text token to connect:*

Client vẫn cần dùng token dạng rõ (clear-text) để kết nối:

```shell
nats sub -s nats://dag0HTXl4RGg7dXdaJwbC8@localhost:4222 ">"
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **server**: máy chủ
- **token**: chuỗi xác thực