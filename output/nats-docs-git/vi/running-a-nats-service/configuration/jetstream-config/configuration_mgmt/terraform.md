---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/jetstream-config/configuration_mgmt/terraform
title: Terraform
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Terraform

> 🇬🇧 *[Terraform](https://www.terraform.io/) is a Cloud configuration tool from Hashicorp. We maintain a Provider for Terraform called [terraform-provider-jetstream](https://github.com/nats-io/terraform-provider-jetstream/) that can maintain JetStream using Terraform.*

[Terraform](https://www.terraform.io/) là công cụ config (cấu hình) Cloud của Hashicorp. Chúng tôi duy trì một Provider cho Terraform có tên [terraform-provider-jetstream](https://github.com/nats-io/terraform-provider-jetstream/) — cho phép quản lý JetStream stream (luồng message lưu trữ liên tục) thông qua Terraform.

> 🇬🇧 *Find it in the [Terraform registry](https://registry.terraform.io/providers/nats-io/jetstream/latest/docs).*

Tìm Provider này trên [Terraform registry](https://registry.terraform.io/providers/nats-io/jetstream/latest/docs).

## Cài đặt

> 🇬🇧 *In your project you can configure the Provider like this:*

Trong project của bạn, cấu hình Provider như sau:

```text
provider "jetstream" {
  servers = "connect.ngs.global"
  credentials = "ngs_jetstream_admin.creds"
}
```

> 🇬🇧 *Sample code below that creates the `ORDERS` example. Review the [Project README](https://github.com/nats-io/terraform-provider-jetstream#readme) for full details.*

Code mẫu dưới đây tạo ví dụ `ORDERS`. Xem [Project README](https://github.com/nats-io/terraform-provider-jetstream#readme) để biết toàn bộ chi tiết.

```text
resource "jetstream_stream" "ORDERS" {
  name     = "ORDERS"
  subjects = ["ORDERS.*"]
  storage  = "file"
  max_age  = 60 * 60 * 24 * 365
}

resource "jetstream_consumer" "ORDERS_NEW" {
  stream_id      = jetstream_stream.ORDERS.id
  durable_name   = "NEW"
  deliver_all    = true
  filter_subject = "ORDERS.received"
  sample_freq    = 100
}

resource "jetstream_consumer" "ORDERS_DISPATCH" {
  stream_id      = jetstream_stream.ORDERS.id
  durable_name   = "DISPATCH"
  deliver_all    = true
  filter_subject = "ORDERS.processed"
  sample_freq    = 100
}

resource "jetstream_consumer" "ORDERS_MONITOR" {
  stream_id        = jetstream_stream.ORDERS.id
  durable_name     = "MONITOR"
  deliver_last     = true
  ack_policy       = "none"
  delivery_subject = "monitor.ORDERS"
}

output "ORDERS_SUBJECTS" {
  value = jetstream_stream.ORDERS.subjects
}
```

## Thuật ngữ trong bài

- **config**: cấu hình
- **stream**: luồng message lưu trữ liên tục