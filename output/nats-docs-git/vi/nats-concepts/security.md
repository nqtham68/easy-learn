---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/security
title: Bảo mật
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Bảo mật

> 🇬🇧 *NATS has a lot of security features:*

NATS cung cấp nhiều tính năng bảo mật:

* Kết nối có thể được [_mã hóa_ bằng TLS](../running-a-nats-service/configuration/securing_nats/tls.md)
* Kết nối client có thể được [_xác thực_](../running-a-nats-service/configuration/securing_nats/auth_intro) theo nhiều cách:
  * [Token Authentication](../running-a-nats-service/configuration/securing_nats/auth_intro/tokens.md)
  * [Username/Password credentials](../running-a-nats-service/configuration/securing_nats/auth_intro/username_password.md)
  * [TLS Certificate](../running-a-nats-service/configuration/securing_nats/auth_intro/tls_mutual_auth.md)
  * [NKEY with Challenge](../running-a-nats-service/configuration/securing_nats/auth_intro/nkey_auth.md)
  * [Decentralized JWT Authentication/Authorization](../running-a-nats-service/configuration/securing_nats/jwt)
  * Bạn cũng có thể tích hợp NATS với hệ thống xác thực/phân quyền hiện có, hoặc tự xây dựng cơ chế xác thực tùy chỉnh bằng [Auth callout](../running-a-nats-service/configuration/securing_nats/auth_callout.md)
* Sau khi xác thực, client được nhận dạng là user và có một tập hợp [_authorizations_](../running-a-nats-service/configuration/securing_nats/authorization.md)

> 🇬🇧 *You can use [accounts](../running-a-nats-service/configuration/securing_nats/accounts.md) for multi-tenancy: each account has its own independent 'subject namespace' and you control the import/export of both streams of messages and services between accounts, and any number of users that client applications can be authenticated as. The subjects or subject wildcards that a user is allowed to publish and/or subscribe to can be controlled either through server configuration or as part of signed JWTs.*

Bạn có thể dùng [accounts](../running-a-nats-service/configuration/securing_nats/accounts.md) để hỗ trợ multi-tenancy: mỗi account có một 'subject (chuỗi định danh message) namespace' độc lập, và bạn kiểm soát việc import/export cả stream (luồng message lưu trữ liên tục) lẫn service giữa các account, cùng với số lượng user tùy ý mà ứng dụng client có thể xác thực. Các subject hoặc subject wildcard mà user được phép publish và/hoặc subscribe có thể được kiểm soát qua server config hoặc thông qua signed JWT.

> 🇬🇧 *JWT authentication/authorization administration is decentralized because each account private key holder can manage their users and their authorizations on their own, without the need for any configuration change on the NATS servers by minting their own JWTs and distributing them to the users. There is no need for the NATS server to ever store any user private keys as they only need to validate the signature chain of trust contained in the user JWT presented by the client application to validate that they have the proper public key for that user.*

Việc quản trị xác thực/phân quyền JWT là phi tập trung: mỗi người nắm private key của account có thể tự quản lý user và permission (quyền truy cập) của họ mà không cần thay đổi config trên NATS server — chỉ cần tự ký JWT và phân phát cho user. NATS server không cần lưu trữ bất kỳ private key nào của user; server chỉ cần xác minh chuỗi chữ ký tin cậy có trong JWT mà ứng dụng client gửi lên, để xác nhận rằng public key trong JWT đó là hợp lệ cho user đó.

> 🇬🇧 *The JetStream persistence layer of NATS also provides [encryption at rest](../running-a-nats-service/nats_admin/jetstream_admin/encryption_at_rest.md).*

Tầng lưu trữ JetStream của NATS còn hỗ trợ [mã hóa dữ liệu lúc lưu trữ (encryption at rest)](../running-a-nats-service/nats_admin/jetstream_admin/encryption_at_rest.md).

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **permission**: quyền truy cập
- **server**: máy chủ
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **token**: chuỗi xác thực