---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/reference/nats-protocol/nats-protocol
title: Giao thức Client
translated: true
translated_at: '2026-05-13T00:00:00+00:00'
---

# Giao thức Client

## Giao thức Client

> 🇬🇧 *The wire protocol used to communicate between the NATS server and clients is a simple, text-based publish/subscribe style protocol. Clients connect to and communicate with `nats-server` (the NATS server) through a regular TCP/IP socket using a small set of protocol operations that are terminated by a new line.*

Giao thức dây (wire protocol) dùng để giao tiếp giữa NATS server và các client là một giao thức publish/subscribe dạng text đơn giản. Client kết nối và giao tiếp với `nats-server` qua TCP/IP socket thông thường, sử dụng một tập nhỏ các lệnh giao thức kết thúc bằng ký tự xuống dòng.

> 🇬🇧 *Unlike traditional messaging systems that use a binary message format that require an API to consume, the text-based NATS protocol makes it easy to implement clients in a wide variety of programming and scripting languages. In fact, refer to the topic [NATS Protocol Demo](../nats-protocol-demo.md) to play with the NATS protocol for yourself using telnet.*

Khác với các hệ thống messaging truyền thống dùng định dạng nhị phân và yêu cầu API để đọc, giao thức dạng text của NATS giúp triển khai client dễ dàng trên nhiều ngôn ngữ lập trình và scripting. Tham khảo [NATS Protocol Demo](../nats-protocol-demo.md) để tự trải nghiệm giao thức NATS qua telnet.

> 🇬🇧 *The NATS server implements a [zero allocation byte parser](https://youtu.be/ylRKac5kSOk?t=10m46s) that is fast and efficient.*

NATS server triển khai [zero allocation byte parser](https://youtu.be/ylRKac5kSOk?t=10m46s) — bộ phân tích cú pháp nhanh và hiệu quả, không phân bổ bộ nhớ thêm.

## Quy ước giao thức

> 🇬🇧 *Control Line with Optional Content: Each interaction between the client and server consists of a control, or protocol, line of text followed, optionally by message content. Most of the protocol messages don't require content, only `PUB`, `MSG`, `HPUB`, and `HMSG` include payloads.*

**Control Line với nội dung tùy chọn**: Mỗi tương tác giữa client và server gồm một dòng lệnh điều khiển (control line), theo sau tùy chọn là nội dung message. Hầu hết các message giao thức không có nội dung; chỉ `PUB`, `MSG`, `HPUB` và `HMSG` mang payload (nội dung chính của message).

> 🇬🇧 *Field Delimiters: The fields of NATS protocol messages are delimited by whitespace characters ` ` (space) or `	` (tab). Multiple whitespace characters will be treated as a single field delimiter.*

**Dấu phân cách trường**: Các trường trong NATS protocol message được phân cách bằng ký tự khoảng trắng ` ` (dấu cách) hoặc `	` (tab). Nhiều ký tự khoảng trắng liên tiếp được coi là một dấu phân cách duy nhất.

> 🇬🇧 *Newlines: NATS uses `␍` followed by `␊` (`␍␊`, `0x0D0A`) to terminate protocol messages. This newline sequence is also used to mark the end of the message payload in `PUB`, `MSG`, `HPUB`, and `HMSG` protocol messages.*

**Ký tự xuống dòng**: NATS dùng `␍` theo sau bởi `␊` (`␍␊`, `0x0D0A`) để kết thúc protocol message. Chuỗi xuống dòng này cũng đánh dấu cuối payload trong các message `PUB`, `MSG`, `HPUB` và `HMSG`.

> 🇬🇧 *Subject names: Subject names, including reply subject names, are case-sensitive and must be non-empty alphanumeric strings with no embedded whitespace. All UTF-8 characters except spaces/tabs and separators which are `.` and `>` are allowed. Subject names can be optionally token-delimited using the dot character (`.`), e.g.:*

**Tên subject** (chuỗi định danh message): Tên subject, bao gồm cả reply subject, phân biệt hoa/thường và phải là chuỗi alphanumeric không rỗng, không chứa khoảng trắng. Tất cả ký tự UTF-8 trừ dấu cách/tab và các ký tự phân cách `.` và `>` đều hợp lệ. Tên subject có thể phân tách token bằng dấu chấm (`.`), ví dụ:

`FOO`, `BAR`, `foo.bar`, `foo.BAR`, `FOO.BAR` và `FOO.BAR.BAZ` đều là tên subject hợp lệ

`FOO. BAR`, `foo. .bar` và`foo..bar` _không_ phải tên subject hợp lệ

> 🇬🇧 *A subject is comprised of 1 or more tokens. Tokens are separated by `.` and can be any non whitespace UTF-8 character. The full wildcard token `>` is only valid as the last token and matches all tokens past that point. A token wildcard, `*` matches any token in the position it was listed. Wildcard tokens should only be used in a wildcard capacity and not part of a literal token.*

Một subject gồm 1 hoặc nhiều token, phân tách bằng `.` và có thể là bất kỳ ký tự UTF-8 nào không phải khoảng trắng. Full wildcard token `>` chỉ hợp lệ ở vị trí cuối cùng và khớp với tất cả token từ đó trở đi. Token wildcard `*` khớp với bất kỳ token nào tại vị trí đó. Wildcard token chỉ nên dùng theo nghĩa wildcard, không nên là một phần của literal token.

> 🇬🇧 *Character Encoding: Subject names should be UTF-8 compatible.*

**Mã hóa ký tự**: Tên subject phải tương thích UTF-8.

> 🇬🇧 *Wildcards: NATS supports the use of wildcards in subject subscriptions.*

**Wildcards**: NATS hỗ trợ dùng wildcard khi subscribe subject.

* Ký tự dấu hoa thị (`*`) khớp với một token đơn ở bất kỳ cấp nào của subject.
* Ký tự lớn hơn (`>`), hay còn gọi là _full wildcard_, khớp với một hoặc nhiều token ở cuối subject và phải là token cuối cùng. Subject wildcard `foo.>` sẽ khớp với `foo.bar` hoặc `foo.bar.baz.1`, nhưng không khớp `foo`.
* Wildcard phải là token riêng biệt (`foo.*.baz` hoặc `foo.>` hợp lệ về cú pháp; `foo*.bar`, `f*o.b*r` và `foo>` thì không)

> 🇬🇧 *For example, the wildcard subscriptions `foo.*.quux` and `foo.>` both match `foo.bar.quux`, but only the latter matches `foo.bar.baz`. With the full wildcard, it is also possible to express interest in every subject that may exist in NATS: `sub > 1`, limited of course by authorization settings.*

Ví dụ, subscription wildcard `foo.*.quux` và `foo.>` đều khớp `foo.bar.quux`, nhưng chỉ cái sau mới khớp `foo.bar.baz`. Với full wildcard, có thể đăng ký nhận mọi subject trong NATS: `sub > 1`, tất nhiên bị giới hạn bởi cài đặt authorization.

## Các message giao thức

> 🇬🇧 *The following table briefly describes the NATS protocol messages. NATS protocol operation names are case insensitive, thus `SUB foo 1␍␊` and `sub foo 1␍␊` are equivalent.*

Bảng dưới đây mô tả ngắn gọn các protocol message của NATS. Tên operation không phân biệt hoa/thường, vì vậy `SUB foo 1␍␊` và `sub foo 1␍␊` là tương đương.

> 🇬🇧 *Click the name to see more detailed information, including syntax:*

Nhấn vào tên để xem thông tin chi tiết, bao gồm cú pháp:

| OP Name                 | Sent By | Description                                                                        |
|-------------------------|---------|------------------------------------------------------------------------------------|
| [`INFO`](.#info)       | Server  | Sent to client after initial TCP/IP connection                                     |
| [`CONNECT`](.#connect) | Client  | Sent to server to specify connection information                                   |
| [`PUB`](.#pub)         | Client  | Publish a message to a subject, with optional reply subject                        |
| [`HPUB`](.#hpub)       | Client  | Publish a message to a subject including NATS headers, with optional reply subject |
| [`SUB`](.#sub)         | Client  | Subscribe to a subject (or subject wildcard)                                       |
| [`UNSUB`](.#unsub)     | Client  | Unsubscribe (or auto-unsubscribe) from subject                                     |
| [`MSG`](.#msg)         | Server  | Delivers a message payload to a subscriber                                         |
| [`HMSG`](.#hmsg)       | Server  | Delivers a message payload to a subscriber with NATS headers                       |
| [`PING`](.#pingpong)   | Both    | PING keep-alive message                                                            |
| [`PONG`](.#pingpong)   | Both    | PONG keep-alive response                                                           |
| [`+OK`](.#okerr)       | Server  | Acknowledges well-formed protocol message in `verbose` mode                        |
| [`-ERR`](.#okerr)      | Server  | Indicates a protocol error. May cause client disconnect.                           |

> 🇬🇧 *The following sections explain each protocol message.*

Các phần dưới đây giải thích từng protocol message.

## INFO

### Mô tả

> 🇬🇧 *A client will need to start as a plain TCP connection, then when the server accepts a connection from the client, it will send information about itself, the configuration and security requirements necessary for the client to successfully authenticate with the server and exchange messages.*

Client bắt đầu bằng kết nối TCP thuần. Khi server chấp nhận kết nối, nó gửi thông tin về bản thân — cấu hình và các yêu cầu bảo mật cần thiết để client xác thực thành công và bắt đầu trao đổi message.

> 🇬🇧 *When using the updated client protocol (see [`CONNECT`](.#connect) below), `INFO` messages can be sent anytime by the server. This means clients with that protocol level need to be able to asynchronously handle `INFO` messages.*

Khi dùng protocol client phiên bản mới (xem [`CONNECT`](.#connect) bên dưới), server có thể gửi message `INFO` bất kỳ lúc nào. Điều này có nghĩa là client ở cấp protocol đó cần xử lý message `INFO` một cách bất đồng bộ (async).

### Cú pháp

`INFO {"option_name":option_value,...}␍␊`

Các tùy chọn hợp lệ được mã hóa dưới dạng JSON như sau:

| name              | description                                                                                                                                                            | type     | presence |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|----------|
| `server_id`       | The unique identifier of the NATS server.                                                                                                                              | string   | always   |
| `server_name`     | The name of the NATS server.                                                                                                                                           | string   | always   |
| `version`         | The version of NATS.                                                                                                                                                   | string   | always   |
| `go`              | The version of golang the NATS server was built with.                                                                                                                  | string   | always   |
| `host`            | The IP address used to start the NATS server, by default this will be `0.0.0.0` and can be configured with `-client_advertise host:port`.                              | string   | always   |
| `port`            | The port number the NATS server is configured to listen on.                                                                                                            | int      | always   |
| `headers`         | Whether the server supports headers.                                                                                                                                   | bool     | always   |
| `max_payload`     | Maximum payload size, in bytes, that the server will accept from the client.                                                                                           | int      | always   |
| `proto`           | An integer indicating the protocol version of the server. The server version 1.2.0 sets this to `1` to indicate that it supports the "Echo" feature.                   | int      | always   |
| `client_id`       | The internal client identifier in the server. This can be used to filter client connections in monitoring, correlate with error logs, etc...                           | uint64   | optional |
| `auth_required`   | If this is true, then the client should try to authenticate upon connect.                                                                                              | bool     | optional |
| `tls_required`    | If this is true, then the client must perform the TLS/1.2 handshake. Note, this used to be `ssl_required` and has been updated along with the protocol from SSL to TLS.| bool     | optional |
| `tls_verify`      | If this is true, the client must provide a valid certificate during the TLS handshake.                                                                                 | bool     | optional |
| `tls_available`   | If this is true, the client can provide a valid certificate during the TLS handshake.                                                                                  | bool     | optional |
| `connect_urls`    | List of server urls that a client can connect to.                                                                                                                      | [string] | optional |
| `ws_connect_urls` | List of server urls that a websocket client can connect to.                                                                                                            | [string] | optional |
| `ldm`             | If the server supports _Lame Duck Mode_ notifications, and the current server has transitioned to lame duck, `ldm` will be set to `true`.                              | bool     | optional |
| `git_commit`      | The git hash at which the NATS server was built.                                                                                                                       | string   | optional |
| `jetstream`       | Whether the server supports JetStream.                                                                                                                                 | bool     | optional |
| `ip`              | The IP of the server.                                                                                                                                                  | string   | optional |
| `client_ip`       | The IP of the client.                                                                                                                                                  | string   | optional |
| `nonce`           | The nonce for use in CONNECT.                                                                                                                                          | string   | optional |
| `cluster`         | The name of the cluster.                                                                                                                                               | string   | optional |
| `domain`          | The configured NATS domain of the server.                                                                                                                              | string   | optional |

#### connect_urls

> 🇬🇧 *The `connect_urls` field is a list of urls the server may send when a client first connects, and when there are changes to server cluster topology. This field is considered optional, and may be omitted based on server configuration and client protocol level.*

Trường `connect_urls` là danh sách URL mà server có thể gửi khi client kết nối lần đầu và khi có thay đổi về topology của cluster. Trường này là tùy chọn và có thể bị bỏ qua tùy theo cấu hình server và cấp protocol của client.

> 🇬🇧 *When a NATS server cluster expands, an `INFO` message is sent to the client with an updated `connect_urls` list. This cloud-friendly feature asynchronously notifies a client of known servers, allowing it to connect to servers not originally configured.*

Khi cluster NATS server mở rộng, một message `INFO` được gửi tới client kèm danh sách `connect_urls` cập nhật. Tính năng thân thiện với cloud này thông báo bất đồng bộ cho client biết các server hiện có, cho phép client kết nối tới server không được cấu hình ban đầu.

> 🇬🇧 *The `connect_urls` will contain a list of strings with an IP and port, looking like this: `"connect_urls":["10.0.0.184:4333","192.168.129.1:4333","192.168.192.1:4333"]`*

`connect_urls` chứa danh sách chuỗi gồm IP và port, có dạng: `"connect_urls":["10.0.0.184:4333","192.168.129.1:4333","192.168.192.1:4333"]`

### Ví dụ

> 🇬🇧 *Below you can see a sample connection string from a telnet connection to the `demo.nats.io` site.*

Dưới đây là ví dụ chuỗi kết nối từ một phiên telnet tới site `demo.nats.io`.

```bash
telnet demo.nats.io 4222
```
```
Trying 107.170.221.32...
Connected to demo.nats.io.
Escape character is '^]'.
INFO {"server_id":"Zk0GQ3JBSrg3oyxCRRlE09","version":"1.2.0","proto":1,"go":"go1.10.3","host":"0.0.0.0","port":4222,"max_payload":1048576,"client_id":2392}
```

## CONNECT

### Mô tả

> 🇬🇧 *The `CONNECT` message is the client version of the [`INFO`](.#info) message. Once the client has established a TCP/IP socket connection with the NATS server, and an [`INFO`](.#info) message has been received from the server, the client may send a `CONNECT` message to the NATS server to provide more information about the current connection as well as security information.*

Message `CONNECT` là phiên bản client của message [`INFO`](.#info). Sau khi client thiết lập kết nối TCP/IP với NATS server và nhận được message [`INFO`](.#info) từ server, client có thể gửi message `CONNECT` để cung cấp thêm thông tin về kết nối hiện tại cũng như thông tin bảo mật.

### Cú pháp

`CONNECT {"option_name":option_value,...}␍␊`

Các tùy chọn hợp lệ được mã hóa dưới dạng JSON như sau:

| name            | description                                                                                                                                                                                                                                                                       | type   | required                     |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------------------------------|
| `verbose`       | Turns on [`+OK`](.#okerr) protocol acknowledgements.                                                                                                                                                                                                                             | bool   | true                         |
| `pedantic`      | Turns on additional strict format checking, e.g. for properly formed subjects.                                                                                                                                                                                                    | bool   | true                         |
| `tls_required`  | Indicates whether the client requires an SSL connection.                                                                                                                                                                                                                          | bool   | true                         |
| `auth_token`    | Client authorization token.                                                                                                                                                                                                                                                       | string | if `auth_required` is `true` |
| `user`          | Connection username.                                                                                                                                                                                                                                                              | string | if `auth_required` is `true` |
| `pass`          | Connection password.                                                                                                                                                                                                                                                              | string | if `auth_required` is `true` |
| `name`          | Client name.                                                                                                                                                                                                                                                                      | string | false                        |
| `lang`          | The implementation language of the client.                                                                                                                                                                                                                                        | string | true                         |
| `version`       | The version of the client.                                                                                                                                                                                                                                                        | string | true                         |
| `protocol`      | Sending `0` (or absent) indicates client supports original protocol. Sending `1` indicates that the client supports dynamic reconfiguration of cluster topology changes by asynchronously receiving [`INFO`](.#info) messages with known servers it can reconnect to.            | int    | false                        |
| `echo`          | If set to `false`, the server (version 1.2.0+) will not send originating messages from this connection to its own subscriptions. Clients should set this to `false` only for server supporting this feature, which is when `proto` in the `INFO` protocol is set to at least `1`. | bool   | false                        |
| `sig`           | In case the server has responded with a `nonce` on `INFO`, then a NATS client must use this field to reply with the signed `nonce`.                                                                                                                                               | string | if `nonce` received          |
| `jwt`           | The JWT that identifies a user permissions and account.                                                                                                                                                                                                                           | string | false                        |
| `no_responders` | Enable [quick replies for cases where a request is sent to a topic with no responders](../../../nats-concepts/core-nats/request-reply/reqreply.md#no-responders).                                                                                                                                           | bool   | false                        |
| `headers`       | Whether the client supports headers.                                                                                                                                                                                                                                              | bool   | false                        |
| `nkey`          | The public NKey to authenticate the client. This will be used to verify the signature (`sig`) against the `nonce` provided in the `INFO` message.                                                                                                                                 | string | false                        |

### Ví dụ

> 🇬🇧 *Here is an example from the default string of the Go client:*

Dưới đây là ví dụ từ chuỗi mặc định của Go client:

```
CONNECT {"verbose":false,"pedantic":false,"tls_required":false,"name":"","lang":"go","version":"1.2.2","protocol":1}␍␊
```

> 🇬🇧 *Most clients set `verbose` to `false` by default. This means that the server should not confirm each message it receives on this connection with a [`+OK`](.#okerr) back to the client.*

Hầu hết client đặt `verbose` thành `false` theo mặc định, nghĩa là server sẽ không xác nhận từng message nhận được trên kết nối này bằng [`+OK`](.#okerr) gửi lại cho client.

## PUB

### Mô tả

> 🇬🇧 *The `PUB` message publishes the message payload to the given subject name, optionally supplying a reply subject. If a reply subject is supplied, it will be delivered to eligible subscribers along with the supplied payload. Note that the payload itself is optional. To omit the payload, set the payload size to 0, but the second CRLF is still required.*

Message `PUB` publish payload (nội dung chính của message) lên subject đã cho, tùy chọn kèm reply subject. Nếu có reply subject, nó sẽ được gửi tới các subscriber (bên đăng ký nhận message) hợp lệ cùng với payload. Payload là tùy chọn — để bỏ qua payload, đặt kích thước bằng 0, nhưng CRLF thứ hai vẫn bắt buộc.

### Cú pháp

`PUB <subject> [reply-to] <#bytes>␍␊[payload]␍␊`

where:

| name       | description                                                                                   | type   | required |
|------------|-----------------------------------------------------------------------------------------------|--------|----------|
| `subject`  | The destination subject to publish to.                                                        | string | true     |
| `reply-to` | The reply subject that subscribers can use to send a response back to the publisher/requestor.| string | false    |
| `#bytes`   | The payload size in bytes.                                                                    | int    | true     |
| `payload`  | The message payload data.                                                                     | string | false    |

### Ví dụ

> 🇬🇧 *To publish the ASCII string message payload "Hello NATS!" to subject FOO:*

Publish payload chuỗi ASCII "Hello NATS!" lên subject FOO:

`PUB FOO 11␍␊Hello NATS!␍␊`

> 🇬🇧 *To publish a request message "Knock Knock" to subject FRONT.DOOR with reply subject JOKE.22:*

Publish request message "Knock Knock" lên subject FRONT.DOOR với reply subject JOKE.22:

`PUB FRONT.DOOR JOKE.22 11␍␊Knock Knock␍␊`

> 🇬🇧 *To publish an empty message to subject NOTIFY:*

Publish message rỗng lên subject NOTIFY:

`PUB NOTIFY 0␍␊␍␊`

## HPUB

### Mô tả

> 🇬🇧 *The `HPUB` message is the same as `PUB` but extends the message payload to include NATS headers. Note that the payload itself is optional. To omit the payload, set the total message size equal to the size of the headers. Note that the trailing CR+LF is still required.*

Message `HPUB` tương tự `PUB` nhưng mở rộng payload để bao gồm NATS header. Payload là tùy chọn — để bỏ qua payload, đặt tổng kích thước message bằng kích thước header. CR+LF cuối vẫn bắt buộc.

> 🇬🇧 *NATS headers are similar, in structure and semantics, to HTTP headers as `name: value` pairs including supporting multi-value headers. Headers can be mixed case and NATS will preserve case between message publisher and message receiver(s). See also [ADR-4 NATS Message Headers](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-4.md).*

NATS header có cấu trúc và ngữ nghĩa tương tự HTTP header, dạng cặp `name: value`, hỗ trợ cả multi-value header. Header có thể viết hoa/thường tùy ý và NATS sẽ giữ nguyên case giữa publisher (bên gửi message) và receiver. Xem thêm [ADR-4 NATS Message Headers](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-4.md).

### Cú pháp

`HPUB <subject> [reply-to] <#header bytes> <#total bytes>␍␊[headers]␍␊␍␊[payload]␍␊`

where:

| name            | description                                                                                     | type   | required |
|-----------------|-------------------------------------------------------------------------------------------------|--------|----------|
| `subject`       | The destination subject to publish to.                                                          | string | true     |
| `reply-to`      | The reply subject that subscribers can use to send a response back to the publisher/requestor.  | string | false    |
| `#header bytes` | The size of the headers section in bytes including the `␍␊␍␊` delimiter before the payload.     | int    | true     |
| `#total bytes`  | The total size of headers and payload sections in bytes.                                        | int    | true     |
| `headers`       | Header version `NATS/1.0␍␊` followed by one or more `name: value` pairs, each separated by `␍␊`.| string | false    |
| `payload`       | The message payload data.                                                                       | string | false    |

### Ví dụ

> 🇬🇧 *To publish the ASCII string message payload "Hello NATS!" to subject FOO with one header Bar with value Baz:*

Publish payload "Hello NATS!" lên subject FOO với một header Bar có giá trị Baz:

`HPUB FOO 22 33␍␊NATS/1.0␍␊Bar: Baz␍␊␍␊Hello NATS!␍␊`

> 🇬🇧 *To publish a request message "Knock Knock" to subject FRONT.DOOR with reply subject JOKE.22 and two headers:*

Publish request "Knock Knock" lên subject FRONT.DOOR với reply subject JOKE.22 và hai header:

`HPUB FRONT.DOOR JOKE.22 45 56␍␊NATS/1.0␍␊BREAKFAST: donut␍␊LUNCH: burger␍␊␍␊Knock Knock␍␊`

> 🇬🇧 *To publish an empty message to subject NOTIFY with one header Bar with value Baz:*

Publish message rỗng lên subject NOTIFY với một header Bar có giá trị Baz:

`HPUB NOTIFY 22 22␍␊NATS/1.0␍␊Bar: Baz␍␊␍␊␍␊`

> 🇬🇧 *To publish a message to subject MORNING MENU with one header BREAKFAST having two values and payload "Yum!"*

Publish message lên subject MORNING MENU với header BREAKFAST có hai giá trị và payload "Yum!":

`HPUB MORNING.MENU 47 51␍␊NATS/1.0␍␊BREAKFAST: donut␍␊BREAKFAST: eggs␍␊␍␊Yum!␍␊`

## SUB

### Mô tả

> 🇬🇧 *`SUB` initiates a subscription to a subject, optionally joining a distributed queue group.*

`SUB` khởi tạo subscription lên một subject, tùy chọn tham gia vào queue group (nhóm subscribers chia sẻ tải) phân tán.

### Cú pháp

`SUB <subject> [queue group] <sid>␍␊`

where:

| name          | description                                                    | type   | required |
|---------------|----------------------------------------------------------------|--------|----------|
| `subject`     | The subject name to subscribe to.                              | string | true     |
| `queue group` | If specified, the subscriber will join this queue group.       | string | false    |
| `sid`         | A unique alphanumeric subscription ID, generated by the client.| string | true     |

### Ví dụ

> 🇬🇧 *To subscribe to the subject `FOO` with the connection-unique subscription identifier (sid) `1`:*

Subscribe subject `FOO` với subscription identifier (sid) duy nhất trong kết nối là `1`:

`SUB FOO 1␍␊`

> 🇬🇧 *To subscribe the current connection to the subject `BAR` as part of distribution queue group `G1` with sid `44`:*

Subscribe kết nối hiện tại tới subject `BAR` trong queue group phân phối `G1` với sid `44`:

`SUB BAR G1 44␍␊`

## UNSUB

### Mô tả

> 🇬🇧 *`UNSUB` unsubscribes the connection from the specified subject, or auto-unsubscribes after the specified number of messages has been received.*

`UNSUB` hủy subscription của kết nối khỏi subject đã chỉ định, hoặc tự động hủy sau khi nhận đủ số lượng message nhất định.

### Cú pháp

`UNSUB <sid> [max_msgs]␍␊`

where:

| name       | description                                                                | type   | required |
|------------|----------------------------------------------------------------------------|--------|----------|
| `sid`      | The unique alphanumeric subscription ID of the subject to unsubscribe from.| string | true     |
| `max_msgs` | A number of messages to wait for before automatically unsubscribing.       | int    | false    |

### Ví dụ

> 🇬🇧 *The following examples concern subject `FOO` which has been assigned sid `1`. To unsubscribe from `FOO`:*

Các ví dụ sau liên quan đến subject `FOO` với sid `1`. Để hủy subscription khỏi `FOO`:

`UNSUB 1␍␊`

> 🇬🇧 *To auto-unsubscribe from `FOO` after 5 messages have been received:*

Tự động hủy subscription khỏi `FOO` sau khi nhận được 5 message:

`UNSUB 1 5␍␊`

## MSG

### Mô tả

> 🇬🇧 *The `MSG` protocol message is used to deliver an application message to the client.*

Protocol message `MSG` dùng để gửi application message tới client.

### Cú pháp

`MSG <subject> <sid> [reply-to] <#bytes>␍␊[payload]␍␊`

where:

| name       | description                                                   | type   | presence |
|------------|---------------------------------------------------------------|--------|----------|
| `subject`  | Subject name this message was received on.                    | string | always   |
| `sid`      | The unique alphanumeric subscription ID of the subject.       | string | always   |
| `reply-to` | The subject on which the publisher is listening for responses.| string | optional |
| `#bytes`   | Size of the payload in bytes.                                 | int    | always   |
| `payload`  | The message payload data.                                     | string | optional |

### Ví dụ

> 🇬🇧 *The following message delivers an application message from subject `FOO.BAR`:*

Message sau gửi application message từ subject `FOO.BAR`:

`MSG FOO.BAR 9 11␍␊Hello World␍␊`

> 🇬🇧 *To deliver the same message along with a reply subject:*

Gửi cùng message kèm theo reply subject:

`MSG FOO.BAR 9 GREETING.34 11␍␊Hello World␍␊`

## HMSG

### Mô tả

> 🇬🇧 *The `HMSG` message is the same as `MSG`, but extends the message payload with headers. See also [ADR-4 NATS Message Headers](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-4.md).*

Message `HMSG` tương tự `MSG`, nhưng mở rộng payload với header. Xem thêm [ADR-4 NATS Message Headers](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-4.md).

### Cú pháp

`HMSG <subject> <sid> [reply-to] <#header bytes> <#total bytes>␍␊[headers]␍␊␍␊[payload]␍␊`

where:

| name            | description                                                                                     | type   | presence |
|-----------------|-------------------------------------------------------------------------------------------------|--------|----------|
| `subject`       | Subject name this message was received on.                                                      | string | always   |
| `sid`           | The unique alphanumeric subscription ID of the subject.                                         | string | always   |
| `reply-to`      | The subject on which the publisher is listening for responses.                                  | string | optional |
| `#header bytes` | The size of the headers section in bytes including the `␍␊␍␊` delimiter before the payload.     | int    | always   |
| `#total bytes`  | The total size of headers and payload sections in bytes.                                        | int    | always   |
| `headers`       | Header version `NATS/1.0␍␊` followed by one or more `name: value` pairs, each separated by `␍␊`.| string | optional |
| `payload`       | The message payload data.                                                                       | string | optional |

### Ví dụ

> 🇬🇧 *The following message delivers an application message from subject `FOO.BAR` with a header:*

Message sau gửi application message từ subject `FOO.BAR` kèm header:

`HMSG FOO.BAR 34 45␍␊NATS/1.0␍␊FoodGroup: vegetable␍␊␍␊Hello World␍␊`

> 🇬🇧 *To deliver the same message along with a reply subject:*

Gửi cùng message kèm reply subject:

`HMSG FOO.BAR 9 BAZ.69 34 45␍␊NATS/1.0␍␊FoodGroup: vegetable␍␊␍␊Hello World␍␊`

## PING/PONG

### Mô tả

> 🇬🇧 *`PING` and `PONG` implement a simple keep-alive mechanism between client and server. Once a client establishes a connection to the NATS server, the server will continuously send `PING` messages to the client at a configurable interval. If the client fails to respond with a `PONG` message within the configured response interval, the server will terminate its connection. If your connection stays idle for too long, it is cut off.*

`PING` và `PONG` triển khai cơ chế keep-alive đơn giản giữa client và server. Sau khi client thiết lập kết nối, server liên tục gửi message `PING` tới client theo chu kỳ cấu hình được. Nếu client không phản hồi bằng message `PONG` trong khoảng thời gian cấu hình, server sẽ ngắt kết nối. Kết nối idle quá lâu cũng bị cắt.

> 🇬🇧 *If the server sends a ping request, you can reply with a pong message to notify the server that you are still interested. You can also ping the server and will receive a pong reply. The ping/pong interval is configurable.*

Khi server gửi ping, client có thể reply bằng pong để báo hiệu vẫn còn kết nối. Client cũng có thể chủ động ping server và nhận được pong. Chu kỳ ping/pong có thể cấu hình.

> 🇬🇧 *The server uses normal traffic as a ping/pong proxy, so a client that has messages flowing may not receive a ping from the server.*

Server coi lưu lượng message bình thường là bằng chứng của kết nối hoạt động, nên client đang có message lưu chuyển có thể không nhận được ping từ server.

### Cú pháp

`PING␍␊`

`PONG␍␊`

### Ví dụ

> 🇬🇧 *The following example shows the demo server pinging the client and finally shutting it down.*

Ví dụ sau minh họa demo server ping client và cuối cùng ngắt kết nối.

```
telnet demo.nats.io 4222

Trying 107.170.221.32...
Connected to demo.nats.io.
Escape character is '^]'.
INFO {"server_id":"Zk0GQ3JBSrg3oyxCRRlE09","version":"1.2.0","proto":1,"go":"go1.10.3","host":"0.0.0.0","port":4222,"max_payload":1048576,"client_id":2392}
PING
PING
-ERR 'Stale Connection'
Connection closed by foreign host.
```

## +OK/ERR

### Mô tả

> 🇬🇧 *When the `verbose` connection option is set to `true` (the default value), the server acknowledges each well-formed protocol message from the client with a `+OK` message. Most NATS clients set the `verbose` option to `false` using the [`CONNECT`](.#connect) message*

Khi tùy chọn kết nối `verbose` được đặt thành `true` (giá trị mặc định), server xác nhận từng protocol message hợp lệ từ client bằng message `+OK`. Hầu hết NATS client đặt tùy chọn `verbose` thành `false` qua message [`CONNECT`](.#connect).

> 🇬🇧 *The `-ERR` message is used by the server indicate a protocol, authorization, or other runtime connection error to the client. Most of these errors result in the server closing the connection.*

Message `-ERR` được server dùng để thông báo lỗi giao thức, lỗi authorization hoặc lỗi runtime khác cho client. Hầu hết các lỗi này dẫn đến server đóng kết nối.

> 🇬🇧 *Handling of these errors usually has to be done asynchronously.*

Việc xử lý các lỗi này thường phải thực hiện bất đồng bộ (async).

### Cú pháp

`+OK␍␊`

`-ERR <error message>␍␊`

> 🇬🇧 *Some protocol errors result in the server closing the connection. Upon receiving these errors, the connection is no longer valid and the client should clean up relevant resources. These errors include:*

Một số lỗi giao thức khiến server đóng kết nối. Khi nhận được các lỗi này, kết nối không còn hợp lệ và client cần dọn dẹp tài nguyên liên quan. Các lỗi đó bao gồm:

* `-ERR 'Unknown Protocol Operation'`: Unknown protocol error
* `-ERR 'Attempted To Connect To Route Port'`: Client attempted to connect to a route port instead of the client port
* `-ERR 'Authorization Violation'`: Client failed to authenticate to the server with credentials specified in the [`CONNECT`](.#connect) message
* `-ERR 'Authorization Timeout'`: Client took too long to authenticate to the server after establishing a connection (default 1 second)
* `-ERR 'Invalid Client Protocol'`: Client specified an invalid protocol version in the [`CONNECT`](.#connect) message
* `-ERR 'Maximum Control Line Exceeded'`: Message destination subject and reply subject length exceeded the maximum control line value specified by the `max_control_line` server option. The default is 1024 bytes.
* `-ERR 'Parser Error'`: Cannot parse the protocol message sent by the client
* `-ERR 'Secure Connection - TLS Required'`: The server requires TLS and the client does not have TLS enabled.
* `-ERR 'Stale Connection'`: The server hasn't received a message from the client, including a `PONG` in too long.
* `-ERR 'Maximum Connections Exceeded`': This error is sent by the server when creating a new connection and the server has exceeded the maximum number of connections specified by the `max_connections` server option. The default is 64k.
* `-ERR 'Slow Consumer'`: The server pending data size for the connection has reached the maximum size (default 10MB).
* `-ERR 'Maximum Payload Violation'`: Client attempted to publish a message with a payload size that exceeds the `max_payload` size configured on the server. This value is supplied to the client upon connection in the initial [`INFO`](.#info) message. The client is expected to do proper accounting of byte size to be sent to the server in order to handle this error synchronously.

> 🇬🇧 *Protocol error messages where the connection remains open are listed below. The client should not close the connection in these cases.*

Các lỗi giao thức không kéo theo đóng kết nối được liệt kê dưới đây. Client không nên đóng kết nối trong các trường hợp này.

* `-ERR 'Invalid Subject'`: Client sent a malformed subject (e.g. `sub foo. 90`)
* `-ERR 'Permissions Violation for Subscription to <subject>'`: The user specified in the [`CONNECT`](.#connect) message does not have permission to subscribe to the subject.
* `-ERR 'Permissions Violation for Publish to <subject>'`: The user specified in the [`CONNECT`](.#connect) message does not have permissions to publish to the subject.

## Thuật ngữ trong bài

- **async**: bất đồng bộ
- **cluster**: cụm nhiều server chạy chung
- **credential**: thông tin đăng nhập
- **header**: phần metadata kèm theo
- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **permission**: quyền truy cập
- **port**: cổng kết nối
- **publisher**: bên gửi message
- **queue group**: nhóm subscribers chia sẻ tải
- **request**: yêu cầu
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **timeout**: thời gian chờ tối đa
- **TLS**: mã hóa TLS
- **token**: chuỗi xác thực