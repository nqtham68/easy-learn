---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/core-nats/request-reply/reqreply
title: Request-Reply
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Request-Reply

> 🇬🇧 *Request-Reply is a common pattern in modern distributed systems. A request is sent, and the application either waits on the response with a certain timeout, or receives a response asynchronously.*

Request-Reply là một pattern phổ biến trong các hệ thống phân tán hiện đại. Một request (yêu cầu) được gửi đi, và ứng dụng hoặc chờ response với một timeout nhất định, hoặc nhận response theo cơ chế async (bất đồng bộ).

> 🇬🇧 *The increased complexity of modern systems necessitates features like [location transparency](https://en.wikipedia.org/wiki/Location\_transparency), scale-up and scale-down, observability (measuring a system's state based on the data it generates) and more. In order to implement this feature-set, various other technologies needed to incorporate additional components, sidecars (processes or services that support the primary application) and proxies. NATS on the other hand, implemented Request-Reply much more easily.*

Độ phức tạp ngày càng tăng của các hệ thống hiện đại đòi hỏi những tính năng như [location transparency](https://en.wikipedia.org/wiki/Location\_transparency), scale-up/scale-down, observability (đo lường trạng thái hệ thống dựa trên dữ liệu nó tạo ra) và nhiều hơn nữa. Để đáp ứng bộ tính năng này, nhiều công nghệ khác phải tích hợp thêm các thành phần phụ, sidecar (tiến trình hoặc service hỗ trợ ứng dụng chính) và proxy. NATS thì khác — việc triển khai Request-Reply đơn giản hơn nhiều.

### NATS giúp Request-Reply trở nên đơn giản và mạnh mẽ

> 🇬🇧 *NATS supports the Request-Reply pattern using its core communication mechanism — publish and subscribe. A request is published on a given subject using a reply subject. Responders listen on that subject and send responses to the reply subject. Reply subjects are called "**inbox**". These are unique subjects that are dynamically directed back to the requester, regardless of the location of either party.*

NATS hỗ trợ pattern Request-Reply thông qua cơ chế giao tiếp cốt lõi — publish và subscribe. Một request được publish lên một subject (chuỗi định danh message) kèm theo reply subject. Các responder lắng nghe subject đó và gửi response về reply subject. Reply subject được gọi là "**inbox**" — đây là các subject duy nhất được định tuyến động trở lại về phía requester, bất kể vị trí của hai bên.

> 🇬🇧 *Multiple NATS responders can form dynamic queue groups. Therefore, it's not necessary to manually add or remove subscribers from the group for them to start or stop being distributed messages. It's done automatically. This allows responders to scale up or down as per demand.*

Nhiều NATS responder có thể tạo thành queue group (nhóm subscribers chia sẻ tải) động. Vì vậy, không cần thủ công thêm hoặc xóa subscriber khỏi nhóm để bắt đầu hoặc dừng nhận message — tất cả diễn ra tự động. Điều này cho phép các responder scale up hoặc scale down theo nhu cầu.

> 🇬🇧 *NATS applications "drain before exiting" (processing buffered messages before closing the connection). This allows the applications to scale down without dropping requests.*

Các ứng dụng NATS thực hiện "drain before exiting" (xử lý hết message trong buffer trước khi đóng kết nối). Điều này giúp ứng dụng có thể scale down mà không bị mất request nào.

> 🇬🇧 *Since NATS is based on publish-subscribe, observability is as simple as running another application that can view requests and responses to measure latency, watch for anomalies, direct scalability and more.*

Vì NATS dựa trên publish-subscribe, observability trở nên đơn giản — chỉ cần chạy thêm một ứng dụng khác để quan sát request và response, đo latency, phát hiện bất thường, điều phối khả năng mở rộng và nhiều hơn nữa.

> 🇬🇧 *The power of NATS even allows multiple responses, where the first response is utilized and the system efficiently discards the additional ones. This allows for a sophisticated pattern to have multiple responders, reduce response latency and jitter.*

NATS còn cho phép nhận nhiều response cùng lúc, trong đó response đầu tiên được sử dụng còn các response thừa được hệ thống loại bỏ hiệu quả. Cơ chế này cho phép xây dựng pattern phức tạp với nhiều responder nhằm giảm latency và jitter của response.

### Pattern

> 🇬🇧 *![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/reqrepl.svg)*

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/reqrepl.svg)

> 🇬🇧 *Try NATS request-reply on your own, using a live server by walking through the [request-reply walkthrough.](https://docs.nats.io/nats-concepts/core-nats/request-reply/reqreply\_walkthrough)*

Hãy tự thử Request-Reply của NATS trên server thực tế bằng cách làm theo [request-reply walkthrough.](https://docs.nats.io/nats-concepts/core-nats/request-reply/reqreply\_walkthrough)

### Không có responder

> 🇬🇧 *When a request is sent to a subject that has no subscribers, it can be convenient to know about it right away. For this use-case, a NATS client can [opt-into no\_responder messages](../../../reference/nats-protocol/nats-protocol#syntax-1). This requires a server and client that support headers. When enabled, a request sent to a subject with no subscribers will immediately receive a reply that has no body, and a `503` status.*

Khi một request được gửi đến subject không có subscriber nào, sẽ rất hữu ích nếu biết ngay điều đó. Với use-case này, NATS client có thể [bật tính năng no\_responder messages](../../../reference/nats-protocol/nats-protocol#syntax-1). Tính năng này yêu cầu server và client hỗ trợ header. Khi được bật, một request gửi đến subject không có subscriber sẽ ngay lập tức nhận được reply rỗng kèm status `503`.

> 🇬🇧 *Most clients will represent this case by raising or returning an error. For example:*

Hầu hết các client sẽ biểu thị trường hợp này bằng cách ném ra hoặc trả về một error. Ví dụ:

```go
m, err := nc.Request("foo", nil, time.Second);
# err == nats.ErrNoResponders
```

## Thuật ngữ trong bài

- **async**: bất đồng bộ
- **buffer**: vùng đệm tạm
- **client**: bên gọi (phía người dùng)
- **header**: phần metadata kèm theo
- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **queue group**: nhóm subscribers chia sẻ tải
- **request**: yêu cầu
- **response**: phản hồi
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **timeout**: thời gian chờ tối đa