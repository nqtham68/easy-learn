---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/jetstream/object-store/obj_store
title: Object Store
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Object Store

> 🇬🇧 *JetStream, the persistence layer of NATS, not only allows for the higher qualities of service and features associated with 'streaming', but it also enables some functionalities not found in messaging systems.*

JetStream, tầng lưu trữ bền vững của NATS, không chỉ cung cấp các chất lượng dịch vụ và tính năng liên quan đến 'streaming', mà còn cho phép một số chức năng không có trong các hệ thống messaging thông thường.

> 🇬🇧 *One such feature is the Object store functionality, which allows client applications to create `buckets` (corresponding to streams) that can store a set of files. Files are stored and transmitted in chunks, allowing files of arbitrary size to be transferred safely over the NATS infrastructure.*

Một trong số đó là chức năng Object store, cho phép các ứng dụng client tạo `buckets` (tương ứng với các stream (luồng message lưu trữ liên tục)) để lưu trữ tập hợp các file. File được lưu và truyền theo từng chunk, cho phép chuyển file có kích thước tùy ý một cách an toàn qua hạ tầng NATS.

> 🇬🇧 ***Note:** Object store is not a distributed storage system. All files in a bucket will need to fit on the target file system.*

**Lưu ý:** Object store không phải là hệ thống lưu trữ phân tán. Tất cả file trong một bucket đều phải vừa với file system đích.

* [Walkthrough](./obj_walkthrough.md)
* [Details](../../../using-nats/developing-with-nats/js/object.md)

## Khả năng Cơ Bản

> 🇬🇧 *The Object Store implements a chunking mechanism, allowing you to for example store and retrieve files (i.e. the object) of any size by associating them with a path or file name as the key.*

Object Store triển khai cơ chế chunking, cho phép lưu trữ và truy xuất file (tức là object) có kích thước tùy ý bằng cách gắn với một đường dẫn hoặc tên file làm khóa.

* `add` a `bucket` to hold the files.
* `put` Add a file to the bucket
* `get` Retrieve the file and store it to a designated location
* `del` Delete a file

## Khả năng Nâng Cao

* `watch` Subscribe to changes in the bucket. Will receive notifications on successful `put` and `del` operations.

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **stream**: luồng message lưu trữ liên tục