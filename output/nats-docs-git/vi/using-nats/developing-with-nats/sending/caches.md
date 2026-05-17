---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/sending/caches
title: Cache, Flush và Ping
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Cache, Flush và Ping

> 🇬🇧 *For performance reasons, most if not all, of the client libraries will buffer outgoing data so that bigger chunks can be written to the network at one time. This may be as simple as a byte buffer that stores a few messages before being pushed to the network.*

Vì lý do hiệu năng, hầu hết các thư viện client đều buffer (vùng đệm tạm) dữ liệu đầu ra để ghi các chunk lớn hơn lên mạng mỗi lần. Cơ chế này có thể đơn giản như một byte buffer lưu vài message (gói dữ liệu được gửi đi) trước khi đẩy lên mạng.

> 🇬🇧 *These buffers do not hold messages forever, generally they are designed to hold messages in high throughput scenarios, while still providing good latency in low throughput situations.*

Các buffer này không giữ message mãi mãi — chúng được thiết kế để xử lý tình huống throughput cao, trong khi vẫn đảm bảo độ trễ thấp khi throughput thấp.

> 🇬🇧 *It is the libraries job to make sure messages flow in a high performance manner. But there may be times when an application needs to know that a message has "hit the wire." In this case, applications can use a flush call to tell the library to move data through the system.*

Thư viện có trách nhiệm đảm bảo message được truyền đi với hiệu năng cao. Tuy nhiên, đôi khi ứng dụng cần biết chắc rằng một message đã thực sự được gửi lên mạng. Trong trường hợp đó, ứng dụng có thể dùng lệnh flush để yêu cầu thư viện đẩy toàn bộ dữ liệu qua hệ thống.

#### Go

```go
nc, err := nats.Connect("demo.nats.io")
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Just to not collide using the demo server with other users.
subject := nats.NewInbox()

if err := nc.Publish(subject, []byte("All is Well")); err != nil {
    log.Fatal(err)
}
// Sends a PING and wait for a PONG from the server, up to the given timeout.
// This gives guarantee that the server has processed the above message.
if err := nc.FlushTimeout(time.Second); err != nil {
    log.Fatal(err)
}
```

#### Java

```java
Connection nc = Nats.connect("nats://demo.nats.io:4222");

nc.publish("updates", "All is Well".getBytes(StandardCharsets.UTF_8));
nc.flush(Duration.ofSeconds(1)); // Flush the message queue

nc.close();
```

#### JavaScript

```javascript
const start = Date.now();
nc.flush().then(() => {
  t.log("round trip completed in", Date.now() - start, "ms");
});
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://demo.nats.io:4222"])

await nc.publish("updates", b'All is Well')

# Sends a PING and wait for a PONG from the server, up to the given timeout.
# This gives guarantee that the server has processed above message.
await nc.flush(timeout=1)
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;

await using var client = new NatsClient();

await client.PublishAsync("updates", "All is well");

// Sends a PING and wait for a PONG from the server.
// This gives a guarantee that the server has processed the above message
// since the underlining TCP connection sends and receives messages in order.
await client.PingAsync();
```

#### Ruby

```ruby
require 'nats/client'
require 'fiber'

NATS.start(servers:["nats://127.0.0.1:4222"]) do |nc|
  nc.subscribe("updates") do |msg|
    puts msg
  end

  nc.publish("updates", "All is Well")

  nc.flush do
    # Sends a PING and wait for a PONG from the server, up to the given timeout.
    # This gives guarantee that the server has processed above message at this point.
  end
end
```

#### C

```c
natsConnection      *conn      = NULL;
natsStatus          s          = NATS_OK;

s = natsConnection_ConnectTo(&conn, NATS_DEFAULT_URL);

// Send a request and wait for up to 1 second
if (s == NATS_OK)
    s = natsConnection_PublishString(conn, "foo", "All is Well");

// Sends a PING and wait for a PONG from the server, up to the given timeout.
// This gives guarantee that the server has processed the above message.
if (s == NATS_OK)
    s = natsConnection_FlushTimeout(conn, 1000);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
```

## Flush và Ping/Pong

> 🇬🇧 *Many of the client libraries use the [PING/PONG interaction](../connecting/pingpong.md) built into the NATS protocol to ensure that flush pushed all of the buffered messages to the server. When an application calls flush, most libraries will put a PING on the outgoing queue of messages, and wait for the server to respond with a PONG before saying that the flush was successful.*

Nhiều thư viện client dùng cơ chế [PING/PONG](../connecting/pingpong.md) tích hợp sẵn trong giao thức NATS để xác nhận rằng flush đã đẩy hết toàn bộ message đang buffer lên server. Khi ứng dụng gọi flush, hầu hết các thư viện sẽ đặt một PING vào queue (hàng đợi message) đầu ra và chờ server phản hồi bằng PONG trước khi xác nhận flush thành công.

> 🇬🇧 *Even though the client may use PING/PONG for flush, pings sent this way do not count towards [max outgoing pings](../connecting/pingpong.md).*

Dù client có thể dùng PING/PONG cho flush, các ping gửi theo cách này không được tính vào giới hạn [max outgoing pings](../connecting/pingpong.md).

## Thuật ngữ trong bài

- **buffer**: vùng đệm tạm
- **client**: bên gọi (phía người dùng)
- **message**: gói dữ liệu được gửi đi
- **queue**: hàng đợi message
- **server**: máy chủ