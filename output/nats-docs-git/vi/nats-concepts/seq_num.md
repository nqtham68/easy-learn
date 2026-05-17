---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/seq_num
title: Số Thứ Tự (Sequence Numbers)
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Số Thứ Tự (Sequence Numbers)

> 🇬🇧 *A common problem for one-to-many messages is that a message can get lost or dropped due to a network failure. A simple pattern for resolving this situation is to include a sequence id with the message. Receivers can check the sequence id to see if they have missed anything. Sequence numbers combined with heartbeats, in the absence of new data, form a powerful and resilient pattern to detect loss. Systems that store and persist messages can also solve this problem, but sometimes are overkill for the problem at hand and usually cause additional management and operational cost.*

Trong các tình huống gửi message (gói dữ liệu được gửi đi) theo mô hình một-nhiều, message có thể bị mất do sự cố mạng. Một cách đơn giản để xử lý là đính kèm sequence id vào mỗi message. Phía nhận có thể kiểm tra sequence id để phát hiện message bị bỏ sót. Kết hợp sequence number với heartbeat — khi không có dữ liệu mới — tạo thành một pattern mạnh mẽ và bền vững để phát hiện mất mát. Các hệ thống lưu trữ message cũng có thể giải quyết vấn đề này, nhưng đôi khi lại quá phức tạp cho nhu cầu thực tế và kéo theo chi phí vận hành cao hơn.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/seqno.svg)

> 🇬🇧 *In order to really leverage sequence ids there are a few things to keep in mind:*

Để tận dụng sequence id hiệu quả, cần lưu ý một số điểm:

* Each sender will have to use their own sequence
* If possible, receivers should be able to ask for missing messages by id

- Mỗi publisher (bên gửi message) phải duy trì sequence riêng của mình.
- Nếu có thể, subscriber (bên đăng ký nhận message) nên có khả năng yêu cầu lại các message bị thiếu theo id.

> 🇬🇧 *With NATS you can embed sequence ids in the message or include them as a token in the subject. For example, a sender can send messages to `updates.1`, `updates.2`, etc... and the subscribers can listen to `updates.*` and parse the subject to determine the sequence id. Placing a sequence token into the subject may be desireable if the payload is unknown or embedding additional data such as a sequence number in the payload is not possible.*

Với NATS, có thể nhúng sequence id trực tiếp vào message hoặc đưa vào dưới dạng token (chuỗi xác thực) trong subject (chuỗi định danh message). Ví dụ, publisher có thể gửi message tới `updates.1`, `updates.2`... và subscriber có thể lắng nghe `updates.*` rồi phân tích subject để xác định sequence id. Cách đặt sequence token vào subject phù hợp khi payload (nội dung chính của message) chưa xác định hoặc không thể nhúng thêm dữ liệu như sequence number vào payload.

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **publisher**: bên gửi message
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **token**: chuỗi xác thực