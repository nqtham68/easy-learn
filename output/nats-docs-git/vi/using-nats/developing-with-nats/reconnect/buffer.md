---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/reconnect/buffer
title: Buffer Message Khi Đang Thử Kết Nối Lại
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Buffer Message Khi Đang Thử Kết Nối Lại

> 🇬🇧 *The Core NATS client libraries try as much as possible to be fire and forget, and you should use JetStream functionalities to get higher qualities of service that can deal with Core NATS messages being dropped due to the server connection being interrupted. That said, one of the features that may be included in the library you are using is the ability to buffer outgoing messages when the connection is down.*

Các client library của Core NATS được thiết kế theo hướng "gửi và quên" (fire-and-forget). Để đảm bảo độ tin cậy cao hơn khi message (gói dữ liệu được gửi đi) bị mất do mất kết nối với server, nên sử dụng JetStream. Tuy nhiên, một số library còn hỗ trợ tính năng buffer (vùng đệm tạm) các message gửi đi khi kết nối đang bị gián đoạn.

> 🇬🇧 *During a short reconnect, the client can allow applications to publish messages that, because the server is offline, will be cached in the client. The library will then send those messages once reconnected. When the maximum reconnect buffer is reached, messages will no longer be publishable by the client and an error will be returned.*

Trong thời gian kết nối lại ngắn, client cho phép ứng dụng tiếp tục publish message — các message này sẽ được lưu tạm trong client khi server chưa sẵn sàng. Khi kết nối được khôi phục, library sẽ tự động gửi lại các message đó. Nếu buffer đầy, client sẽ từ chối publish và trả về lỗi.

> 🇬🇧 *Be aware, while the message appears to be sent to the application it is possible that it is never sent because the connection is never remade. Your applications should use patterns like acknowledgements or use the JetStream publish call to ensure delivery.*

Cần lưu ý rằng mặc dù ứng dụng thấy message đã được gửi, thực tế message có thể không bao giờ đến đích nếu kết nối không được khôi phục. Hãy dùng các cơ chế như acknowledgement hoặc gọi JetStream publish để đảm bảo message được giao thành công.

> 🇬🇧 *For clients that support this feature, you are able to configure the size of this buffer with bytes, messages or both.*

Với các client hỗ trợ tính năng này, có thể cấu hình kích thước buffer theo bytes, số lượng message, hoặc cả hai.

#### Go

```go
// Set reconnect buffer size in bytes (5 MB)
nc, err := nats.Connect("demo.nats.io", nats.ReconnectBufSize(5*1024*1024))
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
Options options = new Options.Builder()
    .server("nats://demo.nats.io:4222")
    .reconnectBufferSize(5 * 1024 * 1024)  // Set buffer in bytes
    .build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
// Reconnect buffer size is not configurable on NATS JavaScript client
```

#### Python

```python
# Asyncio NATS client currently does not implement a reconnect buffer
```

#### C#

```csharp
// Reconnect buffer size is not configurable on NATS .NET client
```

#### Ruby

```ruby
# There is currently no reconnect pending buffer as part of the Ruby NATS client
```

#### C

```c
natsConnection      *conn      = NULL;
natsOptions         *opts      = NULL;
natsStatus          s          = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    // Set reconnect buffer size in bytes (5 MB)
    s = natsOptions_SetReconnectBufSize(opts, 5*1024*1024);
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

> _Như đã đề cập xuyên suốt tài liệu này, mỗi client library có thể có hành vi khác nhau đôi chút. Vui lòng tham khảo tài liệu của library bạn đang sử dụng._

## Thuật ngữ trong bài

- **buffer**: vùng đệm tạm
- **client**: bên gọi (phía người dùng)
- **message**: gói dữ liệu được gửi đi
- **server**: máy chủ