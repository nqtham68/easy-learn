---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/clustering/jetstream_clustering/troubleshooting
title: Xử lý sự cố
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Xử lý sự cố

> 🇬🇧 *Diagnosing problems in NATS JetStream clusters requires: knowledge of [JetStream concepts](../../../../nats-concepts/jetstream) and knowledge of the [NATS Command Line Interface (CLI)](https://github.com/nats-io/natscli#the-nats-command-line-interface)*

Để chẩn đoán sự cố trong NATS JetStream cluster (cụm nhiều server chạy chung), bạn cần nắm:

* kiến thức về [các khái niệm JetStream](../../../../nats-concepts/jetstream)
* kiến thức về [NATS Command Line Interface (CLI)](https://github.com/nats-io/natscli#the-nats-command-line-interface)

> 🇬🇧 *The following tips and commands (while not an exhaustive list) can be useful when diagnosing problems in NATS JetStream clusters:*

Các gợi ý và lệnh dưới đây (không phải danh sách đầy đủ) có thể hữu ích khi chẩn đoán sự cố trong NATS JetStream cluster:

## Gợi ý xử lý sự cố

> 🇬🇧 *1. Look at [nats-server](https://github.com/nats-io/nats-server) logs. By default, only warning and error logs are produced, but debug and trace logs can be turned on from the command line using `-D` and `-DV`, respectively. Alternatively, enabling `debug` or `trace` in the [server config](../..#monitoring-and-tracing).*

1. Xem log của [nats-server](https://github.com/nats-io/nats-server). Mặc định chỉ có log warning và error, nhưng có thể bật log debug và trace từ dòng lệnh bằng `-D` và `-DV` tương ứng. Hoặc có thể bật `debug` hay `trace` trong [server config](../..#monitoring-and-tracing).

> 🇬🇧 *2. Make sure that in the [NATS JetStream configuration](.#configuration), at least one system user is configured in this section: `{ $SYS { users } }`.*

2. Đảm bảo trong [cấu hình NATS JetStream](.#configuration) có ít nhất một system user được khai báo trong mục: `{ $SYS { users } }`.

### Lệnh `nats account`

| Lệnh                                                                 | Mô tả                                 |
| ----------------------------------------------------------------------- | ------------------------------------------- |
| [`nats account info`](https://docs.nats.io/running-a-nats-service/nats\_admin/jetstream\_admin/account) | Xác nhận JetStream đã được bật trên account |

### Lệnh `nats server` cơ bản

| Lệnh                                                       | Mô tả                            |
| ------------------------------------------------------------- | -------------------------------------- |
| `nats server ls`                                              | Liệt kê các server đã biết                     |
| `nats server ping`                                            | Ping tất cả server                       |
| `nats server info`                                            | Hiển thị thông tin một server cụ thể |
| [`nats server check`](../../../clients.md#testing-your-setup) | Kiểm tra sức khỏe NATS server          |

### Lệnh `nats server report`

| Lệnh                                                                       | Mô tả                  |
| ----------------------------------------------------------------------------- | ---------------------------- |
| `nats server report connections`                                              | Báo cáo kết nối        |
| `nats server report accounts`                                                 | Báo cáo hoạt động account   |
| [`nats server report jetstream`](./administration.md#viewing-the-cluster-state) | Báo cáo hoạt động JetStream |

### Lệnh `nats server request`

| Lệnh                                                                        | Mô tả                   |
| ------------------------------------------------------------------------------ | ----------------------------- |
| [`nats server request jetstream`](./administration.md#viewing-the-cluster-state) | Hiển thị chi tiết JetStream        |
| `nats server request subscriptions`                                            | Hiển thị thông tin subscription |
| `nats server request variables`                                                | Hiển thị biến runtime        |
| `nats server request connections`                                              | Hiển thị chi tiết kết nối       |
| `nats server request routes`                                                   | Hiển thị chi tiết route          |
| `nats server request gateways`                                                 | Hiển thị chi tiết gateway         |
| `nats server request leafnodes`                                                | Hiển thị chi tiết leafnode        |
| `nats server request accounts`                                                 | Hiển thị chi tiết account         |

### Lệnh `nats server cluster`

| Lệnh                                                                                       | Mô tả                                                          |
| --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [`nats server cluster step-down`](./administration.md#forcing-stream-and-consumer-leader-election) | Buộc bầu leader (server chính trong nhóm replica) mới bằng cách cho leader hiện tại đứng xuống |
| [`nats server cluster peer-remove`](./administration.md#evicting-a-peer)                           | Xóa một server khỏi JetStream cluster                            |

### Lệnh thử nghiệm

| Lệnh                                                                                | Mô tả                                      |
| -------------------------------------------------------------------------------------- | ------------------------------------------------ |
| [`nats traffic`](https://github.com/nats-io/natscli/blob/main/cli/traffic\_command.go) | Giám sát traffic NATS. (**Lệnh thử nghiệm**) |

## Tài liệu tham khảo thêm

* [Kiểm tra cài đặt của bạn](../../../clients.md#testing-your-setup)

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **leader**: server chính trong nhóm replica
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục