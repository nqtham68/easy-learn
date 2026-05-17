---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/mqtt
title: MQTT
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# MQTT

_Hỗ trợ từ NATS Server phiên bản 2.2_

> 🇬🇧 *NATS follows as closely as possible to the MQTT v3.1.1 [specification](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html). Refer to the [MQTT implementation overview](https://github.com/nats-io/nats-server/blob/main/server/README-MQTT.md) in the nats-server repo.*

NATS tuân thủ sát nhất có thể theo [đặc tả](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html) MQTT v3.1.1. Tham khảo thêm [tổng quan triển khai MQTT](https://github.com/nats-io/nats-server/blob/main/server/README-MQTT.md) trong repo nats-server.

> 🇬🇧 *NATS supports MQTT QoS: 0, 1 and 2*

NATS hỗ trợ MQTT QoS: 0, 1 và 2.

## Khi Nào Nên Dùng MQTT

> 🇬🇧 *MQTT support in NATS is intended to be an enabling technology allowing users to leverage existing investments in their IoT deployments. Updating software on the edge or endpoints can be onerous and risky, especially when embedded applications are involved.*

Hỗ trợ MQTT trong NATS được thiết kế như một công nghệ nền, giúp người dùng tận dụng hạ tầng IoT đã đầu tư. Việc cập nhật phần mềm trên thiết bị đầu cuối hoặc edge thường phức tạp và rủi ro, nhất là với các ứng dụng nhúng.

> 🇬🇧 *In greenfield IoT deployments, when possible, we prefer NATS extended out to endpoints and devices for a few reasons. There are significant advantages with security and observability when using a single technology end to end. Compared to MQTT, NATS is nearly as lightweight in terms of protocol bandwidth and maintainer supported clients efficiently utilize resources so we consider NATS to be a good choice to use end to end, including use on resource constrained devices.*

Với các deploy IoT mới hoàn toàn, chúng tôi ưu tiên mở rộng NATS ra tận thiết bị đầu cuối vì một vài lý do: sử dụng một công nghệ thống nhất từ đầu đến cuối mang lại lợi thế đáng kể về bảo mật và khả năng quan sát. So với MQTT, NATS gần như nhẹ tương đương về băng thông giao thức, và các client được bảo trì chính thức sử dụng tài nguyên hiệu quả — vì vậy NATS là lựa chọn phù hợp cho cả thiết bị bị hạn chế tài nguyên.

> 🇬🇧 *In existing MQTT deployments or in situations when endpoints can only support MQTT, using a NATS server as a drop-in MQTT server replacement to securely connect to a remote NATS cluster or supercluster is compelling. You can keep your existing IoT investment and use NATS for secure, resilient, and scalable access to your streams and services.*

Với hạ tầng MQTT đang có, hoặc khi thiết bị đầu cuối chỉ hỗ trợ MQTT, việc dùng NATS server thay thế trực tiếp cho MQTT server để kết nối an toàn tới một NATS cluster (cụm nhiều server chạy chung) hoặc supercluster là rất hấp dẫn. Bạn giữ nguyên hạ tầng IoT hiện tại và dùng NATS để truy cập an toàn, bền vững, có khả năng mở rộng vào các stream và service.

## Yêu Cầu JetStream

> 🇬🇧 *For an MQTT client to connect to the NATS server, the user's account must be JetStream enabled. This is because persistence is needed for the sessions and retained messages since even retained messages of QoS 0 are persisted.*

Để MQTT client kết nối được với NATS server, tài khoản người dùng phải bật JetStream. Lý do là cần lưu trữ bền vững cho session và retained message — kể cả retained message của QoS 0 cũng được lưu lại.

## MQTT Topic và NATS Subject

> 🇬🇧 *MQTT Topics are similar to NATS Subjects, but have distinctive differences.*

MQTT Topic tương tự NATS Subject (chuỗi định danh message), nhưng có những điểm khác biệt quan trọng.

> 🇬🇧 *MQTT topic uses ``/`` as a level separator. For instance `foo/bar` would translate to NATS subject `foo.bar`. But in MQTT, `/foo/bar/` is a valid subject, which, if simply translated, would become `.foo.bar.`, which is NOT a valid NATS Subject.*

MQTT topic dùng `/` làm ký tự phân cấp. Ví dụ `foo/bar` sẽ được chuyển thành NATS subject `foo.bar`. Tuy nhiên trong MQTT, `/foo/bar/` là subject hợp lệ, nhưng nếu chuyển thẳng sẽ thành `.foo.bar.`, vốn KHÔNG phải NATS Subject hợp lệ.

> 🇬🇧 *NATS Server will convert an MQTT topic following those rules:*

NATS Server chuyển đổi MQTT topic theo các quy tắc sau:

|     Ký tự MQTT     |  Ký tự NATS  | Topic (MQTT) | Subject (NATS) |
| :--------------------: | :-------------------: | :------------: | :--------------: |
| `/` giữa hai cấp |          `.`          |   `foo/bar`    |    `foo.bar`     |
|   `/` ở cấp đầu   |         `/.`          |   `/foo/bar`   |   `/.foo.bar`    |
|   `/` ở cấp cuối    |         `./`          |   `foo/bar/`   |   `foo.bar./`    |
|  `/` kề nhau   |         `./`          |   `foo//bar`   |   `foo./.bar`    |
|  `/` kề nhau   |         `/.`          |  `//foo/bar`   |  `/./.foo.bar`   |
|          `.`           | `//` (xem ghi chú bên dưới) |   `foo.bar`    |    `foo//bar`    |
|          ` `           |     Không hỗ trợ     |   `foo bar`    |  Không hỗ trợ   |

_Ghi chú: Trước NATS Server v2.10.0, ký tự `.` không được hỗ trợ. Từ v2.10.0 trở lên, ký tự `.` sẽ được chuyển thành `//`._

> 🇬🇧 *As indicated above, if an MQTT topic contains the character ` ` (or `.` prior to v2.10.0), NATS will reject it, causing the connection to be closed for published messages, and returning a failure code in the SUBACK packet for a subscriptions.*

Như đã nêu, nếu MQTT topic chứa ký tự ` ` (hoặc `.` trước v2.10.0), NATS sẽ từ chối — đóng kết nối với các message publish, và trả về mã lỗi trong gói SUBACK với các subscription.

### MQTT Wildcards

> 🇬🇧 *As in NATS, MQTT wildcards represent either multi or single levels. As in NATS, they are allowed only for subscriptions, not for published messages.*

Giống NATS, MQTT wildcard đại diện cho nhiều hoặc một cấp. Cũng giống NATS, chúng chỉ được dùng trong subscription, không dùng khi publish message.

| MQTT Wildcard | NATS Wildcard |
| :-----------: | :-----------: |
|      `#`      |      `>`      |
|      `+`      |      `*`      |

> 🇬🇧 *The wildcard `#` matches any number of levels within a topic, which means that a subscription on `foo/#` would receive messages on `foo/bar`, or `foo/bar/baz`, but also on `foo`. This is not the case in NATS where a subscription on `foo.>` can receive messages on `foo/bar` or `foo/bar/baz`, but not on `foo`. To solve this, NATS Server will create two subscriptions, one on `foo.>` and one on `foo`. If the MQTT subscription is simply on `#`, then a single NATS subscription on `>` is enough.*

Wildcard `#` khớp với bất kỳ số cấp nào trong topic, nghĩa là subscription trên `foo/#` sẽ nhận message từ `foo/bar`, `foo/bar/baz`, và cả `foo`. Trong NATS thì khác: subscription trên `foo.>` chỉ nhận được message từ `foo/bar` hoặc `foo/bar/baz`, không nhận `foo`. Để giải quyết, NATS Server tạo hai subscription: một trên `foo.>` và một trên `foo`. Nếu MQTT subscription chỉ là `#`, một NATS subscription duy nhất trên `>` là đủ.

> 🇬🇧 *The wildcard `+` matches a single level, which means `foo/+` can receive message on `foo/bar` or `foo/baz`, but not on `foo/bar/baz` nor `foo`. This is the same with NATS subscriptions using the wildcard `*`. Therefore `foo/+` would translate to `foo.*`.*

Wildcard `+` khớp với một cấp duy nhất, tức `foo/+` nhận được message từ `foo/bar` hoặc `foo/baz`, nhưng không nhận `foo/bar/baz` hay `foo`. Điều này giống hệt NATS subscription dùng wildcard `*`. Do đó `foo/+` sẽ được chuyển thành `foo.*`.

## Giao Tiếp Giữa MQTT và NATS

> 🇬🇧 *When an MQTT client creates a subscription on a topic, the NATS server creates the similar NATS subscription \(with conversion from MQTT topic to NATS subject\) so that the interest is registered in the cluster and known to any NATS publishers.*

Khi MQTT client tạo subscription trên một topic, NATS server tạo NATS subscription tương ứng (sau khi chuyển đổi MQTT topic sang NATS subject) để interest được đăng ký trong cluster và mọi NATS publisher (bên gửi message) đều biết đến.

> 🇬🇧 *That is, say an MQTT client connects to server "A" and creates a subscription of `foo/bar`, server "A" creates a subscription on `foo.bar`, which interest is propagated as any other NATS subscription. A publisher connecting anywhere in the cluster and publishing on `foo.bar` would cause server "A" to deliver a QoS 0 message to the MQTT subscription.*

Ví dụ: MQTT client kết nối tới server "A" và tạo subscription trên `foo/bar`, server "A" tạo subscription trên `foo.bar` và propagate interest này như bất kỳ NATS subscription nào khác. Một publisher kết nối tại bất kỳ đâu trong cluster và publish lên `foo.bar` sẽ khiến server "A" giao QoS 0 message tới MQTT subscription đó.

> 🇬🇧 *This works the same way for MQTT publishers. When the server receives an MQTT publish message, it is converted to the NATS subject and published, which means that any matching NATS subscription will receive the MQTT message.*

Chiều ngược lại cũng tương tự: khi server nhận MQTT publish message, message được chuyển sang NATS subject và publish — mọi NATS subscriber (bên đăng ký nhận message) khớp subject đều nhận được MQTT message đó.

> 🇬🇧 *If the MQTT subscription is QoS1 and an MQTT publisher publishes an MQTT QoS1 message on the same or any other server in the cluster, the message will be persisted in the cluster and routed and delivered as QoS 1 to the MQTT subscription.*

Nếu MQTT subscription là QoS 1 và MQTT publisher publish QoS 1 message lên cùng server hoặc bất kỳ server nào khác trong cluster, message sẽ được lưu trữ, định tuyến và giao đến MQTT subscription với QoS 1.

## Re-delivery cho QoS 1 và 2

> 🇬🇧 *When the server delivers a QoS 1 or 2 message to a QoS 1 or 2 subscription, it will keep the message until it receives the PUBACK for the corresponding packet identifier. If it does not receive it within the "ack_wait" interval, that message will be resent.*

Khi server giao QoS 1 hoặc 2 message tới subscription QoS 1 hoặc 2, server giữ message cho đến khi nhận được PUBACK cho packet identifier tương ứng. Nếu không nhận được trong khoảng thời gian `ack_wait`, message sẽ được gửi lại.

## Max Ack Pending

> 🇬🇧 *This is the amount of QoS 1 or 2 messages the server can send to a subscription without receiving any PUBACK for those messages. The maximum value is 65535.*

Đây là số lượng QoS 1 hoặc 2 message mà server có thể gửi tới một subscription mà chưa nhận PUBACK nào. Giá trị tối đa là 65535.

> 🇬🇧 *The total of subscriptions' `max_ack_pending` on a given session cannot exceed 65535. Attempting to create a subscription that would bring the total above the limit would result in the server returning a failure code in the SUBACK for this subscription.*

Tổng `max_ack_pending` của tất cả subscription trong một session không được vượt quá 65535. Nếu tạo subscription mới khiến tổng vượt giới hạn, server sẽ trả về mã lỗi trong SUBACK cho subscription đó.

> 🇬🇧 *Due to how the NATS server handles the MQTT "`#`" wildcard, each subscription ending with "`#`" will use 2 times the `max_ack_pending` value.*

Do cách NATS server xử lý MQTT wildcard "`#`", mỗi subscription kết thúc bằng "`#`" sẽ dùng 2 lần giá trị `max_ack_pending`.

## Session

> 🇬🇧 *NATS Server will persist all sessions, even if they are created with the "clean session" flag, meaning that sessions only last for the duration of the network connection between the client and the server.*

NATS Server lưu trữ tất cả session, kể cả session được tạo với flag "clean session" — tức session chỉ tồn tại trong suốt thời gian kết nối mạng giữa client và server.

> 🇬🇧 *A session is identified by a client identifier. If two connections try to use the same client identifier, the server, per specification, will close the existing connection and accept the new one.*

Session được định danh bằng client identifier. Nếu hai kết nối dùng cùng client identifier, server sẽ theo đặc tả đóng kết nối cũ và chấp nhận kết nối mới.

> 🇬🇧 *If the user incorrectly starts two applications that use the same client identifier, this would result in a very quick flapping if the MQTT client has a reconnect feature and quickly reconnects.*

Nếu người dùng vô tình khởi động hai ứng dụng dùng cùng client identifier, tình trạng flapping rất nhanh có thể xảy ra nếu MQTT client có tính năng reconnect.

> 🇬🇧 *To prevent this, the NATS server will accept the new session and will delay the closing of the old connection to reduce the flapping rate.*

Để tránh điều này, NATS server chấp nhận session mới nhưng trì hoãn việc đóng kết nối cũ nhằm giảm tốc độ flapping.

> 🇬🇧 *Detection of the concurrent use of sessions also works in cluster mode.*

Phát hiện session bị dùng đồng thời cũng hoạt động trong chế độ cluster.

## Retained Message

> 🇬🇧 *When a server receives an MQTT publish packet with the RETAIN flag set \(regardless of its QoS\), it stores the application message and its QoS, so that it can be delivered to future subscribers whose subscriptions match its topic name.*

Khi server nhận MQTT publish packet có RETAIN flag (bất kể QoS), server lưu lại message và QoS của nó để giao cho các subscriber sau này có subscription khớp topic name.

> 🇬🇧 *When a new subscription is established, the last retained message, if any, on each matching topic name will be sent to the subscriber.*

Khi subscription mới được thiết lập, retained message cuối cùng (nếu có) trên từng topic name khớp sẽ được gửi tới subscriber.

> 🇬🇧 *A PUBLISH Packet with a RETAIN flag set to 1 and a payload containing zero bytes will be processed as normal and sent to clients with a subscription matching the topic name. Additionally any existing retained message with the same topic name will be removed and any future subscribers for the topic will not receive a retained message.*

PUBLISH Packet có RETAIN flag = 1 và payload rỗng (0 byte) sẽ được xử lý bình thường và gửi tới client có subscription khớp topic name. Ngoài ra, mọi retained message hiện có với cùng topic name sẽ bị xóa, và các subscriber tương lai sẽ không nhận được retained message nữa.

## Clustering

> 🇬🇧 *NATS supports MQTT in a NATS cluster. The replication factor is automatically set based on the size of the cluster.*

NATS hỗ trợ MQTT trong NATS cluster. Replication factor được tự động thiết lập dựa trên kích thước cluster.

### Kết Nối Với Cùng Client ID

> 🇬🇧 *If a client is connected to a server "A" in the cluster and another client connects to a server "B" and uses the same client identifier, server "A" will close its client connection upon discovering the use of an active client identifier.*

Nếu một client đang kết nối tới server "A" trong cluster và client khác kết nối tới server "B" với cùng client identifier, server "A" sẽ đóng kết nối của mình khi phát hiện client identifier đó đang hoạt động.

> 🇬🇧 *Users should avoid this situation as this is not as easy and immediate as if the two applications are connected to the same server.*

Người dùng nên tránh tình huống này vì xử lý sẽ không nhanh và trực tiếp như khi cả hai ứng dụng cùng kết nối tới một server.

> 🇬🇧 *There may be cases where the server will reject the new connection if there is no safe way to close the existing connection, such as when it is in the middle of processing some MQTT packets.*

Có thể xảy ra trường hợp server từ chối kết nối mới nếu không có cách an toàn để đóng kết nối hiện tại, chẳng hạn khi server đang xử lý một số MQTT packet.

### Retained Message

> 🇬🇧 *Retained messages are stored in the cluster and available to any server in the cluster. However, this is not immediate and if a producer connects to a server and produces a retained message and another connection connects to another server and starts a matching subscription, it may not receive the retained message if the server it connects to has not yet been made aware of this retained message.*

Retained message được lưu trong cluster và mọi server trong cluster đều có thể truy cập. Tuy nhiên, việc này không tức thời: nếu một producer (bên tạo dữ liệu cho stream) kết nối tới một server và tạo retained message, trong khi một kết nối khác tới server khác tạo subscription khớp, kết nối đó có thể không nhận được retained message nếu server đó chưa được thông báo.

> 🇬🇧 *In other words, retained messages in clustering mode is best-effort, and applications that rely on the presence of a retained message should connect on the server that produced them.*

Nói cách khác, retained message trong chế độ cluster là best-effort. Các ứng dụng phụ thuộc vào retained message nên kết nối tới server đã tạo ra chúng.

## Giới Hạn

> 🇬🇧 *- NATS messages published to MQTT subscriptions are always delivered as QoS 0 messages.*
> *- MQTT published messages on topic names containing "````" or "`.\`" characters will cause the connection to be closed. Presence of those characters in MQTT subscriptions will result in error code in the SUBACK packet.*
> *- MQTT wildcard `#` may cause the NATS server to create two subscriptions.*
> *- MQTT concurrent sessions may result in the new connection to be evicted instead of the existing one.*
> *- MQTT retained messages in clustering mode is best effort.*

- NATS message được publish tới MQTT subscription luôn được giao dưới dạng QoS 0.
- MQTT message publish trên topic name chứa ký tự "````" or "`.\`" sẽ khiến kết nối bị đóng. Các ký tự đó trong MQTT subscription sẽ trả về mã lỗi trong gói SUBACK.
- MQTT wildcard `#` có thể khiến NATS server tạo hai subscription.
- MQTT session đồng thời có thể dẫn đến việc kết nối mới bị evict thay vì kết nối cũ.
- Retained message của MQTT trong chế độ cluster là best-effort.

## Xem Thêm

[Thay thế MQTT Broker của bạn bằng NATS Server](https://nats.io/blog/replace-your-mqtt-broker-with-nats/)

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **producer**: bên tạo dữ liệu cho stream
- **publisher**: bên gửi message
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **subscription**: đăng ký nhận message