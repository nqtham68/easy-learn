---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/receiving/sync
title: Subscription Đồng Bộ
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Subscription Đồng Bộ

> 🇬🇧 *Synchronous subscriptions require the application to wait for messages. This type of subscription is easy to set-up and use, but requires the application to deal with looping if multiple messages are expected. For situations where a single message is expected, synchronous subscriptions are sometimes easier to manage, depending on the language.*

Subscription (bên đăng ký nhận message) đồng bộ yêu cầu ứng dụng chờ message (gói dữ liệu được gửi đi) đến. Kiểu subscription này dễ thiết lập và sử dụng, nhưng ứng dụng cần tự xử lý vòng lặp khi cần nhận nhiều message. Với trường hợp chỉ chờ một message duy nhất, subscription đồng bộ đôi khi dễ quản lý hơn, tùy ngôn ngữ lập trình.

> 🇬🇧 *For example, to subscribe to the subject `updates` and receive a single message you could do:*

Ví dụ, để subscribe vào subject (chuỗi định danh message) `updates` và nhận một message duy nhất:

#### Go

```go
nc, err := nats.Connect("demo.nats.io")
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Subscribe
sub, err := nc.SubscribeSync("updates")
if err != nil {
    log.Fatal(err)
}

// Wait for a message
msg, err := sub.NextMsg(10 * time.Second)
if err != nil {
    log.Fatal(err)
}

// Use the response
log.Printf("Reply: %s", msg.Data)
```

#### Java

```java
Connection nc = Nats.connect("nats://demo.nats.io:4222");

// Subscribe
Subscription sub = nc.subscribe("updates");

// Read a message
Message msg = sub.nextMessage(Duration.ZERO);

String str = new String(msg.getData(), StandardCharsets.UTF_8);
System.out.println(str);

// Close the connection
nc.close();
```

#### JavaScript

```javascript
// node-nats subscriptions are always async.
```

#### Python

```python
# Asyncio NATS client currently does not have a sync subscribe API
```

#### C#

```csharp
// NATS .NET subscriptions are always async.
```

#### Ruby

```ruby
# The Ruby NATS client subscriptions are all async.
```

#### C

```c
natsConnection      *conn      = NULL;
natsSubscription    *sub       = NULL;
natsMsg             *msg       = NULL;
natsStatus          s          = NATS_OK;

s = natsConnection_ConnectTo(&conn, NATS_DEFAULT_URL);

// Subscribe
if (s == NATS_OK)
    s = natsConnection_SubscribeSync(&sub, conn, "updates");

// Wait for messages
if (s == NATS_OK)
    s = natsSubscription_NextMsg(&msg, sub, 10000);

if (s == NATS_OK)
{
    printf("Received msg: %s - %.*s\n",
            natsMsg_GetSubject(msg),
            natsMsg_GetDataLength(msg),
            natsMsg_GetData(msg));

    // Destroy message that was received
    natsMsg_Destroy(msg);
}

(...)

// Destroy objects that were created
natsSubscription_Destroy(sub);
natsConnection_Destroy(conn);
```

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message