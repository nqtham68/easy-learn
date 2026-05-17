---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/jetstream/key-value-store
title: Key/Value Store
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Key/Value Store

> 🇬🇧 *JetStream, the persistence layer of NATS, not only allows for the higher qualities of service and features associated with 'streaming', but it also enables some functionalities not found in messaging systems.*

JetStream, tầng lưu trữ bền vững của NATS, không chỉ cung cấp chất lượng dịch vụ cao và các tính năng liên quan đến streaming, mà còn hỗ trợ nhiều chức năng không có trong các hệ thống messaging thông thường.

> 🇬🇧 *One such feature is the Key/Value store functionality, which allows client applications to create `buckets` and use them as immediately (as opposed to eventually) consistent, persistent [associative arrays](https://en.wikipedia.org/wiki/Associative_array) (or maps). Note that this is an abstraction on top of the Stream functionality. Buckets are materialized as Streams (with a name starting with `KV_`), everything you can do with a bucket you can do with a Stream, but you ultimately have more functionality and flexibility and control when using the Stream functionality directly.*

Một trong số đó là tính năng Key/Value store, cho phép ứng dụng client tạo `buckets` và sử dụng chúng như những [mảng kết hợp](https://en.wikipedia.org/wiki/Associative_array) (hay map) nhất quán tức thì (immediate consistency, khác với eventual consistency) và bền vững. Đây là một lớp trừu tượng xây dựng trên nền Stream (luồng message lưu trữ liên tục). Mỗi bucket được hiện thực hóa thành một Stream (với tên bắt đầu bằng `KV_`). Bất kỳ thao tác nào thực hiện được với bucket đều có thể làm với Stream, nhưng dùng trực tiếp Stream sẽ cho nhiều khả năng, linh hoạt và kiểm soát hơn.

> 🇬🇧 *Do note, while we do guarantee immediate consistency when it comes to [monotonic writes](https://jepsen.io/consistency/models/monotonic-writes) and [monotonic reads](https://jepsen.io/consistency/models/monotonic-reads). We don't guarantee [read your writes](https://jepsen.io/consistency/models/read-your-writes) at this time, as reads through _direct get_ requests may be served by followers or mirrors. More consistent results can be achieved by sending get requests to the underlying stream leader of the Key/Value store.*

Lưu ý: mặc dù NATS đảm bảo nhất quán tức thì với [monotonic writes](https://jepsen.io/consistency/models/monotonic-writes) và [monotonic reads](https://jepsen.io/consistency/models/monotonic-reads), nhưng hiện tại không đảm bảo [read your writes](https://jepsen.io/consistency/models/read-your-writes), vì các request _direct get_ có thể được phục vụ bởi follower (server phụ trong nhóm replica) hoặc mirror. Để có kết quả nhất quán hơn, hãy gửi request get trực tiếp đến stream leader của Key/Value store.

* [Walkthrough](./kv_walkthrough.md)
* [Details](../../../using-nats/developing-with-nats/js/kv.md)

## Quản lý Key/Value Store

> 🇬🇧 *1. Create a bucket, which corresponds to a stream in the underlying storage. Define KV/Stream limits as appropriate*
> 🇬🇧 *2. Use the operation below.*

1. Tạo một bucket, tương ứng với một stream trong lớp lưu trữ bên dưới. Đặt giới hạn KV/Stream phù hợp.
2. Sử dụng các thao tác ở phần tiếp theo.

## Các thao tác kiểu Map

> 🇬🇧 *You can use KV buckets to perform the typical operations you would expect from an immediately consistent key/value store:*

Có thể dùng KV bucket để thực hiện các thao tác tiêu chuẩn của một key/value store nhất quán tức thì:

* **put**: gán một giá trị cho một key
* **get**: lấy giá trị gắn với một key
* **delete**: xóa giá trị gắn với một key
* **purge**: xóa toàn bộ giá trị của tất cả các key
* **keys**: lấy bản sao danh sách tất cả các key (kèm giá trị hoặc thao tác liên quan)

## Các thao tác atomic dùng cho locking và kiểm soát đồng thời

> 🇬🇧 *- create: associate the value with a key only if there is currently no value associated with that key (i.e. compare to null and set)*
> 🇬🇧 *- update: compare and set (aka compare and swap) the value for a key*

* **create**: gán giá trị cho một key chỉ khi key đó chưa có giá trị nào (tức là so sánh với null rồi mới gán)
* **update**: compare-and-set (hay compare-and-swap) giá trị của một key

## Giới hạn kích thước, TTL, v.v.

> 🇬🇧 *You can set limits for your buckets, such as:*
> 🇬🇧 *- the maximum size of the bucket*
> 🇬🇧 *- the maximum size for any single value*
> 🇬🇧 *- a TTL: how long the store will keep values for*

Có thể đặt các giới hạn cho bucket:

* kích thước tối đa của bucket
* kích thước tối đa của một giá trị đơn lẻ
* TTL: thời gian lưu trữ giá trị trong store

## Sử dụng Key/Value Store như một message stream

> 🇬🇧 *Finally, you can even do things that typically can not be done with a Key/Value Store:*

Ngoài ra, có thể thực hiện những thao tác thường không có trong Key/Value Store thông thường:

> 🇬🇧 *- watch: watch for changes happening for a key, which is similar to subscribing (in the publish/subscribe sense) to the key: the watcher receives updates due to put or delete operations on the key pushed to it in real-time as they happen*
> 🇬🇧 *- watch all: watch for all the changes happening on all the keys in the bucket*
> 🇬🇧 *- history: retrieve a history of the values (and delete operations) associated with each key over time (by default the history of buckets is set to 1, meaning that only the latest value/operation is stored)*

* **watch**: theo dõi các thay đổi xảy ra với một key, tương tự như subscribe (theo nghĩa publish/subscribe) vào key đó — watcher nhận cập nhật theo thời gian thực khi có thao tác put hoặc delete trên key
* **watch all**: theo dõi tất cả các thay đổi trên mọi key trong bucket
* **history**: lấy lịch sử các giá trị (và thao tác delete) của từng key theo thời gian (mặc định history của bucket là 1, tức chỉ lưu giá trị/thao tác mới nhất)

## Ghi chú

> 🇬🇧 *A valid key can contain the following characters: `a-z`, `A-Z`, `0-9`, `_`, `-`, `.`, `=` and `/`, i.e. it can be a dot-separated list of tokens (which means that you can then use wildcards to match hierarchies of keys when watching a bucket). The value can be any byte array.*

Một key hợp lệ có thể chứa các ký tự sau: `a-z`, `A-Z`, `0-9`, `_`, `-`, `.`, `=` và `/` — tức là key có thể là danh sách các token phân tách bằng dấu chấm (cho phép dùng wildcard để khớp theo cấu trúc phân cấp khi watch một bucket). Value có thể là bất kỳ mảng byte nào.

## Thuật ngữ trong bài

- **consumer**: bên xử lý dữ liệu từ stream
- **follower**: server phụ trong nhóm replica
- **leader**: server chính trong nhóm replica
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)