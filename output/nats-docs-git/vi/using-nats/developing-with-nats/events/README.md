---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/events
title: Giám sát Kết nối
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Giám sát Kết nối

> 🇬🇧 *Managing the interaction with the server is primarily the job of the client library but most of the libraries also provide some insight into what is happening under the covers.*

Việc quản lý tương tác với server chủ yếu là nhiệm vụ của client library (thư viện), nhưng hầu hết các library cũng cung cấp thêm thông tin về những gì đang diễn ra bên dưới.

> 🇬🇧 *For example, the client library may provide a mechanism to get the connection's current status:*

Chẳng hạn, client library (bên gọi phía người dùng) có thể cung cấp cơ chế để lấy trạng thái hiện tại của kết nối:

#### Go

```go
nc, err := nats.Connect("demo.nats.io", nats.Name("API Example"))
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

getStatusTxt := func(nc *nats.Conn) string {
    switch nc.Status() {
    case nats.CONNECTED:
        return "Connected"
    case nats.CLOSED:
        return "Closed"
    default:
        return "Other"
    }
}
log.Printf("The connection is %v\n", getStatusTxt(nc))

nc.Close()

log.Printf("The connection is %v\n", getStatusTxt(nc))
```

#### Java

```java
Connection nc = Nats.connect("nats://demo.nats.io:4222");

System.out.println("The Connection is: " + nc.getStatus()); // CONNECTED

nc.close();

System.out.println("The Connection is: " + nc.getStatus()); // CLOSED
```

#### JavaScript

```javascript
  // you can find out where you connected:
t.log(`connected to a nats server version ${nc.info.version}`);

// or information about the data in/out of the client:
const stats = nc.stats();
t.log(`client sent ${stats.outMsgs} messages and received ${stats.inMsgs}`);
```

#### Python

```python
nc = NATS()

await nc.connect(
   servers=["nats://demo.nats.io:4222"],
   )

# Do something with the connection.

print("The connection is connected?", nc.is_connected)

while True:
  if nc.is_reconnecting:
    print("Reconnecting to NATS...")
    break
  await asyncio.sleep(1)

await nc.close()

print("The connection is closed?", nc.is_closed)
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;

await using var client = new NatsClient();

Console.WriteLine($"{client.Connection.ConnectionState}"); // Closed

await client.ConnectAsync();

Console.WriteLine($"{client.Connection.ConnectionState}"); // Open
```

#### Ruby

```ruby
NATS.start(max_reconnect_attempts: 2) do |nc|
  puts "Connect is connected?: #{nc.connected?}"

  timer = EM.add_periodic_timer(1) do
    if nc.closing?
      puts "Connection closed..."
      EM.cancel_timer(timer)
      NATS.stop
    end

    if nc.reconnecting?
      puts "Reconnecting to NATS..."
      next
    end
  end
end
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **library**: thư viện
- **server**: máy chủ