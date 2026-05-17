---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/receiving/queues
title: Queue Subscriptions (Đăng ký theo nhóm hàng đợi)
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Đăng ký theo Queue Group

> 🇬🇧 *Subscribing to a [queue group](../../../nats-concepts/core-nats/queue-groups/queue.md) is only slightly different than subscribing to a subject alone. The application simply includes a queue name with the subscription. The server will load balance between all members of the queue group. In a cluster setup, every member has the same chance of receiving a particular message.*

Đăng ký vào một [queue group](../../../nats-concepts/core-nats/queue-groups/queue.md) (nhóm subscribers chia sẻ tải) chỉ khác một chút so với việc đăng ký theo subject (chuỗi định danh message) thông thường. Ứng dụng chỉ cần thêm tên queue vào lúc đăng ký. Server sẽ tự động cân bằng tải giữa tất cả các thành viên trong queue group. Trong môi trường cluster, mỗi thành viên đều có cơ hội nhận bất kỳ message nào như nhau.

> 🇬🇧 *Keep in mind that queue groups in NATS are dynamic and do not require any server configuration.*

Lưu ý rằng queue group trong NATS là động và không cần cấu hình gì trên server.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/queues.svg)

> 🇬🇧 *As an example, to subscribe to the queue `workers` with the subject `updates`:*

Ví dụ, để đăng ký vào queue `workers` với subject `updates`:

#### Go

```go
nc, err := nats.Connect("demo.nats.io")
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Use a WaitGroup to wait for 10 messages to arrive
wg := sync.WaitGroup{}
wg.Add(10)

// Create a queue subscription on "updates" with queue name "workers"
if _, err := nc.QueueSubscribe("updates", "workers", func(m *nats.Msg) {
    wg.Done()
}); err != nil {
    log.Fatal(err)
}

// Wait for messages to come in
wg.Wait()
```

#### Java

```java
Connection nc = Nats.connect("nats://demo.nats.io:4222");

// Use a latch to wait for 10 messages to arrive
CountDownLatch latch = new CountDownLatch(10);

// Create a dispatcher and inline message handler
Dispatcher d = nc.createDispatcher((msg) -> {
    String str = new String(msg.getData(), StandardCharsets.UTF_8);
    System.out.println(str);
    latch.countDown();
});

// Subscribe to the "updates" subject with a queue group named "workers"
d.subscribe("updates", "workers");

// Wait for a message to come in
latch.await(); 

// Close the connection
nc.close();
```

#### JavaScript

```javascript
nc.subscribe(subj, {
    queue: "workers",
    callback: (_err, _msg) => {
      t.log("worker1 got message");
    },
});

nc.subscribe(subj, {
    queue: "workers",
    callback: (_err, _msg) => {
      t.log("worker2 got message");
    },
});
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://demo.nats.io:4222"])

future = asyncio.Future()

async def cb(msg):
  nonlocal future
  future.set_result(msg)

await nc.subscribe("updates", queue="workers", cb=cb)
await nc.publish("updates", b'All is Well')

msg = await asyncio.wait_for(future, 1)
print("Msg", msg)
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;

await using var client = new NatsClient();

var count = 0;

// Subscribe to the "updates" subject with a queue group named "workers"
await foreach (var msg in client.SubscribeAsync<string>(subject: "updates", queueGroup: "workers"))
{
    Console.WriteLine($"Received {++count}: {msg.Subject}: {msg.Data}");
    
    // Break after 10 messages
    if (count == 10)
    {
        break;
    }
}

Console.WriteLine("Done");
```

#### Ruby

```ruby
require 'nats/client'
require 'fiber'

NATS.start(servers:["nats://127.0.0.1:4222"]) do |nc|
  Fiber.new do
    f = Fiber.current

    nc.subscribe("updates", queue: "worker") do |msg, reply|
      f.resume Time.now
    end

    nc.publish("updates", "A")

    # Use the response
    msg = Fiber.yield
    puts "Msg: #{msg}"
  end.resume
end
```

#### C

```c
static void
onMsg(natsConnection *conn, natsSubscription *sub, natsMsg *msg, void *closure)
{
    printf("Received msg: %s - %.*s\n",
           natsMsg_GetSubject(msg),
           natsMsg_GetDataLength(msg),
           natsMsg_GetData(msg));

    // Need to destroy the message!
    natsMsg_Destroy(msg);
}


(...)

natsConnection      *conn = NULL;
natsSubscription    *sub  = NULL;
natsStatus          s;

s = natsConnection_ConnectTo(&conn, NATS_DEFAULT_URL);

// Create a queue subscription on "updates" with queue name "workers"
if (s == NATS_OK)
    s = natsConnection_QueueSubscribe(&sub, conn, "updates", "workers", onMsg, NULL);

(...)


// Destroy objects that were created
natsSubscription_Destroy(sub);
natsConnection_Destroy(conn);
```

> 🇬🇧 *If you run this example with the publish examples that send to `updates`, you will see that one of the instances gets a message while the others you run won't. But the instance that receives the message will change.*

Nếu chạy ví dụ này cùng với các publish example gửi đến `updates`, bạn sẽ thấy chỉ một instance nhận được message trong khi các instance còn lại thì không. Tuy nhiên, instance nào được nhận sẽ thay đổi sau mỗi lần.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **message**: gói dữ liệu được gửi đi
- **queue**: hàng đợi message
- **queue group**: nhóm subscribers chia sẻ tải
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message