---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/tls_mutual_auth
title: Xác thực TLS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Xác thực TLS

> 🇬🇧 *The server can require TLS certificates from a client. When needed, you can use the certificates to:*
> *- Validate the client certificate matches a known or trusted CA*
> *- Extract information from a trusted certificate to provide authentication*

Server có thể yêu cầu TLS certificate từ phía client. Khi cần, certificate có thể dùng để:

* Xác nhận certificate của client khớp với một CA đã biết hoặc đáng tin cậy
* Trích xuất thông tin từ certificate tin cậy để thực hiện xác thực

> Note: To simplify the common scenario of maintainers looking at the monitoring endpoint, `verify` and `verify_and_map` do not apply to the monitoring port.

> Lưu ý: Để đơn giản hóa cho trường hợp người quản trị xem monitoring endpoint, `verify` và `verify_and_map` không áp dụng cho monitoring port.

> 🇬🇧 *The examples in the following sections make use of the certificates you [generated](../tls.md#self-signed-certificates-for-testing) locally.*

Các ví dụ trong phần tiếp theo sử dụng certificate mà bạn đã [tạo](../tls.md#self-signed-certificates-for-testing) ở máy cục bộ.

## Xác thực Certificate của Client

> 🇬🇧 *The server can verify a client certificate using a CA certificate. To require verification, add the option `verify` to the TLS configuration section as follows:*

Server có thể xác minh certificate của client bằng CA certificate. Để bắt buộc xác minh, thêm tùy chọn `verify` vào phần config (cấu hình) TLS như sau:

```
tls {
  cert_file: "server-cert.pem"
  key_file:  "server-key.pem"
  ca_file:   "rootCA.pem"
  verify:    true
}
```

> 🇬🇧 *Or via the command line:*

Hoặc qua command line:

```bash
nats-server --tlsverify --tlscert=server-cert.pem --tlskey=server-key.pem --tlscacert=rootCA.pem
```

> 🇬🇧 *This option verifies the client's certificate is signed by the CA specified in the `ca_file` option. When `ca_file` is not present it will default to CAs in the system trust store. It also makes sure that the client provides a certificate with the extended key usage `TLS Web Client Authentication`.*

Tùy chọn này xác minh rằng certificate của client được ký bởi CA chỉ định trong tùy chọn `ca_file`. Khi `ca_file` không có mặt, mặc định sẽ dùng các CA trong system trust store. Ngoài ra, tùy chọn này còn đảm bảo client cung cấp certificate với extended key usage `TLS Web Client Authentication`.

## Ánh Xạ Certificate Client Sang User

> 🇬🇧 *In addition to verifying that a specified CA issued a client certificate, you can use information encoded in the certificate to authenticate a client. The client wouldn't have to provide or track usernames or passwords.*

Ngoài việc xác minh CA đã phát hành certificate cho client, bạn có thể dùng thông tin được mã hóa trong certificate để xác thực client. Như vậy, client không cần cung cấp hoặc quản lý username hay password — đây chính là hình thức sử dụng credential (thông tin đăng nhập) từ certificate.

> 🇬🇧 *To have TLS Mutual Authentication map certificate attributes to the user's identity use `verify_and_map` as shown as follows:*

Để TLS Mutual Authentication ánh xạ thuộc tính certificate sang danh tính user, dùng `verify_and_map` như sau:

```
tls {
  cert_file: "server-cert.pem"
  key_file:  "server-key.pem"
  ca_file:   "rootCA.pem"
  # Require a client certificate and map user id from certificate
  verify_and_map: true
}
```

> Note that `verify` was changed to `verify_and_map`.

> Lưu ý rằng `verify` đã được đổi thành `verify_and_map`.

> 🇬🇧 *When present, the server will check if a Subject Alternative Name (SAN) maps to a user. It will search all email addresses first, then all DNS names. If no user could be found, it will try the certificate subject.*

Khi có mặt, server sẽ kiểm tra xem Subject Alternative Name (SAN) có ánh xạ tới user nào không. Server tìm kiếm tất cả địa chỉ email trước, sau đó là tất cả DNS name. Nếu không tìm thấy user nào, server sẽ thử dùng subject (chuỗi định danh message) của certificate.

> Note: This mechanism will pick the user it finds first. There is no configuration to restrict this.

> Lưu ý: Cơ chế này sẽ chọn user đầu tiên tìm thấy. Không có config nào để hạn chế điều này.

```shell
openssl x509 -noout -text -in  client-cert.pem
```
```
Certificate:
...
        X509v3 extensions:
            X509v3 Subject Alternative Name:
                DNS:localhost, IP Address:0:0:0:0:0:0:0:1, email:email@localhost
            X509v3 Extended Key Usage:
                TLS Web Client Authentication
...
```

> 🇬🇧 *The configuration to authorize this user would be as follow:*

Config để cấp quyền cho user này như sau:

```
authorization {
  users = [
    {user: "email@localhost"}
  ]
}
```

> 🇬🇧 *Use the [RFC 2253 Distinguished Names](https://tools.ietf.org/html/rfc2253) syntax to specify a user corresponding to the certificate subject:*

Dùng cú pháp [RFC 2253 Distinguished Names](https://tools.ietf.org/html/rfc2253) để chỉ định user tương ứng với certificate subject. Cú pháp này cho phép thiết lập permission (quyền truy cập) dựa trên thông tin định danh trong certificate:

```shell
openssl x509 -noout -text -in client-cert.pem
```
```
Certificate:
    Data:
...
        Subject: O=mkcert development certificate, OU=testuser@MacBook-Pro.local (Test User)
...
```

> Note that for this example to work you will have to modify the user to match what is in your certificates subject. In doing so, watch out for the order of attributes!

> Lưu ý: Để ví dụ này hoạt động, bạn cần chỉnh sửa user cho khớp với nội dung trong certificate subject. Khi làm vậy, hãy chú ý thứ tự của các thuộc tính!

> 🇬🇧 *The configuration to authorize this user would be as follows:*

Config để cấp quyền cho user này như sau:

```
authorization {
  users = [
    {user: "OU=testuser@MacBook-Pro.local (Test User),O=mkcert development certificate"}
  ]
}
```

## TLS Timeout

> 🇬🇧 *[TLS timeout](../tls.md#tls-timeout) is described here.*

[TLS timeout](../tls.md#tls-timeout) được mô tả tại đây.

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **permission**: quyền truy cập
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)