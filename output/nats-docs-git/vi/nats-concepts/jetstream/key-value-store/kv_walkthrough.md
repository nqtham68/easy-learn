---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/jetstream/key-value-store/kv_walkthrough
title: Hướng dẫn sử dụng Key/Value Store
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Hướng dẫn sử dụng Key/Value Store

> 🇬🇧 *The Key/Value Store is a JetStream feature, so we need to verify it is enabled by*

Key/Value Store là tính năng của JetStream, vì vậy cần kiểm tra xem JetStream đã được bật chưa bằng lệnh:

```shell
nats account info
```

> 🇬🇧 *which may return*

Lệnh trên có thể trả về:

```
JetStream Account Information:

   JetStream is not supported in this account
```

> 🇬🇧 *In this case, you should enable JetStream.*

Nếu gặp kết quả trên, hãy bật JetStream.

## Điều kiện tiên quyết: bật JetStream

> 🇬🇧 *If you are running a local `nats-server` stop it and restart it with JetStream enabled using `nats-server -js` (if that's not already done)*

Nếu đang chạy `nats-server` cục bộ, hãy dừng lại và khởi động lại với JetStream được bật bằng `nats-server -js` (nếu chưa làm).

> 🇬🇧 *You can then check that JetStream is enabled by using*

Sau đó kiểm tra JetStream đã được bật chưa bằng:

```shell
nats account info
```

```
Connection Information:

               Client ID: 6
               Client IP: 127.0.0.1
                     RTT: 64.996µs
       Headers Supported: true
         Maximum Payload: 1.0 MiB
           Connected URL: nats://127.0.0.1:4222
       Connected Address: 127.0.0.1:4222
     Connected Server ID: ND2XVDA4Q363JOIFKJTPZW3ZKZCANH7NJI4EJMFSSPTRXDBFG4M4C34K

JetStream Account Information:

           Memory: 0 B of Unlimited
          Storage: 0 B of Unlimited
          Streams: 0 of Unlimited
        Consumers: 0 of Unlimited 
```

## Tạo KV bucket

> 🇬🇧 *A 'KV bucket' is like a stream; you need to create it before using it, as in `nats kv add <KV Bucket Name>`:*

Một 'KV bucket' tương tự như một stream (luồng message lưu trữ liên tục) — cần tạo trước khi sử dụng, ví dụ với `nats kv add <KV Bucket Name>`:

```shell
nats kv add my-kv
```

```
my_kv Key-Value Store Status

         Bucket Name: my-kv
         History Kept: 1
        Values Stored: 0
           Compressed: false
   Backing Store Kind: JetStream
          Bucket Size: 0 B
  Maximum Bucket Size: unlimited
   Maximum Value Size: unlimited
          Maximum Age: unlimited
     JetStream Stream: KV_my-kv
              Storage: File
```

## Lưu một giá trị

> 🇬🇧 *Now that we have a bucket, we can assign, or 'put', a value to a specific key:*

Sau khi có bucket, ta có thể gán ('put') một giá trị cho một key cụ thể:

```shell
nats kv put my-kv Key1 Value1
```

> 🇬🇧 *which should return the key's value `Value1`*

Lệnh này sẽ trả về giá trị của key là `Value1`.

## Lấy một giá trị

> 🇬🇧 *We can fetch, or 'get', the value for a key "Key1":*

Ta có thể truy xuất ('get') giá trị của key "Key1":

```shell
nats kv get my-kv Key1
```

```
my-kv > Key1 created @ 12 Oct 21 20:08 UTC

Value1
```

## Xóa một giá trị

> 🇬🇧 *You can always delete a key and its value by using*

Để xóa một key cùng giá trị của nó, dùng:

```shell
nats kv del my-kv Key1
```

> 🇬🇧 *It is harmless to delete a non-existent key (check this!!).*

Xóa một key không tồn tại là hoàn toàn vô hại (hãy tự kiểm chứng!!).

## Các thao tác atomic

> 🇬🇧 *K/V Stores can also be used in concurrent design patterns, such as semaphores, by using atomic 'create' and 'update' operations.*

K/V Store còn có thể dùng trong các mô hình lập trình đồng thời, chẳng hạn như semaphore, thông qua các thao tác atomic 'create' và 'update'.

> 🇬🇧 *E.g. a client wanting exclusive use of a file can lock it by creating a key, whose value is the file name, with `create` and deleting this key after completing use of that file. A client can increase the resilience against failure by using a timeout for the `bucket` containing this key. The client can use `update` with a revision number to keep the `bucket` alive.*

Ví dụ, một client muốn dùng độc quyền một file có thể lock nó bằng cách tạo một key có giá trị là tên file đó với `create`, rồi xóa key sau khi dùng xong. Để tăng độ bền khi có sự cố, client có thể đặt timeout (thời gian chờ tối đa) cho `bucket` chứa key đó. Client có thể dùng `update` kèm revision number để giữ cho `bucket` tiếp tục hoạt động.

> 🇬🇧 *Updates can also be used for more fine-grained concurrency control, sometimes known as `optimistic locking`, where multiple clients can try a task, but only one can successfully complete it.*

Thao tác update còn cho phép kiểm soát đồng thời ở mức độ chi tiết hơn, đôi khi gọi là `optimistic locking`, khi đó nhiều client cùng thử thực hiện một tác vụ nhưng chỉ một client hoàn thành được.

### Tạo (hay còn gọi là exclusive locking)

> 🇬🇧 *Create a lock/semaphore with the `create` operation.*

Tạo lock/semaphore bằng thao tác `create`.

```shell 
nats kv create my-sem Semaphore1 Value1
```

> 🇬🇧 *Only one `create` can succeed. First come, first serve. All concurrent attempts will result in an error until the key is deleted*

Chỉ một `create` thành công. Ai đến trước được trước. Mọi lần thử đồng thời khác đều trả về lỗi cho đến khi key bị xóa.

```shell 
nats kv create my-sem Semaphore1 Value1
nats: error: nats: wrong last sequence: 1: key exists
```

### Update với CAS (hay còn gọi là optimistic locking)

> 🇬🇧 *We can also atomically `update`, sometimes known as a CAS (compare and swap) operation, a key with an additional parameter `revision`*

Ta cũng có thể thực hiện `update` theo kiểu atomic, đôi khi gọi là thao tác CAS (compare and swap), với tham số bổ sung `revision`.

```shell 
nats kv update my-sem Semaphore1 Value2 13
```

> 🇬🇧 *A second attempt with the same revision 13, will fail*

Lần thử thứ hai với cùng revision 13 sẽ thất bại:

```shell 
nats kv update my-sem Semaphore1 Value2 13
nats: error: nats: wrong last sequence: 14
```

## Theo dõi K/V Store

> 🇬🇧 *An unusual functionality of a K/V Store is being able to 'watch' a bucket, or a specific key in that bucket, and receive real-time updates to changes in the store.*

Một tính năng đặc biệt của K/V Store là khả năng 'watch' — theo dõi toàn bộ bucket hoặc một key cụ thể trong bucket, và nhận cập nhật theo thời gian thực khi có thay đổi.

> 🇬🇧 *For the example above, run `nats kv watch my-kv`. This will start a watcher on the bucket we have just created earlier. By default, the KV bucket has a history size of one, and so it only remembers the last change. In our case, the watcher should see a delete of the value associated with the key "Key1":*

Để thực hành, chạy `nats kv watch my-kv`. Lệnh này sẽ khởi động watcher trên bucket vừa tạo ở trên. Mặc định, KV bucket có history size bằng 1, tức là chỉ ghi nhớ thay đổi cuối cùng. Trong ví dụ này, watcher sẽ thấy thao tác xóa giá trị của key "Key1":

```shell
nats kv watch my-kv
```

```
[2021-10-12 13:15:03] DEL my-kv > Key1
```

> 🇬🇧 *If we now concurrently change the value of 'my-kv' by*

Nếu ta đồng thời thay đổi giá trị của 'my-kv' bằng:

```shell
nats kv put my-kv Key1 Value2
```

> 🇬🇧 *The watcher will see that change:*

Watcher sẽ nhận được thay đổi đó:

```shell
[2021-10-12 13:25:14] PUT my-kv > Key1: Value2
```

## Dọn dẹp

> 🇬🇧 *When you are finished using a bucket, you can delete the bucket, and its resources, by using the `rm` operator:*

Khi không còn cần dùng bucket nữa, có thể xóa bucket cùng toàn bộ tài nguyên của nó bằng toán tử `rm`:

```shell
nats kv rm my-kv
```

## Thuật ngữ trong bài

- **stream**: luồng message lưu trữ liên tục
- **timeout**: thời gian chờ tối đa