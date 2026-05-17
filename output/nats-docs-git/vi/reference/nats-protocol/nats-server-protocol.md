---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/reference/nats-protocol/nats-server-protocol
title: NATS Cluster Protocol
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# NATS Cluster Protocol

## NATS Cluster Protocol

> 🇬🇧 *The NATS server clustering protocol describes the protocols passed between NATS servers within a [cluster](../../running-a-nats-service/configuration/clustering) to share accounts, subscriptions, forward messages, and share cluster topology regarding new servers. It is a simple text-based protocol. Servers communicate with each other through a regular TCP/IP or TLS socket using a small set of protocol operations that are terminated by newline.*

NATS cluster (cụm nhiều server chạy chung) protocol mô tả các giao thức trao đổi giữa các NATS server trong cùng một cluster nhằm chia sẻ account, subscription, chuyển tiếp message và cập nhật topology khi có server mới. Đây là giao thức dạng văn bản đơn giản. Các server giao tiếp với nhau qua TCP/IP thông thường hoặc TLS, sử dụng một tập nhỏ các lệnh protocol kết thúc bằng ký tự newline.

> 🇬🇧 *The NATS server implements a [zero allocation byte parser](https://youtu.be/ylRKac5kSOk?t=10m46s) that is fast and efficient.*

NATS server triển khai [zero allocation byte parser](https://youtu.be/ylRKac5kSOk?t=10m46s) — bộ phân tích nhanh và hiệu quả, không cấp phát bộ nhớ động.

> 🇬🇧 *The NATS cluster protocol is very similar to that of the NATS client protocol. In the context of a cluster, it can be helpful to visualize a server being a proxy operating on behalf of its connected clients, subscribing, unsubscribing, sending and receiving messages.*

NATS cluster protocol rất giống với NATS client protocol. Trong ngữ cảnh cluster, có thể hình dung mỗi server như một proxy hoạt động thay mặt cho các client đang kết nối — đăng ký, hủy đăng ký, gửi và nhận message.

## Quy ước NATS Cluster Protocol

> 🇬🇧 ***Subject names and wildcards**: The NATS cluster protocol has the same features and restrictions as the client with respect to subject names and wildcards. Clients are bound to a single account, however the cluster protocol handles all accounts.*

**Tên subject và wildcard**: NATS cluster protocol có cùng tính năng và ràng buộc với client protocol về tên subject (chuỗi định danh message) và wildcard. Mỗi client chỉ thuộc một account, nhưng cluster protocol xử lý toàn bộ các account.

> 🇬🇧 ***Field Delimiters**: The fields of NATS protocol messages are delimited by whitespace characters '`` `'\(space\) or ``\t\` (tab). Multiple whitespace characters will be treated as a single field delimiter.*

**Dấu phân cách trường**: Các trường trong NATS protocol message được phân tách bằng ký tự khoảng trắng '`` ``'\(space\) hoặc ``\t\`` (tab). Nhiều ký tự khoảng trắng liên tiếp được xem là một dấu phân cách duy nhất.

> 🇬🇧 ***Newlines**: Like other text-based protocols, NATS uses `CR` followed by `LF` (`CR+LF`, `\r`, `0x0D0A`) to terminate protocol messages. This newline sequence is also used to mark the beginning of the actual message payload in a `RMSG` protocol message.*

**Newline**: Giống các giao thức văn bản khác, NATS dùng `CR` theo sau là `LF` (`CR+LF`, `\r`, `0x0D0A`) để kết thúc protocol message. Chuỗi newline này cũng đánh dấu vị trí bắt đầu của payload (nội dung chính của message) thực sự trong message `RMSG`.

## Các message trong NATS Cluster Protocol

> 🇬🇧 *The following table briefly describes the NATS cluster protocol messages. As in the client protocol, the NATS protocol operation names are case insensitive, thus `SUB foo 1\r` and `sub foo 1\r` are equivalent.*

Bảng dưới đây mô tả tóm tắt các message trong NATS cluster protocol. Giống client protocol, tên các lệnh không phân biệt hoa thường — `SUB foo 1\r` và `sub foo 1\r` là tương đương.

> 🇬🇧 *Click the name to see more detailed information, including syntax:*

Nhấn tên lệnh để xem thông tin chi tiết bao gồm cú pháp:

| OP Name                                      | Sent By       | Description                                                                  |
| -------------------------------------------- | ------------- | ---------------------------------------------------------------------------- |
| [`INFO`](./nats-server-protocol.md#info)       | All Servers   | Sent after initial TCP/IP connection and to update cluster knowledge         |
| [`CONNECT`](./nats-server-protocol.md#connect) | All Servers   | Sent to establish a route                                                    |
| [`RS+`](./nats-server-protocol.md#sub)         | All Servers   | Subscribes to a subject for a given account on behalf of interested clients. |
| [`RS-`](./nats-server-protocol.md#unsub)       | All Servers   | Unsubscribe (or auto-unsubscribe) from subject for a given account.          |
| [`RMSG`](./nats-server-protocol.md#rmsg)       | Origin Server | Delivers a message for a given subject and account to another server.        |
| [`PING`](./nats-server-protocol.md#pingpong)   | All Servers   | PING keep-alive message                                                      |
| [`PONG`](./nats-server-protocol.md#pingpong)   | All Servers   | PONG keep-alive response                                                     |
| [`-ERR`](./nats-server-protocol.md#-err)       | All Servers   | Indicates a protocol error. May cause the remote server to disconnect.       |

> 🇬🇧 *The following sections explain each protocol message.*

Các phần tiếp theo giải thích chi tiết từng protocol message.

## INFO

### Mô tả

> 🇬🇧 *As soon as the server accepts a connection from another server, it will send information about itself and the configuration and security requirements that are necessary for the other server to successfully authenticate with the server and exchange messages.*

Ngay khi server chấp nhận kết nối từ server khác, nó gửi thông tin về bản thân cùng các yêu cầu config và bảo mật cần thiết để server đối tác xác thực thành công và trao đổi message.

> 🇬🇧 *The connecting server also sends an `INFO` message. The accepting server will add an `ip` field containing the address and port of the connecting server, and forward the new server's `INFO` message to all servers it is routed to.*

Server đang kết nối cũng gửi message `INFO`. Server chấp nhận kết nối sẽ thêm trường `ip` chứa địa chỉ và port của server kết nối, sau đó chuyển tiếp message `INFO` của server mới tới tất cả các server trong route của nó.

> 🇬🇧 *Any servers in a cluster receiving an `INFO` message with an `ip` field will attempt to connect to the server at that address, unless already connected. This propagation of `INFO` messages on behalf of a connecting server provides automatic discovery of new servers joining a cluster.*

Bất kỳ server nào trong cluster nhận được message `INFO` có trường `ip` đều sẽ thử kết nối tới địa chỉ đó, trừ khi đã kết nối rồi. Cơ chế lan truyền message `INFO` này cho phép tự động phát hiện server mới gia nhập cluster.

### Cú pháp

`INFO {["option_name":option_value],...}`

> 🇬🇧 *The valid options are as follows:*

Các tùy chọn hợp lệ:

* `server_id`: Định danh duy nhất của NATS server
* `version`: Phiên bản NATS server
* `go`: Phiên bản golang dùng để build NATS server
* `host`: Host chỉ định trong tham số/tùy chọn cluster
* `port`: Port chỉ định trong tham số/tùy chọn cluster
* `auth_required`: Nếu được đặt, server phải xác thực khi kết nối.
* `tls_required`: Nếu được đặt, server bắt buộc xác thực qua TLS.
* `max_payload`: Kích thước payload tối đa server chấp nhận.
* `connect_urls` : Danh sách URL server mà client có thể kết nối.
* `ip`: Địa chỉ kết nối route tùy chọn của server, `nats-route://<hostname>:<port>`

### Ví dụ

> 🇬🇧 *Below is an example of an `INFO` string received by a NATS server, with the `ip` field.*

Dưới đây là ví dụ chuỗi `INFO` mà một NATS server nhận được, kèm trường `ip`.

```
INFO {"server_id":"KP19vTlB417XElnv8kKaC5","version":"2.0.0","go":"","host":"localhost","port":5222,"auth_required":false,"tls_required":false,"tls_verify":false,"max_payload":1048576,"ip":"nats-route://127.0.0.1:5222/","connect_urls":["localhost:4222"]}
```

## CONNECT

### Mô tả

> 🇬🇧 *The `CONNECT` message is analogous to the [`INFO`](./nats-server-protocol.md#info) message. Once the NATS server has established a TCP/IP socket connection with another server, and an [`INFO`](./nats-server-protocol.md#info) message has been received, the server will send a `CONNECT` message to provide more information about the current connection as well as security information.*

Message `CONNECT` tương tự như message [`INFO`](./nats-server-protocol.md#info). Sau khi NATS server thiết lập kết nối TCP/IP socket với server khác và nhận được message [`INFO`](./nats-server-protocol.md#info), server sẽ gửi message `CONNECT` để cung cấp thêm thông tin về kết nối hiện tại và thông tin bảo mật.

### Cú pháp

`CONNECT {["option_name":option_value],...}`

> 🇬🇧 *The valid options are as follows:*

Các tùy chọn hợp lệ:

* `tls_required`: Cho biết server có yêu cầu kết nối SSL không.
* `auth_token`: Token xác thực
* `user`: Username kết nối (nếu `auth_required` được đặt)
* `pass`: Password kết nối (nếu `auth_required` được đặt)
* `name`: Tên server được tạo tự động
* `lang`: Ngôn ngữ triển khai server (go).
* `version`: Phiên bản server.

### Ví dụ

> 🇬🇧 *Here is an example from the default string from a server.*

Dưới đây là ví dụ chuỗi mặc định từ một server.

`CONNECT {"tls_required":false,"name":"wt0vffeQyoDGMVBC2aKX0b"}\r`

## RS+

### Mô tả

> 🇬🇧 *`RS+` initiates a subscription to a subject on on a given account, optionally with a distributed queue group name and weighting factor. Note that queue subscriptions will use RS+ for increases and decreases to queue weight except when the weighting factor is 0.*

`RS+` khởi tạo subscription tới một subject trên account nhất định, tùy chọn kèm tên queue group và hệ số weight. Lưu ý: các queue subscription dùng RS+ để tăng/giảm queue weight, trừ khi hệ số weight bằng 0.

### Cú pháp

**Subscription**: `RS+ <account> <subject>\r`

**Queue Subscription**: `RS+ <account> <subject> <queue> <weight>\r`

> 🇬🇧 *where:*

trong đó:

* `account`: Account liên kết với subject interest
* `subject`: Subject
* `queue`: Tên queue group tùy chọn
* `weight`: Hệ số weight queue group tùy chọn, biểu thị mức độ interest/số subscriber

## RS-

### Mô tả

> 🇬🇧 *`RS-` unsubcribes from the specified subject on the given account. It is sent by a server when it no longer has interest in a given subject.*

`RS-` hủy subscription khỏi subject chỉ định trên account đã cho. Server gửi lệnh này khi không còn interest với subject đó.

### Cú pháp

**Subscription**: `RS- <account> <subject>\r`

> 🇬🇧 *where:*

trong đó:

* `account`: Account liên kết với subject interest
* `subject`: Subject

## RMSG

### Mô tả

> 🇬🇧 *The `RMSG` protocol message delivers a message to another server.*

Protocol message `RMSG` chuyển tiếp một message tới server khác.

### Cú pháp

`RMSG <account> <subject> [reply-to] <#bytes>\r\n[payload]\r`

> 🇬🇧 *where:*

trong đó:

* `account`: Account liên kết với subject interest
* `subject`: Tên subject mà message này được nhận trên đó
* `reply-to`: Reply subject tùy chọn
* `#bytes`: Kích thước payload tính theo byte
* `payload`: Dữ liệu payload của message

## PING/PONG

### Mô tả

> 🇬🇧 *`PING` and `PONG` implement a simple keep-alive mechanism between servers. Once two servers establish a connection with each other, the NATS server will continuously send `PING` messages to other servers at a configurable interval. If another server fails to respond with a `PONG` message within the configured response interval, the server will terminate its connection. If your connection stays idle for too long, it is cut off.*

`PING` và `PONG` triển khai cơ chế keep-alive đơn giản giữa các server. Sau khi hai server thiết lập kết nối, NATS server liên tục gửi message `PING` tới server đối tác theo chu kỳ có thể cấu hình. Nếu server kia không phản hồi bằng message `PONG` trong khoảng thời gian cho phép, kết nối sẽ bị cắt. Kết nối để idle quá lâu cũng sẽ bị ngắt.

> 🇬🇧 *If the another server sends a ping request, a server will reply with a pong message to notify the other server that it is still present.*

Nếu server đối tác gửi yêu cầu ping, server hiện tại sẽ phản hồi bằng pong để thông báo rằng nó vẫn đang hoạt động.

### Cú pháp

`PING\r` `PONG\r`

## -ERR

### Mô tả

> 🇬🇧 *The `-ERR` message is used by the server to indicate a protocol, authorization, or other runtime connection error to another server. Most of these errors result in the remote server closing the connection.*

Message `-ERR` được server dùng để thông báo lỗi protocol, lỗi authorization hoặc lỗi runtime khác tới server đối tác. Phần lớn các lỗi này dẫn đến việc server từ xa đóng kết nối.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **payload**: nội dung chính của message
- **port**: cổng kết nối
- **queue group**: nhóm subscribers chia sẻ tải
- **subject**: chuỗi định danh message (giống topic)
- **TLS**: mã hóa TLS
- **token**: chuỗi xác thực