---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/what-is-nats/walkthrough_setup
title: Thiết lập Môi trường Walkthrough
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Thiết lập Môi trường Walkthrough

> 🇬🇧 *We have provided Walkthroughs for you to try NATS (and JetStream) on your own. In order to follow along with the walkthroughs, you could choose one of these options:*

Chúng tôi cung cấp các bài Walkthrough để bạn tự thực hành NATS (và JetStream). Để theo dõi các bài này, bạn có thể chọn một trong các phương án sau:

* Cần cài đặt CLI tool (công cụ dòng lệnh) `nats` và một NATS server cục bộ (hoặc dùng remote server mà bạn có quyền truy cập).
* Bạn có thể dùng Synadia's NGS.
* Hoặc dùng demo server của NATS. Server này truy cập qua `nats://demo.nats.io` (đây là NATS connection URL, không phải browser URL — bạn truyền nó vào NATS client application).

## Cài đặt CLI Tool [`nats`](https://docs.nats.io/using-nats/nats-tools/nats\_cli)

> 🇬🇧 *Please refer to the [installation section in the readme](https://github.com/nats-io/natscli?tab=readme-ov-file#installation).*

Tham khảo [phần installation trong readme](https://github.com/nats-io/natscli?tab=readme-ov-file#installation).

## Cài đặt NATS Server cục bộ (nếu cần)

> 🇬🇧 *If you are going to run a server locally you need to first install it and start it. Please refer to the [nats server installation doc](../../running-a-nats-service/installation.md)*

Nếu bạn muốn chạy server (máy chủ) cục bộ, hãy cài đặt và khởi động nó trước. Xem hướng dẫn tại [nats server installation doc](../../running-a-nats-service/installation.md).

> 🇬🇧 *Alternatively if you already know how to use NATS on a remote server, you only need to pass the server URL to `nats` using the `-s` option or preferably create a context using `nats context add`, to specify the server URL(s) and credentials file containing your user JWT.*

Nếu bạn đã quen với NATS trên remote server, chỉ cần truyền server URL vào `nats` qua tùy chọn `-s`, hoặc tốt hơn là tạo một context bằng `nats context add` để chỉ định server URL và file credential (thông tin đăng nhập) chứa user JWT của bạn.

### Khởi động NATS Server (nếu cần)

> 🇬🇧 *To start a simple demonstration server locally, simply run:*

Để khởi động một server demo đơn giản cục bộ, chạy lệnh:

```bash
nats-server
```

> 🇬🇧 *(or `nats-server -m 8222` if you want to enable the HTTP monitoring functionality)*

(hoặc `nats-server -m 8222` nếu bạn muốn bật tính năng HTTP monitoring)

> 🇬🇧 *When the server starts successfully, you will see the following messages:*

Khi server khởi động thành công, bạn sẽ thấy các thông báo sau:

```
[14524] 2021/10/25 22:53:53.525530 [INF] Starting nats-server
[14524] 2021/10/25 22:53:53.525640 [INF]   Version:  2.6.1
[14524] 2021/10/25 22:53:53.525643 [INF]   Git:      [not set]
[14524] 2021/10/25 22:53:53.525647 [INF]   Name:     NDAUZCA4GR3FPBX4IFLBS4VLAETC5Y4PJQCF6APTYXXUZ3KAPBYXLACC
[14524] 2021/10/25 22:53:53.525650 [INF]   ID:       NDAUZCA4GR3FPBX4IFLBS4VLAETC5Y4PJQCF6APTYXXUZ3KAPBYXLACC
[14524] 2021/10/25 22:53:53.526392 [INF] Starting http monitor on 0.0.0.0:8222
[14524] 2021/10/25 22:53:53.526445 [INF] Listening for client connections on 0.0.0.0:4222
[14524] 2021/10/25 22:53:53.526684 [INF] Server is ready
```

> 🇬🇧 *The NATS server listens for client connections on TCP Port 4222.*

NATS server lắng nghe kết nối từ client trên TCP port (cổng kết nối) 4222.

## Thuật ngữ trong bài

- **CLI**: công cụ dòng lệnh
- **client**: bên gọi (phía người dùng)
- **credential**: thông tin đăng nhập
- **port**: cổng kết nối
- **server**: máy chủ