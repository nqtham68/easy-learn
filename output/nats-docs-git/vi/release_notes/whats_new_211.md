---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/release_notes/whats_new_211
title: Điểm mới trong NATS 2.11
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# NATS 2.11

> 🇬🇧 *This guide is tailored for existing NATS users upgrading from NATS version v2.10.x. This will read as a summary with links to specific documentation pages to learn more about the feature or improvement.*

Tài liệu này dành cho người dùng NATS đang nâng cấp từ v2.10.x. Nội dung là bản tóm tắt kèm liên kết đến tài liệu chi tiết cho từng tính năng hoặc cải tiến.

## Tính năng

### Khả năng quan sát

> 🇬🇧 ***Distributed message tracing:** Users can now trace messages as they move through the system by setting a `Nats-Trace-Dest` header to an inbox subject. Servers on the message path will return events to the provided subject that report each time a message enters or leaves a server, by which connection type, when subject mappings occur, or when messages traverse an account import/export boundary. Additionally, the `Nats-Trace-Only` header (if set to true) will allow tracing events to propagate on a specific subject without delivering them to subscribers of that subject.*

* **Distributed message tracing:** Người dùng có thể theo dõi message (gói dữ liệu được gửi đi) khi nó di chuyển qua hệ thống bằng cách đặt header `Nats-Trace-Dest` trỏ đến một inbox subject (chuỗi định danh message). Các server trên đường đi của message sẽ gửi event về subject đã cung cấp, báo cáo mỗi lần message vào hoặc ra khỏi server, theo loại kết nối nào, khi nào xảy ra subject mapping, hoặc khi message vượt qua ranh giới import/export giữa các account. Ngoài ra, header `Nats-Trace-Only` (nếu đặt thành true) cho phép sự kiện tracing lan truyền trên một subject cụ thể mà không giao nhận đến subscriber của subject đó.

### Streams

> 🇬🇧 ***JetStream per-message TTLs:** It is now possible to age out individual messages using a per-message TTL. The `Nats-TTL` header, in either string or integer format (in seconds) allows for individual message expiration independent of stream limits. This can be combined with other limits in place on the stream. More information is available in [ADR-43](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-43.md).*

* **JetStream per-message TTLs:** Giờ đây có thể cho phép message hết hạn riêng lẻ bằng TTL theo từng message. Header `Nats-TTL` (định dạng string hoặc integer, tính bằng giây) cho phép từng message hết hạn độc lập với giới hạn của stream (luồng message lưu trữ liên tục). Tính năng này có thể kết hợp với các giới hạn khác đang áp dụng trên stream. Xem thêm tại [ADR-43](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-43.md).

> 🇬🇧 ***Subject delete markers on MaxAge:** The `SubjectDeleteMarkerTTL` stream configuration option now allows for the placement of delete marker messages in the stream when the configured `MaxAge` limit causes the last message for a given subject to be deleted. The delete markers include a `Nats-Marker-Reason` header explaining which limit was responsible for the deletion.*

* **Subject delete markers on MaxAge:** Tùy chọn cấu hình stream `SubjectDeleteMarkerTTL` nay cho phép đặt delete marker vào stream khi giới hạn `MaxAge` xóa message cuối cùng của một subject nhất định. Các delete marker bao gồm header `Nats-Marker-Reason` giải thích giới hạn nào chịu trách nhiệm xóa.

> 🇬🇧 ***Stream ingest rate limiting:** New options `max_buffered_size` and `max_buffered_msgs` in the `jetstream` configuration block enable rate limiting on Core NATS publishing into JetStream streams, protecting the system from overload.*

* **Stream ingest rate limiting:** Các tùy chọn mới `max_buffered_size` và `max_buffered_msgs` trong block cấu hình `jetstream` cho phép giới hạn tốc độ publish Core NATS vào JetStream stream, bảo vệ hệ thống khỏi quá tải.

### Consumers

> 🇬🇧 ***Pull consumer priority groups:** Pull consumers now support priority groups with pinning and overflow, enabling flexible failover and priority management when multiple clients are pulling from the same consumer. Configurable policies based on the number of pending messages on the consumer, or the number of pending acks, can control when messages overflow from one client to another, enabling new design patterns or regional awareness.*

* **Pull consumer priority groups:** Pull consumer (bên xử lý dữ liệu từ stream) nay hỗ trợ priority group với cơ chế pinning và overflow, giúp quản lý failover và độ ưu tiên linh hoạt khi nhiều client cùng kéo dữ liệu từ một consumer. Các policy có thể cấu hình dựa trên số lượng message đang chờ hoặc số ack đang chờ, kiểm soát thời điểm message overflow từ client này sang client khác — cho phép các pattern thiết kế mới hoặc nhận thức theo vùng địa lý.

> 🇬🇧 ***Consumer pausing:** Message delivery to consumers can be temporarily suspended using the new pause API endpoint (or the `PauseUntil` configuration option when creating), ideal for maintenance or migrations. Message delivery automatically resumes once the configured deadline has passed. Consumer clients continue to receive heartbeat messages as usual to ensure that they do not surface errors during the pause.*

* **Consumer pausing:** Việc giao nhận message đến consumer có thể tạm dừng bằng API endpoint (địa chỉ API cụ thể) pause mới (hoặc tùy chọn cấu hình `PauseUntil` khi khởi tạo), lý tưởng cho bảo trì hay migration. Message delivery tự động tiếp tục sau khi deadline đã cấu hình trôi qua. Consumer client vẫn tiếp tục nhận heartbeat message như thường để không phát sinh lỗi trong thời gian tạm dừng.

### Vận hành

> 🇬🇧 ***Replication traffic in asset accounts:** Raft replication traffic can optionally be moved into the same account in which replicated assets live on a per-account basis, rather than being sent and received in the system account using the new [`cluster_traffic` property ](../running-a-nats-service/configuration#jetstream-account-settings)in the JetStream account settings of an account. When combined with multiple route connections, this can help to reduce latencies and avoid head-of-line blocking issues that may occur in heavily-loaded multi-tenant or multi-account deployments.*

* **Replication traffic in asset accounts:** Raft replication traffic có thể chuyển tùy chọn vào cùng account chứa các asset được replicate theo từng account, thay vì gửi và nhận trong system account — sử dụng thuộc tính mới [`cluster_traffic`](../running-a-nats-service/configuration#jetstream-account-settings) trong JetStream account settings. Kết hợp với nhiều route connection, cách này giúp giảm latency và tránh head-of-line blocking trong các deployment multi-tenant hoặc multi-account tải cao.

> 🇬🇧 ***TLS first on leafnode connections:** A new `handshake_first` in the leafnode `tls` block allows setting up leafnode connections that perform TLS negotiation first, before any other protocol handshakes take place.*

* **TLS first on leafnode connections:** Tùy chọn mới `handshake_first` trong block `tls` của leafnode cho phép thiết lập kết nối leafnode thực hiện TLS negotiation trước, trước khi bất kỳ protocol handshake nào khác diễn ra.

> 🇬🇧 ***Configuration state digest:** A new `-t` command line flag on the server binary can generate a hash of the configuration file. The `config_digest` item in `varz` displays the hash of the currently running configuration file, making it possible to check whether a configuration file has changed on disk compared to the currently running configuration.*

* **Configuration state digest:** Flag dòng lệnh mới `-t` trên server binary có thể tạo hash của file cấu hình. Mục `config_digest` trong `varz` hiển thị hash của file cấu hình đang chạy, giúp kiểm tra xem file cấu hình trên đĩa có thay đổi so với cấu hình hiện tại hay không.

> 🇬🇧 ***TPM encryption on Windows:** When running on Windows, the filestore can now store encryption keys in the TPM, useful in environments where physical access may be a concern.*

* **TPM encryption on Windows:** Khi chạy trên Windows, filestore nay có thể lưu khóa mã hóa trong TPM, hữu ích trong môi trường cần quan tâm đến bảo mật vật lý.

### MQTT

> 🇬🇧 ***SparkplugB:** The built-in MQTT support is now compliant with SparkplugB Aware, with support for `NBIRTH` and `NDEATH` messages.*

* **SparkplugB:** Hỗ trợ MQTT tích hợp sẵn nay tuân thủ SparkplugB Aware, với hỗ trợ cho message `NBIRTH` và `NDEATH`.

## Cải tiến

> 🇬🇧 ***Replicated delete proposals:** Message removals in clustered interest-based or workqueue streams are now propagated via Raft to guarantee consistent removal order across replicas, reducing a number of possible ways that a cluster failure can result in de-synced streams.*

* **Replicated delete proposals:** Việc xóa message trong clustered interest-based hoặc workqueue stream nay được truyền qua Raft để đảm bảo thứ tự xóa nhất quán trên tất cả replica (bản sao dữ liệu), giảm thiểu các trường hợp cluster (cụm nhiều server chạy chung) gặp sự cố dẫn đến stream mất đồng bộ.

> 🇬🇧 ***Metalayer, stream and consumer consistency:** A new leader now only responds to read/write requests after synchronizing with its Raft log, preventing desynchronization between KV key updates and the stream during leader changes.*

* **Metalayer, stream and consumer consistency:** Leader (server chính trong nhóm replica) mới chỉ phản hồi các yêu cầu đọc/ghi sau khi đồng bộ với Raft log, ngăn chặn mất đồng bộ giữa cập nhật KV key và stream trong quá trình thay đổi leader.

> 🇬🇧 ***Replicated consumer reliability:** Replicated consumers now consistently redeliver unacknowledged messages after a leader change.*

* **Replicated consumer reliability:** Consumer được replicate nay re-deliver message chưa được ack một cách nhất quán sau khi leader thay đổi.

> 🇬🇧 ***Consumer starting sequence:** The consumer starting sequence is now always respected, except for internal hidden consumers for sources/mirrors.*

* **Consumer starting sequence:** Starting sequence của consumer nay luôn được tuân thủ, ngoại trừ các internal hidden consumer dành cho source/mirror.

## Lưu ý khi nâng cấp

#### Stream ingest rate limiting

> 🇬🇧 *The NATS Server can now return a 429 error with type `JSStreamTooManyRequests` when too many messages have been queued up for a stream. It should not generally be possible to hit this limit while using JetStream publishes and waiting for PubAcks, but may trigger if trying to publish into JetStream using Core NATS publishes without waiting for PubAcks, which is not advised.*

NATS Server nay có thể trả về lỗi 429 với type `JSStreamTooManyRequests` khi quá nhiều message được xếp hàng cho một stream. Thông thường không thể chạm giới hạn này khi dùng JetStream publish và chờ PubAck, nhưng có thể xảy ra nếu publish vào JetStream qua Core NATS mà không chờ PubAck — cách làm này không được khuyến nghị.

> 🇬🇧 *The new `max_buffered_size` and `max_buffered_msgs` options control how many messages can be queued for each stream before the rate limit is hit, therefore if needed, you can increase these limits on your deployments. The default values for `max_buffered_size` and `max_buffered_msgs` are 128MB and 10,000 respectively, whereas in v2.10 these were unlimited.*

Các tùy chọn mới `max_buffered_size` và `max_buffered_msgs` kiểm soát số message tối đa có thể xếp hàng cho mỗi stream trước khi đạt giới hạn. Nếu cần, bạn có thể tăng các giới hạn này trong deployment của mình. Giá trị mặc định cho `max_buffered_size` và `max_buffered_msgs` lần lượt là 128MB và 10.000, trong khi ở v2.10 hai giá trị này không giới hạn.

> 🇬🇧 *You can detect in the server logs whether running into a queue limit with the following warning:*

Bạn có thể phát hiện trong server log liệu có đang chạm giới hạn queue hay không qua cảnh báo sau:

```
[WRN] Dropping messages due to excessive stream ingest rate on 'account' > 'my-stream': IPQ len limit reached
```

> 🇬🇧 *If your application starts to log the above warnings then you can first try to increase the limits to higher values while investigating the fast publishers, for example:*

Nếu ứng dụng bắt đầu ghi log các cảnh báo trên, trước tiên hãy thử tăng giới hạn lên giá trị cao hơn trong khi điều tra các publisher gửi quá nhanh, ví dụ:

```
jetstream {
  max_buffered_msgs: 50000
  max_buffered_size: 256mib
}
```

#### Replicated delete proposals

> 🇬🇧 *Since stream deletes are now replicated through group proposals in a replicated stream, there may be a slight increase in replication traffic on this version.*

Vì xóa stream nay được replicate qua group proposal trong replicated stream, có thể có sự gia tăng nhỏ trong replication traffic ở phiên bản này.

#### JetStream healthcheck

> 🇬🇧 *The `js-server-only` healthcheck no longer checks for the health of the metaleader on v2.11.0. Since this healthcheck was designed to detect the server readiness (or in k8s for the readiness probe) checking the metaleader would sometimes cause a NATS server to be considered unhealthy when restarting the servers. In v2.11, this should no longer be an issue. If the previous behavior from v2.10 is preferred, there is a new healthcheck option `js-meta-only` which can be used to check whether the meta group is healthy.*

Healthcheck `js-server-only` không còn kiểm tra sức khỏe của metaleader trong v2.11.0. Vì healthcheck này được thiết kế để phát hiện server readiness (hoặc readiness probe trong k8s), việc kiểm tra metaleader đôi khi khiến NATS server bị coi là unhealthy khi đang khởi động lại. Trong v2.11, vấn đề này không còn xảy ra nữa. Nếu muốn giữ hành vi cũ từ v2.10, có thêm tùy chọn healthcheck `js-meta-only` để kiểm tra xem meta group có khỏe mạnh hay không.

#### Exit code

> 🇬🇧 *Earlier versions of the NATS Server would return an exit code 1 when gracefully shut down, i.e. after SIGTERM. From v2.11, an exit code of 0 (zero) will now be returned instead.*

Các phiên bản NATS Server trước đây trả về exit code 1 khi tắt bình thường (sau SIGTERM). Từ v2.11, exit code 0 (không) sẽ được trả về thay thế.

#### Server, cluster và gateway names

> 🇬🇧 *Configurations that have server, cluster, and gateway names with spaces are now considered invalid, as this can cause problems at the protocol level. A server running NATS v2.11 will fail to start with spaces configured in these names. Please ensure that spaces are not used in server, cluster or gateway names.*

Cấu hình có tên server, cluster và gateway chứa dấu cách nay bị coi là không hợp lệ, vì điều này có thể gây vấn đề ở tầng protocol. Server chạy NATS v2.11 sẽ không khởi động được nếu các tên này có dấu cách. Hãy đảm bảo không dùng dấu cách trong tên server, cluster hoặc gateway.

## Lưu ý khi hạ cấp

#### Stream state

> 🇬🇧 *When downgrading from v2.11 to v2.10, the stream state files on disk will be rebuilt due to a change in the format of these files in v2.11. This requires re-scanning all stream message blocks, which may use higher CPU than usual and will likely take longer for the restarted node to report healthy. This will only happen on the first restart after downgrading and will not result in data loss.*

Khi hạ cấp từ v2.11 xuống v2.10, các file stream state trên đĩa sẽ được xây dựng lại do thay đổi định dạng trong v2.11. Quá trình này yêu cầu quét lại toàn bộ stream message block, có thể tốn CPU cao hơn thông thường và node khởi động lại sẽ mất nhiều thời gian hơn trước khi báo cáo trạng thái healthy. Điều này chỉ xảy ra ở lần khởi động lại đầu tiên sau khi hạ cấp và sẽ không gây mất dữ liệu.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **endpoint**: địa chỉ API cụ thể
- **header**: phần metadata kèm theo
- **leader**: server chính trong nhóm replica
- **log**: bản ghi sự kiện
- **message**: gói dữ liệu được gửi đi
- **node**: một server trong cluster
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **TLS**: mã hóa TLS