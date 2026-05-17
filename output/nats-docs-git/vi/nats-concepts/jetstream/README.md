---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/jetstream
title: JetStream
translated: true
translated_at: '2026-05-13T00:00:00+00:00'
---

# JetStream

> 🇬🇧 *NATS has a built-in persistence engine called [JetStream](https://docs.nats.io/using-nats/jetstream/develop\_jetstream) which enables messages to be stored and replayed at a later time. Unlike _NATS Core_ which requires you to have an active subscription to process messages as they happen, JetStream allows the NATS server to capture messages and replay them to consumers as needed. This functionality enables a different quality of service for your NATS messages, and enables fault-tolerant and high-availability configurations.*

NATS tích hợp sẵn engine lưu trữ có tên [JetStream](https://docs.nats.io/using-nats/jetstream/develop\_jetstream), cho phép lưu trữ message và phát lại sau. Khác với _NATS Core_ — yêu cầu subscription đang hoạt động để nhận message theo thời gian thực — JetStream cho phép NATS server bắt giữ message và phát lại cho consumer (bên xử lý dữ liệu từ stream) theo yêu cầu. Tính năng này mang lại chất lượng dịch vụ cao hơn và hỗ trợ cấu hình fault-tolerant và high-availability.

> 🇬🇧 *JetStream is built into `nats-server`. If you have a cluster of JetStream-enabled servers you can enable data replication and thus guard against failures and service disruptions.*

JetStream được tích hợp sẵn trong `nats-server`. Nếu có một cluster (cụm nhiều server chạy chung) các server đã bật JetStream, bạn có thể kích hoạt data replication để bảo vệ khỏi lỗi và gián đoạn dịch vụ.

> 🇬🇧 *JetStream was created to address the problems identified with streaming technology today - complexity, fragility, and a lack of scalability. Some technologies address these better than others, but no current streaming technology is truly multi-tenant, horizontally scalable, or supports multiple deployment models. No other technology that we are aware of can scale from edge to cloud using the same security context while having complete deployment observability for operations.*

JetStream được tạo ra để giải quyết các vấn đề của công nghệ streaming hiện nay: sự phức tạp, tính dễ vỡ, và thiếu khả năng mở rộng. Một số công nghệ giải quyết những vấn đề này tốt hơn, nhưng chưa có công nghệ streaming nào thực sự multi-tenant, horizontally scalable, hay hỗ trợ nhiều mô hình triển khai. Cũng chưa có công nghệ nào có thể scale từ edge đến cloud trong cùng một security context với khả năng quan sát triển khai đầy đủ cho vận hành.

#### Các tính năng bổ sung được kích hoạt bởi JetStream

> 🇬🇧 *The JetStream persistence layer enables additional use cases typically not found in messaging systems. Being built on top of JetStream they inherit the core capabilities of JetStream, replication, security, routing limits, and mirroring.*

Lớp lưu trữ của JetStream mở ra các use case thường không có trong các hệ thống messaging. Vì được xây dựng trên JetStream, chúng kế thừa các tính năng cốt lõi: replication, bảo mật, giới hạn routing, và mirroring.

* [Key Value Store](.#key-value-store) — map (mảng kết hợp) với các thao tác atomic
* [Object Store](.#object-store) — API truyền file, replication và lưu trữ. Sử dụng chunked transfer để mở rộng quy mô.

> 🇬🇧 *Key/Value and File transfer are capabilities commonly found in in-memory databases or deployment tools. While NATS does not intend to compete with the feature set of such tools, it is our goal to provide the developer with reasonable complete set of data storage and replications features for use cases like micro service, edge deployments and server management.*

Key/Value và File transfer là các tính năng thường thấy trong in-memory database hoặc công cụ triển khai. NATS không có ý định cạnh tranh với bộ tính năng đầy đủ của những công cụ đó, nhưng mục tiêu là cung cấp cho developer một bộ tính năng lưu trữ và replication đủ dùng cho các use case như microservice, edge deployment và quản lý server.

#### Cấu hình

> 🇬🇧 *To configure a `nats-server` with JetStream refer to:*

Để cấu hình `nats-server` với JetStream, tham khảo:

* [Configuring JetStream](https://docs.nats.io/running-a-nats-service/configuration/jetstream-config/resource\_management)
* [JetStream Clustering](https://docs.nats.io/running-a-nats-service/configuration/clustering/jetstream\_clustering)

#### Ví dụ

> 🇬🇧 *For runnable JetStream code examples, refer to [NATS by Example](https://natsbyexample.com).*

Để xem các ví dụ code JetStream có thể chạy được, tham khảo [NATS by Example](https://natsbyexample.com).

#### Mục tiêu thiết kế

> 🇬🇧 *JetStream was developed with the following goals in mind:*

JetStream được phát triển với các mục tiêu sau:

* Hệ thống phải dễ cấu hình, vận hành và có thể quan sát được.
* Hệ thống phải an toàn và hoạt động tốt với mô hình bảo mật NATS 2.0.
* Hệ thống phải mở rộng theo chiều ngang và phù hợp với tốc độ nhập dữ liệu cao.
* Hệ thống phải hỗ trợ nhiều use case.
* Hệ thống phải tự phục hồi.
* Hệ thống phải cho phép NATS message tham gia vào stream khi cần.
* Hệ thống phải hoạt động bất khả tri với payload.
* Hệ thống không được phụ thuộc vào thư viện bên thứ ba.

### Các tính năng của JetStream

#### Streaming: tách rời thời gian giữa publisher và subscriber

> 🇬🇧 *One of the tenets of basic publish/subscribe messaging is that there is a required temporal coupling between the publishers and the subscribers: subscribers only receive the messages that are published when they are actively connected to the messaging system (i.e. they do not receive messages that are published while they are not subscribing or not running or disconnected). The traditional way for messaging systems to provide temporal decoupling of the publishers and subscribers is through the 'durable subscriber' functionality or sometimes through 'queues', but neither one is perfect:*

Một nguyên tắc cơ bản của publish/subscribe là sự ràng buộc thời gian giữa publisher (bên gửi message) và subscriber (bên đăng ký nhận message): subscriber chỉ nhận được message khi đang kết nối — không nhận được message gửi lúc nó offline. Cách truyền thống để tách rời thời gian là dùng "durable subscriber" hoặc "queue", nhưng cả hai đều không hoàn hảo:

* durable subscriber phải được tạo _trước_ khi message được gửi
* queue dùng để phân phối và xử lý công việc, không phải để phát lại message.

> 🇬🇧 *However, in many use cases, you do not need to 'consume exactly once' functionality but rather the ability to replay messages on demand, as many times as you want. This need has led to the popularity of some 'streaming' messaging platforms.*

Tuy nhiên, trong nhiều use case, không cần chức năng "consume exactly once" mà chỉ cần khả năng phát lại message theo yêu cầu, bao nhiêu lần tùy thích. Nhu cầu này đã thúc đẩy sự phổ biến của các nền tảng "streaming".

> 🇬🇧 *JetStream provides _both_ the ability to _consume_ messages as they are published (i.e. 'queueing') as well as the ability to _replay_ messages on demand (i.e. 'streaming'). See [retention policies](.#Retention-policies-and-limits) below.*

JetStream cung cấp _cả hai_: khả năng _consume_ message ngay khi được gửi (tức "queueing") lẫn khả năng _phát lại_ message theo yêu cầu (tức "streaming"). Xem [retention policies](.#Retention-policies-and-limits) bên dưới.

**Chính sách phát lại (Replay policies)**

> 🇬🇧 *JetStream consumers support multiple replay policies, depending on whether the consuming application wants to receive either:*

JetStream consumer hỗ trợ nhiều replay policy, tùy theo nhu cầu của ứng dụng muốn nhận:

* _Tất cả_ message đang lưu trong stream — nghĩa là phát lại toàn bộ. Tốc độ phát lại có thể chọn:
  * _instant_ — message được gửi đến consumer nhanh nhất có thể.
  * _original_ — message được gửi với tốc độ bằng lúc chúng được publish vào stream, hữu ích cho staging traffic production.
* Message _cuối cùng_ trong stream, hoặc _message cuối cho từng subject_ (vì stream có thể thu thập nhiều subject).
* Bắt đầu từ một _sequence number_ cụ thể.
* Bắt đầu từ một _thời điểm_ cụ thể.

**Chính sách lưu trữ (Retention policies) và giới hạn**

> 🇬🇧 *JetStream enables new functionalities and higher qualities of service on top of the base 'Core NATS' functionality. However, practically speaking, streams can't always just keep growing 'forever' and therefore JetStream supports multiple retention policies as well as the ability to impose size limits on streams.*

JetStream bổ sung các tính năng mới và chất lượng dịch vụ cao hơn trên nền Core NATS. Tuy nhiên, thực tế stream (luồng message lưu trữ liên tục) không thể tăng trưởng mãi, vì vậy JetStream hỗ trợ nhiều retention policy và giới hạn kích thước stream.

**Giới hạn**

> 🇬🇧 *You can impose the following limits on a stream*

Bạn có thể đặt các giới hạn sau cho một stream:

* Tuổi tối đa của message.
* Tổng kích thước tối đa của stream (tính bằng bytes).
* Số lượng message tối đa trong stream.
* Kích thước tối đa của mỗi message.
* Số lượng consumer tối đa được định nghĩa cho stream tại bất kỳ thời điểm nào.

> 🇬🇧 *You must also select a **discard policy** which specifies what should happen once the stream has reached one of its limits and a new message is published:*

Bạn cũng phải chọn một **discard policy** — xác định hành động khi stream đạt giới hạn và có message mới được gửi đến:

* _discard old_ — stream tự xóa message cũ nhất để nhường chỗ cho message mới.
* _discard new_ — message mới bị bỏ (lệnh publish JetStream trả về lỗi báo đã đạt giới hạn).

**Retention policy**

> 🇬🇧 *You can choose what kind of retention you want for each stream:*

Bạn có thể chọn loại retention cho từng stream:

* _limits_ (mặc định) — lưu để phát lại message trong stream.
* _work queue_ — stream hoạt động như shared queue, message bị xóa sau khi được consume — dùng cho exactly-once consumption.
* _interest_ — message được giữ chừng nào còn consumer chưa nhận. Là biến thể của work queue, chỉ giữ message nếu có consumer đang quan tâm đến subject của message.

> 🇬🇧 *Note that regardless of the retention policy selected, the limits (and the discard policy) _always_ apply.*

Lưu ý: dù chọn retention policy nào, các giới hạn (và discard policy) _luôn luôn_ được áp dụng.

**Biến đổi subject mapping**

> 🇬🇧 *JetStream also enables the ability to apply subject mapping transformations to messages as they are ingested into a stream.*

JetStream cũng cho phép áp dụng subject mapping transformation cho message khi chúng được đưa vào stream.

#### Lưu trữ phân tán bền vững và nhất quán

> 🇬🇧 *You can choose the durability as well as the resilience of the message storage according to your needs.*

Bạn có thể chọn độ bền lưu trữ và khả năng chịu lỗi phù hợp với nhu cầu:

* Lưu trữ trên bộ nhớ (Memory storage).
* Lưu trữ trên file (File storage).
* Replication (1 (không), 2, 3) giữa các NATS server để Fault Tolerance.

> 🇬🇧 *JetStream uses a NATS optimized RAFT distributed quorum algorithm to distribute the persistence service between NATS servers in a cluster while maintaining immediate consistency (as opposed to [eventual consistency](https://en.wikipedia.org/wiki/Eventual\_consistency)) even in the face of failures.*

JetStream sử dụng thuật toán RAFT distributed quorum được tối ưu hóa cho NATS để phân phối dịch vụ lưu trữ giữa các NATS server trong một cluster, đồng thời duy trì tính nhất quán tức thì (thay vì [eventual consistency](https://en.wikipedia.org/wiki/Eventual\_consistency)) ngay cả khi có lỗi xảy ra.

> 🇬🇧 *For writes (publications to a stream), the formal consistency model of NATS JetStream is [Linearizable](https://jepsen.io/consistency/models/linearizable). On the read side (listening to or replaying messages from streams) the formal models don't really apply because JetStream does not support atomic batching of multiple operations together (so the only kind of 'transaction' is the persisting, replicating and voting of a single operation on the stream) but in essence, JetStream is [serializable](https://jepsen.io/consistency/models/serializable) because messages are added to a stream in one global order (which you can control using compare and publish).*

Đối với ghi (publish lên stream), mô hình nhất quán chính thức của NATS JetStream là [Linearizable](https://jepsen.io/consistency/models/linearizable). Về phía đọc (lắng nghe hoặc phát lại message từ stream), các mô hình chính thức không thực sự áp dụng vì JetStream không hỗ trợ batching atomic nhiều thao tác cùng lúc (đơn vị "transaction" duy nhất là việc lưu trữ, replicate và vote cho một thao tác trên stream). Về bản chất, JetStream là [serializable](https://jepsen.io/consistency/models/serializable) vì message được thêm vào stream theo một thứ tự toàn cục duy nhất (có thể kiểm soát bằng compare and publish).

> 🇬🇧 *Do note, while we do guarantee immediate consistency when it comes to [monotonic writes](https://jepsen.io/consistency/models/monotonic-writes) and [monotonic reads](https://jepsen.io/consistency/models/monotonic-reads). We don't guarantee [read your writes](https://jepsen.io/consistency/models/read-your-writes) at this time, as reads through _direct get_ requests may be served by followers or mirrors. More consistent results can be achieved by sending get requests to the stream leader.*

Lưu ý: chúng tôi đảm bảo tính nhất quán tức thì với [monotonic writes](https://jepsen.io/consistency/models/monotonic-writes) và [monotonic reads](https://jepsen.io/consistency/models/monotonic-reads), nhưng chưa đảm bảo [read your writes](https://jepsen.io/consistency/models/read-your-writes), vì các request _direct get_ có thể được phục vụ bởi follower hoặc mirror. Để có kết quả nhất quán hơn, hãy gửi get request đến stream leader.

> 🇬🇧 *JetStream can also provide encryption at rest of the messages being stored.*

JetStream cũng có thể mã hóa message khi lưu trữ (encryption at rest).

> 🇬🇧 *In JetStream the configuration for storing messages is defined separately from how they are consumed. Storage is defined in a [_Stream_](./streams.md) and consuming messages is defined by multiple [_Consumers_](./consumers.md).*

Trong JetStream, cấu hình lưu trữ message được định nghĩa tách biệt với cách consume chúng. Lưu trữ được định nghĩa trong một [_Stream_](./streams.md), còn việc consume message được định nghĩa bởi nhiều [_Consumer_](./consumers.md).

**Hệ số replication của stream**

> 🇬🇧 *A stream's replication factor (R, often referred to as the number 'Replicas') determines how many places it is stored allowing you to tune to balance risk with resource usage and performance. A stream that is easily rebuilt or temporary might be memory-based with a R=1 and a stream that can tolerate some downtime might be file-based R-1.*

Hệ số replication của stream (R, thường gọi là số 'Replicas') xác định stream được lưu ở bao nhiêu nơi, giúp cân bằng rủi ro với tài nguyên và hiệu năng. Stream dễ rebuild hoặc tạm thời có thể dùng bộ nhớ với R=1; stream chịu được một khoảng downtime có thể dùng file với R=1.

> 🇬🇧 *Typical usage to operate in typical outages and balance performance would be a file-based stream with R=3. A highly resilient, but less performant and more expensive configuration is R=5, the replication factor limit.*

Để vận hành tốt trong các sự cố thông thường và cân bằng hiệu năng, cấu hình phổ biến là file-based stream với R=3. Cấu hình R=5 cho khả năng phục hồi cao nhất nhưng kém hiệu năng hơn và tốn chi phí hơn — đây là giới hạn replication factor.

> 🇬🇧 *Rather than defaulting to the maximum, we suggest selecting the best option based on the use case behind the stream. This optimizes resource usage to create a more resilient system at scale.*

Thay vì chọn giá trị tối đa mặc định, hãy chọn tùy vào use case cụ thể. Cách này tối ưu tài nguyên và tạo ra hệ thống có khả năng chịu lỗi tốt hơn ở quy mô lớn.

* Replicas=1 — Không hoạt động khi server phục vụ stream bị lỗi. Hiệu năng cao nhất.
* Replicas=2 — Không có lợi ích đáng kể hiện tại. Khuyến nghị dùng Replicas=3 thay thế.
* Replicas=3 — Chịu được mất một server. Cân bằng lý tưởng giữa rủi ro và hiệu năng.
* Replicas=4 — Không có lợi ích đáng kể hơn Replicas=3, trừ trường hợp cụm 5 node.
* Replicas=5 — Chịu được mất đồng thời hai server. Giảm thiểu rủi ro nhưng hiệu năng thấp hơn.

**Mirroring và Sourcing giữa các stream**

> 🇬🇧 *JetStream also allows server administrators to easily mirror streams, for example between different JetStream domains in order to offer disaster recovery. You can also define a stream that 'sources' from one or more other streams.*

JetStream cho phép admin server dễ dàng mirror stream, ví dụ giữa các JetStream domain khác nhau để hỗ trợ disaster recovery. Bạn cũng có thể định nghĩa stream "source" từ một hoặc nhiều stream khác.

**Đồng bộ dữ liệu xuống đĩa**

> 🇬🇧 *JetStream's file-based streams persist messages to disk. However, while JetStream does flush file writes to the OS synchronously, under the default configuration it does not immediately `fsync` data to disk. The server uses a configurable `sync_interval` option, with a default value of 2 minutes, which controls how often the server will `fsync` its data. The data will be `fsync`-ed no later than this interval. This has important consequences for durability with respect to OS failures (meaning ungraceful exit of the Operating System such as a power outage, and not just ungraceful exit or killing of the `nats-server` process itself):*

File-based stream của JetStream lưu message xuống đĩa. Tuy nhiên, dù JetStream flush file write xuống OS một cách đồng bộ, trong cấu hình mặc định nó không lập tức `fsync` dữ liệu xuống đĩa vật lý. Server dùng tùy chọn `sync_interval` có thể cấu hình được, mặc định là 2 phút, để kiểm soát tần suất `fsync` dữ liệu. Dữ liệu sẽ được `fsync`-ed chậm nhất sau khoảng thời gian này. Điều này có hậu quả quan trọng với độ bền dữ liệu khi OS gặp sự cố (ví dụ mất điện — không chỉ là process `nats-server` bị tắt không sạch):

> 🇬🇧 *In a non-replicated setup, an OS failure may result in data loss. A client might publish a message and receive an acknowledgment, but the data may not yet be safely stored to disk. As a result, after an OS failure recovery, a server may have lost recently acknowledged messages.*

Trong cấu hình không có replication, OS failure có thể gây mất dữ liệu. Client có thể đã publish message và nhận acknowledgment, nhưng dữ liệu chưa được lưu an toàn xuống đĩa. Do đó, sau khi OS khôi phục, server có thể mất các message đã được acknowledge gần đây.

> 🇬🇧 *In a replicated setup, a published message is acknowledged after it successfully replicated to at least a quorum of servers. However, replication alone is not enough to guarantee the strongest level of durability against multiple systemic failures.*

Trong cấu hình có replication, message được acknowledge sau khi replicate thành công đến ít nhất một quorum server. Tuy nhiên, replication đơn thuần chưa đủ để đảm bảo mức độ bền vững cao nhất khi xảy ra nhiều lỗi hệ thống cùng lúc.

- Nếu nhiều server lỗi đồng thời do OS failure, trước khi dữ liệu được `fsync`-ed, cluster có thể không khôi phục lại được các message đã acknowledge gần nhất.
- Nếu server bị lỗi mất dữ liệu cục bộ do OS failure, dù cực kỳ hiếm, có một số tổ hợp sự kiện khiến nó có thể rejoin cluster và tạo thành majority mới với các node chưa từng nhận hoặc lưu trữ một message nhất định. Cluster khi đó có thể tiếp tục với dữ liệu không đầy đủ, gây mất message đã được acknowledge.

> 🇬🇧 *Setting a lower `sync_interval` increases the frequency of disk writes, and reduces the window for potential data loss, but at the expense of performance. Additionally, setting `sync_interval: always` will make sure servers `fsync` after every message before it is acknowledged. This setting, combined with replication in different data centers or availability zones, provides the strongest durability guarantees but at the slowest performance.*

Đặt `sync_interval` thấp hơn giúp tăng tần suất ghi đĩa, thu hẹp cửa sổ mất dữ liệu tiềm ẩn, nhưng ảnh hưởng đến hiệu năng. Ngoài ra, đặt `sync_interval: always` sẽ đảm bảo server `fsync` sau mỗi message trước khi acknowledge. Kết hợp với replication ở các data center hoặc availability zone khác nhau, cấu hình này cho độ bền tốt nhất nhưng hiệu năng thấp nhất.

> 🇬🇧 *The default settings have been chosen to balance performance and risk of data loss in what we consider to be a typical production deployment scenario across multiple availability zones.*

Cài đặt mặc định được chọn để cân bằng hiệu năng và nguy cơ mất dữ liệu trong kịch bản triển khai production điển hình trên nhiều availability zone.

> 🇬🇧 *For example, consider a stream with 3 replicas deployed across three separate availability zones. For the stream state to diverge across nodes would require that:*

Ví dụ, xét một stream với 3 replica (bản sao dữ liệu) triển khai trên ba availability zone riêng biệt. Để trạng thái stream bị phân kỳ giữa các node, cần xảy ra đồng thời:

- Một trong 3 server đã offline, bị cô lập hoặc bị phân vùng.
- OS của server thứ hai bị lỗi, làm mất dữ liệu của các message chỉ có trên 2/3 node vì chưa được `fsync`-ed.
- stream leader thuộc nhóm 2/3 node trên bị down hoặc bị cô lập/phân vùng.
- Server đầu tiên trong partition ban đầu chưa nhận được dữ liệu khôi phục từ partition.
- Server bị OS-fail quay lại và tiếp xúc với server đầu tiên nhưng không với stream leader cũ.

> 🇬🇧 *In the end, 2 out of 3 nodes will be available, the previous stream leader with the writes will be unavailable, one server will have lost some writes due to the OS failure, and one server will have never seen these writes due to the earlier partition. The last two servers could then form a majority and accept new writes, essentially losing some of the former writes.*

Kết quả là 2/3 node khả dụng, stream leader cũ có dữ liệu đầy đủ lại không khả dụng, một server mất một số dữ liệu do OS failure, một server chưa bao giờ nhận được dữ liệu đó do partition trước đó. Hai server còn lại có thể tạo thành majority và chấp nhận write mới, về bản chất mất đi một phần dữ liệu đã ghi trước đó.

> 🇬🇧 *Importantly this is a failure condition where stream state could diverge, but in a system that is deployed across multiple availability zones, it would require multiple faults to align precisely in the right way.*

Đây là điều kiện lỗi có thể khiến trạng thái stream phân kỳ, nhưng trong hệ thống triển khai trên nhiều availability zone, cần nhiều lỗi căn chỉnh chính xác mới có thể xảy ra.

> 🇬🇧 *A potential mitigation to a failure of this kind is not automatically bringing back a server process that was OS-failed until it is known that a majority of the remaining servers have received the new writes, or by peer-removing the crashed server and admitting it as a new and wiped peer and allowing it to recover over the network from existing healthy nodes (although this could be expensive depending on the amount of data involved).*

Cách giảm thiểu rủi ro này là không tự động khởi động lại server bị OS-fail cho đến khi biết chắc majority các server còn lại đã nhận được dữ liệu mới, hoặc loại bỏ server bị crash ra khỏi peer và cho nó gia nhập lại như một peer mới (đã xóa sạch), để nó khôi phục qua mạng từ các node lành mạnh hiện có (dù cách này có thể tốn kém tùy lượng dữ liệu).

> 🇬🇧 *For use cases where minimizing loss is an absolute priority, `sync_interval: always` can of course still be configured, but note that this will have a server-wide performance impact that may affect throughput or latencies. For production environments, operators should evaluate whether the default is correct for their use case, target environment, costs, and performance requirements.*

Với các use case mà giảm thiểu mất mát dữ liệu là ưu tiên tuyệt đối, `sync_interval: always` vẫn có thể cấu hình được, nhưng lưu ý rằng điều này sẽ ảnh hưởng đến hiệu năng toàn server, có thể tác động đến throughput hoặc latency. Trong môi trường production, operator nên đánh giá liệu cài đặt mặc định có phù hợp với use case, môi trường đích, chi phí và yêu cầu hiệu năng của mình không.

> 🇬🇧 *Alternatively, a hybrid approach can be used where existing clusters still function under their default `sync_interval` settings but a new cluster gets added that's configured with `sync_interval: always`, and utilizes server tags. The placement of a stream can then be specified to have this stream store data on this higher durability cluster through the use of [placement tags](./streams.md#placement).*

Ngoài ra, có thể dùng cách tiếp cận lai: các cluster hiện tại vẫn hoạt động với cài đặt `sync_interval` mặc định, trong khi thêm một cluster mới được cấu hình với `sync_interval: always` và dùng server tag. Khi đó, placement của stream có thể được chỉ định để lưu dữ liệu trên cluster có độ bền cao hơn này thông qua [placement tags](./streams.md#placement).

```
# Configure a cluster that's dedicated to always sync writes.
server_tags: ["sync:always"]

jetstream {
    sync_interval: always
}
```

> 🇬🇧 *Create a replicated stream that's specifically placed in the cluster using `sync_interval: always`, to ensure the strongest durability only for stream writes that require this level of durability.*

Tạo một replicated stream được đặt cụ thể trong cluster bằng `sync_interval: always`, để đảm bảo độ bền cao nhất chỉ cho các stream write yêu cầu mức độ bền vững này.

```
nats stream add --replicas 3 --tag sync:always
```

#### Flow control tách rời

> 🇬🇧 *JetStream provides decoupled flow control over streams, the flow control is not 'end to end' where the publisher(s) are limited to publish no faster than the slowest of all the consumers (i.e. the lowest common denominator) can receive but is instead happening individually between each client application (publishers or consumers) and the nats server.*

JetStream cung cấp flow control tách rời trên các stream — không phải flow control "đầu-đến-cuối" giới hạn publisher không gửi nhanh hơn consumer chậm nhất, mà thay vào đó diễn ra riêng lẻ giữa mỗi ứng dụng client (publisher hoặc consumer) với NATS server.

> 🇬🇧 *When using the JetStream publish calls to publish to streams there is an acknowledgment mechanism between the publisher and the NATS server, and you have the choice of making synchronous or asynchronous (i.e. 'batched') JetStream publish calls.*

Khi dùng JetStream publish call để gửi lên stream, có cơ chế acknowledgment giữa publisher và NATS server. Bạn có thể chọn thực hiện JetStream publish call theo kiểu sync hoặc async (tức "batched").

> 🇬🇧 *On the subscriber side, the sending of messages from the NATS server to the client applications receiving or consuming messages from streams is also flow controlled.*

Về phía subscriber, việc gửi message từ NATS server đến các ứng dụng client nhận hoặc consume message từ stream cũng được flow control.

#### Exactly once semantics

> 🇬🇧 *Because publications to streams using the JetStream publish calls are acknowledged by the server the base quality of service offered by streams is '_at least once_', meaning that while reliable and normally duplicate free there are some specific failure scenarios that could result in a publishing application believing (wrongly) that a message was not published successfully and therefore publishing it again, and there are failure scenarios that could result in a client application's consumption acknowledgment getting lost and therefore in the message being re-sent to the consumer by the server. Those failure scenarios while being rare and even difficult to reproduce do exist and can result in perceived 'message duplication' at the application level.*

Vì các publication lên stream sử dụng JetStream publish call được server acknowledge, chất lượng dịch vụ cơ bản của stream là '_at least once_' — nghĩa là dù đáng tin cậy và thường không có bản sao, vẫn tồn tại các kịch bản lỗi hiếm gặp khiến ứng dụng publish tin rằng (nhầm) message chưa gửi được và gửi lại, hoặc acknowledgment của ứng dụng consume bị mất khiến server re-deliver message đến consumer. Các kịch bản này dù hiếm nhưng có tồn tại và có thể dẫn đến "message trùng lặp" ở tầng ứng dụng.

> 🇬🇧 *Therefore, JetStream also offers an '_exactly once_' quality of service. For the publishing side, it relies on the publishing application attaching a unique message or publication ID in a message header and on the server keeping track of those IDs for a configurable rolling period of time in order to detect the publisher publishing the same message twice. For the subscribers a _double_ acknowledgment mechanism is used to avoid a message being erroneously re-sent to a subscriber by the server after some kinds of failures.*

Vì vậy, JetStream cũng cung cấp chất lượng dịch vụ '_exactly once_'. Về phía publisher, cơ chế này dựa vào ứng dụng gắn một ID message/publication duy nhất vào header và server theo dõi các ID đó trong một khoảng thời gian rolling có thể cấu hình để phát hiện publisher gửi trùng. Về phía subscriber, cơ chế _double_ acknowledgment được dùng để tránh server re-deliver nhầm message đến subscriber sau một số loại lỗi.

#### Consumer

> 🇬🇧 *JetStream [consumers](./consumers.md) are 'views' on a stream, they are subscribed to (or pulled) by client applications to receive copies of (or to consume if the stream is set as a working queue) messages stored in the stream.*

JetStream [consumer](./consumers.md) là "góc nhìn" trên một stream — được client application subscribe (hoặc pull) để nhận bản sao (hoặc consume nếu stream được cấu hình là working queue) các message lưu trong stream.

**Fast push consumer**

> 🇬🇧 *Client applications can choose to use fast un-acknowledged `push` (ordered) consumers to receive messages as fast as possible (for the selected replay policy) on a specified delivery subject or to an inbox. Those consumers are meant to be used to 'replay' rather than 'consume' the messages in a stream.*

Ứng dụng client có thể dùng `push` (ordered) consumer không cần acknowledge để nhận message nhanh nhất có thể (theo replay policy đã chọn) trên một delivery subject hoặc inbox. Các consumer này dùng để "phát lại" chứ không phải "consume" message trong stream.

**Pull consumer có thể mở rộng ngang với batching**

> 🇬🇧 *Client applications can also use and share `pull` consumers that are demand-driven, support batching and must explicitly acknowledge message reception and processing which means that they can be used to consume (i.e. use the stream as a distributed queue) as well as process the messages in a stream.*

Ứng dụng client cũng có thể dùng và chia sẻ `pull` consumer theo kiểu demand-driven, hỗ trợ batching và phải acknowledge tường minh khi nhận và xử lý message — nghĩa là chúng có thể dùng để consume (tức dùng stream như distributed queue) cũng như xử lý message trong stream.

> 🇬🇧 *Pull consumers can and are meant to be shared between applications (just like queue groups) in order to provide easy and transparent horizontal scalability of the processing or consumption of messages in a stream without having (for example) to worry about having to define partitions or worry about fault-tolerance.*

Pull consumer có thể và được thiết kế để chia sẻ giữa các ứng dụng (giống như queue group) nhằm cung cấp khả năng mở rộng ngang dễ dàng và minh bạch cho việc xử lý hoặc consume message trong stream, mà không cần lo lắng về việc định nghĩa partition hay fault-tolerance.

> 🇬🇧 *Note: using pull consumers doesn't mean that you can't get updates (new messages published into the stream) 'pushed' in real-time to your application, as you can pass a (reasonable) timeout to the consumer's Fetch call and call it in a loop.*

Lưu ý: dùng pull consumer không có nghĩa là bạn không thể nhận cập nhật (message mới publish vào stream) theo thời gian thực, vì bạn có thể truyền một timeout hợp lý vào lệnh Fetch của consumer và gọi nó trong vòng lặp.

**Consumer acknowledgment**

> 🇬🇧 *While you can decide to use un-acknowledged consumers trading quality of service for the fastest possible delivery of messages, most processing is not idem-potent and requires higher qualities of service (such as the ability to automatically recover from various failure scenarios that could result in some messages not being processed or being processed more than once) and you will want to use acknowledged consumers. JetStream supports more than one kind of acknowledgment:*

Dù bạn có thể dùng consumer không cần acknowledge để đổi lấy tốc độ giao nhận tối đa, hầu hết xử lý không phải idempotent và cần chất lượng dịch vụ cao hơn (chẳng hạn tự động khôi phục từ các kịch bản lỗi khiến message không được xử lý hoặc bị xử lý nhiều lần). JetStream hỗ trợ nhiều loại acknowledgment:

* Một số consumer hỗ trợ acknowledge _tất cả_ message đến sequence number của message hiện tại; một số consumer cung cấp chất lượng dịch vụ cao nhất nhưng yêu cầu acknowledge từng message một cách tường minh, kèm theo thời gian tối đa server chờ acknowledgment trước khi re-deliver (đến process khác đang gắn vào consumer).
* Bạn cũng có thể gửi _negative_ acknowledgment.
* Thậm chí có thể gửi acknowledgment _in progress_ (báo hiệu đang xử lý và cần thêm thời gian trước khi ack hoặc nack).

### Key Value Store

> 🇬🇧 *The JetStream persistence layer enables the Key Value store: the ability to store, retrieve and delete `value` messages associated with a `key` into a `bucket`.*

Lớp lưu trữ JetStream cho phép Key Value store: khả năng lưu, truy xuất và xóa `value` message gắn với một `key` vào một `bucket`.

* [Concepts](./key-value-store)
* [Walkthrough](https://docs.nats.io/nats-concepts/jetstream/key-value-store/kv\_walkthrough)
* [API and details](../../using-nats/developing-with-nats/js/kv.md)

#### Watch và History

> 🇬🇧 *You can subscribe to changes in a Key Value on the bucket or individual key level with `watch` and optionally retrieve a `history` of the values (and deletions) that have happened on a particular key.*

Bạn có thể subscribe vào các thay đổi của Key Value ở cấp bucket hoặc từng key riêng lẻ bằng `watch`, và tùy chọn lấy `history` các giá trị (và lần xóa) đã xảy ra trên một key cụ thể.

#### Cập nhật atomic và locking

> 🇬🇧 *The Key Value store supports atomic `create` and `update` operations. This enables pessimistic locks (by creating a key and holding on to it) and optimistic locks (using CAS - compare and set).*

Key Value store hỗ trợ các thao tác `create` và `update` atomic. Điều này cho phép pessimistic lock (bằng cách tạo key và giữ nó) và optimistic lock (dùng CAS — compare and set).

### Object Store

> 🇬🇧 *The Object Store is similar to the Key Value Store. The key being replaced by a file name and value being designed to store arbitrarily large `objects` (e.g. files, even if they are very large) rather than 'values' that are message-sized (i.e. limited to 1Mb by default). This is achieved by chunking messages.*

Object Store tương tự Key Value Store, nhưng key được thay bằng tên file và value được thiết kế để lưu `objects` tùy ý lớn (ví dụ file dung lượng lớn) thay vì "value" có kích thước message (mặc định giới hạn 1MB). Điều này đạt được bằng cách chunking message.

* [Concepts](https://docs.nats.io/nats-concepts/jetstream/object-store/obj\_store)
* [Walkthrough](https://docs.nats.io/nats-concepts/jetstream/object-store/obj\_walkthrough)
* [API and details](../../using-nats/developing-with-nats/js/object.md)

## Legacy

> 🇬🇧 *Note that JetStream completely replaces the [STAN](https://docs.nats.io/legacy/stan) legacy NATS streaming layer.*

Lưu ý: JetStream thay thế hoàn toàn lớp streaming legacy [STAN](https://docs.nats.io/legacy/stan) của NATS.

## Thuật ngữ trong bài

- **async**: bất đồng bộ
- **cache**: bộ nhớ đệm
- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **leader**: server chính trong nhóm replica
- **message**: gói dữ liệu được gửi đi
- **node**: một server trong cluster
- **publisher**: bên gửi message
- **queue**: hàng đợi message
- **queue group**: nhóm subscribers chia sẻ tải
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **sync**: đồng bộ