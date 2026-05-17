---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/jetstream-config/resource_management
title: Cấu hình JetStream
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Cấu hình JetStream

### Bật JetStream cho nats-server

> 🇬🇧 *To enable JetStream in a server we have to configure it at the top level first:*

Để bật JetStream trên server, cần cấu hình ở cấp top-level trước:

```
jetstream: enabled
```

> 🇬🇧 *You can also use the `-js, --jetstream` and `-sd, --store_dir <dir>` flags from the command line*

Ngoài ra có thể dùng flag `-js, --jetstream` và `-sd, --store_dir <dir>` từ dòng lệnh.

## Multi-tenancy & Quản lý tài nguyên

> 🇬🇧 *JetStream is compatible with NATS 2.0 Multi-Tenancy using Accounts. A JetStream enabled server supports creating fully isolated JetStream environments for different accounts.*

JetStream tương thích với Multi-Tenancy của NATS 2.0 thông qua Accounts. Server đã bật JetStream hỗ trợ tạo môi trường JetStream hoàn toàn độc lập cho từng account.

> 🇬🇧 *JetStream environments in leaf nodes should be isolated in their own JetStream domain - [Leaf nodes](../leafnodes)*

Môi trường JetStream trên leaf node nên được cô lập trong JetStream domain riêng — [Leaf nodes](../leafnodes).

> 🇬🇧 *This will dynamically determine the available resources. It's recommended that you set specific limits though:*

Cách này sẽ tự động xác định tài nguyên khả dụng, nhưng khuyến nghị nên đặt giới hạn cụ thể:

```
jetstream {
    store_dir: /data/jetstream
    max_mem: 1G
    max_file: 100G
    domain: acme
}
```

### Đặt giới hạn tài nguyên cho account

> 🇬🇧 *At this point JetStream will be enabled and if you have a server that does not have accounts enabled, all users in the server would have access to JetStream*

Lúc này JetStream đã được bật. Nếu server chưa kích hoạt accounts, mọi user đều có quyền truy cập JetStream.

```
jetstream {
    store_dir: /data/jetstream
    max_mem: 1G
    max_file: 100G
}

accounts {
    HR: {
        jetstream: enabled
    }
}
```

> 🇬🇧 *Here the `HR` account would have access to all the resources configured on the server, we can restrict it:*

Trong ví dụ này, account `HR` có quyền truy cập toàn bộ tài nguyên trên server. Có thể giới hạn lại như sau:

```
jetstream {
    store_dir: /data/jetstream
    max_mem: 1G
    max_file: 100G
}

accounts {
    HR: {
        jetstream {
            max_mem: 512M
            max_file: 1G
            max_streams: 10
            max_consumers: 100
        }
    }
}
```

> 🇬🇧 *Now the `HR` account is limited in various dimensions.*

Giờ account `HR` đã bị giới hạn ở nhiều chiều tài nguyên khác nhau.

> 🇬🇧 *If you try to configure JetStream for an account without enabling it globally you'll get a warning and the account designated as System cannot have JetStream enabled.*

Nếu cố cấu hình JetStream cho một account mà chưa bật globally, server sẽ báo cảnh báo. Account được chỉ định là System không thể bật JetStream.

#### Đặt giới hạn JetStream API và Max HA assets

> 🇬🇧 *Since version v2.10.21, the NATS JetStream API has a limit of 10K inflight requests after which it will start to drop requests in order to protect from memory buildup and to avoid overwhelming the JetStream service. Sometimes it might be necessary to reduce the limit further in order to reduce the possibility of an increase in JetStream traffic impacting the service. Another important limit is `max_ha_assets` which would constrain the maximum number of supported R3 or R5 streams and consumers per server:*

Từ phiên bản v2.10.21, NATS JetStream API (giao diện lập trình) có giới hạn 10K inflight request. Khi vượt ngưỡng này, server sẽ bắt đầu loại bỏ request để tránh memory buildup và quá tải JetStream service. Đôi khi cần giảm giới hạn hơn nữa để hạn chế ảnh hưởng khi lưu lượng JetStream tăng đột biến. Một giới hạn quan trọng khác là `max_ha_assets`, giúp khống chế số lượng stream (luồng message lưu trữ liên tục) R3/R5 và consumer (bên xử lý dữ liệu từ stream) tối đa được hỗ trợ trên mỗi server:

Ví dụ:

```
jetstream {
  request_queue_limit: 1000
    limits {
      max_ha_assets = 2000
    }
  }
```

> 🇬🇧 *When the request limit is reached, all pending requests are dropped, therefore it may be necessary in some situations to reduce the limit further in order to lessen the impact on applications. In the logs the following would appear reporting that requests have been dropped:*

Khi đạt giới hạn request, toàn bộ request đang chờ sẽ bị loại bỏ. Trong một số tình huống, cần giảm giới hạn xuống thấp hơn để giảm thiểu ảnh hưởng lên application. Log sẽ xuất hiện thông báo như sau khi request bị loại bỏ:

```
[WRN] JetStream API queue limit reached, dropping 1000 requests
```

> 🇬🇧 *For an application, this will mean that those operations will error and will have to be retried. This will also emit an advisory under the subject `$JS.EVENT.ADVISORY.API.LIMIT_REACHED` whenever it occurs.*

Với application, điều này có nghĩa các thao tác đó sẽ báo lỗi và cần retry. Mỗi khi xảy ra, hệ thống cũng phát ra một advisory dưới subject `$JS.EVENT.ADVISORY.API.LIMIT_REACHED`.

#### Giới hạn tài nguyên account ở Operator mode dùng CLI tool `nsc`

> 🇬🇧 *If your setup is in operator mode, JetStream specific account configuration can be stored in account JWT. The earlier account named HR can be configured as follows:*

Nếu hệ thống chạy ở operator mode, cấu hình JetStream cho từng account có thể lưu trong account JWT. Account HR ở ví dụ trước có thể cấu hình như sau:

```bash
nsc add account --name HR
nsc edit account --name HR --js-mem-storage 1G --js-disk-storage 512M  --js-streams 10 --js-consumer 100
```

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **consumer**: bên xử lý dữ liệu từ stream
- **retry**: thử lại khi fail
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)