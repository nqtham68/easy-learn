---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/sending/request_reply
title: Ngữ nghĩa Request-Reply
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Ngữ nghĩa Request-Reply

> 🇬🇧 *The pattern of sending a message and receiving a response is encapsulated in most client libraries into a request method. Under the covers this method will publish a message with a unique reply-to subject and wait for the response before returning.*

Hầu hết các client library đều đóng gói pattern gửi message và nhận response vào một method gọi là request. Bên dưới, method này publish một message kèm theo một reply-to subject (chuỗi định danh message) duy nhất, rồi chờ response trước khi trả kết quả về.

> 🇬🇧 *In the older versions of some libraries a completely new reply-to subject is created each time. In newer versions, a subject hierarchy is used so that a single subscriber in the client library listens for a wildcard, and requests are sent with a unique child subject of a single subject.*

Ở các phiên bản cũ, một reply-to subject hoàn toàn mới được tạo ra mỗi lần gọi. Ở các phiên bản mới hơn, cơ chế phân cấp subject được sử dụng: một subscriber (bên đăng ký nhận message) duy nhất trong library lắng nghe wildcard, còn mỗi request được gửi kèm một subject con duy nhất.

> 🇬🇧 *The primary difference between the request method and publishing with a reply-to is that the library is only going to accept one response, and in most libraries the request will be treated as a synchronous action. The library may even provide a way to set the timeout.*

Điểm khác biệt chính giữa request method và publish thông thường kèm reply-to là library chỉ chấp nhận một response duy nhất, và trong hầu hết các library, request được xử lý theo kiểu sync. Một số library còn cho phép thiết lập timeout (thời gian chờ tối đa).

> 🇬🇧 *For example, updating the previous publish example we may request `time` with a one second timeout:*

Ví dụ, cập nhật lại ví dụ publish trước đó, ta có thể request `time` với timeout một giây:

#### Go

```go
nc, err := nats.Connect("demo.nats.io")
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Send the request
msg, err := nc.Request("time", nil, time.Second)
if err != nil {
    log.Fatal(err)
}

// Use the response
log.Printf("Reply: %s", msg.Data)

// Close the connection
nc.Close()
```

#### Java

```java
Connection nc = Nats.connect("nats://demo.nats.io:4222");

// set up a listener for "time" requests
Dispatcher d = nc.createDispatcher(msg -> {
    System.out.println("Received time request");
    nc.publish(msg.getReplyTo(), ("" + System.currentTimeMillis()).getBytes());
});
d.subscribe("time");

// make a request to the "time" subject and wait 1 second for a response
Message msg = nc.request("time", null, Duration.ofSeconds(1));

// look at the response
long time = Long.parseLong(new String(msg.getData()));
System.out.println(new Date(time));

nc.close();
```

#### JavaScript

```javascript
// set up a subscription to process the request
const sc = StringCodec();
nc.subscribe("time", {
  callback: (_err, msg) => {
    msg.respond(sc.encode(new Date().toLocaleTimeString()));
  },
});

const r = await nc.request("time");
t.log(sc.decode(r.data));
```

#### Python

```python
nc = NATS()

async def sub(msg):
  await nc.publish(msg.reply, b'response')

await nc.connect(servers=["nats://demo.nats.io:4222"])
await nc.subscribe("time", cb=sub)

# Send the request
try:
  msg = await nc.request("time", b'', timeout=1)
  # Use the response
  print("Reply:", msg)
except asyncio.TimeoutError:
  print("Timed out waiting for response")
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;

await using var client = new NatsClient();

using CancellationTokenSource cts = new();

// Process the time messages in a separate task
Task subscription = Task.Run(async () =>
{
    await foreach (var msg in client.SubscribeAsync<string>("time", cancellationToken: cts.Token))
    {
        await msg.ReplyAsync(DateTimeOffset.Now);
    }
});

// Wait for the subscription task to be ready
await Task.Delay(1000);

var reply = await client.RequestAsync<DateTimeOffset>("time");

Console.WriteLine($"Reply: {reply.Data:O}");

await cts.CancelAsync();
await subscription;

// Output:
// Reply: 2024-10-23T05:20:55.0000000+01:00
```

#### Ruby

```ruby
require 'nats/client'
require 'fiber'

NATS.start(servers:["nats://127.0.0.1:4222"]) do |nc|
  nc.subscribe("time") do |msg, reply|
    nc.publish(reply, "response")
  end

  Fiber.new do
    # Use the response
    msg = nc.request("time", "")
    puts "Reply: #{msg}"
  end.resume
end
```

#### C

```c
natsConnection      *conn      = NULL;
natsMsg             *msg       = NULL;
natsStatus          s          = NATS_OK;

s = natsConnection_ConnectTo(&conn, NATS_DEFAULT_URL);

// Send a request and wait for up to 1 second
if (s == NATS_OK)
    s = natsConnection_RequestString(&msg, conn, "request", "this is the request", 1000);

if (s == NATS_OK)
{
    printf("Received msg: %s - %.*s\n",
           natsMsg_GetSubject(msg),
           natsMsg_GetDataLength(msg),
           natsMsg_GetData(msg));

    // Destroy the message that was received
    natsMsg_Destroy(msg);
}

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
```

> 🇬🇧 *You can think of request-reply in the library as a subscribe, get one message, unsubscribe pattern. In Go this might look something like:*

Có thể hình dung request-reply trong library theo pattern: subscribe, nhận một message, rồi unsubscribe. Trong Go, cách triển khai này trông như sau:

```go
sub, err := nc.SubscribeSync(replyTo)
if err != nil {
    log.Fatal(err)
}

// Send the request immediately
nc.PublishRequest(subject, replyTo, []byte(input))
nc.Flush()

// Wait for a single response
for {
    msg, err := sub.NextMsg(1 * time.Second)
    if err != nil {
        log.Fatal(err)
    }

    response = string(msg.Data)
    break
}
sub.Unsubscribe()
```

## Scatter-Gather

> 🇬🇧 *You can expand the request-reply pattern into something often called scatter-gather. To receive multiple messages, with a timeout, you could do something like the following, where the loop getting messages is using time as the limitation, not the receipt of a single message:*

Có thể mở rộng pattern request-reply thành dạng thường gọi là scatter-gather. Để nhận nhiều message với một timeout, vòng lặp nhận message dùng thời gian làm giới hạn thay vì chỉ dừng sau một message:

```go
sub, err := nc.SubscribeSync(replyTo)
if err != nil {
    log.Fatal(err)
}
nc.Flush()

// Send the request
nc.PublishRequest(subject, replyTo, []byte(input))

// Wait for a single response
max := 100 * time.Millisecond
start := time.Now()
for time.Now().Sub(start) < max {
    msg, err := sub.NextMsg(1 * time.Second)
    if err != nil {
        break
    }

    responses = append(responses, string(msg.Data))
}
sub.Unsubscribe()
```

> 🇬🇧 *Or, you can loop on a counter and a timeout to try to get _at least N_ responses:*

Hoặc, có thể kết hợp bộ đếm với timeout để cố nhận _ít nhất N_ response:

```go
sub, err := nc.SubscribeSync(replyTo)
if err != nil {
    log.Fatal(err)
}
nc.Flush()

// Send the request
nc.PublishRequest(subject, replyTo, []byte(input))

// Wait for a single response
max := 500 * time.Millisecond
start := time.Now()
for time.Now().Sub(start) < max {
    msg, err := sub.NextMsg(1 * time.Second)
    if err != nil {
        break
    }

    responses = append(responses, string(msg.Data))

    if len(responses) >= minResponses {
        break
    }
}
sub.Unsubscribe()
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **request**: yêu cầu
- **response**: phản hồi
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **timeout**: thời gian chờ tối đa