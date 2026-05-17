---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/reference/nats-protocol/nats-protocol/nats-client-dev
title: Phát triển một Client
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Phát triển một Client

## Hướng dẫn phát triển NATS Client

> 🇬🇧 *This guide provides you with considerations for developing NATS clients, including:*

Hướng dẫn này trình bày các vấn đề cần lưu ý khi phát triển NATS client, bao gồm:

* Xử lý CONNECT
* Authorization
* Verbose (acks)
* Chế độ Pedantic
* Khoảng thời gian Ping/pong
* Phân tích cú pháp protocol
* Lựa chọn chiến lược parsing
* Lưu trữ và dispatch các subscription callback
* Triển khai request/response
* Xử lý lỗi, ngắt kết nối và kết nối lại
* Hỗ trợ cluster

> 🇬🇧 *Probably the best way to learn about implementing a client is to look at one of the client's maintained by the Synadia team. These clients are generally full featured, so if you can use them, that is even better, but if you have to write a client these may go beyond your needs while still capturing many of the design considerations discussed here.*

Cách hiệu quả nhất để học cách triển khai một client là xem các client do nhóm Synadia duy trì. Những client này thường đầy đủ tính năng — nếu dùng được thì càng tốt. Nếu bạn phải tự viết, chúng có thể vượt quá nhu cầu thực tế nhưng vẫn thể hiện rõ nhiều cân nhắc thiết kế được đề cập ở đây.

* [GoLang](https://github.com/nats-io/nats.go)
* [Java](https://github.com/nats-io/nats.java)
* [C\# / .NET](https://github.com/nats-io/nats.net)
* [Rust](https://github.com/nats-io/nats.rs)
* [JavaScript](https://github.com/nats-io/nats.js)
* [Python](https://github.com/nats-io/nats.py)
* [C](https://github.com/nats-io/nats.c)

Xem [Developing with NATS](../../../using-nats/developing-with-nats/developer.md) để biết thêm các link và ngôn ngữ được cộng đồng hỗ trợ.

## Tùy chọn kết nối của Client

> 🇬🇧 *Clients can connect in authenticated or unauthenticated mode, as well as verbose mode which enables acknowledgements. See the [protocol documentation](.#connect) for details.*

Client có thể kết nối theo chế độ có xác thực (authenticated) hoặc không xác thực (unauthenticated), cũng như chế độ verbose để bật acknowledgement. Xem [tài liệu protocol](.#connect) để biết chi tiết.

## Authorization cho Client

> 🇬🇧 *By default clients can connect to the server in unauthenticated mode. You can configure the NATS server to require password authentication to connect.*

Mặc định, client có thể kết nối với server ở chế độ không xác thực. Bạn có thể cấu hình NATS server yêu cầu xác thực bằng mật khẩu khi kết nối.

> 🇬🇧 *For example, using the command line:*

Ví dụ, dùng command line:

```shell
nats-server -DV -m 8222 -user foo -pass bar
```

> 🇬🇧 *The client must then authenticate to connect to the server. For example:*

Khi đó client phải xác thực để kết nối với server. Ví dụ:

```shell
nats.Connect("nats://foo:bar@localhost:4222")
```

## Chế độ Verbose

> 🇬🇧 *When 'verbose' is enabled (via the `CONNECT` message), the NATS server will return `+OK` to acknowledge receipt of a valid protocol message. The NATS server automatically runs in verbose mode. Most client implementations disable verbose mode (set it to `false` in the `CONNECT` message) for performance reasons.*

Khi bật chế độ verbose (qua message `CONNECT`), NATS server sẽ trả về `+OK` để xác nhận đã nhận được một protocol message hợp lệ. NATS server mặc định chạy ở chế độ verbose. Hầu hết các cài đặt client tắt chế độ này (đặt thành `false` trong message `CONNECT`) vì lý do hiệu năng.

## Chế độ Pedantic

> 🇬🇧 *A client may also support 'pedantic' mode. Pedantic mode indicates to the server that strict protocol enforcement is required.*

Client cũng có thể hỗ trợ chế độ pedantic. Chế độ này báo cho server biết rằng cần thực thi protocol một cách nghiêm ngặt.

## Khoảng thời gian Ping/pong

> 🇬🇧 *NATS implements auto-pruning. When a client connects to the server, the server expects that client to be active. Periodically, the NATS server pings each subscriber, expecting a reply. If there is no reply within the configurable time limit, the server disconnects the client.*

NATS triển khai cơ chế auto-pruning. Khi client kết nối vào server, server mong đợi client đó luôn hoạt động. Định kỳ, NATS server gửi ping đến từng subscriber (bên đăng ký nhận message) và chờ phản hồi. Nếu không nhận được phản hồi trong khoảng thời gian cấu hình, server sẽ ngắt kết nối client.

## Phân tích cú pháp Protocol

> 🇬🇧 *NATS provides a text-based message format. The text-based [protocol](.) makes it easy to implement NATS clients. The key consideration is deciding on a parsing strategy.*

NATS sử dụng định dạng message dạng văn bản. [Protocol](.) dạng này giúp việc triển khai NATS client trở nên đơn giản. Điều quan trọng là cần quyết định chiến lược parsing ngay từ đầu.

> 🇬🇧 *The NATS server implements a [zero allocation byte parser](https://youtu.be/ylRKac5kSOk?t=10m46s) that is fast and efficient. Off the wire, a NATS message is simply a slice of bytes. Across the wire the message is transported as an immutable string over a TCP connection. It is up to the client to implement logic to parse the message.*

NATS server triển khai [zero allocation byte parser](https://youtu.be/ylRKac5kSOk?t=10m46s) — nhanh và hiệu quả. Khi nhận từ wire, một NATS message chỉ đơn giản là một slice byte. Trên đường truyền, message được vận chuyển dưới dạng chuỗi bất biến qua kết nối TCP. Client phải tự triển khai logic để parse message.

> 🇬🇧 *The NATS message structure includes the Subject string, an optional Reply string, and an optional Data field that is a byte array. The type `Msg` is a structure used by Subscribers and PublishMsg().*

Cấu trúc NATS message gồm chuỗi subject (chuỗi định danh message), một chuỗi Reply tùy chọn, và một trường Data tùy chọn là mảng byte. Kiểu `Msg` là cấu trúc được dùng bởi subscriber và `PublishMsg()`.

```text
type Msg struct {
    Subject string
    Reply   string
    Data    []byte
    Sub     *Subscription
}
```

> 🇬🇧 *A NATS publisher publishes the data argument to the given subject. The data argument is left untouched and needs to be correctly interpreted on the receiver. How the client parses a NATS message depends on the programming language.*

Publisher (bên gửi message) publish đối số data lên subject đã chỉ định. Đối số data được giữ nguyên và cần được phía nhận tự diễn giải đúng. Cách client parse một NATS message phụ thuộc vào ngôn ngữ lập trình.

## Lựa chọn Chiến lược Parsing

> 🇬🇧 *Generally, protocol parsing for a NATS client is a string operation. In Python, for example, string operations are faster than regex. The Go and Java clients also use string operations to parse the message. But, if you look at the Ruby client, regex is used to parse the protocol because in Ruby regex is faster than string operations.*

Nhìn chung, parsing protocol trong NATS client là thao tác chuỗi. Trong Python, thao tác chuỗi nhanh hơn regex. Client Go và Java cũng dùng thao tác chuỗi để parse message. Tuy nhiên, với Ruby client lại dùng regex vì trong Ruby, regex nhanh hơn thao tác chuỗi.

> 🇬🇧 *In sum, there is no magic formula for parsing—it depends on the programming language. But, you need to take into consideration how you are going to parse the message when you write a client.*

Tóm lại, không có công thức cố định cho việc parsing — tất cả phụ thuộc vào ngôn ngữ lập trình. Khi viết client, bạn cần cân nhắc trước cách parse message.

## Lưu trữ và Dispatch Subscription Callback

> 🇬🇧 *When you make a subscription to the server, you need to store and dispatch callback handlers.*

Khi tạo một subscription lên server, bạn cần lưu trữ và dispatch các callback (hàm được gọi lại) handler.

> 🇬🇧 *On the client side, you need a hash map for this data structure. The hash map will be storing the callback that maps the subscription ID to the subscription.*

Ở phía client, cần một hash map cho cấu trúc dữ liệu này. Hash map lưu callback ánh xạ subscription ID sang subscription tương ứng.

> 🇬🇧 *The key of the hash map is the subscription ID. The key is used to look up the callback in the hash map. When you process the NATS message off the wire, you pass the parameters subject, reply subject, and the payload to the callback handler, which does its work.*

Key của hash map là subscription ID, dùng để tra cứu callback. Khi xử lý NATS message từ wire, bạn truyền các tham số subject, reply subject và payload (nội dung chính của message) vào callback handler để nó thực thi.

> 🇬🇧 *Thus, you must store the mapping of subscription ID to the callback. Inside the subscription you have the callback.*

Do đó, bạn phải lưu ánh xạ từ subscription ID sang callback. Bên trong subscription chứa callback đó.

## Triển khai Request/Response

> 🇬🇧 *When to use pub/sub vs. req/rep depends on your use case. Run the tutorials for each to understand the differences between each style of implementation.*

Việc dùng pub/sub hay req/rep phụ thuộc vào use case của bạn. Hãy chạy thử các tutorial cho từng kiểu để hiểu sự khác biệt.

## Xử lý Lỗi, Ngắt kết nối và Kết nối lại

> 🇬🇧 *Considerations for error handling primarily include handling client disconnections and implementing retry logic.*

Các vấn đề xử lý lỗi chủ yếu xoay quanh việc xử lý ngắt kết nối của client và triển khai retry logic.

## Hỗ trợ Cluster

> 🇬🇧 *The NATS client has reconnection logic. So, if you are implementing clustering, you need to implement reconnect callbacks a priori, meaning you cannot modify it during runtime. When you start it, you need to have that information already.*

NATS client có sẵn logic kết nối lại. Vì vậy, khi triển khai clustering, bạn cần khai báo reconnect callback từ trước — không thể thay đổi trong lúc runtime. Thông tin đó phải có sẵn ngay khi khởi động.

## Thuật ngữ trong bài

- **callback**: hàm được gọi lại
- **cluster**: cụm nhiều server chạy chung
- **payload**: nội dung chính của message
- **publisher**: bên gửi message
- **request**: yêu cầu
- **response**: phản hồi
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **subscription**: (đăng ký nhận message)