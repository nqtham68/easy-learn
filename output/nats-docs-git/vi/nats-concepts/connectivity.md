---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/connectivity
title: Kết nối NATS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Kết nối NATS

> 🇬🇧 *NATS supports several kinds of connectivity _directly_ to the NATS servers.*

NATS hỗ trợ nhiều kiểu kết nối _trực tiếp_ đến các NATS server.

> 🇬🇧 *- Plain NATS connections*
> *- TLS encrypted NATS connections*
> *- [WebSocket](https://github.com/nats-io/nats.ws) NATS connections*
> *- [MQTT](../running-a-nats-service/configuration/mqtt) client connections*

* Kết nối NATS thuần (plain)
* Kết nối NATS mã hóa bằng TLS (mã hóa TLS)
* Kết nối NATS qua [WebSocket](https://github.com/nats-io/nats.ws) (giao thức WebSocket)
* Kết nối [MQTT](../running-a-nats-service/configuration/mqtt) client

> 🇬🇧 *There is also a number of adapters available to bridge traffic to and from other messaging systems*

Ngoài ra còn có các adapter để bridge lưu lượng đến/đi từ các hệ thống messaging khác.

> 🇬🇧 *- [Kafka Bridge](https://github.com/nats-io/nats-kafka)*
> *- [JMS](https://github.com/nats-io/nats-jms-bridge) which can also be used to bridge MQ and RabbitMQ, since they both offer a JMS interface*

* [Kafka Bridge](https://github.com/nats-io/nats-kafka)
* [JMS](https://github.com/nats-io/nats-jms-bridge) — có thể dùng để bridge cả MQ và RabbitMQ vì cả hai đều cung cấp JMS interface

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **TLS**: mã hóa TLS
- **WebSocket**: giao thức WebSocket