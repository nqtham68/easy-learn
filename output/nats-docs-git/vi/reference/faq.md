---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/reference/faq
title: Câu hỏi thường gặp (FAQ)
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Câu hỏi thường gặp (FAQ)

### Tổng quan

* [NATS là gì?](./faq.md#what-is-nats)
* [NATS được viết bằng ngôn ngữ gì?](./faq.md#what-language-is-nats-written-in)
* [Ai duy trì NATS?](./faq.md#who-maintains-nats)
* [NATS hỗ trợ những client nào?](./faq.md#what-client-support-exists-for-nats)
* [Chữ viết tắt NATS có nghĩa là gì?](./faq.md#what-does-the-nats-acronym-stand-for)
* [JetStream và NATS Streaming?](./faq.md#jetstream-and-nats-streaming)

### Câu hỏi kỹ thuật

* [Sự khác nhau giữa Request() và Publish() là gì?](./faq.md#what-is-the-difference-between-request-and-publish)
* [Nhiều subscriber có thể nhận một Request không?](./faq.md#can-multiple-subscribers-receive-a-request)
* [Làm thế nào để giám sát NATS cluster?](./faq.md#how-can-i-monitor-my-nats-cluster)
* [NATS có hỗ trợ queuing không? NATS có hỗ trợ load balancing không?](./faq.md#does-nats-do-queuing-does-nats-do-load-balancing)
* [Có thể liệt kê các subject tồn tại trong NATS cluster không?](./faq.md#can-i-list-the-subjects-that-exist-in-my-nats-cluster)
* [NATS có hỗ trợ wildcard cho subject không?](./faq.md#does-nats-support-subject-wildcards)
* [Nên dùng loại Stream consumer nào?](./faq.md)
* ['verbose' và 'pedantic' có nghĩa gì khi dùng CONNECT?](./faq.md#what-do-verbose-and-pedantic-mean-when-using-connect)
* [NATS có đảm bảo thứ tự message không?](./faq.md#does-nats-offer-any-guarantee-of-message-ordering)
* [NATS có giới hạn kích thước message không?](./faq.md#is-there-a-message-size-limitation-in-nats)
* [NATS có giới hạn số lượng subject không?](./faq.md#does-nats-impose-any-limits-on-the-of-subjects)
* [NATS có đảm bảo giao nhận message không?](./faq.md#does-nats-guarantee-message-delivery)
* [NATS có hỗ trợ replay/redelivery dữ liệu lịch sử không?](./faq.md#does-nats-support-replay-redelivery-of-historical-data)
* [Làm thế nào để tắt gracefully một asynchronous subscriber?](./faq.md#how-do-i-gracefully-shut-down-an-asynchronous-subscriber)
* [Làm thế nào để tạo subject?](./faq.md#how-do-i-create-subjects)
* [Có bao nhiêu client có thể kết nối đồng thời?](./faq.md#how-many-clients-can-connect-simultaneously)

## Tổng quan

### NATS là gì?

> 🇬🇧 *NATS is an open source, lightweight, high-performance cloud native infrastructure messaging system. It implements a highly scalable and elegant publish-subscribe (pub/sub) distribution model. The performant nature of NATS make it an ideal base for building modern, reliable, scalable cloud native distributed systems.*

NATS là một hệ thống messaging hạ tầng cloud native mã nguồn mở, nhẹ và hiệu năng cao. NATS triển khai mô hình phân phối publish-subscribe (pub/sub) vừa linh hoạt vừa thanh lịch. Với đặc tính hiệu năng cao, NATS là nền tảng lý tưởng để xây dựng các hệ thống phân tán cloud native hiện đại, đáng tin cậy và có khả năng mở rộng.

> 🇬🇧 *NATS is offered in two interoperable modules in a single "NATS Server" binary (often referred to as `nats-server` throughout this site):*

NATS cung cấp hai module tương thích nhau trong cùng một file binary "NATS Server" (thường được gọi là `nats-server` trên trang này):

* 'Core NATS' là tập hợp các chức năng cốt lõi và chất lượng dịch vụ của NATS.
* ['JetStream'](../using-nats/jetstream/develop_jetstream.md) là lớp persistence tích hợp (có thể bật tuỳ chọn), bổ sung cho Core NATS khả năng streaming (luồng message lưu trữ liên tục), đảm bảo at-least-once và exactly-once, replay dữ liệu lịch sử, flow-control tách rời, cùng chức năng key/value store.

> 🇬🇧 *NATS was created by Derek Collison, who has over 25 years of experience designing, building, and using publish-subscribe messaging systems. NATS is maintained by an amazing Open Source Ecosystem, find more at [GitHub](https://www.github.com/nats-io).*

NATS được tạo ra bởi Derek Collison — người có hơn 25 năm kinh nghiệm thiết kế, xây dựng và sử dụng các hệ thống messaging publish-subscribe. NATS hiện được duy trì bởi một hệ sinh thái Open Source sôi động. Xem thêm tại [GitHub](https://www.github.com/nats-io).

### Chữ viết tắt NATS có nghĩa là gì?

> 🇬🇧 *NATS stands for Neural Autonomic Transport System. Derek Collison conceived NATS as a messaging platform that functions like a central nervous system.*

NATS là viết tắt của Neural Autonomic Transport System. Derek Collison hình dung NATS như một nền tảng messaging hoạt động tương tự hệ thần kinh trung ương.

### JetStream và NATS Streaming?

> 🇬🇧 *As of NATS Server 2.2, NATS [JetStream](../using-nats/jetstream/develop_jetstream.md) is the recommended option for persistence, streaming and higher message guarantees. [NATS Streaming](https://github.com/nats-io/nats-streaming-server) a.k.a. 'STAN' is now deprecated.*

Kể từ NATS Server 2.2, [JetStream](../using-nats/jetstream/develop_jetstream.md) là lựa chọn được khuyến nghị cho persistence, streaming và đảm bảo giao nhận message nâng cao. [NATS Streaming](https://github.com/nats-io/nats-streaming-server) (hay còn gọi là 'STAN') đã bị deprecated.

### NATS được viết bằng ngôn ngữ gì?

> 🇬🇧 *The NATS server (`nats-server`) is written in Go. There is client support for a wide variety of languages. Please see the [Developing with NATS](../using-nats/developing-with-nats/developer.md) page for more info.*

NATS server (`nats-server`) được viết bằng Go. NATS cũng cung cấp client hỗ trợ nhiều ngôn ngữ lập trình khác nhau. Xem thêm tại trang [Developing with NATS](../using-nats/developing-with-nats/developer.md).

### Ai duy trì NATS?

> 🇬🇧 *NATS is maintained by a select group of Maintainers following a Governance process as part of the [Cloud Native Computing Foundation (CNCF)](http://cncf.io). The team of engineers at [Synadia](https://www.synadia.com?utm_source=nats_docs&utm_medium=nats) in conjunction with Community Maintainers, maintain the NATS server, NATS Streaming Server, as well as the official Go, Ruby, Node.js, C, C#, Java and several other client libraries. Our very active user community also contributes client libraries and connectors for several other implementation languages. Please see the [download](https://nats.io/download) page for the complete list, and links to the relevant source repositories and documentation.*

NATS được duy trì bởi một nhóm Maintainer được chọn lọc theo quy trình Governance trong khuôn khổ [Cloud Native Computing Foundation (CNCF)](http://cncf.io). Đội ngũ kỹ sư tại [Synadia](https://www.synadia.com?utm_source=nats_docs&utm_medium=nats) cùng với Community Maintainers chịu trách nhiệm duy trì NATS server, NATS Streaming Server, cùng các thư viện client chính thức cho Go, Ruby, Node.js, C, C#, Java và nhiều ngôn ngữ khác. Cộng đồng người dùng rất tích cực cũng đóng góp thêm các client library và connector cho nhiều ngôn ngữ. Xem danh sách đầy đủ và link đến các repository tại trang [download](https://nats.io/download).

### NATS hỗ trợ những client nào?

> 🇬🇧 *Please see the [Developing with NATS](../using-nats/developing-with-nats/developer.md) page for the latest list of Synadia and Community maintained NATS clients.*

Xem trang [Developing with NATS](../using-nats/developing-with-nats/developer.md) để biết danh sách mới nhất các NATS client do Synadia và Community duy trì.

## Câu hỏi kỹ thuật

### Sự khác nhau giữa Request() và Publish() là gì?

> 🇬🇧 *Publish() sends a message to `nats-server` with a subject as its address, and `nats-server` delivers the message to any interested/eligible subscriber of that subject. Optionally, you may also send along a reply subject with your message, which provides a way for subscribers who have received your message(s) to send messages back to you.*

`Publish()` gửi một message đến `nats-server` với subject (chuỗi định danh message) là địa chỉ, và `nats-server` sẽ chuyển message đến bất kỳ subscriber (bên đăng ký nhận message) nào đang quan tâm đến subject đó. Tuỳ chọn, bạn có thể đính kèm một reply subject cùng message để subscriber có thể gửi message ngược lại cho bạn.

> 🇬🇧 *Request() is simply a convenience API that does this for you in a pseudo-synchronous fashion, using a timeout supplied by you. It creates an INBOX (a type of subject that is unique to the requestor), subscribes to it, then publishes your request message with the reply address set to the inbox subject. It will then wait for a response, or the timeout period to elapse, whichever comes first.*

`Request()` là một API tiện lợi thực hiện điều trên theo kiểu giả đồng bộ, với timeout do bạn cung cấp. Nó tạo một INBOX (một loại subject duy nhất cho requestor), đăng ký nhận từ INBOX đó, rồi publish message yêu cầu với reply address trỏ về INBOX subject. Sau đó nó chờ response, hoặc cho đến khi hết timeout — tuỳ điều kiện nào xảy ra trước.

### Nhiều subscriber có thể nhận một Request không?

> 🇬🇧 *Yes. NATS is a publish and subscribe system that also has distributed queueing functionality on a per subscriber basis. When you publish a message, for instance at the beginning of a request, every subscriber will receive the message. If subscribers form a queue group, only one subscriber will be picked at random to receive the message. However, note that the requestor does not know or control this information. What the requestor does control is that it only wants one answer to the request, and NATS handles this very well by actively pruning the interest graph.*

Có. NATS là hệ thống publish-subscribe cũng hỗ trợ distributed queueing theo từng subscriber. Khi bạn publish một message — ví dụ ở đầu một request — mọi subscriber đều nhận được message đó. Nếu các subscriber thuộc cùng một queue group (nhóm subscribers chia sẻ tải), thì chỉ một subscriber được chọn ngẫu nhiên để nhận message. Tuy nhiên, requestor không biết và cũng không điều khiển thông tin này. Điều requestor kiểm soát là nó chỉ muốn nhận một câu trả lời cho request, và NATS xử lý rất tốt điều này bằng cách chủ động loại bỏ các nhánh thừa trong interest graph.

### Làm thế nào để giám sát NATS cluster?

> 🇬🇧 *NATS can be deployed to have an HTTP(s) monitoring port - see the demo server here: [https://demo.nats.io:8222/](https://demo.nats.io:8222/). Alternately, there are several options available, including some from the active NATS community:*

NATS có thể được triển khai với một monitoring port HTTP(s) — xem demo server tại: [https://demo.nats.io:8222/](https://demo.nats.io:8222/). Ngoài ra, còn có nhiều lựa chọn khác, bao gồm một số công cụ từ cộng đồng NATS:

* [Prometheus NATS Exporter](https://github.com/nats-io/prometheus-nats-exporter) — Dùng Prometheus để thu thập metric và Grafana để hiển thị trực quan.
* [nats-top](https://github.com/nats-io/nats-top) — Công cụ giám sát tương tự `top`, phát triển bởi Wally Quevedo của Synadia.
* [natsboard](https://github.com/cmfatih/natsboard) — Công cụ giám sát phát triển bởi Fatih Cetinkaya.
* [nats-mon](https://github.com/repejota/nats-mon) — Công cụ giám sát phát triển bởi Raül Pérez và Adrià Cidre.

> 🇬🇧 *A more detailed overview of monitoring is available under [NATS Server Monitoring](../running-a-nats-service/configuration/monitoring.md).*

Tổng quan chi tiết hơn về monitoring có tại [NATS Server Monitoring](../running-a-nats-service/configuration/monitoring.md).

### NATS có hỗ trợ queuing không? NATS có hỗ trợ load balancing không?

> 🇬🇧 *The term 'queueing' implies different things in different contexts, so we must be careful with its use. NATS implements non-persistent distributed queuing via subscriber queue groups. Subscriber queue groups offer a form of message-distribution load balancing. Subject subscriptions in NATS may be either 'individual' subscriptions or queue group subscriptions. The choice to join a queue group is made when the subscription is created, by supplying an optional queue group name. For individual subject subscribers, `nats-server` will attempt to deliver a copy of _every_ message published to that subject to _every_ eligible subscriber of that subject. For subscribers in a queue group, `nats-server` will attempt to deliver each successive message to exactly _one_ subscriber in the group, chosen at random.*

Thuật ngữ 'queueing' có thể mang nhiều nghĩa khác nhau tuỳ ngữ cảnh, vì vậy cần cẩn thận khi dùng từ này. NATS triển khai distributed queueing không persistent thông qua queue group của subscriber. Queue group cung cấp một dạng load balancing phân phối message. Subscription trong NATS có thể là 'individual' (đăng ký riêng lẻ) hoặc queue group subscription. Quyết định tham gia queue group được thực hiện khi tạo subscription, bằng cách cung cấp tên queue group tuỳ chọn. Với subscriber riêng lẻ theo subject, `nats-server` sẽ cố gắng giao một bản sao của _mọi_ message được publish đến subject đó tới _mỗi_ subscriber hợp lệ. Với các subscriber trong queue group, `nats-server` sẽ cố gắng giao mỗi message tiếp theo đến đúng _một_ subscriber trong nhóm, được chọn ngẫu nhiên.

> 🇬🇧 *This form of distributed queueing is done in real time, and messages are not persisted to secondary storage. Further, the distribution is based on interest graphs (subscriptions), so it is not a publisher operation, but instead is controlled entirely by `nats-server`.*

Hình thức distributed queueing này diễn ra theo thời gian thực, message không được lưu vào bộ nhớ thứ cấp. Hơn nữa, việc phân phối dựa trên interest graph (subscription), nên đây không phải là thao tác của publisher (bên gửi message) mà được điều khiển hoàn toàn bởi `nats-server`.

### Có thể liệt kê các subject tồn tại trong NATS cluster không?

> 🇬🇧 *NATS maintains and constantly updates the interest graph (subjects and their subscribers) in real time. Do not think of it as a "directory" that is aggregated over time. The interest graph is dynamic, and will change constantly as publishers and subscribers come and go.*

NATS duy trì và liên tục cập nhật interest graph (các subject và subscriber của chúng) theo thời gian thực. Đừng coi đây như một "thư mục" được tổng hợp theo thời gian — interest graph hoàn toàn động và sẽ thay đổi liên tục khi publisher và subscriber kết nối hoặc ngắt kết nối.

> 🇬🇧 *If you are determined to gather this information, it can be indirectly derived at any instant in time by polling the monitoring endpoint for /connz and /routez. See [Server Monitoring](../running-a-nats-service/configuration/monitoring.md) for more information.*

Nếu cần thu thập thông tin này, bạn có thể gián tiếp lấy nó tại bất kỳ thời điểm nào bằng cách poll monitoring endpoint `/connz` và `/routez`. Xem [Server Monitoring](../running-a-nats-service/configuration/monitoring.md) để biết thêm chi tiết.

### NATS có hỗ trợ wildcard cho subject không?

> 🇬🇧 *Yes. The valid wildcards are as follows:*

Có. Các wildcard hợp lệ như sau:

> 🇬🇧 *The dot character `'.'` is the token separator.*

Ký tự dấu chấm `'.'` là dấu phân tách token.

> 🇬🇧 *The asterisk character `'*'` is a token wildcard match.*

Ký tự dấu hoa thị `'*'` là wildcard khớp theo token.

```
 e.g foo.* matches foo.bar, foo.baz, but not foo.bar.baz.
```

> 🇬🇧 *The greater-than symbol `'>'` is a full wildcard match.*

Ký hiệu lớn hơn `'>'` là wildcard khớp toàn bộ.

```
e.g. foo.> matches foo.bar, foo.baz, foo.bar.baz, foo.bar.1, etc.
```

### Nên dùng loại Stream consumer nào?

> 🇬🇧 *It depends on the access pattern of the application using the stream: if you want to horizontally scale the processing of all the messages stored in a stream and/or process a high-throughput stream of messages in real-time using batching, then use a shared pull consumer (as they scale well horizontally and batching is in practice key to achieving high throughput). But if the access pattern is more like individual application instances needing their own individual replay of the messages in a stream on demand: then an 'ordered push consumer' is best. Consider the use of a durable push consumer with a queue-group for the clients if you want a scalable low latency real time processing of the messages inserted into a stream.*

Tuỳ thuộc vào access pattern của ứng dụng sử dụng stream: nếu muốn scale ngang việc xử lý toàn bộ message trong stream và/hoặc xử lý stream thông lượng cao theo thời gian thực với batching, hãy dùng shared pull consumer (chúng scale ngang tốt và batching là yếu tố then chốt để đạt throughput cao). Nhưng nếu access pattern thiên về từng instance ứng dụng cần replay riêng lẻ theo yêu cầu, thì 'ordered push consumer' là lựa chọn tốt nhất. Cân nhắc dùng durable push consumer kết hợp queue group nếu muốn xử lý thời gian thực có độ trễ thấp và có khả năng mở rộng cho các message được đưa vào stream.

### 'verbose' và 'pedantic' có nghĩa gì khi dùng CONNECT?

> 🇬🇧 *'Verbose' means all protocol commands will be acked with a +OK or -ERR. If verbose is off, you don't get the +OK for each command. Pedantic means the server does lots of extra checking, mostly around properly formed subjects, etc. Verbose mode is ON by default for new connections; most client implementations disable verbose mode by default in their INFO handshake during connection.*

'Verbose' nghĩa là mọi lệnh protocol sẽ được ack bằng `+OK` hoặc `-ERR`. Nếu tắt verbose, bạn sẽ không nhận được `+OK` cho mỗi lệnh. 'Pedantic' nghĩa là server thực hiện nhiều kiểm tra bổ sung, chủ yếu về định dạng subject, v.v. Verbose mode mặc định là BẬT cho các kết nối mới; hầu hết các client implementation đều tắt verbose trong quá trình INFO handshake khi kết nối.

### NATS có đảm bảo thứ tự message không?

> 🇬🇧 *NATS implements source ordered delivery per publisher. That is to say, messages from a given single publisher will be delivered to all eligible subscribers in the order in which they were originally published. There are no guarantees of message delivery order amongst multiple publishers.*

NATS triển khai giao nhận theo thứ tự nguồn trên từng publisher. Nghĩa là các message từ một publisher cụ thể sẽ được giao đến tất cả subscriber hợp lệ theo đúng thứ tự chúng được publish ban đầu. Không có bảo đảm về thứ tự giao nhận message giữa nhiều publisher khác nhau.

### NATS có giới hạn kích thước message không?

> 🇬🇧 *Messages have a maximum size (which is set in the server configuration with `max_payload`) that is enforced by the server and communicated to the client during connection setup. The size is set to 1 MB by default, but can be increased up to 64 MB if needed (though we recommend keeping the max message size to something more reasonable like 8 MB).*

Message có kích thước tối đa (được đặt trong server config bằng `max_payload`) do server áp đặt và thông báo cho client trong quá trình thiết lập kết nối. Mặc định là 1 MB, nhưng có thể tăng lên đến 64 MB nếu cần (tuy nhiên nên giữ ở mức hợp lý hơn, chẳng hạn 8 MB).

### NATS có giới hạn số lượng subject không?

> 🇬🇧 *No. As of `nats-server` v0.8.0, there is no hard limit on the maximum number of subjects.*

Không. Kể từ `nats-server` v0.8.0, không có giới hạn cứng về số lượng subject tối đa.

### NATS có đảm bảo giao nhận message không?

> 🇬🇧 *Core NATS, offers "at-most-once" delivery. This means messages are guaranteed to arrive intact, in order from a given publisher, but not across different publishers. NATS does everything required to remain available and provide a dial-tone. However, if a subscriber is problematic or goes offline it will not receive messages, as the basic NATS platform is a simple pub-sub transport system that offers only TCP reliability.*

Core NATS cung cấp đảm bảo giao nhận "at-most-once". Nghĩa là message được đảm bảo đến nguyên vẹn và đúng thứ tự từ một publisher nhất định, nhưng không đảm bảo thứ tự giữa các publisher khác nhau. NATS làm mọi thứ cần thiết để duy trì sẵn sàng hoạt động. Tuy nhiên, nếu subscriber gặp sự cố hoặc offline, nó sẽ không nhận được message, vì nền tảng NATS cơ bản chỉ là hệ thống pub-sub transport đơn giản với đảm bảo ở mức TCP.

> 🇬🇧 *As of NATS Server 2.2, NATS JetStream offers persistence with "at-least-once" and "exactly-once" (within a time window) delivery. See the [JetStream](../using-nats/jetstream/develop_jetstream.md) documentation for detailed information.*

Kể từ NATS Server 2.2, NATS JetStream cung cấp persistence với đảm bảo giao nhận "at-least-once" và "exactly-once" (trong một khoảng thời gian nhất định). Xem tài liệu [JetStream](../using-nats/jetstream/develop_jetstream.md) để biết thêm chi tiết.

### NATS có hỗ trợ replay/redelivery dữ liệu lịch sử không?

> 🇬🇧 *NATS [JetStream](../using-nats/jetstream/develop_jetstream.md) offers message store and replay by time or sequence.*

NATS [JetStream](../using-nats/jetstream/develop_jetstream.md) hỗ trợ lưu trữ message và replay theo thời gian hoặc theo sequence.

### Làm thế nào để tắt gracefully một asynchronous subscriber?

> 🇬🇧 *To gracefully shut down an asynchronous subscriber so that any outstanding MsgHandlers have a chance to complete outstanding work, call sub.Unsubscribe(). There is a Go routine per subscription. These will be cleaned up on Unsubscribe(), or upon connection teardown.*

Để tắt gracefully một async subscriber và cho phép các MsgHandler đang chạy hoàn tất công việc, hãy gọi `sub.Unsubscribe()`. Mỗi subscription có một Go routine riêng. Chúng sẽ được dọn dẹp khi `Unsubscribe()` được gọi hoặc khi kết nối bị đóng.

### Làm thế nào để tạo subject?

> 🇬🇧 *Subjects are created and pruned (deleted) dynamically based on interest (subscriptions). This means that a subject does not exist in a NATS cluster until a client subscribes to it, and the subject goes away after the last subscribing client unsubscribes from that subject.*

Subject được tạo và xoá động theo interest (subscription). Nghĩa là một subject không tồn tại trong NATS cluster cho đến khi có client đăng ký nhận nó, và subject sẽ biến mất sau khi client đăng ký cuối cùng huỷ đăng ký.

### Có bao nhiêu client có thể kết nối đồng thời?

> 🇬🇧 *The default setting for a single server is 65,536. Although there is no specified limit to the number of connections supported by NATS, there are some environmental factors that will influence your decision as to how many connections to allow per server.*

Mặc định cho một server đơn là 65.536 kết nối. Mặc dù NATS không đặt giới hạn cứng về số lượng kết nối, có một số yếu tố môi trường ảnh hưởng đến quyết định cho phép bao nhiêu kết nối mỗi server.

> 🇬🇧 *Most systems can handle several thousand NATS connections per server without any changes although some have a very low default such as OS X. You'll want to look at kernel/OS settings to increase that limit. You'll also want to look at default TCP buffer sizes to best optimize your machine for your traffic characteristics.*

Hầu hết hệ thống có thể xử lý hàng nghìn kết nối NATS mỗi server mà không cần thay đổi gì, dù một số hệ thống như OS X có giá trị mặc định rất thấp. Bạn cần xem xét cài đặt kernel/OS để tăng giới hạn này. Cũng nên kiểm tra kích thước TCP buffer mặc định để tối ưu máy chủ cho đặc tính traffic của bạn.

> 🇬🇧 *If you are using TLS you'll want to be sure the hardware can handle the CPU load created by TLS negotiation when there is the thundering herd of inbound connections after an outage or network partition event. This often overlooked factor is usually the constraint limiting the number of connections a single server should support. Choosing a cipher suite that is supported by TLS acceleration can mitigate this (e.g. AES with x86). Thinking of the entire system, you'll also want to look at a range of reconnect delay times or add reconnect jitter to the NATS clients to even out the distribution of connection attempts over time and reduce CPU spikes.*

Nếu dùng TLS, cần đảm bảo phần cứng đủ khả năng xử lý tải CPU sinh ra bởi TLS negotiation khi có một lượng lớn kết nối đổ vào đồng thời sau sự cố hoặc network partition. Yếu tố thường bị bỏ qua này thường là giới hạn thực sự cho số kết nối mà một server nên hỗ trợ. Chọn cipher suite được hỗ trợ TLS acceleration (ví dụ AES trên x86) có thể giảm thiểu vấn đề này. Nhìn toàn hệ thống, bạn cũng nên xem xét dải thời gian reconnect hoặc thêm reconnect jitter cho các NATS client để dàn đều các lần kết nối theo thời gian và giảm CPU spike.

> 🇬🇧 *All said, each server can be tuned to handle a large number of clients, and given the flexibility and scalability of NATS with clusters, superclusters, and leaf nodes one can build a NATS deployment supporting many millions of connections.*

Tóm lại, mỗi server có thể được tinh chỉnh để xử lý số lượng lớn client. Với sự linh hoạt và khả năng mở rộng của NATS thông qua cluster, supercluster và leaf node, có thể xây dựng một hệ thống NATS hỗ trợ hàng triệu kết nối.

## Thuật ngữ trong bài

- **async**: bất đồng bộ
- **buffer**: vùng đệm tạm
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **endpoint**: địa chỉ API cụ thể
- **message**: gói dữ liệu được gửi đi
- **metric**: số liệu đo lường
- **publisher**: bên gửi message
- **queue group**: nhóm subscribers chia sẻ tải
- **request**: yêu cầu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **timeout**: thời gian chờ tối đa
- **TLS**: mã hóa TLS