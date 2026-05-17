---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/slow_consumers
title: Slow Consumers (Consumer xử lý chậm)
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Consumer Xử Lý Chậm

> 🇬🇧 *To support resiliency and high availability, NATS provides built-in mechanisms to automatically prune the registered listener interest graph that is used to keep track of subscribers, including slow consumers and lazy listeners. NATS automatically handles a slow consumer. If a client is not processing messages quick enough, the NATS server cuts it off. To support scaling, NATS provides for auto-pruning of client connections. If a subscriber does not respond to ping requests from the server within the [ping-pong interval](../../reference/nats-protocol/nats-protocol#PINGPONG), the client is cut off (disconnected). The client will need to have reconnect logic to reconnect with the server.*

Để hỗ trợ tính bền vững và khả năng sẵn sàng cao, NATS tích hợp sẵn cơ chế tự động dọn dẹp đồ thị interest graph của các listener đã đăng ký — dùng để theo dõi subscriber (bên đăng ký nhận message), bao gồm cả slow consumer và lazy listener. NATS tự động xử lý slow consumer: nếu client không xử lý message đủ nhanh, NATS server sẽ ngắt kết nối. Để hỗ trợ mở rộng quy mô, NATS cũng tự động dọn dẹp các client connection không hoạt động. Nếu subscriber không phản hồi ping request trong [khoảng thời gian ping-pong](../../reference/nats-protocol/nats-protocol#PINGPONG), client sẽ bị ngắt kết nối và cần có logic tự kết nối lại.

> 🇬🇧 *In core NATS, consumers that cannot keep up are handled differently from many other messaging systems: NATS favors the approach of protecting the system as a whole over accommodating a particular consumer to ensure message delivery.*

Trong core NATS, consumer (bên xử lý dữ liệu từ stream) xử lý chậm được xử lý khác với nhiều hệ thống messaging khác: NATS ưu tiên bảo vệ toàn bộ hệ thống hơn là chiều theo một consumer cụ thể để đảm bảo giao nhận message.

**Slow consumer là gì?**

> 🇬🇧 *A slow consumer is a subscriber that cannot keep up with the message flow delivered from the NATS server. This is a common case in distributed systems because it is often easier to generate data than it is to process it. When consumers cannot process data fast enough, back pressure is applied to the rest of the system. NATS has mechanisms to reduce this back pressure.*

Slow consumer là subscriber không theo kịp luồng message từ NATS server. Đây là tình huống phổ biến trong hệ thống phân tán vì tốc độ tạo dữ liệu thường dễ đạt hơn tốc độ xử lý. Khi consumer không xử lý kịp, back pressure sẽ lan ra toàn hệ thống. NATS có các cơ chế để giảm back pressure này.

> 🇬🇧 *NATS identifies slow consumers in the client or the server, providing notification through registered callbacks, log messages, and statistics in the server's monitoring endpoints.*

NATS phát hiện slow consumer ở cả phía client lẫn server, thông báo qua callback đã đăng ký, log message, và số liệu thống kê tại các monitoring endpoint (địa chỉ API cụ thể) của server.

**Điều gì xảy ra với slow consumer?**

> 🇬🇧 *When detected at the client, the application is notified and messages are dropped to allow the consumer to continue and reduce potential back pressure. When detected in the server, the server will disconnect the connection with the slow consumer to protect itself and the integrity of the messaging system.*

Khi phát hiện ở phía client, ứng dụng được thông báo và các message bị bỏ qua để consumer có thể tiếp tục và giảm back pressure. Khi phát hiện ở phía server, server sẽ ngắt kết nối với slow consumer để bảo vệ bản thân và tính toàn vẹn của hệ thống messaging.

## Slow Consumer Được Phát Hiện Ở Phía Client

> 🇬🇧 *A [client can detect it is a slow consumer](../../using-nats/developing-with-nats/events/slow.md#detect-a-slow-consumer-and-check-for-dropped-messages) on a local connection and notify the application through use of the asynchronous error callback. It is better to catch a slow consumer locally in the client rather than to allow the server to detect this condition. This example demonstrates how to define and register an asynchronous error handler that will handle slow consumer errors.*

[Client có thể tự phát hiện mình là slow consumer](../../using-nats/developing-with-nats/events/slow.md#detect-a-slow-consumer-and-check-for-dropped-messages) trên local connection và thông báo cho ứng dụng qua async error callback. Tốt hơn là bắt slow consumer sớm ở phía client thay vì để server phát hiện. Ví dụ dưới đây minh họa cách định nghĩa và đăng ký async error handler để xử lý lỗi slow consumer.

```go
func natsErrHandler(nc *nats.Conn, sub *nats.Subscription, natsErr error) {
    fmt.Printf("error: %v\n", natsErr)
    if natsErr == nats.ErrSlowConsumer {
        pendingMsgs, _, err := sub.Pending()
        if err != nil {
            fmt.Printf("couldn't get pending messages: %v", err)
            return
        }
        fmt.Printf("Falling behind with %d pending messages on subject %q.\n",
            pendingMsgs, sub.Subject)
        // Log error, notify operations...
    }
    // check for other errors
}

// Set the error handler when creating a connection.
nc, err := nats.Connect("nats://localhost:4222",
  nats.ErrorHandler(natsErrHandler))
```

> 🇬🇧 *With this example code and default settings, a slow consumer error would generate output something like this:*

Với code ví dụ trên và cấu hình mặc định, lỗi slow consumer sẽ tạo ra output tương tự như sau:

```
error: nats: slow consumer, messages dropped
Falling behind with 65536 pending messages on subject "foo".
```

> 🇬🇧 *Note that if you are using a synchronous subscriber, `Subscription.NextMsg(timeout time.Duration)` will also return an error indicating there was a slow consumer and messages have been dropped.*

Lưu ý: nếu bạn dùng synchronous subscriber, `Subscription.NextMsg(timeout time.Duration)` cũng sẽ trả về lỗi cho biết đã xảy ra slow consumer và một số message bị bỏ qua.

## Slow Consumer Được Phát Hiện Bởi Server

> 🇬🇧 *When a client does not process messages fast enough, the server will buffer messages in the outbound connection to the client. When this happens and the server cannot write data fast enough to the client, in order to protect itself, it will designate a subscriber as a "slow consumer" and may drop the associated connection.*

Khi client không xử lý message đủ nhanh, server sẽ buffer message trong outbound connection tới client. Nếu server không thể ghi dữ liệu đủ nhanh, để tự bảo vệ, server sẽ đánh dấu subscriber đó là "slow consumer" và có thể ngắt kết nối.

> 🇬🇧 *When the server initiates a slow consumer error, you'll see the following in the server output:*

Khi server khởi tạo lỗi slow consumer, bạn sẽ thấy output sau trong log của server:

```
[54083] 2017/09/28 14:45:18.001357 [INF] ::1:63283 - cid:7 - Slow Consumer Detected
```

> 🇬🇧 *The server will also keep count of the number of slow consumer errors encountered, available through the monitoring `varz` endpoint in the `slow_consumers` field.*

Server cũng ghi nhận số lần gặp lỗi slow consumer, có thể xem qua monitoring endpoint `varz` trong trường `slow_consumers`.

## Xử Lý Slow Consumer

> 🇬🇧 *Apart from using [JetStream](../../nats-concepts/jetstream) or optimizing your consuming application, there are a few options available: scale, meter, or tune NATS to your environment.*

Ngoài việc dùng [JetStream](../../nats-concepts/jetstream) hoặc tối ưu ứng dụng consumer, có thêm vài hướng xử lý: mở rộng quy mô, điều tiết publisher, hoặc tinh chỉnh config NATS.

**Mở rộng với queue subscriber**

> 🇬🇧 *This is ideal if you do not rely on message order. Ensure your NATS subscription belongs to a [queue group](../../nats-concepts/core-nats/queue-groups/queue.md), then scale as required by creating more instances of your service or application. This is a great approach for microservices - each instance of your microservice will receive a portion of the messages to process, and simply add more instances of your service to scale. No code changes, configuration changes, or downtime whatsoever.*

Hướng này phù hợp khi không cần đảm bảo thứ tự message. Đảm bảo subscription NATS thuộc một [queue group](../../nats-concepts/core-nats/queue-groups/queue.md), rồi tăng số lượng instance service khi cần. Đây là cách tiếp cận lý tưởng cho microservice — mỗi instance nhận một phần message để xử lý, chỉ cần thêm instance là đã mở rộng được. Không cần thay đổi code, config, hay dừng hệ thống.

**Tạo subject namespace có khả năng mở rộng**

> 🇬🇧 *You can distribute work further through the subject namespace, with some forethought in design. This approach is useful if you need to preserve message order. The general idea is to publish to a deep subject namespace, and consume with wildcard subscriptions while giving yourself room to expand and distribute work in the future.*

Bạn có thể phân tán công việc thêm thông qua subject (chuỗi định danh message) namespace nếu thiết kế có sự cân nhắc trước. Hướng này hữu ích khi cần giữ nguyên thứ tự message. Ý tưởng chính là publish vào subject namespace sâu và subscribe bằng wildcard, để lại dư địa mở rộng và phân tán tải về sau.

> 🇬🇧 *For a simple example, if you have a service that receives telemetry data from IoT devices located throughout a city, you can publish to a subject namespace like `Sensors.North`, `Sensors.South`, `Sensors.East` and `Sensors.West`. Initially, you'll subscribe to `Sensors.>` to process everything in one consumer. As your enterprise grows and data rates exceed what one consumer can handle, you can replace your single consumer with four consuming applications to subscribe to each subject representing a smaller segment of your data. Note that your publishing applications remain untouched.*

Ví dụ đơn giản: nếu bạn có service nhận dữ liệu telemetry từ thiết bị IoT khắp thành phố, có thể publish vào subject namespace như `Sensors.North`, `Sensors.South`, `Sensors.East` và `Sensors.West`. Ban đầu, subscribe vào `Sensors.>` để xử lý tất cả trong một consumer. Khi hệ thống phát triển và tốc độ dữ liệu vượt quá khả năng một consumer, thay thế bằng bốn ứng dụng consumer, mỗi ứng dụng subscribe vào một subject tương ứng với một phân đoạn dữ liệu nhỏ hơn. Lưu ý: các ứng dụng publish không cần thay đổi.

**Điều tiết publisher**

> 🇬🇧 *A less favorable option may be to meter the publisher. There are several ways to do this varying from simply slowing down your publisher to a more complex approach periodically issuing a blocking request-reply to match subscriber rates.*

Một hướng kém lý tưởng hơn là điều tiết publisher. Có nhiều cách thực hiện: từ đơn giản là làm chậm publisher, đến phức tạp hơn là định kỳ gửi blocking request-reply để khớp với tốc độ subscriber.

**Tinh chỉnh NATS qua config**

> 🇬🇧 *The NATS server can be tuned to determine how much data can be buffered before a consumer is considered slow, and some officially supported clients allow buffer sizes to be adjusted. Decreasing buffer sizes will let you identify slow consumers more quickly. Increasing buffer sizes is not typically recommended unless you are handling temporary bursts of data. Often, increasing buffer capacity will only _postpone_ slow consumer problems.*

NATS server có thể tinh chỉnh để xác định lượng dữ liệu tối đa được buffer trước khi một consumer bị coi là chậm. Một số client được hỗ trợ chính thức cũng cho phép điều chỉnh kích thước buffer. Giảm buffer size giúp phát hiện slow consumer nhanh hơn. Tăng buffer size thường không được khuyến nghị trừ khi bạn đang xử lý burst dữ liệu tạm thời — thường thì tăng buffer chỉ _trì hoãn_ vấn đề slow consumer mà thôi.

### Cấu Hình Server

> 🇬🇧 *The NATS server has a write deadline it uses to write to a connection. When this write deadline is exceeded, a client is considered to have a slow consumer. If you are encountering slow consumer errors in the server, you can increase the write deadline to buffer more data.*

NATS server có write deadline để ghi vào connection. Khi vượt quá deadline này, client được coi là slow consumer. Nếu bạn gặp lỗi slow consumer ở phía server, hãy tăng write deadline để buffer thêm dữ liệu.

> 🇬🇧 *The `write_deadline` configuration option in the NATS server configuration file will tune this:*

Tùy chọn config `write_deadline` trong file config của NATS server dùng để điều chỉnh thông số này:

```
write_deadline: 2s
```

> 🇬🇧 *Tuning this parameter is ideal when you have bursts of data to accommodate. _**Be sure you are not just postponing a slow consumer error.**_*

Tinh chỉnh tham số này phù hợp khi bạn cần xử lý các burst dữ liệu đột biến. _**Hãy chắc chắn rằng bạn không chỉ đang trì hoãn lỗi slow consumer.**_

### Cấu Hình Client

> 🇬🇧 *Most officially supported clients have an internal buffer of pending messages and will notify your application through an asynchronous error callback if a local subscription is not catching up. Receiving an error locally does not necessarily mean that the server will have identified a subscription as a slow consumer.*

Hầu hết client được hỗ trợ chính thức đều có buffer nội bộ chứa các message đang chờ và sẽ thông báo cho ứng dụng qua async error callback nếu subscription tại local không theo kịp. Nhận lỗi ở phía local không nhất thiết có nghĩa là server đã đánh dấu subscription đó là slow consumer.

> 🇬🇧 *This buffer can be configured through setting the pending limits after a subscription has been created:*

Buffer này có thể được cấu hình bằng cách đặt pending limit sau khi subscription được tạo:

```go
if err := sub.SetPendingLimits(1024*500, 1024*5000); err != nil {
  log.Fatalf("Unable to set pending limits: %v", err)
}
```

> 🇬🇧 *The default subscriber pending message limit is `65536`, and the default subscriber pending byte limit is `65536*1024`*

Giới hạn pending message mặc định của subscriber là `65536`, và giới hạn pending byte mặc định là `65536*1024`.

> 🇬🇧 *If the client reaches this internal limit, it will drop messages and continue to process new messages. This is aligned with NATS at most once delivery. It is up to your application to detect the missing messages and recover from this condition.*

Khi client đạt giới hạn nội bộ này, nó sẽ bỏ qua các message cũ và tiếp tục xử lý message mới — phù hợp với ngữ nghĩa "at most once delivery" của NATS. Ứng dụng của bạn cần tự phát hiện các message bị thiếu và xử lý phục hồi.

## Thuật ngữ trong bài

- **callback**: hàm được gọi lại
- **client**: bên gọi (phía người dùng)
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **endpoint**: địa chỉ API cụ thể
- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **queue group**: nhóm subscribers chia sẻ tải
- **server**: máy chủ
- **service**: dịch vụ
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message