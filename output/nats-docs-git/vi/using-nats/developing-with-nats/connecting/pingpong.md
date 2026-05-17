---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/pingpong
title: Giao thức Ping/Pong
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Giao thức Ping/Pong

> 🇬🇧 *NATS client applications use a PING/PONG protocol to check that there is a working connection to the NATS service. Periodically the client will send PING messages to the server, which responds with a PONG. This period is configured by specifying a ping interval on the client connection settings.*

Ứng dụng NATS client sử dụng giao thức PING/PONG để kiểm tra kết nối với NATS service. Định kỳ, client sẽ gửi message (gói dữ liệu được gửi đi) PING lên server; server phản hồi bằng PONG. Chu kỳ này được cấu hình thông qua tham số ping interval trong config (cấu hình) kết nối của client.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/pingpong.svg)

> 🇬🇧 *The connection will be closed as stale when the client reaches a number of pings which recieved no pong in response, which is configured by specifying the maximum pings outstanding on the client connection settings.*

Kết nối sẽ bị đóng do hết hiệu lực (stale) khi client gửi đủ số lần PING mà không nhận được PONG tương ứng. Giới hạn này được thiết lập qua tham số maximum pings outstanding trong config kết nối của client.

> 🇬🇧 *The ping interval and the maximum pings outstanding work together to specify how quickly the client connection will be notified of a problem. This will also help when there is a remote network partition where the operating system does not detect a socket error. Upon connection close, the client will attempt to reconnect. When it knows about other servers, these will be tried next.*

Ping interval và maximum pings outstanding phối hợp với nhau để xác định mức độ nhanh chóng client phát hiện sự cố kết nối. Cơ chế này còn hữu ích khi xảy ra network partition từ xa mà hệ điều hành không phát hiện được lỗi socket. Sau khi kết nối bị đóng, client sẽ tự động thử kết nối lại và lần lượt thử các server khác nếu biết đến chúng.

> 🇬🇧 *In the presence of traffic, such as messages or client side pings, the server will not initiate the PING/PONG interaction.*

Khi có lưu lượng truyền đi — chẳng hạn message hoặc ping từ phía client — server sẽ không tự khởi tạo chu trình PING/PONG.

> 🇬🇧 *On connections with significant traffic, the client will often figure out there is a problem between PINGS, and as a result the default ping interval is typically on the order of minutes. To close an unresponsive connection after 100s, set the ping interval to 20s and the maximum pings outstanding to 5:*

Trên các kết nối có lưu lượng lớn, client thường phát hiện sự cố giữa các lần PING, do đó ping interval mặc định thường được đặt ở mức vài phút. Để đóng kết nối không phản hồi sau 100 giây, hãy đặt ping interval là 20 giây và maximum pings outstanding là 5:

#### Go

```go
// Set Ping Interval to 20 seconds and Max Pings Outstanding to 5
nc, err := nats.Connect("demo.nats.io", nats.Name("API Ping Example"), nats.PingInterval(20*time.Second), nats.MaxPingsOutstanding(5))
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
Options options = new Options.Builder()
    .server("nats://demo.nats.io")
    .pingInterval(Duration.ofSeconds(20)) // Set Ping Interval
    .maxPingsOut(5) // Set max pings in flight
    .build();

// Connection is AutoCloseable
try (Connection nc = Nats.connect(options)) {
    // Do something with the connection
}
```

#### JavaScript

```javascript
// Set Ping Interval to 20 seconds and Max Pings Outstanding to 5
const nc = await connect({
    pingInterval: 20 * 1000,
    maxPingOut: 5,
    servers: ["demo.nats.io:4222"],
});
```

#### Python

```python
nc = NATS()

await nc.connect(
   servers=["nats://demo.nats.io:4222"],
   # Set Ping Interval to 20 seconds and Max Pings Outstanding to 5
   ping_interval=20,
   max_outstanding_pings=5,
   )

# Do something with the connection.
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using NATS.Client.Core;

await using var client = new NatsClient(new NatsOpts
{
    Url = "nats://demo.nats.io:4222",
    
    // Set Ping Interval to 20 seconds and Max Pings Outstanding to 5
    PingInterval = TimeSpan.FromSeconds(20),
    MaxPingOut = 5,
});
```

#### Ruby

```ruby
require 'nats/client'
# Set Ping Interval to 20 seconds and Max Pings Outstanding to 5
NATS.start(ping_interval: 20, max_outstanding_pings: 5) do |nc|
   nc.on_reconnect do
    puts "Got reconnected to #{nc.connected_server}"
  end

  nc.on_disconnect do |reason|
    puts "Got disconnected! #{reason}"
  end

  # Do something with the connection
end
```

#### C

```c
natsConnection      *conn    = NULL;
natsOptions         *opts    = NULL;
natsStatus          s        = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    // Set Ping interval to 20 seconds (20,000 milliseconds)
    s = natsOptions_SetPingInterval(opts, 20000);
if (s == NATS_OK)
    // Set the limit to 5
    s = natsOptions_SetMaxPingsOut(opts, 5);
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **config**: cấu hình
- **message**: gói dữ liệu được gửi đi
- **server**: máy chủ
- **service**: dịch vụ