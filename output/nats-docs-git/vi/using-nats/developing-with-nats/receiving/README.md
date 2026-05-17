---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/receiving
title: Nhận Messages
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Nhận Messages

> 🇬🇧 *In general, applications can receive messages asynchronously or synchronously. Receiving messages with NATS can be library dependent.*

Về cơ bản, ứng dụng có thể nhận message (gói dữ liệu được gửi đi) theo kiểu async (bất đồng bộ) hoặc sync (đồng bộ). Cách nhận message với NATS có thể phụ thuộc vào library đang dùng.

> 🇬🇧 *Some languages, like Go or Java, provide synchronous and asynchronous APIs, while others may only support one type of subscription.*

Một số ngôn ngữ như Go hay Java cung cấp cả hai loại API — sync và async — trong khi các ngôn ngữ khác có thể chỉ hỗ trợ một kiểu subscription.

> 🇬🇧 *In all cases, the process of subscribing involves having the client library tell the NATS system that an application is interested in a particular subject. When an application is done with a subscription it unsubscribes telling the server to stop sending messages.*

Trong mọi trường hợp, quá trình đăng ký subscription đều yêu cầu client library thông báo với hệ thống NATS rằng ứng dụng quan tâm đến một subject (chuỗi định danh message) cụ thể. Khi ứng dụng không còn cần subscription nữa, nó sẽ hủy đăng ký để báo cho server dừng gửi message.

> 🇬🇧 *A client will receive a message for each matching subscription, so if a connection has multiple subscriptions using identical or overlapping subjects \(say `foo` and `>`\) the same message will be sent to the client multiple times.*

Một client sẽ nhận message cho mỗi subscription khớp với subject. Vì vậy, nếu một connection có nhiều subscription dùng subject trùng nhau hoặc chồng lấp nhau (ví dụ `foo` và `>`) thì cùng một message sẽ được gửi đến client nhiều lần.

> 🇬🇧 *Note: The client API (asynchronous) subscribe call can return before the subscription is actually fully established at the nats-server. Call `Flush()` on the connection right after you call subscribe if you need to synchronize with the subscription being ready at the server level.*

Lưu ý: Lời gọi subscribe qua API bất đồng bộ của client có thể trả về trước khi subscription thực sự được thiết lập hoàn toàn ở phía nats-server. Gọi `Flush()` trên connection ngay sau khi subscribe nếu bạn cần đồng bộ hóa với thời điểm subscription sẵn sàng ở cấp server.

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **async**: bất đồng bộ
- **client**: bên gọi (phía người dùng)
- **library**: thư viện
- **message**: gói dữ liệu được gửi đi
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)
- **sync**: đồng bộ