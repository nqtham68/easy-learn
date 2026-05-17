---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/core-nats/queue-groups/queue
title: Queue Groups
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Queue Groups

> 🇬🇧 *When subscribers register themselves to receive messages from a publisher, the 1:N fan-out pattern of messaging ensures that any message sent by a publisher, reaches all subscribers that have registered. NATS provides an additional feature named "queue", which allows subscribers to register themselves as part of a queue. Subscribers that are part of a queue, form the "queue group".*

Khi subscriber (bên đăng ký nhận message) đăng ký nhận message từ publisher (bên gửi message), mô hình fan-out 1:N đảm bảo mọi message đều được gửi đến tất cả subscriber đã đăng ký. NATS cung cấp thêm tính năng "queue", cho phép subscriber đăng ký tham gia vào một queue. Các subscriber thuộc cùng một queue tạo thành "queue group" (nhóm subscribers chia sẻ tải).

## Cách queue group hoạt động

> 🇬🇧 *As an example, consider message delivery occurring in the 1:N pattern to all subscribers based on the subject name (delivery happens even to subscribers that are not part of a queue group). If a subscriber is registered based on a queue name, it will always receive messages it is subscribed to, based on the subject name. However, if more subscribers are added to the same queue name, they become a queue group, and only one randomly chosen subscriber of the queue group will consume a message each time a message is received by the queue group. Such distributed queues are a built-in load balancing feature that NATS provides.*

Ví dụ: message được giao theo mô hình 1:N đến tất cả subscriber dựa theo tên subject (bao gồm cả subscriber không thuộc queue group nào). Nếu subscriber đăng ký theo tên queue, nó sẽ nhận đúng các message theo subject (bên đăng ký nhận message) tương ứng. Tuy nhiên, khi nhiều subscriber cùng đăng ký vào một queue name, chúng tạo thành queue group — mỗi khi queue group nhận được message, chỉ một subscriber được chọn ngẫu nhiên để xử lý. Đây là tính năng load balancing tích hợp sẵn của NATS.

**Ưu điểm**

* Đảm bảo khả năng chịu lỗi cho ứng dụng
* Có thể scale workload lên hoặc xuống linh hoạt
* Scale số lượng consumer (bên xử lý dữ liệu từ stream) lên/xuống mà không bị duplicate message
* Không cần cấu hình thêm
* Queue group được định nghĩa bởi ứng dụng và các queue subscriber, không phải do cấu hình server

> 🇬🇧 *Queue group names follow the same naming rules as [subjects](../../subjects.md). Foremost, they are case sensitive and cannot contain whitespace. Consider structuring queue groups hierarchically using a period `.`. Some server functionalities like [queue permissions](../../../running-a-nats-service/configuration/securing_nats/authorization.md#queue-permissions) can use [wildcard matching](../../subjects.md#wildcards) on them.*

Tên queue group tuân theo cùng quy tắc đặt tên như [subject](../../subjects.md) (chuỗi định danh message). Quan trọng nhất: tên phân biệt chữ hoa/thường và không được chứa khoảng trắng. Nên cấu trúc tên queue group theo dạng phân cấp bằng dấu chấm `.`. Một số tính năng server như [queue permissions](../../../running-a-nats-service/configuration/securing_nats/authorization.md#queue-permissions) hỗ trợ [wildcard matching](../../subjects.md#wildcards) trên tên queue group.

> 🇬🇧 *Queue subscribers are ideal for scaling services. Scale up is as simple as running another application, scale down is terminating the application with a signal that drains the in flight requests. This flexibility and lack of any configuration changes makes NATS an excellent service communication technology that can work with all platform technologies.*

Queue subscriber rất phù hợp để scale service. Scale up đơn giản chỉ cần chạy thêm một instance ứng dụng; scale down chỉ cần gửi tín hiệu để ứng dụng drain hết các request đang xử lý rồi tắt. Sự linh hoạt này, cùng với việc không cần thay đổi cấu hình, khiến NATS trở thành công nghệ giao tiếp service xuất sắc, tương thích với mọi nền tảng công nghệ.

### No responder

> 🇬🇧 *When a request is made to a service (request/reply) and the NATS Server knows there are no services available (since there are no client applications currently subscribing to the subject in a queue-group) the server will send a "no-responders" protocol message back to the requesting client which will break from blocking API calls. This allows applications to react immediately. This further enables building a highly responsive system at scale, even in the face of application failures and network partitions.*

Khi có request gửi đến một service theo mô hình request/reply mà NATS Server biết không có service nào khả dụng (do không có client nào đang subscribe vào subject trong queue group), server sẽ gửi lại message protocol "no-responders" cho client yêu cầu, giải phóng ngay các blocking API call. Điều này giúp ứng dụng phản ứng tức thì, từ đó xây dựng được hệ thống có độ phản hồi cao ở quy mô lớn, kể cả khi ứng dụng bị lỗi hay xảy ra network partition.

## Stream dùng như queue

> 🇬🇧 *With [JetStream](../../jetstream) a stream can also be used as a queue by setting the retention policy to `WorkQueuePolicy` and leveraging [`pull` consumers](../../jetstream/consumers.md) to get easy horizontal scalability of the processing (or using an explicit ack push consumer with a queue group of subscribers).*

Với [JetStream](../../jetstream), stream (luồng message lưu trữ liên tục) cũng có thể dùng như một queue bằng cách đặt retention policy thành `WorkQueuePolicy` và sử dụng [`pull` consumers](../../jetstream/consumers.md) để dễ dàng scale ngang quá trình xử lý (hoặc dùng push consumer với explicit ack kết hợp queue group subscriber).

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/queue.svg)

### Geo-affinity khi queuing

> 🇬🇧 *When connecting to a globally distributed NATS super-cluster, there is an automatic service geo-affinity due to the fact that a service request message will only be routed to another cluster (i.e. another region) if there are no listeners on the cluster available to handle the request locally.*

Khi kết nối vào một NATS super-cluster phân tán toàn cầu, hệ thống tự động đảm bảo geo-affinity cho service: message request chỉ được route sang cluster khác (tức vùng địa lý khác) khi không có listener nào trên cluster hiện tại có thể xử lý request cục bộ.

### Hướng dẫn thực hành

> 🇬🇧 *Try NATS queue subscriptions on your own, using a live server by walking through the [queueing walkthrough](https://docs.nats.io/nats-concepts/core-nats/queue-groups/queues\_walkthrough).*

Tự thực hành NATS queue subscription với server thực tế qua bài [queueing walkthrough](https://docs.nats.io/nats-concepts/core-nats/queue-groups/queues\_walkthrough).

## Thuật ngữ trong bài

- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **permission**: quyền truy cập
- **publisher**: bên gửi message
- **queue**: hàng đợi message
- **queue group**: nhóm subscribers chia sẻ tải
- **request**: yêu cầu
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message