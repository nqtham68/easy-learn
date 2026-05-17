---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/subjects
title: Nhắn Tin Dựa Trên Subject
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Nhắn Tin Dựa Trên Subject

> 🇬🇧 *NATS is a system for publishing and listening for messages on named communication channels we call `Subjects`. Fundamentally, NATS is an `interest-based` messaging system, where the listener has to `subscribe` to a subset of `subjects`.*

NATS là hệ thống gửi và lắng nghe message trên các kênh giao tiếp có tên gọi, gọi là subject (chuỗi định danh message). Về bản chất, NATS là hệ thống nhắn tin `interest-based`, trong đó bên lắng nghe phải `subscribe` vào một tập con của `subjects`.

> 🇬🇧 *In other middleware systems subjects may be called `topics`, `channels`, `streams` (Note that in NATS the term `stream` is used for a [JetStream](./jetstream) message storage).*

Trong các hệ thống middleware khác, subject có thể được gọi là `topics`, `channels`, `streams` (lưu ý: trong NATS, thuật ngữ `stream` dùng để chỉ nơi lưu trữ message của [JetStream](./jetstream)).

> 🇬🇧 *At its simplest, a subject is just a string of characters that form a name the publisher and subscriber can use to find each other. More commonly [subject hierarchies](#subject-hierarchies) are used to scope messages into semantic namespaces.*

**Subject là gì?**
Ở dạng đơn giản nhất, subject chỉ là một chuỗi ký tự tạo thành tên để publisher (bên gửi message) và subscriber (bên đăng ký nhận message) tìm thấy nhau. Thông thường, [subject hierarchy](#subject-hierarchies) được dùng để phân nhóm message theo không gian tên có ngữ nghĩa.

> **ℹ️ Info:**
> Please check the [constraint and conventions](#characters-allowed-and-recommended-for-subject-names) on naming for subjects here.

> **ℹ️ Info:**
> Xem các [quy tắc và quy ước đặt tên](#characters-allowed-and-recommended-for-subject-names) cho subject tại đây.

> 🇬🇧 *Through subject-based addressing, NATS provides location transparency across a (large) cloud of routed NATS servers.*

**Location transparency**
Thông qua cơ chế định địa chỉ dựa trên subject, NATS cung cấp tính minh bạch về vị trí trên toàn bộ đám mây server NATS được định tuyến.

> 🇬🇧 *Subject subscriptions are automatically propagated within the server cloud. Messages will be automatically routed to all interested subscribers, independent of location. Messages with no subscribers to their subject are automatically discarded (Please see the [JetStream](./jetstream) feature for message persistence).*

* Subscription theo subject được tự động lan truyền trong đám mây server.
* Message được tự động định tuyến đến tất cả subscriber quan tâm, bất kể vị trí.
* Message không có subscriber nào đăng ký subject tương ứng sẽ bị tự động loại bỏ (xem tính năng [JetStream](./jetstream) để lưu trữ message lâu dài).

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/subjects1.svg)

## Wildcard

> 🇬🇧 *NATS provides two _wildcards_ that can take the place of one or more elements in a dot-separated subject. Publishers will always send a message to a fully specified subject, without the wildcard. While subscribers can use these wildcards to listen to multiple subjects with a single subscription.*

NATS cung cấp hai loại wildcard có thể thay thế một hoặc nhiều phần tử trong subject được phân tách bằng dấu chấm. Publisher (bên gửi message) luôn gửi message đến một subject được chỉ định đầy đủ, không dùng wildcard. Trong khi đó, subscriber có thể dùng wildcard để lắng nghe nhiều subject chỉ với một subscription duy nhất.

## Subject Hierarchy

> 🇬🇧 *The `.` character is used to create a subject hierarchy. For example, a world clock application might define the following to logically group related subjects:*

Ký tự `.` được dùng để tạo subject hierarchy. Ví dụ, ứng dụng đồng hồ thế giới có thể định nghĩa như sau để nhóm các subject liên quan theo logic:

```markup
time.us
time.us.east
time.us.east.atlanta
time.eu.east
time.eu.east.warsaw
```

## Các Thực Hành Tốt Nhất Khi Dùng Subject

> 🇬🇧 *There is no hard limit to subject size, but it is recommended to keep the maximum number of tokens in your subjects to a reasonable value. E.g. a maximum of 16 tokens and the subject length to less than 256 characters.*

Không có giới hạn cứng về kích thước subject, nhưng nên giữ số lượng token tối đa ở mức hợp lý — ví dụ: tối đa 16 token và độ dài subject dưới 256 ký tự.

### Số Lượng Subject

> 🇬🇧 *NATS can manage 10s of millions of subjects efficiently, therefore, you can use fine-grained addressing for your business entities. Subjects are ephemeral resources, which will disappear when no longer subscribed to.*

NATS có thể quản lý hàng chục triệu subject một cách hiệu quả, vì vậy có thể dùng định địa chỉ chi tiết cho các thực thể nghiệp vụ. Subject là tài nguyên tạm thời — sẽ biến mất khi không còn ai đăng ký.

> 🇬🇧 *Still, subject subscriptions need to be cached by the server in memory. Consider when increasing your subscribed subject count to more than one million you will need more than 1GB of server memory and it will grow linearly from there.*

Tuy nhiên, các subscription theo subject vẫn cần được server cache trong memory. Khi số lượng subject được đăng ký vượt quá một triệu, bạn sẽ cần hơn 1GB memory trên server và con số đó sẽ tăng tuyến tính từ đó.

### Lọc Subject và Bảo Mật

> 🇬🇧 *The message subject can be filtered with various means and through various configuration elements in your NATS server cluster. For example, but not limited to:*

Subject của message có thể được lọc bằng nhiều cách và thông qua nhiều thành phần config khác nhau trong NATS server cluster:

* Bảo mật - cho phép/từ chối theo user
* Import/export giữa các account
* Automatic transformation
* Khi đưa message vào JetStream stream
* Khi sourcing/mirroring JetStream stream
* Khi kết nối leaf node (NATS edge server)
* ...

> 🇬🇧 *A well-designed subject hierarchy will make the job a lot easier for those tasks.*

Một subject hierarchy được thiết kế tốt sẽ giúp các công việc trên dễ dàng hơn nhiều.

### Đặt Tên

> **ℹ️ Info:**
> There are only two hard problems in computer science: cache invalidation, naming things, and off-by-one errors. -- Unknown author

> **ℹ️ Info:**
> Trong khoa học máy tính chỉ có hai bài toán khó: cache invalidation, đặt tên, và lỗi off-by-one. -- Tác giả vô danh

> 🇬🇧 *A subject hierarchy is a powerful tool for addressing your application resources. Most NATS users therefore encode business semantics into the subject name. You are free to choose a structure fit for your purpose, but you should refrain from over-complicating your subject design at the start of the project.*

Subject hierarchy là công cụ mạnh để định địa chỉ tài nguyên ứng dụng. Phần lớn người dùng NATS mã hóa ngữ nghĩa nghiệp vụ vào tên subject. Bạn được tự do chọn cấu trúc phù hợp, nhưng không nên làm phức tạp quá thiết kế subject ngay từ đầu dự án.

**Một số hướng dẫn:**

> 🇬🇧 *Use the first token(s) to establish a general namespace.*

* Dùng token đầu tiên (hoặc vài token đầu) để xác lập namespace chung.

````shell
factory1.tools.group42.unit17
````

> 🇬🇧 *Use the final token(s) for identifiers*

* Dùng token cuối cùng (hoặc vài token cuối) cho các identifier.

````shell
service.deploy.server-acme.app123
````

> 🇬🇧 *A subject _should_ be used for more than one message. Subscriptions _should_ be stable (exist for receiving more than one message). Use wildcard subscriptions over subscribing to individual subjects whenever feasible. Name business or physical entities. Refrain from encoding too much data into the subject. Encode (business) intent into the subject, not technical details.*

* Một subject _nên_ được dùng cho nhiều hơn một message.
* Subscription _nên_ ổn định (tồn tại để nhận nhiều hơn một message).
* Ưu tiên dùng wildcard subscription thay vì đăng ký từng subject riêng lẻ khi có thể.
* Đặt tên theo thực thể nghiệp vụ hoặc vật lý. Tránh nhồi nhét quá nhiều dữ liệu vào subject.
* Mã hóa ý định (nghiệp vụ) vào subject, không phải chi tiết kỹ thuật.

Thực tế:

````shell
orders.online.store123.order171711
````

Không thực sự hữu ích:

````shell
orders.online.us.server42.ccpayment.premium.store123.electronics.deliver-dhl.order171711.create
````

> 🇬🇧 *NATS messages support headers. These can be used for additional metadata. There are subscription modes, which deliver headers only, allowing for efficient scanning of metadata in the message flow.*

* NATS message hỗ trợ header. Header có thể dùng để chứa metadata bổ sung. Có các chế độ subscription chỉ giao nhận header, cho phép quét metadata hiệu quả trong luồng message.

### Khớp Một Token Đơn

> 🇬🇧 *The first wildcard is `*` which will match a single token. For example, if an application wanted to listen for eastern time zones, they could subscribe to `time.*.east`, which would match `time.us.east` and `time.eu.east`. Note that `*` can not match a substring within a token `time.New*.east`.*

Wildcard đầu tiên là `*`, khớp với một token duy nhất. Ví dụ: nếu ứng dụng muốn lắng nghe các múi giờ phía đông, có thể subscribe vào `time.*.east`, sẽ khớp với `time.us.east` và `time.eu.east`. Lưu ý: `*` không thể khớp với một chuỗi con bên trong token `time.New*.east`.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/subjects2.svg)

### Khớp Nhiều Token

> 🇬🇧 *The second wildcard is `>` which will match one or more tokens, and can only appear at the end of the subject. For example, `time.us.>` will match `time.us.east` and `time.us.east.atlanta`, while `time.us.*` would only match `time.us.east` since it can't match more than one token.*

Wildcard thứ hai là `>`, khớp với một hoặc nhiều token và chỉ có thể xuất hiện ở cuối subject. Ví dụ: `time.us.>` sẽ khớp với `time.us.east` và `time.us.east.atlanta`, trong khi `time.us.*` chỉ khớp với `time.us.east` vì không thể khớp nhiều hơn một token.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/subjects3.svg)

### Giám Sát và Wire Tap

> 🇬🇧 *Subject to your security configuration, wildcards can be used for monitoring by creating something called a _wire tap_. In the simplest case, you can create a subscriber for `>`. This application will receive all messages -- again, subject to security settings -- sent on your NATS cluster.*

Tùy theo cấu hình bảo mật, wildcard có thể dùng để giám sát bằng cách tạo cái gọi là _wire tap_. Trong trường hợp đơn giản nhất, tạo một subscriber cho `>`. Ứng dụng này sẽ nhận tất cả message — vẫn phụ thuộc vào cài đặt bảo mật — được gửi trên NATS cluster.

### Kết Hợp Wildcard

> 🇬🇧 *The wildcard `*` can appear multiple times in the same subject. Both types can be used as well. For example, `*.*.east.>` will receive `time.us.east.atlanta`.*

Wildcard `*` có thể xuất hiện nhiều lần trong cùng một subject. Cả hai loại wildcard cũng có thể dùng kết hợp. Ví dụ: `*.*.east.>` sẽ nhận `time.us.east.atlanta`.

## Ký Tự Được Phép và Khuyến Nghị Cho Tên Subject

> 🇬🇧 *For compatibility across clients and ease of maintaining configuration files, we recommend using alphanumeric characters, `-` (dash) and `_` (underscore) ASCII characters for subject and other entity names created by the user.*

Để đảm bảo tương thích giữa các client và dễ bảo trì file config, nên dùng ký tự chữ-số, `-` (gạch ngang) và `_` (gạch dưới) ASCII cho subject và các tên thực thể do người dùng tạo.

> 🇬🇧 *UTF-8 (UTF8) characters are supported in subjects. Please use UTF-8 characters at your own risk. Using multilingual names for technical entities can create many issues for editing, configuration files, display, and cross-border collaboration.*

UTF-8 được hỗ trợ trong subject. Tuy nhiên, việc dùng ký tự UTF-8 là tự chịu rủi ro. Đặt tên thực thể kỹ thuật bằng nhiều ngôn ngữ có thể gây ra nhiều vấn đề về chỉnh sửa, file config, hiển thị và cộng tác xuyên biên giới.

> 🇬🇧 *The rules and recommendations here apply to ALL system names, subjects, streams, durables, buckets, keys (in key-value stores), as NATS will create API subjects that contain those names. NATS will enforce these constraints in most cases, but we recommend not relying on this.*

Các quy tắc và khuyến nghị này áp dụng cho TẤT CẢ tên hệ thống: subject, stream (luồng message lưu trữ liên tục), durable, bucket, key (trong key-value store), vì NATS sẽ tạo API subject chứa các tên đó. NATS thực thi các ràng buộc này trong hầu hết trường hợp, nhưng không nên dựa vào điều đó.

* **Ký tự được phép**: Bất kỳ ký tự Unicode nào ngoại trừ `null`, khoảng trắng, `.`, `*` và `>`

* **Ký tự khuyến nghị:** (`a` - `z`), (`A` - `Z`), (`0` - `9`), `-` và `_` (tên có phân biệt hoa/thường và không được chứa khoảng trắng).

* **Quy ước đặt tên:** Nếu muốn phân tách từ, dùng PascalCase như `MyServiceOrderCreate` hoặc `-` và `_` như `my-service-order-create`

* **Ký tự đặc biệt:** Dấu chấm `.` (dùng để tách token trong subject), `*` và `>` (`*` và `>` được dùng làm wildcard) là ký tự dành riêng, không được sử dụng.

* **Tên dành riêng:** Theo quy ước, tên subject bắt đầu bằng `$` được dành cho hệ thống (ví dụ: tên bắt đầu bằng `$SYS` hoặc `$JS` hoặc `$KV`, v.v...). Nhiều subject hệ thống cũng dùng `_` (gạch dưới) (ví dụ: _INBOX, KV_ABC, OBJ_XYZ...).

Tên tốt

```markup
time.us
time.us2.east1
time.new-york
time.SanFrancisco
```

Tên subject không nên dùng nữa

```markup
location.Malmö
$location.Stockholm
_Subjects_.mysubject
```

Tên stream bị cấm

```markup
all*data
<my_stream>
service.stream.1
```

### Chế Độ Pedantic

> 🇬🇧 *By default, for the sake of efficiency, subject names are not verified during message publishing. In particular, when generating subjects programmatically, this will result in illegal subjects which cannot be subscribed to. E.g. subjects containing wildcards may be ignored.*

Theo mặc định, để đảm bảo hiệu suất, tên subject không được xác thực khi publishing message. Đặc biệt, khi tạo subject theo chương trình, điều này có thể tạo ra subject không hợp lệ không thể subscribe. Ví dụ: subject chứa wildcard có thể bị bỏ qua.

> 🇬🇧 *To enable subject name verification, activate `pedantic` mode in the client connection options.*

Để bật xác thực tên subject, kích hoạt chế độ `pedantic` trong tùy chọn kết nối client.

```markup
//Java
Options options = Options.builder()
    .server("nats://127.0.0.1:4222")
    .pedantic()
    .build();
Connection nc = Nats.connect(options)
```

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **cache**: bộ nhớ đệm
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **publisher**: bên gửi message
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **topic**: chủ đề phân loại message