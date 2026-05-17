---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nats_top
title: nats-top - Công cụ giám sát NATS server
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# nats-top

> 🇬🇧 *[nats-top](https://github.com/nats-io/nats-top) is a [top](http://man7.org/linux/man-pages/man1/top.1.html)-like tool for monitoring nats-server servers.*

[nats-top](https://github.com/nats-io/nats-top) là công cụ giám sát nats-server tương tự lệnh [top](http://man7.org/linux/man-pages/man1/top.1.html) trên Linux.

> **ℹ️ Info:**
> The `nats-top` functionality is now available in the [`nats`](https://docs.nats.io/using-nats/nats-tools/using-nats/nats-tools/nats\_cli) CLI tool using the `nats top` command.

> 🇬🇧 *The nats-top tool provides a dynamic real-time view of a NATS server. nats-top can display a variety of system summary information about the NATS server, such as subscription, pending bytes, number of messages, and more, in real time. For example:*

nats-top cung cấp giao diện theo dõi thời gian thực cho NATS server (máy chủ). Công cụ này hiển thị nhiều thông tin tổng quan như subscription, pending bytes, số lượng message (gói dữ liệu được gửi đi), và nhiều metric (số liệu đo lường) khác. Ví dụ:

```bash
nats-top
```
```text
nats-server version 0.6.4 (uptime: 31m42s)
Server:
  Load: CPU: 0.8%   Memory: 5.9M  Slow Consumers: 0
  In:   Msgs: 34.2K  Bytes: 3.0M  Msgs/Sec: 37.9  Bytes/Sec: 3389.7
  Out:  Msgs: 68.3K  Bytes: 6.0M  Msgs/Sec: 75.8  Bytes/Sec: 6779.4

Connections: 4
  HOST                 CID      SUBS    PENDING     MSGS_TO     MSGS_FROM   BYTES_TO    BYTES_FROM  LANG     VERSION SUBSCRIPTIONS
  127.0.0.1:56134      2        5       0           11.6K       11.6K       1.1M        905.1K      go       1.1.0   foo, hello
  127.0.1.1:56138      3        1       0           34.2K       0           3.0M        0           go       1.1.0    _INBOX.a96f3f6853616154d23d1b5072
  127.0.0.1:56144      4        5       0           11.2K       11.1K       873.5K      1.1M        go       1.1.0   foo, hello
  127.0.0.1:56151      5        8       0           11.4K       11.5K       1014.6K     1.0M        go       1.1.0   foo, hello
```

## Cài đặt

> 🇬🇧 *nats-top can be installed using `go install`. For example:*

nats-top có thể cài đặt bằng `go install`. Ví dụ:

```bash
go install github.com/nats-io/nats-top
```

> 🇬🇧 *With newer versions of Go, you will be required to use `go install github.com/nats-io/nats-top@latest`.*

Với các phiên bản Go mới hơn, bạn cần dùng `go install github.com/nats-io/nats-top@latest`.

> 🇬🇧 *NOTE: You may have to run the above command as user `sudo` depending on your setup. If you receive an error that you cannot install nats-top because your $GOPATH is not set, when in fact it is set, use command `sudo -E go get github.com/nats-io/nats-top` to install nats-top. The `-E` flag tells sudo to preserve the current user's environment.*

NOTE: Tùy vào cấu hình hệ thống, bạn có thể cần chạy lệnh trên với quyền `sudo`. Nếu nhận lỗi không cài được nats-top do `$GOPATH` chưa được đặt trong khi thực tế đã đặt rồi, hãy dùng lệnh `sudo -E go get github.com/nats-io/nats-top` để cài. Flag `-E` yêu cầu sudo giữ nguyên biến môi trường của user hiện tại.

## Sử dụng

> 🇬🇧 *Once installed, nats-top can be run with the command `nats-top` and optional arguments.*

Sau khi cài xong, chạy nats-top bằng lệnh `nats-top` kèm các tham số tùy chọn.

```bash
nats-top [-s server] [-m monitor] [-n num_connections] [-d delay_in_secs] [-sort by]
```

## Tùy chọn

> 🇬🇧 *Optional arguments inclde the following:*

Các tham số tùy chọn bao gồm:

| Option | Description |
| :--- | :--- |
| `-m monitor` | Monitoring http port from nats-server. |
| `-n num_connections` | Limit the connections requested to the server \(default 1024\). |
| `-d delay_in_secs` | Screen refresh interval \(default 1 second\). |
| `-sort by` | Field to use for sorting the connections \(see below\). |

## Lệnh

> 🇬🇧 *While in nats-top view, you can use the following commands.*

Trong giao diện nats-top, bạn có thể dùng các lệnh sau.

### option

> 🇬🇧 *Use the `o<option>` command to set the primary sort key to the `<option>` value. The option value can be one of the following: `cid`, `subs`, `pending`, `msgs_to`, `msgs_from`, `bytes_to`, `bytes_from`, `lang`, `version`.*

Dùng lệnh `o<option>` để đặt khóa sắp xếp chính thành giá trị `<option>`. Giá trị option có thể là một trong: `cid`, `subs`, `pending`, `msgs_to`, `msgs_from`, `bytes_to`, `bytes_from`, `lang`, `version`.

> 🇬🇧 *You can also set the sort option on the command line using the `-sort` flag. For example: `nats-top -sort bytes_to`.*

Bạn cũng có thể đặt tùy chọn sắp xếp từ command line bằng flag `-sort`. Ví dụ: `nats-top -sort bytes_to`.

### limit

> 🇬🇧 *Use the `n<limit>` command to set the sample size of connections to request from the server.*

Dùng lệnh `n<limit>` để đặt số lượng kết nối tối đa lấy từ server.

> 🇬🇧 *You can also set this on the command line using the `-n num_connections` flag. For example: `nats-top -n 1`.*

Bạn cũng có thể đặt giá trị này từ command line bằng flag `-n num_connections`. Ví dụ: `nats-top -n 1`.

> 🇬🇧 *Note that if `n<limit>` is used in conjunction with `-sort`, the server will respect both options allowing queries such as the following: Query for the connection with largest number of subscriptions: `nats-top -n 1 -sort subs`.*

Lưu ý rằng khi dùng `n<limit>` kết hợp với `-sort`, server sẽ áp dụng cả hai tùy chọn, cho phép truy vấn như: lấy kết nối có số subscription nhiều nhất: `nats-top -n 1 -sort subs`.

### Lệnh s, ? và q

> 🇬🇧 *Use the `s` command to toggle displaying connection subscriptions.*

Dùng lệnh `s` để bật/tắt hiển thị subscription của các kết nối.

> 🇬🇧 *Use the `?` command to show help message with options.*

Dùng lệnh `?` để hiển thị thông tin trợ giúp kèm các tùy chọn.

> 🇬🇧 *Use the `q` command to quit nats-top.*

Dùng lệnh `q` để thoát nats-top.

### Hướng dẫn thực hành

> 🇬🇧 *For a walkthrough with `nats-top` check out the [tutorial](./nats-top-tutorial.md).*

Để thực hành chi tiết với `nats-top`, xem [tutorial](./nats-top-tutorial.md).

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **metric**: số liệu đo lường
- **server**: máy chủ