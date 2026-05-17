---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro
title: Xác thực (Authentication)
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Xác thực

> 🇬🇧 *NATS authentication is multi-level. All of the security modes have an [_accounts_](.) level with [_users_](.#user-configuration-map) belonging to those accounts. The decentralized JWT Authentication also has an _operator_ to which the accounts belong.*

Xác thực trong NATS hoạt động theo nhiều tầng. Tất cả các chế độ bảo mật đều có tầng [_accounts_](.), trong đó [_users_](.#user-configuration-map) thuộc về từng account. Với JWT Authentication phi tập trung, còn có thêm tầng _operator_ quản lý các account.

> 🇬🇧 *Each account has its own independent subject namespace: a message published on subject 'foo' in one account will not be seen by subscribers to 'foo' in other accounts. Accounts can however define exports and imports of subject(s) streams as well as expose request-reply services between accounts. Users within an account will share the same subject namespace but can be restricted to only be able to publish-subscribe to specific subjects.*

Mỗi account có không gian tên subject (chuỗi định danh message) riêng biệt: message được publish lên subject `foo` trong một account sẽ không đến được subscriber lắng nghe `foo` ở account khác. Tuy nhiên, các account vẫn có thể định nghĩa export/import stream (luồng message lưu trữ liên tục) theo subject và expose các service request-reply giữa các account. Các user trong cùng một account chia sẻ chung không gian tên subject, nhưng có thể bị giới hạn chỉ publish/subscribe trên những subject cụ thể.

## Các phương thức xác thực

> 🇬🇧 *The NATS server provides various ways of authenticating clients:*

NATS server hỗ trợ nhiều cách xác thực client:

- [Token Authentication](./tokens.md)
- [Plain Text Username/Password credentials](./username_password.md#plain-text-passwords)
- [Bcrypted Username/Password credentials](./username_password.md#bcrypted-passwords)
- [TLS Certificate](./tls_mutual_auth.md)
- [NKEY with Challenge](./nkey_auth.md)
- [Decentralized JWT Authentication/Authorization](../jwt)

> 🇬🇧 *Authentication deals with allowing a NATS client to connect to the server. Except for JWT authentication, authentication and authorization are configured in the `authorization` section of the configuration. With JWT authentication the account and user information are stored in the [resolver](../jwt/resolver.md) rather than in the server configuration file.*

Xác thực xử lý việc cho phép NATS client kết nối đến server. Ngoại trừ JWT authentication, cả xác thực lẫn phân quyền đều được cấu hình trong mục `authorization`. Với JWT authentication, thông tin account và user được lưu trong [resolver](../jwt/resolver.md) thay vì trong file cấu hình server.

## Authorization Map

> 🇬🇧 *The `authorization` block provides _authentication_ configuration as well as [_authorization_](../authorization.md):*

Block `authorization` cung cấp cấu hình _authentication_ cũng như [_authorization_](../authorization.md):

| Property                                       | Description                                                                                                                           |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| [`token`](./tokens.md)                           | Chỉ định một token (chuỗi xác thực) toàn cục để xác thực với server (không dùng chung với user và password)                            |
| [`user`](./username_password.md#single-user)     | Chỉ định một tên người dùng _toàn cục_ cho client kết nối đến server (không dùng chung với token)                                                |
| [`password`](./username_password.md)             | Chỉ định một password _toàn cục_ cho client kết nối đến server (không dùng chung với `token`)                                               |
| [`users`](./username_password.md#multiple-users) | Danh sách các [user configuration](#user-configuration-map) map. Dùng danh sách `users` khi cần nhiều cặp username/password khác nhau. |
| [`timeout`](./auth_timeout.md)                   | Số giây tối đa chờ client xác thực                                                                                                    |
| [`auth_callout`](../auth_callout.md)           | Kích hoạt extension auth callout                                                                                                    |

## User Configuration Map

> 🇬🇧 *A `user` configuration map specifies credentials and permissions options for a single user:*

Map cấu hình `user` chỉ định credential (thông tin đăng nhập) và các tùy chọn permission (quyền truy cập) cho từng user:

| Property                             | Description                                                                                                                                   |
| :----------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| [`user`](./username_password.md)       | Username để xác thực client. (Cũng có thể là user cho [tls authentication](./tls_mutual_auth.md#mapping-client-certificates-to-a-user)) |
| [`password`](./username_password.md)   | Password cho user entry                                                                                                                   |
| [`nkey`](./nkey_auth.md)               | Public nkey định danh user                                                                                                               |
| [`permissions`](../authorization.md) | Map permission cấu hình các subject mà user được phép truy cập                                                                                   |

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **credential**: thông tin đăng nhập
- **permission**: quyền truy cập
- **server**: máy chủ
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **token**: chuỗi xác thực