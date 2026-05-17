---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/core-nats/request-reply/reqreply_walkthrough
title: Hướng dẫn thực hành NATS Request-Reply
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Hướng dẫn thực hành NATS Request-Reply

> 🇬🇧 *NATS supports [request-reply](./reqreply.md) messaging. In this tutorial you explore how to exchange point-to-point messages using NATS.*

NATS hỗ trợ kiểu nhắn tin request-reply. Trong hướng dẫn này, bạn sẽ tìm hiểu cách trao đổi message (gói dữ liệu được gửi đi) theo mô hình point-to-point bằng NATS.

## Điều kiện tiên quyết

> 🇬🇧 *If you have not already done so, you need to [install](../../what-is-nats/walkthrough_setup.md) the `nats` CLI Tool and optionally, the nats-server on your machine.*

Nếu chưa thực hiện, bạn cần [cài đặt](../../what-is-nats/walkthrough_setup.md) CLI Tool `nats` và tùy chọn cài thêm nats-server trên máy.

## Thực hành

> 🇬🇧 *Start two terminal sessions. These will be used to run the NATS request and reply clients.*

Mở hai terminal. Hai terminal này dùng để chạy NATS request client và reply client.

### Trong một terminal, chạy reply client

```bash
nats reply help.please 'OK, I CAN HELP!!!'
```

> 🇬🇧 *You should see the message: _Listening on \[help.please\]_*
>
> 🇬🇧 *This means that the NATS receiver client is listening for request messages on the "help.please" subject. In NATS, the receiver is a subscriber.*

Bạn sẽ thấy thông báo: _Listening on \[help.please\]_

Điều này có nghĩa là NATS receiver client đang lắng nghe các request message trên subject (chuỗi định danh message) "help.please". Trong NATS, receiver chính là một subscriber (bên đăng ký nhận message).

### Trong terminal còn lại, chạy request client

```bash
nats request help.please 'I need help!'
```

> 🇬🇧 *The NATS requestor client makes a request by sending the message "I need help!" on the "help.please" subject.*
>
> 🇬🇧 *The NATS receiver client receives the message, formulates the reply \("OK, I CAN HELP!!!"\), and sends it to the inbox of the requester.*

NATS requestor client gửi request bằng cách publish message "I need help!" lên subject "help.please".

NATS receiver client nhận message, tạo reply "OK, I CAN HELP!!!" và gửi về inbox của requester.

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message