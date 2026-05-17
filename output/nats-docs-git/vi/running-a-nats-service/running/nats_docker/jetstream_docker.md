---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/running/nats_docker/jetstream_docker
title: Chạy JetStream trong Docker
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Chạy JetStream trong Docker

> 🇬🇧 *This mini-tutorial shows how to run a NATS server with JetStream enabled in a local Docker container. This enables quick and consequence-free experimentation with the many features of JetStream.*

Mini-tutorial này hướng dẫn cách chạy NATS server với JetStream được bật trong một Docker container cục bộ. Cách này giúp thử nghiệm nhanh các tính năng của JetStream mà không lo ảnh hưởng đến môi trường thật.

> 🇬🇧 *Using the official `nats` image, start a server. The `-js` option is passed to the server to enable JetStream. The `-p` option forwards your local 4222 port to the server inside the container, 4222 is the default client connection port.*

Dùng image `nats` chính thức để khởi động server. Option `-js` kích hoạt JetStream. Option `-p` chuyển tiếp port 4222 trên máy cục bộ vào container — đây là port kết nối client mặc định.

```shell
docker run -p 4222:4222 nats -js
```

> 🇬🇧 *To persist JetStream data to a volume, you can use the `-v` option in combination with `-sd`:*

Để lưu dữ liệu JetStream vào volume, dùng option `-v` kết hợp với `-sd`:

```shell
docker run -p 4222:4222 -v nats:/data nats -js -sd /data
```

> 🇬🇧 *With the server running, use `nats bench` to create a stream and publish some messages to it.*

Sau khi server chạy, dùng `nats bench` để tạo stream (luồng message lưu trữ liên tục) và publish một số message lên đó.

```shell
nats bench -s localhost:4222 benchsubject --js --pub 1 --msgs=100000
```

> 🇬🇧 *JetStream persists the messages (on disk by default). Now consume them with:*

JetStream lưu các message xuống disk theo mặc định. Để consume (bên xử lý dữ liệu từ stream) chúng, chạy lệnh sau:

```shell
nats bench -s localhost:4222 benchsubject --js --sub 3 --msgs=100000
```

> 🇬🇧 *You can use `nats` to inspect various aspects of the stream, for example:*

Dùng `nats` để kiểm tra các thông tin của stream, ví dụ:

```shell
nats -s localhost:4222 stream list
╭────────────────────────────────────────────────────────────────────────────────────╮
│                                       Streams                                      │
├─────────────┬─────────────┬─────────────────────┬──────────┬────────┬──────────────┤
│ Name        │ Description │ Created             │ Messages │ Size   │ Last Message │
├─────────────┼─────────────┼─────────────────────┼──────────┼────────┼──────────────┤
│ benchstream │             │ 2024-06-07 20:26:38 │ 100,000  │ 16 MiB │ 35s          │
╰─────────────┴─────────────┴─────────────────────┴──────────┴────────┴──────────────╯
```

### Tài liệu liên quan:
 * Official [Docker image for the NATS server on GitHub](https://github.com/nats-io/nats-docker) and [issues](https://github.com/nats-io/nats-docker/issues)
 * [`nats` images on DockerHub](https://hub.docker.com/_/nats)
 * [`nats` CLI tool](/using-nats/nats-tools/nats\_cli/) and [`nats bench`](/using-nats/nats-tools/nats\_cli/natsbench)
 * [`Administer JetStream`](/nats\_admin/jetstream\_admin/)

## Thuật ngữ trong bài

- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **stream**: luồng message lưu trữ liên tục