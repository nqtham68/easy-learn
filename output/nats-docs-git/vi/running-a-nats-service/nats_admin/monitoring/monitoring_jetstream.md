---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/monitoring/monitoring_jetstream
title: Giám sát JetStream
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Giám sát JetStream

## Tùy chọn thương mại

> 🇬🇧 *If you want a "batteries-included" approach to high-cardinality NATS monitoring and observability, including JetStream streams and consumers, try the standalone [Synadia Insights](https://www.synadia.com/insights).*

Nếu bạn muốn một giải pháp giám sát và quan sát NATS toàn diện "dùng ngay không cần cấu hình", bao gồm JetStream stream (luồng message lưu trữ liên tục) và consumer (bên xử lý dữ liệu từ stream), hãy thử [Synadia Insights](https://www.synadia.com/insights).

## Metric từ Server

> 🇬🇧 *JetStream has a /[jsz](../../configuration/monitoring.md#jetstream-information) HTTP endpoint and advisories available.*

JetStream cung cấp HTTP endpoint (địa chỉ API cụ thể) `/jsz` và các advisory để theo dõi trạng thái hệ thống.

## Advisory

> 🇬🇧 *JetStream publishes a number of advisories that can inform operations about the health and the state of the Streams. These advisories are published to normal NATS subjects below `$JS.EVENT.ADVISORY.>` and one can store these advisories in JetStream Streams if desired.*

JetStream phát hành nhiều advisory thông báo về tình trạng sức khỏe và trạng thái của các stream. Các advisory này được publish lên các NATS subject (chuỗi định danh message) thông thường bên dưới `$JS.EVENT.ADVISORY.>` và có thể lưu trữ chúng vào JetStream stream nếu cần.

> 🇬🇧 *The command `nats event --js-advisory` can view all these events on your console. The Golang package [jsm.go](https://github.com/nats-io/jsm.go) can consume and render these events and have data types for each of these events.*

Lệnh `nats event --js-advisory` hiển thị toàn bộ các event này trên console. Package Golang [jsm.go](https://github.com/nats-io/jsm.go) có thể consume và render các event này, đồng thời cung cấp kiểu dữ liệu cho từng loại event.

> 🇬🇧 *All these events have JSON Schemas that describe them, schemas can be viewed on the CLI using the `nats schema show <schema kind>` command.*

Tất cả các event đều có JSON Schema mô tả cấu trúc, có thể xem trên CLI bằng lệnh `nats schema show <schema kind>`.

| Mô tả                                                        | Subject | Kind                                                    |
|:-------------------------------------------------------------| :--- |:--------------------------------------------------------|
| Tương tác API                                                | `$JS.EVENT.ADVISORY.API` | `io.nats.jetstream.advisory.v1.api_audit`               |
| Các thao tác CRUD trên stream                                | `$JS.EVENT.ADVISORY.STREAM.CREATED.<STREAM>` | `io.nats.jetstream.advisory.v1.stream_action`           |
| Các thao tác CRUD trên consumer                              | `$JS.EVENT.ADVISORY.CONSUMER.CREATED.<STREAM>.<CONSUMER>` | `io.nats.jetstream.advisory.v1.consumer_action`         |
| Snapshot bắt đầu bằng `nats stream backup`                  | `$JS.EVENT.ADVISORY.STREAM.SNAPSHOT_CREATE.<STREAM>` | `io.nats.jetstream.advisory.v1.snapshot_create`         |
| Snapshot hoàn tất                                            | `$JS.EVENT.ADVISORY.STREAM.SNAPSHOT_COMPLETE.<STREAM>` | `io.nats.jetstream.advisory.v1.snapshot_complete`       |
| Restore bắt đầu bằng `nats stream restore`                  | `$JS.EVENT.ADVISORY.STREAM.RESTORE_CREATE.<STREAM>` | `io.nats.jetstream.advisory.v1.restore_create`          |
| Restore hoàn tất                                             | `$JS.EVENT.ADVISORY.STREAM.RESTORE_COMPLETE.<STREAM>` | `io.nats.jetstream.advisory.v1.restore_complete`        |
| Consumer đạt ngưỡng giao nhận tối đa                        | `$JS.EVENT.ADVISORY.CONSUMER.MAX_DELIVERIES.<STREAM>.<CONSUMER>` | `io.nats.jetstream.advisory.v1.max_deliver`             |
| Giao nhận message bị từ chối bằng AckNak                    | `$JS.EVENT.ADVISORY.CONSUMER.MSG_NAKED.<STREAM>.<CONSUMER>` | `io.nats.jetstream.advisory.v1.nak`                     |
| Giao nhận message bị hủy bằng AckTerm                       | `$JS.EVENT.ADVISORY.CONSUMER.MSG_TERMINATED.<STREAM>.<CONSUMER>` | `io.nats.jetstream.advisory.v1.terminated`              |
| Message được acknowledge trong consumer có sampling          | `$JS.EVENT.METRIC.CONSUMER.ACK.<STREAM>.<CONSUMER>` | `io.nats.jetstream.metric.v1.consumer_ack`              |
| Stream trong cluster (cụm nhiều server chạy chung) bầu chọn leader mới | `$JS.EVENT.ADVISORY.STREAM.LEADER_ELECTED.<STREAM>` | `io.nats.jetstream.advisory.v1.stream_leader_elected`   |
| Stream trong cluster mất quorum                              | `$JS.EVENT.ADVISORY.STREAM.QUORUM_LOST.<STREAM>` | `io.nats.jetstream.advisory.v1.stream_quorum_lost`      |
| Consumer trong cluster bầu chọn leader mới                  | `$JS.EVENT.ADVISORY.CONSUMER.LEADER_ELECTED.<STREAM>.<CONSUMER>` | `io.nats.jetstream.advisory.v1.consumer_leader_elected` |
| Consumer trong cluster mất quorum                            | `$JS.EVENT.ADVISORY.CONSUMER.QUORUM_LOST.<STREAM>.<CONSUMER>` | `io.nats.jetstream.advisory.v1.consumer_quorum_lost`    |

## Dashboard

> 🇬🇧 *Check out [NATS Surveyor Dashboards](https://github.com/nats-io/nats-surveyor/tree/main/docker-compose/grafana/provisioning/dashboards).*

Xem thêm tại [NATS Surveyor Dashboards](https://github.com/nats-io/nats-surveyor/tree/main/docker-compose/grafana/provisioning/dashboards).

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **endpoint**: địa chỉ API cụ thể
- **leader**: server chính trong nhóm replica
- **message**: gói dữ liệu được gửi đi
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)