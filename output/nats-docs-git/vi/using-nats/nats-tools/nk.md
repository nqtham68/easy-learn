---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nk
title: Công cụ nk — Tạo và quản lý NKeys
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# nk

> 🇬🇧 *`nk` is a command line tool that generates `nkeys`. NKeys are a highly secure public-key signature system based on [Ed25519](https://ed25519.cr.yp.to/).*

`nk` là công cụ dòng lệnh dùng để tạo `nkeys`. NKeys là hệ thống chữ ký public-key bảo mật cao, xây dựng trên nền tảng [Ed25519](https://ed25519.cr.yp.to/).

> 🇬🇧 *With NKeys the server can verify identity without ever storing secrets on the server. The authentication system works by requiring a connecting client to provide its public key and digitally sign a challenge with its private key. The server generates a random challenge with every connection request, making it immune to playback attacks. The generated signature is validated a public key, thus proving the identity of the client. If the public key validation succeeds, authentication succeeds.*

Với NKeys, server xác minh danh tính mà không cần lưu secret (chuỗi bí mật) trên server. Cơ chế hoạt động: client kết nối phải cung cấp public key và ký số một challenge bằng private key của mình. Server sinh ra một challenge ngẫu nhiên cho mỗi yêu cầu kết nối, giúp hệ thống miễn nhiễm với replay attack. Chữ ký được xác thực bằng public key, qua đó chứng minh danh tính của client. Nếu xác thực public key thành công, quá trình authentication thành công.

> NKey là lựa chọn thay thế tuyệt vời cho token (chuỗi xác thực) authentication, vì client kết nối phải chứng minh rằng mình sở hữu private key tương ứng với public key đã được cấp phép.

## Cài đặt nk

> 🇬🇧 *To get started with NKeys, you'll need the `nk` tool from [https://github.com/nats-io/nkeys/tree/master/nk](https://github.com/nats-io/nkeys/tree/master/nk) repository. If you have _go_ installed, enter the following at a command prompt:*

Để bắt đầu với NKeys, cần cài công cụ `nk` từ repository [https://github.com/nats-io/nkeys/tree/master/nk](https://github.com/nats-io/nkeys/tree/master/nk). Nếu đã cài _go_, chạy lệnh sau:

```bash
go install github.com/nats-io/nkeys/nk@latest
```

## Tạo NKeys và Cấu hình Server

> 🇬🇧 *To generate a _User_ NKEY:*

Để tạo NKEY cho _User_:

```shell
nk -gen user -pubout
```
```text
SUACSSL3UAHUDXKFSNVUZRF5UHPMWZ6BFDTJ7M6USDXIEDNPPQYYYCU3VY
UDXU4RCSJNZOIQHZNWXHXORDPRTGNJAHAHFRGZNEEJCPQTT2M7NLCNF4
```

> 🇬🇧 *The first output line starts with the letter `S` for _Seed_. The second letter `U` stands for _User_. Seeds are private keys; you should treat them as secrets and guard them with care.*

Dòng output đầu tiên bắt đầu bằng chữ `S` — viết tắt của _Seed_. Chữ thứ hai `U` là viết tắt của _User_. Seed là private key; hãy coi chúng là secret và bảo vệ cẩn thận.

> 🇬🇧 *The second line starts with the letter `U` for _User_, and is a public key which can be safely shared.*

Dòng thứ hai bắt đầu bằng chữ `U` — viết tắt của _User_, và là public key có thể chia sẻ công khai.

> 🇬🇧 *To use `nkey` authentication, add a user, and set the `nkey` property to the public key of the user you want to authenticate. You are only required to use the public key and no other properties are required. Here is a snippet of configuration for the `nats-server`:*

Để dùng `nkey` authentication, thêm user và đặt thuộc tính `nkey` bằng public key của user cần xác thực. Chỉ cần public key, không cần thuộc tính nào khác. Đây là đoạn config mẫu cho `nats-server`:

```
authorization: {
  users: [
    { nkey: UDXU4RCSJNZOIQHZNWXHXORDPRTGNJAHAHFRGZNEEJCPQTT2M7NLCNF4 }
  ]
}
```

> 🇬🇧 *To complete the end-to-end configuration and use an `nkey`, the [client is configured](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/auth\_intro/nkey\_auth#client-configuration) to use the seed, which is the private key.*

Để hoàn tất cấu hình đầu-cuối và sử dụng `nkey`, [client được cấu hình](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/auth\_intro/nkey\_auth#client-configuration) để dùng seed — chính là private key.

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **config**: cấu hình
- **secret**: chuỗi bí mật
- **server**: máy chủ
- **token**: chuỗi xác thực