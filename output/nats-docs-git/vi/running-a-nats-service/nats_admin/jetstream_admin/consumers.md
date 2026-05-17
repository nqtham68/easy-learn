---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/jetstream_admin/consumers
title: Consumer
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Consumer

> 🇬🇧 *Messages are read or consumed from the Stream by Consumers. We support pull and push-based Consumers and the example scenario has both, let's walk through that.*

Message được đọc từ stream (luồng message lưu trữ liên tục) thông qua các consumer (bên xử lý dữ liệu từ stream). Hệ thống hỗ trợ cả pull và push consumer — kịch bản ví dụ sau đây bao gồm cả hai loại.

## Tạo Pull Consumer

> 🇬🇧 *The `NEW` and `DISPATCH` Consumers are pull-based, meaning the services consuming data from them have to ask the system for the next available message. This means you can easily scale your services up by adding more workers and the messages will get spread across the workers based on their availability.*

Consumer `NEW` và `DISPATCH` là pull-based, nghĩa là các service muốn nhận dữ liệu phải chủ động yêu cầu hệ thống gửi message tiếp theo. Điều này giúp dễ dàng scale bằng cách thêm worker — message sẽ được phân phối tự động theo độ sẵn sàng của từng worker.

> 🇬🇧 *Pull-based Consumers are created the same as push-based Consumers, you just don't specify a delivery target.*

Pull consumer được tạo giống push consumer, chỉ khác là không chỉ định delivery target.

```shell
nats con ls ORDERS
```
```text
No Consumers defined
```

> 🇬🇧 *We have no Consumers, lets add the `NEW` one:*

Hiện chưa có consumer nào, hãy thêm consumer `NEW`:

> 🇬🇧 *I supply the `--sample` options on the CLI as this is not prompted for at present, everything else is prompted. The help in the CLI explains each:*

Các tùy chọn `--sample` phải truyền trực tiếp qua CLI vì hiện chưa có prompt tương tác cho chúng; các tùy chọn còn lại đều được hỏi. Phần help của CLI giải thích từng tùy chọn:

```shell
nats con add --sample 100
```
```text
? Select a Stream ORDERS
? Consumer name NEW
? Delivery target
? Start policy (all, last, 1h, msg sequence) all
? Filter Stream by subject (blank for all) ORDERS.received
? Maximum Allowed Deliveries 20
Information for Consumer ORDERS > NEW

Configuration:

        Durable Name: NEW
           Pull Mode: true
             Subject: ORDERS.received
         Deliver All: true
        Deliver Last: false
          Ack Policy: explicit
            Ack Wait: 30s
       Replay Policy: instant
  Maximum Deliveries: 20
       Sampling Rate: 100

State:

  Last Delivered Message: Consumer sequence: 1 Stream sequence: 1
    Acknowledgment floor: Consumer sequence: 0 Stream sequence: 0
        Pending Messages: 0
    Redelivered Messages: 0
```

> 🇬🇧 *This is a pull-based Consumer (empty Delivery Target), it gets messages from the first available message and requires specific acknowledgement of each and every message.*

Đây là pull consumer (không có Delivery Target), lấy message từ vị trí đầu tiên có sẵn và yêu cầu xác nhận (ack) riêng cho từng message.

> 🇬🇧 *It only received messages that originally entered the Stream on `ORDERS.received`. Remember the Stream subscribes to `ORDERS.*`, this lets us select a subset of messages from the Stream.*

Consumer này chỉ nhận message có subject (chuỗi định danh message) gốc là `ORDERS.received`. Stream đang subscribe `ORDERS.*`, nên ta có thể lọc một tập con message từ stream.

> 🇬🇧 *A Maximum Delivery limit of 20 is set, this means if the message is not acknowledged it will be retried but only up to this maximum total deliveries.*

Maximum Delivery được đặt là 20 — nếu message chưa được ack, hệ thống sẽ re-delivery nhưng không vượt quá tổng số lần này.

> 🇬🇧 *Again this can all be done in a single CLI call, lets make the `DISPATCH` Consumer:*

Tất cả cũng có thể thực hiện trong một lệnh CLI duy nhất, hãy tạo consumer `DISPATCH`:

```shell
nats con add ORDERS DISPATCH --filter ORDERS.processed --ack explicit --pull --deliver all --sample 100 --max-deliver 20
```

> 🇬🇧 *Additionally, one can store the configuration in a JSON file, the format of this is the same as `$ nats con info ORDERS DISPATCH -j | jq .config`:*

Ngoài ra, có thể lưu config vào file JSON với định dạng giống `$ nats con info ORDERS DISPATCH -j | jq .config`:

```shell
nats con add ORDERS MONITOR --config monitor.json
```

## Tạo Push Consumer

> 🇬🇧 *Our `MONITOR` Consumer is push-based, has no ack and will only get new messages and is not sampled:*

Consumer `MONITOR` là push-based, không cần ack, chỉ nhận message mới và không lấy mẫu:

```shell
nats con add
```
```text
? Select a Stream ORDERS
? Consumer name MONITOR
? Delivery target monitor.ORDERS
? Start policy (all, last, 1h, msg sequence) last
? Acknowledgement policy none
? Replay policy instant
? Filter Stream by subject (blank for all)
? Maximum Allowed Deliveries -1
Information for Consumer ORDERS > MONITOR

Configuration:

      Durable Name: MONITOR
  Delivery Subject: monitor.ORDERS
       Deliver All: false
      Deliver Last: true
        Ack Policy: none
     Replay Policy: instant

State:

  Last Delivered Message: Consumer sequence: 1 Stream sequence: 3
    Acknowledgment floor: Consumer sequence: 0 Stream sequence: 2
        Pending Messages: 0
    Redelivered Messages: 0
```

> 🇬🇧 *Again you can do this with a single non-interactive command:*

Cũng có thể thực hiện với một lệnh không tương tác:

```shell
nats con add ORDERS MONITOR --ack none --target monitor.ORDERS --deliver last --replay instant --filter ''
```

> 🇬🇧 *Additionally one can store the configuration in a JSON file, the format of this is the same as `$ nats con info ORDERS MONITOR -j | jq .config`:*

Tương tự, có thể lưu config vào file JSON với định dạng giống `$ nats con info ORDERS MONITOR -j | jq .config`:

```shell
nats con add ORDERS --config monitor.json
```

## Liệt kê Consumer

> 🇬🇧 *You can get a quick list of all the Consumers for a specific Stream:*

Để xem nhanh danh sách tất cả consumer của một stream cụ thể:

```shell
nats con ls ORDERS
```
```text
Consumers for Stream ORDERS:

        DISPATCH
        MONITOR
        NEW
```

## Truy vấn thông tin Consumer

> 🇬🇧 *All details for a Consumer can be queried, lets first look at a pull-based Consumer:*

Có thể truy vấn toàn bộ thông tin chi tiết của một consumer. Hãy xem trước một pull consumer:

```text
$ nats con info ORDERS DISPATCH
Information for Consumer ORDERS > DISPATCH

Configuration:

      Durable Name: DISPATCH
         Pull Mode: true
           Subject: ORDERS.processed
       Deliver All: true
      Deliver Last: false
        Ack Policy: explicit
          Ack Wait: 30s
     Replay Policy: instant
     Sampling Rate: 100

State:

  Last Delivered Message: Consumer sequence: 1 Stream sequence: 1
    Acknowledgment floor: Consumer sequence: 0 Stream sequence: 0
        Pending Messages: 0
    Redelivered Messages: 0
```

> 🇬🇧 *More details about the `State` section will be shown later when discussing the ack models in depth.*

Thông tin chi tiết hơn về phần `State` sẽ được trình bày khi thảo luận về các ack model.

### Số thứ tự Stream và Consumer

> 🇬🇧 *The two number are not directly related: the Stream sequence number is the pointer to the exact message, while the Consumer sequence number is an ever-increasing counter for consumer actions.*

Hai con số này không liên quan trực tiếp: sequence number của stream trỏ đến message cụ thể, còn sequence number của consumer là bộ đếm tăng dần cho mỗi hành động xử lý.

> 🇬🇧 *So for example a stream with 1 message in it would have stream sequence of 1, but if the consumer attempted 10 deliveries of that message consumer sequence would be 10 or 11.*

Ví dụ: stream có 1 message thì stream sequence là 1, nhưng nếu consumer thực hiện 10 lần re-delivery message đó thì consumer sequence sẽ là 10 hoặc 11.

## Sử dụng Pull Consumer

> 🇬🇧 *Pull-based Consumers require you to specifically ask for messages and ack them, typically you would do this with the client library `Request()` feature, but the `nats` utility has a helper:*

Pull consumer yêu cầu chủ động xin message và ack chúng — thông thường thực hiện qua tính năng `Request()` của client library, nhưng tiện ích `nats` cũng có helper hỗ trợ:

> 🇬🇧 *First, we ensure we have a message:*

Trước tiên, hãy đảm bảo có message:

```shell
nats pub ORDERS.processed "order 1"
nats pub ORDERS.processed "order 2"
nats pub ORDERS.processed "order 3"
```

> 🇬🇧 *We can now read them using `nats`:*

Giờ có thể đọc message bằng `nats`:

```shell
nats con next ORDERS DISPATCH
```
```text
--- received on ORDERS.processed
order 1

Acknowledged message
```

Consumer another one

```shell
nats con next ORDERS DISPATCH
```
```text
--- received on ORDERS.processed
order 2

Acknowledged message
```

> 🇬🇧 *You can prevent ACKs by supplying `--no-ack`.*

Có thể tắt ACK bằng cách truyền `--no-ack`.

> 🇬🇧 *To do this from code you'd send a `Request()` to `$JS.API.CONSUMER.MSG.NEXT.ORDERS.DISPATCH`:*

Để thực hiện từ code, gửi `Request()` đến `$JS.API.CONSUMER.MSG.NEXT.ORDERS.DISPATCH`:

```shell
nats req '$JS.API.CONSUMER.MSG.NEXT.ORDERS.DISPATCH' ''
```
```text
Published [$JS.API.CONSUMER.MSG.NEXT.ORDERS.DISPATCH] : ''
Received [ORDERS.processed] : 'order 3'
```

> 🇬🇧 *Here `nats req` cannot ack, but in your code you'd respond to the received message with a nil payload as an Ack to JetStream.*

Ở đây `nats req` không thể ack, nhưng trong code bạn sẽ phản hồi message nhận được với payload nil để gửi Ack đến JetStream.

## Sử dụng Push Consumer

> 🇬🇧 *Push-based Consumers will publish messages to a subject and anyone who subscribes to the subject will get them, they support different Acknowledgement models covered later, but here on the `MONITOR` Consumer we have no Acknowledgement.*

Push consumer sẽ publish message đến một subject và mọi subscriber (bên đăng ký nhận message) nào subscribe subject đó đều nhận được. Chúng hỗ trợ các ack model khác nhau sẽ đề cập sau — ở consumer `MONITOR` này không có Acknowledgement.

```shell
nats con info ORDERS MONITOR
```

Output extract

```text
...
  Delivery Subject: monitor.ORDERS
...
```

> 🇬🇧 *The Consumer is publishing to that subject, so let's listen there:*

Consumer đang publish lên subject đó, hãy lắng nghe ở đó:

```shell
nats sub monitor.ORDERS
```
```text
Listening on [monitor.ORDERS]
[#3] Received on [ORDERS.processed]: 'order 3'
[#4] Received on [ORDERS.processed]: 'order 4'
```

> 🇬🇧 *Note the subject here of the received message is reported as `ORDERS.processed` this helps you distinguish what you're seeing in a Stream covering a wildcard, or multiple subjects, subject space.*

Lưu ý subject của message nhận được được báo cáo là `ORDERS.processed` — điều này giúp phân biệt nguồn gốc trong stream bao phủ wildcard hoặc nhiều subject.

> 🇬🇧 *This Consumer needs no ack, so any new message into the ORDERS system will show up here in real-time.*

Consumer này không cần ack, nên mọi message mới vào hệ thống ORDERS sẽ xuất hiện ở đây theo thời gian thực.

## Thuật ngữ trong bài

- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message