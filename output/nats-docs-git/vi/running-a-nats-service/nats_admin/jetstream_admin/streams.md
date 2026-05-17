---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/jetstream_admin/streams
title: Quản lý Stream trong JetStream
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Quản lý Stream trong JetStream

> 🇬🇧 *The first step is to set up storage for our `ORDERS` related messages, these arrive on a wildcard of subjects all flowing into the same Stream and they are kept for 1 year.*

Bước đầu tiên là thiết lập bộ nhớ lưu trữ cho các message liên quan đến `ORDERS`. Các message này đến qua wildcard của nhiều subject (chuỗi định danh message) khác nhau, tất cả đều đổ vào cùng một stream (luồng message lưu trữ liên tục) và được giữ trong 1 năm.

## Tạo Stream

> 🇬🇧 *You can get prompted interactively for missing information as above, or do it all on one command. Pressing `?` in the CLI will help you map prompts to CLI options:*

```shell
nats str add ORDERS
```
```text
? Subjects to consume ORDERS.*
? Storage backend file
? Retention Policy Limits
? Discard Policy Old
? Message count limit -1
? Message size limit -1
? Maximum message age limit 1y
? Maximum individual message size [? for help] (-1) -1
Stream ORDERS was created

Information for Stream ORDERS

Configuration:

             Subjects: ORDERS.*
     Acknowledgements: true
            Retention: File - Limits
             Replicas: 1
     Maximum Messages: -1
        Maximum Bytes: -1
          Maximum Age: 8760h0m0s
 Maximum Message Size: -1
  Maximum Consumers: -1

Statistics:

            Messages: 0
               Bytes: 0 B
            FirstSeq: 0
             LastSeq: 0
    Active Consumers: 0
```

Có thể nhập thông tin theo từng bước như trên, hoặc thực hiện toàn bộ bằng một lệnh duy nhất. Nhấn `?` trong CLI để xem cách ánh xạ từng prompt sang CLI option:

```shell
nats str add ORDERS --subjects "ORDERS.*" --ack --max-msgs=-1 --max-bytes=-1 --max-age=1y --storage file --retention limits --max-msg-size=-1 --discard old --dupe-window="0s" --replicas 1
```

> 🇬🇧 *Additionally one can store the configuration in a JSON file, the format of this is the same as `$ nats str info ORDERS -j | jq .config`:*

Ngoài ra, có thể lưu config (cấu hình) trong file JSON với định dạng giống `$ nats str info ORDERS -j | jq .config`:

```shell
nats str add ORDERS --config orders.json
```

## Liệt Kê Stream

> 🇬🇧 *We can confirm our Stream was created:*

Kiểm tra xác nhận stream đã được tạo:

```shell
nats str ls
```
```text
Streams:

    ORDERS
```

## Truy Vấn Stream

> 🇬🇧 *Information about the configuration of the Stream can be seen, and if you did not specify the Stream like below, it will prompt you based on all known ones:*

Xem thông tin config của stream. Nếu không chỉ định tên stream như bên dưới, CLI sẽ hiển thị danh sách để chọn:

```shell
nats str info ORDERS
```
```text
Information for Stream ORDERS created 2021-02-27T16:49:36-07:00

Configuration:

             Subjects: ORDERS.*
     Acknowledgements: true
            Retention: File - Limits
             Replicas: 1
       Discard Policy: Old
     Duplicate Window: 2m0s
     Maximum Messages: unlimited
        Maximum Bytes: unlimited
          Maximum Age: 1y0d0h0m0s
 Maximum Message Size: unlimited
    Maximum Consumers: unlimited

State:

             Messages: 0
                Bytes: 0 B
             FirstSeq: 0
              LastSeq: 0
     Active Consumers: 0
```

> 🇬🇧 *Most commands that show data as above support `-j` to show the results as JSON:*

Hầu hết các lệnh hiển thị dữ liệu như trên đều hỗ trợ `-j` để xuất kết quả dưới dạng JSON:

```shell
nats str info ORDERS -j
```
```json
{
  "config": {
    "name": "ORDERS",
    "subjects": [
      "ORDERS.*"
    ],
    "retention": "limits",
    "max_consumers": -1,
    "max_msgs": -1,
    "max_bytes": -1,
    "max_age": 31536000000000000,
    "max_msg_size": -1,
    "storage": "file",
    "discard": "old",
    "num_replicas": 1,
    "duplicate_window": 120000000000
  },
  "created": "2021-02-27T23:49:36.700424Z",
  "state": {
    "messages": 0,
    "bytes": 0,
    "first_seq": 0,
    "first_ts": "0001-01-01T00:00:00Z",
    "last_seq": 0,
    "last_ts": "0001-01-01T00:00:00Z",
    "consumer_count": 0
  }
}
```

> 🇬🇧 *This is the general pattern for the entire `nats` utility as it relates to JetStream - prompting for needed information but every action can be run non-interactively making it usable as a CLI API. All information output like seen above can be turned into JSON using `-j`.*

Đây là cách hoạt động chung của toàn bộ tiện ích `nats` đối với JetStream — hiển thị prompt để hỏi thông tin cần thiết, nhưng mọi thao tác đều có thể chạy non-interactive để dùng như một CLI API. Toàn bộ output như trên đều có thể chuyển sang JSON bằng `-j`.

## Sao Chép Stream

> 🇬🇧 *A stream can be copied into another, which also allows the configuration of the new one to be adjusted via CLI flags:*

Có thể sao chép một stream sang stream khác, đồng thời điều chỉnh config của stream mới qua các CLI flag:

```shell
nats str cp ORDERS ARCHIVE --subjects "ORDERS_ARCHIVE.*" --max-age 2y
```
```text
Stream ORDERS was created

Information for Stream ORDERS created 2021-02-27T16:52:46-07:00

Configuration:

             Subjects: ORDERS_ARCHIVE.*
     Acknowledgements: true
            Retention: File - Limits
             Replicas: 1
       Discard Policy: Old
     Duplicate Window: 2m0s
     Maximum Messages: unlimited
        Maximum Bytes: unlimited
          Maximum Age: 2y0d0h0m0s
 Maximum Message Size: unlimited
    Maximum Consumers: unlimited

State:

             Messages: 0
                Bytes: 0 B
             FirstSeq: 0
              LastSeq: 0
     Active Consumers: 0
```

## Chỉnh Sửa Stream

> 🇬🇧 *A stream configuration can be edited, which allows the configuration to be adjusted via CLI flags. Here I have an incorrectly created ORDERS stream that I fix:*

Config của stream có thể được chỉnh sửa qua các CLI flag. Ví dụ dưới đây sửa stream ORDERS được tạo sai:

```shell
nats str info ORDERS -j | jq .config.subjects
```
```text
[
  "ORDERS.new"
]
```

> 🇬🇧 *Change the subjects for the stream*

Thay đổi subject của stream:

```shell
nats str edit ORDERS --subjects "ORDERS.*"
```
```text
Stream ORDERS was updated

Information for Stream ORDERS

Configuration:

             Subjects: ORDERS.*
....
```

> 🇬🇧 *Additionally, one can store the configuration in a JSON file, the format of this is the same as `$ nats str info ORDERS -j | jq .config`:*

Ngoài ra, có thể lưu config trong file JSON với định dạng giống `$ nats str info ORDERS -j | jq .config`:

```shell
nats str edit ORDERS --config orders.json
```

## Publish Vào Stream

> 🇬🇧 *Now let's add some messages to our Stream. You can use `nats pub` to add messages, pass the `--wait` flag to see the publish ack being returned.*

Thêm message vào stream bằng `nats pub`. Truyền flag `--wait` để xem publish ack được trả về.

> 🇬🇧 *You can publish without waiting for acknowledgement:*

Publish (bên gửi message) mà không cần chờ xác nhận:

```shell
nats pub ORDERS.scratch hello
```

> 🇬🇧 *But if you want to be sure your messages got to JetStream and were persisted you can make a request:*

Nếu muốn đảm bảo message đã được JetStream nhận và lưu trữ, hãy thực hiện request:

```shell
nats req ORDERS.scratch hello
```
```text
13:45:03 Sending request on [ORDERS.scratch]
13:45:03 Received on [_INBOX.M8drJkd8O5otORAo0sMNkg.scHnSafY]: '+OK'
```

> 🇬🇧 *Keep checking the status of the Stream while doing this and you'll see its stored messages increase.*

Theo dõi trạng thái của stream trong quá trình này, số message được lưu sẽ tăng dần.

```shell
nats str info ORDERS
```
```text
Information for Stream ORDERS
...
Statistics:

            Messages: 3
               Bytes: 147 B
            FirstSeq: 1
             LastSeq: 3
    Active Consumers: 0
```

> 🇬🇧 *After putting some throwaway data into the Stream, we can purge all the data out - while keeping the Stream active:*

Sau khi đưa dữ liệu thử vào stream, có thể xóa sạch toàn bộ dữ liệu trong khi vẫn giữ stream hoạt động:

## Xóa Toàn Bộ Dữ Liệu

> 🇬🇧 *To delete all data in a stream use `purge`:*

Dùng `purge` để xóa toàn bộ dữ liệu trong stream:

```shell
nats str purge ORDERS -f
```
```text
...
State:

            Messages: 0
               Bytes: 0 B
            FirstSeq: 1,000,001
             LastSeq: 1,000,000
    Active Consumers: 0
```

## Xóa Một Message

> 🇬🇧 *A single message can be securely removed from the stream:*

Một message đơn lẻ có thể được xóa an toàn khỏi stream:

```shell
nats str rmm ORDERS 1 -f
```

## Xóa Stream

> 🇬🇧 *Finally, for demonstration purposes, you can also delete the whole Stream and recreate it. Then we're ready for creating the Consumers:*

Cuối cùng, để minh họa, có thể xóa toàn bộ stream và tạo lại từ đầu. Sau đó ta sẵn sàng tạo consumer:

```shell
nats str rm ORDERS -f
nats str add ORDERS --subjects "ORDERS.*" --ack --max-msgs=-1 --max-bytes=-1 --max-age=1y --storage file --retention limits --max-msg-size=-1 --discard old --dupe-window="0s" --replicas 1
```

## Thuật ngữ trong bài

- **CLI**: công cụ dòng lệnh
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **request**: yêu cầu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)