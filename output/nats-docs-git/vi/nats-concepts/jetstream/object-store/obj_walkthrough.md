---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/jetstream/object-store/obj_walkthrough
title: Hướng Dẫn Sử Dụng Object Store
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Hướng Dẫn Sử Dụng Object Store

> 🇬🇧 *If you are running a local `nats-server` stop it and restart it with JetStream enabled using `nats-server -js` (if that's not already done)*

Nếu đang chạy `nats-server` cục bộ, hãy dừng lại và khởi động lại với JetStream (stream (luồng message lưu trữ liên tục) do NATS quản lý) được bật bằng `nats-server -js` (nếu chưa làm).

> 🇬🇧 *You can then check that JetStream is enabled by using*

Sau đó kiểm tra JetStream đã được bật chưa bằng lệnh:

```shell
nats account info
```

> 🇬🇧 *Which should output something like:*

Kết quả sẽ trông như sau:

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

> 🇬🇧 *If you see the below instead then JetStream is _not_ enabled*

Nếu thấy kết quả bên dưới thì JetStream _chưa_ được bật:

```
JetStream Account Information:

   JetStream is not supported in this account
```

## Tạo Bucket Object Store

> 🇬🇧 *Just like you need to create streams before you can use them you need to first create an Object Store bucket*

Tương tự như stream, bạn cần tạo bucket Object Store trước khi sử dụng:

```shell
nats object add myobjbucket
```

> 🇬🇧 *which outputs*

Kết quả:

```
myobjbucket Object Store Status

         Bucket Name: myobjbucket
            Replicas: 1
                 TTL: unlimitd
              Sealed: false
                Size: 0 B
  Backing Store Kind: JetStream
    JetStream Stream: OBJ_myobjbucket
```

## Đưa File Vào Bucket

```shell
nats object put myobjbucket ~/Movies/NATS-logo.mov
```

```
1.5 GiB / 1.5 GiB [====================================================================================]

Object information for myobjbucket > /Users/jnmoyne/Movies/NATS-logo.mov

               Size: 1.5 GiB
  Modification Time: 14 Apr 22 00:34 +0000
             Chunks: 12,656
             Digest: sha-256 8ee0679dd1462de393d81a3032d71f43d2bc89c0c8a557687cfe2787e926
```

## Đưa File Vào Bucket Với Tên Chỉ Định

> 🇬🇧 *By default the full file path is used as a key. Provide the key explicitly (e.g. a relative path ) with `--name`*

Mặc định, đường dẫn đầy đủ của file được dùng làm key. Dùng `--name` để chỉ định key tường minh (ví dụ: đường dẫn tương đối):

```shell
nats object put --name /Movies/NATS-logo.mov myobjbucket ~/Movies/NATS-logo.mov
```

```
1.5 GiB / 1.5 GiB [====================================================================================]

Object information for myobjbucket > /Movies/NATS-logo.mov

               Size: 1.5 GiB
  Modification Time: 14 Apr 22 00:34 +0000
             Chunks: 12,656
             Digest: sha-256 8ee0679dd1462de393d81a3032d71f43d2bc89c0c8a557687cfe2787e926
```

## Liệt Kê Các Object Trong Bucket

```shell
nats object ls myobjbucket
```

```
╭───────────────────────────────────────────────────────────────────────────╮
│                              Bucket Contents                              │
├─────────────────────────────────────┬─────────┬───────────────────────────┤
│ Name                                │ Size    │ Time                      │
├─────────────────────────────────────┼─────────┼───────────────────────────┤
│ /Users/jnmoyne/Movies/NATS-logo.mov │ 1.5 GiB │ 2022-04-13T17:34:55-07:00 │
│ /Movies/NATS-logo.mov               │ 1.5 GiB │ 2022-04-13T17:35:41-07:00 │
╰─────────────────────────────────────┴─────────┴───────────────────────────╯
```

## Lấy Object Từ Bucket

```shell
nats object get myobjbucket ~/Movies/NATS-logo.mov
```

```
1.5 GiB / 1.5 GiB [====================================================================================]

Wrote: 1.5 GiB to /Users/jnmoyne/NATS-logo.mov in 5.68s average 279 MiB/s
```

## Lấy Object Từ Bucket Với Đường Dẫn Output Chỉ Định

> 🇬🇧 *By default, the file will be stored relative to the local path under its name (not the full path). To specify an output path use `--output`*

Mặc định, file được lưu theo đường dẫn tương đối tại thư mục hiện tại theo tên file (không phải đường dẫn đầy đủ). Dùng `--output` để chỉ định đường dẫn output:

```shell
nats object get myobjbucket --output /temp/Movies/NATS-logo.mov /Movies/NATS-logo.mov
```

```
1.5 GiB / 1.5 GiB [====================================================================================]

Wrote: 1.5 GiB to /temp/Movies/NATS-logo.mov in 5.68s average 279 MiB/s
```

## Xóa Object Khỏi Bucket

```shell
nats object rm myobjbucket ~/Movies/NATS-logo.mov
```

```
? Delete 1.5 GiB byte file myobjbucket > /Users/jnmoyne/Movies/NATS-logo.mov? Yes
Removed myobjbucket > /Users/jnmoyne/Movies/NATS-logo.mov
myobjbucket Object Store Status

         Bucket Name: myobjbucket
            Replicas: 1
                 TTL: unlimitd
              Sealed: false
                Size: 16 MiB
  Backing Store Kind: JetStream
    JetStream Stream: OBJ_myobjbucket
```

## Xem Thông Tin Bucket

```shell
nats object info myobjbucket
```

```
myobjbucket Object Store Status

         Bucket Name: myobjbucket
            Replicas: 1
                 TTL: unlimitd
              Sealed: false
                Size: 1.6 GiB
  Backing Store Kind: JetStream
    JetStream Stream: OBJ_myobjbucket
```

## Theo Dõi Thay Đổi Trong Bucket

```shell
nats object watch myobjbucket
```

```
[2022-04-13 17:51:28] PUT myobjbucket > /Users/jnmoyne/Movies/NATS-logo.mov: 1.5 GiB bytes in 12,656 chunks
[2022-04-13 17:53:27] DEL myobjbucket > /Users/jnmoyne/Movies/NATS-logo.mov
```

### Seal Bucket

> 🇬🇧 *You can seal a bucket, meaning that no further changes are allowed on that bucket*

Có thể seal một bucket, tức là không cho phép thêm bất kỳ thay đổi nào vào bucket đó nữa:

```shell
nats object seal myobjbucket
```

```
? Really seal Bucket myobjbucket, sealed buckets can not be unsealed or modified Yes
myobjbucket has been sealed
myobjbucket Object Store Status

         Bucket Name: myobjbucket
            Replicas: 1
                 TTL: unlimitd
              Sealed: true
                Size: 1.6 GiB
  Backing Store Kind: JetStream
    JetStream Stream: OBJ_myobjbucket
```

## Xóa Bucket

> 🇬🇧 *Using `nats object rm myobjbucket` will delete the bucket and all the files stored in it.*

Dùng `nats object rm myobjbucket` để xóa bucket cùng toàn bộ file đang lưu trong đó.

## Thuật ngữ trong bài

- **stream**: luồng message lưu trữ liên tục