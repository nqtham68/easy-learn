---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/clients
title: NATS Server - Kết Nối Client
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# NATS Server - Kết Nối Client

> 🇬🇧 *A NATS client is an application making a connection to one of the nats servers pointed to by its connection URL, and uses a credential file to authenticate and indicate its authorization to the server and the whole NATS infrastructure.*

NATS client là một ứng dụng kết nối đến một trong các nats-server thông qua connection URL, đồng thời dùng credential file (thông tin đăng nhập) để xác thực và khai báo quyền truy cập với server cũng như toàn bộ hạ tầng NATS.

> 🇬🇧 *The nats-server doesn't come bundled with any clients, but its companion is the [`nats`](https://docs.nats.io/using-nats/nats-tools/nats\_cli) CLI tool that you should install (even if you don't intend to run your own servers) as it is the best tool to use to test, monitor, manage and generally interact with a NATS infrastructure (regardless of that infrastructure being an isolated local server, a leaf node server, a cluster or even a global super-cluster).*

nats-server không đi kèm bất kỳ client nào, nhưng công cụ bổ trợ của nó là CLI tool [`nats`](https://docs.nats.io/using-nats/nats-tools/nats\_cli) — nên cài đặt ngay cả khi bạn không định tự vận hành server, vì đây là công cụ tốt nhất để test, monitor, quản lý và tương tác với hạ tầng NATS (dù là một server cục bộ độc lập, leaf node server, cluster (cụm nhiều server chạy chung), hay thậm chí một super-cluster toàn cầu).

> 🇬🇧 *Other NATS client tools to know about are the [`nsc`](../using-nats/nats-tools/nsc) CLI tool (to manage accounts attributes and user JWT tokens) and the ['nk'](../using-nats/nats-tools/nk.md) tool (and library) to manage Nkeys.*

Các công cụ client NATS khác cần biết: CLI tool [`nsc`](../using-nats/nats-tools/nsc) (quản lý thuộc tính account và JWT token của user) và tool (cùng library) [`nk`](../using-nats/nats-tools/nk.md) để quản lý Nkeys.

> 🇬🇧 *Also, most client libraries come with sample programs that allow you to publish, subscribe, send requests and reply messages.*

Ngoài ra, hầu hết các client library đều đi kèm chương trình mẫu cho phép publish, subscribe, gửi request và reply message (gói dữ liệu được gửi đi).

## Nhúng NATS vào ứng dụng

> 🇬🇧 *If your application is in Go, and if it fits your use case and deployment scenarios, you can even embed a NATS server inside your application.*

Nếu ứng dụng viết bằng Go và phù hợp với use case cùng kịch bản deploy, bạn có thể nhúng trực tiếp NATS server vào trong ứng dụng.

[Embedding NATS in Go](https://dev.to/karanpratapsingh/embedding-nats-in-go-19o)

## Cài đặt CLI Tool `nats`

> 🇬🇧 *Please refer to the [installation section in the readme](https://github.com/nats-io/natscli?tab=readme-ov-file#installation).*

Tham khảo [phần hướng dẫn cài đặt trong readme](https://github.com/nats-io/natscli?tab=readme-ov-file#installation).

## Kiểm thử cài đặt

> 🇬🇧 *Open a terminal and [start a nats-server](https://docs.nats.io/running-a-nats-service/broken-reference):*

Mở terminal và [khởi động nats-server](https://docs.nats.io/running-a-nats-service/broken-reference):

```shell
nats-server
```

```
[45695] 2021/09/29 02:22:53.570667 [INF] Starting nats-server
[45695] 2021/09/29 02:22:53.570796 [INF]   Version:  2.6.1
[45695] 2021/09/29 02:22:53.570799 [INF]   Git:      [not set]
[45695] 2021/09/29 02:22:53.570804 [INF]   Name:     NAAACXGWSD6ZW5KVHOTSGGPU2JCMZUDSMY5GVZZP27DMRPWYINC2X6ZI
[45695] 2021/09/29 02:22:53.570807 [INF]   ID:       NAAACXGWSD6ZW5KVHOTSGGPU2JCMZUDSMY5GVZZP27DMRPWYINC2X6ZI
[45695] 2021/09/29 02:22:53.571747 [INF] Listening for client connections on 0.0.0.0:4222
[45695] 2021/09/29 02:22:53.572051 [INF] Server is ready
```

> 🇬🇧 *On another terminal session first check the connection to the server*

Ở một terminal khác, kiểm tra kết nối đến server trước:

```shell
nats server check connection -s nats://0.0.0.0:4222
```

```
OK Connection OK:connected to nats://127.0.0.1:4222 in 790.28µs OK:rtt time 69.896µs OK:round trip took 0.000102s | connect_time=0.0008s;0.5000;1.0000 rtt=0.0001s;0.5000;1.0000 request_time=0.0001s;0.5000;1.0000
```

> 🇬🇧 *Next, start a subscriber using the `nats` CLI tool:*

Tiếp theo, khởi động một subscriber (bên đăng ký nhận message) bằng CLI tool `nats`:

```shell
nats subscribe ">" -s nats://0.0.0.0:4222
```

> 🇬🇧 *Note that when the client connected, the server didn't log anything interesting because server output is relatively quiet unless something interesting happens.*

Lưu ý rằng khi client kết nối, server không ghi log gì đáng chú ý — output của server khá im lặng trừ khi có sự kiện quan trọng xảy ra.

> 🇬🇧 *To make the server output more lively, you can specify the `-V` flag to enable logging of server protocol tracing messages. Go ahead and `<ctrl>+c` the process running the server, and restart the server with the `-V` flag:*

Để server output chi tiết hơn, dùng flag `-V` để bật log trace protocol. Hãy `<ctrl>+c` process đang chạy server rồi khởi động lại với flag `-V`:

```shell
nats-server -V
```

```
[45703] 2021/09/29 02:23:05.189377 [INF] Starting nats-server
[45703] 2021/09/29 02:23:05.189489 [INF]   Version:  2.6.1
[45703] 2021/09/29 02:23:05.189493 [INF]   Git:      [not set]
[45703] 2021/09/29 02:23:05.189497 [INF]   Name:     NAIBOVQLOZSDIUFQYZOQUGV3PNZUT66D4WF5MKS2G7N423UGJDH2DFWG
[45703] 2021/09/29 02:23:05.189500 [INF]   ID:       NAIBOVQLOZSDIUFQYZOQUGV3PNZUT66D4WF5MKS2G7N423UGJDH2DFWG
[45703] 2021/09/29 02:23:05.190236 [INF] Listening for client connections on 0.0.0.0:4222
[45703] 2021/09/29 02:23:05.190504 [INF] Server is ready
[45703] 2021/09/29 02:23:07.111053 [TRC] 127.0.0.1:51653 - cid:4 - <<- [CONNECT {"verbose":false,"pedantic":false,"tls_required":false,"name":"NATS CLI Version 0.0.26","lang":"go","version":"1.12.0","protocol":1,"echo":true,"headers":true,"no_responders":true}]
[45703] 2021/09/29 02:23:07.111282 [TRC] 127.0.0.1:51653 - cid:4 - "v1.12.0:go:NATS CLI Version 0.0.26" - <<- [PING]
[45703] 2021/09/29 02:23:07.111301 [TRC] 127.0.0.1:51653 - cid:4 - "v1.12.0:go:NATS CLI Version 0.0.26" - ->> [PONG]
[45703] 2021/09/29 02:23:07.111632 [TRC] 127.0.0.1:51653 - cid:4 - "v1.12.0:go:NATS CLI Version 0.0.26" - <<- [SUB >  1]
[45703] 2021/09/29 02:23:07.111679 [TRC] 127.0.0.1:51653 - cid:4 - "v1.12.0:go:NATS CLI Version 0.0.26" - <<- [PING]
[45703] 2021/09/29 02:23:07.111689 [TRC] 127.0.0.1:51653 - cid:4 - "v1.12.0:go:NATS CLI Version 0.0.26" - ->> [PONG]
```

> 🇬🇧 *If you had created a subscriber, you should notice output on the subscriber telling you that it disconnected, and reconnected. The server output above is more interesting. You can see the subscriber send a `CONNECT` protocol message and a `PING` which was responded to by the server with a `PONG`.*

Nếu đã tạo subscriber trước đó, bạn sẽ thấy thông báo disconnect rồi reconnect trên cửa sổ subscriber. Output của server lúc này thú vị hơn — bạn có thể thấy subscriber gửi protocol message `CONNECT` và `PING`, và server phản hồi lại bằng `PONG`.

> You can learn more about the [NATS protocol here](../reference-protocols.md), but more interesting than the protocol description is [an interactive demo](../reference/nats-protocol/nats-protocol-demo.md).

> Tìm hiểu thêm về [NATS protocol tại đây](../reference-protocols.md), nhưng thú vị hơn phần mô tả protocol là [bản demo tương tác](../reference/nats-protocol/nats-protocol-demo.md).

> 🇬🇧 *On a third terminal, publish your first message:*

Trên terminal thứ ba, publish message đầu tiên:

```shell
nats pub hello world -s nats://0.0.0.0:4222
```

> 🇬🇧 *On the subscriber window you should see:*

Trên cửa sổ subscriber, bạn sẽ thấy:

```
[#1] Received on "hello"
world
```

## Kiểm thử với Server từ xa

> 🇬🇧 *If the NATS server were running in a different machine or a different port, you'd have to specify that to the client by specifying a _NATS URL_ (either in a `nats context` or using the `-s` flag).*

Nếu NATS server chạy trên máy khác hoặc port khác, bạn cần truyền thông tin đó cho client bằng cách chỉ định _NATS URL_ (trong `nats context` hoặc dùng flag `-s`).

### NATS URLs

> 🇬🇧 *NATS URLs take the form of: `nats://<server>:<port>` and `tls://<server>:<port>`. URLs with a `tls` protocol sport a secured TLS connection.*

NATS URL có dạng: `nats://<server>:<port>` và `tls://<server>:<port>`. URL với protocol `tls` sử dụng kết nối TLS (mã hóa TLS) bảo mật.

> 🇬🇧 *If you are connecting to a cluster you can specify more than one URL (comma separated). e.g. `nats://localhost:4222,nats://localhost:5222,nats://localhost:6222` if you are running a test cluster of 3 nats servers on your local machine, listening at ports 4222, 5222, and 6222 respectively.*

Khi kết nối đến một cluster, có thể chỉ định nhiều URL ngăn cách bằng dấu phẩy. Ví dụ: `nats://localhost:4222,nats://localhost:5222,nats://localhost:6222` nếu bạn chạy test cluster gồm 3 nats-server trên máy local, lắng nghe lần lượt tại port 4222, 5222 và 6222.

### Ví dụ

```shell
nats sub -s nats://server:port ">"
```

> 🇬🇧 *If you want to try on a remote server, the NATS team maintains a demo server you can reach at `demo.nats.io`.*

Để thử nghiệm với server từ xa, đội ngũ NATS duy trì một demo server tại `demo.nats.io`.

```shell
nats sub -s nats://demo.nats.io ">"
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **cluster**: cụm nhiều server chạy chung
- **credential**: thông tin đăng nhập
- **message**: gói dữ liệu được gửi đi
- **port**: cổng kết nối
- **request**: yêu cầu
- **server**: máy chủ
- **subscriber**: bên đăng ký nhận message
- **TLS**: mã hóa TLS