---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/core-nats/publish-subscribe/pubsub_walkthrough
title: Hướng dẫn thực hành NATS Pub/Sub
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

> 🇬🇧 *NATS is a [publish subscribe](./pubsub.md) messaging system [based on subjects](../../subjects.md). Subscribers listening on a subject receive messages published on that subject. If the subscriber is not actively listening on the subject, the message is not received. Subscribers can use the wildcard tokens such as `*` and `>` to match a single token or to match the tail of a subject.*

NATS là hệ thống messaging theo mô hình publish-subscribe, hoạt động dựa trên subject (chuỗi định danh message). Subscriber (bên đăng ký nhận message) lắng nghe trên một subject sẽ nhận được tất cả message mà publisher (bên gửi message) gửi lên subject đó. Nếu subscriber không lắng nghe tại thời điểm message được gửi, message đó sẽ bị bỏ qua. Subscriber có thể dùng wildcard token như `*` và `>` để khớp một token đơn hoặc phần đuôi của subject.

# Hướng dẫn thực hành NATS Pub/Sub

> 🇬🇧 *This simple walkthrough demonstrates some ways in which subscribers listen on subjects, and publishers send messages on specific subjects.*

Hướng dẫn này minh họa cách subscriber lắng nghe trên các subject và publisher gửi message đến các subject cụ thể.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/pubsubtut.svg)

## Yêu cầu trước khi bắt đầu

> 🇬🇧 *If you have not already done so, you need to [install](../../what-is-nats/walkthrough_setup.md) the `nats` CLI Tool and optionally the nats-server on your machine.*

Nếu chưa cài đặt, bạn cần [cài](../../what-is-nats/walkthrough_setup.md) CLI Tool `nats` và tùy chọn cả nats-server trên máy.

### 1. Tạo Subscriber 1

> 🇬🇧 *In a shell or command prompt session, start a client subscriber program.*

Mở một shell hoặc command prompt, khởi chạy chương trình subscriber.

```bash
nats sub <subject>
```

> 🇬🇧 *Here, `<subject>` is a subject to listen on. It helps to use unique and well thought-through subject strings because you need to ensure that messages reach the correct subscribers even when wildcards are used.*

Trong đó, `<subject>` là subject cần lắng nghe. Nên đặt chuỗi subject rõ ràng và có tính duy nhất để đảm bảo message luôn đến đúng subscriber, kể cả khi dùng wildcard.

> 🇬🇧 *For example:*

Ví dụ:

```bash
nats sub msg.test
```

Bạn sẽ thấy thông báo: _Listening on \[msg.test\]_

### 2. Tạo Publisher và gửi message

> 🇬🇧 *In another shell or command prompt, create a NATS publisher and send a message.*

Mở một shell khác, tạo NATS publisher và gửi message.

```bash
nats pub <subject> <message>
```

> 🇬🇧 *Where `<subject>` is the subject name and `<message>` is the text to publish.*

Trong đó `<subject>` là tên subject và `<message>` là nội dung cần gửi.

> 🇬🇧 *For example:*

Ví dụ:

```bash
nats pub msg.test "NATS MESSAGE"
```

### 3. Xác nhận việc gửi và nhận message

> 🇬🇧 *You'll notice that the publisher sends the message and prints: _Published \[msg.test\] : 'NATS MESSAGE'_.*

Publisher gửi message và in ra: _Published \[msg.test\] : 'NATS MESSAGE'_.

> 🇬🇧 *The subscriber receives the message and prints: _\[\#1\] Received on \[msg.test\]: 'NATS MESSAGE'_.*

Subscriber nhận được message và in ra: _\[\#1\] Received on \[msg.test\]: 'NATS MESSAGE'_.

> 🇬🇧 *If the receiver does not get the message, you'll need to check if you are using the same subject name for the publisher and the subscriber.*

Nếu subscriber không nhận được message, hãy kiểm tra xem publisher và subscriber có đang dùng cùng tên subject hay không.

### 4. Thử gửi thêm message

```bash
nats pub msg.test "NATS MESSAGE 2"
```

> 🇬🇧 *You'll notice that the subscriber receives the message. Note that a message count is incremented each time your subscribing client receives a message on that subject.*

Subscriber sẽ nhận được message. Lưu ý rằng bộ đếm message tăng lên mỗi khi subscriber nhận được message trên subject đó.

### 5. Tạo Subscriber 2

> 🇬🇧 *In a new shell or command prompt, start a new NATS subscriber.*

Mở một shell mới, khởi chạy thêm một NATS subscriber.

```bash
nats sub msg.test
```

### 6. Gửi thêm message từ publisher

```bash
nats pub msg.test "NATS MESSAGE 3"
```

> 🇬🇧 *Verify that both subscribing clients receive the message.*

Xác nhận rằng cả hai subscriber đều nhận được message.

### 7. Tạo Subscriber 3

> 🇬🇧 *In a new shell or command prompt session, create a new subscriber that listens on a different subject.*

Mở một shell mới, tạo subscriber lắng nghe trên một subject khác.

```bash
nats sub msg.test.new
```

### 8. Gửi thêm message

```bash
nats pub msg.test "NATS MESSAGE 4"
```

> 🇬🇧 *Subscriber 1 and Subscriber 2 receive the message, but Subscriber 3 does not. Why? Because Subscriber 3 is not listening on the message subject used by the publisher.*

Subscriber 1 và Subscriber 2 nhận được message, nhưng Subscriber 3 thì không — vì Subscriber 3 không lắng nghe trên subject mà publisher đang dùng.

### 9. Cập nhật Subscriber 3 để dùng wildcard

> 🇬🇧 *Change the last subscriber to listen on msg.\* and run it:*

Thay đổi subscriber cuối để lắng nghe trên `msg.*` rồi chạy lại:

```bash
nats sub msg.*
```

> 🇬🇧 *Note: NATS supports the use of wildcard characters for message subscribers only. You cannot publish a message using a wildcard subject.*

Lưu ý: NATS chỉ hỗ trợ wildcard cho subscriber. Không thể publish message lên subject dạng wildcard.

### 10. Gửi thêm message

```bash
nats pub msg.test "NATS MESSAGE 5"
```

> 🇬🇧 *This time, all three subscribing clients should receive the message.*

Lần này, cả ba subscriber đều sẽ nhận được message.

> 🇬🇧 *Do try out a few more variations of substrings and wildcards to test your understanding.*

Hãy thử thêm các biến thể khác nhau của subject và wildcard để kiểm tra lại hiểu biết của bạn.

# Xem thêm

Publish-subscribe pattern with the NATS CLI&#x20;

[Publish-subscribe pattern - NATS CLI](https://www.youtube.com/watch?v=jLTVhP08Tq0)

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message