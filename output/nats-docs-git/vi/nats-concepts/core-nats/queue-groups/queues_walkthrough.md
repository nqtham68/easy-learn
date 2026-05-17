---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/core-nats/queue-groups/queues_walkthrough
title: Hướng dẫn NATS Queueing
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Hướng dẫn NATS Queueing

> 🇬🇧 *NATS supports a form of load balancing using [queue groups](./queue.md). Subscribers register a queue group name. A single subscriber in the group is randomly selected to receive the message.*

NATS hỗ trợ cân bằng tải thông qua [queue groups](./queue.md). Subscriber (bên đăng ký nhận message) đăng ký tên queue group (nhóm subscribers chia sẻ tải). Mỗi lần có message đến, hệ thống chọn ngẫu nhiên một subscriber trong nhóm để xử lý.

## Yêu cầu trước khi bắt đầu

> 🇬🇧 *If you have not already done so, you need to [install](../../what-is-nats/walkthrough_setup.md) the `nats` CLI tool and optionally the nats-server on your machine.*

Nếu chưa cài đặt, bạn cần [cài đặt](../../what-is-nats/walkthrough_setup.md) công cụ CLI `nats` và tùy chọn nats-server trên máy.

### 1. Khởi động thành viên đầu tiên của queue group

> 🇬🇧 *The `nats reply` instances don't just subscribe to the subject but also automatically join a queue group (`"NATS-RPLY-22"` by default)*

Các instance `nats reply` không chỉ subscribe vào subject (chuỗi định danh message) mà còn tự động tham gia queue group (mặc định là `"NATS-RPLY-22"`).

```bash
nats reply foo "service instance A Reply# {{Count}}"
```

### 2. Khởi động thành viên thứ hai của queue group

> 🇬🇧 *In a new window*

Mở cửa sổ mới.

```bash
nats reply foo "service instance B Reply# {{Count}}"
```

### 3. Khởi động thành viên thứ ba của queue group

> 🇬🇧 *In a new window*

Mở cửa sổ mới.

```bash
nats reply foo "service instance C Reply# {{Count}}"
```

### 4. Publish một NATS message

```bash
nats request foo "Simple request"
```

### 5. Xác nhận việc gửi và nhận message

> 🇬🇧 *You should see that only one of the my-queue group subscribers receives the message and replies to it, and you can also see which one of the available queue group subscribers processed the request from the reply message received (i.e. service instance A, B or C)*

Chỉ một subscriber trong nhóm my-queue nhận message và phản hồi. Từ reply message nhận được, bạn có thể xác định instance nào trong queue group đã xử lý request (instance A, B hoặc C).

### 6. Publish thêm message

```bash
nats request foo "Another simple request"
```

> 🇬🇧 *You should see that a different queue group subscriber receives the message this time, chosen at random among the 3 queue group members.*

Lần này một subscriber khác trong queue group sẽ nhận message, được chọn ngẫu nhiên trong số 3 thành viên.

> 🇬🇧 *You can also send any number of requests back-to-back. From the received messages, you'll see the distribution of those requests amongst the members of the queue group. For example: `nats request foo --count 10 "Request {{Count}}"`*

Bạn cũng có thể gửi nhiều request liên tiếp và quan sát cách các request được phân phối cho từng thành viên của queue group. Ví dụ: `nats request foo --count 10 "Request {{Count}}"`

### 7. Dừng/khởi động lại thành viên queue group

> 🇬🇧 *You can at any time start yet another service instance, or stop one and see how the queue group automatically takes care of adding/removing those instances from the group.*

Bạn có thể thêm hoặc dừng một service instance bất kỳ lúc nào. Queue group tự động xử lý việc thêm/xóa các instance đó khỏi nhóm mà không cần cấu hình thêm.

## Xem thêm

> 🇬🇧 *Queue groups using the NATS CLI*

Queue groups sử dụng NATS CLI

[Queue Groups NATS CLI](https://youtu.be/jLTVhP08Tq0?t=101)

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **publisher**: bên gửi message
- **queue group**: nhóm subscribers chia sẻ tải
- **request**: yêu cầu
- **service**: dịch vụ
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message