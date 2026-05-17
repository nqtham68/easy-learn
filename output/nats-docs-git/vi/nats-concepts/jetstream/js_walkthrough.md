---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/jetstream/js_walkthrough
title: Hướng dẫn thực hành NATS JetStream
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Hướng dẫn thực hành NATS JetStream

> 🇬🇧 *The following is a small walkthrough on creating a stream and a consumer and interacting with the stream using the [nats cli](https://github.com/nats-io/natscli).*

Dưới đây là hướng dẫn ngắn gọn về cách tạo stream (luồng message lưu trữ liên tục) và consumer (bên xử lý dữ liệu từ stream), đồng thời tương tác với stream bằng [nats cli](https://github.com/nats-io/natscli).


## Điều kiện tiên quyết: bật JetStream

> 🇬🇧 *If you are running a local `nats-server` stop it and restart it with JetStream enabled using `nats-server -js` (if that's not already done)*

Nếu đang chạy `nats-server` cục bộ, hãy dừng lại và khởi động lại với JetStream được bật bằng cách dùng `nats-server -js` (nếu chưa làm).

> 🇬🇧 *You can then check that JetStream is enabled by using*

Sau đó kiểm tra JetStream đã được bật chưa bằng lệnh:

```shell
nats account info
```
```text
Account Information

                           User: 
                        Account: $G
                        Expires: never
                      Client ID: 5
                      Client IP: 127.0.0.1
                            RTT: 128µs
              Headers Supported: true
                Maximum Payload: 1.0 MiB
                  Connected URL: nats://127.0.0.1:4222
              Connected Address: 127.0.0.1:4222
            Connected Server ID: NAMR7YBNZA3U2MXG2JH3FNGKBDVBG2QTMWVO6OT7XUSKRINKTRFBRZEC
       Connected Server Version: 2.11.0-dev
                 TLS Connection: no

JetStream Account Information:

Account Usage:

                        Storage: 0 B
                         Memory: 0 B
                        Streams: 0
                      Consumers: 0

Account Limits:

            Max Message Payload: 1.0 MiB

  Tier: Default:

      Configuration Requirements:

        Stream Requires Max Bytes Set: false
         Consumer Maximum Ack Pending: Unlimited

      Stream Resource Usage Limits:

                               Memory: 0 B of Unlimited
                    Memory Per Stream: Unlimited
                              Storage: 0 B of Unlimited
                   Storage Per Stream: Unlimited
                              Streams: 0 of Unlimited
                            Consumers: 0 of Unlimited
```

> 🇬🇧 *If you see the below then JetStream is _not_ enabled*

Nếu thấy kết quả bên dưới thì JetStream _chưa_ được bật:

```text
JetStream Account Information:

   JetStream is not supported in this account
```

## 1. Tạo một stream

> 🇬🇧 *Let's start by creating a stream to capture and store the messages published on the subject "foo".*

Bắt đầu bằng cách tạo một stream để ghi lại và lưu trữ các message được publish lên subject (chuỗi định danh message) "foo".

> 🇬🇧 *Enter `nats stream add <Stream name>` (in the examples below we will name the stream "my_stream"), then enter "foo" as the subject name and hit return to use the defaults for all the other stream attributes:*

Nhập `nats stream add <Stream name>` (trong ví dụ này stream được đặt tên là "my_stream"), sau đó nhập "foo" làm tên subject rồi nhấn Enter để dùng giá trị mặc định cho các thuộc tính còn lại:

```shell
nats stream add my_stream
```
```text
? Subjects foo
? Storage file
? Replication 1
? Retention Policy Limits
? Discard Policy Old
? Stream Messages Limit -1
? Per Subject Messages Limit -1
? Total Stream Size -1
? Message TTL -1
? Max Message Size -1
? Duplicate tracking time window 2m0s
? Allow message Roll-ups No
? Allow message deletion Yes
? Allow purging subjects or the entire stream Yes
Stream my_stream was created

Information for Stream my_stream created 2024-06-07 12:29:36

              Subjects: foo
              Replicas: 1
               Storage: File

Options:

             Retention: Limits
       Acknowledgments: true
        Discard Policy: Old
      Duplicate Window: 2m0s
            Direct Get: true
     Allows Msg Delete: true
          Allows Purge: true
        Allows Rollups: false

Limits:

      Maximum Messages: unlimited
   Maximum Per Subject: unlimited
         Maximum Bytes: unlimited
           Maximum Age: unlimited
  Maximum Message Size: unlimited
     Maximum Consumers: unlimited

State:

              Messages: 0
                 Bytes: 0 B
        First Sequence: 0
         Last Sequence: 0
      Active Consumers: 0
```

> 🇬🇧 *You can then check the information about the stream you just created:*

Kiểm tra thông tin stream vừa tạo bằng lệnh:

```shell
nats stream info my_stream
```
```text
Information for Stream my_stream created 2024-06-07 12:29:36

              Subjects: foo
              Replicas: 1
               Storage: File

Options:

             Retention: Limits
       Acknowledgments: true
        Discard Policy: Old
      Duplicate Window: 2m0s
            Direct Get: true
     Allows Msg Delete: true
          Allows Purge: true
        Allows Rollups: false

Limits:

      Maximum Messages: unlimited
   Maximum Per Subject: unlimited
         Maximum Bytes: unlimited
           Maximum Age: unlimited
  Maximum Message Size: unlimited
     Maximum Consumers: unlimited

State:

              Messages: 0
                 Bytes: 0 B
        First Sequence: 0
         Last Sequence: 0
      Active Consumers: 0
```

## 2. Publish message vào stream

> 🇬🇧 *Let's now start a publisher*

Khởi động một publisher (bên gửi message):

```shell
nats pub foo --count=1000 --sleep 1s "publication #{{.Count}} @ {{.TimeStamp}}"
```

> 🇬🇧 *As messages are being published on the subject "foo" they are also captured and stored in the stream, you can check that by using `nats stream info my_stream` and even look at the messages themselves using `nats stream view my_stream` or `nats stream get my_stream`*

Khi message được publish lên subject "foo", chúng cũng được ghi lại và lưu vào stream. Có thể kiểm tra bằng `nats stream info my_stream` và xem nội dung từng message bằng `nats stream view my_stream` hoặc `nats stream get my_stream`.

## 3. Tạo một consumer

> 🇬🇧 *Now at this point if you create a 'Core NATS' (i.e. non-streaming) subscriber to listen for messages on the subject 'foo', you will _only_ receive the messages being published after the subscriber was started, this is normal and expected for the basic 'Core NATS' messaging. In order to receive a 'replay' of all the messages contained in the stream (including those that were published in the past) we will now create a 'consumer'*

Lúc này, nếu tạo một subscriber 'Core NATS' (tức là không dùng streaming) để lắng nghe message trên subject 'foo', bạn sẽ _chỉ_ nhận được các message được publish sau khi subscriber đó khởi động — đây là hành vi bình thường của 'Core NATS'. Để nhận lại toàn bộ message đã lưu trong stream (kể cả các message được publish từ trước), ta cần tạo một consumer.

> 🇬🇧 *We can administratively create a consumer using the 'nats consumer add <Consumer name>' command, in this example we will name the consumer "pull_consumer", and we will leave the delivery subject to 'nothing' (i.e. just hit return at the prompt) because we are creating a 'pull consumer' and select `all` for the start policy, you can then just use the defaults and hit return for all the other prompts. The stream the consumer is created on should be the stream 'my_stream' we just created above.*

Có thể tạo consumer bằng lệnh 'nats consumer add \<Consumer name\>'. Trong ví dụ này, consumer được đặt tên là "pull_consumer". Để trống delivery subject (nhấn Enter khi được hỏi) vì đây là pull consumer, chọn `all` cho start policy, rồi nhấn Enter để dùng mặc định cho các tùy chọn còn lại. Stream mà consumer được tạo trên phải là stream 'my_stream' vừa tạo ở trên.

```shell
nats consumer add
```
```text
? Consumer name pull_consumer
? Delivery target (empty for Pull Consumers) 
? Start policy (all, new, last, subject, 1h, msg sequence) all
? Acknowledgment policy explicit
? Replay policy instant
? Filter Stream by subjects (blank for all) 
? Maximum Allowed Deliveries -1
? Maximum Acknowledgments Pending 0
? Deliver headers only without bodies No
? Add a Retry Backoff Policy No
? Select a Stream my_stream
Information for Consumer my_stream > pull_consumer created 2024-06-07T12:32:09-05:00

Configuration:

                    Name: pull_consumer
               Pull Mode: true
          Deliver Policy: All
              Ack Policy: Explicit
                Ack Wait: 30.00s
           Replay Policy: Instant
         Max Ack Pending: 1,000
       Max Waiting Pulls: 512

State:

  Last Delivered Message: Consumer sequence: 0 Stream sequence: 0
    Acknowledgment Floor: Consumer sequence: 0 Stream sequence: 0
        Outstanding Acks: 0 out of maximum 1,000
    Redelivered Messages: 0
    Unprocessed Messages: 74
           Waiting Pulls: 0 of maximum 512
```

> 🇬🇧 *You can check on the status of any consumer at any time using `nats consumer info` or view the messages in the stream using `nats stream view my_stream` or `nats stream get my_stream`, or even remove individual messages from the stream using `nats stream rmm`*

Có thể kiểm tra trạng thái consumer bất kỳ lúc nào bằng `nats consumer info`, xem message trong stream bằng `nats stream view my_stream` hoặc `nats stream get my_stream`, hoặc xóa từng message khỏi stream bằng `nats stream rmm`.

## 3. Subscribe từ consumer

> 🇬🇧 *Now that the consumer has been created and since there are messages in the stream we can now start subscribing to the consumer:*

Sau khi consumer đã được tạo và stream đã có message, ta có thể bắt đầu subscribe từ consumer:

```shell
nats consumer next my_stream pull_consumer --count 1000
```

> 🇬🇧 *This will print out all the messages in the stream starting with the first message (which was published in the past) and continuing with new messages as they are published until the count is reached.*

Lệnh này sẽ in ra toàn bộ message trong stream, bắt đầu từ message đầu tiên (được publish từ trước) rồi tiếp tục với các message mới cho đến khi đạt đủ số lượng chỉ định.

> 🇬🇧 *Note that in this example we are creating a pull consumer with a 'durable' name, this means that the consumer can be shared between as many consuming processes as you want. For example instead of running a single `nats consumer next` with a count of 1000 messages you could have started two instances of `nats consumer` each with a message count of 500 and you would see the consumption of the messages from the consumer distributed between those instances of `nats`*

Lưu ý rằng trong ví dụ này ta đang tạo pull consumer với tên 'durable', nghĩa là consumer có thể được chia sẻ giữa bao nhiêu tiến trình consuming tùy ý. Ví dụ, thay vì chạy một `nats consumer next` duy nhất với 1000 message, bạn có thể chạy hai instance của `nats consumer` mỗi instance với 500 message và sẽ thấy việc tiêu thụ message từ consumer được phân phối giữa các instance của `nats`.

#### Phát lại message

> 🇬🇧 *Once you have iterated over all the messages in the stream with the consumer, you can get them again by simply creating a new consumer or by deleting that consumer (`nats consumer rm`) and re-creating it (`nats consumer add`).*

Sau khi đã duyệt qua tất cả message trong stream bằng consumer, có thể nhận lại chúng bằng cách tạo một consumer mới hoặc xóa consumer đó (`nats consumer rm`) rồi tạo lại (`nats consumer add`).

## 4. Dọn dẹp

> 🇬🇧 *You can clean up a stream (and release the resources associated with it (e.g. the messages stored in the stream)) using `nats stream purge`*

Có thể dọn sạch stream (và giải phóng tài nguyên liên quan, ví dụ các message đã lưu trong stream) bằng `nats stream purge`.

> 🇬🇧 *You can also delete a stream (which will also automatically delete all of the consumers that may be defined on that stream) using `nats stream rm`*

Cũng có thể xóa stream (sẽ tự động xóa toàn bộ consumer được định nghĩa trên stream đó) bằng `nats stream rm`.

## Thuật ngữ trong bài

- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)