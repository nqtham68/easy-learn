---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/release_notes/whats_new_214
title: Điểm mới trong NATS 2.14
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# NATS 2.14

> 🇬🇧 *This guide is tailored for existing NATS users upgrading from NATS version v2.12.x. This will read as a summary with links to specific documentation pages to learn more about the feature or improvement.*

Tài liệu này dành cho người dùng NATS đang nâng cấp từ phiên bản v2.12.x. Nội dung là tóm tắt các thay đổi, kèm link đến trang tài liệu chi tiết cho từng tính năng hoặc cải tiến.

## Tính năng mới

### Streams

> 🇬🇧 ***Fast batch publish:** The `AllowBatchPublish` stream configuration option allows for high throughput and flow controlled publishing into a stream. This includes support for replicated and non-replicated streams, as well as doing per-message consistency checks without intermediate staging of messages (like with atomic batch publish). More information is available in [ADR-50](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-50.md#fast-ingest-batch-publishing).*

- **Fast batch publish:** Tùy chọn cấu hình stream (luồng message lưu trữ liên tục) `AllowBatchPublish` cho phép publish vào stream với thông lượng cao và có flow control. Hỗ trợ cả replicated và non-replicated stream, đồng thời kiểm tra tính nhất quán từng message mà không cần staging trung gian (như với atomic batch publish). Xem thêm tại [ADR-50](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-50.md#fast-ingest-batch-publishing).

> 🇬🇧 ***Recurring schedules:** The `AllowMsgSchedules` stream configuration option now also allows the usage of recurring schedules, either based on a simple interval, or with Cron. More information is available in [ADR-51](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-51.md#cron-like-schedules).*

- **Recurring schedules:** Tùy chọn config (cấu hình) stream `AllowMsgSchedules` giờ đây hỗ trợ lịch lặp lại, có thể dùng interval đơn giản hoặc cú pháp Cron. Xem thêm tại [ADR-51](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-51.md#cron-like-schedules).

> 🇬🇧 ***Scheduled subject sampling:** The `AllowMsgSchedules` stream configuration option now also allows to source the data of the last message matching the subject in the scheduled message. Useful for downsampling data on an interval. More information is available in [ADR-51](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-51.md#subject-sampling).*

- **Scheduled subject sampling:** Tùy chọn config stream `AllowMsgSchedules` giờ đây cho phép lấy dữ liệu từ message cuối cùng khớp với subject (chuỗi định danh message) trong scheduled message. Hữu ích khi cần downsample dữ liệu theo interval. Xem thêm tại [ADR-51](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-51.md#subject-sampling).

> 🇬🇧 ***Reliable WorkQueue and Interest mirroring/sourcing:** Sourcing or mirroring from a WorkQueue or Interest retention stream is now supported. A durable consumer, as opposed to an ephemeral one, will automatically be used to perform the async replication. A new ack policy of `AckFlowControl` is used to acknowledge messages after they were persisted, based on flow control. More information is available in [ADR-60](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-60.md), see also the upgrade considerations below.*

- **Reliable WorkQueue và Interest mirroring/sourcing:** Đã hỗ trợ sourcing hoặc mirroring từ WorkQueue hoặc Interest retention stream. Một durable consumer (bên xử lý dữ liệu từ stream) — thay vì ephemeral — sẽ tự động được dùng để thực hiện async replication. Ack policy mới `AckFlowControl` dùng để xác nhận message sau khi đã được lưu trữ, dựa trên flow control. Xem thêm tại [ADR-60](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-60.md), cũng như lưu ý nâng cấp bên dưới.

### Consumers

> 🇬🇧 ***Consumer reset API:** Consumer delivery state can now be reset back to the acknowledgement floor, or to an arbitrary sequence (while still respecting start sequences etc). The consumer state after reset equals what would otherwise be a consumer delete and recreate at a specific starting sequence. More information is available in [ADR-60](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-60.md#consumer-delivery-state-reset-api).*

- **Consumer reset API:** Trạng thái delivery của consumer giờ có thể được reset về acknowledgement floor, hoặc về một sequence tùy ý (vẫn tuân thủ start sequence, v.v.). Trạng thái sau khi reset tương đương với việc xóa và tạo lại consumer tại một sequence bắt đầu cụ thể. Xem thêm tại [ADR-60](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-60.md#consumer-delivery-state-reset-api).

### Operations

> 🇬🇧 ***Leafnode remote config reload:** The leaf node remotes section can now be added and removed via a configuration reload, without requiring a server restart.*

- **Leafnode remote config reload:** Phần cấu hình remotes của leaf node giờ có thể thêm hoặc xóa thông qua configuration reload, không cần khởi động lại server.

> 🇬🇧 ***Filestore I/O error handling:** Previously, not all filestore I/O errors were properly handled, allowing the stream and server to continue to run. These errors will now be surfaced in the logs and show up in the health check, as well as freeze the stream to prevent further updates (see upgrade considerations below).*

- **Xử lý lỗi I/O của filestore:** Trước đây, không phải tất cả lỗi I/O của filestore đều được xử lý đúng cách, khiến stream và server vẫn tiếp tục chạy. Các lỗi này giờ sẽ xuất hiện trong log và hiển thị trong health check, đồng thời stream sẽ bị đóng băng để ngăn cập nhật thêm (xem lưu ý nâng cấp bên dưới).

> 🇬🇧 ***Raft overrun protection:** The server now recognizes if its Raft layer is being overrun by proposals, bounding the number of memory and disk resources the server is allowed to use during such an event (see upgrade considerations below).*

- **Raft overrun protection:** Server giờ nhận biết được khi lớp Raft bị quá tải bởi các proposal, từ đó giới hạn lượng tài nguyên bộ nhớ và đĩa được phép sử dụng trong tình huống đó (xem lưu ý nâng cấp bên dưới).

## Cải tiến

> 🇬🇧 ***Deduplication changes when using stream sourcing:** Streams with sources now allow deduplication to be disabled. Additionally, sourcing streams can now perform deduplication when fanning in multiple sources.*

- **Thay đổi deduplication khi dùng stream sourcing:** Stream có sources giờ cho phép tắt deduplication. Ngoài ra, sourcing stream giờ có thể thực hiện deduplication khi fan-in nhiều source.

> 🇬🇧 ***Atomic batch publish, EOB commit support:** Atomic batches can now be committed through an EOB (End of Batch) message without persisting this final message. This is also supported when using the new fast batch publish.*

- **Atomic batch publish, hỗ trợ EOB commit:** Atomic batch giờ có thể được commit qua message EOB (End of Batch) mà không cần lưu trữ message cuối đó. Tính năng này cũng được hỗ trợ khi dùng fast batch publish mới.

> 🇬🇧 ***Scheduled subject rollups:** The `Nats-Schedule-Rollup` header can now be used to place a rollup on the scheduled message, similar to the `Nats-Schedule-TTL` header.*

- **Scheduled subject rollups:** Header `Nats-Schedule-Rollup` giờ có thể dùng để đặt rollup trên scheduled message, tương tự header `Nats-Schedule-TTL`.

> 🇬🇧 ***Feature flags:** The server now supports a `feature_flags` field in the config which allows users to opt-in or opt-out to specific fixes or improvements prior to them becoming the default in a future release.*

- **Feature flags:** Server giờ hỗ trợ field `feature_flags` trong config, cho phép người dùng opt-in hoặc opt-out các bản vá hoặc cải tiến cụ thể trước khi chúng trở thành mặc định trong bản phát hành tương lai.

> 🇬🇧 ***Domain-aware acknowledgement and flow control subjects:** The server now supports both v1 and v2 of the consumer acknowledgement and flow control subjects. More information is available in [ADR-15](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-15.md#jsack).*

- **Domain-aware acknowledgement và flow control subjects:** Server giờ hỗ trợ cả v1 và v2 của consumer acknowledgement và flow control subjects. Xem thêm tại [ADR-15](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-15.md#jsack).

> 🇬🇧 ***Traceparent header:** The `traceparent` header is no longer modified by the message tracing.*

- **Traceparent header:** Header `traceparent` giờ không còn bị chỉnh sửa bởi message tracing.

> 🇬🇧 ***Asynchronous stream state snapshots for replicated streams:** Allows stream state snapshots to be taken and written without pausing stream processing, improving tail latencies. This is particularly impactful in cases where the stream has a large number of interior deletes.*

- **Snapshot trạng thái stream bất đồng bộ cho replicated stream:** Cho phép lấy và ghi snapshot trạng thái stream mà không cần dừng xử lý, cải thiện tail latency. Đặc biệt có tác động lớn khi stream có nhiều interior delete.

## Lưu ý khi nâng cấp

#### Reliable WorkQueue và Interest mirroring/sourcing

> 🇬🇧 *Version 2.14 adds support for sourcing and mirroring from WorkQueue or Interest streams. During an upgrade or downgrade, the server could temporarily log the following message:*

Phiên bản 2.14 bổ sung hỗ trợ sourcing và mirroring từ WorkQueue hoặc Interest stream. Trong quá trình nâng cấp hoặc hạ cấp, server có thể tạm thời ghi log (bản ghi sự kiện) sau:

```
[WRN] Invalid JetStream request '$G > $JS.API.CONSUMER.CREATE.O': json: unknown field "sourcing"
```

> 🇬🇧 *This means that an upgraded server tried to create the 'new-style' sourcing consumer but the older target server didn't recognize it and logged a warning. The upgraded server will automatically respond to this error and will send the request again using the 'old-style' sourcing consumer. It is expected that these logs could temporarily occur during upgrades/downgrades, but these should resolve once the whole system is upgraded.*

Điều này có nghĩa là server đã nâng cấp cố tạo sourcing consumer kiểu mới nhưng server đích phiên bản cũ không nhận ra và ghi warning. Server đã nâng cấp sẽ tự động phản hồi lỗi này và gửi lại request dùng sourcing consumer kiểu cũ. Các log này có thể tạm thời xuất hiện trong quá trình nâng cấp/hạ cấp và sẽ tự biến mất sau khi toàn bộ hệ thống được nâng cấp xong.

#### Domain-aware acknowledgement và flow control subjects

> 🇬🇧 *The server now supports both v1 and v2 acknowledgement and flow control reply subjects documented in [ADR-15](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-15.md#jsack). The v2 format includes a domain and account hash to deconflict stream and consumer names across domains and accounts:*

Server giờ hỗ trợ cả định dạng v1 và v2 cho acknowledgement và flow control reply subjects được ghi lại trong [ADR-15](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-15.md#jsack). Định dạng v2 bổ sung domain và account hash để tránh xung đột tên stream và consumer giữa các domain và account:

```
v1: $JS.ACK.<stream name>.<consumer name>.<num delivered>.<stream sequence>.<consumer sequence>.<timestamp>.<num pending>
v2: $JS.ACK.<domain>.<account hash>.<stream name>.<consumer name>.<num delivered>.<stream sequence>.<consumer sequence>.<timestamp>.<num pending>
```

> 🇬🇧 *While both v1 and v2 formats will be supported starting from 2.14, v1 remains the default. However, in version 2.15 the default will change to be the v2 format. Users that have defined account imports/exports or subject permissions containing the `$JS.ACK.<stream>.>` or `$JS.FC.<stream>.>` (or more granular) subjects **will be required to update their ACLs and/or account imports/exports before the 2.15 release** to allow the same stream and consumer names to be used in different domains or accounts without them conflicting with each other.*

Cả hai định dạng v1 và v2 đều được hỗ trợ từ phiên bản 2.14, nhưng v1 vẫn là mặc định. Tuy nhiên, trong phiên bản 2.15, mặc định sẽ chuyển sang định dạng v2. Người dùng đã định nghĩa account imports/exports hoặc subject permissions chứa `$JS.ACK.<stream>.>` hoặc `$JS.FC.<stream>.>` (hoặc chi tiết hơn) **sẽ phải cập nhật ACL và/hoặc account imports/exports trước khi phát hành 2.15** để cho phép dùng cùng tên stream và consumer trong các domain hoặc account khác nhau mà không bị xung đột.

> 🇬🇧 *If you have not defined such account imports/exports or subject permissions, for example if you use JetStream only within a single account, or you defined them as the "catch-all wildcard" `$JS.ACK.>` or `$JS.FC.>` then you will not need to make any changes. The default will change in version 2.15 and there should be no impact.*

Nếu bạn chưa định nghĩa account imports/exports hay subject permissions như vậy — ví dụ nếu chỉ dùng JetStream trong một account duy nhất, hoặc đã định nghĩa chúng dưới dạng "catch-all wildcard" `$JS.ACK.>` hoặc `$JS.FC.>` — thì sẽ không cần thay đổi gì. Mặc định sẽ thay đổi trong phiên bản 2.15 và không ảnh hưởng đến bạn.

> 🇬🇧 *To ease the migration path, the server now supports feature flags to test and enable this at your own convenience. Not specifying the feature flag means "use the server default" which for 2.14 will be the v1 format. Setting it to `true` will use the v2 format (also the v1 format will still be supported) and setting it to `false` will use the v1 format but still support v2.*

Để hỗ trợ quá trình migration, server giờ hỗ trợ feature flags để kiểm tra và bật tính năng này theo lịch tùy ý. Không chỉ định feature flag nghĩa là "dùng mặc định của server" — với 2.14 là định dạng v1. Đặt thành `true` sẽ dùng định dạng v2 (v1 vẫn được hỗ trợ), đặt thành `false` sẽ dùng v1 nhưng vẫn hỗ trợ v2.

```
feature_flags {
  js_ack_fc_v2: true
}
```

#### Xử lý lỗi I/O của filestore

> 🇬🇧 *Previously, not all filestore I/O errors were appropriately handled, allowing the stream and server to continue to run. In 2.14, these errors are surfaced: an affected stream freezes, logs the error, and reports an unhealthy state in health checks. Other streams on the same server remain unaffected, and for replicated streams another replica picks up the work transparently.*

Trước đây, không phải tất cả lỗi I/O của filestore đều được xử lý đúng, khiến stream và server vẫn tiếp tục chạy. Trong 2.14, các lỗi này được phơi bày: stream bị ảnh hưởng sẽ bị đóng băng, ghi log lỗi và báo trạng thái unhealthy trong health check. Các stream khác trên cùng server không bị ảnh hưởng, và với replicated stream, một replica (bản sao dữ liệu) khác sẽ tự động tiếp quản công việc.

> 🇬🇧 *This change introduces a new operational condition to watch for: if I/O errors are encountered, each stream affected by it will stop making progress. NATS core traffic is not affected by I/O errors, so the server keeps functioning, but will require a restart to recover from these I/O issues. This condition can be observed by the health check failing and reporting an I/O related error, the error message will contain `write error` and which error was encountered.*

Thay đổi này đưa vào một điều kiện vận hành mới cần theo dõi: nếu gặp lỗi I/O, mỗi stream bị ảnh hưởng sẽ ngừng tiến trình. NATS core traffic không bị ảnh hưởng bởi lỗi I/O nên server vẫn tiếp tục hoạt động, nhưng sẽ cần khởi động lại để khôi phục. Tình trạng này có thể nhận biết qua health check thất bại và báo lỗi liên quan đến I/O — message lỗi sẽ chứa `write error` và mô tả lỗi đã xảy ra.

#### Raft overrun protection

> 🇬🇧 *A new back-pressure mechanism in the Raft consensus layer prevents unbounded memory growth in overloaded clusters. In prior versions, there could be situations where entries would be written to the Raft write-ahead log faster than they could be committed and applied, resulting in increased memory and disk usage.*

Cơ chế back-pressure mới trong lớp Raft consensus ngăn bộ nhớ tăng không giới hạn trong cluster (cụm nhiều server chạy chung) bị quá tải. Trong các phiên bản trước, có thể xảy ra tình huống các entry được ghi vào Raft write-ahead log nhanh hơn tốc độ commit và apply, dẫn đến tăng mức sử dụng bộ nhớ và đĩa.

> 🇬🇧 *In 2.14, this condition is recognized and gives the relevant servers room to catch up. Leaders that detect they are falling behind step down so that a healthier peer can take over. If a majority of peers are equally overloaded, the system remains in this degraded state. The protection is a safety net for transient overload, not a substitute for adequate capacity, but it will allow the system to continue in a degraded but functional mode instead of allowing the system to become overloaded further.*

Trong 2.14, tình trạng này được nhận biết và cho phép các server liên quan có thời gian bắt kịp. Các leader (server chính trong nhóm replica) phát hiện mình đang tụt hậu sẽ nhường quyền để một peer khỏe mạnh hơn tiếp quản. Nếu đa số peer đều bị quá tải tương đương, hệ thống sẽ ở lại trạng thái degraded này. Đây là lưới an toàn cho trường hợp quá tải tạm thời, không phải thay thế cho capacity đủ dùng — nhưng sẽ cho phép hệ thống tiếp tục ở chế độ degraded thay vì bị quá tải thêm.

## Lưu ý khi hạ cấp

#### Reliable WorkQueue và Interest mirroring/sourcing

> 🇬🇧 *The same consideration as mentioned above under the upgrade considerations holds here as well. The `Invalid JetStream request` log line may be observed during a downgrade. Additionally, stream sourcing or mirroring might temporarily be unable to function until all servers are downgraded to the 2.12 version.*

Lưu ý tương tự như phần nâng cấp ở trên cũng áp dụng ở đây. Dòng log `Invalid JetStream request` có thể xuất hiện trong quá trình hạ cấp. Ngoài ra, stream sourcing hoặc mirroring có thể tạm thời không hoạt động cho đến khi tất cả server được hạ cấp về phiên bản 2.12.

> 🇬🇧 *If you've started using stream sourcing or mirroring on WorkQueue or Interest streams after upgrading, this will still seem to function but will operate under the less reliable ephemeral consumer mode. Additionally, any durable consumers created using the new configuration of `AckFlowControl` will be marked as "offline" and will not be usable until upgraded back to 2.14.*

Nếu bạn đã bắt đầu dùng stream sourcing hoặc mirroring trên WorkQueue hoặc Interest stream sau khi nâng cấp, chức năng này vẫn có vẻ hoạt động nhưng sẽ chạy ở chế độ ephemeral consumer kém tin cậy hơn. Ngoài ra, mọi durable consumer được tạo với config mới `AckFlowControl` sẽ bị đánh dấu "offline" và không thể dùng cho đến khi nâng cấp lại lên 2.14.

#### Feature flags

> 🇬🇧 *If you have defined the `feature_flags` field in your server config, you'll need to remove this prior to downgrading, since prior server versions will not recognize this field.*

Nếu đã định nghĩa field `feature_flags` trong server config, bạn cần xóa field này trước khi hạ cấp, vì các phiên bản server cũ sẽ không nhận ra field này.

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **async**: bất đồng bộ
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **leader**: server chính trong nhóm replica
- **log**: bản ghi sự kiện
- **message**: gói dữ liệu được gửi đi
- **node**: một server trong cluster
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)