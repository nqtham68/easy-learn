---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/auth_timeout
title: Thời Gian Chờ Xác Thực
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Thời Gian Chờ Xác Thực

> 🇬🇧 *You can specify a timeout to limit how long the server will wait for a client to authenticate.*

Bạn có thể chỉ định một timeout (thời gian chờ tối đa) để giới hạn thời gian server chờ client xác thực.

> 🇬🇧 *If you don't specify a value, or if you specify the value "0", then the default will be 1 second more than the `tls_timeout`.*

Nếu không chỉ định giá trị, hoặc chỉ định giá trị "0", mặc định sẽ là 1 giây nhiều hơn `tls_timeout`.

> 🇬🇧 *If you do specify an invalid value, it will use a default of 1 second.*

Nếu chỉ định giá trị không hợp lệ, server sẽ dùng mặc định là 1 giây.

> 🇬🇧 *If a client doesn't authenticate to the server within the specified time, the server disconnects the server to prevent abuses.*

Nếu client không xác thực trong thời gian cho phép, server sẽ ngắt kết nối để ngăn chặn lạm dụng.

> 🇬🇧 *Timeouts are specified in seconds (and can be fractional). Unlike `tls_timeout`, you cannot use "human readable" values like `10s`, you must specify a number, which will be interpreted as seconds. `10` will be 10 seconds, `3.5` will be 3 seconds and 500 milliseconds, etc.*

Timeout được tính bằng giây (có thể dùng số thập phân). Khác với `tls_timeout`, bạn không thể dùng giá trị dạng "human readable" như `10s` — phải chỉ định một con số, được hiểu là giây. Ví dụ: `10` là 10 giây, `3.5` là 3 giây 500 milliseconds, v.v.

> 🇬🇧 *As with TLS timeouts, long timeouts can be an opportunity for abuse. If setting the authentication timeout, it is important to note that it should be longer than the `tls timeout` option, as the authentication timeout includes the TLS upgrade time.*

Giống như timeout của TLS (mã hóa TLS), timeout xác thực quá dài có thể tạo cơ hội cho kẻ tấn công lạm dụng. Khi cấu hình authentication timeout, cần lưu ý rằng giá trị này phải lớn hơn tùy chọn `tls timeout`, vì authentication timeout bao gồm cả thời gian nâng cấp TLS.

```
authorization: {
    timeout: 3
    users: [
        {user: a, password b},
        {user: b, password a}
    ]
}
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **server**: máy chủ
- **timeout**: thời gian chờ tối đa
- **TLS**: mã hóa TLS