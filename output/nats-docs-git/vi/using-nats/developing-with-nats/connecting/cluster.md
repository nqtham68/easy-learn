---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/cluster
title: Kết nối đến Cluster
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Kết nối đến Cluster

> 🇬🇧 *When connecting to a cluster, there are a few things to think about.*

Khi kết nối đến một cluster (cụm nhiều server chạy chung), có một số điểm cần lưu ý:

* Truyền URL cho từng thành viên trong cluster (tùy chọn một phần)
* Thuật toán kết nối
* Thuật toán reconnect (sẽ được trình bày sau)
* Các URL do server cung cấp thêm

> 🇬🇧 *When a client library first tries to connect it will use the list of URLs provided to the connection options or function. These URLs are usually checked in random order as to not have every client connect to the same server. The first successful connection is used. Randomization can be [explicitly disabled](../reconnect/random.md).*

Khi client library lần đầu kết nối, nó dùng danh sách URL được truyền vào connection options hoặc hàm kết nối. Các URL này thường được kiểm tra theo thứ tự ngẫu nhiên để tránh mọi client đều kết nối vào cùng một server. Kết nối thành công đầu tiên sẽ được sử dụng. Có thể [tắt tính năng ngẫu nhiên hóa này](../reconnect/random.md) một cách tường minh.

> 🇬🇧 *After a client connects to the server, the server may provide a list of URLs for additional known servers. This allows a client to connect to one server and still have other servers available during reconnect.*

Sau khi client kết nối thành công, server có thể trả về danh sách URL của các server khác đã biết. Điều này giúp client có thể kết nối lại qua các server khác khi cần reconnect.

> 🇬🇧 *To ensure the initial connection, your code should include a list of reasonable _front line_ or _seed_ servers. Those servers may know about other members of the cluster, and may tell the client about those members. But you don't have to configure the client to pass every valid member of the cluster in the connect method.*

Để đảm bảo kết nối ban đầu thành công, code nên bao gồm một danh sách các _front line_ hoặc _seed_ server hợp lý. Những server này có thể biết về các thành viên khác trong cluster và thông báo lại cho client. Không cần thiết phải cấu hình client với toàn bộ danh sách thành viên của cluster trong phương thức connect.

> 🇬🇧 *By providing the ability to pass multiple connect options, NATS can handle the possibility of a machine going down or being unavailable to a client. By adding the ability of the server to feed clients a list of known servers as part of the client-server protocol the mesh created by a cluster can grow and change organically while the clients are running.*

Nhờ khả năng truyền nhiều connection option, NATS có thể xử lý tình huống một máy bị down hoặc không khả dụng với client. Khi server có thể cung cấp cho client danh sách các server đã biết như một phần của giao thức client-server, mạng lưới do cluster tạo thành có thể phát triển và thay đổi tự nhiên trong khi các client vẫn đang chạy.

> 🇬🇧 *_Note, failure behavior is library dependent, please check the documentation for your client library on information about what happens if the connect fails._*

_Lưu ý: hành vi khi kết nối thất bại phụ thuộc vào từng library. Hãy kiểm tra tài liệu của client library đang dùng để biết điều gì xảy ra khi connect thất bại._

#### Go

```go
servers := []string{"nats://127.0.0.1:1222", "nats://127.0.0.1:1223", "nats://127.0.0.1:1224"}

nc, err := nats.Connect(strings.Join(servers, ","))
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
    .build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
const nc = await connect({
    servers: [
      "nats://demo.nats.io:4222",
      "nats://localhost:4222",
    ],
});
// Do something with the connection
doSomething();
// When done close it
await nc.close();
```

#### Python

```python
nc = NATS()
await nc.connect(servers=[
   "nats://127.0.0.1:1222",
   "nats://127.0.0.1:1223",
   "nats://127.0.0.1:1224"
   ])

# Do something with the connection

await nc.close()
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;

await using var client = new NatsClient("nats://127.0.0.1:1222,nats://127.0.0.1:1223,nats://127.0.0.1:1224");

// It's optional to call ConnectAsync()
// as it will be called when needed automatically
await client.ConnectAsync();
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(servers: ["nats://127.0.0.1:1222", "nats://127.0.0.1:1223", "nats://127.0.0.1:1224"]) do |nc|
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
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **cluster**: cụm nhiều server chạy chung
- **node**: một server trong cluster
- **reconnect**: thử lại khi fail
- **server**: máy chủ