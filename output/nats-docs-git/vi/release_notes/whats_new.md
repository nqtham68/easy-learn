---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/release_notes/whats_new
title: Có Gì Mới!
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Có Gì Mới!

> 🇬🇧 *The NATS.io team is continually working to bring you features that enhance your NATS experience. Below, you will find summaries of new NATS implementations. Release notes for the latest patch releases are available on [GitHub Releases](https://github.com/nats-io/nats-server/releases)*

Đội ngũ NATS.io liên tục phát triển các tính năng mới. Dưới đây là tóm tắt các cải tiến mới nhất. Release notes cho các bản vá gần đây có thể xem tại [GitHub Releases](https://github.com/nats-io/nats-server/releases).

## Lộ trình cho các bản phát hành tiếp theo

> 🇬🇧 *See [https://nats.io/about/#roadmap](https://nats.io/about/#roadmap)*

Xem tại [https://nats.io/about/#roadmap](https://nats.io/about/#roadmap).

## Server release v2.14.0

> 🇬🇧 *Check out the:*
> - *[Upgrade guide](./whats_new_214.md)*
> - *[Release notes](https://github.com/nats-io/nats-server/releases/tag/v2.14.0)*

Tham khảo:

- [Hướng dẫn nâng cấp](./whats_new_214.md)
- [Release notes](https://github.com/nats-io/nats-server/releases/tag/v2.14.0)

## Server release v2.12.0

> 🇬🇧 *Check out the:*
> - *[Upgrade guide](./whats_new_212.md)*
> - *[Release notes](https://github.com/nats-io/nats-server/releases/tag/v2.12.0)*

Tham khảo:

- [Hướng dẫn nâng cấp](./whats_new_212.md)
- [Release notes](https://github.com/nats-io/nats-server/releases/tag/v2.12.0)

## Server release v2.11.0

> 🇬🇧 *Check out the:*
> - *[Upgrade guide](./whats_new_211.md)*
> - *[Release notes](https://github.com/nats-io/nats-server/releases/tag/v2.11.0)*

Tham khảo:

- [Hướng dẫn nâng cấp](./whats_new_211.md)
- [Release notes](https://github.com/nats-io/nats-server/releases/tag/v2.11.0)

## Server release v2.10.0

> 🇬🇧 *Check out the:*
> - *[Upgrade guide](./whats_new_210.md)*
> - *[Podcast EP06: The journey and features of the NATS.io 2.10 release](https://youtu.be/9J4pRzHSc2k)*
> - *[Release notes](https://github.com/nats-io/nats-server/releases/tag/v2.10.0)*

Tham khảo:

- [Hướng dẫn nâng cấp](./whats_new_210.md)
- [Podcast EP06: Hành trình và tính năng của bản NATS.io 2.10](https://youtu.be/9J4pRzHSc2k)
- [Release notes](https://github.com/nats-io/nats-server/releases/tag/v2.10.0)

## Server release v2.9.0

> 🇬🇧 *Please check out the [announcement post](https://nats.io/blog/nats-server-29-release/) on the blog and the [detailed release notes](https://github.com/nats-io/nats-server/releases/tag/v2.9.0) in the server repo.*

Xem [bài thông báo](https://nats.io/blog/nats-server-29-release/) trên blog và [release notes chi tiết](https://github.com/nats-io/nats-server/releases/tag/v2.9.0) trong repo của server.

## Server release v2.8.0

### LeafNode

> 🇬🇧 *Support for a `min_version` in the `leafnodes{}` that would reject servers with a lower version. Note that this would work only for servers that are v2.8.0 and above.*

Hỗ trợ `min_version` trong `leafnodes{}` để từ chối các server có version thấp hơn. Lưu ý: tính năng này chỉ hoạt động với server từ v2.8.0 trở lên.

### Monitoring

> 🇬🇧 *- Server version in monitoring landing page.*
> *- Logging to `/healthz` endpoint when failure occurs.*
> *- MQTT and Websocket blocks in the `/varz` endpoint.*

- Hiển thị version server trên trang monitoring chính.
- Ghi log vào endpoint (địa chỉ API cụ thể) `/healthz` khi xảy ra lỗi.
- Bổ sung block MQTT và WebSocket trong endpoint `/varz`.

### JetStream

> 🇬🇧 *- Consumer check added to `healthz` endpoint.*
> *- Max stream bytes checks.*
> *- Ability to limit a consumer's `MaxAckPending` value.*
> *- Allow streams and consumers to migrate between clusters. This feature is considered "beta".*
> *- New `unique_tag` option in `jetstream{}` configuration block to prevent placing a stream in the same availability zone twice.*
> *- Stream `Alternates` field in `StreamInfo` response. They provide a priority list of mirrors and the source in relation to where the request originated.*
> *- Deterministic subject tokens to partition mapping.*

- Thêm kiểm tra consumer (bên xử lý dữ liệu từ stream) vào endpoint `healthz`.
- Kiểm tra giới hạn bytes tối đa của stream (luồng message lưu trữ liên tục).
- Khả năng giới hạn giá trị `MaxAckPending` của consumer.
- Cho phép stream và consumer di chuyển giữa các cluster. _Tính năng này được coi là "beta"._
- Tùy chọn `unique_tag` mới trong block cấu hình `jetstream{}` để tránh đặt một stream hai lần trong cùng availability zone.
- Trường `Alternates` của stream trong response `StreamInfo`, cung cấp danh sách ưu tiên các mirror và source so với nơi request xuất phát.
- Ánh xạ deterministic từ subject token sang partition.

> 🇬🇧 *For full release information, see links below;*

Để xem đầy đủ thông tin bản phát hành:

- Release notes [2.8.0](https://github.com/nats-io/nats-server/releases/tag/v2.8.0)
- Danh sách thay đổi đầy đủ [2.7.4...2.8.0](https://github.com/nats-io/nats-server/compare/v2.7.4...v2.8.0)

## Server release v2.7.0

### **Lưu ý cho người dùng JetStream**

> 🇬🇧 *See [important note](https://github.com/nats-io/nats-server/pull/2693#issuecomment-996212582) if using LeafNode regarding domains.*

Xem [ghi chú quan trọng](https://github.com/nats-io/nats-server/pull/2693#issuecomment-996212582) nếu đang dùng LeafNode liên quan đến domain.

### Cấu hình

> 🇬🇧 *Ability to configure account limits (`max_connections`, `max_subscriptions`, `max_payload`, `max_leafnodes`) in server configuration file.*

Có thể cấu hình giới hạn tài khoản (`max_connections`, `max_subscriptions`, `max_payload`, `max_leafnodes`) trực tiếp trong file cấu hình server.

### JetStream

> 🇬🇧 *- Overflow placement for streams. A stream can now be placed in the closest cluster from the origin request if it can be placed there.*
> *- Support for ephemeral Pull consumers (client libraries will need to be updated to allow those).*
> *- New consumer configuration options*
>   *- For Pull Consumers: `MaxRequestBatch` to limit the batch size any client can request `MaxRequestExpires` to limit the expiration any client can request*
>   *- For ephemeral consumers: `InactiveThreshold` duration that instructs the server to cleanup ephemeral consumers that are inactive for that long.*
> *- Ability to configure `max_file_store` and `max_memory_store` in the `jetstream{}` block as strings with the following suffixes `K`, `M`, `G` and `T`, for instance: `max_file_store: "256M"`.*
> *- Support for the JWT field `MaxBytesRequired`, which defines a per-account maximum bytes for assets.*

- Overflow placement cho stream: stream có thể được đặt vào cluster gần nhất so với request xuất phát nếu khả thi.
- Hỗ trợ ephemeral Pull consumer (các thư viện client cần cập nhật để dùng tính năng này).
- Tùy chọn cấu hình consumer mới:
  - Với Pull Consumer: `MaxRequestBatch` giới hạn batch size, `MaxRequestExpires` giới hạn thời gian hết hạn mà client có thể yêu cầu.
  - Với ephemeral consumer: khoảng thời gian `InactiveThreshold` chỉ thị server dọn dẹp các ephemeral consumer không hoạt động trong thời gian đó.
- Khả năng cấu hình `max_file_store` và `max_memory_store` trong block `jetstream{}` dưới dạng string với các hậu tố `K`, `M`, `G` và `T`, ví dụ: `max_file_store: "256M"`.
- Hỗ trợ trường JWT `MaxBytesRequired` định nghĩa số bytes tối đa cho tài sản theo từng tài khoản.

### MQTT

> 🇬🇧 *Support for websocket protocol. MQTT clients must connect to the opened websocket port and add `/mqtt` to the URL path.*

Hỗ trợ giao thức WebSocket. Client MQTT phải kết nối đến port WebSocket đã mở và thêm `/mqtt` vào đường dẫn URL.

### TLS

> 🇬🇧 *Ability to rate-limit the clients connections by adding the `connection_rate_limit: <number of connections per seconds>` in the `tls{}` top-level block.*

Có thể giới hạn tốc độ kết nối của client bằng cách thêm `connection_rate_limit: <number of connections per seconds>` vào block cấp cao nhất `tls{}`.

> 🇬🇧 *For full release information, see links below;*

Để xem đầy đủ thông tin bản phát hành:

- Release notes [2.7.0](https://github.com/nats-io/nats-server/releases/tag/v2.7.0)
- Danh sách thay đổi đầy đủ [2.6.6...2.7.0](https://github.com/nats-io/nats-server/compare/v2.6.6...v2.7.0)

## Server release v2.6.0

### **Lưu ý cho người dùng JetStream**

> 🇬🇧 *See important [note](https://github.com/nats-io/nats-server/releases/tag/v2.4.0) if upgrading from a version prior to NATS Server v2.4.0.*

Xem [ghi chú quan trọng](https://github.com/nats-io/nats-server/releases/tag/v2.4.0) nếu nâng cấp từ phiên bản trước NATS Server v2.4.0.

### Lưu ý cho người dùng MQTT

> 🇬🇧 *See important [notes](https://github.com/nats-io/nats-server/releases/tag/v2.5.0) if upgrading from a version prior to v2.5.0.*

Xem [ghi chú quan trọng](https://github.com/nats-io/nats-server/releases/tag/v2.5.0) nếu nâng cấp từ phiên bản trước v2.5.0.

### Monitoring

> 🇬🇧 *- JetStream's reserved memory and memory used from accounts with reservations in `/jsz` and `/varz` endpoints.*
> *- Hardened systemd service.*

- Bộ nhớ dự trữ và bộ nhớ đã dùng của JetStream từ các tài khoản có đăng ký dự trữ, hiển thị trong endpoint `/jsz` và `/varz`.
- Tăng cường bảo mật cho systemd service.

> 🇬🇧 *For full release information, see links below;*

Để xem đầy đủ thông tin bản phát hành:

- Release notes [2.6.0](https://github.com/nats-io/nats-server/releases/tag/v2.6.0)
- Danh sách thay đổi đầy đủ [2.5.0...2.6.0](https://github.com/nats-io/nats-server/compare/v2.6.0...v2.5.0)

## Server release v2.5.0

### **Lưu ý cho người dùng JetStream**

> 🇬🇧 *See important [note](.#notice-for-jetstream-users) if upgrading from a version prior to NATS Server v2.4.0.*

Xem [ghi chú quan trọng](.#notice-for-jetstream-users) nếu nâng cấp từ phiên bản trước NATS Server v2.4.0.

### MQTT/Monitoring

> 🇬🇧 *- `MQTTClient` in the `/connz` connections report and system events CONNECT and DISCONNECT. Ability to select on `mqtt_client`.*

- `MQTTClient` trong báo cáo kết nối `/connz` và các system event CONNECT, DISCONNECT. Hỗ trợ lọc theo `mqtt_client`.

### Cải tiến MQTT

> 🇬🇧 *Sessions are now all stored inside a single stream, as opposed to individual streams, reducing resources usage.*

Toàn bộ session giờ được lưu trong một stream duy nhất thay vì nhiều stream riêng lẻ, giúp giảm tiêu thụ tài nguyên.

### Cập nhật MQTT

> 🇬🇧 *Due to the aforementioned improvement described above, when an MQTT client connects for the first time after an upgrade to this server version, the server will migrate all individual `$MQTT_sess_<xxxx>` streams to a new `$MQTT_sess` stream for the user's account.*

Do cải tiến nêu trên, khi một MQTT client kết nối lần đầu sau khi nâng cấp lên phiên bản này, server sẽ tự động di chuyển tất cả stream `$MQTT_sess_<xxxx>` riêng lẻ sang stream `$MQTT_sess` mới cho tài khoản của người dùng.

> 🇬🇧 *For full release information, see links below;*

Để xem đầy đủ thông tin bản phát hành:

- Release notes [2.5.0](https://github.com/nats-io/nats-server/releases/tag/v2.5.0)
- Danh sách thay đổi đầy đủ [2.4.0...2.5.0](https://github.com/nats-io/nats-server/compare/v2.4.0...v2.5.0)

## Server release v2.4.0

### Lưu ý cho người dùng JetStream

> 🇬🇧 *With the latest release of the NATS server, we have fixed bugs around queue subscriptions and have restricted undesired behavior that could be confusing or introduce data loss by unintended/undefined behavior of client applications. If you are using queue subscriptions on a JetStream Push Consumer or have created multiple push subscriptions on the same consumer, you may be affected and need to upgrade your client version along with the server version. We've detailed the behavior with different client versions below.*

Bản phát hành mới nhất của NATS server đã sửa các lỗi liên quan đến queue subscription và hạn chế những hành vi không mong muốn có thể gây nhầm lẫn hoặc mất dữ liệu do hành vi không xác định của ứng dụng client. Nếu bạn đang dùng queue subscription trên JetStream Push Consumer, hoặc đã tạo nhiều push subscription trên cùng một consumer, bạn có thể bị ảnh hưởng và cần nâng cấp cả client lẫn server.

> 🇬🇧 *With a NATS Server **prior** to v2.4.0 and client libraries **prior** to these versions: NATS C client v3.1.0, Go client v1.12.0, Java client 2.12.0-SNAPSHOT, NATS.js v2.2.0, NATS.ws v1.3.0, NATS.deno v1.2.0, NATS .NET 0.14.0-pre2:*

Với NATS Server **trước** v2.4.0 và các thư viện client **trước** các phiên bản: NATS C client v3.1.0, Go client v1.12.0, Java client 2.12.0-SNAPSHOT, NATS.js v2.2.0, NATS.ws v1.3.0, NATS.deno v1.2.0, NATS .NET 0.14.0-pre2:

> 🇬🇧 *- It was possible to create multiple non-queue subscription instances for the same JetStream durable consumer. This is not correct since each instance will receive the same copy of a message and acknowledgment is therefore meaningless since the first instance to acknowledge the message will prevent other instances to control if/when a message should be acknowledged.*
> *- Similar to the first issue, it was possible to create many different queue groups for one single JetStream consumer.*
> *- For queue subscriptions, if no consumer nor durable name was provided, the libraries would create ephemeral JetStream consumers, which meant that each member of the same group would receive the same message as the other members, which was not the expected behavior. Users assumed that 2 members subscribing to "foo" with the queue group named "bar" would load-balance the consumption of messages from the stream/consumer.*
> *- It was possible to create a queue subscription on a JetStream consumer configured with heartbeat and/or flow control. This does not make sense because by definition, queue members would receive some (randomly distributed) messages, so the library would think that heartbeats are missed, and flow control would also be disrupted.*

- Có thể tạo nhiều instance non-queue subscription cho cùng một JetStream durable consumer. Đây là hành vi sai vì mỗi instance sẽ nhận cùng một bản sao message, khiến việc acknowledge trở nên vô nghĩa — instance nào acknowledge trước sẽ ngăn các instance khác kiểm soát việc message có/khi nào được acknowledge.
- Tương tự, có thể tạo nhiều queue group (nhóm subscribers chia sẻ tải) khác nhau cho cùng một JetStream consumer.
- Với queue subscription, nếu không cung cấp consumer hay durable name, các thư viện sẽ tạo ephemeral JetStream consumer, khiến mỗi thành viên trong nhóm nhận cùng một message — trái với hành vi mong đợi là load-balance.
- Có thể tạo queue subscription trên JetStream consumer được cấu hình với heartbeat và/hoặc flow control. Điều này không hợp lý vì các thành viên queue sẽ nhận message phân tán ngẫu nhiên, gây ra hiện tượng heartbeat bị bỏ lỡ và flow control bị gián đoạn.

> 🇬🇧 *If above client libraries are not updated to the latest but the NATS Server is upgraded to v2.4.0:*

Nếu các thư viện client chưa được cập nhật lên phiên bản mới nhất nhưng NATS Server đã nâng cấp lên v2.4.0:

> 🇬🇧 *- It is still possible to create multiple non-queue subscription instances for the same JetStream durable consumer. Since the check is performed by the library (with the help of a new field called `PushBound` in the consumer information object set by the server), this misbehavior is still possible.*
> *- Queue subscriptions will not receive any message. This is because the server now has a new field `DeliverGroup` in the consumer configuration, which won't be set for existing JetStream consumers and by the older libraries, and detects interest (and starts delivering) only when a subscription on the deliver subject for a queue subscription matching the "deliver group" name is found. Since the JetStream consumer is thought to be a non-deliver-group consumer, the opposite happens: the server detects a core NATS queue subscription on the "deliver subject", therefore does not trigger delivery on the JetStream consumer's "deliver subject".*

- Vẫn có thể tạo nhiều instance non-queue subscription cho cùng một JetStream durable consumer, vì kiểm tra được thực hiện phía thư viện (dựa trên trường mới `PushBound` trong đối tượng consumer information do server thiết lập).
- Queue subscription sẽ không nhận được message nào. Server v2.4.0 có thêm trường `DeliverGroup` trong cấu hình consumer, trường này không được thiết lập với consumer cũ và thư viện cũ. Server chỉ bắt đầu giao nhận khi tìm thấy subscription trên deliver subject khớp với tên "deliver group". Do consumer bị xác định là non-deliver-group, server phát hiện một queue subscription core NATS trên "deliver subject" và không kích hoạt giao nhận.

> 🇬🇧 *The 2 other issues are still present because those checks are done in the updated libraries.*

2 vấn đề còn lại vẫn tồn tại vì các kiểm tra đó được thực hiện trong thư viện đã cập nhật.

> 🇬🇧 *If the above client libraries are updated to the latest version, but the NATS Server is still to version prior to v2.4.0 (that is, up to v2.3.4):*

Nếu các thư viện client đã cập nhật lên phiên bản mới nhất nhưng NATS Server vẫn ở phiên bản trước v2.4.0 (tức là tối đa v2.3.4):

> 🇬🇧 *- It is still possible to create multiple non-queue subscription instances for the same JetStream durable consumer. This is because the JetStream consumer's information retrieved by the library will not have the `PushBound` boolean set by the server, therefore will not be able to alert the user that they are trying to create multiple subscription instances for the same JetStream consumer.*
> *- Queue subscriptions will fail because the consumer information returned will not contain the `DeliverGroup` field. The error will be likely to the effect that the user tries to create a queue subscription to a non-queue JetStream consumer. Note that if the application creates a queue subscription for a non-yet created JetStream consumer, then this call will succeed, however, adding new members or restarting the application with the now existing JetStream consumer will fail.*
> *- Creating queue subscriptions without a named consumer/durable will now result in the library using the queue name as the durable name.*
> *- Trying to create a queue subscription with a consumer configuration that has heartbeat and/or flow control will now return an error message.*

- Vẫn có thể tạo nhiều instance non-queue subscription cho cùng một JetStream durable consumer, vì thông tin consumer lấy từ server sẽ không có giá trị boolean `PushBound` nên thư viện không thể cảnh báo người dùng.
- Queue subscription sẽ thất bại vì thông tin consumer trả về không chứa trường `DeliverGroup`. Lỗi thường là người dùng đang cố tạo queue subscription cho một non-queue JetStream consumer. Lưu ý: nếu tạo queue subscription cho consumer chưa tồn tại thì thành công, nhưng thêm thành viên mới hoặc khởi động lại ứng dụng khi consumer đã có sẽ thất bại.
- Tạo queue subscription mà không có tên consumer/durable sẽ khiến thư viện dùng tên queue làm durable name.
- Cố tạo queue subscription với consumer có cấu hình heartbeat và/hoặc flow control sẽ trả về lỗi.

> 🇬🇧 *For completeness, using the latest client libraries and NATS Server v2.4.0:*

Để đầy đủ, khi dùng thư viện client mới nhất cùng NATS Server v2.4.0:

> 🇬🇧 *- Trying to start multiple non-queue subscriptions instances for the same JetStream consumer will now return an error to the effect that the user is trying to create a "duplicate subscription". That is, there is already an active subscription on that JetStream consumer. It is now only possible to create a queue group for a JetStream consumer created for that group. The `DeliverGroup` field will be set by the library or need to be provided when creating the consumer externally.*
> *- Trying to create a queue subscription without a durable nor consumer name results in the library creating/using the queue group as the JetStream consumer's durable name.*
> *- Trying to create a queue subscription with a consumer configuration that has heartbeat and/or flow control will now return an error message.*

- Cố tạo nhiều instance non-queue subscription cho cùng một JetStream consumer sẽ trả về lỗi "duplicate subscription" — tức là đã có subscription đang hoạt động trên consumer đó. Chỉ có thể tạo queue group cho JetStream consumer được tạo dành riêng cho nhóm đó. Trường `DeliverGroup` sẽ do thư viện thiết lập hoặc cần cung cấp khi tạo consumer bên ngoài.
- Tạo queue subscription mà không có durable hay consumer name khiến thư viện dùng tên queue group làm durable name của JetStream consumer.
- Cố tạo queue subscription với consumer có cấu hình heartbeat và/hoặc flow control sẽ trả về lỗi.

> 🇬🇧 *Note that if the server v2.4.0 recovers existing JetStream consumers that were created prior to v2.4.0 (and with older libraries), none of them will have a `DeliverGroup`, so none of them can be used for queue subscriptions. They will have to be recreated.*

Lưu ý: nếu server v2.4.0 khôi phục các JetStream consumer được tạo trước v2.4.0 (với thư viện cũ), không consumer nào có `DeliverGroup`, nên không thể dùng chúng cho queue subscription — cần tạo lại.

### JetStream

> 🇬🇧 *- Domain to the content of a `PubAck` protocol*
> *- `PushBound` boolean in `ConsumerInfo` to indicate that a push consumer is already bound to an active subscription*
> *- `DeliverGroup` string in `ConsumerConfig` to specify which deliver group (or queue group name) the consumer is created for*
> *- Warning log statement in situations where catchup for a stream resulted in an error*

- Thêm domain vào nội dung protocol `PubAck`.
- Boolean `PushBound` trong `ConsumerInfo` để chỉ thị push consumer đã được gắn với một subscription đang hoạt động.
- Chuỗi `DeliverGroup` trong `ConsumerConfig` để xác định deliver group (hoặc tên queue group) mà consumer được tạo cho.
- Thêm cảnh báo log khi quá trình catchup của stream gặp lỗi.

### Monitoring

> 🇬🇧 *- The ability for normal accounts to access scoped `connz` information*

- Cho phép các tài khoản thông thường truy cập thông tin `connz` có phạm vi giới hạn.

### Misc

> 🇬🇧 *- Operator option `resolver_pinned_accounts` to ensure users are signed by certain accounts*

- Tùy chọn operator `resolver_pinned_accounts` để đảm bảo người dùng được ký bởi các tài khoản nhất định.

> 🇬🇧 *For full release information, see links below;*

Để xem đầy đủ thông tin bản phát hành:

- Release notes [2.4.0](https://github.com/nats-io/nats-server/releases/tag/v2.4.0)
- Danh sách thay đổi đầy đủ [2.3.4...2.4.0](https://github.com/nats-io/nats-server/compare/v2.3.4...v2.4.0)

## Server release v2.3.0

> 🇬🇧 *- [OCSP support](../running-a-nats-service/configuration/ocsp.md)*

- [Hỗ trợ OCSP](../running-a-nats-service/configuration/ocsp.md)

### JetStream

> 🇬🇧 *- Richer API errors. JetStream errors now contain an ErrCode that uniquely describes the error.*
> *- Ability to send more advanced Stream purge requests that can purge all messages for a specific subject*
> *- Stream can now be configured with a per-subject message limit*
> *- Encryption of JetStream data at rest*

- Lỗi API phong phú hơn — JetStream error giờ chứa ErrCode mô tả chính xác lỗi.
- Hỗ trợ gửi yêu cầu Stream purge nâng cao, có thể xóa toàn bộ message theo subject (chuỗi định danh message) cụ thể.
- Stream có thể cấu hình giới hạn message theo từng subject.
- Mã hóa dữ liệu JetStream lưu trữ ở trạng thái nghỉ.

> 🇬🇧 *For full release information, see links below;*

Để xem đầy đủ thông tin bản phát hành:

- Release notes [2.3.0](https://github.com/nats-io/nats-server/releases/tag/v2.3.0)
- Danh sách thay đổi đầy đủ [2.2.6...2.3.0](https://github.com/nats-io/nats-server/compare/v2.2.6...v2.3.0)

## Server release v2.2.0

> 🇬🇧 *See [NATS 2.2](./whats_new_22.md) for new features.*

Xem [NATS 2.2](./whats_new_22.md) để biết các tính năng mới.

## Server release v2.1.7

### Monitoring Endpoint qua System Service

> 🇬🇧 *Monitoring endpoints as listed in the table below are accessible as system services using the following subject pattern:*

Các monitoring endpoint được liệt kê trong bảng dưới đây có thể truy cập dưới dạng system service theo mẫu subject sau:

- `$SYS.REQ.SERVER.<id>.<endpoint-name>` (gửi yêu cầu đến monitoring endpoint của server tương ứng với tên endpoint.)
- `$SYS.REQ.SERVER.PING.<endpoint-name>` (yêu cầu monitoring endpoint từ tất cả server — sẽ trả về nhiều message.)

> 🇬🇧 *For more information on monitoring endpoints see [NATS Server Configurations System Events](../running-a-nats-service/configuration/sys_accounts).*

Để biết thêm về monitoring endpoint, xem [NATS Server Configurations System Events](../running-a-nats-service/configuration/sys_accounts).

### Thêm cấu hình `no_auth_user`

> 🇬🇧 *Configuration of `no_auth_user` allows you to refer to a configured user/account when no credentials are provided.*

Cấu hình `no_auth_user` cho phép tham chiếu đến một user/account đã cấu hình khi không có credential (thông tin đăng nhập) nào được cung cấp.

> 🇬🇧 *For more information and examples, see [Securing NATS](../running-a-nats-service/configuration/securing_nats)*

Xem thêm thông tin và ví dụ tại [Securing NATS](../running-a-nats-service/configuration/securing_nats).

> 🇬🇧 *For full release information, see links below;*

Để xem đầy đủ thông tin bản phát hành:

- Release notes [2.1.7](https://github.com/nats-io/nats-server/releases/tag/v2.1.7)
- Danh sách thay đổi đầy đủ [2.1.6...2.1.7](https://github.com/nats-io/nats-server/compare/v2.1.6...v2.1.7)

## Server release v2.1.6

### Cấu hình TLS cho Account Resolver

> 🇬🇧 *This release adds the ability to specify TLS configuration for the account resolver.*

Bản phát hành này bổ sung khả năng chỉ định cấu hình TLS cho account resolver.

```
resolver_tls {
  cert_file: ...
  key_file: ...
  ca_file: ...
}
```

### Tùy chọn Verbosity Trace & Debug bổ sung

> 🇬🇧 *`trace_verbose` and command line parameters `-VV` and `-DVV` added. See [NATS Logging Configuration](../running-a-nats-service/configuration/logging.md#configuring-logging)*

Thêm `trace_verbose` và các tham số dòng lệnh `-VV` và `-DVV`. Xem [NATS Logging Configuration](../running-a-nats-service/configuration/logging.md#configuring-logging).

### Chi tiết Subscription trong Monitoring Endpoint

> 🇬🇧 *We've added the option to include subscription details in monitoring endpoints `/routez` and `/connz`. For instance `/connz?subs=detail` will now return not only the subjects of the subscription, but the queue name (if applicable) and some other details.*

Bổ sung tùy chọn bao gồm chi tiết subscription trong monitoring endpoint `/routez` và `/connz`. Ví dụ, `/connz?subs=detail` giờ trả về không chỉ các subject của subscription mà còn tên queue (nếu có) và một số thông tin khác.

- Release notes [2.1.6](https://github.com/nats-io/nats-server/releases/tag/v2.1.6)
- Danh sách thay đổi đầy đủ [2.1.4...2.1.6](https://github.com/nats-io/nats-server/compare/v2.1.4...v2.1.6)

## Server release v2.1.4

### Log Rotation

> 🇬🇧 *NATS introduces `logfile_size_limit` allowing auto-rotation of log files when the size is greater than the configured limit set in `logfile_size_limit` as a number of bytes. You can provide the size with units, such as MB, GB, etc. The backup files will have the same name as the original log file with the suffix .yyyy.mm.dd.hh.mm.ss.micros. For more information see Configuring Logging in the [NATS Server Configuration section](../running-a-nats-service/configuration/logging.md).*

NATS giới thiệu `logfile_size_limit` cho phép tự động xoay vòng file log khi kích thước vượt giới hạn được cấu hình trong `logfile_size_limit` (tính bằng byte). Có thể dùng đơn vị như MB, GB, v.v. File backup sẽ có tên giống file log gốc với hậu tố .yyyy.mm.dd.hh.mm.ss.micros. Xem thêm tại mục [NATS Server Configuration](../running-a-nats-service/configuration/logging.md).

- Release notes [2.1.4](https://github.com/nats-io/nats-server/releases/tag/v2.1.4)
- Danh sách thay đổi đầy đủ [2.1.2...2.1.4](https://github.com/nats-io/nats-server/compare/v2.1.2...v2.1.4)

## Server release v2.1.2

### Queue Permission

> 🇬🇧 *Queue Permissions allow you to express authorization for queue groups. As queue groups are integral to implementing horizontally scalable microservices, control of who is allowed to join a specific queue group is important to the overall security model. Original PR - [https://github.com/nats-io/nats-server/pull/1143](https://github.com/nats-io/nats-server/pull/1143)*

Queue Permission cho phép định nghĩa quyền truy cập cho queue group. Vì queue group là thành phần cốt lõi để xây dựng microservice có khả năng mở rộng ngang, việc kiểm soát ai được phép tham gia một queue group cụ thể rất quan trọng với mô hình bảo mật tổng thể. PR gốc: [https://github.com/nats-io/nats-server/pull/1143](https://github.com/nats-io/nats-server/pull/1143).

> 🇬🇧 *More information on Queue Permissions can be found in the [Developing with NATS](../using-nats/developing-with-nats/receiving/queues.md) section.*

Xem thêm về Queue Permission trong phần [Developing with NATS](../using-nats/developing-with-nats/receiving/queues.md).

## Server release v2.1.0

### Theo dõi Latency Service

> 🇬🇧 *As services and service mesh functionality has become prominent, we have been looking at ways to make running scalable services on NATS.io a great experience. One area we have been looking at is observability. With publish/subscribe systems, everything is inherently observable, however we realized it was not as simple as it could be. We wanted the ability to transparently add service latency tracking to any given service with no changes to the application. We also realized that global systems, such as those NATS.io can support, needed something more than a single metric. The solution was to allow any sampling rate to be attached to an exported service, with a delivery subject for all collected metrics. We collect metrics that show the requestor's view of latency, the responder's view of latency and the NATS subsystem itself, even when requestor and responder are in different parts of the world and connected to different servers in a NATS supercluster.*

Khi service và service mesh ngày càng được sử dụng rộng rãi, chúng tôi tìm cách cải thiện trải nghiệm chạy service có khả năng mở rộng trên NATS.io. Một điểm chúng tôi chú trọng là khả năng quan sát. Với hệ thống publish/subscribe, mọi thứ vốn đã có thể quan sát, nhưng chúng tôi nhận thấy còn có thể đơn giản hóa hơn. Mục tiêu là thêm tính năng theo dõi latency một cách trong suốt vào bất kỳ service nào mà không cần sửa ứng dụng. Với các hệ thống toàn cầu mà NATS.io hỗ trợ, một metric (số liệu đo lường) đơn lẻ là không đủ. Giải pháp là cho phép gắn bất kỳ tỉ lệ sampling nào vào một service xuất ra, kèm theo delivery subject cho tất cả metric đã thu thập — bao gồm góc nhìn latency từ phía người gửi, người nhận, và chính NATS subsystem, kể cả khi hai bên ở các vùng khác nhau trên thế giới và kết nối đến các server khác nhau trong NATS supercluster.

- Release notes [2.1.0](https://github.com/nats-io/nats-server/releases/tag/v2.1.0)
- Danh sách thay đổi đầy đủ [2.0.4...2.1.0](https://github.com/nats-io/nats-server/compare/v2.0.4...v2.1.0)

## Server release v2.0.4

### Response Only Permission

> 🇬🇧 *For services, the authorization for responding to requests usually included wildcards for \_INBOX.> and possibly $GR.> with a supercluster for sending responses. What we really wanted was the ability to allow a service responder to only respond to the reply subject it was sent.*

Với service, quyền truy cập để phản hồi request thường dùng wildcard cho `_INBOX.>` và có thể cả `$GR.>` với supercluster. Điều chúng tôi thực sự muốn là cho phép service chỉ được phép phản hồi đúng reply subject mà nó nhận được.

### Kiểu phản hồi (Response Types)

> 🇬🇧 *Exported Services were originally tied to a single response. We added the type for the service response and now support singletons (default), streams and chunked. Stream responses represent multiple response messages, chunked represents a single response that may have to be broken up into multiple messages.*

Trước đây, Exported Service chỉ hỗ trợ một phản hồi duy nhất. Giờ đây đã thêm kiểu phản hồi: singleton (mặc định), stream và chunked. Phản hồi dạng stream gồm nhiều message, dạng chunked là một phản hồi đơn có thể bị chia thành nhiều message.

- Release notes [2.0.4](https://github.com/nats-io/nats-server/releases/tag/v2.0.4)
- Danh sách thay đổi đầy đủ [2.0.2...2.0.4](https://github.com/nats-io/nats-server/compare/v2.0.2...v2.0.4)

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **credential**: thông tin đăng nhập
- **endpoint**: địa chỉ API cụ thể
- **log**: bản ghi sự kiện
- **message**: gói dữ liệu được gửi đi
- **metric**: số liệu đo lường
- **permission**: quyền truy cập
- **queue**: hàng đợi message
- **queue group**: nhóm subscribers chia sẻ tải
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **TLS**: mã hóa TLS