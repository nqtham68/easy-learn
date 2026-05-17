---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/what-is-nats
title: NATS là gì
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# NATS là gì

> 🇬🇧 *Software applications and services need to exchange data. NATS is an infrastructure that allows such data exchange, segmented in the form of messages. We call this a "**message oriented middleware**".*

Các ứng dụng và service cần trao đổi dữ liệu với nhau. NATS là hạ tầng cho phép trao đổi dữ liệu đó, được phân tách dưới dạng message (gói dữ liệu được gửi đi). Chúng ta gọi đây là "**message oriented middleware** (tầng trung gian)".

> 🇬🇧 *With NATS, application developers can:*
>
> *- Effortlessly build distributed and scalable client-server applications.*
> *- Store and distribute data in realtime in a general manner. This can flexibly be achieved across various environments, languages, cloud providers and on-premises systems.*

Với NATS, developer có thể:

* Xây dựng ứng dụng client-server phân tán và có khả năng mở rộng một cách dễ dàng.
* Lưu trữ và phân phối dữ liệu theo thời gian thực. Điều này có thể thực hiện linh hoạt trên nhiều môi trường, ngôn ngữ, cloud provider và hệ thống on-premises khác nhau.

### Ứng dụng NATS Client

> 🇬🇧 *Developers use one of the NATS client libraries in their application code to allow them to publish, subscribe, request and reply between instances of the application or between completely separate applications. Those applications are generally referred to as 'client applications' or sometimes just as 'clients' throughout this manual (since from the point of view of the NATS server, they are clients).*

Developer sử dụng một trong các NATS client library trong code của mình để publish, subscribe, request và reply giữa các instance của ứng dụng hoặc giữa các ứng dụng hoàn toàn khác nhau. Các ứng dụng này thường được gọi là 'client application' hoặc đơn giản là 'client' trong tài liệu này (vì từ góc độ của NATS server, chúng là client).

### Hạ tầng dịch vụ NATS

> 🇬🇧 *The NATS services are provided by one or more NATS server processes that are configured to interconnect with each other and provide a _NATS service infrastructure_. The NATS service infrastructure can scale from a single NATS server process running on an end device (the `nats-server` process is less than 20 MB in size!) all the way to a public global super-cluster of many clusters spanning all major cloud providers and all regions of the world such as Synadia's NGS.*

Dịch vụ NATS được cung cấp bởi một hoặc nhiều NATS server process được cấu hình để kết nối với nhau, tạo thành _NATS service infrastructure_. Hạ tầng này có thể scale từ một NATS server process đơn lẻ chạy trên thiết bị đầu cuối (tiến trình `nats-server` có kích thước dưới 20 MB!) cho đến một super-cluster toàn cầu gồm nhiều cluster trải rộng trên tất cả các cloud provider lớn và mọi khu vực trên thế giới, như Synadia's NGS.

### Kết nối NATS Client với NATS Server

> 🇬🇧 *To connect a NATS client application with a NATS service, and then subscribe or publish messages to subjects, it only needs to be configured with:*
>
> *1. **URL:** A ['NATS URL'](../../using-nats/developing-with-nats/connecting#nats-url). This is a string (in a URL format) that specifies the IP address and port where the NATS server(s) can be reached, and what kind of connection to establish (plain TCP, TLS, or Websocket).*
> *2. **Authentication** (if needed): [Authentication](../../using-nats/developing-with-nats/connecting#authentication-details) details for the application to identify itself with the NATS server(s). NATS supports multiple authentication schemes (username/password, decentralized JWT, token, TLS certificates and Nkey with challenge).*

Để kết nối NATS client application với dịch vụ NATS, sau đó subscribe hoặc publish message lên các subject (chuỗi định danh message), chỉ cần cấu hình:

1. **URL:** Một ['NATS URL'](../../using-nats/developing-with-nats/connecting#nats-url). Đây là chuỗi theo định dạng URL chỉ định địa chỉ IP và port để kết nối đến NATS server, cùng loại kết nối cần thiết lập (TCP thuần, TLS, hoặc WebSocket).
2. **Authentication** (nếu cần): Thông tin [Authentication](../../using-nats/developing-with-nats/connecting#authentication-details) để ứng dụng xác thực với NATS server. NATS hỗ trợ nhiều scheme xác thực (username/password, decentralized JWT, token, TLS certificate và Nkey with challenge).

## Thiết kế messaging đơn giản

> 🇬🇧 *NATS makes it easy for applications to communicate by sending and receiving messages. These messages are addressed and identified by subject strings, and do not depend on network location.*

NATS giúp các ứng dụng giao tiếp dễ dàng thông qua việc gửi và nhận message. Mỗi message được định địa chỉ và nhận dạng bằng chuỗi subject, không phụ thuộc vào vị trí mạng.

> 🇬🇧 *Data is encoded and framed as a message and sent by a publisher. The message is received, decoded, and processed by one or more subscribers.*

Dữ liệu được encode và đóng gói thành message rồi gửi đi bởi publisher (bên gửi message). Message sau đó được nhận, decode và xử lý bởi một hoặc nhiều subscriber (bên đăng ký nhận message).

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/intro.svg)

> 🇬🇧 *With this simple design, NATS lets programs share common message-handling code, isolate resources and interdependencies, and scale by easily handling an increase in message volume, whether those are service requests or stream data.*

Với thiết kế đơn giản này, NATS cho phép các chương trình dùng chung code xử lý message, tách biệt tài nguyên và phụ thuộc, đồng thời scale dễ dàng khi lượng message tăng lên, dù là service request hay dữ liệu stream (luồng message lưu trữ liên tục).

### Chất lượng dịch vụ NATS (QoS)

> 🇬🇧 *NATS offers multiple qualities of service, depending on whether the application uses just the _Core NATS_ functionality or also leverages the added functionalities enabled by _NATS JetStream_ (JetStream is built into `nats-server` but may not be enabled on all service infrastructures).*

NATS cung cấp nhiều mức chất lượng dịch vụ, tùy thuộc vào việc ứng dụng chỉ dùng chức năng _Core NATS_ hay cũng tận dụng các tính năng bổ sung của _NATS JetStream_ (JetStream được tích hợp sẵn trong `nats-server` nhưng có thể không được bật trên mọi hạ tầng dịch vụ).

> 🇬🇧 *- **At most once QoS:** _Core NATS_ offers an **at most once** quality of service. If a subscriber is not listening on the subject (no subject match), or is not active when the message is sent, the message is not received. This is the same level of guarantee that TCP/IP provides. _Core NATS_ is a fire-and-forget messaging system. It will only hold messages in memory and will never write messages directly to disk.*
> *- **At-least / exactly once QoS:** If you need higher qualities of service (**at least once** and **exactly once**), or functionalities such as persistent streaming, de-coupled flow control, and Key/Value Store, you can use [NATS JetStream](../jetstream), which is built in to the NATS server (but needs to be enabled). Of course, you can also always build additional reliability into your client applications yourself with proven and scalable reference designs such as acks and sequence numbers.*

* **At most once QoS:** _Core NATS_ cung cấp mức chất lượng **at most once**. Nếu subscriber không lắng nghe trên subject đó (không khớp subject), hoặc không hoạt động khi message được gửi, message sẽ không được nhận. Đây là mức đảm bảo tương đương TCP/IP. _Core NATS_ là hệ thống fire-and-forget — chỉ giữ message trong bộ nhớ và không bao giờ ghi trực tiếp ra đĩa.
* **At-least / exactly once QoS:** Nếu cần mức chất lượng cao hơn (**at least once** và **exactly once**), hoặc các tính năng như persistent streaming, de-coupled flow control và Key/Value Store, có thể dùng [NATS JetStream](../jetstream), được tích hợp sẵn trong NATS server (nhưng cần bật lên). Tất nhiên, vẫn có thể tự xây dựng thêm độ tin cậy vào client application bằng các thiết kế tham chiếu đã được kiểm chứng như ack và sequence number.

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **message**: gói dữ liệu được gửi đi
- **middleware**: tầng trung gian
- **publisher**: bên gửi message
- **server**: máy chủ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **token**: chuỗi xác thực