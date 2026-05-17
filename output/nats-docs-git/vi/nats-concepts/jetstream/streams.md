---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/jetstream/streams
title: Streams (Luồng message lưu trữ liên tục)
translated: true
translated_at: '2026-05-13T00:00:00+00:00'
---

# Streams

> 🇬🇧 *Streams are message stores, each stream defines how messages are stored and what the limits (duration, size, interest) of the retention are. Streams consume normal [NATS subjects](../subjects.md), any message published on those subjects will be captured in the defined storage system. You can do a normal publish to the subject for unacknowledged delivery, though it's better to use the JetStream publish calls instead as the JetStream server will reply with an acknowledgement that it was successfully stored.*

Stream (luồng message lưu trữ liên tục) là nơi lưu trữ message, mỗi stream định nghĩa cách message được lưu và giới hạn retention (thời gian, kích thước, interest). Stream nhận message từ các [NATS subject](../subjects.md) thông thường — bất kỳ message nào được publish lên các subject đó đều được ghi vào hệ thống lưu trữ đã cấu hình. Có thể publish thông thường lên subject mà không cần acknowledgement, nhưng nên dùng JetStream publish call để server phản hồi xác nhận đã lưu thành công.

![Orders](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/streams-and-consumers-75p.png)

> 🇬🇧 *The diagram above shows the concept of storing all `ORDERS.*` in the Stream even though there are many types of order related messages. We'll show how you can selectively consume subsets of messages later. Relatively speaking the Stream is the most resource consuming component so being able to combine related data in this manner is important to consider.*

Sơ đồ trên minh họa việc lưu tất cả `ORDERS.*` vào cùng một Stream dù có nhiều loại message liên quan đến đơn hàng. Phần sau sẽ hướng dẫn cách consume (bên xử lý dữ liệu từ stream) có chọn lọc các tập con message. Nhìn chung, Stream tiêu tốn tài nguyên nhiều nhất, vì vậy khả năng gom dữ liệu liên quan vào một nơi là điều đáng cân nhắc kỹ.

> 🇬🇧 *Streams can consume many subjects. Here we have `ORDERS.*` but we could also consume `SHIPPING.state` into the same Stream should that make sense.*

Stream có thể nhận từ nhiều subject (chuỗi định danh message). Ở đây ta có `ORDERS.*`, nhưng hoàn toàn có thể gom thêm `SHIPPING.state` vào cùng Stream nếu phù hợp.

## Giới hạn stream và chính sách retention

> 🇬🇧 *Streams support various retention policies which define when messages in the stream can be automatically deleted, such as when stream limits are hit (like max count, size or age of messages), or also more novel options that apply on top of the limits such as interest-based retention or work-queue semantics (see [Retention Policy](#retentionpolicy)).*

Stream hỗ trợ nhiều retention policy xác định khi nào message được tự động xóa — ví dụ khi đạt giới hạn (số lượng, kích thước, hoặc tuổi message) — cũng như các tùy chọn nâng cao như retention dựa trên interest hoặc ngữ nghĩa work-queue (xem [Retention Policy](#retentionpolicy)).

> 🇬🇧 *Upon reaching message limits, the server will automatically discard messages either by removing the oldest messages to make room for new ones (`DiscardOld`) or by refusing to store new messages (`DiscardNew`). For more details, see [Discard Policy](#discardpolicy).*

Khi đạt giới hạn, server sẽ tự động discard message bằng cách xóa các message cũ nhất để nhường chỗ (`DiscardOld`) hoặc từ chối nhận message mới (`DiscardNew`). Xem thêm tại [Discard Policy](#discardpolicy).

> 🇬🇧 *Streams support deduplication using a `Nats-Msg-Id` header and a sliding window within which to track duplicate messages. See the [Message Deduplication](../../using-nats/jetstream/model_deep_dive.md#message-deduplication) section.*

Stream hỗ trợ loại trùng lặp (deduplication) qua header `Nats-Msg-Id` cùng một cửa sổ trượt để theo dõi message trùng. Xem phần [Message Deduplication](../../using-nats/jetstream/model_deep_dive.md#message-deduplication).

> 🇬🇧 *For examples on how to configure streams with your preferred NATS client, see [NATS by Example](https://natsbyexample.com).*

Ví dụ cấu hình stream với client NATS tùy chọn, xem tại [NATS by Example](https://natsbyexample.com).

## Cấu hình

> 🇬🇧 *Below are the set of stream configuration options that can be defined. The `Version` column indicates the version of the server the option was introduced. The `Editable` column indicates the option can be edited after the stream created. See client-specific examples [here](https://natsbyexample.com).*

Dưới đây là các tùy chọn cấu hình stream. Cột `Version` cho biết phiên bản server mà tùy chọn được giới thiệu. Cột `Editable` cho biết tùy chọn có thể chỉnh sửa sau khi stream đã được tạo. Xem ví dụ theo từng client [tại đây](https://natsbyexample.com).

| Field                                 | Description                                                                                                                                                                                                                                                                                               | Version | Editable             |
|:--------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------|:---------------------|
| Name                                  | Identifies the stream and has to be unique within JetStream account. Names cannot contain whitespace, `.`, `*`, `>`, path separators (forward or backwards slash), and non-printable characters.                                                                                                          | 2.2.0   | No                   |
| [Storage](#storagetype)               | The storage type for stream data.                                                                                                                                                                                                                                                                         | 2.2.0   | No                   |
| [Subjects](#subjects)                 | A list of subjects to bind. Wildcards are supported. Cannot be set for [mirror](#mirrors) streams.                                                                                                                                                                                                        | 2.2.0   | Yes                  |
| Replicas                              | How many replicas to keep for each message in a clustered JetStream, maximum 5.                                                                                                                                                                                                                           | 2.2.0   | Yes                  |
| MaxAge                                | Maximum age of any message in the Stream, expressed in nanoseconds.                                                                                                                                                                                                                                       | 2.2.0   | Yes                  |
| MaxBytes                              | Maximum number of bytes stored in the stream. Adheres to Discard Policy, removing oldest or refusing new messages if the Stream exceeds this size.                                                                                                                                                        | 2.2.0   | Yes                  |
| MaxMsgs                               | Maximum number of messages stored in the stream. Adheres to Discard Policy, removing oldest or refusing new messages if the Stream exceeds this number of messages.                                                                                                                                       | 2.2.0   | Yes                  |
| MaxMsgSize                            | The largest message that will be accepted by the Stream. The size of a message is a sum of payload and headers.                                                                                                                                                                                           | 2.2.0   | Yes                  |
| MaxConsumers                          | Maximum number of Consumers that can be defined for a given Stream, `-1` for unlimited.                                                                                                                                                                                                                   | 2.2.0   | No                   |
| NoAck                                 | Default `false`. Disables acknowledging messages that are received by the Stream. This is mandatory when archiving messages which have a reply subject set. E.g. requests in an Request/Reply communication. By default JetStream will acknowledge each message with an empty reply on the reply subject. | 2.2.0   | Yes                  |
| [Retention](#retentionpolicy)         | Declares the retention policy for the stream.                                                                                                                                                                                                                                                             | 2.2.0   | No                   |
| [Discard](#discardpolicy)             | The behavior of discarding messages when any streams' limits have been reached.                                                                                                                                                                                                                           | 2.2.0   | Yes                  |
| DuplicateWindow                       | The window within which to track duplicate messages, expressed in nanoseconds.                                                                                                                                                                                                                            | 2.2.0   | Yes                  |
| [Placement](#placement)               | Used to declare where the stream should be placed via tags and/or an explicit cluster name.                                                                                                                                                                                                               | 2.2.0   | Yes                  |
| [Mirror](#mirrors)                    | If set, indicates this stream is a mirror of another stream.                                                                                                                                                                                                                                              | 2.2.0   | Yes (since 2.12.0)   |
| [Sources](#stream-sources)            | If defined, declares one or more streams this stream will source messages from.                                                                                                                                                                                                                           | 2.2.0   | Yes                  |
| MaxMsgsPerSubject                     | Limits maximum number of messages in the stream to retain _per subject_.                                                                                                                                                                                                                                  | 2.3.0   | Yes                  |
| Description                           | A verbose description of the stream.                                                                                                                                                                                                                                                                      | 2.3.3   | Yes                  |
| Sealed                                | Sealed streams do not allow messages to be deleted via limits or API, sealed streams can not be unsealed via configuration update. Can only be set on already created streams via the Update API.                                                                                                         | 2.6.2   | Yes (once)           |
| DenyDelete                            | Restricts the ability to delete messages from a stream via the API.                                                                                                                                                                                                                                       | 2.6.2   | No                   |
| DenyPurge                             | Restricts the ability to purge messages from a stream via the API.                                                                                                                                                                                                                                        | 2.6.2   | No                   |
| [AllowRollup](#allowrollup)           | Allows the use of the `Nats-Rollup` header to replace all contents of a stream, or subject in a stream, with a single new message.                                                                                                                                                                        | 2.6.2   | Yes                  |
| [RePublish](#republish)               | If set, messages stored to the stream will be immediately _republished_ to the configured subject.                                                                                                                                                                                                        | 2.8.3   | Yes                  |
| AllowDirect                           | If true, and the stream has more than one replica, each replica will respond to _direct get_ requests for individual messages, not only the leader.                                                                                                                                                       | 2.9.0   | Yes                  |
| MirrorDirect                          | If true, and the stream is a mirror, the mirror will participate in a serving _direct get_ requests for individual messages from origin stream.                                                                                                                                                           | 2.9.0   | Yes                  |
| DiscardNewPerSubject                  | If true, applies discard new semantics on a per subject basis. Requires `DiscardPolicy` to be `DiscardNew` and the `MaxMsgsPerSubject` to be set.                                                                                                                                                         | 2.9.0   | Yes                  |
| Metadata                              | A set of application-defined key-value pairs for associating metadata on the stream.                                                                                                                                                                                                                      | 2.10.0  | Yes                  |
| Compression                           | If file-based and a compression algorithm is specified, the stream data will be compressed on disk. Valid options are nothing (empty string) or `s2` for Snappy compression.                                                                                                                              | 2.10.0  | Yes                  |
| FirstSeq                              | If specified, a new stream will be created with its initial sequence set to this value.                                                                                                                                                                                                                   | 2.10.0  | No                   |
| [SubjectTransform](#subjecttransform) | Applies a subject transform (to matching messages) before storing the message.                                                                                                                                                                                                                            | 2.10.0  | Yes                  |
| ConsumerLimits                        | Sets default limits for consumers created for a stream. Those can be overridden per consumer.                                                                                                                                                                                                             | 2.10.0  | Yes                  |
| AllowMsgTTL                           | If set, allows header initiated per-message TTLs, instead of relying solely on MaxAge.                                                                                                                                                                                                                    | 2.11.0  | No (can only enable) |
| SubjectDeleteMarkerTTL                | If set, a subject delete marker will be placed after the last message of a subject ages out. This defines the TTL of the delete marker that's left behind.                                                                                                                                                | 2.11.0  | Yes                  |
| AllowAtomicPublish                    | If set, allows atomically writing a batch of N messages into the stream.                                                                                                                                                                                                                                  | 2.12.0  | Yes                  |
| AllowBatchPublish                     | If set, allows writing a batch of N messages into the stream.                                                                                                                                                                                                                                             | 2.14.0  | Yes                  |
| AllowMsgCounter                       | If set, the stream will function as a counter stream, hosting distributed counter CRDTs.                                                                                                                                                                                                                  | 2.12.0  | No                   |
| AllowMsgSchedules                     | If set, allows message scheduling in the stream.                                                                                                                                                                                                                                                          | 2.12.0  | No (can only enable) |

### StorageType

> 🇬🇧 *The storage types include:*
> 🇬🇧 *- `File` (default) - Uses file-based storage for stream data.*
> 🇬🇧 *- `Memory` - Uses memory-based storage for stream data.*

Các loại storage bao gồm:

- `File` (mặc định) - Lưu dữ liệu stream trên file.
- `Memory` - Lưu dữ liệu stream trên memory.

### Subjects

> 🇬🇧 *Note: a stream configured as a [mirror](#mirrors) cannot be configured with a set of subjects. A mirror implicitly sources a subset of the origin stream (optionally with a filter), but does not subscribe to additional subjects.*

_Lưu ý: stream được cấu hình là [mirror](#mirrors) không thể đồng thời khai báo danh sách subject. Mirror mặc nhiên nhận từ một tập con của origin stream (có thể kèm bộ lọc), nhưng không subscribe thêm subject nào khác._

> 🇬🇧 *If no explicit subject is specified, the default subject will be the same name as the stream. Multiple subjects can be specified and edited over time. Note, if messages are stored by a stream on a subject that is subsequently removed from the stream config, consumers will still observe those messages if their subject filter overlaps.*

Nếu không khai báo subject nào, subject mặc định sẽ trùng với tên stream. Có thể khai báo nhiều subject và chỉnh sửa theo thời gian. Lưu ý: nếu một subject bị xóa khỏi config stream nhưng stream đã lưu message trên subject đó, consumer vẫn nhìn thấy các message đó nếu bộ lọc subject khớp.

### RetentionPolicy

> 🇬🇧 *The retention options include:*

Các tùy chọn retention bao gồm:

- `LimitsPolicy` (mặc định) - Retention dựa trên các giới hạn đã đặt: `MaxMsgs`, `MaxBytes`, `MaxAge`, và `MaxMsgsPerSubject`. Giới hạn nào đạt trước sẽ kích hoạt tự động xóa message tương ứng. Xem [ví dụ đầy đủ][limits-example].
- `WorkQueuePolicy` - Retention theo kiểu FIFO queue. Mỗi message chỉ được consume một lần — được đảm bảo bằng cách chỉ cho phép _một_ consumer _mỗi subject_ trên work-queue stream (tức các bộ lọc subject của consumer không được chồng lên nhau). Sau khi message được ack, nó sẽ bị xóa khỏi stream. Xem [ví dụ đầy đủ][workqueue-example].
- `InterestPolicy` - Retention dựa trên _interest_ của consumer đối với stream và message. Khi không có consumer nào được định nghĩa, mọi message publish vào stream sẽ bị xóa ngay lập tức vì không có ai _quan tâm_. Điều này có nghĩa là consumer phải được bind vào stream trước khi message được publish. Sau khi message được ack bởi _tất cả_ consumer lọc trên subject đó, message bị xóa (tương tự `WorkQueuePolicy`). Xem [ví dụ đầy đủ][interest-example].

> **⚠️ Cảnh báo:**
> Khi chọn `InterestPolicy` hoặc `WorkQueuePolicy` cho stream, các giới hạn đã đặt vẫn được áp dụng. Ví dụ với work-queue stream, nếu `MaxMsgs` được đặt và discard policy mặc định là _old_, message sẽ bị tự động xóa dù consumer chưa nhận.

> **ℹ️ Thông tin:**
> Với `InterestPolicy` stream, khi một consumer bị xóa — thủ công hoặc tự động khi hết `InactiveThreshold` — và đó là consumer cuối cùng đánh dấu interest trên tập subject đó, server có thể không xóa ngay tất cả message thuộc tập subject đó vì lý do hiệu năng. Thay vào đó, việc xóa có thể được hoãn đến khi các message đó đến đầu stream.

> **ℹ️ Thông tin:**
> Stream `WorkQueuePolicy` chỉ xóa message khi đạt giới hạn hoặc khi message đã được consumer `Ack’d` thành công. Message đã thử re-delivery và đạt `MaxDeliver` lần vẫn tồn tại trong stream và phải xóa thủ công qua JetStream API.

[limits-example]: <a href="https://natsbyexample.com/examples/jetstream/limits-stream/go"><a href="https://natsbyexample.com/examples/jetstream/limits-stream/go"><a href="https://natsbyexample.com/examples/jetstream/limits-stream/go">https://natsbyexample.com/examples/jetstream/limits-stream/go</a></a></a>
[interest-example]: <a href="https://natsbyexample.com/examples/jetstream/interest-stream/go"><a href="https://natsbyexample.com/examples/jetstream/interest-stream/go"><a href="https://natsbyexample.com/examples/jetstream/interest-stream/go">https://natsbyexample.com/examples/jetstream/interest-stream/go</a></a></a>
[workqueue-example]: <a href="https://natsbyexample.com/examples/jetstream/workqueue-stream/go"><a href="https://natsbyexample.com/examples/jetstream/workqueue-stream/go"><a href="https://natsbyexample.com/examples/jetstream/workqueue-stream/go">https://natsbyexample.com/examples/jetstream/workqueue-stream/go</a></a></a>

### DiscardPolicy

> 🇬🇧 *The discard behavior applies only for streams that have at least one limit defined. The options include:*

Hành vi discard chỉ áp dụng cho stream có ít nhất một giới hạn được khai báo. Các tùy chọn bao gồm:

- `DiscardOld` (mặc định) - Xóa message cũ nhất để duy trì giới hạn. Ví dụ, nếu `MaxAge` được đặt là một phút, server sẽ tự động xóa message cũ hơn một phút.
- `DiscardNew` - Từ chối _message mới_ nếu việc thêm vào sẽ _vượt_ một trong các giới hạn. Mở rộng của policy này là `DiscardNewPerSubject` áp dụng hành vi trên theo từng subject trong stream.

### Placement

> 🇬🇧 *Refers to the placement of the stream assets (data) within a NATS deployment, be it a single cluster or a supercluster. A given stream, including all replicas (not mirrors), are bound to a single cluster. So when creating or moving a stream, a cluster will be chosen to host the assets.*

Placement xác định vị trí dữ liệu stream trong một NATS deployment — dù là một cluster (cụm nhiều server chạy chung) đơn lẻ hay supercluster. Một stream cùng toàn bộ replica (không tính mirror) được gắn với một cluster duy nhất. Khi tạo hoặc di chuyển stream, một cluster sẽ được chọn để lưu trữ dữ liệu.

> 🇬🇧 *Without declaring explicit placement for a stream, by default, the stream will be created within the cluster that the client is connected to assuming it has sufficient storage available.*

Nếu không khai báo placement, stream mặc định được tạo trong cluster mà client đang kết nối, với điều kiện cluster đó có đủ dung lượng lưu trữ.

> 🇬🇧 *By declaring stream placement, where these assets are located can be controlled explicitly. This is generally useful to co-locate with the most active clients (publishers or consumers) or may be required for data sovereignty reasons.*

Khai báo placement cho phép kiểm soát rõ ràng vị trí lưu trữ — hữu ích khi cần đặt gần các client hoạt động nhiều nhất (publisher hoặc consumer) hoặc đáp ứng yêu cầu về chủ quyền dữ liệu.

> 🇬🇧 *Placement is supported in all client SDKs as well as the CLI. For example, adding a stream via the CLI to place a stream in a specific cluster looks like this:*

Placement được hỗ trợ trong tất cả client SDK cũng như CLI. Ví dụ, tạo stream bằng CLI và chỉ định cluster cụ thể:

```
nats stream add --cluster aws-us-east1-c1
```

> 🇬🇧 *For this to work, all servers in a given cluster must define the `name` field within the [`cluster`][cluster-config] server configuration block.*

Để điều này hoạt động, tất cả server trong cluster phải khai báo trường `name` trong khối config server [`cluster`][cluster-config].

```
cluster {
  name: aws-us-east1-c1
  # etc..
}
```

> 🇬🇧 *If you have multiple clusters that form a supercluster, then each is required to have a different name.*

Nếu có nhiều cluster tạo thành một supercluster, mỗi cluster phải có tên khác nhau.

> 🇬🇧 *Another placement option are _tags_. Each server can have its own set of tags, [defined in configuration][tag-config], typically describing properties of geography, hosting provider, sizing tiers, etc. In addition, tags are often used in conjunction with the `jetstream.unique_tag` config option to ensure that replicas must be placed on servers having _different_ values for the tag.*

Tùy chọn placement khác là _tag_. Mỗi server có thể có tập tag riêng, [khai báo trong config][tag-config], thường mô tả vị trí địa lý, nhà cung cấp hosting, tầng tài nguyên, v.v. Ngoài ra, tag thường dùng kết hợp với tùy chọn config `jetstream.unique_tag` để đảm bảo các replica (bản sao dữ liệu) được đặt trên các server có _giá trị tag khác nhau_.

> 🇬🇧 *For example, a server A, B, and C in the above cluster might all the same configuration except for the availability zone they are deployed to.*

Ví dụ, server A, B và C trong cluster trên có thể có cùng cấu hình, chỉ khác nhau ở availability zone được deploy.

```
// Server A
server_tags: ["cloud:aws", "region:us-east1", "az:a"]

jetstream: {
  unique_tag: "az"
}

// Server B
server_tags: ["cloud:aws", "region:us-east1", "az:b"]

jetstream: {
  unique_tag: "az"
}

// Server C
server_tags: ["cloud:aws", "region:us-east1", "az:c"]

jetstream: {
  unique_tag: "az"
}
```

> 🇬🇧 *Now we can create a stream by using tags, for example indicating we want a stream in us-east1.*

Giờ ta có thể tạo stream bằng tag, ví dụ chỉ định stream ở us-east1:

```
nats stream add --tag region:us-east1
```

> 🇬🇧 *If we had a second cluster in Google Cloud with the same region tag, the stream could be placed in either the AWS or GCP cluster. However, the `unique_tag` constraint ensures each replica will be placed in a different AZ in the cluster that was selected implicitly by the placement tags.*

Nếu có cluster thứ hai trên Google Cloud với cùng region tag, stream có thể được đặt ở cluster AWS hoặc GCP. Tuy nhiên, ràng buộc `unique_tag` đảm bảo mỗi replica được đặt ở AZ khác nhau trong cluster đã được chọn ngầm qua placement tag.

> 🇬🇧 *Although less common, note that both the cluster _and_ tags can be used for placement. This would be used if a single cluster contains servers have different properties.*

Ít phổ biến hơn, nhưng có thể dùng cả cluster _và_ tag cho placement — trường hợp này hữu ích khi một cluster chứa các server có đặc điểm khác nhau.

[cluster-config]: <a href="https://docs.nats.io/running-a-nats-service/configuration/clustering/cluster_config"><a href="https://docs.nats.io/running-a-nats-service/configuration/clustering/cluster_config"><a href="https://docs.nats.io/running-a-nats-service/configuration/clustering/cluster_config">https://docs.nats.io/running-a-nats-service/configuration/clustering/cluster_config</a></a></a>
[tag-config]: <a href="https://docs.nats.io/running-a-nats-service/configuration#cluster-configuration-monitoring-and-tracing"><a href="https://docs.nats.io/running-a-nats-service/configuration#cluster-configuration-monitoring-and-tracing"><a href="https://docs.nats.io/running-a-nats-service/configuration#cluster-configuration-monitoring-and-tracing">https://docs.nats.io/running-a-nats-service/configuration#cluster-configuration-monitoring-and-tracing</a></a></a>

### Sources và Mirrors

> 🇬🇧 *When a stream is configured with a `source` or `mirror`, it will automatically and asynchronously replicate messages from the origin stream. There are several options when declaring the configuration.*

Khi stream được cấu hình với `source` hoặc `mirror`, stream đó sẽ tự động và bất đồng bộ sao chép message từ origin stream. Có nhiều tùy chọn khi khai báo cấu hình này.

> 🇬🇧 *A source or mirror stream can have its own retention policy, replication, and storage type. Changes to the source or mirror, e.g. deleting messages or publishing, do not reflect on the origin stream.*

Stream source hoặc mirror có thể có retention policy, replication và storage type riêng. Các thay đổi trên source hoặc mirror — như xóa message hay publish — không ảnh hưởng đến origin stream.

> **ℹ️ Thông tin:**
> `Sources` là dạng tổng quát hóa của `Mirror` và cho phép nhận dữ liệu từ một hoặc nhiều stream đồng thời. Khuyến nghị dùng `Sources` cho các cấu hình mới.
> Nếu cần stream đích hoạt động như read-only replica:
> - Cấu hình stream không có listen subject **hoặc**
> - Tạm thời vô hiệu hóa listen subject qua client authorization.

#### Stream sources

> 🇬🇧 *A stream defining `Sources` is a generalized replication mechanism and allows for sourcing data from one or more streams concurrently as well as allowing direct write/publish by clients. Essentially the source streams and client writes are aggregated into a single interleaved stream. Subject transformation and filtering allow for powerful data distribution architectures.*

Stream khai báo `Sources` là cơ chế replication tổng quát, cho phép nhận dữ liệu từ một hoặc nhiều stream đồng thời đồng thời vẫn cho phép client ghi/publish trực tiếp. Về cơ bản, stream source và các lần ghi của client được gộp thành một stream duy nhất xen kẽ nhau. Subject transformation và filtering cho phép xây dựng kiến trúc phân phối dữ liệu mạnh mẽ.

#### Mirrors

> 🇬🇧 *A mirror can source its messages from exactly one stream and a clients can not directly write to the mirror. Although messages cannot be published to a mirror directly by clients, messages can be deleted on-demand (beyond the retention policy), and consumers have all capabilities available on regular streams.*

Mirror chỉ có thể nhận message từ đúng một stream và client không thể ghi trực tiếp vào mirror. Dù không publish trực tiếp vào mirror, vẫn có thể xóa message theo yêu cầu (ngoài retention policy), và consumer có đầy đủ khả năng như trên stream thông thường.

**Xem thêm:**
* [Source and Mirror](./source_and_mirror.md)


### AllowRollup

> 🇬🇧 *If enabled, the `AllowRollup` stream option allows for a published message having a `Nats-Rollup` header indicating all prior messages should be purged. The scope of the _purge_ is defined by the header value, either `all` or `sub`.*

Khi được bật, tùy chọn stream `AllowRollup` cho phép một message được publish kèm header `Nats-Rollup` để chỉ định toàn bộ message trước đó nên bị purge. Phạm vi _purge_ được xác định bởi giá trị header: `all` hoặc `sub`.

> 🇬🇧 *The `Nats-Rollup: all` header will purge all prior messages in the stream. Whereas the `sub` value will purge all prior messages for a given subject.*

Header `Nats-Rollup: all` sẽ purge toàn bộ message trước đó trong stream. Còn giá trị `sub` chỉ purge message trước đó của một subject cụ thể.

> 🇬🇧 *A common use case for rollup is for state snapshots, where the message being published has accumulated all the necessary state from the prior messages, relative to the stream or a particular subject.*

Một use case phổ biến của rollup là snapshot trạng thái — message mới được publish đã tích lũy đầy đủ trạng thái từ các message trước đó, theo phạm vi stream hoặc một subject cụ thể.

### RePublish

> 🇬🇧 *If enabled, the `RePublish` stream option will result in the server re-publishing messages received into a stream automatically and immediately after a successful write, to a distinct destination subject.*

Khi được bật, tùy chọn stream `RePublish` khiến server tự động re-publish ngay lập tức các message nhận vào stream — sau khi ghi thành công — đến một destination subject riêng biệt.

> 🇬🇧 *For high scale needs where, currently, a dedicated consumer may add too much overhead, clients can establish a core NATS subscription to the destination subject and receive messages that were appended to the stream in real-time.*

Với các hệ thống cần throughput cao, khi dùng consumer chuyên dụng có thể tốn quá nhiều overhead, client có thể subscribe trực tiếp lên destination subject qua core NATS và nhận message được thêm vào stream theo thời gian thực.

> 🇬🇧 *The fields for configuring republish include:*

Các trường cấu hình republish bao gồm:

- `Source` - Pattern subject tùy chọn, là tập con của các subject bind vào stream. Mặc định là tất cả message trong stream, ví dụ `>`.
- `Destination` - Subject đích mà message sẽ được re-publish đến. Source và destination phải là [subject mapping](../subject_mapping.md) hợp lệ.
- `HeadersOnly` - Nếu true, nội dung message sẽ không được đưa vào message re-publish, chỉ có thêm header `Nats-Msg-Size` cho biết kích thước message tính bằng byte.

> 🇬🇧 *For each message that is republished, a set of [headers](./headers.md) are automatically added.*

Với mỗi message được re-publish, một tập [header](./headers.md) sẽ được tự động thêm vào.

> 🇬🇧 ***Note:**  The `reply-subject` is being removed on republished messages, even if `no-ack` is set on the stream.*

**Lưu ý:** `reply-subject` bị xóa khỏi message re-publish, dù `no-ack` đã được đặt trên stream.

### SubjectTransform

> 🇬🇧 *If configured, the `SubjectTransform` will perform a subject transform to matching subjects of messages received by the stream and transform the subject, before storing it in the stream. The transform configuration specifies a `Source` and `Destination` field, following the rules of [subject transform](../../running-a-nats-service/configuration/configuring_subject_mapping.md).*

Khi được cấu hình, `SubjectTransform` sẽ thực hiện biến đổi subject cho các message khớp nhận vào stream — trước khi lưu. Cấu hình transform chỉ định trường `Source` và `Destination`, tuân theo quy tắc của [subject transform](../../running-a-nats-service/configuration/configuring_subject_mapping.md).

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)