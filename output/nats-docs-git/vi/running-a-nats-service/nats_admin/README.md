---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin
title: Quản lý và Giám sát Hạ tầng NATS Server
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Quản lý và Giám sát Hạ tầng NATS Server

> 🇬🇧 *Managing a NATS Server is simple, typical lifecycle operations include:*

Quản lý NATS Server khá đơn giản. Các thao tác vòng đời thông thường bao gồm:

* Dùng CLI tool [`nats`](https://docs.nats.io/using-nats/nats-tools/nats\_cli) để kiểm tra kết nối và độ trễ trong cluster (cụm nhiều server chạy chung), lấy thông tin account, cũng như quản lý và tương tác với stream (luồng message lưu trữ liên tục). Thử các ví dụ sau để nắm những cách dùng `nats` phổ biến nhất.
  * `nats cheat`
  * `nats cheat server`
  * `nats stream --help` để giám sát, quản lý và tương tác với stream
  * `nats consumer --help` để giám sát, quản lý stream consumer (bên xử lý dữ liệu từ stream)
  * `nats context --help` khi cần chuyển đổi giữa các server, cluster hoặc credential người dùng
* Dùng CLI tool [`nsc`](../../using-nats/nats-tools/nsc) khi sử dụng xác thực và phân quyền dựa trên JWT, để tạo, thu hồi JWT và key cho operator, account và user (tức các ứng dụng client).
* [Gửi signal](./signals.md) đến server để reload config hoặc xoay vòng file log.
* [Nâng cấp](https://docs.nats.io/running-a-nats-service/nats_admin/upgrading\_cluster) server (hoặc cluster).
* Tìm hiểu về [slow consumer](https://docs.nats.io/running-a-nats-service/nats_admin/slow\_consumers).
* Giám sát server qua:
  * [Endpoint](./monitoring) giám sát và các công cụ như [nats-top](https://docs.nats.io/using-nats/nats-tools/nats\_top)
  * Đăng ký nhận [system event](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts)
    * Tùy chọn thương mại cho giám sát high-cardinality qua system account: [Synadia Insights](https://www.synadia.com/insights)
* Tắt server an toàn bằng [Lame Duck Mode](https://docs.nats.io/running-a-nats-service/nats_admin/lame\_duck\_mode).

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **credential**: thông tin đăng nhập
- **endpoint**: địa chỉ API cụ thể
- **stream**: luồng message lưu trữ liên tục