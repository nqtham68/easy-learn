---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting
title: Kết nối
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Kết nối

> 🇬🇧 *In order for a NATS client application to connect to the NATS service, and then subscribe or publish messages to subjects, it needs to be able to be configured with the details of how to connect to the NATS service infrastructure and of how to authenticate with it.*

Để kết nối được với NATS service, ứng dụng client cần được cấu hình với thông tin kết nối đến hạ tầng NATS và thông tin xác thực tương ứng. Sau khi kết nối thành công, ứng dụng mới có thể subscribe hoặc publish message lên các subject (chuỗi định danh message).

## NATS URL

> 🇬🇧 *A 'NATS URL' is a string (in a URL format) that specifies the IP address and port where the NATS server(s) can be reached, and what kind of connection to establish:*
> - *TLS encrypted only TCP connection (i.e. NATS URLs starting with `tls://...`)*
> - *TLS encrypted if the server is configured for it or plain un-encrypted TCP connection otherwise (i.e. NATS URLs starting with `nats://...`)*
> - *Websocket connection (i.e. NATS URLs starting with `ws://...`)*

1. 'NATS URL' là một chuỗi theo định dạng URL, chỉ định địa chỉ IP và port để kết nối đến NATS server, đồng thời xác định loại kết nối:
   * Kết nối TCP mã hóa TLS (credential) bắt buộc (URL bắt đầu bằng `tls://...`)
   * Kết nối TCP mã hóa TLS (mã hóa TLS) nếu server hỗ trợ, hoặc TCP thường nếu không (URL bắt đầu bằng `nats://...`)
   * Kết nối WebSocket (URL bắt đầu bằng `ws://...`)

### Kết nối đến cluster

> 🇬🇧 *Note that when connecting to a NATS service infrastructure with clusters there is more than one URL and the application should allow for more than one URL to be specified in its NATS connect call (typically you pass a comma separated list of URLs as the URL, e.g. `"nats://server1:port1,nats://server2:port2"`).*

Khi kết nối đến hạ tầng NATS có cluster (cụm nhiều server chạy chung), sẽ có nhiều hơn một URL. Ứng dụng cần hỗ trợ truyền nhiều URL trong lệnh kết nối NATS, thông thường dưới dạng danh sách phân tách bằng dấu phẩy, ví dụ: `"nats://server1:port1,nats://server2:port2"`.

> 🇬🇧 *When connecting to a cluster it is best to provide the complete set of 'seed' URLs for the cluster.*

Khi kết nối đến cluster, nên cung cấp đầy đủ tập 'seed' URL của cluster đó.

## Thông tin xác thực

> 🇬🇧 *If required: authentication details for the application to identify itself with the NATS server(s). NATS supports multiple authentication schemes:*
> - *Username/Password credentials*
> - *Decentralized JWT Authentication/Authorization*
> - *Token Authentication*
> - *TLS Certificate*
> - *NKEY with Challenge*

1. Khi cần xác thực, ứng dụng phải cung cấp thông tin để định danh với NATS server. NATS hỗ trợ nhiều phương thức xác thực:
   * [Username/Password credentials](./security/userpass.md) — có thể truyền trực tiếp trong NATS URL
   * [Decentralized JWT Authentication/Authorization](./security/creds.md) — ứng dụng được cấu hình với đường dẫn đến file credential (thông tin đăng nhập) chứa JWT và private Nkey
   * [Token Authentication](./security/token.md#connecting-with-a-token) — ứng dụng được cấu hình với chuỗi token (chuỗi xác thực)
   * [TLS Certificate](./security/tls.md#connecting-with-tls-and-verify-client-identity) — client dùng TLS certificate phía client; server ánh xạ certificate đó sang user được định nghĩa trong cấu hình server
   * [NKEY with Challenge](./security/nkey.md) — client được cấu hình với Seed và User NKeys

### Cấu hình runtime

> 🇬🇧 *Your application should expose a way to be configured at run time with the NATS URL(s) to use. If you want to use a secure infrastructure, the application must provide for the definition of either the credentials file (.creds) to use, or the means to encode the token, or Nkey, in the URL(s).*

Ứng dụng nên cho phép cấu hình NATS URL tại runtime. Nếu dùng hạ tầng bảo mật, ứng dụng cần hỗ trợ khai báo đường dẫn file credential (.creds), hoặc cách mã hóa token hay Nkey vào trong URL.

## Connection Options

> 🇬🇧 *Besides the connectivity and security details, there are numerous options for a NATS connection ranging from timeouts to reconnect settings to setting asynchronous error and connection event callback handlers in your application.*

Ngoài thông tin kết nối và bảo mật, NATS còn cung cấp nhiều tùy chọn khác như [timeout](../reconnect#connection-timeout-attributes), [reconnect settings](../reconnect#reconnection-attributes), hay đăng ký [callback xử lý lỗi và sự kiện kết nối bất đồng bộ](../reconnect#advisories).

## Xem Thêm

WebSocket và NATS

[WebSocket and NATS | Hello World](https://www.youtube.com/watch?v=AbAR9zgJnjY)

NATS WebSockets và React

[NATS WebSockets and React](https://www.youtube.com/watch?v=XS_Q0i6orSk)

## Thuật ngữ trong bài

- **callback**: hàm được gọi lại
- **client**: bên gọi (phía người dùng)
- **cluster**: cụm nhiều server chạy chung
- **credential**: thông tin đăng nhập
- **message**: gói dữ liệu được gửi đi
- **port**: cổng kết nối
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)
- **timeout**: thời gian chờ tối đa
- **TLS**: mã hóa TLS
- **token**: chuỗi xác thực