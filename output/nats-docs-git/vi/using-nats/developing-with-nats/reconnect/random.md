---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/reconnect/random
title: Tránh Hiện Tượng Thundering Herd
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Tránh Hiện Tượng Thundering Herd

> 🇬🇧 *When a server goes down, there is a possible anti-pattern called the _Thundering Herd_ where all of the clients try to reconnect immediately, thus creating a denial of service attack. In order to prevent this, most NATS client libraries randomize the servers they attempt to connect to. This setting has no effect if only a single server is used, but in the case of a cluster, randomization, or shuffling, will ensure that no one server bears the brunt of the client reconnect attempts.*

Khi một server ngừng hoạt động, có một anti-pattern gọi là _Thundering Herd_ — toàn bộ client cùng thử kết nối lại ngay lập tức, vô tình tạo ra một cuộc tấn công từ chối dịch vụ. Để ngăn chặn điều này, hầu hết các thư viện NATS client sẽ xáo trộn ngẫu nhiên danh sách server mà chúng kết nối đến. Cài đặt này không có tác dụng khi chỉ dùng một server duy nhất, nhưng trong trường hợp có cluster (cụm nhiều server chạy chung), việc xáo trộn ngẫu nhiên đảm bảo không có server nào phải gánh toàn bộ các kết nối lại từ client.

> 🇬🇧 *However, if you want to disable the randomization process for connect and reconnect, so that servers are always checked in the same order, you can do that in most libraries with a connection option:*

Tuy nhiên, nếu muốn tắt quá trình xáo trộn ngẫu nhiên khi connect và reconnect — để server luôn được kiểm tra theo thứ tự cố định — bạn có thể thực hiện trong hầu hết các thư viện thông qua một connection option:

#### Go

```go
servers := []string{"nats://127.0.0.1:1222",
    "nats://127.0.0.1:1223",
    "nats://127.0.0.1:1224",
}

nc, err := nats.Connect(strings.Join(servers, ","), nats.DontRandomize())
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
Options options = new Options.Builder()
    .server("nats://127.0.0.1:1222,nats://127.0.0.1:1223,nats://127.0.0.1:1224")
    .noRandomize() // Disable randomizing servers in the bootstrap and later discovered 
    .build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
const nc = await connect({
    noRandomize: false,
    servers: ["127.0.0.1:4443", "demo.nats.io"],
});
```

#### Python

```python
nc = NATS()
await nc.connect(
   servers=[
      "nats://demo.nats.io:1222",
      "nats://demo.nats.io:1223",
      "nats://demo.nats.io:1224"
      ],
   dont_randomize=True,
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
    NoRandomize = true,
});
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(servers: ["nats://127.0.0.1:1222", "nats://127.0.0.1:1223", "nats://127.0.0.1:1224"], dont_randomize_servers: true) do |nc|
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
const char          *servers[] = {"nats://127.0.0.1:1222", "nats://127.0.0.1:1223", "nats://127.0.0.1:1224"};

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_SetServers(opts, servers, 3);
if (s == NATS_OK)
    s = natsOptions_SetNoRandomize(opts, true);
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **client**: bên gọi (phía người dùng)
- **server**: máy chủ