---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/jetstream/model_deep_dive
title: Khám Phá Sâu Mô Hình JetStream
translated: true
translated_at: '2026-05-13T00:00:00+00:00'
---

# Khám Phá Sâu Mô Hình JetStream

## Giới Hạn, Retention và Policy của Stream

> 🇬🇧 *Streams store data on disk, but we cannot store all data forever, so we need ways to control their size automatically.*

Stream (luồng message lưu trữ liên tục) lưu dữ liệu trên đĩa, nhưng không thể lưu mãi mãi, nên cần cơ chế tự động kiểm soát kích thước.

> 🇬🇧 *There are 3 features that come into play when Streams decide how long they store data.*

Có 3 tính năng tác động đến quyết định lưu dữ liệu bao lâu của stream.

> 🇬🇧 *The `Retention Policy` describes based on what criteria a set will evict messages from its storage:*

`Retention Policy` mô tả tiêu chí để stream xóa message khỏi bộ lưu trữ:

| Retention Policy  | Description                                                                                                                                                                                                                                                                                                                                                                |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `LimitsPolicy`    | Limits are set for how many messages, how big the storage and how old messages may be.                                                                                                                                                                                                                                                                                     |
| `WorkQueuePolicy` | Messages are kept until they are consumed: meaning delivered ( by _the_ consumer filtering on the message's subject (in this mode of operation you can not have any overlapping consumers defined on the Stream - each subject captured by the stream can only have one consumer at a time)) to a subscribing application and explicitly acknowledged by that application. |
| `InterestPolicy`  | Messages are kept as long as there are Consumers on the stream (matching the message's subject if they are filtered consumers) for which the message has not yet been ACKed. Once all currently defined consumers have received explicit acknowledgement from a subscribing application for the message it is then removed from the stream.                                |

> 🇬🇧 *In all Retention Policies the basic limits apply as upper bounds, these are `MaxMsgs` for how many messages are kept in total, `MaxBytes` for how big the set can be in total and `MaxAge` for what is the oldest message that will be kept. These are the only limits in play with `LimitsPolicy` retention.*

Trong mọi Retention Policy, các giới hạn cơ bản luôn đóng vai trò giới hạn trên: `MaxMsgs` là tổng số message được giữ, `MaxBytes` là tổng dung lượng tối đa, và `MaxAge` là tuổi thọ tối đa của message. Đây là những giới hạn duy nhất áp dụng với retention `LimitsPolicy`.

> 🇬🇧 *One can then define additional ways a message may be removed from the Stream earlier than these limits. In `WorkQueuePolicy` the messages will be removed as soon as _the_ Consumer received an Acknowledgement. In `InterestPolicy` messages will be removed as soon as _all_ Consumers of the stream for that subject have received an Acknowledgement for the message.*

Ngoài ra, có thể định nghĩa thêm điều kiện xóa message sớm hơn giới hạn đó. Với `WorkQueuePolicy`, message bị xóa ngay khi consumer (bên xử lý dữ liệu từ stream) nhận được acknowledgement. Với `InterestPolicy`, message chỉ bị xóa khi _tất cả_ consumer của stream cho subject đó đã acknowledge message.

> 🇬🇧 *In both `WorkQueuePolicy` and `InterestPolicy` the age, size and count limits will still apply as upper bounds.*

Trong cả hai mode `WorkQueuePolicy` và `InterestPolicy`, các giới hạn về tuổi thọ, dung lượng và số lượng message vẫn áp dụng như giới hạn trên.

> 🇬🇧 *A final control is the Maximum Size any single message may have. NATS have it's own limit for maximum size (1 MiB by default), but you can say a Stream will only accept messages up to 1024 bytes using `MaxMsgSize`.*

Một tùy chọn cuối là kích thước tối đa cho mỗi message. NATS có giới hạn mặc định là 1 MiB, nhưng bạn có thể cấu hình stream chỉ chấp nhận message tối đa 1024 byte bằng `MaxMsgSize`.

> 🇬🇧 *The `Discard Policy` sets how messages are discarded when limits set by `LimitsPolicy` are reached. The `DiscardOld` option removes old messages making space for new, while `DiscardNew` refuses any new messages.*

`Discard Policy` quy định cách xử lý message khi đạt giới hạn của `LimitsPolicy`. Tùy chọn `DiscardOld` xóa message cũ để nhường chỗ cho message mới, còn `DiscardNew` từ chối mọi message mới.

> 🇬🇧 *The `WorkQueuePolicy` mode is a specialized mode where a message, once consumed and acknowledged, is removed from the Stream.*

Mode `WorkQueuePolicy` là mode đặc biệt: message sau khi được consume và acknowledge sẽ bị xóa khỏi stream.

## Deduplication Message

> 🇬🇧 *JetStream support idempotent message writes by ignoring duplicate messages as indicated by the `Nats-Msg-Id` header.*

JetStream hỗ trợ ghi message idempotent bằng cách bỏ qua các message trùng lặp dựa trên header (phần metadata kèm theo) `Nats-Msg-Id`.

```shell
nats req -H Nats-Msg-Id:1 ORDERS.new hello1
nats req -H Nats-Msg-Id:1 ORDERS.new hello2
nats req -H Nats-Msg-Id:1 ORDERS.new hello3
nats req -H Nats-Msg-Id:1 ORDERS.new hello4
```

> 🇬🇧 *Here we set a `Nats-Msg-Id:1` header which tells JetStream to ensure we do not have duplicates of this message - we only consult the message ID not the body.*

Ở đây ta đặt header `Nats-Msg-Id:1` để JetStream đảm bảo không có message trùng — hệ thống chỉ kiểm tra message ID, không kiểm tra nội dung.

```shell
nats stream info ORDERS
```

> 🇬🇧 *and in the output you can see that the duplicate publications were detected and only one message (the first one) is actually stored in the stream*

Trong output, có thể thấy các lần publish trùng đã được phát hiện và chỉ một message (lần đầu tiên) được lưu vào stream.

```
....
State:

            Messages: 1
               Bytes: 67 B
```

> 🇬🇧 *The default window to track duplicates in is 2 minutes, this can be set on the command line using `--dupe-window` when creating a stream, though we would caution against large windows.*

Cửa sổ thời gian mặc định để theo dõi trùng lặp là 2 phút, có thể điều chỉnh khi tạo stream bằng `--dupe-window`, nhưng nên tránh đặt cửa sổ quá lớn.

## Các Mô Hình Acknowledgement

> 🇬🇧 *Streams support acknowledging receiving a message, if you send a `Request()` to a subject covered by the configuration of the Stream the service will reply to you once it stored the message. If you just publish, it will not. A Stream can be set to disable Acknowledgements by setting `NoAck` to `true` in it's configuration.*

Stream hỗ trợ xác nhận nhận message: nếu bạn gửi `Request()` tới subject (chuỗi định danh message) thuộc phạm vi cấu hình của stream, service sẽ phản hồi sau khi lưu message. Nếu chỉ publish đơn thuần thì không có phản hồi. Stream có thể tắt acknowledgement bằng cách đặt `NoAck` thành `true`.

> 🇬🇧 *Consumers have 4 acknowledgement modes:*

Consumer có 4 mode acknowledgement:

| Mode             | Description                                                                                                                                             |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `AckExplicit`    | This requires every message to be specifically acknowledged, it's the only supported option for pull-based Consumers                                    |
| `AckAll`         | In this mode if you acknowledge message `100` it will also acknowledge message `1`-`99`, this is good for processing batches and to reduce ack overhead |
| `AckNone`        | No acknowledgements are supported                                                                                                                       |
| `AckFlowControl` | (2.14) Messages are acknowledged based on flow control. Primarily used for stream sourcing/mirroring using a durable consumer                           |

> 🇬🇧 *To understand how Consumers track messages we will start with a clean `ORDERS` Stream and `DISPATCH` Consumer.*

Để hiểu cách consumer theo dõi message, ta bắt đầu với stream `ORDERS` và consumer `DISPATCH` sạch.

```shell
nats str info ORDERS
```

```
...
Statistics:

            Messages: 0
               Bytes: 0 B
            FirstSeq: 0
             LastSeq: 0
    Active Consumers: 1
```

> 🇬🇧 *The Set is entirely empty*

Stream hoàn toàn rỗng.

```shell
nats con info ORDERS DISPATCH
```

```
...
State:

  Last Delivered Message: Consumer sequence: 1 Stream sequence: 1
    Acknowledgment floor: Consumer sequence: 0 Stream sequence: 0
        Pending Messages: 0
    Redelivered Messages: 0
```

> 🇬🇧 *The Consumer has no messages outstanding and has never had any (Consumer sequence is 1).*

Consumer không có message nào tồn đọng và chưa từng xử lý message nào (Consumer sequence là 1).

> 🇬🇧 *We publish one message to the Stream and see that the Stream received it:*

Ta publish một message vào stream và kiểm tra xác nhận:

```shell
nats pub ORDERS.processed "order 4"
```

```
Published 7 bytes to ORDERS.processed
$ nats str info ORDERS
...
Statistics:

            Messages: 1
               Bytes: 53 B
            FirstSeq: 1
             LastSeq: 1
    Active Consumers: 1
```

> 🇬🇧 *As the Consumer is pull-based, we can fetch the message, ack it, and check the Consumer state:*

Vì consumer là pull-based, ta fetch message, ack nó rồi kiểm tra trạng thái consumer:

```shell
nats con next ORDERS DISPATCH
```

```
--- received on ORDERS.processed
order 4

Acknowledged message

$ nats con info ORDERS DISPATCH
...
State:

  Last Delivered Message: Consumer sequence: 2 Stream sequence: 2
    Acknowledgment floor: Consumer sequence: 1 Stream sequence: 1
        Pending Messages: 0
    Redelivered Messages: 0
```

> 🇬🇧 *The message got delivered and acknowledged - `Acknowledgement floor` is `1` and `1`, the sequence of the Consumer is `2` which means its had only the one message through and got acked. Since it was acked, nothing is pending or redelivering.*

Message đã được giao và acknowledge — `Acknowledgement floor` là `1` và `1`, sequence của consumer là `2` nghĩa là chỉ có đúng một message đi qua và đã được acked. Vì đã acked, không có gì pending hay re-delivery.

> 🇬🇧 *We'll publish another message, fetch it but not Ack it this time and see the status:*

Ta publish thêm một message, fetch nhưng lần này không ack và quan sát trạng thái:

```shell
nats pub ORDERS.processed "order 5"
```

```
Published 7 bytes to ORDERS.processed
```

> 🇬🇧 *Get the next message from the consumer (but do not acknowledge it)*

Lấy message tiếp theo từ consumer (không acknowledge).

```shell
nats consumer next ORDERS DISPATCH --no-ack
```

```
--- received on ORDERS.processed
order 5
```

> 🇬🇧 *Show the consumer info*

Xem thông tin consumer.

```shell
nats consumer info ORDERS DISPATCH
```

```
State:

  Last Delivered Message: Consumer sequence: 3 Stream sequence: 3
    Acknowledgment floor: Consumer sequence: 1 Stream sequence: 1
        Pending Messages: 1
    Redelivered Messages: 0
```

> 🇬🇧 *Now we can see the Consumer has processed 2 messages (obs sequence is 3, next message will be 3) but the Ack floor is still 1 - thus 1 message is pending acknowledgement. Indeed this is confirmed in the `Pending messages`.*

Có thể thấy consumer đã xử lý 2 message (obs sequence là 3, message tiếp theo sẽ là 3) nhưng Ack floor vẫn là 1 — tức 1 message đang chờ acknowledgement. Điều này được xác nhận trong `Pending messages`.

> 🇬🇧 *If I fetch it again and again do not ack it:*

Nếu fetch lại lần nữa và vẫn không ack:

```shell
nats consumer next ORDERS DISPATCH --no-ack
```

```
--- received on ORDERS.processed
order 5
```

> 🇬🇧 *Show the consumer info again*

Xem thông tin consumer lại.

```shell
nats consumer info ORDERS DISPATCH
```

```
State:

  Last Delivered Message: Consumer sequence: 4 Stream sequence: 3
    Acknowledgment floor: Consumer sequence: 1 Stream sequence: 1
        Pending Messages: 1
    Redelivered Messages: 1
```

> 🇬🇧 *The Consumer sequence increases - each delivery attempt increases the sequence - and our redelivered count also goes up.*

Consumer sequence tăng lên — mỗi lần thử giao đều tăng sequence — và số lần re-delivery cũng tăng theo.

> 🇬🇧 *Finally, if I then fetch it again and ack it this time:*

Cuối cùng, nếu fetch lại và ack lần này:

```shell
nats consumer next ORDERS DISPATCH 
```

```
--- received on ORDERS.processed
order 5

Acknowledged message
```

> 🇬🇧 *Show the consumer info*

Xem thông tin consumer.

```shell
nats consumer info ORDERS DISPATCH
```

```
State:

  Last Delivered Message: Consumer sequence: 5 Stream sequence: 3
    Acknowledgment floor: Consumer sequence: 1 Stream sequence: 1
        Pending Messages: 0
    Redelivered Messages: 0
```

> 🇬🇧 *Having now Acked the message there are no more pending.*

Sau khi acked message, không còn gì pending nữa.

> 🇬🇧 *Additionally, there are a few types of acknowledgements:*

Ngoài ra, có một số loại acknowledgement:

| Type          | Bytes       | Description                                                                                                                        |
| ------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `AckAck`      | nil, `+ACK` | Acknowledges a message was completely handled                                                                                      |
| `AckNak`      | `-NAK`      | Signals that the message will not be processed now and processing can move onto the next message, NAK'd message will be retried    |
| `AckProgress` | `+WPI`      | When sent before the AckWait period indicates that work is ongoing and the period should be extended by another equal to `AckWait` |
| `AckNext`     | `+NXT`      | Acknowledges the message was handled and requests delivery of the next message to the reply subject. Only applies to Pull-mode.    |
| `AckTerm`     | `+TERM`     | Instructs the server to stop redelivery of a message without acknowledging it as successfully processed                            |

> 🇬🇧 *So far all of the examples were the `AckAck` type of acknowledgement, by replying to the Ack with the body as indicated in `Bytes` you can pick what mode of acknowledgement you want. Note that this description is documenting the internal JetStream protocol. Client libraries offer APIs for performing all the above acknowledgments using specific APIs where you don't worry about the internal protocol payloads.*

Tất cả các ví dụ trên đều dùng loại acknowledgement `AckAck`. Bằng cách reply vào Ack với nội dung tương ứng theo `Bytes`, bạn có thể chọn mode acknowledgement mong muốn. Lưu ý đây là tài liệu về internal protocol của JetStream. Các client library cung cấp API riêng để thực hiện mọi loại acknowledgement trên mà không cần quan tâm đến payload (nội dung chính của message) của internal protocol.

> 🇬🇧 *All of these acknowledgement modes, except `AckNext`, support double acknowledgement - if you set a reply subject when acknowledging the server will in turn acknowledge having received your ACK.*

Tất cả các mode acknowledgement, trừ `AckNext`, đều hỗ trợ double acknowledgement — nếu bạn đặt reply subject khi ack, server sẽ xác nhận lại việc nhận được ACK của bạn.

> 🇬🇧 *The `+NXT` acknowledgement can have a few formats: `+NXT 10` requests 10 messages and `+NXT {"no_wait": true}` which is the same data that can be sent in a Pull Request.*

Acknowledgement `+NXT` có vài định dạng: `+NXT 10` yêu cầu 10 message và `+NXT {"no_wait": true}` là dữ liệu tương tự có thể gửi trong Pull Request.

## Exactly Once Semantics

> 🇬🇧 *JetStream supports Exactly Once publication and consumption by combining Message Deduplication and double acks.*

JetStream hỗ trợ ngữ nghĩa Exactly Once cho cả publish lẫn consume bằng cách kết hợp Message Deduplication và double acks.

> 🇬🇧 *On the publishing side you can avoid duplicate message ingestion using the [Message Deduplication](https://docs.nats.io/using-nats/jetstream/model\_deep\_dive#message-deduplication) feature.*

Ở phía publish, bạn có thể tránh nhập message trùng lặp bằng tính năng [Message Deduplication](https://docs.nats.io/using-nats/jetstream/model\_deep\_dive#message-deduplication).

> 🇬🇧 *Consumers can be 100% sure a message was correctly processed by requesting the server Acknowledge having received your acknowledgement (sometimes referred to as double-acking) by calling the message's `AckSync()` (rather than `Ack()`) function which sets a reply subject on the Ack and waits for a response from the server on the reception and processing of the acknowledgement. If the response received from the server indicates success you can be sure that the message will never be re-delivered by the consumer (due to a loss of your acknowledgement).*

Consumer có thể chắc chắn 100% rằng message đã được xử lý đúng bằng cách yêu cầu server xác nhận lại việc nhận ACK (còn gọi là double-acking): gọi hàm `AckSync()` thay vì `Ack()` để đặt reply subject trên ACK và chờ phản hồi từ server. Nếu server phản hồi thành công, bạn có thể chắc chắn message sẽ không bao giờ bị re-deliver nữa (kể cả khi ACK bị mất).

## Vị Trí Bắt Đầu của Consumer

> 🇬🇧 *When setting up a Consumer you can decide where to start, the system supports the following for the `DeliverPolicy`:*

Khi thiết lập consumer, bạn có thể chọn điểm bắt đầu. Hệ thống hỗ trợ các tùy chọn sau cho `DeliverPolicy`:

| Policy              | Description                                                                |
| ------------------- | -------------------------------------------------------------------------- |
| `all`               | Delivers all messages that are available                                   |
| `last`              | Delivers the latest message, like a `tail -n 1 -f`                         |
| `new`               | Delivers only new messages that arrive after subscribe time                |
| `by_start_time`     | Delivers from a specific time onward. Requires `OptStartTime` to be set    |
| `by_start_sequence` | Delivers from a specific stream sequence. Requires `OptStartSeq` to be set |

> 🇬🇧 *Regardless of what mode you set, this is only the starting point. Once started it will always give you what you have not seen or acknowledged. So this is merely how it picks the very first message.*

Dù chọn mode nào, đây chỉ là điểm bắt đầu. Sau khi khởi động, consumer luôn giao các message bạn chưa thấy hoặc chưa acknowledge. Đây chỉ là cách chọn message đầu tiên.

> 🇬🇧 *Let's look at each of these, first we make a new Stream `ORDERS` and add 100 messages to it.*

Hãy xem từng tùy chọn — trước tiên tạo stream `ORDERS` và thêm 100 message vào đó.

> 🇬🇧 *Now create a `DeliverAll` pull-based Consumer:*

Tạo consumer pull-based `DeliverAll`:

```shell
nats consumer add ORDERS ALL --pull --filter ORDERS.processed --ack none --replay instant --deliver all 
nats consumer next ORDERS ALL
```

```
--- received on ORDERS.processed
order 1

Acknowledged message
```

> 🇬🇧 *Now create a `DeliverLast` pull-based Consumer:*

Tạo consumer pull-based `DeliverLast`:

```shell
nats consumer add ORDERS LAST --pull --filter ORDERS.processed --ack none --replay instant --deliver last
nats consumer next ORDERS LAST
```

```
--- received on ORDERS.processed
order 100

Acknowledged message
```

> 🇬🇧 *Now create a `MsgSetSeq` pull-based Consumer:*

Tạo consumer pull-based `MsgSetSeq`:

```shell
nats consumer add ORDERS TEN --pull --filter ORDERS.processed --ack none --replay instant --deliver 10
nats consumer next ORDERS TEN
```

```
--- received on ORDERS.processed
order 10

Acknowledged message
```

> 🇬🇧 *And finally a time-based Consumer. Let's add some messages a minute apart:*

Và cuối cùng là consumer dựa trên thời gian. Ta thêm một số message cách nhau 1 phút:

```shell
nats stream purge ORDERS
for i in 1 2 3
do
  nats pub ORDERS.processed "order ${i}"
  sleep 60
done
```

> 🇬🇧 *Then create a Consumer that starts 2 minutes ago:*

Sau đó tạo consumer bắt đầu từ 2 phút trước:

```shell
nats consumer add ORDERS 2MIN --pull --filter ORDERS.processed --ack none --replay instant --deliver 2m
nats consumer next ORDERS 2MIN
```

```
--- received on ORDERS.processed
order 2

Acknowledged message
```

## Ephemeral Consumers

> 🇬🇧 *So far, all the Consumers you have seen were Durable, meaning they exist even after you disconnect from JetStream. In our Orders scenario, though the `MONITOR` a Consumer could very well be a short-lived thing there just while an operator is debugging the system, there is no need to remember the last seen position if all you are doing is wanting to observe the real-time state.*

Tất cả consumer trong các ví dụ trên đều là Durable, nghĩa là chúng tồn tại kể cả sau khi ngắt kết nối khỏi JetStream. Trong kịch bản Orders, `MONITOR` consumer có thể chỉ cần tồn tại tạm thời trong khi operator debug — không cần nhớ vị trí đã xem nếu mục đích chỉ là quan sát trạng thái real-time.

> 🇬🇧 *In this case, we can make an Ephemeral Consumer by first subscribing to the delivery subject, then creating a durable and giving it no durable name. An Ephemeral Consumer exists as long as any subscription is active on its delivery subject. It is automatically be removed, after a short grace period to handle restarts, when there are no subscribers.*

Trong trường hợp này, ta tạo Ephemeral Consumer bằng cách subscribe vào delivery subject, rồi tạo một durable không đặt tên. Ephemeral Consumer tồn tại chừng nào còn có subscription active trên delivery subject. Nó sẽ tự xóa sau một khoảng thời gian chờ ngắn khi không còn subscriber (bên đăng ký nhận message) nào.

Terminal 1:

```shell
nats sub my.monitor
```

Terminal 2:

```shell
nats consumer add ORDERS --filter '' --ack none --target 'my.monitor' --deliver last --replay instant --ephemeral
```

> 🇬🇧 *The `--ephemeral` switch tells the system to make an Ephemeral Consumer.*

Tham số `--ephemeral` yêu cầu hệ thống tạo Ephemeral Consumer.

## Tốc Độ Giao Message của Consumer

> 🇬🇧 *Typically, what you want is if a new Consumer is made the selected messages are delivered to you as quickly as possible. You might want to replay messages at the rate they arrived though, meaning if messages first arrived 1 minute apart, and you make a new Consumer it will get the messages a minute apart.*

Thông thường, khi tạo consumer mới, message sẽ được giao càng nhanh càng tốt. Tuy nhiên, bạn cũng có thể muốn phát lại message theo tốc độ gốc — ví dụ nếu message ban đầu đến cách nhau 1 phút, consumer mới cũng sẽ nhận được message cách nhau 1 phút.

> 🇬🇧 *This is useful in load testing scenarios etc. This is called the `ReplayPolicy` and have values of `ReplayInstant` and `ReplayOriginal`.*

Tính năng này hữu ích trong các kịch bản load testing. Đây gọi là `ReplayPolicy` với các giá trị `ReplayInstant` và `ReplayOriginal`.

> 🇬🇧 *You can only set `ReplayPolicy` on push-based Consumers.*

Chỉ có thể đặt `ReplayPolicy` trên consumer push-based.

```shell
nats consumer add ORDERS REPLAY --target out.original --filter ORDERS.processed --ack none --deliver all --sample 100 --replay original
```

```
...
     Replay Policy: original
...
```

> 🇬🇧 *Now let's publish messages into the Set 10 seconds apart:*

Giờ ta publish message vào Set cách nhau 10 giây:

```shell
for i in 1 2 3                                                                                                                                                      <15:15:35
do
  nats pub ORDERS.processed "order ${i}"
  sleep 10
done
```

```
Published [ORDERS.processed] : 'order 1'
Published [ORDERS.processed] : 'order 2'
Published [ORDERS.processed] : 'order 3'
```

> 🇬🇧 *And when we consume them they will come to us 10 seconds apart:*

Và khi consume, chúng sẽ đến cách nhau 10 giây:

```shell
nats sub -t out.original
```

```
Listening on [out.original]
2020/01/03 15:17:26 [#1] Received on [ORDERS.processed]: 'order 1'
2020/01/03 15:17:36 [#2] Received on [ORDERS.processed]: 'order 2'
2020/01/03 15:17:46 [#3] Received on [ORDERS.processed]: 'order 3'
^C
```

## Ack Sampling

> 🇬🇧 *In the earlier sections we saw that samples are being sent to a monitoring system. Let's look at that in depth; how the monitoring system works and what it contains.*

Ở các phần trước, ta thấy rằng sample được gửi đến hệ thống monitoring. Hãy tìm hiểu sâu hơn: hệ thống monitoring hoạt động thế nào và chứa những gì.

> 🇬🇧 *As messages pass through a Consumer you'd be interested in knowing how many are being redelivered and how many times but also how long it takes for messages to be acknowledged.*

Khi message đi qua consumer, bạn sẽ muốn biết bao nhiêu message đang được re-delivery, bao nhiêu lần, và mất bao lâu để được acknowledge.

> 🇬🇧 *Consumers can sample Ack'ed messages for you and publish samples so your monitoring system can observe the health of a Consumer. We will add support for this to [NATS Surveyor](https://github.com/nats-io/nats-surveyor).*

Consumer có thể lấy mẫu các message đã được acked và publish (bên gửi message) sample đó để hệ thống monitoring theo dõi sức khỏe của consumer. Tính năng này sẽ được tích hợp vào [NATS Surveyor](https://github.com/nats-io/nats-surveyor).

### Cấu Hình

> 🇬🇧 *You can configure a Consumer for sampling bypassing the `--sample 80` option to `nats consumer add`, this tells the system to sample 80% of Acknowledgements.*

Bạn có thể cấu hình consumer để lấy mẫu bằng cách đặt tùy chọn `--sample 80` thành `nats consumer add`, yêu cầu hệ thống lấy mẫu 80% acknowledgement.

> 🇬🇧 *When viewing info of a Consumer you can tell if it's sampled or not:*

Khi xem thông tin consumer, bạn có thể biết nó có được lấy mẫu hay không:

```shell
nats consumer info ORDERS NEW
```

> 🇬🇧 *Output contains*

Output chứa:

```
...
     Sampling Rate: 100
...
```

## Storage Overhead

> 🇬🇧 *JetStream file storage is very efficient, storing as little extra information about the message as possible.*

JetStream lưu trữ file rất hiệu quả, giữ thông tin phụ trợ về message ở mức tối thiểu.

> 🇬🇧 *We do store some message data with each message, namely:*

Dữ liệu được lưu kèm mỗi message gồm:

* Message headers
* The subject it was received on
* The time it was received
* The message payload
* A hash of the message
* The message sequence
* A few other bits like the length of the subject and the length of headers

> 🇬🇧 *Without any headers the size is:*

Khi không có header, kích thước là:

```
length of the message record (4bytes) + seq(8) + ts(8) + subj_len(2) + subj + msg + hash(8)
```

> 🇬🇧 *A 5 byte `hello` message without headers will take 39 bytes.*

Một message `hello` 5 byte không có header sẽ chiếm 39 byte.

> 🇬🇧 *With headers:*

Khi có header:

```
length of the message record (4bytes) + seq(8) + ts(8) + subj_len(2) + subj + hdr_len(4) + hdr + msg + hash(8)
```

> 🇬🇧 *So if you are publishing many small messages the overhead will be, relatively speaking, quite large, but for larger messages the overhead is very small. If you publish many small messages it's worth trying to optimize the subject length.*

Nếu publish nhiều message nhỏ, overhead tương đối khá lớn; ngược lại với message lớn, overhead rất nhỏ. Khi publish nhiều message nhỏ, nên cân nhắc tối ưu độ dài subject.

## Thuật ngữ trong bài

- **consumer**: bên xử lý dữ liệu từ stream
- **header**: phần metadata kèm theo
- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **publisher**: bên gửi message
- **request**: yêu cầu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message