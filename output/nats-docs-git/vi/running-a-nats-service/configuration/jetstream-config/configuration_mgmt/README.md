---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/jetstream-config/configuration_mgmt
title: Quản lý Cấu hình
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Quản lý Cấu hình

> 🇬🇧 *In many cases managing the configuration in your application code is the best model, many teams though wish to pre-create Streams and Consumers.*

Trong nhiều trường hợp, quản lý config (cấu hình) ngay trong code ứng dụng là cách tiếp cận tốt nhất. Tuy nhiên, nhiều team muốn tạo sẵn Stream (luồng message lưu trữ liên tục) và Consumer (bên xử lý dữ liệu từ stream) trước khi chạy ứng dụng.

> 🇬🇧 *We support a number of tools to assist with this:*

Chúng tôi hỗ trợ một số công cụ để giúp việc này:

* [CLI with Configuration Files](./nats-admin-cli.md)
* [Terraform](./terraform.md)
* [GitHub Actions](./github_actions.md)
* [Kubernetes JetStream Controller](./kubernetes_controller.md)

## Thuật ngữ trong bài

- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **stream**: luồng message lưu trữ liên tục