---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools
title: Công cụ dòng lệnh NATS
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Công cụ dòng lệnh NATS

## Sử dụng NATS từ ứng dụng client

> 🇬🇧 *The most common form of connecting to the NATS messaging system will be through an application built with any of the [40+ client libraries](../developing-with-nats/developer.md) available for NATS.*

Cách phổ biến nhất để kết nối với hệ thống messaging NATS là thông qua ứng dụng được xây dựng bằng một trong số [hơn 40 client library](../developing-with-nats/developer.md) có sẵn cho NATS.

> 🇬🇧 *The client application will connect to an instance of the NATS server, be it a single server, a cluster of servers or even a global super-cluster such as [Synadia Cloud](https://www.synadia.com/cloud?utm_source=nats_docs&utm_medium=nats), sending and receiving messages via a range of subscribers contracts. If the application is written in GoLang the NATS server can even be [embedded into a Go](https://dev.to/karanpratapsingh/embedding-nats-in-go-19o) application.*

Ứng dụng client (bên gọi phía người dùng) sẽ kết nối đến một instance NATS server — có thể là server đơn lẻ, một cluster (cụm nhiều server chạy chung) hoặc thậm chí là super-cluster toàn cầu như [Synadia Cloud](https://www.synadia.com/cloud?utm_source=nats_docs&utm_medium=nats) — để gửi và nhận message thông qua các subscriber. Nếu ứng dụng được viết bằng GoLang, NATS server còn có thể được [nhúng trực tiếp vào ứng dụng Go](https://dev.to/karanpratapsingh/embedding-nats-in-go-19o).

> 🇬🇧 *Client APIs will also allow access to almost all server configuration tasks when using an account with sufficient permissions.*

Client API cũng cho phép thực hiện hầu hết các tác vụ cấu hình server khi dùng tài khoản có đủ permission (quyền truy cập).

## Các công cụ dòng lệnh

> 🇬🇧 *Besides using the client API to manage NATS servers, the NATS ecosystem also has many tools to interact with other applications and services over NATS and streams, support server configuration, enhance monitoring or tune performance such as:*

Ngoài việc dùng client API để quản lý NATS server, hệ sinh thái NATS còn cung cấp nhiều công cụ để tương tác với các ứng dụng và service qua NATS và stream (luồng message lưu trữ liên tục), hỗ trợ cấu hình server, giám sát và tối ưu hiệu năng:

* Tương tác và quản lý chung
  * [nats](./nats_cli) - The `nats` Command Line Tool là cách dễ nhất để tương tác, kiểm thử và quản lý NATS cùng JetStream từ terminal hoặc script. Danh sách tính năng ngày càng được mở rộng, hãy tải [phiên bản mới nhất](https://github.com/nats-io/natscli/releases).
* Bảo mật
  * [nk](./nk.md) - Tạo NKey dùng với JSON Web Token (JWT) trong nsc
  * [nsc](./nsc) - Cấu hình Operator, Account, User và permission offline rồi push lên server production. Đây là công cụ được khuyến nghị để tạo cấu hình bảo mật, trừ khi bạn đang dùng [Synadia Control Plane](https://www.docs.synadia.com/platform/control-plane?utm_source=nats_docs&utm_medium=nats)
  * [nats account server](https://nats-io.gitbook.io/legacy-nats-docs/nats-account-server) - (**legacy, đã được thay thế bởi NATS resolver tích hợp sẵn**) một security server tùy chỉnh. NAS vẫn có thể dùng làm tài liệu tham chiếu cho các tích hợp bảo mật riêng.
* Giám sát
  * [nats top](./nats_top) - Giám sát NATS Server
  * [prometheus-nats-exporter](https://github.com/nats-io/prometheus-nats-exporter) - Xuất metric (số liệu đo lường) của NATS server sang [Prometheus](https://prometheus.io/) và dashboard [Grafana](https://grafana.com).
* Benchmark
  * Xem subcommand [nats bench](./nats_cli/natsbench.md) của công cụ [nats](./nats_cli)

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **cluster**: cụm nhiều server chạy chung
- **message**: gói dữ liệu được gửi đi
- **metric**: số liệu đo lường
- **permission**: quyền truy cập
- **server**: máy chủ
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subscriber**: bên đăng ký nhận message