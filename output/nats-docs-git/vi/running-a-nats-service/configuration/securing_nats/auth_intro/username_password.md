---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/username_password
title: Tên người dùng/Mật khẩu
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Tên người dùng/Mật khẩu

## Mật khẩu dạng văn bản thuần

> 🇬🇧 *You can authenticate one or more clients using username and passwords; this enables you to have greater control over the management and issuance of credential secrets.*

Có thể xác thực một hoặc nhiều client bằng username và password. Cách này giúp kiểm soát tốt hơn việc quản lý và cấp phát credential (thông tin đăng nhập) secret.

## Một người dùng duy nhất

```
authorization: {
    user: a,
    password: b
}
```

> 🇬🇧 *You can also specify a single username/password by:*

Cũng có thể chỉ định một username/password duy nhất bằng cách:

```
> nats-server --user a --pass b
```

## Nhiều người dùng

```
authorization: {
    users: [
        {user: a, password: b},
        {user: b, password: a}
    ]
}
```

## Mật khẩu Bcrypt

> 🇬🇧 *Username/password also supports bcrypted passwords using the [`nats`](https://docs.nats.io/using-nats/nats-tools/nats\_cli) tool. Simply replace the clear text password with the bcrypted entries:*

Username/password còn hỗ trợ mật khẩu bcrypt thông qua công cụ [`nats`](https://docs.nats.io/using-nats/nats-tools/nats\_cli). Chỉ cần thay thế mật khẩu văn bản thuần bằng các giá trị bcrypt tương ứng:

```
> nats server passwd
? Enter password [? for help] **********************
? Reenter password [? for help] **********************

$2a$11$V1qrpBt8/SLfEBr4NJq4T.2mg8chx8.MTblUiTBOLV3MKDeAy.f7u
```

> 🇬🇧 *And on the configuration file:*

Và trong config (cấu hình):

```
authorization: {
    users: [
        {user: a, password: "$2a$11$V1qrpBt8/SLfEBr4NJq4T.2mg8chx8.MTblUiTBOLV3MKDeAy.f7u"},
        ...
    ]
}
```

## Tải lại cấu hình

> 🇬🇧 *As you add/remove passwords from the server configuration file, you'll want your changes to take effect. To reload without restarting the server and disconnecting clients, do:*

Khi thêm hoặc xóa mật khẩu trong file config của server, bạn cần áp dụng thay đổi mà không khởi động lại server hay ngắt kết nối các client. Để reload, chạy lệnh:

```
> nats-server --signal reload
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **secret**: chuỗi bí mật
- **server**: máy chủ