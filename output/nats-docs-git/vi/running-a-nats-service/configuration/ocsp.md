---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/ocsp
title: OCSP Stapling
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# OCSP Stapling

_Hỗ trợ từ NATS Server phiên bản 2.3_

> 🇬🇧 *[OCSP Stapling](https://en.wikipedia.org/wiki/OCSP_stapling) is honored by default for certificates that have the [status_request Must-Staple flag](https://datatracker.ietf.org/doc/html/rfc6961).*

[OCSP Stapling](https://en.wikipedia.org/wiki/OCSP_stapling) được kích hoạt mặc định cho các certificate có [cờ Must-Staple status_request](https://datatracker.ietf.org/doc/html/rfc6961).

> 🇬🇧 *When a certificate is configured with OCSP Must-Staple, the NATS Server will fetch staples from the configured OCSP responder URL that is present in a certificate. For example, given a certificate with the following configuration:*

Khi certificate được cấu hình với OCSP Must-Staple, NATS Server sẽ tải staple từ OCSP responder URL có trong certificate. Ví dụ, với certificate có config (cấu hình) như sau:

```text
[ ext_ca ]
...                                                                           
authorityInfoAccess = OCSP;URI:http://ocsp.example.net:80
tlsfeature = status_request
...
```

> 🇬🇧 *The NATS server will make a request to the OCSP responder to fetch a new staple which will then be presented to any TLS connection that is accepted by the server during the TLS handshake.*

NATS Server sẽ gửi request tới OCSP responder để lấy staple mới. Staple này sau đó được trình bày cho mọi kết nối TLS (mã hóa TLS) mà server chấp nhận trong quá trình TLS handshake.

> 🇬🇧 *OCSP Stapling can be explicitly enabled or disabled in the NATS Server by setting the following flag in the NATS configuration file at the top-level:*

OCSP Stapling có thể được bật hoặc tắt tường minh trong NATS Server bằng cách thiết lập flag sau trong file config NATS ở cấp cao nhất:

```text
ocsp: false
```

> 🇬🇧 ***Note**: When OCSP Stapling is disabled, the NATS Server will not request staples even if the certificate has the Must-Staple flag.*

**Lưu ý**: Khi OCSP Stapling bị tắt, NATS Server sẽ không yêu cầu staple dù certificate có cờ Must-Staple.

## Cấu hình nâng cao

> 🇬🇧 *By default, the NATS Server will be running in OCSP `auto` mode. In this mode the server will only fetch staples when the Must-Staple flag is configured in the certificate.*

Mặc định, NATS Server chạy ở chế độ OCSP `auto`. Ở chế độ này, server chỉ tải staple khi certificate có cờ Must-Staple.

> 🇬🇧 *There are other OCSP modes that control the behavior as to whether OCSP should be enforced and the server should shutdown if the certificate runs with a revoked staple:*

Có các chế độ OCSP khác kiểm soát hành vi — liệu OCSP có bị bắt buộc không và server có nên tắt khi certificate chạy với staple bị thu hồi không:

| Mode | Mô tả | Server tắt khi bị thu hồi |
| :--- | :--- | :--- |
| auto | Kích hoạt OCSP Stapling khi certificate có cờ must staple/status_request | Không |
| must | Kích hoạt OCSP Stapling khi certificate có cờ must staple/status_request | Có |
| always | Kích hoạt OCSP Stapling cho tất cả certificate | Có |
| never | Tắt OCSP Stapling dù có cờ must staple \(tương đương `ocsp: false`\) | Không |

> 🇬🇧 *For example, in the following OCSP configuration, the mode is set to `must`. This means that staples will be fetched only for certificates that have the Must-Staple flag enabled as well, but in case of revocation the server will shutdown rather than run with a revoked staple.*
> *In this configuration, the `url` will also override the OCSP responder URL that may have been configured in the certificate.*

Ví dụ, trong cấu hình OCSP sau, mode được đặt là `must`. Điều này có nghĩa là staple chỉ được tải cho các certificate có cờ Must-Staple, nhưng khi bị thu hồi, server sẽ tắt thay vì tiếp tục chạy với staple không hợp lệ.
Trong cấu hình này, `url` cũng sẽ ghi đè OCSP responder URL có thể đã được cấu hình trong certificate.

```text
ocsp {
  mode: must
  url: "http://ocsp.example.net"
}
```

> 🇬🇧 *If staples are always required, regardless of the configuration of the certificate, you can enforce the behavior as follows:*

Nếu luôn yêu cầu staple bất kể cấu hình certificate, có thể ép buộc hành vi này như sau:

```text
ocsp {
  mode: always
  url: "http://ocsp.example.net"
}
```

## Lưu cache Staple

> 🇬🇧 *When a `store_dir` is configured in the NATS Server, the directory will be used to cache staples on disk to allow the server to resume in case of restarts without having to make another request to the OCSP responder if the staple is still valid.*

Khi `store_dir` được cấu hình trong NATS Server, thư mục đó sẽ được dùng để cache (bộ nhớ đệm) staple xuống disk, giúp server khởi động lại mà không cần gọi lại OCSP responder nếu staple vẫn còn hiệu lực.

```text
ocsp: true

store_dir: "/path/to/store/dir"

tls {
    cert_file: "configs/certs/ocsp/server-status-request-url.pem"
    key_file: "configs/certs/ocsp/server-status-request-url-key.pem"
    ca_file: "configs/certs/ocsp/ca-cert.pem"
    timeout: 5
}
```

> 🇬🇧 *If JetStream is enabled, then the same `store_dir` will be reused and disk caching will be automatically enabled.*

Nếu JetStream được bật, cùng một `store_dir` sẽ được tái sử dụng và disk caching sẽ tự động được kích hoạt.

## Thuật ngữ trong bài

- **cache**: bộ nhớ đệm
- **config**: cấu hình
- **request**: yêu cầu
- **TLS**: mã hóa TLS