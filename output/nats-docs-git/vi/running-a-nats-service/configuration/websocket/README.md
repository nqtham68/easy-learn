---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/websocket
title: WebSocket
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# WebSocket

> 🇬🇧 *_Supported since NATS Server version 2.2_*

_Hỗ trợ từ NATS Server phiên bản 2.2_

> 🇬🇧 *WebSocket support can be enabled in the server and may be used alongside the traditional TCP socket connections. TLS, compression and Origin Header checking are supported.*

WebSocket (giao thức WebSocket) có thể được bật trên server và dùng song song với kết nối TCP socket truyền thống. Hỗ trợ TLS (mã hóa TLS), nén dữ liệu và kiểm tra Origin Header.

> 🇬🇧 ***Important***

**Lưu ý quan trọng**

> 🇬🇧 ** NATS Supports only WebSocket data frames in Binary, not Text format \([https://tools.ietf.org/html/rfc6455\#section-5.6](https://tools.ietf.org/html/rfc6455#section-5.6)\). The server will always send in Binary and your clients MUST send in Binary too.*

* NATS chỉ hỗ trợ WebSocket data frame ở định dạng Binary, không phải Text \([https://tools.ietf.org/html/rfc6455\#section-5.6](https://tools.ietf.org/html/rfc6455#section-5.6)\). Server luôn gửi ở định dạng Binary và các client của bạn cũng PHẢI gửi ở định dạng Binary.

> 🇬🇧 ** For writers of client libraries: a WebSocket frame is not guaranteed to contain a full NATS protocol \(actually will generally not\). Any data from a frame must be going through a parser that can handle partial protocols. See the protocol description [here](../../../reference/nats-protocol/nats-protocol).*

* Dành cho người viết client library: một WebSocket frame không đảm bảo chứa đầy đủ một NATS protocol (thực tế thường không chứa đủ). Mọi dữ liệu từ frame phải đi qua một parser có khả năng xử lý partial protocol. Xem mô tả protocol [tại đây](../../../reference/nats-protocol/nats-protocol).

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **server**: máy chủ
- **TLS**: mã hóa TLS
- **WebSocket**: giao thức WebSocket