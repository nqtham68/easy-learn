---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/core-nats/publish-subscribe/pubsub
title: Publish-Subscribe
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Publish-Subscribe

> 🇬🇧 *NATS implements a publish-subscribe message distribution model for one-to-many communication. A publisher sends a message on a subject and any active subscriber listening on that subject receives the message. Subscribers can also register interest in wildcard subjects that work a bit like a regular expression \(but only a bit\). This one-to-many pattern is sometimes called a fan-out.*

NATS triển khai mô hình phân phối message theo kiểu publish-subscribe cho giao tiếp một-nhiều. Publisher (bên gửi message) gửi message lên một subject (chuỗi định danh message), và mọi subscriber (bên đăng ký nhận message) đang lắng nghe trên subject đó đều nhận được message. Subscriber cũng có thể đăng ký quan tâm đến các wildcard subject, hoạt động tương tự như regular expression (nhưng chỉ ở mức tương đối). Pattern một-nhiều này đôi khi được gọi là fan-out.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/pubsub.svg)

# Messages

> 🇬🇧 *Messages are composed of:*
> *1. A subject.*
> *2. A payload in the form of a byte array.*
> *3. Any number of header fields.*
> *4. An optional 'reply' address field.*

Message được cấu thành từ:
1. Một subject.
2. Một payload (nội dung chính của message) dưới dạng mảng byte.
3. Bất kỳ số lượng header field nào.
4. Một trường địa chỉ 'reply' tùy chọn.

> 🇬🇧 *Messages have a maximum size (which is set in the server configuration with `max_payload`). The size is set to 1 MB by default, but can be increased up to 64 MB if needed (though we recommend keeping the max message size to something more reasonable like 8 MB).*

Message có kích thước tối đa được cấu hình trên server thông qua `max_payload`. Mặc định là 1 MB, nhưng có thể tăng lên tới 64 MB nếu cần (tuy nhiên nên giữ ở mức hợp lý hơn, chẳng hạn 8 MB).

## Thuật ngữ trong bài

- **header**: phần metadata kèm theo
- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **publisher**: bên gửi message
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message