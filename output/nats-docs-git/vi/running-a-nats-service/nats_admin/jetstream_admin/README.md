---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/jetstream_admin
title: Quản trị & Sử dụng qua CLI
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Quản trị & Sử dụng qua CLI

> 🇬🇧 *Once the server is running it's time to use the management tool. Please refer to the [installation section in the readme](https://github.com/nats-io/natscli?tab=readme-ov-file#installation).*

Sau khi server khởi động, đã đến lúc dùng công cụ quản lý. Xem hướng dẫn cài đặt tại [mục installation trong readme](https://github.com/nats-io/natscli?tab=readme-ov-file#installation).

```
nats --help
nats cheat
```

> 🇬🇧 *We'll walk through the above scenario and introduce features of the CLI and of JetStream as we recreate the setup above.*

Chúng ta sẽ đi qua kịch bản trên và giới thiệu các tính năng của CLI (công cụ dòng lệnh) cũng như JetStream khi tái tạo lại cấu hình đó.

> 🇬🇧 *Throughout this example, we'll show other commands like `nats pub` and `nats sub` to interact with the system. These are normal existing core NATS commands and JetStream is fully usable by only using core NATS.*

Xuyên suốt ví dụ này, chúng ta sẽ dùng thêm các lệnh như `nats pub` và `nats sub` để tương tác với hệ thống. Đây là các lệnh NATS core thông thường — JetStream hoàn toàn có thể dùng chỉ với NATS core.

> 🇬🇧 *We'll touch on some additional features but please review the section on the design model to understand all possible permutations.*

Chúng ta cũng sẽ đề cập thêm một số tính năng khác, nhưng hãy xem phần design model để hiểu đầy đủ các tổ hợp có thể có.

## Thuật ngữ trong bài

- **CLI**: công cụ dòng lệnh
- **consumer**: bên xử lý dữ liệu từ stream
- **stream**: luồng message lưu trữ liên tục