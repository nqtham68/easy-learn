---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/jetstream_admin/naming
title: Đặt tên cho Stream, Consumer và Account
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Đặt tên cho Stream, Consumer và Account

> 🇬🇧 *Stream, Consumer (durable name), and Account names are used in both the subject namespace used by JetStream and the filesystem backing JetStream persistence. This means that when naming streams, consumers, and accounts, names must adhere to subject naming rules as well as being friendly to the file system.*

Tên của stream (luồng message lưu trữ liên tục), consumer (bên xử lý dữ liệu từ stream) và Account được dùng trong cả không gian subject (chuỗi định danh message) của JetStream lẫn hệ thống file lưu trữ JetStream. Do đó, khi đặt tên cho stream, consumer và account, tên phải tuân theo quy tắc đặt tên subject và phải tương thích với hệ thống file.

> 🇬🇧 *We recommend the following guideline for stream, consumer, and account names:*

Khuyến nghị áp dụng các quy tắc sau khi đặt tên cho stream, consumer và account:

> 🇬🇧 *Alphanumeric values are recommended. Spaces, tabs, period (`.`), greater than (`>`) or asterisk (`*`) are prohibited. Path separators (i.e. forward slash and backward slash) are prohibited. Limit name length: The JetStream storage directories will include the account, stream name, and consumer name, so a generally safe approach would be to keep names under 32 characters. Do not use reserved file names like NUL, LPT1, etc. Be aware that some file systems are case insensitive so do not use stream or account names that would collide in a file system. For example, `Foo` and `foo` would collide on a Windows or Mac OSx System.*

* Nên dùng ký tự chữ-số (alphanumeric).
* Không dùng: khoảng trắng, tab, dấu chấm (`.`), dấu lớn hơn (`>`) hoặc dấu hoa thị (`*`).
* Không dùng ký tự phân cách đường dẫn (dấu gạch chéo xuôi và ngược).
* Giới hạn độ dài tên: thư mục lưu trữ JetStream bao gồm account, tên stream và tên consumer, vì vậy nên giữ tên **dưới 32 ký tự** để an toàn.
* Không dùng tên file hệ thống dành riêng như NUL, LPT1, v.v.
* Lưu ý rằng một số hệ thống file không phân biệt hoa/thường — tránh đặt tên stream hay account có thể bị trùng khi so sánh không phân biệt hoa/thường. Ví dụ: `Foo` và `foo` sẽ bị trùng trên Windows hoặc Mac OSX.

> 🇬🇧 *We plan to address these limitations in a future release.*

Các giới hạn này dự kiến sẽ được giải quyết trong phiên bản tới.

## Thuật ngữ trong bài

- **consumer**: bên xử lý dữ liệu từ stream
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)