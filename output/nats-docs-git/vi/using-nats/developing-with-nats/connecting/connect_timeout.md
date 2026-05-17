---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/connect_timeout
title: Đặt Thời Gian Chờ Kết Nối
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Đặt Thời Gian Chờ Kết Nối

> 🇬🇧 *Each library has its own, language preferred way, to pass connection options. One of the most common options is a connect timeout. It limits how long it can take to establish a connection to a server. Should multiple URLs be provided, this timeout applies to each cluster member individually. To set the maximum time to connect to a server to 10 seconds:*

Mỗi thư viện có cách riêng để truyền các tùy chọn kết nối theo đặc trưng của ngôn ngữ. Một trong những tùy chọn phổ biến nhất là timeout (thời gian chờ tối đa) kết nối. Tùy chọn này giới hạn thời gian tối đa để thiết lập kết nối đến server. Khi cung cấp nhiều URL, timeout này được áp dụng riêng cho từng thành viên trong cluster (cụm nhiều server chạy chung). Để đặt thời gian kết nối tối đa đến server là 10 giây:

#### Go

```go
nc, err := nats.Connect("demo.nats.io", nats.Name("API Options Example"), nats.Timeout(10*time.Second))
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
    .connectionTimeout(Duration.ofSeconds(10)) // Set timeout
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
  connect_timeout=10)

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
    Url = "nats://demo.nats.io:4222",
    ConnectTimeout = TimeSpan.FromSeconds(10)
});

// You don't have to call ConnectAsync() explicitly,
// first operation will make the connection otherwise.
await client.ConnectAsync();
```

#### Ruby

```ruby
# There is currently no connect timeout as part of the Ruby NATS client API, but you can use a timer to mimic it.
require 'nats/client'

timer = EM.add_timer(10) do
  NATS.connect do |nc|
    # Do something with the connection

    # Close the connection
    nc.close
  end
end
EM.cancel_timer(timer)
```

#### C

```c
nnatsConnection      *conn    = NULL;
 natsOptions         *opts    = NULL;
 natsStatus          s        = NATS_OK;

 s = natsOptions_Create(&opts);
 if (s == NATS_OK)
     // Set the timeout to 10 seconds (10,000 milliseconds)
     s = natsOptions_SetTimeout(opts, 10000);
 if (s == NATS_OK)
     s = natsConnection_Connect(&conn, opts);

 (...)

 // Destroy objects that were created
 natsConnection_Destroy(conn);
 natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **server**: máy chủ
- **timeout**: thời gian chờ tối đa