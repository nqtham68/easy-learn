---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/jetstream/concepts
title: Các khái niệm trong JetStream
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Các khái niệm trong JetStream

## Các tính năng mà JetStream cung cấp

> 🇬🇧 *JetSteam is NATS' built-in distributed persistence sub-system. It enables new functionalities and higher qualities of service on top of the base 'Core NATS' functionality.*

JetStream là hệ thống lưu trữ phân tán tích hợp sẵn trong NATS. Nó bổ sung các tính năng mới và nâng cao chất lượng dịch vụ so với nền tảng 'Core NATS'.

### Tách biệt theo thời gian (Temporal de-coupling)

> 🇬🇧 *In modern systems applications can expose services or produce and consume data streams using publish-subscribe messaging systems such as NATS.*

Trong các hệ thống hiện đại, ứng dụng có thể cung cấp service hoặc tạo và tiêu thụ các luồng dữ liệu thông qua hệ thống messaging publish-subscribe như NATS.

> 🇬🇧 *A basic aspect of basic publish-subscribe messaging is temporal coupling: the subscribers need to be up and running to receive the message when it is published. At a high level, if observability is required, applications need to consume messages in the future, need to come consume at their own pace, or need all messages, then JetStream's streaming functionalities provide the temporal de-coupling between publishers and consumers.*

Một đặc điểm cơ bản của publish-subscribe là sự ràng buộc theo thời gian: subscriber (bên đăng ký nhận message) phải đang chạy mới nhận được message khi nó được publish. Nếu ứng dụng cần tiêu thụ message sau này, tiêu thụ theo tốc độ riêng, hoặc cần toàn bộ message, thì tính năng streaming của JetStream sẽ tạo ra sự tách biệt theo thời gian giữa publisher (bên gửi message) và consumer (bên xử lý dữ liệu từ stream).

### Queuing và replay

> 🇬🇧 *JetStream enables the ability to queue messages for future consumption and replay of messages. Streams can be configured to either queue messages for future consumption by consumers using the `WorkingQueue` retention policy, meaning that the messages are deleted from the stream as they are consumed, or consumers can be configured using the `Limits` retention policy to provide on demand individual or distributed replay messages from the beginning of the stream or from a specific point in time.*

JetStream cho phép đưa message vào queue để tiêu thụ sau và replay lại. Stream (luồng message lưu trữ liên tục) có thể được cấu hình để queue message theo chính sách retention `WorkingQueue` — nghĩa là message bị xóa khỏi stream sau khi được tiêu thụ — hoặc cấu hình consumer theo chính sách retention `Limits` để replay theo yêu cầu, từ đầu stream hoặc từ một thời điểm cụ thể.

### Mirroring và Sourcing

> 🇬🇧 *JetStream enables the ability to mirror messages from one stream to another, and to source messages from one stream to another. This enables the ability to build complex topologies of streams and consumers.*

JetStream hỗ trợ mirror message từ stream này sang stream khác, và source message từ stream này vào stream khác. Điều này cho phép xây dựng các topology phức tạp giữa các stream và consumer.

> 🇬🇧 *For example, you can have an initial stream that captures messages only for a limited amount of time and is used for replay of messages that can also feed any number of other streams configured for message consumption in a queue that mirror or source from this initial stream. This enables the ability to have consumers consuming from the mirrored/sourced stream without impacting that original stream and at their own pace.*

Ví dụ: có thể dùng một stream ban đầu để lưu message trong thời gian giới hạn và replay lại, đồng thời cho phép stream đó cấp dữ liệu cho bất kỳ số lượng stream nào khác được cấu hình để tiêu thụ theo queue — thông qua mirror hoặc source từ stream ban đầu. Nhờ đó, các consumer có thể tiêu thụ từ stream mirror/sourced mà không ảnh hưởng đến stream gốc và theo tốc độ riêng của mình.

### Chất lượng dịch vụ cao hơn

> 🇬🇧 *Besides temporal decoupling of the publishers and subscribers (i.e. 'streaming'), there are other functionalities and qualities of service that JetStream enables.*

Ngoài việc tách biệt theo thời gian giữa publisher và subscriber (tức là 'streaming'), JetStream còn cung cấp nhiều tính năng và chất lượng dịch vụ khác.

#### Guaranteed messaging

> 🇬🇧 *The 'core NATS' basic quality of service is what is called *'at most once'* delivery of messages. It means that while relying on reliable network transport protocol (i.e. TCP) for communications between servers and clients (and between the servers themselves in clusters) to recover from 'casual' network failures (i.e. packet drops), it is not a 'guaranteed' quality of service: there are some failure scenarios that can cause client applications to experience 'message loss', specifically:*

Chất lượng dịch vụ cơ bản của 'Core NATS' là *'at most once'* — tức là mỗi message được giao tối đa một lần. Mặc dù dựa vào TCP để chịu lỗi mạng thông thường (như packet drop), đây không phải là dịch vụ "đảm bảo": một số tình huống lỗi có thể khiến ứng dụng client bị mất message:

* **Disconnections:** Nếu ứng dụng client bị mất kết nối đủ lâu để TCP connection bị reset, nó có thể mất các message đã được buffer hoặc publish trong thời gian đó.
* **Slow consumers:** Hạ tầng NATS server được thiết kế để tự bảo vệ trước các "bad client". Nếu một client đăng ký nhận message không xử lý kịp tốc độ publish (tức là "slow consumer"), nats-server sẽ cố buffer message nhưng bộ nhớ có giới hạn. Khi buffer đầy, nats-server sẽ reset kết nối với client đó và xóa buffer.

> 🇬🇧 *While the nats-server does log a 'slow consumer' message when dropping a client connection to protect itself, from the client application's point of view it simply looks like the application experienced temporary server disconnection, and some messages may never be received.*

Mặc dù nats-server ghi log 'slow consumer' khi ngắt kết nối, từ phía ứng dụng client thì chỉ trông như bị ngắt kết nối tạm thời — và một số message có thể không bao giờ đến được.

> 🇬🇧 *JetStream offers a "guaranteed" quality of service through the use of various acknowledgements (for both the publishers and subscribers) that offer two qualities of service beyond the base 'at most once' quality of service of Core NATS:*

JetStream cung cấp chất lượng dịch vụ "guaranteed" thông qua các cơ chế acknowledgement (cho cả publisher lẫn subscriber), vượt ra ngoài mức 'at most once' của Core NATS:

* *"at least once"*: sử dụng Publish call có acknowledgement và consumer có acknowledgement để đảm bảo không mất message, kể cả khi ứng dụng tạm dừng hoặc xử lý chậm. Gọi là 'at least once' vì trong một số trường hợp lỗi hiếm gặp, message có thể được nhận nhiều hơn một lần — không thành vấn đề nếu xử lý là idempotent.
* *"exactly once"*: bổ sung thêm khả năng de-duplicate message ở phía publisher và tránh consumer nhận trùng message khi phục hồi sau lỗi, thông qua cơ chế 'double acknowledgement'.

> 🇬🇧 *Both of those qualities of service mean that client applications will automatically recover from getting disconnected from the nats-server without any message loss (if durable consumers are used, the client applications can even stop and restart later). For 'slow consumers' using a stream means that the 'buffering' of the messages for that slow consumer happen in a stream (which can be much larger than a server buffer) rather than a server buffer.*

Cả hai mức chất lượng này đều giúp ứng dụng tự động phục hồi khi mất kết nối mà không mất message (nếu dùng durable consumer, ứng dụng còn có thể dừng và khởi động lại sau). Với slow consumer, việc buffer xảy ra trong stream — có thể lớn hơn nhiều so với server buffer — thay vì trong bộ nhớ server.

### Flow control

> 🇬🇧 *The most obvious way to avoid 'slow consumers' would be to implement some form of flow-control. While there is an inherent form of flow-control provided by TCP for communications over a network, it doesn't directly apply to publish/subscribe messaging systems because unlike TCP which is purely point-to-point (i.e. '1 to 1'), publish-subscribe allows for '1 to N' (and 'N to M') communications.*

Cách trực quan nhất để tránh slow consumer là triển khai một dạng flow-control. TCP có flow-control sẵn, nhưng nó không áp dụng trực tiếp cho publish-subscribe vì TCP là point-to-point (1 đến 1), còn publish-subscribe cho phép giao tiếp 1 đến N (và N đến M).

> 🇬🇧 *If you were to implement a form of flow control for basic 'Core NATS' publish-subscribe you would have to implement an 'end-to-end' form of flow control (meaning between the publisher and all of its current subscribers) and it would mean that you would end up flow controlling you publisher(s) to the _lowest common denominator_ of all the current subscribers. Meaning that the publisher(s) would be slowed down to not publish faster than the _slowest_ of all its subscribers.*

Nếu triển khai flow-control end-to-end cho Core NATS, tốc độ publish sẽ bị giới hạn bởi subscriber chậm nhất trong số tất cả subscriber hiện tại — tức là bị hạn chế theo _mẫu số chung thấp nhất_.

> 🇬🇧 *Because of this 'lowest common denominator' aspect of end-to-end flow control in 1-to-N or N-to-M communications and because one of the most important use-case for publish-subscribe messaging systems is the distribution of *real-time* data, 'Core NATS' does _not_ implement any kind of end-to-end flow control.*

Vì lý do đó, và vì một trong các use case quan trọng nhất của publish-subscribe là phân phối dữ liệu *thời gian thực*, 'Core NATS' không triển khai bất kỳ dạng flow-control end-to-end nào.

> 🇬🇧 *While you can certainly implement your own form of end-to-end flow-control with 'Core NATS' by leveraging the request-reply interaction, it is instead much easier (and better) to use JetStream and leverage the *de-coupled* flow control functionality that it offers.*

Dù có thể tự triển khai flow-control end-to-end với Core NATS qua request-reply, sẽ đơn giản hơn và tốt hơn khi dùng JetStream và tận dụng tính năng flow-control *de-coupled* mà nó cung cấp.

> 🇬🇧 *Flow-control over JetStream is *de-coupled* because it is not 'end-to-end' but rather independently between the client application publishing with JetStream and stream (i.e. the JetStream enabled nats-server(s)) and between the stream and the client applications using JetStream consumers.*

Flow-control trong JetStream là *de-coupled* vì nó không phải end-to-end mà hoạt động độc lập: giữa ứng dụng publish và stream (tức là nats-server có JetStream), và giữa stream và các ứng dụng dùng JetStream consumer.

## Storage

> 🇬🇧 *In JetStream the configuration for storing messages is defined separately from how they are consumed. Storage is defined in a _Stream_ and consuming messages is defined by multiple _Consumers_.*

Trong JetStream, cấu hình lưu trữ message được định nghĩa tách biệt với cách tiêu thụ chúng. Lưu trữ được định nghĩa trong một _Stream_, còn việc tiêu thụ message được định nghĩa bởi nhiều _Consumer_.

## Thuật ngữ trong bài

- **broker**: trung gian truyền message
- **buffer**: vùng đệm tạm
- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **queue**: hàng đợi message
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subscriber**: bên đăng ký nhận message
- **timeout**: thời gian chờ tối đa
- **topic**: chủ đề phân loại message