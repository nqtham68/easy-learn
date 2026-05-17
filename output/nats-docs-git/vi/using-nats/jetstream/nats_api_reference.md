---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/jetstream/nats_api_reference
title: Tài liệu tham khảo NATS API
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Tài liệu tham khảo NATS API

> 🇬🇧 *The normal way to use JetStream is through the NATS client libraries which expose a set of JetStream functions that you can use directly in your programs. But that is not the only way you can interact with the JetStream infrastructure programmatically. Just like core NATS has a wire protocol on top of TCP, the JetStream enabled nats-server(s) expose a set of Services over core NATS.*

Cách thông thường để dùng JetStream là thông qua các thư viện NATS client, vốn cung cấp sẵn các hàm JetStream để gọi trực tiếp trong code. Tuy nhiên, đây không phải cách duy nhất để tương tác lập trình với hạ tầng JetStream. Tương tự như core NATS có wire protocol trên TCP, các nats-server hỗ trợ JetStream cũng expose một tập Service qua core NATS.

## Tham khảo

> 🇬🇧 *All of these subjects are found as constants in the NATS Server source, so for example the subject `$JS.API.STREAM.LIST` is represented by `api.JSApiStreamList` constant in the nats-server source. Tables below will reference these constants and payload related data structures.*

Tất cả các subject (chuỗi định danh message) này đều được định nghĩa dưới dạng hằng số trong source code NATS Server. Ví dụ, subject `$JS.API.STREAM.LIST` được đại diện bởi hằng số `api.JSApiStreamList` trong source nats-server. Các bảng bên dưới sẽ tham chiếu các hằng số này cùng với các cấu trúc dữ liệu liên quan đến payload (nội dung chính của message).

> 🇬🇧 *Note that if the resources you're trying to access have a JetStream [domain](../../running-a-nats-service/configuration/leafnodes/jetstream_leafnodes.md#leaf-nodes) associated with them, then the subject prefix will be `$JS.{domain}.API` rather than `$JS.API`.*

Lưu ý: nếu các tài nguyên cần truy cập có liên kết với một JetStream [domain](../../running-a-nats-service/configuration/leafnodes/jetstream_leafnodes.md#leaf-nodes), prefix của subject sẽ là `$JS.{domain}.API` thay vì `$JS.API`.

## Xử lý lỗi

> 🇬🇧 *The APIs used for administrative tools all respond with standardised JSON and these include errors.*

Các API (giao diện lập trình) dùng cho công cụ quản trị đều trả về JSON chuẩn hóa, bao gồm cả thông tin lỗi.

```shell
nats req '$JS.API.STREAM.INFO.nonexisting' ''
```
```text
Published 11 bytes to $JS.API.STREAM.INFO.nonexisting
Received  [_INBOX.lcWgjX2WgJLxqepU0K9pNf.mpBW9tHK] : {
  "type": "io.nats.jetstream.api.v1.stream_info_response",
  "error": {
    "code": 404,
    "description": "stream not found"
  }
}
```

```shell
nats req '$JS.STREAM.INFO.ORDERS' ''
```
```text
Published 6 bytes to $JS.STREAM.INFO.ORDERS
Received  [_INBOX.fwqdpoWtG8XFXHKfqhQDVA.vBecyWmF] : '{
  "type": "io.nats.jetstream.api.v1.stream_info_response",
  "config": {
    "name": "ORDERS",
  ...
}
```

> 🇬🇧 *Here the responses include a `type` which can be used to find the JSON Schema for each response.*

Các response ở đây bao gồm trường `type` dùng để tra cứu JSON Schema tương ứng với từng loại response.

> 🇬🇧 *Non-admin APIs - like those for adding a message to the stream will respond with `-ERR` or `+OK` with an optional reason after.*

Các API không phải admin — chẳng hạn API thêm message vào stream (luồng message lưu trữ liên tục) — sẽ phản hồi bằng `-ERR` hoặc `+OK` kèm theo lý do tùy chọn.

## Admin API

> 🇬🇧 *All of the admin actions the `nats` CLI can do fall in the sections below. The API structure is kept in the `api` package in the `jsm.go` repository.*

Toàn bộ các thao tác admin mà CLI `nats` hỗ trợ đều nằm trong các phần bên dưới. Cấu trúc API được lưu trong package `api` thuộc repository `jsm.go`.

> 🇬🇧 *Subjects that end in `T` like `api.JSApiConsumerCreateT` are formats and would need to have the Stream Name and in some cases also the Consumer name interpolated into them. In this case `t := fmt.Sprintf(api.JSApiConsumerCreateT, streamName)` to get the final subject.*

Các subject kết thúc bằng `T` như `api.JSApiConsumerCreateT` là dạng template — cần điền tên Stream và trong một số trường hợp là cả tên Consumer. Ví dụ, điền vào để được `t := fmt.Sprintf(api.JSApiConsumerCreateT, streamName)` là subject cuối cùng.

> 🇬🇧 *The command `nats events` will show you an audit log of all API access events which includes the full content of each admin request, use this to view the structure of messages the `nats` command sends.*

Lệnh `nats events` hiển thị audit log của tất cả sự kiện truy cập API, bao gồm toàn bộ nội dung của từng admin request. Dùng lệnh này để xem cấu trúc message mà lệnh `nats` gửi đi.

> 🇬🇧 *The API uses JSON for inputs and outputs, all the responses are typed using a `type` field which indicates their Schema. A JSON Schema repository can be found in `nats-io/jsm.go/schemas`.*

API sử dụng JSON cho cả input và output. Mọi response đều có trường `type` chỉ định Schema tương ứng. Kho JSON Schema được lưu tại `nats-io/jsm.go/schemas`.

### Thông tin chung

| Subject | Constant | Description | Request Payload | Response Payload |
| :--- | :--- | :--- | :--- | :--- |
| `$JS.API.INFO` | `api.JSApiAccountInfo` | Retrieves stats and limits about your account | empty payload | `api.JetStreamAccountStats` |

### Streams

| Subject | Constant | Description | Request Payload | Response Payload |
| :--- | :--- | :--- | :--- | :--- |
| `$JS.API.STREAM.LIST` | `api.JSApiStreamList` | Paged list known Streams including all their current information | `api.JSApiStreamListRequest` | `api.JSApiStreamListResponse` |
| `$JS.API.STREAM.NAMES` | `api.JSApiStreamNames` | Paged list of Streams | `api.JSApiStreamNamesRequest` | `api.JSApiStreamNamesResponse` |
| `$JS.API.STREAM.CREATE.*` | `api.JSApiStreamCreateT` | Creates a new Stream | `api.StreamConfig` | `api.JSApiStreamCreateResponse` |
| `$JS.API.STREAM.UPDATE.*` | `api.JSApiStreamUpdateT` | Updates an existing Stream with new config | `api.StreamConfig` | `api.JSApiStreamUpdateResponse` |
| `$JS.API.STREAM.INFO.*` | `api.JSApiStreamInfoT` | Information about config and state of a Stream | empty payload, Stream name in subject | `api.JSApiStreamInfoResponse` |
| `$JS.API.STREAM.DELETE.*` | `api.JSApiStreamDeleteT` | Deletes a Stream and all its data | empty payload, Stream name in subject | `api.JSApiStreamDeleteResponse` |
| `$JS.API.STREAM.PURGE.*` | `api.JSApiStreamPurgeT` | Purges all of the data in a Stream, leaves the Stream | empty payload, Stream name in subject | `api.JSApiStreamPurgeResponse` |
| `$JS.API.STREAM.MSG.DELETE.*` | `api.JSApiMsgDeleteT` | Deletes a specific message in the Stream by sequence, useful for GDPR compliance | `api.JSApiMsgDeleteRequest` | `api.JSApiMsgDeleteResponse` |
| `$JS.API.STREAM.MSG.GET.*` | `api.JSApiMsgGetT` | Retrieves a specific message from the stream | `api.JSApiMsgGetRequest` | `api.JSApiMsgGetResponse` |
| `$JS.API.STREAM.SNAPSHOT.*` | `api.JSApiStreamSnapshotT` | Initiates a streaming backup of a streams data | `api.JSApiStreamSnapshotRequest` | `api.JSApiStreamSnapshotResponse` |
| `$JS.API.STREAM.RESTORE.*` | `api.JSApiStreamRestoreT` | Initiates a streaming restore of a stream | `{}` | `api.JSApiStreamRestoreResponse` |

### Consumers

| Subject                               | Constant | Description                                                                     | Request Payload | Response Payload |
|:--------------------------------------| :--- |:--------------------------------------------------------------------------------| :--- | :--- |
| `$JS.API.CONSUMER.CREATE.<stream>`           | `api.JSApiConsumerCreateT` | Create an ephemeral consumer                                                    | `api.ConsumerConfig` | `api.JSApiConsumerCreateResponse` |
| `$JS.API.CONSUMER.DURABLE.CREATE.<stream>.<consumer>` | `api.JSApiDurableCreateT` | Create a consumer                                                              | `api.ConsumerConfig` | `api.JSApiConsumerCreateResponse` |
| `$JS.API.CONSUMER.CREATE.<stream>.<consumer>.<filter>` | `api.JSApiConsumerCreateExT` | Create a consumer (server 2.9+) | `api.CreateConsumerRequest` | `api.JSApiConsumerCreateResponse` |
| `$JS.API.CONSUMER.LIST.<stream>`             | `api.JSApiConsumerListT` | Paged list of known consumers including their current info for a given stream | `api.JSApiConsumerListRequest` | `api.JSApiConsumerListResponse` |
| `$JS.API.CONSUMER.NAMES.<stream>`            | `api.JSApiConsumerNamesT` | Paged list of known consumer names for a given stream | `api.JSApiConsumerNamesRequest` | `api.JSApiConsumerNamesResponse` |
| `$JS.API.CONSUMER.INFO.<stream>.<consumer>`           | `api.JSApiConsumerInfoT` | Information about a specific consumer by name | empty payload | `api.JSApiConsumerInfoResponse` |
| `$JS.API.CONSUMER.DELETE.<stream>.<consumer>` | `api.JSApiConsumerDeleteT` | Deletes a Consumer                                                             | empty payload | `api.JSApiConsumerDeleteResponse` |
| `$JS.FC.<stream>.>` | N/A | Consumer to subscriber flow control replies for `PUSH` consumer. Also used for sourcing and mirroring, which are implemented as `PUSH` consumers. If this subject is not forwarded, the consumer my stall under high load.| empty payload |  N/A |
| `$JSC.R.<uid>` | N/A | Reply subject used by source and mirror consumer create request | Consumer info |  N/A |
| `$JS.S.<uid>` | N/A | Default delivery subject for sourced streams. Can be overwritten by the `deliver` attribute in the source configuration. | Message data |  N/A |
| `$JS.M.<uid>` | N/A | Default delivery subject for mirroed streams. Can be overwritten by the `deliver` attribute in the source configuration. | Message data |  N/A |
| `$JS.ACK.<stream>.>` | N/A | Acknowledgments for `PULL` consumers. When this subject is not forwarded, `PULL` consumers in acknowledgment modes `all` or `explicit` will fail. | empty payload |  reply subject |


### Stream Source và Mirror

> 🇬🇧 *Sourcing and mirroring streams use 3 inbound and 2 outbound subjects to establish and control the data flow. When setting permissions or creating export/import agreements all 5 subjects may need to be considered.*

Sourcing và mirroring stream sử dụng 3 subject inbound và 2 subject outbound để thiết lập và kiểm soát luồng dữ liệu. Khi cấu hình permission hoặc tạo thỏa thuận export/import, cần cân nhắc cả 5 subject này.

> 🇬🇧 *Notes:*
> - *There are two variants to the consumer-create subject depending on the number of filters.*
> - *In some setup a domain prefix may be present e.g. `$JS.<domain>.API.CONSUMER.CREATE.<stream>.>`*

Lưu ý:
* Subject consumer-create có 2 biến thể tùy theo số lượng filter.
* Trong một số cấu hình, prefix domain có thể xuất hiện, ví dụ `$JS.<domain>.API.CONSUMER.CREATE.<stream>.>`


| Subject                               | Direction | Description   | Reply | 
|:--------------------------------------| :--- |:--------------------------------------------------------------------------------| :--- | 
| `$JS.API.CONSUMER.CREATE.<stream>.>`  and/or  `$JS.API.CONSUMER.CREATE.<stream>`     | outbound | Create an ephemeral consumer to deliver pending messages. Note that this subject may be prefixed with a JetStream domain  `$JS.<domain>.API.CONSUMER.CREATE.<stream>.<consumer>`. <br>The consumer create comes in 2 flavors depending on the number of filter subjects:<br>* `$JS.API.CONSUMER.CREATE.<stream>` - When there is no filter or there are multiple filters.<br> * `$JS.API.CONSUMER.CREATE.<stream>.<consumer>.<filter subject>` - When there is exactly one filter subject                              | service request with `$JSC.R.<uid>` as reply subject |
|`$JS.FC.<stream>.>`  | outbound | Flow control messages. Will on slow routes or when the target cannot keep up with the message flow.   | service request with `$JSC.R.<uid>` as reply subject |
|`$JSC.R.<uid>`           | inbound | Reply to consumer creation request  | reply message to service request |
|`$JS.S.<uid>` (source) OR `$JS.M.<uid>` (mirror) OR `<custom deliver subject>`          | inbound | Message data and heartbeats  | message stream|

#### Heartbeat và Retry

> 🇬🇧 *The stream from which data is sourced/mirrored MAY NOT be reachable. It may not have been created yet OR the route may be down. This does not prevent the source/mirror agreement from being created.*

Stream nguồn dữ liệu được sourced/mirrored có thể không truy cập được — có thể chưa được tạo hoặc route đang bị ngắt. Điều này không ngăn việc tạo thỏa thuận source/mirror.

> 🇬🇧 *- The target stream will try to create a consumer every 10s to 60s. (This value may change in the future or may be configurable). Note that delivery may therefore only resume after a short delay.*
> *- For active consumers heartbeats are sent at a rate of 1/s.*

* Stream đích sẽ thử tạo consumer (bên xử lý dữ liệu từ stream) cứ mỗi 10–60 giây (giá trị này có thể thay đổi hoặc cho phép cấu hình). Vì vậy, việc delivery có thể chỉ tiếp tục sau một khoảng trễ ngắn.
* Với các consumer đang hoạt động, heartbeat được gửi với tốc độ 1/s.


#### Ràng buộc và Giới hạn

> 🇬🇧 *- Do not delete and recreate the original stream! Please flush/purge the stream instead. The target stream remembers the last sequence id to be delivered. A delete will reset the sequence ID.*
> *- `$JS.FC.<stream>.>` - The flow control subject is NOT prefixed with a JetStream domain. This creates a limitation where identically named streams in different domains cannot be reliably sourced/mirrored into the same account. Please create unique stream names to avoid this limitation.*

* Không được xóa rồi tạo lại stream gốc! Hãy flush/purge stream thay thế. Stream đích ghi nhớ sequence ID cuối cùng đã được delivery — việc xóa sẽ reset sequence ID đó.
* `$JS.FC.<stream>.>` — Subject flow control KHÔNG có prefix JetStream domain. Điều này tạo ra giới hạn: các stream trùng tên ở các domain khác nhau không thể được sourced/mirrored vào cùng một account một cách đáng tin cậy. Hãy đặt tên stream duy nhất để tránh giới hạn này.

### ACL

> 🇬🇧 *When using the subjects-based ACL, please note the patterns in the subjects grouped by purpose below.*

Khi sử dụng ACL dựa trên subject, hãy chú ý các pattern subject được nhóm theo mục đích bên dưới.

Thông tin chung

```text
$JS.API.INFO
```

Stream Admin
```text
$JS.API.STREAM.CREATE.<stream>
$JS.API.STREAM.UPDATE.<stream>
$JS.API.STREAM.DELETE.<stream>
$JS.API.STREAM.INFO.<stream>
$JS.API.STREAM.PURGE.<stream>
$JS.API.STREAM.LIST
$JS.API.STREAM.NAMES
$JS.API.STREAM.MSG.DELETE.<stream>
$JS.API.STREAM.MSG.GET.<stream>
$JS.API.STREAM.SNAPSHOT.<stream>
$JS.API.STREAM.RESTORE.<stream>
```
Consumer Admin
```text
$JS.API.CONSUMER.CREATE.<stream>
$JS.API.CONSUMER.DURABLE.CREATE.<stream>.<consumer>
$JS.API.CONSUMER.DELETE.<stream>.<consumer>
$JS.API.CONSUMER.INFO.<stream>.<consumer>
$JS.API.CONSUMER.LIST.<stream>
$JS.API.CONSUMER.NAMES.<stream>
```

Luồng message của Consumer

```text
$JS.API.CONSUMER.MSG.NEXT.<stream>.<consumer>
$JS.SNAPSHOT.RESTORE.<stream>.<msg id>
$JS.ACK.<stream>.<consumer>.x.x.x
$JS.SNAPSHOT.ACK.<stream>.<msg id>
$JS.FC.<stream>.>
```

Sự kiện và Advisory tùy chọn:

```text
$JS.EVENT.METRIC.CONSUMER_ACK.<stream>.<consumer>
$JS.EVENT.ADVISORY.CONSUMER.MAX_DELIVERIES.<stream>.<consumer>
$JS.EVENT.ADVISORY.CONSUMER.MSG_TERMINATED.<stream>.<consumer>
$JS.EVENT.ADVISORY.STREAM.CREATED.<stream>
$JS.EVENT.ADVISORY.STREAM.DELETED.<stream>
$JS.EVENT.ADVISORY.STREAM.UPDATED.<stream>
$JS.EVENT.ADVISORY.CONSUMER.CREATED.<stream>.<consumer>
$JS.EVENT.ADVISORY.CONSUMER.DELETED.<stream>.<consumer>
$JS.EVENT.ADVISORY.STREAM.SNAPSHOT_CREATE.<stream>
$JS.EVENT.ADVISORY.STREAM.SNAPSHOT_COMPLETE.<stream>
$JS.EVENT.ADVISORY.STREAM.RESTORE_CREATE.<stream>
$JS.EVENT.ADVISORY.STREAM.RESTORE_COMPLETE.<stream>
$JS.EVENT.ADVISORY.STREAM.LEADER_ELECTED.<stream>
$JS.EVENT.ADVISORY.STREAM.QUORUM_LOST.<stream>
$JS.EVENT.ADVISORY.CONSUMER.LEADER_ELECTED.<stream>.<consumer>
$JS.EVENT.ADVISORY.CONSUMER.QUORUM_LOST.<stream>.<consumer>
$JS.EVENT.ADVISORY.API
```

> 🇬🇧 *This design allows you to easily create ACL rules that limit users to a specific Stream or Consumer and to specific verbs for administration purposes. For ensuring only the receiver of a message can Ack it we have response permissions ensuring you can only Publish to Response subject for messages you received.*

Thiết kế này cho phép dễ dàng tạo các quy tắc ACL giới hạn người dùng vào một Stream hoặc Consumer cụ thể, với các verb quản trị nhất định. Để đảm bảo chỉ người nhận message mới có thể Ack, hệ thống có response permission — chỉ cho phép Publish đến reply subject của message mà mình đã nhận.

## Xác nhận nhận Message

> 🇬🇧 *Messages that need acknowledgment will have a Reply subject set, something like `$JS.ACK.ORDERS.test.1.2.2`, this is the prefix defined in `api.JetStreamAckPre` followed by `<stream>.<consumer>.<delivered count>.<stream sequence>.<consumer sequence>.<timestamp>.<pending messages>`.*

Message cần xác nhận sẽ có Reply subject được đặt, ví dụ `$JS.ACK.ORDERS.test.1.2.2` — đây là prefix được định nghĩa trong `api.JetStreamAckPre` theo sau bởi `<stream>.<consumer>.<delivered count>.<stream sequence>.<consumer sequence>.<timestamp>.<pending messages>`.

> 🇬🇧 *JetStream and the consumer (including sourced and mirrored streams) may exchange flow control messages. A message with the header: `NATS/1.0 100 FlowControl Request` must be replied to, otherwise the consumer may stall. The reply subjects looks like: `$JS.FC.orders.6i5h0GiQ.ep3Y`*

JetStream và consumer (bao gồm cả stream được sourced và mirrored) có thể trao đổi các flow control message. Message có header `NATS/1.0 100 FlowControl Request` bắt buộc phải được reply, nếu không consumer có thể bị stall. Reply subject trông như sau: `$JS.FC.orders.6i5h0GiQ.ep3Y`

> 🇬🇧 *In all of the Synadia maintained API's you can simply do `msg.Respond(nil)` \(or language equivalent\) which will send nil to the reply subject.*

Trong tất cả các API do Synadia duy trì, bạn có thể đơn giản gọi `msg.Respond(nil)` (hoặc tương đương trong ngôn ngữ đang dùng) để gửi nil đến reply subject.

## Lấy Message Tiếp Theo Từ Pull-based Consumer

> 🇬🇧 *If you have a pull-based Consumer you can send a standard NATS Request to `$JS.API.CONSUMER.MSG.NEXT.<stream>.<consumer>`, here the format is defined in `api.JetStreamRequestNextT` and requires populating using `fmt.Sprintf()`.*

Nếu dùng pull-based Consumer, bạn có thể gửi một NATS Request chuẩn đến `$JS.API.CONSUMER.MSG.NEXT.<stream>.<consumer>`. Format được định nghĩa trong `api.JetStreamRequestNextT` và cần điền thông qua `fmt.Sprintf()`.

```shell
nats req '$JS.API.CONSUMER.MSG.NEXT.ORDERS.test' '1'
```
```text
Published 1 bytes to $JS.API.CONSUMER.MSG.NEXT.ORDERS.test
Received  [js.1] : 'message 1'
```

> 🇬🇧 *Here we ask for just 1 message - `nats req` only shows 1 - but you can fetch a batch of messages by varying the argument. This combines well with the `AckAll` Ack policy.*

Ở đây chúng ta chỉ yêu cầu 1 message — `nats req` chỉ hiển thị 1 — nhưng bạn có thể fetch một batch message bằng cách thay đổi argument. Cách này kết hợp tốt với Ack policy `AckAll`.

> 🇬🇧 *The above request for the next message will stay in the server for as long as the client is connected and future pulls from the same client will accumulate on the server, meaning if you ask for 1 message 100 times and 1000 messages arrive you'll get sent 100 messages not 1.*

Request lấy message tiếp theo ở trên sẽ tồn tại trên server chừng nào client còn kết nối. Các pull tiếp theo từ cùng client sẽ tích lũy trên server — nghĩa là nếu bạn yêu cầu 1 message 100 lần và có 1000 message đến, bạn sẽ nhận được 100 message chứ không phải 1.

> 🇬🇧 *This is often not desired, pull consumers support a mode where a JSON document is sent describing the pull request.*

Đây thường không phải hành vi mong muốn. Pull consumer hỗ trợ một chế độ trong đó một JSON document được gửi đi mô tả pull request.

```json
{
  "expires": 7000000000,
  "batch": 10
}
```

> 🇬🇧 *This requests 10 messages and asks the server to keep this request for 7 seconds, this is useful when you poll the server frequently and do not want the pull requests to accumulate on the server. Set the expire time to now + your poll frequency.*

Đoạn này yêu cầu 10 message và yêu cầu server giữ request trong 7 giây — hữu ích khi bạn poll server thường xuyên và không muốn các pull request tích lũy. Đặt expire time bằng thời điểm hiện tại cộng với tần suất poll của bạn.

```json
{
  "batch": 10,
  "no_wait": true
}
```

> 🇬🇧 *Here we see a second format of the Pull request that will not store the request on the queue at all but when there are no messages to deliver will send a nil bytes message with a `Status` header of `404`, this way you can know when you reached the end of the stream for example. A `409` is returned if the Consumer has reached `MaxAckPending` limits.*

Đây là format thứ hai của Pull request — không lưu request vào queue. Khi không có message nào để delivery, server sẽ gửi một nil bytes message với header `Status` là `404`, giúp bạn biết khi nào đã đến cuối stream chẳng hạn. Nếu Consumer đã đạt đến giới hạn `MaxAckPending`, một `409` sẽ được trả về.

```shell
nats req '$JS.API.CONSUMER.MSG.NEXT.ORDERS.NEW' '{"no_wait": true, "batch": 10}'
 ```
```text
13:45:30 Sending request on "$JS.API.CONSUMER.MSG.NEXT.ORDERS.NEW"
13:45:30 Received on "_INBOX.UKQGqq0W1EKl8inzXU1naH.XJiawTRM" rtt 594.908µs
13:45:30 Status: 404
13:45:30 Description: No Messages
```

## Fetching From a Stream By Sequence

If you know the Stream sequence of a message, you can fetch it directly, this does not support acks. Do a Request\(\) to `$JS.API.STREAM.MSG.GET.ORDERS` sending it the message sequence as payload. Here the prefix is defined in `api.JetStreamMsgBySeqT` which also requires populating using `fmt.Sprintf()`.

```shell
nats req '$JS.API.STREAM.MSG.GET.ORDERS' '{"seq": 1}'
```
```text
Published 1 bytes to $JS.STREAM.ORDERS.MSG.BYSEQ
Received  [_INBOX.cJrbzPJfZrq8NrFm1DsZuH.k91Gb4xM] : '{
  "type": "io.nats.jetstream.api.v1.stream_msg_get_response",
  "message": {
    "subject": "x",
    "seq": 1,
    "data": "aGVsbG8=",
    "time": "2020-05-06T13:18:58.115424+02:00"
  }
}'
```

> 🇬🇧 *The Subject shows where the message was received, Data is base64 encoded and Time is when it was received.*

Subject cho thấy nơi message được nhận, Data được mã hóa base64 và Time là thời điểm nhận.

## Consumer Sample

> 🇬🇧 *Samples are published to a specific subject per Consumer, something like `$JS.EVENT.METRIC.CONSUMER_ACK.<stream>.<consumer>` you can subscribe to that and get `api.ConsumerAckMetric` messages in JSON format. The prefix is defined in `api.JetStreamMetricConsumerAckPre`.*

Sample được publish đến một subject cụ thể cho từng Consumer, ví dụ `$JS.EVENT.METRIC.CONSUMER_ACK.<stream>.<consumer>`. Bạn có thể subscribe vào đó và nhận các message `api.ConsumerAckMetric` ở định dạng JSON. Prefix được định nghĩa trong `api.JetStreamMetricConsumerAckPre`.

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **permission**: quyền truy cập
- **queue**: hàng đợi message
- **request**: yêu cầu
- **response**: phản hồi
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)