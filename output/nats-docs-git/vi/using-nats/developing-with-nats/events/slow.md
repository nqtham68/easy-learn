---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/events/slow
title: Slow Consumer
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Slow Consumer

> 🇬🇧 *NATS is designed to move messages through the server quickly. As a result, NATS depends on the applications to consider and respond to changing message rates. The server will do a bit of impedance matching, but if a client is too slow the server will eventually cut them off by closing the connection. These cut off connections are called [_slow consumers_](../../../running-a-nats-service/nats_admin/slow_consumers.md).*

NATS được thiết kế để truyền message (gói dữ liệu được gửi đi) qua server với tốc độ cao. Do đó, NATS yêu cầu các ứng dụng phải tự xử lý khi tốc độ nhận thay đổi. Server có thể bù đắp một phần, nhưng nếu client quá chậm, server sẽ buộc phải đóng kết nối. Các kết nối bị đóng theo cách này được gọi là [_slow consumers_](../../../running-a-nats-service/nats_admin/slow_consumers.md).

> 🇬🇧 *One way some of the libraries deal with bursty message traffic is to buffer incoming messages for a subscription. So if an application can handle 10 messages per second and sometimes receives 20 messages per second, the library may hold the extra 10 to give the application time to catch up. To the server, the application will appear to be handling the messages and consider the connection healthy. Most client libraries will notify the application that there is a SlowConsumer error and discard messages.*

Một số thư viện xử lý tình trạng message dồn dập bằng cách buffer (vùng đệm tạm) các message đến cho mỗi subscriber (bên đăng ký nhận message). Ví dụ, nếu ứng dụng xử lý được 10 message/giây nhưng đôi khi nhận đến 20 message/giây, thư viện có thể giữ lại 10 message thừa để ứng dụng kịp xử lý. Với server, ứng dụng trông như vẫn đang xử lý bình thường. Hầu hết các client library sẽ thông báo lỗi `SlowConsumer` và bỏ qua message vượt ngưỡng.

> 🇬🇧 *Receiving and dropping messages from the server keeps the connection to the server healthy, but creates an application requirement. There are several common patterns:*
>
> *- Use request-reply to throttle the sender and prevent overloading the subscriber*
> *- Use a queue with multiple subscribers splitting the work*
> *- Persist messages with something like NATS streaming*

Việc nhận và bỏ qua message từ server giúp giữ kết nối ổn định, nhưng ứng dụng cần có chiến lược xử lý phù hợp. Một số pattern phổ biến:

* Dùng request-reply để kiểm soát tốc độ gửi, tránh quá tải subscriber
* Dùng queue với nhiều subscriber chia sẻ tải
* Lưu message bằng NATS streaming

> 🇬🇧 *Libraries that cache incoming messages may provide two controls on the incoming queue, or pending messages. These are useful if the problem is bursty publishers and not a continuous performance mismatch. Disabling these limits can be dangerous in production and although setting these limits to 0 may help find problems, it is also a dangerous proposition in production.*

Các thư viện có cache message đến thường cung cấp hai tham số kiểm soát queue (hàng đợi message) đầu vào — hay còn gọi là pending messages. Các tham số này hữu ích khi vấn đề đến từ publisher (bên gửi message) gửi dồn dập, không phải do chênh lệch hiệu năng liên tục. Tắt các giới hạn này rất nguy hiểm trong môi trường production; dù đặt về 0 có thể giúp phát hiện vấn đề, đây vẫn là cấu hình rủi ro cao.

> 🇬🇧 *Check your libraries documentation for the default settings, and support for disabling these limits.*

> Kiểm tra tài liệu của thư viện đang dùng để biết các giá trị mặc định và cách tắt các giới hạn này.

> 🇬🇧 *The incoming cache is usually per subscriber, but again, check the specific documentation for your client library.*

Cache đầu vào thường được tính riêng cho từng subscriber, nhưng hãy kiểm tra tài liệu của client library cụ thể để xác nhận.

## Giới Hạn Pending Message Theo Số Lượng và Kích Thước

> 🇬🇧 *The first way that the incoming queue can be limited is by message count. The second way to limit the incoming queue is by total size. For example, to limit the incoming cache to 1,000 messages or 5mb whichever comes first:*

Queue đầu vào có thể giới hạn theo số lượng message hoặc theo tổng kích thước. Ví dụ, giới hạn cache ở mức 1.000 message hoặc 5 MB, tùy điều kiện nào đạt trước:

#### Go

```go
nc, err := nats.Connect("demo.nats.io")
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Subscribe
sub1, err := nc.Subscribe("updates", func(m *nats.Msg) {})
if err != nil {
    log.Fatal(err)
}

// Set limits of 1000 messages or 5MB, whichever comes first
sub1.SetPendingLimits(1000, 5*1024*1024)

// Subscribe
sub2, err := nc.Subscribe("updates", func(m *nats.Msg) {})
if err != nil {
    log.Fatal(err)
}

// Set no limits for this subscription
sub2.SetPendingLimits(-1, -1)

// Close the connection
nc.Close()
```

#### Java

```java
// Consumer (Dispatcher, Subscription) API
// void setPendingLimits(long maxMessages, long maxBytes)

Connection nc = Nats.connect("nats://demo.nats.io:4222");

Dispatcher d = nc.createDispatcher((msg) -> {
    // handle message
});

d.subscribe("updates");

d.setPendingLimits(1_000, 5 * 1024 * 1024); // Set limits on a dispatcher

// Subscribe
Subscription sub = nc.subscribe("updates");

sub.setPendingLimits(1_000, 5 * 1024 * 1024); // Set limits on a subscription

// Do something

// Close the connection
nc.close();
```

#### JavaScript

```javascript
// slow pending limits are not configurable on node-nats
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://demo.nats.io:4222"])

future = asyncio.Future()

async def cb(msg):
  nonlocal future
  future.set_result(msg)

# Set limits of 1000 messages or 5MB
await nc.subscribe("updates", cb=cb, pending_bytes_limit=5*1024*1024, pending_msgs_limit=1000)
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using System.Threading.Channels;
using NATS.Client.Core;

await using var client = new NatsClient();

// Set limits of 1000 messages.
// Note: setting the channel capacity over 1024 is not recommended
// as the channel's backing array will be allocated on the LOH (large object heap).
// NATS .NET client does not support setting a limit on the number of bytes
var subOpts = new NatsSubOpts
{
    ChannelOpts = new NatsSubChannelOpts
    {
        Capacity = 1000,
        FullMode = BoundedChannelFullMode.DropOldest
    }
};
await foreach (var msg in client.SubscribeAsync<string>(subject: "updates", opts: subOpts))
{
    Console.WriteLine($"Received: {msg.Subject}: {msg.Data}");    
}
```

#### Ruby

```ruby
# The Ruby NATS client currently does not have option to specify a subscribers pending limits.
```

#### C

```c
natsConnection      *conn      = NULL;
natsSubscription    *sub1      = NULL;
natsSubscription    *sub2      = NULL;
natsStatus          s          = NATS_OK;

s = natsConnection_ConnectTo(&conn, NATS_DEFAULT_URL);

// Subscribe
if (s == NATS_OK)
    s = natsConnection_Subscribe(&sub1, conn, "updates", onMsg, NULL);

// Set limits of 1000 messages or 5MB, whichever comes first
if (s == NATS_OK)
    s = natsSubscription_SetPendingLimits(sub1, 1000, 5*1024*1024);

// Subscribe
if (s == NATS_OK)
    s = natsConnection_Subscribe(&sub2, conn, "updates", onMsg, NULL);

// Set no limits for this subscription
if (s == NATS_OK)
    s = natsSubscription_SetPendingLimits(sub2, -1, -1);

(...)

// Destroy objects that were created
natsSubscription_Destroy(sub1);
natsSubscription_Destroy(sub2);
natsConnection_Destroy(conn);
```

## Phát Hiện Slow Consumer và Kiểm Tra Message Bị Bỏ Qua

> 🇬🇧 *When a slow consumer is detected and messages are about to be dropped, the library may notify the application. This process may be similar to other errors or may involve a custom callback.*

Khi phát hiện slow consumer và sắp có message bị bỏ qua, thư viện có thể thông báo cho ứng dụng. Cơ chế này có thể giống các lỗi thông thường hoặc dùng callback (hàm được gọi lại) riêng.

> 🇬🇧 *Some libraries, like Java, will not send this notification on every dropped message because that could be noisy. Rather the notification may be sent once per time the subscriber gets behind. Libraries may also provide a way to get a count of dropped messages so that applications can at least detect a problem is occurring.*

Một số thư viện, như Java, không thông báo cho từng message bị bỏ — điều đó sẽ tạo ra quá nhiều sự kiện. Thay vào đó, thông báo chỉ được gửi mỗi lần subscriber bị tụt lại phía sau. Nhiều thư viện cũng cung cấp cách đếm số message đã bị bỏ để ứng dụng có thể phát hiện sự cố.

#### Go

```go
// Set the callback that will be invoked when an asynchronous error occurs.
nc, err := nats.Connect("demo.nats.io", nats.ErrorHandler(logSlowConsumer))
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
class SlowConsumerReporter implements ErrorListener {
    public void errorOccurred(Connection conn, String error)
    {
    }

    public void exceptionOccurred(Connection conn, Exception exp) {
    }

    // Detect slow consumers
    public void slowConsumerDetected(Connection conn, Consumer consumer) {
        // Get the dropped count
        System.out.println("A slow consumer dropped messages: "+ consumer.getDroppedCount());
    }
}

public class SlowConsumerListener {
    public static void main(String[] args) {

        try {
            Options options = new Options.Builder().
                                        server("nats://demo.nats.io:4222").
                                        errorListener(new SlowConsumerReporter()). // Set the listener
                                        build();
            Connection nc = Nats.connect(options);

            // Do something with the connection

            nc.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

#### JavaScript

```javascript
// slow consumer detection is not configurable on NATS JavaScript client.
```

#### Python

```python
   nc = NATS()

   async def error_cb(e):
     if type(e) is nats.aio.errors.ErrSlowConsumer:
       print("Slow consumer error, unsubscribing from handling further messages...")
       await nc.unsubscribe(e.sid)

   await nc.connect(
      servers=["nats://demo.nats.io:4222"],
      error_cb=error_cb,
      )

   msgs = []
   future = asyncio.Future()
   async def cb(msg):
       nonlocal msgs
       nonlocal future
       print(msg)
       msgs.append(msg)

       if len(msgs) == 3:
         # Head of line blocking on other messages caused
         # by single message processing taking too long...
         await asyncio.sleep(1)

   await nc.subscribe("updates", cb=cb, pending_msgs_limit=5)

   for i in range(0, 10):
     await nc.publish("updates", "msg #{}".format(i).encode())
     await asyncio.sleep(0)

   try:
     await asyncio.wait_for(future, 1)
   except asyncio.TimeoutError:
     pass

   for msg in msgs:
     print("[Received]", msg)

   await nc.close()
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using System.Threading.Channels;
using NATS.Client.Core;

await using var client = new NatsClient();

// Set the event handler for slow consumers
client.Connection.MessageDropped += async (sender, eventArgs) =>
{
    Console.WriteLine($"Dropped message: {eventArgs.Subject}: {eventArgs.Data}");
    Console.WriteLine($"Current channel size: {eventArgs.Pending}");
};

var subOpts = new NatsSubOpts
{
    ChannelOpts = new NatsSubChannelOpts
    {
        Capacity = 10,
        FullMode = BoundedChannelFullMode.DropOldest

        // If set to wait (default), you won't be able to detect slow consumers
        // FullMode = BoundedChannelFullMode.Wait,
    }
};

using var cts = new CancellationTokenSource();

var subscription = Task.Run(async () =>
{
    await foreach (var msg in client.SubscribeAsync<string>(subject: "updates", opts: subOpts, cancellationToken: cts.Token))
    {
        Console.WriteLine($"Received: {msg.Subject}: {msg.Data}");    
    }
});

for (int i = 0; i < 1_000; i++)
{
    await client.PublishAsync(subject: "updates", data: $"message payload {i}");
}

await cts.CancelAsync();

await subscription;
```

#### Ruby

```ruby
# The Ruby NATS client currently does not have option to customize slow consumer limits per sub.
```

#### C

```c
static void
errorCB(natsConnection *conn, natsSubscription *sub, natsStatus s, void *closure)
{

    // Do something
    printf("Error: %d - %s", s, natsStatus_GetText(s));
}

(...)

natsConnection      *conn      = NULL;
natsOptions         *opts      = NULL;
natsStatus          s          = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_SetErrorHandler(opts, errorCB, NULL);
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **buffer**: vùng đệm tạm
- **callback**: hàm được gọi lại
- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **queue**: hàng đợi message
- **subscriber**: bên đăng ký nhận message