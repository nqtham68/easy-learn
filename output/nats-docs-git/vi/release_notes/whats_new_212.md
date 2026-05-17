---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/release_notes/whats_new_212
title: Có gì mới trong NATS 2.12
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# NATS 2.12

> 🇬🇧 *This guide is tailored for existing NATS users upgrading from NATS version v2.11.x. This will read as a summary with links to specific documentation pages to learn more about the feature or improvement.*

Hướng dẫn này dành cho người dùng NATS đang nâng cấp từ v2.11.x. Nội dung trình bày dưới dạng tóm tắt, kèm link đến các trang tài liệu chi tiết cho từng tính năng hoặc cải tiến.

## Tính năng mới

### Stream

> 🇬🇧 *__Atomic batch publish:__ The `AllowAtomicPublish` stream configuration option allows to atomically publish N messages into a stream. This includes support for replicated and non-replicated streams, as well as doing per-message consistency checks prior to committing the batch. More information is available in [ADR-50](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-50.md).*

- **Atomic batch publish:** Tùy chọn config stream (luồng message lưu trữ liên tục) `AllowAtomicPublish` cho phép publish N message vào stream một cách atomic. Tính năng này hỗ trợ cả stream có replica (bản sao dữ liệu) và không có replica, đồng thời kiểm tra tính nhất quán từng message trước khi commit batch. Xem thêm tại [ADR-50](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-50.md).

> 🇬🇧 *__Distributed Counter CRDT:__ The `AllowMsgCounter` stream configuration option allows increment/decrement counter semantics on a stream. These counter streams can also be mirrored or aggregated through stream mirroring and sourcing. More information is available in [ADR-49](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-49.md)*

- **Distributed Counter CRDT:** Tùy chọn config stream `AllowMsgCounter` cho phép áp dụng ngữ nghĩa tăng/giảm bộ đếm trên một stream. Các counter stream này cũng có thể được mirror hoặc tổng hợp thông qua stream mirroring và sourcing. Xem thêm tại [ADR-49](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-49.md).

> 🇬🇧 *__Delayed Message Scheduling:__ The `AllowMsgSchedules` stream configuration option allows the scheduling of messages. Users can use this feature for delayed publishing/scheduling of messages. More information is available in [ADR-51](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-51.md)*

- **Delayed Message Scheduling:** Tùy chọn config stream `AllowMsgSchedules` cho phép lên lịch gửi message. Tính năng này hữu ích khi cần publish message theo lịch trễ. Xem thêm tại [ADR-51](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-51.md).

### Consumer

> 🇬🇧 *__Prioritized pull consumer policy:__ In addition to the consumer policies like overflow or client pinning, a new `prioritized` policy has been added. In contrast with the overflow policy, this allows a consumer to receive messages sooner instead of delaying failover, but at the cost of potentially flip-flopping work between clients. More information is available in [ADR-42](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-42.md#prioritized-policy)*

- **Prioritized pull consumer policy:** Ngoài các policy hiện có như overflow hay client pinning, consumer (bên xử lý dữ liệu từ stream) nay có thêm policy `prioritized`. Khác với overflow policy, policy này cho phép consumer nhận message sớm hơn thay vì chờ failover, nhưng đổi lại có thể gây tình trạng phân tán công việc qua lại giữa các client. Xem thêm tại [ADR-42](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-42.md#prioritized-policy).

### Vận hành

> 🇬🇧 *__Server metadata:__ Similar to `server_tags` which contains a set of tags describing the server, `server_metadata` is a map containing string keys and values describing metadata of the server.*

- **Server metadata:** Tương tự `server_tags` chứa tập hợp các tag mô tả server, `server_metadata` là một map với các cặp key-value kiểu string mô tả metadata của server.

> 🇬🇧 *__Promoting mirrors:__ A stream that's mirroring can now be promoted to be the primary, enabling new disaster recovery methodology. The current primary stream should be deleted or have its configured subjects removed prior to promoting mirrors, before configuring the promoted mirrors to start listening on those subjects.*

- **Promoting mirrors:** Một stream đang mirror nay có thể được nâng cấp thành primary, mở ra phương pháp disaster recovery mới. Trước khi promote, cần xóa stream primary hiện tại hoặc gỡ bỏ các subject (chuỗi định danh message) đã cấu hình trên đó, sau đó mới cấu hình stream được promote để lắng nghe trên các subject đó.

> 🇬🇧 *__Exponential backoff on route and gateway connections:__ Cluster routes and gateways can now use exponential backoff on reconnection attempts by setting `connect_backoff`. If `true`, will start exponential backoff at 1 second up to 30 seconds. This can slow down the speed of reconnection but significantly reduces the amount of DNS queries and general connection attempts during server restarts or outages.*

- **Exponential backoff cho route và gateway:** Các cluster (cụm nhiều server chạy chung) route và gateway nay có thể dùng exponential backoff khi thử kết nối lại bằng cách đặt `connect_backoff`. Nếu `true`, backoff sẽ bắt đầu từ 1 giây và tăng tối đa đến 30 giây. Cách này làm chậm tốc độ kết nối lại nhưng giảm đáng kể số lượng DNS query và lần thử kết nối trong quá trình khởi động lại server hoặc khi có sự cố.

> 🇬🇧 *__Offline assets:__ When downgrading to an older version, the server can now recognize new features were used and puts the stream and/or consumer into an unsupported/offline mode. For more information, read also the downgrade considerations. More information is available in [ADR-44](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-44.md#offline-assets)*

- **Offline assets:** Khi hạ cấp xuống phiên bản cũ hơn, server nay nhận biết được các tính năng mới đã được sử dụng và đưa stream và/hoặc consumer vào chế độ unsupported/offline. Xem thêm phần downgrade considerations và [ADR-44](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-44.md#offline-assets).

> 🇬🇧 *__Stream/consumer scaleup and reset disk/state protection:__ The server now has better protections against leader elections based on empty state. This also improves reliability of replicated in-memory streams. Usually a quorum of servers needs to be online and contain data. Now all but one server can be restarted and the in-memory stream's data can reliably be caught back up. However, during such a scenario all servers involved with replication of that stream will need to be available, not just what's needed for quorum. This lets the servers decide the best course of action to preserve all data.*

- **Bảo vệ khi scale-up và reset disk/state cho stream/consumer:** Server nay có cơ chế bảo vệ tốt hơn chống lại việc bầu chọn leader (server chính trong nhóm replica) dựa trên trạng thái rỗng. Điều này cũng cải thiện độ tin cậy của các in-memory stream có replica. Thông thường, một quorum server phải online và có dữ liệu. Nay tất cả server trừ một có thể khởi động lại và dữ liệu của in-memory stream sẽ được đồng bộ lại đáng tin cậy. Tuy nhiên, trong tình huống đó, tất cả server tham gia vào việc replication của stream đó phải sẵn sàng, không chỉ số lượng đủ quorum. Điều này cho phép các server tự quyết định phương án tốt nhất để bảo toàn dữ liệu.

## Cải tiến

> 🇬🇧 *__Async stream flushing:__ Replicated streams will now asynchronously flush data to the underlying store on disk, resulting in a significant improvement in performance. Writes to a replicated stream are still persisted synchronously in the Raft log prior to committing them, so the improved performance has no downsides with respect to consistency.*

- **Async stream flushing:** Các stream có replica nay flush dữ liệu xuống store trên disk theo kiểu async (bất đồng bộ), giúp cải thiện đáng kể hiệu năng. Các write vào stream có replica vẫn được lưu đồng bộ vào Raft log trước khi commit, nên hiệu năng tốt hơn không ảnh hưởng đến tính nhất quán.

> 🇬🇧 *__Elastic pointers in the filestore:__ File-based streams now use elastic pointers for its write-through caches. This allows the server to better respond during garbage collection, these caches can be evicted early to avoid out-of-memory conditions (see upgrade considerations below).*

- **Elastic pointers trong filestore:** Các stream dựa trên file nay sử dụng elastic pointer cho write-through cache. Nhờ đó, server phản ứng tốt hơn trong quá trình garbage collection — các cache có thể được giải phóng sớm để tránh tình trạng hết bộ nhớ (xem upgrade considerations bên dưới).

> 🇬🇧 *__Use cipher suites from `crypto/tls`:__ New cipher suites are now automatically added. Additionally, insecure cipher suites are disabled by default, but can be allowed when enabling `allow_insecure_cipher_suites`.*

- **Sử dụng cipher suite từ `crypto/tls`:** Các cipher suite mới giờ được tự động thêm vào. Ngoài ra, các cipher suite không an toàn bị vô hiệu hóa theo mặc định, nhưng có thể bật lại khi kích hoạt `allow_insecure_cipher_suites`.

> 🇬🇧 *__System events for the `$G` account:__ The global account (`$G`) will now also produce system events, such as connect and disconnect events.*

- **System event cho account `$G`:** Global account (`$G`) nay cũng tạo ra các system event như connect và disconnect.

> 🇬🇧 *__`GOMAXPROCS` and `GOMEMLIMIT` in server stats:__ The server stats already contained the CPU and memory usage of the server but now also contains the effective Go limits.*

- **`GOMAXPROCS` và `GOMEMLIMIT` trong server stats:** Server stats đã có thông tin CPU và memory usage, nay bổ sung thêm các Go limit hiệu lực.

> 🇬🇧 *__New subject transforms: `partition(n)` and `random(n)`:__ In addition to `partition(n, …)` which allows to determine a partition number based on tokens at specified indices, `partition(n)` and `random(n)` are convenience functions to create a partition or random number up to `n` based on the whole subject.*

- **Subject transform mới: `partition(n)` và `random(n)`:** Bên cạnh `partition(n, …)` dùng để xác định số partition dựa trên token tại các vị trí chỉ định, `partition(n)` và `random(n)` là các hàm tiện ích tạo số partition hoặc số ngẫu nhiên đến `n` dựa trên toàn bộ subject.

> 🇬🇧 *__Account name and user logging:__ Any logging related to a client connection, for example when reaching maximum connections or for authentication errors, will now include the account name and user of that client connection.*

- **Log account name và user:** Mọi log liên quan đến kết nối client — ví dụ khi đạt giới hạn kết nối tối đa hoặc lỗi xác thực — nay đều bao gồm tên account và user của kết nối đó.

> 🇬🇧 *__Logging improvements:__ Any logging related to a client connection now includes the account and user name. Connection closed logging now includes the remote server name.*

- **Cải tiến logging:** Log liên quan đến kết nối client nay bao gồm tên account và user. Log đóng kết nối nay cũng bao gồm tên server từ xa.

> 🇬🇧 *__Isolated leaf node property:__ In a large deployment with lots of leaf nodes, propagating east-west interest can result in a lot of traffic, which is wasted if leaf nodes don't need to be able to publish/subscribe to each other directly. Instead of the workaround of setting the cluster name of those leaf nodes to be the same, the `isolate_leafnode_interest` property can now be used.*

- **Isolated leaf node property:** Trong một deployment lớn với nhiều leaf node, việc lan truyền interest theo chiều ngang có thể tạo ra lượng traffic lớn — gây lãng phí nếu các leaf node không cần publish/subscribe trực tiếp với nhau. Thay vì dùng workaround là đặt cùng tên cluster cho các leaf node đó, nay có thể dùng thuộc tính `isolate_leafnode_interest`.

> 🇬🇧 *__Disable leaf node connection through config reload:__ This allows disabling a remote leaf node using configuration reload, when using `disabled: true`. If changed from false to true, a solicited leaf node will be disconnected and will not reconnect. If changed from true to false, the leafnode will be solicited again.*

- **Vô hiệu hóa kết nối leaf node qua config reload:** Tính năng này cho phép vô hiệu hóa một remote leaf node bằng cách reload config, khi dùng `disabled: true`. Nếu thay đổi từ false sang true, leaf node đang kết nối sẽ bị ngắt và không kết nối lại. Nếu đổi từ true sang false, leaf node sẽ được kết nối trở lại.

## Lưu ý khi nâng cấp

#### Mức sử dụng bộ nhớ

> 🇬🇧 *With the new elastic pointers in the filestore, it is expected that a NATS Server running 2.12 may show a different memory usage pattern to before. In some systems this may result in lower resident set size (RSS) reported, in others it may result in higher, depending on the number of assets and publish/access patterns.*

Với elastic pointer mới trong filestore, NATS Server chạy 2.12 có thể hiển thị mức sử dụng bộ nhớ khác so với trước. Trên một số hệ thống, RSS (resident set size) có thể thấp hơn; trên hệ thống khác có thể cao hơn — tùy thuộc vào số lượng asset và pattern publish/truy cập.

> 🇬🇧 *For the first time, the server will be able to respond to memory pressure by freeing filestore caches on demand and returning the memory to the operating system. This reduces the chance that sudden spikes in utilisation will result in an out-of-memory (OOM) kill. However, this means that the server can more optimistically retain caches in memory when available resources allow in order to facilitate improved read access times.*

Lần đầu tiên, server có thể phản ứng với tình trạng áp lực bộ nhớ bằng cách giải phóng filestore cache theo nhu cầu và trả bộ nhớ về cho hệ điều hành. Điều này giảm nguy cơ bị OOM kill khi có đột biến tải. Ngược lại, server cũng có thể giữ cache trong bộ nhớ tích cực hơn khi tài nguyên cho phép, nhằm cải thiện thời gian đọc.

> 🇬🇧 *This behaviour is largely controlled by the GC thresholds as set by the `GOMEMLIMIT` [environment variable](https://tip.golang.org/doc/gc-guide#Memory_limit). You may wish to tune this value in your environment based on available system memory, or in the case of Kubernetes environments, memory reservations.*

Hành vi này được kiểm soát chủ yếu bởi ngưỡng GC được đặt qua [biến môi trường](https://tip.golang.org/doc/gc-guide#Memory_limit) `GOMEMLIMIT`. Bạn có thể điều chỉnh giá trị này dựa trên bộ nhớ hệ thống, hoặc trong môi trường Kubernetes, dựa trên memory reservation.

#### Strict JetStream API

> 🇬🇧 *Starting from version v2.11, the server would start logging the following statement if an invalid JetStream request was received:*

Từ phiên bản v2.11, server bắt đầu ghi log câu thông báo sau khi nhận được JetStream request không hợp lệ:

```  
[WRN] Invalid JetStream request '$G > $JS.API.STREAM.CREATE.test-stream': json: unknown field "unknown"  
```

> 🇬🇧 *Starting from version v2.12, the server will not only log, but also return an error to the client as "strict mode" is now enabled by default. This means invalid JetStream requests will be rejected by default.*

Từ phiên bản v2.12, server không chỉ ghi log mà còn trả về lỗi cho client vì "strict mode" nay được bật mặc định. Điều này có nghĩa là các JetStream request không hợp lệ sẽ bị từ chối theo mặc định.

> 🇬🇧 *If the above log message is observed, please make sure that the application or client is sending correct requests to the server and that NATS client libraries are up-to-date. Strict mode can be temporarily disabled in the server configuration, allowing you more time to fix the issue:*

Nếu thấy thông báo log trên, hãy đảm bảo ứng dụng hoặc client đang gửi request đúng định dạng và các NATS client library đã được cập nhật. Strict mode có thể tạm thời vô hiệu hóa trong config server để có thêm thời gian khắc phục:

```  
jetstream {  
  strict: false  
}  
```

## Lưu ý khi hạ cấp

#### Trạng thái stream

> 🇬🇧 *When downgrading from v2.12 to v2.11, the stream state files on disk will be rebuilt due to a change in the format of these files in v2.12. This requires re-scanning all stream message blocks, which may use higher CPU than usual and will likely take longer for the restarted node to report healthy. This will only happen on the first restart after downgrading and will not result in data loss.*

Khi hạ cấp từ v2.12 xuống v2.11, các file stream state trên disk sẽ được xây dựng lại do thay đổi định dạng trong v2.12. Quá trình này yêu cầu quét lại toàn bộ message block của stream, có thể sử dụng CPU cao hơn thường và node (một server trong cluster) khởi động lại có thể mất thêm thời gian để báo trạng thái healthy. Điều này chỉ xảy ra lần đầu sau khi hạ cấp và không gây mất dữ liệu.

> 🇬🇧 *When downgrading, only downgrade to v2.11.9 or higher. Starting from this version, the server will recognize the use of new v2.12 features and will safely put the stream and/or consumer that uses these new features into an unsupported/offline mode. Importantly, this will both protect the data as well as the server itself from accessing unsupported features or data.*

Khi hạ cấp, chỉ hạ xuống v2.11.9 trở lên. Từ phiên bản này, server nhận biết được việc sử dụng các tính năng mới của v2.12 và đưa stream và/hoặc consumer dùng các tính năng đó vào chế độ unsupported/offline một cách an toàn. Điều này vừa bảo vệ dữ liệu, vừa ngăn server truy cập vào các tính năng hoặc dữ liệu không được hỗ trợ.

## Thuật ngữ trong bài

- **async**: bất đồng bộ
- **backoff**: chiến lược chờ tăng dần giữa các lần retry
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **leader**: server chính trong nhóm replica
- **message**: gói dữ liệu được gửi đi
- **node**: một server trong cluster
- **partition**: phần dữ liệu được chia ra
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)