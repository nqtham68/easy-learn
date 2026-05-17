---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/noecho
title: Tắt Tính Năng Echo Message
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Tắt Tính Năng Echo Message

> 🇬🇧 *By default a NATS connection will echo messages if the connection also has interest in the published subject. This means that if a publisher on a connection sends a message to a subject any subscribers on that same connection will receive the message. Clients can opt to turn off this behavior, such that regardless of interest, the message will not be delivered to subscribers on the same connection.*

Theo mặc định, một NATS connection sẽ echo message nếu connection đó cũng có subscriber (bên đăng ký nhận message) quan tâm đến subject (chuỗi định danh message) được publish. Nghĩa là nếu publisher (bên gửi message) trên một connection gửi message đến một subject, mọi subscriber trên cùng connection đó đều sẽ nhận được message. Client có thể tắt hành vi này, khiến message không được giao đến subscriber nào trên cùng connection — bất kể có interest hay không.

> 🇬🇧 *The NoEcho option can be useful in BUS patterns where all applications subscribe and publish to the same subject. Usually a publish represents a state change that the application already knows about, so in the case where the application publishes an update it does not need to process the update itself.*

Tùy chọn `NoEcho` hữu ích trong mô hình BUS, nơi tất cả ứng dụng đều subscribe và publish lên cùng một subject. Thông thường, một lần publish thể hiện một thay đổi trạng thái mà ứng dụng đã biết rồi — vì vậy khi ứng dụng publish một bản cập nhật, nó không cần tự xử lý bản cập nhật đó.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/noecho.svg)

> 🇬🇧 *Keep in mind that each connection will have to turn off echo, and that it is per connection, not per application. Also, turning echo on and off can result in a major change to your applications communications protocol since messages will flow or stop flowing based on this setting and the subscribing code won't have any indication as to why.*

Lưu ý rằng mỗi connection phải tự tắt echo riêng — đây là cài đặt theo connection, không phải theo ứng dụng. Ngoài ra, việc bật/tắt echo có thể làm thay đổi lớn đến luồng giao tiếp của ứng dụng, vì message sẽ chạy hoặc bị chặn tùy theo cài đặt này, và phần code subscriber sẽ không biết lý do tại sao.

#### Go

```go
// Turn off echo
nc, err := nats.Connect("demo.nats.io", nats.Name("API NoEcho Example"), nats.NoEcho())
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
    .noEcho() // Turn off echo
    .build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
const nc = await connect({
    servers: ["demo.nats.io"],
    noEcho: true,
});

const sub = nc.subscribe(subj, { callback: (_err, _msg) => {} });
nc.publish(subj);
await sub.drain();
// we won't get our own messages
t.is(sub.getProcessed(), 0);
```

#### Python

```python
ncA = NATS()
ncB = NATS()

await ncA.connect(no_echo=True)
await ncB.connect()

async def handler(msg):
   # Messages sent by `ncA' will not be received.
   print("[Received] ", msg)

await ncA.subscribe("greetings", cb=handler)
await ncA.flush()
await ncA.publish("greetings", b'Hello World!')
await ncB.publish("greetings", b'Hello World!')

# Do something with the connection

await asyncio.sleep(1)
await ncA.drain()
await ncB.drain()
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using NATS.Client.Core;

await using var client = new NatsClient(new NatsOpts
{
    Url = "nats://demo.nats.io:4222",
    
    // Turn off echo
    Echo = false
});
```

#### Ruby

```ruby
NATS.start("nats://demo.nats.io:4222", no_echo: true) do |nc|
  # ...
end
```

#### C

```c
natsConnection      *conn    = NULL;
natsOptions         *opts    = NULL;
natsStatus          s        = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_SetNoEcho(opts, true);
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message