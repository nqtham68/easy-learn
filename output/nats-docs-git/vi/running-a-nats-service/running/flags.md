---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/running/flags
title: Các Flag Khởi Động NATS Server
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Các Flag Khởi Động NATS Server

> 🇬🇧 *The NATS server has many flags to customize its behavior without having to write a configuration file.*

NATS server cung cấp nhiều flag để tùy chỉnh hoạt động mà không cần viết file config (cấu hình).

> 🇬🇧 *The configuration flags revolve around:*

Các flag được chia theo nhóm chức năng:

* Server Options
* Logging
* Authorization
* TLS Security
* Clustering
* Information

## Tùy Chọn Server

| Flag                  | Mô tả                                                                            |
| --------------------- | -------------------------------------------------------------------------------------- |
| `-a`, `--addr`, `--net` | Địa chỉ host để bind (mặc định: `0.0.0.0` - tất cả interfaces).                       |
| `-p`, `--port`        | Port kết nối NATS client (mặc định: 4222).                                                      |
| `-n`, `--name`, `--server_name` | Tên server (mặc định tự động).                                                   |
| `-P`, `--pid`         | File lưu trữ process ID (PID).                                                    |
| `-m`, `--http_port`   | HTTP port cho monitoring dashboard (loại trừ `--https_port`).                      |
| `-ms`, `--https_port` | HTTPS port cho monitoring dashboard (loại trừ `--http_port`).           |
| `-c`, `--config`      | Đường dẫn đến file config của NATS server.                                                |
| `-sl`, `--signal`     | Gửi signal đến tiến trình nats-server. Xem [process signaling](../nats_admin/signals.md). |
| `--client_advertise`  | HostPort client để quảng bá đến các server khác.                                         |
| `-t`                  | Kiểm tra cấu hình rồi thoát.                                                            |
| `--ports_file_dir     | Tạo file ports trong thư mục chỉ định (<executable_name>_<pid>.ports).       |

## Tùy Chọn JetStream

| Flag                 | Mô tả                     |
| -------------------- | ------------------------------- |
| `-js`, `--jetstream` | Bật tính năng JetStream. |
| `-sd`, `--store_dir` | Đặt thư mục lưu trữ cho stream (luồng message lưu trữ liên tục).      |

## Tùy Chọn Authentication

> 🇬🇧 *The following options control straightforward authentication:*

Các flag sau đây kiểm soát xác thực cơ bản:

| Flag     | Mô tả                                                                              |
| -------- | ---------------------------------------------------------------------------------------- |
| `--user` | _username_ bắt buộc cho kết nối (loại trừ `--auth`).                             |
| `--pass` | _password_ bắt buộc cho kết nối (loại trừ `--auth`).                             |
| `--auth` | _authorization token_ bắt buộc cho kết nối (loại trừ `--user` và `--password`). |

Xem thêm tại [token authentication](../configuration/securing_nats/auth_intro/tokens.md) và [username/password](../configuration/securing_nats/auth_intro/username_password.md).

## Tùy Chọn Logging

> 🇬🇧 *The following flags are available on the server to configure logging:*

Các flag sau đây dùng để cấu hình logging trên server:

| Flag                    | Mô tả                                                   |
| ----------------------- | ------------------------------------------------------------- |
| `-l`, `--log`           | File chuyển hướng log output.                                   |
| `-T`, `--logtime`       | Chỉ định `-T=false` để tắt timestamp trong log.        |
| `-s`, `--syslog`        | Ghi log ra syslog hoặc Windows event log.                            |
| `-r`, `--remote_syslog` | Địa chỉ syslog server, ví dụ `udp://localhost:514`.         |
| `-D`, `--debug`         | Bật debug output.                                       |
| `-V`, `--trace`         | Bật trace log cho protocol.                            |
| `-VV`                   | Verbose trace (bao gồm cả system account).                 |
| `-DV`                   | Bật đồng thời debug và protocol trace.                 |
| `-DVV`                  | Debug và verbose trace (bao gồm cả system account).       |
| `--max_traced_msg_len`  | Độ dài tối đa có thể in cho traced message. 0 là không giới hạn. |
| `--max_traced_msg_len`   | Độ dài tối đa có thể in cho traced message (mặc định: không giới hạn). |

Đọc thêm về [cấu hình logging tại đây](../configuration/logging.md).

## Tùy Chọn TLS

| Flag          | Mô tả                                |
| ------------- | ------------------------------------------ |
| `--tls`       | Bật TLS (mã hóa TLS), không xác thực client.          |
| `--tlscert`   | File certificate của server.                    |
| `--tlskey`    | Private key cho certificate server.         |
| `--tlsverify` | Bật xác thực TLS certificate phía client. |
| `--tlscacert` | CA certificate client để xác thực.     |

Đọc thêm về [cấu hình TLS tại đây](../configuration/securing_nats/tls.md).

## Tùy Chọn Cluster

> 🇬🇧 *The following flags are available on the server to configure clustering:*

Các flag sau đây dùng để cấu hình cluster (cụm nhiều server chạy chung) trên server:

| Flag                  | Mô tả                                                 |
| --------------------- | ----------------------------------------------------------- |
| `--routes`            | Danh sách URL cluster ngăn cách bằng dấu phẩy để kết nối. |
| `--cluster`           | Cluster URL cho các clustering request.                         |
| `--no_advertise`      | Không quảng bá thông tin cluster đến client.       |
| `--cluster_advertise` | Cluster URL để quảng bá đến các server khác.                   |
| `--connect_retries`   | Số lần retry kết nối cho implicit routes.              |
| `--cluster_listen`    | Cluster URL mà các member có thể dùng để tìm routes.           |

Đọc thêm về [cấu hình clustering tại đây](../configuration/clustering/README.md).

## Tùy Chọn Chung

| Flag              | Mô tả       |
| ----------------- | ----------------- |
| `-h`, `--help`    | Hiển thị thông báo trợ giúp. |
| `-v`, `--version` | Hiển thị phiên bản.      |
| `--help_tls`      | Trợ giúp TLS.          |

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **log**: bản ghi sự kiện
- **stream**: luồng message lưu trữ liên tục
- **TLS**: mã hóa TLS
- **token**: chuỗi xác thực