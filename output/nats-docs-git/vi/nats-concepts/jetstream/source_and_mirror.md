---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/jetstream/source_and_mirror
title: Stream Source và Mirror
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Stream Source và Mirror

> 🇬🇧 *When a stream is configured with a `source` or `mirror`, it will automatically and asynchronously replicate messages from the origin stream.*

Khi một stream (luồng message lưu trữ liên tục) được cấu hình với `source` hoặc `mirror`, nó sẽ tự động sao chép message từ stream gốc theo cơ chế bất đồng bộ.

> 🇬🇧 *`source` or `mirror` are designed to be robust and will recover from a loss of connection. They are suitable for geographic distribution over high latency and unreliable connections. E.g. even a leaf node starting and connecting intermittently every few days will still receive or send messages over the source/mirror link. Another use case is when [connecting streams cross-account](../../running-a-nats-service/configuration/securing_nats/accounts.md#exporting-and-importing).*

`source` và `mirror` được thiết kế để hoạt động bền vững, tự phục hồi sau khi mất kết nối. Chúng phù hợp cho việc phân phối theo địa lý qua các kết nối có độ trễ cao hoặc không ổn định. Ví dụ, một leaf node chỉ kết nối gián đoạn vài ngày một lần vẫn có thể nhận hoặc gửi message qua liên kết source/mirror. Trường hợp sử dụng khác là khi [kết nối stream giữa các account](../../running-a-nats-service/configuration/securing_nats/accounts.md#exporting-and-importing).

> 🇬🇧 *There are several options available when declaring the configuration.*

Có một số tùy chọn khi khai báo cấu hình:

* `Name` - Tên stream gốc cần lấy dữ liệu.
* `StartSeq` - Sequence bắt đầu tùy chọn trên stream gốc để bắt đầu mirror từ đó.
* `StartTime` - Thời điểm bắt đầu tùy chọn để mirror. Các message có thời gian bằng hoặc sau mốc này sẽ được đưa vào.
* `FilterSubject` - Subject (chuỗi định danh message) lọc tùy chọn, chỉ lấy các message khớp với subject đó, thường kèm wildcard. Lưu ý: không dùng đồng thời với `SubjectTransforms`.
* `SubjectTransforms` - Tập hợp tùy chọn các [subject transform](../../running-a-nats-service/configuration/configuring_subject_mapping.md) áp dụng khi lấy message từ stream gốc. Trong ngữ cảnh này, `Source` hoạt động như bộ lọc trên stream gốc, còn `Destination` có thể được cung cấp tùy chọn để áp dụng transform. Vì có thể dùng nhiều subject transform, các subject rời rạc có thể được lấy từ stream gốc mà vẫn giữ nguyên thứ tự message. Lưu ý: không dùng đồng thời với `FilterSubject`.
* `Domain` - JetStream domain tùy chọn chỉ nơi stream gốc tồn tại. Thường dùng trong kiến trúc hub cluster và leaf node.

> 🇬🇧 *The stream using a source or mirror configuration can have its own retention policy, replication, and storage type.*

Stream sử dụng cấu hình source hoặc mirror có thể có retention policy, replication (bản sao dữ liệu) và kiểu lưu trữ riêng.

> **ℹ️ Info:**
> * Changes to the stream using source or mirror, e.g. deleting messages or publishing, do not reflect back on the origin stream from which the data was received.
> * Deletes in the origin stream are NOT replicated through a `source` or `mirror` agreement.

Lưu ý: Các thay đổi trên stream đích (xóa message hoặc publish) không ảnh hưởng ngược lại stream gốc. Ngoài ra, việc xóa message ở stream gốc KHÔNG được sao chép qua liên kết `source` hoặc `mirror`.

> **ℹ️ Info:**
> `Sources` is a generalization of the `Mirror` and allows for sourcing data from one or more streams concurrently. If you require the target stream to act as a read-only replica:
>
> * Configure the stream without listen subjects **or**
> * Temporarily disable the listen subjects through client authorizations.

`Sources` là dạng tổng quát hơn của `Mirror`, cho phép lấy dữ liệu từ một hoặc nhiều stream cùng lúc. Nếu cần stream đích chỉ đóng vai trò replica chỉ đọc: cấu hình stream không có listen subject, hoặc tạm thời vô hiệu hóa listen subject qua phân quyền client.

## Hành vi chung

> 🇬🇧 *All configurations are made on the receiving side. The stream from which data is sourced and mirrored does not need to be configured. No cleanup is required on the origin side if the receiver disappears.*

* Toàn bộ cấu hình được thực hiện ở phía nhận. Stream gốc không cần cấu hình gì thêm, và không cần dọn dẹp gì ở phía gốc khi phía nhận biến mất.

> 🇬🇧 *A stream can be the origin (source) for multiple streams. This is useful for geographic distribution or for designing "fan out" topologies where data needs to be distributed reliable to a large number (up to millions) of client connections.*

* Một stream có thể là nguồn (source) cho nhiều stream khác. Điều này hữu ích để phân phối theo địa lý hoặc thiết kế topology "fan out" phân phối dữ liệu tin cậy tới số lượng lớn kết nối client (lên tới hàng triệu).

> 🇬🇧 *Leaf nodes and leaf node domains are explicitly supported through the `API prefix`*

* Leaf node và leaf node domain được hỗ trợ tường minh thông qua `API prefix`.

## Đặc thù của Source

> 🇬🇧 *A stream defining `Sources` is a generalized replication mechanism and allows for sourcing data from **one or more streams** concurrently. A stream with sources can still act as a regular stream allowing direct write/publish by local clients to the stream. Essentially the source streams and local client writes are aggregated into a single interleaved stream. Combined with subject transformation and filtering sourcing allows to design sophisticated data distribution architectures.*

Stream định nghĩa `Sources` là cơ chế sao chép tổng quát, cho phép lấy dữ liệu từ **một hoặc nhiều stream** cùng lúc. Stream có source vẫn hoạt động như stream thông thường, cho phép client ghi/publish trực tiếp vào. Về bản chất, dữ liệu từ các stream nguồn và các lần ghi local được gộp lại thành một stream xen kẽ duy nhất. Kết hợp với subject transform và filtering, tính năng source cho phép thiết kế các kiến trúc phân phối dữ liệu phức tạp.

> **ℹ️ Info:**
> Sourcing messages does not retain sequence numbers. But it retain the in stream sequence of messages . Between streams sourced to the same target, the sequence of messages is undefined.

Lưu ý: Khi source message, sequence number không được giữ nguyên, nhưng thứ tự trong từng stream vẫn được bảo toàn. Thứ tự giữa các stream được source vào cùng đích là không xác định.

## Đặc thù của Mirror

> 🇬🇧 *A mirror can source its messages from **exactly one stream** and a clients can not directly write to the mirror. Although messages cannot be published to a mirror directly by clients, messages can be deleted on-demand (beyond the retention policy), and consumers have all capabilities available on regular streams.*

Mirror chỉ có thể lấy message từ **đúng một stream** duy nhất và client không thể ghi trực tiếp vào mirror. Dù vậy, có thể xóa message theo yêu cầu (ngoài retention policy), và consumer (bên xử lý dữ liệu từ stream) vẫn có đầy đủ tính năng như trên stream thông thường.

> **ℹ️ Info:**
> * Mirrored messages retains the sequence numbers and timestamps of the origin stream.
> * Mirrors can be used for for (geographic) load distribution with the `MirrorDirect` stream attribute. See: [https://docs.nats.io/nats-concepts/jetstream/streams#configuration](./streams.md#configuration)

Lưu ý: Message được mirror giữ nguyên sequence number và timestamp từ stream gốc. Mirror có thể dùng để phân phối tải (theo địa lý) thông qua thuộc tính stream `MirrorDirect`. Xem: [https://docs.nats.io/nats-concepts/jetstream/streams#configuration](./streams.md#configuration).

## Hành vi trong các điều kiện biên

> 🇬🇧 *Source and mirror contracts are designed with one-way (geographic) data replication in mind. Neither configuration provides a full synchronization between streams, which would include deletes or replication of other stream attributes.*

* Source và mirror được thiết kế cho việc sao chép dữ liệu một chiều (theo địa lý). Không cấu hình nào cung cấp đồng bộ hoàn toàn giữa các stream — bao gồm cả việc sao chép lệnh xóa hay các thuộc tính stream khác.

> 🇬🇧 *The content of the stream from which a source or mirror is drawn needs to be reasonable stable. Quickly deleting messages after publishing them may result in inconsistent replication due to the asynchronous nature of the replication process.*

* Nội dung stream gốc cần tương đối ổn định. Xóa message ngay sau khi publish có thể dẫn đến sao chép không nhất quán do tính bất đồng bộ của quá trình replication.

> 🇬🇧 *Sources and Mirror try to be be efficient in replicating messages and are lenient towards the source/mirror origin being unreachable (event for extended periods of time), e.g. when using leaf nodes, which are connected intermittently. For sake of efficiency the recovery interval in case of a disconnect is 10-20s.*

* Source và Mirror cố gắng sao chép message hiệu quả và chịu được việc stream gốc không tiếp cận được (kể cả trong thời gian dài), ví dụ khi dùng leaf node kết nối gián đoạn. Để đảm bảo hiệu quả, khoảng thời gian phục hồi sau khi mất kết nối là 10–20 giây.

> 🇬🇧 *Mirror and source agreements do not create a visible consumer in the origin stream.*

* Liên kết mirror và source không tạo consumer hiển thị ở stream gốc.

### WorkQueue/Interest retention

> **ℹ️ Info:**
> Stream sourcing and mirroring for WorkQueue or Interest streams are supported since version 2.14.

Lưu ý: Sourcing và mirroring stream cho WorkQueue hoặc Interest stream được hỗ trợ từ phiên bản 2.14.

> 🇬🇧 *When using stream sourcing/mirroring on a WorkQueue or Interest stream, the consumer used is automatically 'upgraded' to a durable consumer. This consumer is visible to the user and can be monitored or paused to temporarily stop the sourcing from the sourced-side.*

Khi dùng stream sourcing/mirroring trên WorkQueue hoặc Interest stream, consumer được tự động "nâng cấp" thành durable consumer. Consumer này hiển thị với người dùng và có thể được theo dõi hoặc tạm dừng để ngừng sourcing từ phía nguồn.

> **⚠️ Warning:**
> On versions prior to 2.14, sourcing from a WorkQueue/Interest stream is not supported. JetStream does not forbid this configuration, but the behavior is undefined.

Cảnh báo: Trên các phiên bản trước 2.14, sourcing từ WorkQueue/Interest stream không được hỗ trợ. JetStream không chặn cấu hình này nhưng hành vi là không xác định.

### Consumer tự cung cấp ("Bring your own")

> 🇬🇧 *Starting in version 2.14, you can "bring your own" sourcing consumer. This pre-created consumer can then be used for stream sourcing/mirroring, instead of the server automatically creating it based on the stream configuration. Useful for more flexible consumer configuration, as well as additional monitoring or operational capabilities, or generally when you're not in control of "the other side" and are required to do this from a security point of view.*

Từ phiên bản 2.14, bạn có thể tự cung cấp sourcing consumer ("bring your own"). Consumer được tạo sẵn này sẽ được dùng cho stream sourcing/mirroring thay vì để server tự tạo dựa trên cấu hình stream. Tính năng này hữu ích khi cần cấu hình consumer linh hoạt hơn, bổ sung khả năng theo dõi hoặc vận hành, hoặc khi bạn không kiểm soát được "phía kia" và cần thực hiện điều này từ góc độ bảo mật.

> 🇬🇧 *The following options are used to "bring your own" sourcing consumer:*

Các tùy chọn sau dùng để tự cung cấp sourcing consumer:

* `Name` - Tên stream gốc cần lấy dữ liệu.
* `Consumer.Name` - Tên consumer dùng cho sourcing.
* `Consumer.DeliverSubject` - Deliver subject mà message sẽ được giao tới.

> 🇬🇧 *Other options like `StartSeq`, `StartTime`, `FilterSubject`, etc. are not supported when using this approach. Instead, these settings should be configured directly on the consumer.*

Các tùy chọn khác như `StartSeq`, `StartTime`, `FilterSubject`, v.v. không được hỗ trợ khi dùng cách tiếp cận này. Thay vào đó, hãy cấu hình các thiết lập đó trực tiếp trên consumer.

> 🇬🇧 *This consumer is required to have `AckFlowControl` as its ack policy, meaning the sourced-side will only receive acknowledgements until after the sourcing-side has persisted the messages.*

Consumer này bắt buộc phải có `AckFlowControl` là ack policy, nghĩa là phía nguồn chỉ nhận acknowledgement sau khi phía sourcing đã lưu trữ xong message.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)