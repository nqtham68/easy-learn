---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/jetstream/develop_jetstream
title: Phát triển ứng dụng với JetStream
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Phát triển ứng dụng với JetStream

## Quyết định dùng streaming và chất lượng dịch vụ cao hơn

> 🇬🇧 *In modern systems, applications can expose services or produce and consume data streams. A basic aspect of publish-subscribe messaging is temporal coupling: the subscribers need to be up and running to receive the message when it is published. At a high level, if observability is required, applications need to consume messages in the future, need to consume at their own pace, or need all messages, then JetStream's streaming functionalities provide the temporal de-coupling between publishers and consumers.*

Trong các hệ thống hiện đại, ứng dụng có thể expose service hoặc tạo và tiêu thụ data stream (luồng message lưu trữ liên tục). Một đặc điểm cơ bản của mô hình publish-subscribe là coupling theo thời gian: subscriber (bên đăng ký nhận message) phải đang chạy thì mới nhận được message lúc publisher gửi đi. Ở mức độ cao hơn, nếu cần khả năng quan sát, ứng dụng cần tiêu thụ message trong tương lai, cần tiêu thụ theo tốc độ riêng, hoặc cần nhận tất cả message — thì chức năng streaming của JetStream sẽ tách biệt thời gian giữa publisher (bên gửi message) và consumer.

> 🇬🇧 *Using streaming and its associated higher qualities of service is the facet of messaging with the highest cost in terms of compute and storage.*

Dùng streaming cùng các chất lượng dịch vụ cao hơn là khía cạnh tốn kém nhất về tài nguyên tính toán và lưu trữ trong messaging.

### Khi nào nên dùng streaming

> 🇬🇧 *Streaming is ideal when:*

Streaming phù hợp trong các trường hợp:

* Data producer và consumer (bên xử lý dữ liệu từ stream) tách biệt cao. Chúng có thể online vào các thời điểm khác nhau và consumer phải nhận được message.

* Cần lưu trữ lịch sử dữ liệu trong stream — tức là consumer cần replay lại dữ liệu.

* Message cuối cùng trong stream cần được dùng để khởi tạo trạng thái, trong khi producer có thể đang offline.

* Không biết trước consumer là ai nhưng consumer vẫn phải nhận được message. (Đây thường là giả định sai.)

* Dữ liệu trong message có vòng đời dài hơn vòng đời của ứng dụng.

* Ứng dụng cần tiêu thụ dữ liệu theo tốc độ riêng.

* Muốn flow control tách biệt giữa publisher và consumer của stream.

* Cần chất lượng dịch vụ 'exactly once' với de-duplication khi publish và double-acknowledged consumption.

> 🇬🇧 *Note that no assumptions should ever be made of who will receive and process data in the future, or for what purpose.*

Lưu ý: không bao giờ nên giả định ai sẽ nhận và xử lý dữ liệu trong tương lai, hoặc dùng vào mục đích gì.

### Khi nào nên dùng Core NATS

> 🇬🇧 *Using core NATS is ideal as the fast request path for scalable services where there is tolerance for message loss or when applications themselves handle message delivery guarantees.*

Core NATS phù hợp làm request path nhanh cho các service có khả năng mở rộng, nơi có thể chấp nhận mất message, hoặc khi chính ứng dụng tự xử lý đảm bảo giao nhận message.

> 🇬🇧 *These include:*

Các trường hợp cụ thể:

* Pattern service với request-reply tightly coupled:
    * Ứng dụng gửi request và tự xử lý lỗi khi timeout

      \(gửi lại, báo lỗi, v.v.\). __Phụ thuộc vào messaging system để gửi lại ở đây là anti-pattern.__
* Khi chỉ cần message mới nhất và message mới đến thường xuyên đủ để ứng dụng chấp nhận mất message — ví dụ: stock ticker, trao đổi thường xuyên trong service control plane, hoặc telemetry từ thiết bị.

* Message TTL thấp, tức là giá trị dữ liệu giảm hoặc hết hạn nhanh.

* Biết trước danh sách consumer và consumer dự kiến đang online. Pattern request-reply hoạt động tốt trong trường hợp này, hoặc consumer có thể gửi acknowledgement ở tầng ứng dụng.

* Các message thuộc control plane.

## Tổng quan chức năng JetStream

### Streams

  * Dùng 'Add Stream' để định nghĩa stream và các thuộc tính một cách idempotent (subject nguồn, retention policy, storage policy, giới hạn).
  * Dùng 'Purge' để xóa tất cả message trong stream.
  * Dùng 'Delete' để xóa stream.


### Publish lên stream

> 🇬🇧 *There is interoperability between 'Core NATS' and JetStream in the fact that the streams are listening to core NATS messages. However you will notice that the NATS client libraries' JetStream calls include some 'Publish' calls and so may be wondering what is the difference between a 'Core NATS Publish' and a 'JetStream Publish'.*

Core NATS và JetStream có thể tương tác với nhau vì stream lắng nghe các message Core NATS. Tuy nhiên, các thư viện NATS client cũng có lời gọi 'Publish' trong phần JetStream — điều này dễ gây thắc mắc về sự khác biệt giữa 'Core NATS Publish' và 'JetStream Publish'.

> 🇬🇧 *So yes, when a 'Core NATS' application publishes a message on a Stream's subject, that message will indeed get stored in the stream, but that's not really the intent as you are then publishing with the lower quality of service provided by Core NATS. So, while it will definitely work to just use the Core NATS Publish call to publish to a stream, look at it more as a convenience that you can use to help ease the migration of your applications to use streaming rather the desired end state or ideal design.*

Đúng là khi ứng dụng Core NATS publish message lên subject của một stream, message đó sẽ được lưu vào stream — nhưng đây không phải cách dùng đúng ý định, vì lúc này chất lượng dịch vụ chỉ ở mức Core NATS. Việc dùng Core NATS Publish để publish lên stream tuy vẫn hoạt động, nhưng nên coi đó là bước tiện lợi để dễ dàng migrate ứng dụng sang streaming, chứ không phải thiết kế lý tưởng.

> 🇬🇧 *Instead, it is better for applications to use the JetStream Publish calls (which Core NATS subscribers not using Streams will still receive like any other publication) when publishing to a stream as:*

Thay vào đó, ứng dụng nên dùng JetStream Publish khi publish lên stream (các Core NATS subscriber không dùng stream vẫn nhận được như publication bình thường), vì:

* JetStream publish call được server có JetStream acknowledge lại, nhờ đó cung cấp các chất lượng dịch vụ cao hơn:
    * Nếu publisher nhận được acknowledgement từ server, nó có thể an toàn bỏ trạng thái của publication đó — message không chỉ được server nhận đúng mà còn được lưu trữ thành công.
    * Dù dùng JetStream publish đồng bộ hay bất đồng bộ, đều có flow control ngầm định giữa publisher và hạ tầng JetStream.
    * Có thể đạt chất lượng dịch vụ 'exactly-once' bằng cách ứng dụng publish chèn một publication ID duy nhất vào header field của message.

#### Xem thêm
* [Sync và Async JetStream publishing trong Java](https://nats.io/blog/sync-async-publish-java-client/#synchronous-and-asynchronous-publishing-with-the-nats-java-library)

### Tạo consumer

> 🇬🇧 *[Consumers](../../nats-concepts/jetstream/consumers.md) are 'views' into a stream, with their own cursor. They are how client applications get messages from a stream (i.e. 'replayed') for processing or consumption. They can filter messages in the stream according to a 'filtering subject' and define which part of the stream is replayed according to a 'replay policy'.*

[Consumer](../../nats-concepts/jetstream/consumers.md) là các 'view' vào một stream, mỗi consumer có con trỏ riêng. Đây là cách ứng dụng client lấy message từ stream (tức là 'replay') để xử lý hoặc tiêu thụ. Consumer có thể lọc message trong stream theo 'filtering subject' và xác định phần nào của stream được replay theo 'replay policy'.

> 🇬🇧 *You can create push or pull consumers:*
> 🇬🇧 *Push consumers (specifically ordered push consumers) are the best way for an application to receive its own complete copy of the selected messages in the stream.*
> 🇬🇧 *Pull consumers are the best way to scale horizontally the processing (or consuming) of the selected messages in the stream using multiple client applications sharing the same pull consumer, and allow for the processing of messages in batches.*

Có thể tạo consumer kiểu *push* hoặc *pull*:
* Consumer kiểu *push* (cụ thể là ordered push consumer) là cách tốt nhất để ứng dụng nhận toàn bộ bản sao các message được chọn trong stream.
* Consumer kiểu *pull* là cách tốt nhất để mở rộng ngang việc xử lý các message được chọn trong stream bằng nhiều ứng dụng client chia sẻ cùng pull consumer, đồng thời cho phép xử lý message theo batch.

> 🇬🇧 *Consumers can be ephemeral or durable, and support different sets of acknowledgement policies; none, this sequence number, this sequence number and all before it.*

Consumer có thể là ephemeral hoặc durable, và hỗ trợ các acknowledgement policy khác nhau: không acknowledge, acknowledge theo sequence number này, acknowledge sequence number này và tất cả trước đó.

#### Replay policy

> 🇬🇧 *You select which of the messages in the stream you want to have delivered to your consumer*

Chọn message nào trong stream sẽ được giao đến consumer:
* Tất cả
* Từ một sequence number cụ thể
* Từ một thời điểm cụ thể
* Message cuối cùng
* Message cuối cùng cho tất cả subject trong stream

> 🇬🇧 *And you can select the replay speed to be instant or to match the initial publication rate into the stream*

Có thể chọn tốc độ replay là tức thì hoặc khớp với tốc độ publication ban đầu vào stream.

### Subscribe từ consumer

> 🇬🇧 *Client applications 'subscribe' from consumers using the JetStream's Subscribe, QueueSubscribe or PullSubscribe (and variations) calls. Note that since the initial release of JetStream, clients have developed a more ergonomic API to work with [Consumers](https://github.com/nats-io/nats.go/blob/main/jetstream/README.md#consumers) to process messages.*

Ứng dụng client 'subscribe' từ consumer qua các lời gọi Subscribe, QueueSubscribe hoặc PullSubscribe (và các biến thể) của JetStream. Lưu ý rằng từ khi JetStream ra mắt, các client đã phát triển API tiện dụng hơn để làm việc với [Consumer](https://github.com/nats-io/nats.go/blob/main/jetstream/README.md#consumers) khi xử lý message.

#### Acknowledge message

> 🇬🇧 *Some consumers require the client application code to acknowledge the processing or consumption of the message, but there is more than one way to acknowledge (or not) a message*

Một số consumer yêu cầu code ứng dụng client phải acknowledge việc xử lý hoặc tiêu thụ message, và có nhiều cách để acknowledge (hoặc không):

* `Ack` Xác nhận message đã được xử lý hoàn toàn
* `Nak` Báo hiệu message chưa được xử lý lúc này và có thể chuyển sang message tiếp theo; message bị NAK sẽ được thử lại
* `InProgress` Khi gửi trước thời gian AckWait, báo hiệu công việc đang tiến hành và thời gian cần được gia hạn thêm một khoảng bằng `AckWait`
* `Term` Yêu cầu server dừng re-delivery message mà không acknowledge thành công

#### Xem thêm
* Java
  * [JetStream Java tutorial](https://nats.io/blog/hello-world-java-client/)
  * [Tạo JetStream stream trong Java](https://nats.io/blog/jetstream-java-client-01-stream-create/)
  * [JetStream publishing trong Java](https://nats.io/blog/jetstream-java-client-02-publish/)
  * [Consumer trong Java](https://nats.io/blog/jetstream-java-client-03-consume/)
  * [Push consumer trong Java](https://nats.io/blog/jetstream-java-client-04-push-subscribe/#jetstream-push-consumers-with-the-natsio-java-library)
  * [Pull consumer trong Java](https://nats.io/blog/jetstream-java-client-05-pull-subscribe/#jetstream-pull-consumers-with-the-natsio-java-library)

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message