---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/specific_server
title: Kết nối tới một Server cụ thể
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Kết nối tới một Server cụ thể

> 🇬🇧 *The NATS client libraries can take a full URL, `nats://demo.nats.io:4222`, to specify a specific server host and port to connect to.*

Các thư viện client của NATS hỗ trợ truyền vào một URL đầy đủ, `nats://demo.nats.io:4222`, để chỉ định host (máy chủ vật lý/ảo) và port (cổng kết nối) cần kết nối tới.

> 🇬🇧 *Libraries are removing the requirement for an explicit protocol and may allow `demo.nats.io:4222` or just `demo.nats.io`. In the later example the default port 4222 will be used. Check with your specific client library's documentation to see what URL formats are supported.*

Các thư viện đang dần bỏ yêu cầu khai báo protocol tường minh — có thể dùng `demo.nats.io:4222` hoặc chỉ `demo.nats.io`. Ở dạng sau, port mặc định 4222 sẽ được sử dụng. Tham khảo tài liệu của thư viện client tương ứng để biết các định dạng URL được hỗ trợ.

> 🇬🇧 *For example, to connect to the demo server with a URL you can use:*

Ví dụ, để kết nối tới demo server bằng URL:

#### Go

```java
// If connecting to the default port, the URL can be simplified
// to just the hostname/IP.
// That is, the connect below is equivalent to:
// nats.Connect("nats://demo.nats.io:4222")
nc, err := nats.Connect("demo.nats.io")
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection nc = Nats.connect("nats://demo.nats.io:4222");
```

#### Java

```text
// Connection is AutoCloseable
try (Connection nc = Nats.connect("nats://demo.nats.io:4222")) {
    // Do something with the connection
}
```

#### JavaScript

```javascript
const nc = await connect({ servers: "demo.nats.io" });
// Do something with the connection
doSomething();
await nc.close();
```

#### Python

```python
nc = NATS()
await nc.connect(servers=["nats://demo.nats.io:4222"])

# Do something with the connection

await nc.close()
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;

await using var client = new NatsClient("nats://demo.nats.io:4222");

// It's optional to call ConnectAsync()
// as it will be called when needed automatically
await client.ConnectAsync();
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(servers: ["nats://demo.nats.io:4222"]) do |nc|
   # Do something with the connection

   # Close the connection
   nc.close
end
```

#### C

```c
natsConnection      *conn = NULL;
natsStatus          s;

// If connecting to the default port, the URL can be simplified
// to just the hostname/IP.
// That is, the connect below is equivalent to:
// natsConnection_ConnectTo(&conn, "nats://demo.nats.io:4222");
s = natsConnection_ConnectTo(&conn, "demo.nats.io");
if (s != NATS_OK)
  // handle error

// Destroy connection, no-op if conn is NULL.
natsConnection_Destroy(conn);
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **host**: máy chủ vật lý/ảo
- **port**: cổng kết nối