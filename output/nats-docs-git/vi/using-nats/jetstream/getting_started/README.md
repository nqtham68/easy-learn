---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/jetstream/getting_started
title: Bắt đầu với JetStream
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Bắt đầu với JetStream

> 🇬🇧 *Getting started with JetStream is straightforward. While we speak of JetStream as if it is a separate component, it's actually a subsystem built into the NATS server that needs to be enabled.*

Bắt đầu với JetStream rất đơn giản. Dù ta thường nói về JetStream như một thành phần riêng biệt, thực ra nó là một subsystem tích hợp sẵn trong NATS server (máy chủ) và chỉ cần được bật lên.

## Dòng lệnh

> 🇬🇧 *Enable JetStream by specifying the `-js` flag when starting the NATS server.*

Bật JetStream bằng cách thêm flag `-js` khi khởi động NATS server.

`$ nats-server -js`

## File cấu hình

> 🇬🇧 *You can also enable JetStream through a configuration file. By default, the JetStream subsytem will store data in the /tmp directory. Here's a minimal file that will store data in a local "nats" directory, suitable for development and local testing.*

Có thể bật JetStream qua một config (cấu hình) file. Mặc định, subsystem JetStream lưu dữ liệu vào thư mục `/tmp`. Dưới đây là file tối giản lưu dữ liệu vào thư mục "nats" cục bộ, phù hợp cho môi trường phát triển và kiểm thử.

`$ nats-server -c js.conf`

```text
# js.conf
jetstream {
   store_dir=nats
}
```

> 🇬🇧 *Normally JetStream will be run in clustered mode and will replicate data, so the best place to store JetStream data would be locally on a fast SSD. One should specifically avoid NAS or NFS storage for JetStream.*

Thông thường JetStream chạy ở chế độ cluster (cụm nhiều server chạy chung) và sẽ replicate (bản sao dữ liệu) dữ liệu, nên nơi lưu trữ tối ưu nhất là SSD tốc độ cao cục bộ. Cần tránh dùng NAS hoặc NFS cho JetStream.

> 🇬🇧 *See [Using Docker](../../../running-a-nats-service/running/nats_docker/jetstream_docker.md) and [Using Source](./using_source.md) for more information.*

Xem thêm tại [Using Docker](../../../running-a-nats-service/running/nats_docker/jetstream_docker.md) và [Using Source](./using_source.md).

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **replica**: bản sao dữ liệu
- **server**: máy chủ