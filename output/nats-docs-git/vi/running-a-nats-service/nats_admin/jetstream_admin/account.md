---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/jetstream_admin/account
title: Thông Tin Tài Khoản
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Thông Tin Tài Khoản

## Thông Tin Tài Khoản

> 🇬🇧 *JetStream is multi-tenant so you will need to check that your account is enabled for JetStream and is not limited. You can view your limits as follows:*

JetStream hỗ trợ multi-tenant, vì vậy bạn cần kiểm tra xem tài khoản của mình đã được bật JetStream và chưa bị giới hạn hay chưa. Để xem các giới hạn của stream (luồng message lưu trữ liên tục) và consumer (bên xử lý dữ liệu từ stream), dùng lệnh sau:

```shell
nats account info
```
```text
Connection Information:
               Client ID: 8
               Client IP: 127.0.0.1
                     RTT: 178.545µs
       Headers Supported: true
         Maximum Payload: 1.0 MiB
           Connected URL: nats://localhost:4222
       Connected Address: 127.0.0.1:4222
     Connected Server ID: NCCOHA6ONXJOGAEZP4WPU4UJ3IQP2VVXEPRKTQCGBCW4IL4YYW4V4KKL
JetStream Account Information:
           Memory: 0 B of 5.7 GiB
          Storage: 0 B of 11 GiB
          Streams: 0 of Unlimited
   Max Consumers: unlimited
```

## Thuật ngữ trong bài

- **consumer**: bên xử lý dữ liệu từ stream
- **stream**: luồng message lưu trữ liên tục