---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/jetstream/headers
title: Headers trong JetStream
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Headers trong JetStream

> 🇬🇧 *Message headers are used in a variety of JetStream contexts, such de-duplication, auto-purging of messages, metadata from republished messages, and more.*

Message header (phần metadata kèm theo) được dùng trong nhiều ngữ cảnh JetStream khác nhau: loại trừ trùng lặp, tự động xóa message (gói dữ liệu được gửi đi), metadata từ message được republish, và nhiều mục đích khác.

> 🇬🇧 *`Nats-` is a reserved namespace. Please use a different prefix for your own headers. This list may not be complete. Additional headers may be used for API internal messages or messages used for monitoring and control.*

`Nats-` là namespace dành riêng. Hãy dùng prefix khác cho header của bạn. Danh sách này có thể chưa đầy đủ — một số header bổ sung có thể được dùng cho các message nội bộ API hoặc message phục vụ giám sát và điều khiển.

## Publish

> 🇬🇧 *Headers that can be set by a client when a message being published. These headers are recognized by the server.*

Các header client có thể thiết lập khi publish message. Server sẽ nhận diện các header này.

| Name                                  | Description                                                                                                                                                                                                       | Example                                | Version |
|:----------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------|
| `Nats-Msg-Id`                         | Client-defined unique identifier for a message that will be used by the server apply de-duplication within the configured `Duplicate Window`.                                                                     | `9f01ccf0-8c34-4789-8688-231a2538a98b` | 2.2.0   |
| `Nats-Expected-Stream`                | Used to assert the published message is received by some expected stream.                                                                                                                                         | `my-stream`                            | 2.2.0   |
| `Nats-Expected-Last-Msg-Id`           | Used to apply optimistic concurrency control at the stream-level. The value is the last expected `Nats-Msg-Id` and the server will reject a publish if the current ID does not match.                             | `9f01ccf0-8c34-4789-8688-231a2538a98b` | 2.2.0   |
| `Nats-Expected-Last-Sequence`         | Used to apply optimistic concurrency control at the stream-level. The value is the last expected sequence and the server will reject a publish if the current sequence does not match.                            | `328`                                  | 2.2.0   |
| `Nats-Expected-Last-Subject-Sequence` | Used to apply optimistic concurrency control at the subject-level. The value is the last expected sequence and the server will reject a publish if the current sequence does not match for the message's subject. | `38`                                   | 2.3.1   |
| `Nats-Expected-Last-Subject-Sequence-Subject` | A subject which may include wildcards. Used with `Nats-Expected-Last-Subject-Sequence`. Server will enforce last sequence against the given subject rather than the one being published.                          | `events.orders.1.>`                                                                                                                                               | 2.11.0  |
| `Nats-Rollup`                         | Used to apply a purge of all prior messages in a stream or at the subject-level. The `rollup message` will stay in the stream. Requires the allow rollups to be set on the stream.       | `all` purges the full stream, `sub` purges the subject on which this messages was sent. Wildcards subjects are not allowed and will result in undefined behavior.   | 2.6.2   |
| `Nats-TTL`   |   Used to set a per message TTL. Requires the per message ttl flag to be set on the stream.   | `1h`, `10s` (go duration string format)  | 2.11   |

## RePublish hoặc Direct Get

> 🇬🇧 *When messages are being re-published (must be configured in stream settings) from a stream or retrieved with a direct get operation from stream these headers are being set.*

Khi message được republish từ một stream (luồng message lưu trữ liên tục) — phải cấu hình trong stream settings — hoặc được lấy qua thao tác direct get, các header sau sẽ được tự động gán.

> 🇬🇧 *Do not set these headers on client published messages.*

Không tự thiết lập các header này trên message do client publish.

| Name                 | Description                                                                                                            | Example                       | Version |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------- | :---------------------------- | :------ |
| `Nats-Stream`        | Name of the stream the message was republished from.                                                                   | `Nats-Stream: my-stream`      | 2.8.3   |
| `Nats-Subject`       | The original subject of the message.                                                                                   | `events.mouse_clicked`        | 2.8.3   |
| `Nats-Sequence`      | The original sequence of the message.                                                                                  | `193`                         | 2.8.3   |
| `Nats-Last-Sequence` | The last sequence of the message having the same subject, otherwise zero if this is the first message for the subject. | `190`                         | 2.8.3   |
| `Nats-Time-Stamp`    | The original timestamp of the message.                                                                                 | `2023-08-23T19:53:05.762416Z` | 2.10.0  |
| `Nats-Num-Pending`    | Number of messages pending in the multi/batched get response. or details see:  [ADR-31](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-31.md)                                                                                                  | `5` | 2.10.0  |
| `Nats-UpTo-Sequence`    | On the last messages of multi/batched get response. The `up-to-seq` value of the original request. Helps the client to continue incomplete batch requests. For details see:  [ADR-31](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-31.md)                                                                                |  | 2.11.0  |


## Sources

> 🇬🇧 *Headers that are implicitly added to messages sourced from other streams.*

Các header được tự động thêm vào message khi message được lấy từ các stream khác.

> 🇬🇧 *The format of the header content may change in the future. Please parse conservatively and assume that additional fields may be added or that older nats-server version have fewer fields.*

Định dạng nội dung header có thể thay đổi trong tương lai. Hãy parse một cách thận trọng và giả định rằng có thể có thêm field mới, hoặc phiên bản nats-server cũ hơn có ít field hơn.

| Name                 | Description                                                                                                                                           | Example     | Version |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :---------- | :------ |
| `Nats-Stream-Source` | Contains space delimited:<br> - Origin stream name (disambiguated with domain hash if cross domain sourced)<br> - The original sequence number<br> - The list of subject filters<br> - The list of destination transforms<br> - The original subject<br>  | `ORDERS:vSF0ECo6 17 foo.* bar.$1 foo.abc` | 2.2.0   |

## Tracing

> 🇬🇧 *When tracing is activated every subsystem that touches a message will produce Trace Events. These Events are aggregated per server and published to a destination subject.*

Khi tracing được bật, mọi subsystem xử lý message đều tạo ra Trace Event. Các event này được tổng hợp theo từng server và publish đến một subject (chuỗi định danh message) đích.

> 🇬🇧 *Note that two variants exist. `traceparent` as per the trace context standard and ad hoc tracing through `Nats-Trace-Dest`.*

Có hai biến thể: `traceparent` theo chuẩn trace context, và tracing ad hoc thông qua `Nats-Trace-Dest`.

> 🇬🇧 *Introduced in version 2.11 - see [ADR-41](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-41.md)*

Ra mắt từ phiên bản 2.11 — xem [ADR-41](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-41.md).

| Name            | Description                          | Example | Version |
| :-------------- | :----------------------------------- | :------ | :------ |
| `traceparent` | Triggers tracing as per the [https://www.w3.org/TR/trace-context/](https://www.w3.org/TR/trace-context/) standard. Requires the `msg-trace` section to be configured on the account level. | N/A | 2.11   |
| `Nats-Trace-Dest` |  The subject that will receive the Trace messages  | trace.receiver.all | 2.11   |
| `Nats-Trace-Only` | Optional. Defaults to `false`. Set to `true` to skip message delivery. If true only traces will be produced, but the messages is not sent to a subscribing client or stored in JetStream.   | `true` | 2.11   |
| `Accept-Encoding` | Optional. Enables compression of the payload of the trace messages.  | `gzip`, `snappy` | 2.11   |
| `Nats-Trace-Hop` | Internal. **Do not set**. Set by the server to count hops.  | `<hop count>` | 2.11   |
| `Nats-Trace-Origin-Account` | Internal. **Do not set**. Set by the server when an account boundary is crossed  | `<account name>` | 2.11   |

## Scheduler

> 🇬🇧 *Message scheduling in streams. Needs to be enabled on the stream with "allow schedules" flag.*

Lập lịch message trong stream. Cần bật flag "allow schedules" trên stream.

> 🇬🇧 *Introduced in version 2.12 with extensions in 2.14 - see [ADR-51](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-51.md)*

Ra mắt từ phiên bản 2.12, mở rộng trong 2.14 — xem [ADR-51](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-51.md).

| Name                      | Description                                                                                                                                                                                                                | Example                                                                                        | Version                          |
|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------|:---------------------------------|
| `Nats-Schedule`           | When the message will be sent to the target subject. Several formats are suppported: A timestamp for sending a messages once. Crontab format for repeated messages and simple alias for common crontab formats.            | `0 30 14 * * *`, `@hourly`, `@daily`, `@every 5m`, `@at 2009-11-10T23:00:00Z` (RFC3339 format) | 2.12 (repeating schedules: 2.14) |
| `Nats-Schedule-TTL`       | Optional. The TTL to be set on the final message on the target subject.                                                                                                                                                    | `1h`, `10s` (valid go duration string)                                                         | 2.12                             |
| `Nats-Schedule-Target`    | The target subject the final message will be sent to. Note that this must be distinct from the scheduling subject the message arrived in.                                                                                  | `orders`                                                                                       | 2.12                             |
| `Nats-Schedule-Rollup`    | Optional. The rollup to be set on the final message on the target subject.                                                                                                                                                 | `all`, `sub`                                                                                   | 2.14                             |
| `Nats-Schedule-Source`    | Optional. Instructs the schedule to read the last message on the given subject and publish it. If the Subject is empty, the schedule message's content is the same as the schedule's content. Wildcards are not supported. | `orders.customer_acme`                                                                         | 2.14                             |
| `Nats-Schedule-Time-Zone` | Optional. The time zone used for the Cron schedule. If not specified, the Cron schedule will be in UTC. Not allowed to be used if the schedule is not a Cron schedule.                                                     | `CET`                                                                                          | 2.14                             |

> 🇬🇧 *The final scheduled message will contain the following headers.*

Message được lập lịch cuối cùng sẽ chứa các header sau.

| Name                 | Description                                                                              | Example                         | Version |
|:---------------------|:-----------------------------------------------------------------------------------------|:--------------------------------|:--------|
| `Nats-Scheduler`     | The subject holding the schedule                                                         | `orders.schedule.1234`          | 2.12    |
| `Nats-Schedule-Next` | Timestamp for next invocation for cron schedule messages or `purge` for delayed messages | `2009-11-10T23:00:00Z`, `purge` | 2.12    |
| `Nats-TTL`           | The TTL value when `Nats-Schedule-TTL` was set                                           | `1h`, `10s`                     | 2.12    |
| `Nats-Rollup`        | The rollup value when `Nats-Schedule-Rollup` was set                                     | `all`, `sub`                    | 2.14    |


## Atomic Batch Publish

> 🇬🇧 *Introduced in version 2.12 with optimizations in 2.14 - see [ADR-50](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-50.md)*

Ra mắt từ phiên bản 2.12, tối ưu hóa trong 2.14 — xem [ADR-50](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-50.md).

> 🇬🇧 *Atomic batch publish will use the following headers. A client may reconstruct a batch using the headers below.*

Atomic batch publish sử dụng các header sau. Client có thể tái tạo lại một batch từ các header này.

| Name                  | Description                                                                                                                                                 | Example                    | Version            |
|:----------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------|:-------------------|
| `Nats-Batch-Id`       | Unique identifier for the batch.                                                                                                                            | `<uuid>` (<=64 characters) | 2.12               |
| `Nats-Batch-Sequence` | Monotonically increasing sequence number, starting at `1`                                                                                                   | `1`, `2`                   | 2.12               |
| `Nats-Batch-Commit`   | Only on last message. `1` commit the batch including this message. `eob` commit the batch excluding this message. Any other value will terminate the batch. | `1`, `eob`                 | 2.12 (`eob`: 2.14) |


## Internal

> 🇬🇧 *Headers used internally by API clients and the server. Should not be set by user.*

Các header dùng nội bộ bởi API client và server. Người dùng không nên tự thiết lập.

> 🇬🇧 *This is list is not exhaustive. Headers used in error replies may not be documented.*

Danh sách này chưa đầy đủ. Các header dùng trong error reply có thể không được ghi lại ở đây.

| Name                      | Description                                                                                                                                                                                                                                                                                                                                            | Example                     | Version |
|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------|:--------|
| `Nats-Required-Api-Level` | Optional. The required API level for the JetStream request. Servers from version 2.11 will return an error if larger than the support API level.                                                                                                                                                                                                       | `2` (Integer value)         | 2.12    |
| `Nats-Request-Info`       | When messages cross account boundaries a header with origin information (account, user etc) may be added.                                                                                                                                                                                                                                              |                             | 2.2.0   |
| `Nats-Marker-Reason`      | When messages are removed from a KV where subject delete markers are supported, a delete marker will be placed. And notifications are sent to interested watchers. The message payload is empty and the removal reason is indicated through this header. See [ADR-48](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-48.md) | `MaxAge`, `Remove`, `Purge` | 2.11    |
| `Nats-Incr`               | Used in KV stores to atomically increment counter. Any valid integer (including 0) starting with a sign..  See [ADR-49](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-49.md)                                                                                                                                               | `+1`, `+42`, `-1`, `+0`     | 2.12    |
| `Nats-Counter-Sources`    | Tracking `Nats-Incr` when messages are sourced. For details see: [ADR-49](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-49.md)                                                                                                                                                                                             |                             | 2.12    |

## Mirror

> 🇬🇧 *Headers used for internal flow-control messages for a mirror.*

Các header dùng cho message flow-control nội bộ của mirror.

> 🇬🇧 *This is for information only and may change without notice.*

Phần này chỉ mang tính tham khảo và có thể thay đổi mà không báo trước.

| Name                    | Description | Example | Version |
| :---------------------- | :---------- | :------ | :------ |
| `Nats-Last-Consumer`    |             |         | 2.2.1   |
| `Nats-Last-Stream`      |             |         | 2.2.1   |
| `Nats-Consumer-Stalled` |             |         | 2.4.0   |
| `Nats-Response-Type`    |             |         | 2.6.4   |

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **consumer**: bên xử lý dữ liệu từ stream
- **header**: phần metadata kèm theo
- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **publisher**: bên gửi message
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)