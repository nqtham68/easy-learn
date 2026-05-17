---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/anatomy
title: Bạn dùng NATS để làm gì?
translated: true
translated_at: '2026-05-13T00:00:00Z'
---

# Bạn dùng NATS để làm gì?

> 🇬🇧 *You can use NATS to exchange information with and make requests to other applications. You can also use NATS to make your application into a distributed peer-to-peer application.*

NATS cho phép trao đổi thông tin và gửi request đến các ứng dụng khác. Bạn cũng có thể dùng NATS để biến ứng dụng của mình thành một hệ thống peer-to-peer phân tán.

> 🇬🇧 *At a high level your application can use NATS to:*

Ở mức tổng quan, ứng dụng của bạn có thể dùng NATS để:

1. Gửi (Publish) thông tin đến các ứng dụng khác hoặc các instance của chính ứng dụng.
2. Nhận (Subscribe) thông tin — theo thời gian thực hoặc khi ứng dụng khởi động — từ các ứng dụng khác hoặc các instance của ứng dụng.
3. Gửi request đến một server hoặc service do ứng dụng khác cung cấp.
4. Lưu trữ và đồng bộ trạng thái/dữ liệu dùng chung giữa các ứng dụng hoặc instance.
5. Nhận thông báo theo thời gian thực khi có dữ liệu mới được gửi hoặc khi trạng thái dùng chung thay đổi.

> 🇬🇧 *Using NATS means that, as an application developer you never have to worry about:*

Khi dùng NATS, developer không cần lo về:

* Ai gửi thông tin mà bạn muốn nhận.
* Ai quan tâm đến thông tin bạn gửi, có bao nhiêu người quan tâm, hay họ ở đâu.
* Service bạn gửi request đến đang chạy ở đâu, hay hiện có bao nhiêu instance đang hoạt động.
* Cluster có bao nhiêu partition hoặc server.
* Bảo mật (chỉ cần xác thực danh tính).
* Ứng dụng có đang chạy hay không tại thời điểm thông tin được gửi (dùng JetStream).
* Flow control (dùng JetStream).
* Các chất lượng dịch vụ cao hơn như **exactly-once** (dùng JetStream).
* Fault-tolerance và việc server nào đang hoạt động hay không tại bất kỳ thời điểm nào.
* Topology của hạ tầng NATS server hay cách nó được thiết kế.

# Cấu trúc của một NATS Client Application

> 🇬🇧 *A NATS Client Application will use the NATS Client Library in the following way:*

Một NATS Client Application sử dụng NATS Client Library theo quy trình sau:

> 🇬🇧 *At initialization time it will first connect (securely if needed) to a NATS Service Infrastructure (i.e. one of the NATS servers).*

Khi khởi tạo, ứng dụng trước tiên kết nối (có bảo mật nếu cần) đến NATS Service Infrastructure (tức một trong các NATS server).

> 🇬🇧 *Once successfully connected the application will:*

Sau khi kết nối thành công, ứng dụng có thể:

  * Tạo message và publish lên các subject (chuỗi định danh message) hoặc stream.
  * Subscribe vào các subject hoặc stream consumer để nhận message từ các process khác.
  * Publish request message đến một service và nhận reply message.
  * Nhận request message và gửi lại reply hoặc acknowledgement.
  * Liên kết và truy xuất message gắn với các key trong KV bucket.
  * Lưu trữ và truy xuất các blob kích thước tùy ý bằng key trong object store.

> 🇬🇧 *Finally, when the application terminates it should disconnect from the NATS Service Infrastructure.*

Khi kết thúc, ứng dụng nên ngắt kết nối khỏi NATS Service Infrastructure.

> 🇬🇧 *See the following sections to learn more about those activities.*

Xem các phần tiếp theo để tìm hiểu thêm về từng hoạt động này.

# Kết nối và ngắt kết nối

> 🇬🇧 *The first thing any application needs to do is connect to NATS. Depending on the way the NATS Service Infrastructure being used is configured the connection may need to be secured, and therefore the application also needs to be able to specify security credentials at connection time. An application can create as many NATS connections as needed (each connection being completely independent, it could for example connect twice as two different users), although typically most applications only make a single NATS connection.*

Việc đầu tiên ứng dụng cần làm là kết nối đến NATS. Tùy cách cấu hình NATS Service Infrastructure, kết nối có thể cần bảo mật — khi đó ứng dụng phải cung cấp credential (thông tin đăng nhập) khi kết nối. Một ứng dụng có thể tạo bao nhiêu NATS connection tùy ý (mỗi connection hoàn toàn độc lập, ví dụ có thể kết nối hai lần với hai user khác nhau), nhưng thông thường hầu hết ứng dụng chỉ dùng một NATS connection duy nhất.

> 🇬🇧 *Once you have obtained a valid connection, you can use that connection in your application to use all of the Core NATS functionalities such as subscribing to subjects, publishing messages, making requests (and getting a JetStream context).*

Sau khi có connection hợp lệ, bạn có thể sử dụng toàn bộ chức năng Core NATS: subscribe vào các subject, publish message, gửi request (và lấy JetStream context).

> 🇬🇧 *Finally, the application will need to disconnect safely from NATS.*

Cuối cùng, ứng dụng cần ngắt kết nối an toàn khỏi NATS.

## [Kết nối đến NATS](./connecting)

## Giám sát kết nối NATS

> 🇬🇧 *It is recommended that the application use [connection event listeners](./events/events.md) in order to be alerted and log whenever connections, reconnections or disconnections happen. Note that in case of a disconnection from the NATS server process the client library will automatically attempt to [reconnect](./reconnect) to one of the other NATS servers in the cluster. You can also always check the [current connection status](./events).*

Nên dùng [connection event listeners](./events/events.md) để ghi log mỗi khi kết nối, reconnect hoặc ngắt kết nối xảy ra. Lưu ý rằng khi mất kết nối với NATS server, client library sẽ tự động thử [reconnect](./reconnect) đến một server khác trong cluster. Bạn cũng có thể kiểm tra [trạng thái kết nối hiện tại](./events) bất cứ lúc nào.

## Ngắt kết nối an toàn khỏi NATS

> 🇬🇧 *The recommended way to disconnect is to use [Drain()](./receiving/drain.md) which will wait for any ongoing processing to conclude and clean everything properly, but if you need to close the connection immediately you can use `close()` from your connection object.*

Cách ngắt kết nối được khuyến nghị là dùng [Drain()](./receiving/drain.md) — hàm này sẽ chờ các tác vụ đang xử lý hoàn tất và dọn dẹp đúng cách. Nếu cần đóng kết nối ngay lập tức, hãy dùng `close()` từ connection object.

# Làm việc với message

> 🇬🇧 *Messages store the data that applications exchange with each other. A message has a *subject*, a *data payload* (byte array), and may also have a *reply-to* and *header* fields.*

Message (gói dữ liệu được gửi đi) là đơn vị mang dữ liệu trao đổi giữa các ứng dụng. Một message có một *subject*, một *data payload* (mảng byte), và có thể có thêm trường *reply-to* và *header*.

> 🇬🇧 *You get messages returned or passed to your callbacks from subscribing, or making requests. The publish (and request) operations typically just take a subject and a byte array data payload and create the message for you, but you can also create a message yourself (if you want to set some headers).*

Message được trả về hoặc truyền vào callback khi subscribe hoặc gửi request. Thao tác publish (và request) thường chỉ cần subject và byte array payload — thư viện sẽ tự tạo message. Bạn cũng có thể tự tạo message nếu muốn đặt các header tùy chỉnh.

> 🇬🇧 *Some messages can be 'acknowledged' (for example message received from JetStream pull consumers), and there are multiple forms of acknowledgements (including negative acknowledgements, and acknowledgements indicating that your application has properly received the message but needs more time to process it).*

Một số message có thể được 'acknowledge' (ví dụ: message nhận từ JetStream pull consumer). Có nhiều dạng acknowledgement: bao gồm negative acknowledgement, và acknowledgement báo hiệu rằng ứng dụng đã nhận đúng nhưng cần thêm thời gian xử lý.

### Dữ liệu có cấu trúc

> 🇬🇧 *Some libraries allow you to easily [send](./sending/structure.md) and [receive](./receiving/structure.md) structured data.*

Một số thư viện cho phép dễ dàng [gửi](./sending/structure.md) và [nhận](./receiving/structure.md) dữ liệu có cấu trúc.

# Sử dụng Core NATS

> 🇬🇧 *Once your application has successfully connected to the NATS Server infrastructure, you can then start using the returned connection object to interact with NATS.*

Sau khi kết nối thành công đến NATS Server infrastructure, bạn có thể dùng connection object trả về để tương tác với NATS.

## Publish trong Core NATS

> 🇬🇧 *You can directly [publish](./sending) on a connection some data addressed by a subject (or publish a pre-created messages with headers).*

Bạn có thể trực tiếp [publish](./sending) dữ liệu lên một subject qua connection, hoặc publish message đã tạo sẵn có kèm header.

### Flush và Ping/Pong

> 🇬🇧 *Because of caching, if your application is highly sensitive to latency, you may want to [flush](./sending/caches.md) after publishing.*

Do cơ chế cache, nếu ứng dụng nhạy cảm với độ trễ, bạn nên [flush](./sending/caches.md) sau khi publish.

> 🇬🇧 *Many of the client libraries use the [PING/PONG interaction](./connecting/pingpong.md) built into the NATS protocol to ensure that flush pushed all of the buffered messages to the server. When an application calls flush, most libraries will put a PING on the outgoing queue of messages, and wait for the server to respond with a PONG before saying that the flush was successful.*

Nhiều client library dùng [tương tác PING/PONG](./connecting/pingpong.md) tích hợp sẵn trong NATS protocol để đảm bảo flush đã đẩy toàn bộ message đang buffer lên server. Khi gọi flush, hầu hết các thư viện sẽ đặt một PING vào hàng đợi message gửi đi và chờ server phản hồi PONG trước khi xác nhận flush thành công.

> 🇬🇧 *Even though the client may use PING/PONG for flush, pings sent this way do not count towards [max outgoing pings](./connecting/pingpong.md).*

Dù client dùng PING/PONG để flush, các ping gửi theo cách này không được tính vào [số lượng ping gửi đi tối đa](./connecting/pingpong.md).

## Subscribe trong Core NATS

> 🇬🇧 *The process of subscribing involves having the client library tell the NATS that an application is interested in a particular subject. When an application is done with a subscription it unsubscribes telling the server to stop sending messages.*

Quá trình subscribe là client library thông báo cho NATS biết ứng dụng quan tâm đến một subject cụ thể. Khi không cần nữa, ứng dụng unsubscribe để server ngừng gửi message.

> 🇬🇧 *Receiving messages with NATS can be library dependent, some languages, like Go or Java, provide synchronous and asynchronous APIs, while others may only support one type of subscription. In general, applications can receive messages [asynchronously](./receiving/async.md) or [synchronously](./receiving/sync.md).*

Cách nhận message phụ thuộc vào thư viện: một số ngôn ngữ như Go hay Java cung cấp cả API đồng bộ lẫn bất đồng bộ, trong khi các ngôn ngữ khác chỉ hỗ trợ một kiểu. Nói chung, ứng dụng có thể nhận message [bất đồng bộ](./receiving/async.md) hoặc [đồng bộ](./receiving/sync.md).

> 🇬🇧 *You can always subscribe to more than one subject at a time using [wildcards](./receiving/wildcards.md).*

Bạn có thể subscribe vào nhiều subject cùng lúc bằng cách dùng [wildcard](./receiving/wildcards.md).

> 🇬🇧 *A client will receive a message for each matching subscription, so if a connection has multiple subscriptions using identical or overlapping subjects \(say `foo` and `>`\) the same message will be sent to the client multiple times.*

Client sẽ nhận một message cho mỗi subscription khớp. Vì vậy, nếu một connection có nhiều subscription dùng subject giống hoặc chồng lấn nhau \(ví dụ `foo` và `>`\), cùng một message sẽ được gửi đến client nhiều lần.

### Subscribe với queue group

> 🇬🇧 *You can also subscribe [as part of a distributed *queue group*](./receiving/queues.md). All the subscribers with the same queue group name form the distributed queue. The NATS Servers automatically distributes the messages published on the matching subject(s) between the members of the queue group.*

Bạn có thể subscribe [như một phần của *queue group* phân tán](./receiving/queues.md). Tất cả subscriber (bên đăng ký nhận message) có cùng tên queue group sẽ tạo thành một hàng đợi phân tán. NATS Server tự động phân phối message được publish trên các subject khớp giữa các thành viên trong queue group.

> 🇬🇧 *On a given subject there can be more than one queue group created by subscribing applications, each queue group being an independent queue and distributing its own copy of the messages between the queue group members.*

Trên một subject, nhiều queue group có thể cùng tồn tại — mỗi queue group là một hàng đợi độc lập và phân phối bản sao riêng của message cho các thành viên của nó.

### Slow consumer

> 🇬🇧 *One thing to keep in mind when making Core NATS subscriptions to subjects is that your application must be able to keep up with the flow of messages published on the subject(s) or it will otherwise become a [slow consumer](./events/slow.md)*

Cần lưu ý khi subscribe vào subject trong Core NATS: ứng dụng phải xử lý kịp tốc độ message được publish, nếu không sẽ trở thành [slow consumer](./events/slow.md).

## Unsubscribe

> 🇬🇧 *When you no longer want to receive the messages on a particular subject you must call [unsubscribe](./receiving/unsubscribing.md), or you can [automatically unsubscribe](./receiving/unsub_after.md) after receiving a specific number of messages.*

Khi không muốn nhận message trên một subject nữa, hãy gọi [unsubscribe](./receiving/unsubscribing.md), hoặc cài đặt [tự động unsubscribe](./receiving/unsub_after.md) sau khi nhận đủ số lượng message nhất định.

## Gửi request đến service

> 🇬🇧 *You can also use NATS to easily and transparently invoke services without needing to know about the location or number of servers for the service. The connection's [request](./sending/request_reply.md) call publishes a message on the specified subject that contains a [reply-to](./sending/replyto.md) inbox subject and then waits for a reply message to be received by that inbox.*

NATS cho phép gọi service một cách trong suốt mà không cần biết vị trí hay số lượng server của service đó. Lời gọi [request](./sending/request_reply.md) trên connection sẽ publish một message lên subject chỉ định, kèm subject inbox [reply-to](./sending/replyto.md), rồi chờ nhận reply message tại inbox đó.

## Xử lý và phản hồi request

> 🇬🇧 *The server applications servicing those requests simply need to subscribe to the subject on which the requests are published, process the request messages they receive and [reply](./receiving/reply.md) to the message on the subject contained in the request message's [Reply-to](./receiving/reply.md) attribute.*

Ứng dụng server xử lý các request chỉ cần subscribe vào subject mà request được publish lên, xử lý các request message nhận được và [reply](./receiving/reply.md) đến subject chứa trong thuộc tính [Reply-to](./receiving/reply.md) của request message.

> 🇬🇧 *Typically, there is no reason not to want to make your service distributed (i.e. scalable and fault-tolerant). This means that unless there's a specific reason not to, application servicing requests should [subscribe to the request subject using the same queue group name](./receiving/queues.md). You can have more than one queue group present on a subject (for example you could have one queue group to distribute the processing of the requests between service instances, and another queue group to distribute the logging or monitoring of the requests being made to the service).*

Thông thường, không có lý do gì để không làm service có khả năng phân tán (tức là scalable và fault-tolerant). Vì vậy, trừ khi có lý do đặc biệt, ứng dụng xử lý request nên [subscribe vào subject request bằng cùng tên queue group](./receiving/queues.md). Một subject có thể có nhiều hơn một queue group — ví dụ một queue group để phân phối việc xử lý request giữa các instance của service, và một queue group khác để phân phối việc ghi log hoặc giám sát các request gửi đến service.

# Streaming với JetStream

> 🇬🇧 *Some applications can make use of the extra functionalities enabled by [JetStream](../jetstream/develop_jetstream.md) (streams, KV Store, Object Store). Just like you use the Core NATS connection object to invoke Core NATS operations, you use a [*JetStream context*](./js/context.md) to invoke JetStream operations. You can specify things like the timeout value for all the operations executed from the context. JS context are light-weight, so while it is safe to share a JS context between threads, for best performance do not be afraid to have a context per thread.*

Một số ứng dụng có thể tận dụng các tính năng bổ sung của [JetStream](../jetstream/develop_jetstream.md) (stream, KV Store, Object Store). Tương tự như dùng connection object cho Core NATS, bạn dùng [*JetStream context*](./js/context.md) để thực hiện các thao tác JetStream. Bạn có thể cấu hình timeout cho tất cả thao tác từ context. JS context rất nhẹ, do đó có thể chia sẻ giữa các thread an toàn, nhưng để hiệu năng tốt nhất, hãy mạnh dạn tạo một context riêng cho mỗi thread.

## Các tính năng Streaming

> 🇬🇧 *You can use [streams](../jetstream/model_deep_dive.md#stream-limits-retention-and-policy) for two broad use cases:*

Bạn có thể dùng [stream](../jetstream/model_deep_dive.md#stream-limits-retention-and-policy) cho hai nhóm use case chính:

- Temporal decoupling: cho phép ứng dụng subscriber lấy lại theo yêu cầu các message đã lưu trong stream từ các lần publish trước (và có thể cả tương lai).
- Queuing: cho phép các instance của ứng dụng subscriber lấy, xử lý an toàn và xóa (tức là consume) từng message hoặc batch message khỏi stream — về bản chất là dùng stream như một distributed work queue.

## Định nghĩa stream

> 🇬🇧 *Before you can use a stream to replay or consume messages published on a subject, it must be defined. The stream definition attributes specify*

Trước khi dùng stream để replay hoặc consume message publish lên một subject, stream phải được định nghĩa. Các thuộc tính định nghĩa stream xác định:

- những gì được lưu trữ (tức subject nào stream theo dõi)
- cách lưu trữ (ví dụ: file hay memory storage, số lượng replica)
- thời gian lưu trữ message (ví dụ: theo giới hạn, theo interest, hoặc theo kiểu work queue): retention policy

> 🇬🇧 *Streams can be (and often are) administratively defined ahead of time (for example using the NATS CLI Tool). The application can also [manage streams (and consumers) programmatically](./js/streams.md).*

Stream thường được định nghĩa trước bởi admin (ví dụ dùng NATS CLI Tool). Ứng dụng cũng có thể [quản lý stream (và consumer) theo cách lập trình](./js/streams.md).

## Publish lên stream

> 🇬🇧 *Any message published, on a subject monitored by a stream gets stored in the stream. If your application publishes a message using the Core NATS publish call (from the connection object) on a stream's subject, the message will get stored in the stream, the Core NATS publishers do not know or care whether there is a stream for that subject or not.*

Mọi message được publish lên subject mà stream theo dõi đều được lưu vào stream. Nếu ứng dụng publish bằng lời gọi Core NATS publish (từ connection object) trên subject của stream, message sẽ vẫn được lưu — publisher (bên gửi message) trong Core NATS không quan tâm đến việc có stream cho subject đó hay không.

> 🇬🇧 *However, if you know that there is going to be a stream defined for that subject you will get higher quality of service by [publishing using the JetStream Context's publish call](./js/publish.md) (rather than the connection's publish call). This is because JetStream publications will receive an acknowledgement (or not) from the NATS Servers when the message has been positively received _and_ stored in the stream (while Core NATS publications are not acknowledged by the NATS Servers). This difference is also the reason why there are both synchronous and asynchronous versions of the JetStream publish operation.*

Tuy nhiên, nếu biết rằng subject đó có stream, bạn nên [publish bằng lời gọi publish của JetStream Context](./js/publish.md) để đạt chất lượng dịch vụ cao hơn. Lý do là JetStream publication sẽ nhận được acknowledgement từ NATS Server khi message được nhận thành công _và_ lưu vào stream (trong khi Core NATS publication không được NATS Server acknowledge). Sự khác biệt này cũng là lý do tại sao JetStream publish có cả hai phiên bản đồng bộ và bất đồng bộ.

## Stream consumer

> 🇬🇧 *Stream *consumers* are how application get messages from stream. To make another analogy to database concepts a consumers can be seen as a kind of 'views' (on a stream):*

Stream *consumer* (bên xử lý dữ liệu từ stream) là cơ chế để ứng dụng lấy message từ stream. Tương tự như khái niệm database, consumer có thể xem như một dạng 'view' (trên stream):

- Consumer có thể có *subject filter* để lọc message từ stream theo tên subject.
- Consumer có *ack policy* xác định ứng dụng có phải *acknowledge* việc nhận và xử lý message hay không (lưu ý rằng explicit acknowledgement là *bắt buộc* với một số loại stream và consumer để hoạt động đúng). Bao gồm cả thời gian chờ acknowledgement và số lần consumer thử re-deliver message chưa được acknowledge.
- Consumer có [*deliver policy*](../jetstream/model_deep_dive.md#consumer-starting-position) xác định vị trí trong stream mà consumer bắt đầu giao message.
- Consumer có *replay policy* xác định tốc độ consumer replay message.

> 🇬🇧 *Consumers also have a small amount of state on the NATS Server to store some message sequence numbers 'cursors'. You can have as many consumers as you need per stream.*

Consumer cũng lưu một lượng nhỏ trạng thái trên NATS Server để ghi lại các 'cursor' số thứ tự message. Bạn có thể tạo bao nhiêu consumer tùy ý cho mỗi stream.

> 🇬🇧 *Client applications either create *ephemeral* consumers, or define/find *durable* consumers. Applications either subscribe to 'push' consumers (consumers defined with a delivery subject and optionally a queue group name for that delivery subject), or fetch on demand (including an optional prefetch) from 'pull' consumers (consumers defined without a delivery subject or queue group name as they don't need any while providing the same functionality).*

Ứng dụng client hoặc tạo *ephemeral* consumer, hoặc định nghĩa/tìm kiếm *durable* consumer. Ứng dụng có thể subscribe vào 'push' consumer (consumer được định nghĩa với delivery subject và tùy chọn tên queue group), hoặc fetch theo yêu cầu (bao gồm cả prefetch tùy chọn) từ 'pull' consumer (consumer không có delivery subject hay tên queue group, nhưng vẫn cung cấp chức năng tương đương).

### Ephemeral consumer

> 🇬🇧 *[Ephemeral consumers](../jetstream/model_deep_dive.md#ephemeral-consumers) are, as the name suggest, not meant to last and are automatically cleaned up by the NATS Servers when the application instance that created them shuts down. Ephemeral consumers are created on-demand by individual application instances and are used only by the application instance that created them.*

[Ephemeral consumer](../jetstream/model_deep_dive.md#ephemeral-consumers) — đúng như tên gọi — không được thiết kế để tồn tại lâu dài và sẽ tự động được NATS Server dọn dẹp khi instance ứng dụng tạo ra chúng đóng lại. Ephemeral consumer được tạo theo yêu cầu bởi từng instance ứng dụng và chỉ được dùng bởi instance đó.

> 🇬🇧 *Applications typically use ephemeral *ordered push consumers* to get they own copy of the messages stored in a stream whenever they want.*

Ứng dụng thường dùng *ordered push consumer* ephemeral để lấy bản sao riêng của các message lưu trong stream bất cứ khi nào cần.

### Durable consumer

> 🇬🇧 *Durable consumers are, as the name suggest, meant to be 'always on', and used (shared) by multiple instances of the client application or by applications that get stopped and restarted multiple times and need to maintain state from one run of the application to another.*

Durable consumer — đúng như tên gọi — được thiết kế để 'luôn hoạt động', được dùng chung bởi nhiều instance của ứng dụng client hoặc bởi các ứng dụng khởi động và dừng nhiều lần cần duy trì trạng thái qua các lần chạy.

> 🇬🇧 *Durable consumers can be managed administratively using the NATS CLI Tool, or programmatically by the application itself. A consumer is created as a durable consumer simply by specifying a durable name at creation time.*

Durable consumer có thể được quản lý bởi admin qua NATS CLI Tool, hoặc theo cách lập trình bởi chính ứng dụng. Một consumer trở thành durable consumer đơn giản bằng cách chỉ định tên durable khi tạo.

> 🇬🇧 *Applications typically use *durable pull consumers* to distribute and scale horizontally the processing (or consumption) of the messages in a stream.*

Ứng dụng thường dùng *durable pull consumer* để phân phối và scale ngang việc xử lý (hay consumption) message trong stream.

### Consumer acknowledgement

> 🇬🇧 *Some types of consumers (e.g. pull consumers) require the application receiving messages from the consumer to *explicitly* [acknowledge](../jetstream/model_deep_dive.md#acknowledgement-models) the reception and processing of those messages. The application can invoke one of the following acknowledgement functions on the message received from the consumer:*

Một số loại consumer (ví dụ: pull consumer) yêu cầu ứng dụng nhận message phải *explicitly* [acknowledge](../jetstream/model_deep_dive.md#acknowledgement-models) việc nhận và xử lý message đó. Ứng dụng có thể gọi một trong các hàm acknowledgement sau trên message nhận từ consumer:

- `ack()` để xác nhận tích cực việc nhận và xử lý message thành công.
- `term()` để chỉ ra rằng message không thể và sẽ không bao giờ có thể xử lý được, không cần gửi lại. Dùng term khi request không hợp lệ.
- `nack()` để từ chối xử lý message, yêu cầu gửi lại. Dùng nack khi request hợp lệ nhưng tạm thời không xử lý được. Nếu không xử lý được do điều kiện tạm thời, hãy tạm thời đóng subscription cho đến khi có thể xử lý lại.
- `inProgress()` để báo hiệu rằng message đang được xử lý và cần thêm thời gian (trước khi message bị coi là cần gửi lại).

## Chất lượng dịch vụ cao hơn

> 🇬🇧 *Besides temporal decoupling and queuing, JetStream also enables higher qualities of service compared to Core NATS. Defining a stream on a subject and using consumers brings the quality of service up to *at least once*, meaning that you are guaranteed to get the message (even if your application is down at publication time) but there are some corner case failure scenarios in which you could result in message duplication due to double publication of the message, or double processing of a message due to acknowledgement loss or crashing after processing but before acknowledging. You can enable and use [message de-duplication](../jetstream/model_deep_dive.md#message-deduplication) and double-acking to protect against those failure scenarios and get [exactly once](../jetstream/model_deep_dive.md#exactly-once-delivery) quality of service.*

Ngoài temporal decoupling và queuing, JetStream còn cung cấp chất lượng dịch vụ cao hơn so với Core NATS. Định nghĩa stream trên một subject và dùng consumer nâng chất lượng dịch vụ lên mức *at least once* — đảm bảo bạn sẽ nhận được message (dù ứng dụng bị down khi publish), nhưng vẫn tồn tại một số tình huống lỗi ngoại lệ dẫn đến message bị trùng lặp (do publish kép) hoặc xử lý trùng (do mất acknowledgement hoặc crash sau khi xử lý nhưng trước khi acknowledge). Bạn có thể dùng [message de-duplication](../jetstream/model_deep_dive.md#message-deduplication) và double-acking để phòng tránh các tình huống đó và đạt chất lượng dịch vụ [exactly once](../jetstream/model_deep_dive.md#exactly-once-delivery).

## Key Value Store

> 🇬🇧 *The [Key Value Store](./js/kv.md) functionality is implemented on top of JetStream, but offers a different interface in the form of keys and values rather than subject names and messages. You can use a bucket to put (including compare and set), get and delete a value (a byte array like a message payload) associated with a key (a string, like a subject). It also allows you to 'watch' for changes to the bucket as they happen. And finally it allows you to maintain a history of the values associated with a key over time, as well as get a specific revision of the value.*

Tính năng [Key Value Store](./js/kv.md) được xây dựng trên JetStream, nhưng cung cấp interface dưới dạng key-value thay vì subject và message. Bạn có thể dùng bucket để put (bao gồm compare and set), get và delete một giá trị (mảng byte như payload của message) gắn với một key (chuỗi, giống subject). Tính năng này cũng cho phép 'watch' các thay đổi của bucket khi chúng xảy ra, duy trì lịch sử các giá trị gắn với một key theo thời gian, cũng như lấy một revision cụ thể của giá trị.

## Object Store

**NOTICE: Technology Preview**

> 🇬🇧 *The Object Store is similar to the Key Value Store but meant to be used where the values can be of any arbitrary large size, as opposed to limited to the maximum size of a NATS message, as it the case with the Key Value Store.*

Object Store tương tự Key Value Store nhưng được thiết kế cho trường hợp giá trị có thể có kích thước tùy ý lớn, khác với Key Value Store bị giới hạn bởi kích thước tối đa của một NATS message.

## Thuật ngữ trong bài

- **async**: bất đồng bộ
- **buffer**: vùng đệm tạm
- **cache**: bộ nhớ đệm
- **callback**: hàm được gọi lại
- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **credential**: thông tin đăng nhập
- **header**: phần metadata kèm theo
- **message**: gói dữ liệu được gửi đi
- **partition**: phần dữ liệu được chia ra
- **payload**: nội dung chính của message
- **publisher**: bên gửi message
- **queue**: hàng đợi message
- **queue group**: nhóm subscribers chia sẻ tải
- **replica**: bản sao dữ liệu
- **request**: yêu cầu
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **sync**: đồng bộ
- **timeout**: thời gian chờ tối đa
- **thread**: luồng xử lý