---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/acks
title: Xác nhận nhận tin (Acknowledgements)
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Xác nhận nhận tin (Acknowledgements)

> 🇬🇧 *In a system with at-most-once semantics, there are times when messages can be lost. If your application is doing request-reply it should use timeouts to handle any network or application failures. It is always a good idea to place a timeout on a request and have code that deals with timeouts. When you are publishing an event or data stream, one way to ensure message delivery is to turn it into a request-reply with the concept of an acknowledgement message, or ACKs. In NATS, an ACK can simply be an empty message, a message with no payload.*

Trong hệ thống với ngữ nghĩa at-most-once, message (gói dữ liệu được gửi đi) đôi khi có thể bị mất. Nếu ứng dụng thực hiện request-reply, cần dùng timeout (thời gian chờ tối đa) để xử lý các lỗi mạng hoặc lỗi ứng dụng — luôn nên đặt timeout cho mỗi request và viết code để xử lý trường hợp hết thời gian chờ. Khi publish một event hoặc data stream, một cách đảm bảo message được giao là chuyển nó thành mô hình request-reply kèm khái niệm acknowledgement message, hay ACK. Trong NATS, ACK có thể chỉ là một message rỗng — message không có payload.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/acks.svg)

> 🇬🇧 *Because the ACK can be empty it can take up very little network bandwidth, but the idea of the ACK turns a simple fire-and-forget into a fire-and-know world where the sender can be sure that the message was received by the other side, or with a [scatter-gather pattern](./core-nats/request-reply/reqreply.md), several other sides.*

Vì ACK có thể rỗng nên chiếm rất ít băng thông mạng. Nhưng ý tưởng đằng sau ACK biến mô hình gửi-và-quên đơn giản thành gửi-và-biết — nơi bên gửi có thể chắc chắn rằng message đã được phía bên kia nhận, hoặc với [scatter-gather pattern](./core-nats/request-reply/reqreply.md), là nhiều phía cùng lúc.

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **request**: yêu cầu
- **stream**: luồng message lưu trữ liên tục
- **timeout**: thời gian chờ tối đa