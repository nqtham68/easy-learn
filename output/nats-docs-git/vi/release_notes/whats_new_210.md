---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/release_notes/whats_new_210
title: Tính năng mới trong NATS 2.10
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# NATS 2.10

> 🇬🇧 *This guide is tailored for existing NATS users upgrading from NATS version 2.9.x. This will read as a summary with links to specific documentation pages to learn more about the feature or improvement.*

Hướng dẫn này dành cho người dùng NATS đang nâng cấp từ phiên bản 2.9.x. Nội dung là bản tóm tắt kèm link đến các trang tài liệu chi tiết cho từng tính năng hoặc cải tiến.

## Lưu ý khi nâng cấp

### Phiên bản client

> 🇬🇧 *Although all existing client versions will work, new client versions will expose additional options used to leverage new features. The minimum client versions that have full 2.10.0 support include:*

Các phiên bản client (bên gọi, phía người dùng) hiện tại vẫn hoạt động được, nhưng các phiên bản mới sẽ mở ra thêm tùy chọn để tận dụng tính năng mới. Phiên bản client tối thiểu có đầy đủ hỗ trợ 2.10.0 bao gồm:

* CLI - [v0.1.0](https://github.com/nats-io/natscli/releases/tag/v0.1.0)
* nats.go - [v1.30.0](https://github.com/nats-io/nats.go/releases/tag/v1.30.0)
* nats.rs - [v0.32.0](https://github.com/nats-io/nats.rs/releases/tag/async-nats%2Fv0.32.0)
* nats.deno - [v1.17.0](https://github.com/nats-io/nats.deno/releases/tag/v1.17.0)
* nats.js - [v2.17.0](https://github.com/nats-io/nats.js/releases/tag/v2.17.0)
* nats.ws - [v1.18.0](https://github.com/nats-io/nats.ws/releases/tag/v1.18.0)
* nats.java - [v2.17.0](https://github.com/nats-io/nats.java/releases/tag/2.17.0)
* nats.net - [v1.1.0](https://github.com/nats-io/nats.net/releases/tag/1.1.0)
* nats.net.v2 - Sắp ra mắt!
* nats.py - Sắp ra mắt!
* nats.c - Sắp ra mắt!

### Helm charts

* k8s/nats - [v1.1.0](https://github.com/nats-io/k8s/releases/tag/nats-1.1.0)
* k8s/nack - [v0.24.0](https://github.com/nats-io/k8s/releases/tag/nack-0.24.0)

### Cảnh báo khi hạ cấp

> 🇬🇧 *For critical infrastructure like NATS, zero downtime upgrades are table stakes. Although the best practice for all infrastructure like this is for users to thoroughly test a new release against your specific workloads, inevitably there are cases where an upgrade occurs in production followed by a decision to downgrade. This is never recommended and can cause more harm than good for most infrastructure and data systems.*

Với hạ tầng quan trọng như NATS, nâng cấp không gián đoạn là yêu cầu tối thiểu. Dù thực hành tốt nhất là kiểm thử kỹ phiên bản mới trên workload thực tế, vẫn có trường hợp phải hạ cấp sau khi đã nâng cấp lên production. Điều này không bao giờ được khuyến nghị và có thể gây hại nhiều hơn lợi cho hầu hết các hệ thống hạ tầng và dữ liệu.

> 🇬🇧 *Below are a few important considerations if downgrading is required.*

Dưới đây là một số điểm quan trọng cần lưu ý nếu bắt buộc phải hạ cấp.

#### Thay đổi định dạng lưu trữ

> 🇬🇧 *2.10.0 brings on-disk storage changes which bring significant performance improvements. These are not compatible with previous versions of the NATS Server. If an upgrade is performed to a server with existing stream data on disk, followed by a downgrade, the older version server will not understand the stream data in the new format.*

2.10.0 thay đổi định dạng lưu trữ trên đĩa, mang lại cải thiện hiệu năng đáng kể nhưng không tương thích với các phiên bản NATS Server cũ. Nếu nâng cấp server đang có dữ liệu stream (luồng message lưu trữ liên tục) trên đĩa rồi hạ cấp, server phiên bản cũ sẽ không đọc được dữ liệu stream theo định dạng mới.

> 🇬🇧 *However, being mindful of the possibility of the need to downgrade, a special version of the 2.9.x series was released with awareness of key changes in the new storage format, allowing it to startup properly.*

Để đề phòng trường hợp này, một phiên bản đặc biệt trong dòng 2.9.x đã được phát hành với khả năng nhận biết các thay đổi chính trong định dạng lưu trữ mới, cho phép khởi động bình thường.

> 🇬🇧 *The takeaway is that if a downgrade is the only resort, it must be to 2.9.22 or later to ensure storage format changes are handled appropriately.*

Kết luận: nếu bắt buộc phải hạ cấp, phải hạ về phiên bản 2.9.22 hoặc mới hơn để đảm bảo xử lý đúng các thay đổi định dạng lưu trữ.

#### Tùy chọn cấu hình stream và consumer

> 🇬🇧 *There are new stream and consumer configuration options that could be problematic if a downgrade occurs since previous versions of the server have no awareness of them. Examples include:*

Có các tùy chọn config (cấu hình) mới cho stream và consumer (bên xử lý dữ liệu từ stream) mà các phiên bản server cũ không nhận biết, có thể gây vấn đề nếu hạ cấp:

* Multi-filter consumers - Hạ cấp sẽ khiến không có filter nào được áp dụng vì trường mới được cấu hình dạng danh sách thay vì chuỗi đơn.
* Subject-transform trên stream - Hạ cấp sẽ khiến subject transform không được áp dụng vì server không nhận biết nó.
* Compression trên stream - Hạ cấp khi compression đang bật trên stream sẽ khiến các stream đó không thể load do server cũ không hiểu kiểu nén đang dùng.

## Tính năng mới

### Nền tảng

* Hỗ trợ thử nghiệm cho [IBM z/OS](../running-a-nats-service/installation.md#supported-operating-systems-and-architectures)
* Hỗ trợ thử nghiệm cho [NetBSD](../running-a-nats-service/installation.md#supported-operating-systems-and-architectures)

### Reload

> 🇬🇧 *A server reload can now be performed by sending a message on [`$SYS.REQ.SERVER.<server-id>.RELOAD`](../running-a-nats-service/configuration#configuration-reloading) by a client authenticated in the system account.*

Giờ đây có thể reload server bằng cách gửi message trên [`$SYS.REQ.SERVER.<server-id>.RELOAD`](../running-a-nats-service/configuration#configuration-reloading) từ client đã xác thực trong system account.

### JetStream

> 🇬🇧 *A new [`sync_interval` server config option](../running-a-nats-service/configuration#jetstream) has been added to change the default sync interval of stream data when written to disk, including allowing all writes to be flushed immediately. This option is only relevant if you need to modify durability guarantees.*

Đã thêm [tùy chọn config server `sync_interval`](../running-a-nats-service/configuration#jetstream) mới để thay đổi chu kỳ sync mặc định của dữ liệu stream khi ghi xuống đĩa, kể cả cho phép flush ngay lập tức. Tùy chọn này chỉ cần thiết khi cần điều chỉnh đảm bảo độ bền dữ liệu.

### Subject mapping

> 🇬🇧 *Subject mappings can now be [cluster-scoped](https://docs.nats.io/nats-concepts/subject\_mapping#cluster-scoped-mappings) and weighted, enabling the ability to have different mappings or weights on a per cluster basis.*

Subject mapping giờ có thể [giới hạn theo cluster](https://docs.nats.io/nats-concepts/subject\_mapping#cluster-scoped-mappings) (cụm nhiều server chạy chung) và có trọng số, cho phép dùng mapping hoặc trọng số khác nhau trên từng cluster.

> 🇬🇧 *The requirement to use all wildcard tokens in subject mapping or transforms has been relaxed. This can be applied to config or account-based subject mapping, stream subject transforms, and stream republishing, but not on subject mappings that are associated with stream and service import/export between accounts.*

Yêu cầu phải dùng tất cả wildcard token trong subject mapping hoặc transform đã được nới lỏng. Điều này áp dụng cho subject mapping theo config hoặc theo account, stream subject transform và stream republishing, nhưng không áp dụng cho subject mapping liên quan đến import/export stream và service giữa các account.

### Streams

> 🇬🇧 *A [`subject_transform` field](../nats-concepts/jetstream/streams.md#subjecttransforms) has been added enabling per-stream subject transforms. This applies to standard streams, mirrors, and sourced streams.*

Đã thêm [trường `subject_transform`](../nats-concepts/jetstream/streams.md#subjecttransforms) cho phép cấu hình subject transform theo từng stream. Áp dụng cho stream thông thường, mirror và sourced stream.

> 🇬🇧 *A [`metadata` field](../nats-concepts/jetstream/streams.md#configuration) has been added to stream configuration enabling arbitrary user-defined key-value data. This is to supplant or augment the `description` field.*

Đã thêm [trường `metadata`](../nats-concepts/jetstream/streams.md#configuration) vào config stream cho phép lưu dữ liệu key-value tùy ý do người dùng định nghĩa, thay thế hoặc bổ sung cho trường `description`.

> 🇬🇧 *A [`first_seq` field](../nats-concepts/jetstream/streams.md#configuration) has been added to stream configuration enabling explicitly setting the initial sequence on stream creation.*

Đã thêm [trường `first_seq`](../nats-concepts/jetstream/streams.md#configuration) vào config stream cho phép đặt sequence ban đầu khi tạo stream.

> 🇬🇧 *A [`compression` field](../nats-concepts/jetstream/streams.md#configuration) has been added to stream configuration enabling on-disk compression for file-based streams.*

Đã thêm [trường `compression`](../nats-concepts/jetstream/streams.md#configuration) vào config stream cho phép bật compression trên đĩa cho các stream dùng file storage.

> 🇬🇧 *The ability to edit the [`republish` config option](../nats-concepts/jetstream/streams.md#republish) on a stream after stream creation was added.*

Đã bổ sung khả năng chỉnh sửa [tùy chọn config `republish`](../nats-concepts/jetstream/streams.md#republish) sau khi stream đã được tạo.

> 🇬🇧 *A [`Nats-Time-Stamp` header](../nats-concepts/jetstream/headers.md#republish) is now included in republished messages containing the original message's timestamp.*

[Header `Nats-Time-Stamp`](../nats-concepts/jetstream/headers.md#republish) giờ được đính kèm trong các message được republish, chứa timestamp của message gốc.

> 🇬🇧 *A `ts` field has been added to stream info responses indicating the server time of the snapshot. This was added to allow for local time calculations relying on the local clock.*

Đã thêm trường `ts` vào response stream info, cho biết thời điểm server tạo snapshot. Bổ sung này giúp tính toán thời gian cục bộ dựa trên đồng hồ local.

> 🇬🇧 *An array of subject-transforms (subject filter + subject transform destination) can be added to a mirror or source configuration (can not use the single subject filter/subject transform destination fields at the same time as the array).*

Có thể thêm mảng subject-transform (bộ lọc subject + đích transform) vào config mirror hoặc source. Lưu ý: không thể dùng đồng thời trường subject filter/subject transform đơn lẻ cùng lúc với mảng này.

> 🇬🇧 *A stream configured with `sources` can source from the same stream multiple times when distinct filter+transform options are used, allowing for some messages of a stream to be sourced more than once.*

Stream cấu hình với `sources` có thể source từ cùng một stream nhiều lần khi dùng các tổ hợp filter+transform khác nhau, cho phép một số message được source nhiều hơn một lần.

### Consumers

> 🇬🇧 *A [`filter_subjects` field](../nats-concepts/jetstream/consumers.md#filtersubjects) has been added which enables applying server-side filtering against multiple disjoint subjects, rather than only one.*

Đã thêm [trường `filter_subjects`](../nats-concepts/jetstream/consumers.md#filtersubjects) cho phép lọc phía server trên nhiều subject (chuỗi định danh message) không giao nhau, thay vì chỉ một subject.

> 🇬🇧 *A [`metadata` field](../nats-concepts/jetstream/consumers.md#configuration) has been added to consumer configuration enabling arbitrary user-defined key-value data. This is to supplant or augment the `description` field.*

Đã thêm [trường `metadata`](../nats-concepts/jetstream/consumers.md#configuration) vào config consumer cho phép lưu dữ liệu key-value tùy ý do người dùng định nghĩa, thay thế hoặc bổ sung cho trường `description`.

> 🇬🇧 *A `ts` field has been added to consumer info responses indicating the server time of the snapshot. This was added to allow for local time calculations without relying on the local clock.*

Đã thêm trường `ts` vào response consumer info, cho biết thời điểm server tạo snapshot, giúp tính toán thời gian cục bộ không phụ thuộc vào đồng hồ local.

### Key-value

> 🇬🇧 *A [`metadata` field](../nats-concepts/jetstream/key-value-store#configuration) has been added to key-value configuration enabling arbitrary user-defined key-value data. This is to supplant or augment the `description` field.*

Đã thêm [trường `metadata`](../nats-concepts/jetstream/key-value-store#configuration) vào config key-value cho phép lưu dữ liệu key-value tùy ý do người dùng định nghĩa, thay thế hoặc bổ sung cho trường `description`.

> 🇬🇧 *A bucket configured as a mirror or sourcing from other buckets*

Bucket có thể được cấu hình là mirror hoặc source từ các bucket khác.

### Object store

> 🇬🇧 *A [`metadata` field](../nats-concepts/jetstream/object-store#configuration) has been added to object store configuration enabling arbitrary user-defined key-value data. This is to supplant or augment the `description` field.*

Đã thêm [trường `metadata`](../nats-concepts/jetstream/object-store#configuration) vào config object store cho phép lưu dữ liệu key-value tùy ý do người dùng định nghĩa, thay thế hoặc bổ sung cho trường `description`.

### Authn/Authz

> 🇬🇧 *A pluggable server extension, referred to as [auth callout](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/auth\_callout), has been added. This provides a mechanism for delegating authentication checks against a bring-your-own (BYO) provider and, optionally, dynamically declaring permissions for the authenticated user.*

Đã thêm một server extension có thể cắm vào, gọi là [auth callout](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/auth\_callout). Cơ chế này cho phép ủy thác xác thực cho provider tùy chọn (BYO) và tùy ý khai báo permission (quyền truy cập) động cho người dùng đã xác thực.

### Monitoring

> 🇬🇧 *A `unique_tag` field has been added to the [`/varz`](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#general-information) and [`/jsz`](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#jetstream-information) HTTP endpoint responses, corresponding to the value of `unique_tag` defined in the server config.*

Đã thêm trường `unique_tag` vào response của các HTTP endpoint (địa chỉ API cụ thể) [`/varz`](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#general-information) và [`/jsz`](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#jetstream-information), tương ứng với giá trị `unique_tag` trong config server.

> 🇬🇧 *A `slow_consumer_stats` field has been added to the [`/varz`](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#general-information) HTTP endpoint providing a count of slow consumers for clients, routes, gateways, and leafnodes.*

Đã thêm trường `slow_consumer_stats` vào HTTP endpoint [`/varz`](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#general-information), cung cấp số lượng slow consumer cho client, route, gateway và leafnode.

> 🇬🇧 *A `raft=1` query parameter has been added to the [`/jsz`](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#jetstream-information) HTTP endpoint which adds `stream_raft_group` and `consumer_raft_groups` fields to the response.*

Đã thêm query parameter `raft=1` vào HTTP endpoint [`/jsz`](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#jetstream-information), bổ sung các trường `stream_raft_group` và `consumer_raft_groups` vào response.

> 🇬🇧 *A `num_subscriptions` field has been added to the [`$SYS.REQ.SERVER.PING.STATZ`](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts/sys\_accounts#usdsys.req.server.less-than-id-greater-than.statsz-requesting-server-stats-summary) NATS endpoint responses.*

Đã thêm trường `num_subscriptions` vào response của NATS endpoint [`$SYS.REQ.SERVER.PING.STATZ`](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts/sys\_accounts#usdsys.req.server.less-than-id-greater-than.statsz-requesting-server-stats-summary).

> 🇬🇧 *A system account responder for [`$SYS.REQ.SERVER.PING.IDZ`](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts/sys\_accounts#usdsys.req.server.ping.idz-discovering-servers) has been added which returns info for the server that the client is connected to.*

Đã thêm system account responder cho [`$SYS.REQ.SERVER.PING.IDZ`](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts/sys\_accounts#usdsys.req.server.ping.idz-discovering-servers), trả về thông tin server mà client đang kết nối tới.

> 🇬🇧 *A system account responder for [`$SYS.REQ.SERVER.PING.PROFILEZ`](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts/sys\_accounts#usdsys.req.server.less-than-id-greater-than.profilez-request-profiling-information) has been added and works even if a profiling port is not enabled in the server configuration.*

Đã thêm system account responder cho [`$SYS.REQ.SERVER.PING.PROFILEZ`](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts/sys\_accounts#usdsys.req.server.less-than-id-greater-than.profilez-request-profiling-information), hoạt động ngay cả khi profiling port chưa được bật trong config server.

> 🇬🇧 *A user account responder for [`$SYS.REQ.USER.INFO`](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts/sys\_accounts#usdsys.req.user.info-request-connected-user-information) has been added which allows a connected user to query for the account they are in and permissions they have.*

Đã thêm user account responder cho [`$SYS.REQ.USER.INFO`](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts/sys\_accounts#usdsys.req.user.info-request-connected-user-information), cho phép người dùng đang kết nối truy vấn account và permission của mình.

### MQTT

> 🇬🇧 *Support for [QoS2](../running-a-nats-service/configuration/mqtt) has been added. Check out the new [MQTT implementation details](https://github.com/nats-io/nats-server/blob/main/server/README-MQTT.md) overview.*

Đã bổ sung hỗ trợ [QoS2](../running-a-nats-service/configuration/mqtt). Xem tổng quan [chi tiết triển khai MQTT](https://github.com/nats-io/nats-server/blob/main/server/README-MQTT.md) để biết thêm.

### Clustering

> 🇬🇧 *When defining routes between servers, a handful of optimizations have been introduced including a pool of TCP connections between servers, optional pinning of accounts to connections, and optional compression of traffic. There is quite a bit to dig into, so check out the [v2 routes](https://docs.nats.io/running-a-nats-service/configuration/clustering/v2\_routes) page for details.*

Khi cấu hình route giữa các server, một số tối ưu hóa đã được giới thiệu: pool kết nối TCP giữa các server, tùy chọn ghim account vào kết nối, và tùy chọn nén traffic. Xem trang [v2 routes](https://docs.nats.io/running-a-nats-service/configuration/clustering/v2\_routes) để biết chi tiết.

### Leafnodes

> 🇬🇧 *A [`handshake_first` config option](../running-a-nats-service/configuration/leafnodes#tls-first-handshake) has been added enabling TLS-first handshakes for leafnode connections.*

Đã thêm [tùy chọn config `handshake_first`](../running-a-nats-service/configuration/leafnodes#tls-first-handshake) cho phép thực hiện TLS-first handshake cho kết nối leafnode.

### Windows

> 🇬🇧 *The [`NATS_STARTUP_DELAY` environment variable](https://docs.nats.io/running-a-nats-service/running/windows\_srv#nats\_startup\_delay-environment-variable) has been added to allow changing the default startup for the server of 10 seconds*

Đã thêm [biến môi trường `NATS_STARTUP_DELAY`](https://docs.nats.io/running-a-nats-service/running/windows\_srv#nats\_startup\_delay-environment-variable) cho phép thay đổi thời gian khởi động mặc định 10 giây của server.

## Cải tiến

### Reload

> 🇬🇧 *The [`nats-server --signal` command](https://docs.nats.io/running-a-nats-service/nats\_admin/signals#multiple-processes) now supports a glob expression on the `<pid>` argument which would match a subset of all `nats-server` instances running on the host.*

[Lệnh `nats-server --signal`](https://docs.nats.io/running-a-nats-service/nats\_admin/signals#multiple-processes) giờ hỗ trợ biểu thức glob cho tham số `<pid>`, cho phép khớp một tập con trong tất cả các instance `nats-server` đang chạy trên host.

### Streams

> 🇬🇧 *Prior to 2.10, setting [`republish` configuration](../nats-concepts/jetstream/streams.md#republish) on mirrors would result in an error. On sourcing streams, only messages that were actively between stored matching configured `subjects` would be republished. The behavior has been relaxed to allow republishing on mirrors and includes all messages on sourcing streams.*

Trước phiên bản 2.10, việc đặt [config `republish`](../nats-concepts/jetstream/streams.md#republish) trên mirror sẽ gây lỗi. Trên sourcing stream, chỉ các message khớp với `subjects` đã cấu hình mới được republish. Hành vi này đã được nới lỏng: cho phép republish trên mirror và bao gồm tất cả message trên sourcing stream.

### Consumers

> 🇬🇧 *A new header has been added on a fetch response that indicates to clients the fetch has been fulfilled without requiring clients to rely on heartbeats. It avoids some conditions in which the client would issue fetch requests that could go over limits or have more fetch requests pending than required.*

Đã thêm header mới vào fetch response để thông báo cho client rằng fetch đã hoàn thành mà không cần dựa vào heartbeat. Điều này tránh được các trường hợp client gửi fetch request vượt quá giới hạn hoặc có nhiều fetch request pending hơn mức cần thiết.

### Leafnodes

> 🇬🇧 *Previously, a leafnode configured with two or more remotes binding to the same hub account would be rejected. This restriction has been relaxed since each remote could be binding to a different local account.*

Trước đây, leafnode cấu hình từ hai remote trở lên cùng bind vào một hub account sẽ bị từ chối. Hạn chế này đã được nới lỏng vì mỗi remote có thể bind vào một local account khác nhau.

### MQTT

> 🇬🇧 *Previously a dot `.` in an MQTT topic was not supported, however now it is! Check out the [topic-subject conversion table](../running-a-nats-service/configuration/mqtt) for details.*

Trước đây, dấu chấm `.` trong MQTT topic không được hỗ trợ, nhưng giờ đã được hỗ trợ. Xem [bảng chuyển đổi topic-subject](../running-a-nats-service/configuration/mqtt) để biết chi tiết.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **endpoint**: địa chỉ API cụ thể
- **message**: gói dữ liệu được gửi đi
- **permission**: quyền truy cập
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **TLS**: mã hóa TLS