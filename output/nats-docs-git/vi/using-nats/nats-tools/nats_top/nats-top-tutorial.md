---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nats_top/nats-top-tutorial
title: Hướng dẫn nats-top
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Hướng dẫn nats-top

> 🇬🇧 *You can use [nats-top](https://github.com/nats-io/nats-top) to monitor in realtime NATS server connections and message statistics.*

Bạn có thể dùng [nats-top](https://github.com/nats-io/nats-top) để theo dõi theo thời gian thực các kết nối NATS server và metric (số liệu đo lường) về message.

## Yêu cầu chuẩn bị

* [Cài đặt môi trường Go](https://golang.org/doc/install)
* [Cài đặt NATS server](../../../running-a-nats-service/installation.md)

## 1. Cài đặt nats-top

```bash
go install github.com/nats-io/nats-top@latest
```

> 🇬🇧 *You may need to run the following instead:*

Nếu lệnh trên không hoạt động, hãy thử lệnh sau:

```bash
sudo -E go install github.com/nats-io/nats-top
```

## 2. Khởi động NATS server với tính năng monitoring

```bash
nats-server -m 8222
```

## 3. Khởi động nats-top

```bash
nats-top
```

> 🇬🇧 *Result:*

Kết quả:

```text
nats-server version 0.6.6 (uptime: 2m2s)
Server:
  Load: CPU:  0.0%  Memory: 6.3M  Slow Consumers: 0
  In:   Msgs: 0  Bytes: 0  Msgs/Sec: 0.0  Bytes/Sec: 0
  Out:  Msgs: 0  Bytes: 0  Msgs/Sec: 0.0  Bytes/Sec: 0

Connections: 0
  HOST                 CID      SUBS    PENDING     MSGS_TO     MSGS_FROM   BYTES_TO    BYTES_FROM  LANG     VERSION
```

## 4. Chạy các NATS client program

> 🇬🇧 *Run some NATS client programs and exchange messages.*

Chạy một số NATS client program để gửi và nhận message.

> 🇬🇧 *For the best experience, you will want to run multiple subscribers, at least 2 or 3. Refer to the [example pub-sub clients](../../../running-a-nats-service/clients.md).*

Để có kết quả tốt nhất, hãy chạy nhiều subscriber (bên đăng ký nhận message), ít nhất 2 hoặc 3 subscriber. Tham khảo [ví dụ pub-sub client](../../../running-a-nats-service/clients.md).

## 5. Kiểm tra thống kê trong nats-top

```text
nats-server version 0.6.6 (uptime: 30m51s)
Server:
  Load: CPU:  0.0%  Memory: 10.3M  Slow Consumers: 0
  In:   Msgs: 56  Bytes: 302  Msgs/Sec: 0.0  Bytes/Sec: 0
  Out:  Msgs: 98  Bytes: 512  Msgs/Sec: 0.0  Bytes/Sec: 0

Connections: 3
  HOST                 CID      SUBS    PENDING     MSGS_TO     MSGS_FROM   BYTES_TO    BYTES_FROM  LANG     VERSION
  ::1:58651            6        1       0           52          0           260         0           go       1.1.0
  ::1:58922            38       1       0           21          0           105         0           go       1.1.0
  ::1:58953            39       1       0           21          0           105         0           go       1.1.0
```

## 6. Sắp xếp thống kê trong nats-top

> 🇬🇧 *In nats-top, enter the command `o` followed by the option, such as `bytes_to`. You see that nats-top sorts the BYTES_TO column in ascending order.*

Trong nats-top, nhập lệnh `o` kèm theo tùy chọn, ví dụ `bytes_to`. nats-top sẽ sắp xếp cột BYTES_TO theo thứ tự tăng dần.

```text
nats-server version 0.6.6 (uptime: 45m40s)
Server:
  Load: CPU:  0.0%  Memory: 10.4M  Slow Consumers: 0
  In:   Msgs: 81  Bytes: 427  Msgs/Sec: 0.0  Bytes/Sec: 0
  Out:  Msgs: 154  Bytes: 792  Msgs/Sec: 0.0  Bytes/Sec: 0
sort by [bytes_to]:
Connections: 3
  HOST                 CID      SUBS    PENDING     MSGS_TO     MSGS_FROM   BYTES_TO    BYTES_FROM  LANG     VERSION
  ::1:59259            83       1       0           4           0           20          0           go       1.1.0
  ::1:59349            91       1       0           2           0           10          0           go       1.1.0
  ::1:59342            90       1       0           0           0           0           0           go       1.1.0
```

## 7. Thử các tùy chọn sắp xếp khác

> 🇬🇧 *Use some different sort options to explore nats-top, such as:*

Thử các tùy chọn sắp xếp khác để khám phá nats-top, ví dụ:

`cid`, `subs`, `pending`, `msgs_to`, `msgs_from`, `bytes_to`, `bytes_from`, `lang`, `version`

> 🇬🇧 *You can also set the sort option on the command line using the `-sort` flag. For example: `nats-top -sort bytes_to`.*

Bạn cũng có thể đặt tùy chọn sắp xếp trực tiếp từ command line bằng flag `-sort`. Ví dụ: `nats-top -sort bytes_to`.

## 8. Hiển thị các subscription đã đăng ký

> 🇬🇧 *In nats-top, enter the command `s` to toggle displaying connection subscriptions. When enabled, you see the subscription subject in nats-top table:*

Trong nats-top, nhập lệnh `s` để bật/tắt hiển thị subscription của kết nối. Khi bật, bạn sẽ thấy subject (chuỗi định danh message) của subscription xuất hiện trong bảng nats-top:

```text
nats-server version 0.6.6 (uptime: 1h2m23s)
Server:
  Load: CPU:  0.0%  Memory: 10.4M  Slow Consumers: 0
  In:   Msgs: 108  Bytes: 643  Msgs/Sec: 0.0  Bytes/Sec: 0
  Out:  Msgs: 185  Bytes: 1.0K  Msgs/Sec: 0.0  Bytes/Sec: 0

Connections: 3
  HOST                 CID      SUBS    PENDING     MSGS_TO     MSGS_FROM   BYTES_TO    BYTES_FROM  LANG     VERSION SUBSCRIPTIONS
  ::1:59708            115      1       0           6           0           48          0           go       1.1.0   foo.bar
  ::1:59758            122      1       0           1           0           8           0           go       1.1.0   foo
  ::1:59817            124      1       0           0           0           0           0           go       1.1.0   foo
```

## 9. Thoát nats-top

> 🇬🇧 *Use the `q` command to quit nats-top.*

Dùng lệnh `q` để thoát nats-top.

## 10. Khởi động lại nats-top với một truy vấn cụ thể

> 🇬🇧 *For example, to query for the connection with largest number of subscriptions:*

Ví dụ, để truy vấn kết nối có số lượng subscription lớn nhất:

```bash
nats-top -n 1 -sort subs
```

> 🇬🇧 *Result: nats-top displays only the client connection with the largest number of subscriptions:*

Kết quả: nats-top chỉ hiển thị kết nối client có số lượng subscription lớn nhất:

```text
nats-server version 0.6.6 (uptime: 1h7m0s)
Server:
  Load: CPU:  0.0%  Memory: 10.4M  Slow Consumers: 0
  In:   Msgs: 109  Bytes: 651  Msgs/Sec: 0.0  Bytes/Sec: 0
  Out:  Msgs: 187  Bytes: 1.0K  Msgs/Sec: 0.0  Bytes/Sec: 0

Connections: 3
  HOST                 CID      SUBS    PENDING     MSGS_TO     MSGS_FROM   BYTES_TO    BYTES_FROM  LANG     VERSION
  ::1:59708            115      1       0           6           0           48          0           go       1.1.0
```

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **metric**: số liệu đo lường
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message