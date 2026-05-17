---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/release_notes/whats_new_22
title: Điểm mới trong NATS 2.2
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# NATS 2.2

> 🇬🇧 *NATS 2.2 is the largest feature release since version 2.0. The 2.2 release provides highly scalable, highly performant, secure and easy-to-use next generation streaming in the form of JetStream, allows remote access via websockets, has simplified NATS account management, native MQTT support, and further enables NATS toward our goal of securely democratizing streams and services for the hyperconnected world we live in.*

NATS 2.2 là bản phát hành tính năng lớn nhất kể từ phiên bản 2.0. Phiên bản này mang đến JetStream — nền tảng streaming (luồng message lưu trữ liên tục) thế hệ mới với khả năng mở rộng cao, hiệu suất mạnh và dễ sử dụng — cùng khả năng truy cập từ xa qua WebSocket, quản lý tài khoản đơn giản hơn, hỗ trợ MQTT gốc, và tiếp tục hiện thực hóa mục tiêu dân chủ hóa stream và service một cách an toàn cho thế giới siêu kết nối.

## Streaming Thế Hệ Mới

> 🇬🇧 *JetStream is the next generation streaming platform for NATS, highly resilient, highly available, and easy to use. We've spent a long time listening to our community, learning from our experiences, looking at the needs of today, and thinking deeply about the needs of tomorrow. We built JetStream to address these needs.*

JetStream là nền tảng streaming thế hệ mới của NATS, có khả năng chịu lỗi cao, sẵn sàng cao và dễ sử dụng. Chúng tôi đã dành nhiều thời gian lắng nghe cộng đồng, rút kinh nghiệm từ thực tế, phân tích nhu cầu hiện tại và tương lai để xây dựng JetStream giải quyết tất cả những nhu cầu đó.

> 🇬🇧 *JetStream:*
> - *is easy to deploy and manage, built into the NATS server*
> - *simplifies and accelerates development*
> - *supports wildcard subjects*
> - *supports at least once delivery and exactly once within a window*
> - *is horizontally scalable at runtime with no interruptions*
> - *persists data via streams and delivers or replays via consumers*
> - *supports multiple patterns to consume data on the same stream*
> - *supports push and pull modes when consuming messages*
> - *is account aware*
> - *allows for detailed granularity of security, by stream, by consumer, by function*

JetStream:

* Dễ deploy và quản lý, tích hợp sẵn vào NATS server
* Đơn giản hóa và tăng tốc quá trình phát triển
* Hỗ trợ wildcard subject (chuỗi định danh message)
* Hỗ trợ at-least-once delivery và exactly-once trong một cửa sổ thời gian
* Mở rộng theo chiều ngang tại runtime mà không cần gián đoạn
* Lưu trữ dữ liệu qua stream và phân phối hoặc phát lại qua consumer (bên xử lý dữ liệu từ stream)
* Hỗ trợ nhiều pattern để consume dữ liệu trên cùng một stream
* Hỗ trợ cả push và pull mode khi consuming message
* Nhận biết account
* Cho phép phân quyền bảo mật chi tiết theo stream, theo consumer, theo function

Tìm hiểu thêm tại [JetStream](../nats-concepts/jetstream).

## Bảo Mật và Quản Lý Tài Khoản Đơn Giản Hóa

> 🇬🇧 *Account management just became much easier. This version of NATS has a built-in account management system, eliminating the need to set up an account manager when not using the memory account resolver. With automated default system account generation, and the ability to preload accounts, simply enable a set of servers in your deployment to be account resolvers or account resolver caches, and they will handle public account information provided to the NATS system through the NATS nsc tooling. Have enterprise-scale account management up and running in minutes.*

Quản lý tài khoản đã trở nên dễ dàng hơn nhiều. Phiên bản này tích hợp sẵn hệ thống quản lý tài khoản, loại bỏ nhu cầu cài đặt account manager khi không dùng memory account resolver. Với tính năng tự động tạo system account mặc định và khả năng preload tài khoản, chỉ cần cho phép một tập server trong deployment đóng vai trò account resolver hoặc account resolver cache — chúng sẽ tự xử lý thông tin tài khoản công khai được cung cấp qua công cụ `nsc`. Có thể thiết lập quản lý tài khoản quy mô enterprise chỉ trong vài phút.

### Giới Hạn Tài Khoản Theo Dải CIDR

> 🇬🇧 *By specifying a CIDR block restriction for a user, policy can be applied to limit connections from clients within a certain range or set of IP addresses. Use this as another layer of security atop user credentials to better secure your distributed system. Ensure your applications can only connect from within a specific cloud, enterprise, geographic location, virtual or physical network.*

Khi chỉ định dải CIDR cho một user, có thể áp dụng policy giới hạn kết nối từ client trong một phạm vi hoặc tập hợp địa chỉ IP nhất định. Đây là lớp bảo mật bổ sung chồng lên credential (thông tin đăng nhập) người dùng, giúp đảm bảo ứng dụng chỉ có thể kết nối từ một cloud, tổ chức, vị trí địa lý, hoặc mạng vật lý/ảo cụ thể.

### Giới Hạn Tài Khoản Theo Thời Gian

> 🇬🇧 *Scoped to the user, you can now [specify a specific block of time](../using-nats/nats-tools/nsc/basics.md#user-authorization) during the day when applications can connect. For example, permit certain users or applications to access the system during specified business hours, or protect business operations during the busiest parts of the day from batch driven back-office applications that could adversely impact the system when run at the wrong time.*

Ở phạm vi người dùng, giờ có thể [chỉ định khung giờ cụ thể](../using-nats/nats-tools/nsc/basics.md#user-authorization) trong ngày mà ứng dụng được phép kết nối. Ví dụ: cho phép một số user hoặc ứng dụng truy cập hệ thống trong giờ hành chính, hoặc bảo vệ hoạt động kinh doanh trong giờ cao điểm khỏi các ứng dụng back-office chạy batch có thể ảnh hưởng tiêu cực đến hệ thống nếu chạy sai thời điểm.

### Quyền Mặc Định Cho User

> 🇬🇧 *Now you can specify [default user permissions](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/authorization#examples) within an account. This significantly reduces efforts around policy, reduces chances for error in permissioning, and simplifies the provisioning of user credentials.*

Giờ có thể chỉ định [permission (quyền truy cập) mặc định cho user](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/authorization#examples) trong một account. Điều này giảm đáng kể công sức quản lý policy, hạn chế lỗi khi phân quyền và đơn giản hóa việc cấp phát credential cho người dùng.

## WebSockets

> 🇬🇧 *Connect mobile and web applications to any NATS server using [WebSockets](../running-a-nats-service/configuration/websocket). Built to more easily traverse firewalls and load balancers, NATS WebSocket support provides even more flexibility to NATS deployments and makes it easier to communicate to the edge and endpoints. This is currently supported in NATS server leaf nodes, nats.ts, nats.deno, and the nats.js clients.*

Kết nối ứng dụng mobile và web tới bất kỳ NATS server nào bằng [WebSockets](../running-a-nats-service/configuration/websocket). Được thiết kế để vượt qua firewall và load balancer dễ dàng hơn, hỗ trợ WebSocket mang lại thêm tính linh hoạt cho các deployment NATS và giúp kết nối tới edge và endpoint thuận tiện hơn. Hiện đã được hỗ trợ trong NATS server leaf nodes, nats.ts, nats.deno và các client nats.js.

## Hỗ Trợ MQTT Gốc

> 🇬🇧 *With the [Adaptive Edge architecture](https://nats.io/blog/synadia-adaptive-edge/) and the ease with which NATS can extend a cloud deployment to the edge, it makes perfect sense to leverage existing investments in IoT deployments. It's expensive to update devices and large edge deployments. Our goal is to enable the hyperconnected world, so we added first-class support for [MQTT 3.1.1](../running-a-nats-service/configuration/mqtt) directly into the NATS Server.*

Với [kiến trúc Adaptive Edge](https://nats.io/blog/synadia-adaptive-edge/) và khả năng mở rộng deployment cloud ra edge một cách dễ dàng của NATS, việc tận dụng các đầu tư IoT hiện có là hoàn toàn hợp lý. Việc cập nhật thiết bị và các deployment edge quy mô lớn rất tốn kém, do đó chúng tôi đã tích hợp hỗ trợ hạng nhất cho [MQTT 3.1.1](../running-a-nats-service/configuration/mqtt) trực tiếp vào NATS Server.

> 🇬🇧 *Seamlessly integrate existing IoT deployments using MQTT 3.1.1 with a cloud-native NATS deployment. Add a leaf node that is MQTT enabled and instantly send and receive messages to your MQTT applications and devices from a NATS deployment whether it be edge, single-cloud, multi-cloud, on-premise, or any combination thereof.*

Tích hợp liền mạch các IoT deployment hiện có sử dụng MQTT 3.1.1 với deployment NATS cloud-native. Thêm một leaf node hỗ trợ MQTT để ngay lập tức gửi và nhận message tới ứng dụng và thiết bị MQTT từ bất kỳ deployment NATS nào — dù là edge, single-cloud, multi-cloud, on-premise hay kết hợp tùy ý.

## Xây Dựng Hệ Thống Tốt Hơn

> 🇬🇧 *We've added a variety of features to allow you to build a more resilient, secure, and simply better system at scale.*

Chúng tôi đã bổ sung nhiều tính năng giúp xây dựng hệ thống có khả năng chịu lỗi tốt hơn, bảo mật hơn và đơn giản là tốt hơn ở quy mô lớn.

### Message Headers

> 🇬🇧 *We've added the ability to optionally use headers, following the HTTP semantics familiar to developers. Headers naturally apply overhead, which was why we resisted adding them for so long. By creating new internal protocol messages transparent to developers, we maintain the extremely fast processing of simple NATS messages that we have always had while supporting headers for those who would like to leverage them. Adding headers to messages allows you to provide application-specific metadata, such as compression or encryption-related information, without touching the payload. We also provide some NATS specific headers for use in JetStream and other features.*

Chúng tôi đã bổ sung khả năng sử dụng header tùy chọn, tuân theo ngữ nghĩa HTTP quen thuộc với developer. Header vốn mang lại overhead, đó là lý do chúng tôi trì hoãn việc thêm tính năng này. Bằng cách tạo các protocol message nội bộ mới trong suốt với developer, chúng tôi vẫn duy trì tốc độ xử lý cực nhanh của NATS message đơn giản như trước đây, đồng thời hỗ trợ header cho những ai muốn tận dụng. Thêm header vào message cho phép cung cấp metadata của ứng dụng — như thông tin nén hoặc mã hóa — mà không ảnh hưởng đến payload (nội dung chính của message). Chúng tôi cũng cung cấp một số header đặc thù của NATS để dùng trong JetStream và các tính năng khác.

### Bảo Trì Liền Mạch Với Lame Duck Notifications

> 🇬🇧 *When taking down a server for maintenance, servers can be signaled to enter [Lame Duck Mode](https://docs.nats.io/running-a-nats-service/nats\_admin/lame\_duck\_mode) where they do not accept new connections and evict existing connections over a period of time. Maintainer supported clients will notify applications that a server has entered this state and will be shutting down, allowing a client to smoothly transition to another server or cluster and better maintain business continuity during scheduled maintenance periods.*

Khi đưa server xuống để bảo trì, server có thể được báo hiệu vào [Lame Duck Mode](https://docs.nats.io/running-a-nats-service/nats\_admin/lame\_duck\_mode) — chế độ không nhận kết nối mới và dần trục xuất các kết nối hiện tại theo thời gian. Các client được hỗ trợ bởi maintainer sẽ thông báo cho ứng dụng khi server vào trạng thái này và sắp tắt, cho phép client chuyển sang server hoặc cluster khác một cách trơn tru, duy trì tính liên tục của hoạt động kinh doanh trong các đợt bảo trì theo lịch.

### Phản Ứng Nhanh Hơn Với No-Responder Notifications

> 🇬🇧 *Why wait for timeouts when services aren't available? When a request is made to a service (request-reply) and the NATS Server knows there are no services available the server will short circuit the request. A "no-responders" protocol message will be sent back to the requesting client which will break from blocking API calls. This allows applications to immediately react which further enables building a highly responsive system at scale, even in the face of application failures and network partitions.*

Tại sao phải chờ timeout khi service không khả dụng? Khi một request được gửi đến service (request-reply) mà NATS Server biết không có service nào sẵn sàng, server sẽ short-circuit request đó ngay lập tức. Một protocol message "no-responders" sẽ được gửi lại cho client đang yêu cầu, phá vỡ các blocking API call. Điều này cho phép ứng dụng phản ứng ngay lập tức, tạo điều kiện xây dựng hệ thống phản hồi cao ở quy mô lớn, kể cả khi ứng dụng gặp lỗi hay mạng bị phân vùng.

### Subject Mapping và Traffic Shaping

> 🇬🇧 *Reduce risk when onboarding new services. Canary deployments, A/B testing, and transparent teeing of data streams are now fully supported in NATS. The NATS Server allows accounts to form subject mappings from one subject to another for both client inbound and service import invocations and allows weighted sets for the destinations. Map any percentage - 1 to 100 percent of your traffic - to other subjects, and change this at runtime with a server configuration reload. You can even artificially drop a percentage of traffic to introduce chaos testing into your system. See [Configuring Subject Mapping and Traffic Shaping](https://docs.nats.io/running-a-nats-service/configuration/configuring\_subject\_mapping) in NATS Server configuration for more details.*

Giảm rủi ro khi đưa service mới vào vận hành. Canary deployment, A/B testing và transparent teeing của data stream hiện đã được NATS hỗ trợ đầy đủ. NATS Server cho phép account tạo subject mapping từ subject này sang subject khác cho cả lưu lượng client inbound và service import, đồng thời hỗ trợ weighted set cho destination. Map bất kỳ tỷ lệ phần trăm nào — từ 1 đến 100 phần trăm traffic — tới các subject khác, và thay đổi điều này tại runtime bằng cách reload cấu hình server. Có thể cố tình drop một tỷ lệ traffic để đưa chaos testing vào hệ thống. Xem [Configuring Subject Mapping and Traffic Shaping](https://docs.nats.io/running-a-nats-service/configuration/configuring\_subject\_mapping) để biết thêm chi tiết.

### Account Monitoring - Metric Có Ý Nghĩa Hơn

> 🇬🇧 *NATS now allows for [fine-grained monitoring](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#monitoring-nats) to identify usage metrics tied to a particular account. Inspect messages and bytes sent or received and various connection statistics for a particular account. Accounts can represent anything - a group of applications, a team or organization, a geographic location, or even roles. If NATS is enabling your SaaS solution you could use NATS account scoped metrics to bill users.*

NATS hiện cho phép [giám sát chi tiết](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#monitoring-nats) để xác định metric (số liệu đo lường) sử dụng gắn với từng account cụ thể. Kiểm tra message và bytes đã gửi hoặc nhận cùng các thống kê kết nối cho một account. Account có thể đại diện cho bất kỳ thứ gì — một nhóm ứng dụng, một team hay tổ chức, một vị trí địa lý, hoặc thậm chí các vai trò. Nếu NATS đang hỗ trợ giải pháp SaaS của bạn, có thể dùng metric theo phạm vi account của NATS để tính phí người dùng.

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **credential**: thông tin đăng nhập
- **deploy**: triển khai
- **endpoint**: địa chỉ API cụ thể
- **header**: phần metadata kèm theo
- **message**: gói dữ liệu được gửi đi
- **metric**: số liệu đo lường
- **payload**: nội dung chính của message
- **permission**: quyền truy cập
- **request**: yêu cầu
- **runtime**: môi trường chạy
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **WebSocket**: giao thức WebSocket