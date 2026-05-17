---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/jetstream/example_configuration
title: Ví dụ cấu hình
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Ví dụ cấu hình

> 🇬🇧 *Consider this architecture*

Xét kiến trúc sau:

![Orders](<../../.gitbook/assets/streams-and-consumers-75p (1).png>)

> 🇬🇧 *While it is an incomplete architecture it does show a number of key points:*
> 
> *- Many related subjects are stored in a Stream*
> *- Consumers can have different modes of operation and receive just subsets of the messages*
> *- Multiple Acknowledgement modes are supported*

Dù chưa hoàn chỉnh, kiến trúc này thể hiện một số điểm quan trọng:

* Nhiều subject (chuỗi định danh message) liên quan được lưu trong một Stream (luồng message lưu trữ liên tục)
* Consumer (bên xử lý dữ liệu từ stream) có thể hoạt động theo các chế độ khác nhau và chỉ nhận một tập con của các message
* Hỗ trợ nhiều chế độ Acknowledgement khác nhau

> 🇬🇧 *A new order arrives on `ORDERS.received`, gets sent to the `NEW` Consumer who, on success, will create a new message on `ORDERS.processed`. The `ORDERS.processed` message again enters the Stream where a `DISPATCH` Consumer receives it and once processed it will create an `ORDERS.completed` message which will again enter the Stream. These operations are all `pull` based meaning they are work queues and can scale horizontally. All require acknowledged delivery ensuring no order is missed.*

Một đơn hàng mới đến `ORDERS.received`, được gửi tới Consumer `NEW`, khi thành công sẽ tạo một message mới trên `ORDERS.processed`. Message `ORDERS.processed` lại đi vào Stream, Consumer `DISPATCH` nhận nó và sau khi xử lý sẽ tạo message `ORDERS.completed` tiếp tục đi vào Stream. Tất cả các thao tác này đều dựa trên `pull`, nghĩa là chúng hoạt động như work queue và có thể scale theo chiều ngang. Tất cả đều yêu cầu acknowledged delivery để đảm bảo không bỏ sót đơn hàng nào.

> 🇬🇧 *All messages are delivered to a `MONITOR` Consumer without any acknowledgement and using Pub/Sub semantics - they are pushed to the monitor.*

Tất cả message được giao tới Consumer `MONITOR` mà không cần acknowledgement, theo ngữ nghĩa Pub/Sub — chúng được đẩy tới hệ thống giám sát.

> 🇬🇧 *As messages are acknowledged to the `NEW` and `DISPATCH` Consumers, a percentage of them are Sampled and messages indicating redelivery counts, ack delays and more, are delivered to the monitoring system.*

Khi message được acknowledged tới Consumer `NEW` và `DISPATCH`, một phần trong số đó được Sampled và các message chứa thông tin về số lần re-delivery, độ trễ ack, v.v. sẽ được gửi tới hệ thống giám sát.

## Cấu hình ví dụ

> 🇬🇧 *[Additional documentation](../../running-a-nats-service/configuration/clustering/jetstream_clustering/administration.md) introduces the `nats` utility and how you can use it to create, monitor, and manage streams and consumers, but for completeness and reference this is how you'd create the ORDERS scenario. We'll configure a 1 year retention for order related messages:*

[Tài liệu bổ sung](../../running-a-nats-service/configuration/clustering/jetstream_clustering/administration.md) giới thiệu tiện ích `nats` và cách dùng nó để tạo, giám sát, quản lý stream và consumer. Để tham khảo đầy đủ, dưới đây là cách tạo kịch bản ORDERS với thời gian lưu trữ 1 năm cho các message liên quan đến đơn hàng:

```bash
nats stream add ORDERS --subjects "ORDERS.*" --ack --max-msgs=-1 --max-bytes=-1 --max-age=1y --storage file --retention limits --max-msg-size=-1 --discard=old
nats consumer add ORDERS NEW --filter ORDERS.received --ack explicit --pull --deliver all --max-deliver=-1 --sample 100
nats consumer add ORDERS DISPATCH --filter ORDERS.processed --ack explicit --pull --deliver all --max-deliver=-1 --sample 100
nats consumer add ORDERS MONITOR --filter '' --ack none --target monitor.ORDERS --deliver last --replay instant
```

## Thuật ngữ trong bài

- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)