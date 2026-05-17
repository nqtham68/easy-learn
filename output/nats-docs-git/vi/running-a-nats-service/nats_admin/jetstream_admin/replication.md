---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/jetstream_admin/replication
title: Sao Chép Dữ Liệu
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Sao Chép Dữ Liệu

> 🇬🇧 *Replication allows you to move data between streams in either a 1:1 mirror style or by multiplexing multiple source streams into a new stream. In future builds this will allow data to be replicated between accounts as well, ideal for sending data from a Leafnode into a central store.*

Replication cho phép di chuyển dữ liệu giữa các stream (luồng message lưu trữ liên tục) theo kiểu mirror 1:1, hoặc ghép nhiều stream nguồn vào một stream mới. Trong các phiên bản tương lai, tính năng này sẽ hỗ trợ sao chép dữ liệu giữa các account, rất hữu ích khi cần đẩy dữ liệu từ Leafnode vào một kho lưu trữ trung tâm.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/replication.png)

> 🇬🇧 *Here we have 2 main streams - _ORDERS_ and _RETURNS_ - these streams are clustered across 3 nodes. These Streams have short retention periods and are memory based.*

Ví dụ này có 2 stream chính là _ORDERS_ và _RETURNS_, được phân tán qua cluster (cụm nhiều server chạy chung) gồm 3 node (một server trong cluster). Hai stream này có thời gian lưu giữ ngắn và lưu trên bộ nhớ RAM.

> 🇬🇧 *We create a _ARCHIVE_ stream that has 2 _sources_ set, the _ARCHIVE_ will pull data from the sources into itself. This stream has a very long retention period and is file based and replicated across 3 nodes. Additional messages can be added to the ARCHIVE by sending to it directly.*

Tiếp theo ta tạo stream _ARCHIVE_ với 2 _source_ được cấu hình sẵn — _ARCHIVE_ sẽ kéo dữ liệu từ các source về. Stream này có thời gian lưu giữ rất dài, lưu trên file, và có replica (bản sao dữ liệu) trải dài trên 3 node. Có thể thêm message vào ARCHIVE bằng cách gửi trực tiếp đến nó.

> 🇬🇧 *Finally, we create a _REPORT_ stream mirrored from _ARCHIVE_ that is not clustered and retains data for a month. The _REPORT_ Stream does not listen for any incoming messages, it can only consume data from _ARCHIVE_.*

Cuối cùng, ta tạo stream _REPORT_ được mirror từ _ARCHIVE_, không chạy theo cluster và lưu giữ dữ liệu trong 1 tháng. Stream _REPORT_ không lắng nghe message đến; nó chỉ có thể đọc dữ liệu từ _ARCHIVE_.

## Mirror

> 🇬🇧 *A _mirror_ copies data from 1 other stream, as far as possible IDs and ordering will match exactly the source. A _mirror_ does not listen on a subject for any data to be added. A _mirror_ can filter by subject and the Start Sequence and Start Time can be set. A stream can only have 1 _mirror_ and if it is a mirror it cannot also have any _source_.*

Một _mirror_ sao chép dữ liệu từ đúng 1 stream khác; ID và thứ tự message sẽ khớp với nguồn càng chính xác càng tốt. Một _mirror_ không lắng nghe trên subject nào để nhận dữ liệu mới. Có thể lọc theo subject và thiết lập Start Sequence cùng Start Time. Một stream chỉ có thể có 1 _mirror_, và nếu đã là mirror thì không thể có _source_ nào.

## Source

> 🇬🇧 *A _source_ is a stream where data is copied from, one stream can have multiple sources and will read data in from them all. The stream will also listen for messages on it's own subject. We can therefore not maintain absolute ordering, but data from 1 single source will be in the correct order but mixed in with other streams. You might also find the timestamps of streams can be older and newer mixed in together as a result.*

Một _source_ là stream mà dữ liệu được sao chép từ đó. Một stream có thể có nhiều source và sẽ đọc dữ liệu từ tất cả chúng. Stream vẫn lắng nghe message trên subject của chính nó. Do đó, không thể đảm bảo thứ tự tuyệt đối — dữ liệu từ một source đơn lẻ sẽ theo đúng thứ tự, nhưng sẽ xen lẫn với dữ liệu từ các stream khác. Timestamp của các message cũng có thể xuất hiện lẫn lộn cũ mới.

> 🇬🇧 *A Stream with sources may also listen on subjects, but could have no listening subject. When using the `nats` CLI to create sourced streams use `--subjects` to supply subjects to listen on.*

Stream có source vẫn có thể lắng nghe trên subject, hoặc cũng có thể không cần subject nào. Khi dùng CLI `nats` để tạo sourced stream, hãy dùng `--subjects` để chỉ định các subject cần lắng nghe.

> 🇬🇧 *A source can have Start Time or Start Sequence and can filter by a subject.*

Một source có thể thiết lập Start Time hoặc Start Sequence, và có thể lọc theo subject.

## Cấu Hình

> 🇬🇧 *The ORDERS and RETURNS streams as normal, I will not show how to create them.*

Stream ORDERS và RETURNS được tạo theo cách thông thường, phần này sẽ không trình bày lại.

```shell
nats s report
```
```text
Obtaining Stream stats

+---------+---------+-----------+----------+-------+------+---------+----------------------+
| Stream  | Storage | Consumers | Messages | Bytes | Lost | Deleted | Cluster              |
+---------+---------+-----------+----------+-------+------+---------+----------------------+
| ORDERS  | Memory  | 0         | 0        | 0 B   | 0    | 0       | n1-c2, n2-c2*, n3-c2 |
| RETURNS | Memory  | 0         | 0        | 0 B   | 0    | 0       | n1-c2*, n2-c2, n3-c2 |
+---------+---------+-----------+----------+-------+------+---------+----------------------+
```

> 🇬🇧 *We now add the ARCHIVE:*

Tiếp theo, thêm ARCHIVE:

```shell
nats s add ARCHIVE --source ORDERS --source RETURNS
```
```text
? Storage backend file
? Retention Policy Limits
? Discard Policy Old
? Stream Messages Limit -1
? Message size limit -1
? Maximum message age limit -1
? Maximum individual message size -1
? Duplicate tracking time window 2m0s
? Allow message Roll-ups No
? Allow message deletion Yes
? Allow purging subjects or the entire stream Yes
? Replicas 1
? Adjust source "ORDERS" start Yes
? ORDERS Source Start Sequence 0
? ORDERS Source UTC Time Stamp (YYYY:MM:DD HH:MM:SS)
? ORDERS Source Filter source by subject
? Import "ORDERS" from a different JetStream domain No
? Import "ORDERS" from a different account No
? Adjust source "RETURNS" start No
? Import "RETURNS" from a different JetStream domain No
? Import "RETURNS" from a different account No
Stream ARCHIVE was created

Information for Stream ARCHIVE created 2022-01-21T11:49:52-08:00

Configuration:

     Acknowledgements: true
            Retention: File - Limits
             Replicas: 1
       Discard Policy: Old
     Duplicate Window: 2m0s
    Allows Msg Delete: true
         Allows Purge: true
       Allows Rollups: false
     Maximum Messages: unlimited
        Maximum Bytes: unlimited
          Maximum Age: unlimited
 Maximum Message Size: unlimited
    Maximum Consumers: unlimited
              Sources: ORDERS
                       RETURNS


State:

             Messages: 0
                Bytes: 0 B
             FirstSeq: 0
              LastSeq: 0
     Active Consumers: 0
```

> 🇬🇧 *And we add the REPORT:*

Và thêm REPORT:

```shell
nats s add REPORT --mirror ARCHIVE
```
```text
? Storage backend file
? Retention Policy Limits
? Discard Policy Old
? Stream Messages Limit -1
? Message size limit -1
? Maximum message age limit -1
? Maximum individual message size -1
? Allow message Roll-ups No
? Allow message deletion Yes
? Allow purging subjects or the entire stream Yes
? Replicas 1
? Adjust mirror start No
? Import mirror from a different JetStream domain No
? Import mirror from a different account No
Stream REPORT was created

Information for Stream REPORT created 2022-01-21T11:50:55-08:00

Configuration:

     Acknowledgements: true
            Retention: File - Limits
             Replicas: 1
       Discard Policy: Old
     Duplicate Window: 2m0s
    Allows Msg Delete: true
         Allows Purge: true
       Allows Rollups: false
     Maximum Messages: unlimited
        Maximum Bytes: unlimited
          Maximum Age: unlimited
 Maximum Message Size: unlimited
    Maximum Consumers: unlimited
               Mirror: ARCHIVE


State:

             Messages: 0
                Bytes: 0 B
             FirstSeq: 0
              LastSeq: 0
     Active Consumers: 0
```

> 🇬🇧 *When configured we'll see some additional information in a `nats stream info` output:*

Sau khi cấu hình xong, sẽ thấy thêm thông tin trong output của `nats stream info`:

```shell
nats stream info ARCHIVE
``` 
Output extract
```text
...
Source Information:

          Stream Name: ORDERS
                  Lag: 0
            Last Seen: 2m23s

          Stream Name: RETURNS
                  Lag: 0
            Last Seen: 2m15s
...

$ nats stream info REPORT
...
Mirror Information:

          Stream Name: ARCHIVE
                  Lag: 0
            Last Seen: 2m35s
...
```

> 🇬🇧 *Here the `Lag` is how far behind we were reported as being last time we saw a message.*

Ở đây, `Lag` cho biết mức độ trễ được ghi nhận lần cuối khi nhận được message.

> 🇬🇧 *We can confirm all our setup using a `nats stream report`:*

Có thể xác nhận toàn bộ cấu hình bằng lệnh `nats stream report`:

```shell
nats s report
```
```text
+--------------------------------------------------------------------------------------------------------+
|                                            Stream Report                                               |
+---------+---------+-------------+-----------+----------+-------+------+---------+----------------------+
| Stream  | Storage | Replication | Consumers | Messages | Bytes | Lost | Deleted | Cluster              |
+---------+---------+-------------+-----------+----------+-------+------+---------+----------------------+
| ARCHIVE | File    | Sourced     | 1         | 0        | 0 B   | 0    | 0       | n1-c2*, n2-c2, n3-c2 |
| ORDERS  | Memory  |             | 1         | 0        | 0 B   | 0    | 0       | n1-c2, n2-c2*, n3-c2 |
| REPORT  | File    | Mirror      | 0         | 0        | 0 B   | 0    | 0       | n1-c2*               |
| RETURNS | Memory  |             | 1         | 0        | 0 B   | 0    | 0       | n1-c2, n2-c2, n3-c2* |
+---------+---------+-------------+-----------+----------+-------+------+---------+----------------------+

+---------------------------------------------------------+
|                   Replication Report                    |
+---------+--------+---------------+--------+-----+-------+
| Stream  | Kind   | Source Stream | Active | Lag | Error |
+---------+--------+---------------+--------+-----+-------+
| ARCHIVE | Source | ORDERS        | never  | 0   |       |
| ARCHIVE | Source | RETURNS       | never  | 0   |       |
| REPORT  | Mirror | ARCHIVE       | never  | 0   |       |
+---------+--------+---------------+--------+-----+-------+
```

> 🇬🇧 *We then create some data in both ORDERS and RETURNS:*

Sau đó, tạo một số dữ liệu trong cả ORDERS lẫn RETURNS:

```shell
nats req ORDERS.new "ORDER {{Count}}" --count 100
nats req RETURNS.new "RETURN {{Count}}" --count 100
```

> 🇬🇧 *We can now see from a Stream Report that the data has been replicated:*

Có thể thấy từ Stream Report rằng dữ liệu đã được sao chép thành công:

```shell
nats s report --dot replication.dot
```
```text
Obtaining Stream stats

+---------+---------+-----------+----------+---------+------+---------+----------------------+
| Stream  | Storage | Consumers | Messages | Bytes   | Lost | Deleted | Cluster              |
+---------+---------+-----------+----------+---------+------+---------+----------------------+
| ORDERS  | Memory  | 1         | 100      | 3.3 KiB | 0    | 0       | n1-c2, n2-c2*, n3-c2 |
| RETURNS | Memory  | 1         | 100      | 3.5 KiB | 0    | 0       | n1-c2*, n2-c2, n3-c2 |
| ARCHIVE | File    | 1         | 200      | 27 KiB  | 0    | 0       | n1-c2, n2-c2, n3-c2* |
| REPORT  | File    | 0         | 200      | 27 KiB  | 0    | 0       | n1-c2*               |
+---------+---------+-----------+----------+---------+------+---------+----------------------+

+---------------------------------------------------------+
|                   Replication Report                    |
+---------+--------+---------------+--------+-----+-------+
| Stream  | Kind   | Source Stream | Active | Lag | Error |
+---------+--------+---------------+--------+-----+-------+
| ARCHIVE | Source | ORDERS        | 14.48s | 0   |       |
| ARCHIVE | Source | RETURNS       | 9.83s  | 0   |       |
| REPORT  | Mirror | ARCHIVE       | 9.82s  | 0   |       |
+---------+--------+---------------+--------+-----+-------+
```

> 🇬🇧 *Here we also pass the `--dot replication.dot` argument that writes a GraphViz format map of the replication setup.*

Ở đây ta cũng truyền tham số `--dot replication.dot` để xuất bản đồ cấu hình replication theo định dạng GraphViz.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/replication-setup.png)

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **message**: gói dữ liệu được gửi đi
- **node**: một server trong cluster
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)