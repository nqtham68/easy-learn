---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/reference/nats-protocol/nats-protocol-demo
title: Demo Giao Thức NATS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Demo Giao Thức NATS

> 🇬🇧 *The virtues of the NATS protocol manifest quickly when you experience how easy it is to use NATS. Because the NATS protocol is text-based, you can use NATS across virtually any platform or language.*

Ưu điểm của giao thức NATS bộc lộ ngay khi bạn thực sự dùng thử — mọi thứ đơn giản đến bất ngờ. Do giao thức này dựa trên văn bản thuần túy, bạn có thể sử dụng NATS trên hầu hết mọi nền tảng và ngôn ngữ.

> 🇬🇧 *In the following demo we use [Telnet](https://en.wikipedia.org/wiki/Telnet). On the wire you can publish and subscribe using a simple [set of protocol commands](./nats-protocol).*

Trong demo dưới đây, chúng ta dùng [Telnet](https://en.wikipedia.org/wiki/Telnet). Trên kết nối thực tế, bạn có thể publish (bên gửi message) và subscribe (bên đăng ký nhận message) chỉ với một [tập lệnh giao thức đơn giản](./nats-protocol).

## Khởi tạo kết nối

> 🇬🇧 *Open a terminal and initiate a connection to the NATS demo instance.*

Mở terminal và kết nối đến NATS demo instance.

```
telnet demo.nats.io 4222
```

> 🇬🇧 *The expected result will roughly look like this. Note the IP address, and `INFO` payload may have different values.*

Kết quả trả về sẽ trông tương tự như sau. Lưu ý rằng địa chỉ IP và payload (nội dung chính của message) `INFO` có thể có giá trị khác nhau.

```
Trying 107.170.221.32...
Connected to demo.nats.io.
Escape character is '^]'.
INFO {"server_id":"NCXMJZYQEWUDJFLYLSTTE745I2WUNCVG3LJJ3NRKSFJXEG6RGK7753DJ","version":"2.0.0","proto":1,"go":"go1.11.10","host":"0.0.0.0","port":4222,"max_payload":1048576,"client_id":5089}
```

## Xác nhận kết nối

> 🇬🇧 *Any client establishing a connection with the server must send `CONNECT` message to confirm the connection. There are several options that can be specified to indicate the client supported features, but for the purpose of this example, we can send an empty payload.*

Mọi client khi thiết lập kết nối với server đều phải gửi message `CONNECT` để xác nhận kết nối. Có một số tùy chọn có thể chỉ định để thông báo các tính năng mà client hỗ trợ, nhưng trong ví dụ này, ta chỉ cần gửi payload rỗng.

```
CONNECT {}
```

> 🇬🇧 *You will see a `+OK` message in response.*

Server sẽ phản hồi bằng một message `+OK`.

## Quan sát chu kỳ ping/pong

> 🇬🇧 *Not long after the `CONNECT` you will see a `PING` message. There is a bi-directional behavior between the client and server to check for liveness. In the case of the server, after some period of time without a `PONG`, the server will shutdown the client connection. If the client does not hear back a `PONG`, it will attempt to reconnect to a different server in a clustered setup, if available.*

Ngay sau `CONNECT`, bạn sẽ thấy message `PING`. Đây là cơ chế kiểm tra liveness hai chiều giữa client và server. Về phía server, nếu sau một khoảng thời gian không nhận được `PONG`, server sẽ đóng kết nối của client. Về phía client, nếu không nhận lại được `PONG`, client sẽ cố kết nối lại với server khác trong cluster (cụm nhiều server chạy chung), nếu có.

> 🇬🇧 *You can respond to the server, but simply typing `PONG` followed by a return.*

Bạn có thể phản hồi server bằng cách gõ `PONG` rồi nhấn Enter.

```
PONG
```

## Đăng ký subscription

> 🇬🇧 *Subscribe to the wildcard subject `foo.*` with subscription ID of `90`.*

Subscribe vào subject (chuỗi định danh message) wildcard `foo.*` với subscription ID là `90`.

```
SUB foo.* 90
```

> 🇬🇧 *An `+OK` message will follow, indicating a successful subscription.*

Server sẽ trả về message `+OK` xác nhận subscription thành công.

## Publish một message

> 🇬🇧 *NATS connection are bi-directional, so we can not only subscribe to subjects, but we can publish to them as well.*

Kết nối NATS là hai chiều — ta không chỉ subscribe vào subject mà còn có thể publish lên đó.

> 🇬🇧 *We can send the `PUB` command followed by the subject, and the length of the message payload that will be followed on the second line. In this case, `hello` is the payload. Once that is typed, hit return which will send the message.*

Gửi lệnh `PUB` kèm theo subject và độ dài của message payload ở dòng tiếp theo. Trong ví dụ này, `hello` là payload. Sau khi nhập xong, nhấn Enter để gửi message.

```text
PUB foo.bar 5
hello
```

> 🇬🇧 *An `+OK` message will follow, indicating a successful publish.*

Server sẽ trả về message `+OK` xác nhận publish thành công.

> 🇬🇧 *Immediately following, a `MSG` message will appear which indicates the subscription received the message that was just published.*

Ngay sau đó, message `MSG` sẽ xuất hiện, cho biết subscriber đã nhận được message vừa publish.

```text
MSG foo.bar 90 5
hello
```

## Hủy subscription

> 🇬🇧 *You can use the `UNSUB` command to unsubscribe from a message.*

Dùng lệnh `UNSUB` để hủy subscription.

> 🇬🇧 *Run the subscriber to unsubscribe:*

Chạy lệnh sau để hủy subscriber:

```text
UNSUB 90
```

## Thử publish lại

> 🇬🇧 *Now that we unsubscribed, if we attempt to publish again, we will receive the `+OK`, but will not receive a `MSG`.*

Sau khi đã hủy subscription, nếu publish lại, ta vẫn nhận được `+OK` nhưng sẽ không còn nhận được `MSG`.

```text
PUB foo.bar 7
goodbye
```

## Đóng kết nối

> 🇬🇧 *Use `ctrl+c` to close the connection, however, as noted above, if this is not done, after some period of inactivity the server will automatically close the connection.*

Dùng `ctrl+c` để đóng kết nối. Tuy nhiên, như đã đề cập, nếu không chủ động đóng, server sẽ tự động ngắt kết nối sau một khoảng thời gian không hoạt động.

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **cluster**: cụm nhiều server chạy chung
- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **publisher**: bên gửi message
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message