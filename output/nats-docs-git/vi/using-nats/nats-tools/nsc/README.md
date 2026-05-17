---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nsc
title: Công cụ nsc
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Công cụ nsc

> 🇬🇧 *NATS account configurations are built using the `nsc` tool. The NSC tool allows you to:*
>
> *- Create and edit Operators, Accounts, Users*
> *- Manage publish and subscribe permissions for Users*
> *- Define Service and Stream exports from an account*
> *- Reference Service and Streams from another account*
> *- Generate Activation tokens that grants access to a private service or stream*
> *- Generate User credential files*
> *- Describe Operators, Accounts, Users, and Activations*
> *- Push and pull account JWTs to an account JWTs server*

Cấu hình NATS account được xây dựng bằng công cụ `nsc`. NSC cho phép thực hiện các thao tác sau:

* Tạo và chỉnh sửa Operators, Accounts, Users
* Quản lý permission (quyền truy cập) publish và subscribe cho Users
* Định nghĩa việc export Service và Stream (luồng message lưu trữ liên tục) từ một account
* Tham chiếu Service và Stream từ account khác
* Tạo Activation token (chuỗi xác thực) để cấp quyền truy cập vào service hoặc stream riêng tư
* Tạo file credential (thông tin đăng nhập) cho User
* Mô tả Operators, Accounts, Users và Activations
* Push và pull account JWT lên/xuống account JWT server

## Cài đặt

> 🇬🇧 *Installing `nsc` is easy:*

Cài đặt `nsc` rất đơn giản:

```shell
curl -L https://raw.githubusercontent.com/nats-io/nsc/master/install.py | python
```

> Additional ways of installing nsc are described at [nsc's github repository](https://github.com/nats-io/nsc#install)

Script sẽ tải phiên bản mới nhất của `nsc` và cài đặt vào hệ thống.

> 🇬🇧 *In case NSC is not initialized already do `nsc init`*

Nếu NSC chưa được khởi tạo, hãy chạy `nsc init`.

> 🇬🇧 *Output of `tree -L 2 nsc/`*

Output của `tree -L 2 nsc/`
```text
nsc/
├── accounts
│   ├── nats
│   └── nsc.json
└── nkeys
    ├── creds
    └── keys
5 directories, 1 file
```

> 🇬🇧 ***IMPORTANT**: `nsc` version 2.2.0 has been released. This version of nsc only supports `nats-server` v2.2.0 and `nats-account-server` v1.0.0. For more information please refer to the [nsc 2.2.0 release notes](https://github.com/nats-io/nsc/releases/tag/2.2.0).*

**QUAN TRỌNG**: `nsc` phiên bản 2.2.0 đã được phát hành. Phiên bản nsc này chỉ hỗ trợ `nats-server` v2.2.0 và `nats-account-server` v1.0.0. Xem thêm tại [nsc 2.2.0 release notes](https://github.com/nats-io/nsc/releases/tag/2.2.0).

## Hướng dẫn thực hành

> 🇬🇧 *You can find various task-oriented tutorials to working with the tool here:*

Các hướng dẫn thực hành theo từng tác vụ có thể tìm thấy tại đây:

* [Sử dụng cơ bản](./basics.md)
* [Cấu hình Import/Export Account Streams](./streams.md)
* [Cấu hình Import/Export Account Services](./services.md)
* [Signing Keys](./signing_keys.md)
* [Thu hồi Users hoặc Activations](./revocation.md)
* [Làm việc với Managed Operators](./managed.md)

## Tài liệu công cụ

> 🇬🇧 *For more specific browsing of the tool syntax, check out the `nsc` tool documentation. It can be found within the tool itself:*

Để tra cứu cú pháp chi tiết của công cụ, xem tài liệu `nsc` ngay trong tool:

```shell
nsc help
```

> 🇬🇧 *Or an online version [here](https://nats-io.github.io/nsc).*

Hoặc xem phiên bản trực tuyến [tại đây](https://nats-io.github.io/nsc).

## Thuật ngữ trong bài

- **credential**: thông tin đăng nhập
- **permission**: quyền truy cập
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **token**: chuỗi xác thực