---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/reconnect/wait
title: Tạm Dừng Giữa Các Lần Thử Kết Nối Lại
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Tạm Dừng Giữa Các Lần Thử Kết Nối Lại

> 🇬🇧 *It doesn't make much sense to try to connect to the same server over and over. To prevent this sort of thrashing, and wasted reconnect attempts, especially when using TLS, libraries provide a wait setting. Generally clients make sure that between two reconnect attempts to the **same** server at least a certain amount of time has passed. The concrete implementation depends on the library used.*

Cố kết nối lại cùng một server liên tục là không hiệu quả. Để tránh tình trạng này và các lần retry (thử lại khi fail) lãng phí tài nguyên — đặc biệt khi dùng TLS (mã hóa TLS) — các library cung cấp tùy chọn wait. Thông thường, client đảm bảo rằng giữa hai lần retry đến **cùng** một server phải cách nhau ít nhất một khoảng thời gian nhất định. Cách hiện thực cụ thể tùy thuộc vào library được sử dụng.

> 🇬🇧 *This setting not only prevents wasting client resources, it also alleviates a [_thundering herd_](./random.md) situation when additional servers are not available.*

Tùy chọn này không chỉ giúp tiết kiệm tài nguyên phía client, mà còn giảm thiểu tình trạng [_thundering herd_](./random.md) khi không có server dự phòng khả dụng.

#### Go

```go
// Set reconnect interval to 10 seconds
nc, err := nats.Connect("demo.nats.io", nats.ReconnectWait(10*time.Second))
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
    .reconnectWait(Duration.ofSeconds(10))  // Set Reconnect Wait
    .build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
const nc = await connect({
    reconnectTimeWait: 10 * 1000, // 10s
    servers: ["demo.nats.io"],
});
```

#### Python

```python
nc = NATS()
await nc.connect(
   servers=["nats://demo.nats.io:4222"],
   reconnect_time_wait=10,
   )

# Do something with the connection

await nc.close()
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using NATS.Client.Core;

await using var client = new NatsClient(new NatsOpts
{
    Url = "nats://127.0.0.1:1222,nats://127.0.0.1:1223,nats://127.0.0.1:1224",
    
    // Set reconnect interval to between 5-10 seconds
    ReconnectWaitMin = TimeSpan.FromSeconds(5),
    ReconnectWaitMax = TimeSpan.FromSeconds(10),
});
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(servers: ["nats://127.0.0.1:1222", "nats://127.0.0.1:1223", "nats://127.0.0.1:1224"], reconnect_time_wait: 10) do |nc|
   # Do something with the connection

   # Close the connection
   nc.close
end
```

#### C

```c
natsConnection      *conn      = NULL;
natsOptions         *opts      = NULL;
natsStatus          s          = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    // Set reconnect interval to 10 seconds (10,000 milliseconds)
    s = natsOptions_SetReconnectWait(opts, 10000);
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **retry**: thử lại khi fail
- **server**: máy chủ
- **TLS**: mã hóa TLS