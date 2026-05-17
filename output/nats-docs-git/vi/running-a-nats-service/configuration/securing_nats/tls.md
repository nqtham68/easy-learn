---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/tls
title: Bật TLS
translated: true
translated_at: '2026-05-13T00:00:00Z'
---

# Bật TLS

> 🇬🇧 *The NATS server uses modern TLS semantics to encrypt client, route, and monitoring connections. [Check here for pitfalls.](#problems-with-self-signed-certificates)*

NATS server dùng TLS hiện đại để mã hóa các kết nối client, route và monitoring. [Xem các vấn đề thường gặp tại đây.](#problems-with-self-signed-certificates)

> 🇬🇧 *Server configuration revolves around a `tls` map, which has the following properties:*

Config (cấu hình) server xoay quanh map `tls` với các thuộc tính sau:

| Property | Description |  |  |
| :--- | :--- | :--- | :--- |
| `cert_file` | File certificate TLS. |  |  |
| `key_file` | File key của certificate TLS. |  |  |
| `ca_file` | [File certificate authority](./tls.md#certificate-authorities) TLS. Nếu không có, mặc định dùng system trust store. |  |  |
| `cipher_suites` | Khi được đặt, chỉ các cipher suite TLS được chỉ định mới được phép dùng. Giá trị phải khớp với phiên bản golang dùng để build server. |  |  |
| `curve_preferences` | Danh sách các TLS cipher curve theo thứ tự ưu tiên. |  |  |
| `insecure` | Bỏ qua xác minh certificate. Chỉ áp dụng cho kết nối đi ra, KHÔNG áp dụng cho kết nối client vào. **Không khuyến nghị** |  |  |
| `min_version` | Phiên bản TLS tối thiểu. Mặc định là `"1.2"`. |  |  |
| `timeout` | [Timeout](./tls.md#tls-timeout) TLS handshake tính bằng giây (hỗ trợ số thập phân). Mặc định là `2` giây. |  |  |
| `verify` | Nếu `true`, yêu cầu và [xác minh](./auth_intro/tls_mutual_auth.md#validating-a-client-certificate) certificate client. Để hỗ trợ Browser, tùy chọn này không áp dụng cho monitoring. |  |  |
| `verify_and_map` | Nếu `true`, yêu cầu, xác minh certificate client và [ánh xạ](./auth_intro/tls_mutual_auth.md#mapping-client-certificates-to-a-user) các giá trị certificate cho mục đích xác thực. Cũng không áp dụng cho monitoring. |  |  |
| `verify_cert_and_check_known_urls` | Chỉ có thể đặt trong context không phải client, trong đó `verify: true` là mặc định \([cluster](../clustering)/[gateway](../gateways)\). Các entry `X509v3 Subject Alternative Name` `DNS` trong certificate của kết nối đến sẽ được so khớp với tất cả URL trong context config chứa TLS map này. Nếu khớp thì kết nối được chấp nhận, ngược lại bị từ chối. Với gateway, tất cả DNS entry trong certificate được so với tất cả gateway URL. Với cluster, so với tất cả route URL. Hệ quả là khi cluster tăng trưởng động, các cluster khác có cờ này bật sẽ cần cập nhật config. Việc kiểm tra DNS name thực hiện theo [rfc6125](https://tools.ietf.org/html/rfc6125#section-6.4.1). Chỉ hỗ trợ wildcard đầy đủ `*` cho nhãn ngoài cùng bên trái — đây là một cách giữ linh hoạt cho cluster tăng trưởng. |  |  |
| `pinned_certs` | Danh sách các fingerprint public key ở dạng hex-encoded SHA256 của DER. Khi có, trong quá trình TLS handshake, fingerprint certificate được cung cấp phải nằm trong danh sách, nếu không kết nối bị đóng. Chuỗi lệnh sau tạo ra một entry cho certificate: \`openssl x509 -noout -pubkey -in  | openssl pkey -pubin -outform DER | openssl dgst -sha256\`. |

> 🇬🇧 *The simplest configuration:*

Config đơn giản nhất:

```text
tls: {
  cert_file: "./server-cert.pem"
  key_file: "./server-key.pem"
}
```

> 🇬🇧 *Or by using [server options](../../running/flags.md#tls-options):*

Hoặc dùng [server options](../../running/flags.md#tls-options):

```shell
nats-server --tls --tlscert=./server-cert.pem --tlskey=./server-key.pem
```
```text
[21417] 2019/05/16 11:21:19.801539 [INF] Starting nats-server version 2.0.0
[21417] 2019/05/16 11:21:19.801621 [INF] Git commit [not set]
[21417] 2019/05/16 11:21:19.801777 [INF] Listening for client connections on 0.0.0.0:4222
[21417] 2019/05/16 11:21:19.801782 [INF] TLS required for client connections
[21417] 2019/05/16 11:21:19.801785 [INF] Server id is ND6ZZDQQDGKYQGDD6QN2Y26YEGLTH6BMMOJZ2XJB2VASPVII3XD6RFOQ
[21417] 2019/05/16 11:21:19.801787 [INF] Server is ready
```

> 🇬🇧 *Notice that the log indicates that the client connections will be required to use TLS. If you run the server in Debug mode with `-D` or `-DV`, the logs will show the cipher suite selection for each connected client:*

Log sẽ cho thấy các kết nối client bắt buộc phải dùng TLS. Nếu chạy server ở chế độ Debug với `-D` hoặc `-DV`, log sẽ hiển thị cipher suite được chọn cho từng client kết nối:

```text
[22242] 2019/05/16 11:22:20.216322 [DBG] 127.0.0.1:51383 - cid:1 - Client connection created
[22242] 2019/05/16 11:22:20.216539 [DBG] 127.0.0.1:51383 - cid:1 - Starting TLS client connection handshake
[22242] 2019/05/16 11:22:20.367275 [DBG] 127.0.0.1:51383 - cid:1 - TLS handshake complete
[22242] 2019/05/16 11:22:20.367291 [DBG] 127.0.0.1:51383 - cid:1 - TLS version 1.2, cipher suite TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
```

> 🇬🇧 *When a `tls` section is specified at the root of the configuration, it also affects the monitoring port if `https_port` option is specified. Other sections such as `cluster` can specify a `tls` block.*

Khi section `tls` được khai báo ở root của config, nó cũng ảnh hưởng đến monitoring port nếu tùy chọn `https_port` được chỉ định. Các section khác như `cluster` có thể khai báo riêng một block `tls`.

## TLS-first Handshake

> 🇬🇧 *_As of NATS v2.10.4_*

_Từ NATS v2.10.4_

> 🇬🇧 *Client connections follow the model where, when a TCP connection is created to the server, the server will immediately send an [INFO protocol message](../../../reference/nats-protocol/nats-protocol#info) in clear text. This INFO protocol provides metadata, including whether the server requires a secure connection.*

Kết nối client hoạt động theo mô hình: khi TCP connection được tạo đến server, server lập tức gửi [INFO protocol message](../../../reference/nats-protocol/nats-protocol#info) ở dạng plain text. Tin nhắn INFO này cung cấp metadata, bao gồm thông tin server có yêu cầu kết nối bảo mật hay không.

> 🇬🇧 *Some environments prefer having clients' TLS connections be initiated right away, that is, not having any traffic sent in clear text. It was possible to by-pass this using a websocket connection. However, if a websocket connection is not desired, the server can be configured to perform a TLS handshake before sending the INFO protocol message.*

Một số môi trường yêu cầu TLS được khởi tạo ngay lập tức, tức là không có bất kỳ traffic nào gửi dưới dạng plain text. Trước đây có thể bỏ qua bước này bằng cách dùng WebSocket. Tuy nhiên, nếu không muốn dùng WebSocket, server có thể được config để thực hiện TLS handshake trước khi gửi INFO protocol message.

> 🇬🇧 *Only clients that implement an equivalent option would be able to connect if the server runs with this option enabled.*

Chỉ các client cài đặt tùy chọn tương đương mới có thể kết nối khi server bật tùy chọn này.

> 🇬🇧 *The configuration would look something like this:*

Config sẽ có dạng như sau:

```text
tls: {
  cert_file: "./server-cert.pem"
  key_file: "./server-key.pem"
  handshake_first: true
}
```

> 🇬🇧 *However, the parameter can be set to `auto` or a [Golang time duration](https://pkg.go.dev/time#ParseDuration) (e.g. `250ms`) to fallback to the original behavior. This is intended for deployments where it is known that not all clients have been upgraded to a client library providing the TLS-first handshake option.*

Tuy nhiên, tham số có thể được đặt thành `auto` hoặc một [Golang time duration](https://pkg.go.dev/time#ParseDuration) (ví dụ `250ms`) để fallback về hành vi ban đầu. Điều này dành cho các deployment mà không phải tất cả client đều đã được nâng cấp lên client library hỗ trợ TLS-first handshake.

> 🇬🇧 *After the delay has elapsed without receiving the TLS handshake from the client, the server reverts to sending the INFO protocol so that older clients can connect. Clients that do connect with the "TLS first" option will be marked as such in the monitoring's `Connz` page/result. It will allow the administrator to keep track of applications still needing to upgrade.*

Sau khi hết thời gian chờ mà không nhận được TLS handshake từ client, server chuyển về gửi INFO protocol để các client cũ có thể kết nối. Các client kết nối với tùy chọn "TLS first" sẽ được đánh dấu trên trang/kết quả `Connz` của monitoring, giúp quản trị viên theo dõi các ứng dụng còn cần nâng cấp.

> 🇬🇧 *The configuration would be similar to:*

Config sẽ tương tự như:

```text
tls: {
  cert_file: "./server-cert.pem"
  key_file: "./server-key.pem"
  handshake_first: auto
}
```

> 🇬🇧 *With the above value, the fallback delay used by the server is 50 milliseconds.*

Với giá trị trên, fallback delay của server là 50 milliseconds.

> 🇬🇧 *The duration can be explicitly set, say 300 milliseconds:*

Duration có thể được đặt rõ ràng, ví dụ 300 milliseconds:

```text
tls {
    cert_file: ...
    key_file: ...

    handshake_first: "300ms"
}
```

> 🇬🇧 *It is understood that any configuration other than "true" will result in the server sending the INFO protocol after the elapsed amount of time without the client initiating the TLS handshake. Therefore, for administrators who do not want any data transmitted in plain text, the value must be set to "true" only. It will require applications to be updated to a library that provides the option, which may or may not be readily available.*

Mọi config khác "true" đều dẫn đến việc server gửi INFO protocol sau khoảng thời gian đã đặt nếu client không khởi tạo TLS handshake. Do đó, với quản trị viên không muốn bất kỳ dữ liệu nào truyền dưới dạng plain text, giá trị phải là "true". Điều này yêu cầu ứng dụng được cập nhật lên một library cung cấp tùy chọn này — và library đó có thể chưa sẵn có.

## TLS Timeout

> 🇬🇧 *The `timeout` setting enables you to control the amount of time that a client is allowed to upgrade its connection to tls. If your clients are experiencing disconnects during TLS handshake, you'll want to increase the value, however, if you do be aware that an extended `timeout` exposes your server to attacks where a client doesn't upgrade to TLS and thus consumes resources. Conversely, if you reduce the TLS `timeout` too much, you are likely to experience handshake errors.*

Cài đặt `timeout` cho phép kiểm soát thời gian client được phép nâng cấp kết nối lên TLS. Nếu client bị ngắt kết nối trong quá trình TLS handshake, hãy tăng giá trị này. Tuy nhiên cần lưu ý: timeout (thời gian chờ tối đa) `timeout` dài hơn khiến server dễ bị tấn công từ client không nâng cấp TLS, tiêu tốn tài nguyên. Ngược lại, giảm TLS `timeout` quá thấp sẽ dẫn đến lỗi handshake thường xuyên.

```text
tls: {
  cert_file: "./server-cert.pem"
  key_file: "./server-key.pem"
  # clients will fail to connect (value is too low)
  timeout: 0.0001
}
```

## Certificate Authorities

> 🇬🇧 *The `ca_file` file should contain one or more Certificate Authorities in PEM format, in a bundle. This is a common format.*

File `ca_file` nên chứa một hoặc nhiều Certificate Authority ở định dạng PEM, dưới dạng bundle — đây là định dạng phổ biến.

> 🇬🇧 *When a certificate is issued, it is often accompanied by a copy of the intermediate certificate used to issue it. This is useful for validating that certificate. It is not necessarily a good choice as the only CA suitable for use in verifying other certificates a server may see.*

Khi một certificate được cấp, nó thường đi kèm bản sao của intermediate certificate dùng để cấp nó. Điều này hữu ích để xác thực certificate đó, nhưng không nhất thiết là lựa chọn duy nhất phù hợp để xác minh các certificate khác mà server có thể gặp.

> 🇬🇧 *Do consider though that organizations issuing certificates will change the intermediate they use. For instance, a CA might issue intermediates in pairs, with an active and a standby, and reserve the right to switch to the standby without notice. You probably would want to trust _both_ of those for the `ca_file` directive, to be prepared for such a day, and then after the first CA has been compromised you can remove it. This way the roll from one CA to another will not break your NATS server deployment.*

Cần lưu ý rằng tổ chức cấp certificate có thể thay đổi intermediate họ dùng. Chẳng hạn, một CA có thể cấp intermediate theo cặp — một active và một standby — và có quyền chuyển sang standby mà không báo trước. Tốt nhất nên tin tưởng _cả hai_ cho directive `ca_file`, để sẵn sàng cho tình huống đó; sau khi CA đầu tiên bị compromised, có thể xóa nó đi. Cách này giúp việc chuyển từ CA này sang CA khác không làm gián đoạn NATS server deployment.

## Chứng Chỉ Tự Ký Cho Kiểm Thử

> 🇬🇧 *Explaining [Public key infrastructure](https://en.wikipedia.org/wiki/Public_key_infrastructure), [Certificate Authorities \(CA\)](https://en.wikipedia.org/wiki/Certificate_authority) and [x509](https://tools.ietf.org/html/rfc5280) [certificates](https://en.wikipedia.org/wiki/Public_key_certificate) fall well outside the scope of this document. So does an explanation on how to obtain a properly trusted certificates.*

[Public key infrastructure](https://en.wikipedia.org/wiki/Public_key_infrastructure), [Certificate Authority (CA)](https://en.wikipedia.org/wiki/Certificate_authority) và [x509](https://tools.ietf.org/html/rfc5280) [certificate](https://en.wikipedia.org/wiki/Public_key_certificate) nằm ngoài phạm vi tài liệu này. Cách lấy certificate được tin cậy đúng cách cũng vậy.

> 🇬🇧 *If anybody outside your organization needs to connect, get certs from a public certificate authority. Think carefully about revocation and cycling times, as well as automation, when picking a CA. If arbitrary applications inside your organization need to connect, use a cert from your in-house CA. If only resources inside a specific environment need to connect, that environment might have its own dedicated automatic CA, eg in Kubernetes clusters, so use that.*

Nếu có người bên ngoài tổ chức cần kết nối, hãy lấy cert từ một public certificate authority. Khi chọn CA, cân nhắc kỹ về thời gian thu hồi, chu kỳ cấp lại và automation. Nếu các ứng dụng nội bộ cần kết nối, dùng cert từ CA nội bộ. Nếu chỉ có tài nguyên trong một môi trường cụ thể cần kết nối, môi trường đó có thể có CA tự động riêng — ví dụ trong Kubernetes cluster — hãy dùng CA đó.

> 🇬🇧 ***Only** for **testing** purposes does it make sense to generate self-signed certificates, even your own CA. This is a **short** guide on how to do just that and what to watch out for.*

**Chỉ** với mục đích **kiểm thử** mới nên tạo self-signed certificate, kể cả CA riêng. Đây là hướng dẫn **ngắn gọn** về cách thực hiện và những điều cần lưu ý.

> **KHÔNG SỬ DỤNG các certificate này trong môi trường production!!!**

### Vấn Đề Với Self-Signed Certificates

> 🇬🇧 *The issues and pitfalls listed here are not limited to self-signed certificates. You will most likely encounter them first in DEV environments when using those.*

Các vấn đề liệt kê dưới đây không chỉ giới hạn ở self-signed certificate — bạn sẽ thường gặp chúng đầu tiên trong môi trường DEV.

#### Client advertise không khớp với TLS names

> 🇬🇧 *NATS cluster advertises `host:port` of all nodes in a cluster to the connecting client. When connecting to a server via TLS the server name (or IP) is validated against the certificate presented by the server.*

NATS cluster (cụm nhiều server chạy chung) quảng bá `host:port` của tất cả node đến client đang kết nối. Khi kết nối qua TLS, tên server (hoặc IP) được xác thực so với certificate mà server trình bày.

> 🇬🇧 *When using TLS, it is important to control the hostname that clients will use when discovering the server. By default, the cluster will advertise an IP address, which may result in a failed TLS hostname verification with an IP SANs error.*

Khi dùng TLS, cần kiểm soát hostname mà client dùng khi khám phá server. Mặc định, cluster quảng bá địa chỉ IP, điều này có thể gây lỗi xác minh hostname TLS với lỗi IP SANs.

> 🇬🇧 *Set `avertise` or `cluster_advertise` in the cluster section to advertise verifiable server names. See [cluster_config.md](../clustering/cluster_config.md)*

Đặt `avertise` hoặc `cluster_advertise` trong section cluster để quảng bá tên server có thể xác minh. Xem [cluster_config.md](../clustering/cluster_config.md)

#### Không Có Trong Trust Store

> 🇬🇧 *As they should, these are **not trusted** by the system your server or clients are running on.*

Đúng như kỳ vọng, các certificate này **không được tin cậy** bởi hệ thống mà server hay client đang chạy trên.

> 🇬🇧 *One option is to specify the CA in every client you are using. In case you make use of `verify`, `verify_and_map` or `verify_cert_and_check_known_urls` you need to specify `ca_file` in the server. If you are having a more complex setup involving cluster, gateways or leaf nodes, `ca_file` needs to be present in `tls` maps used to connect to the server with self-signed certificates. While this works for server and libraries from the NATS ecosystem, you will experience issues when connecting with other tools such as your Browser.*

Một lựa chọn là chỉ định CA trong mỗi client. Nếu dùng `verify`, `verify_and_map` hoặc `verify_cert_and_check_known_urls`, cần chỉ định `ca_file` trong server. Với setup phức tạp hơn liên quan đến cluster, gateway hoặc leaf node, `ca_file` cần có trong các map `tls` dùng để kết nối đến server với self-signed certificate. Cách này hoạt động tốt với server và library trong hệ sinh thái NATS, nhưng sẽ gặp vấn đề khi kết nối bằng các công cụ khác như Browser.

> 🇬🇧 *Another option is to configure your system's trust store to include self-signed certificate\(s\). Which trust store needs to be configured depends on what you are testing.*

Lựa chọn khác là cấu hình system trust store để bao gồm self-signed certificate. Trust store nào cần cấu hình phụ thuộc vào nội dung bạn đang kiểm thử.

* OS cho server và một số client nhất định.
* Môi trường runtime cho các client như Java, Python hay Node.js.
* Browser cho các monitoring endpoint và WebSocket.

> 🇬🇧 *Please check your system's documentation on how to trust a particular self-signed certificate.*

Tham khảo tài liệu hệ thống của bạn để biết cách tin cậy một self-signed certificate cụ thể.

#### Thiếu Subject Alternative Name

> 🇬🇧 *Another common problem is failed [identity validation](https://tools.ietf.org/html/rfc6125). The IP or DNS name to connect to needs to match a [Subject Alternative Name \(SAN\)](https://tools.ietf.org/html/rfc4985) inside the certificate. Meaning, if a client/browser/server connect via tls to `127.0.0.1`, the server needs to present a certificate with a SAN containing the IP `127.0.0.1` or the connection will be closed with a handshake error.*

Một vấn đề phổ biến khác là [xác minh danh tính](https://tools.ietf.org/html/rfc6125) thất bại. IP hoặc DNS name dùng để kết nối cần khớp với [Subject Alternative Name (SAN)](https://tools.ietf.org/html/rfc4985) trong certificate. Nghĩa là, nếu client/browser/server kết nối qua TLS đến `127.0.0.1`, server phải trình bày certificate có SAN chứa IP `127.0.0.1`, nếu không kết nối bị đóng với lỗi handshake.

> 🇬🇧 *When `verify_cert_and_check_known_urls` is specified, [Subject Alternative Name \(SAN\)](https://tools.ietf.org/html/rfc4985) `DNS` records are necessary. In order to successfully connect there must be an overlap between the `DNS` records provided as part of the certificate and the urls configured. If you dynamically grow your cluster and use a new certificate, this route or gateway the server connects to will have to be reconfigured to include an url for the new server. Only then can the new server connect. If the `DNS` record is a wildcard, matching according to [rfc6125](https://tools.ietf.org/html/rfc6125#section-6.4.1) will be performed. Using certificates with a wildcard [Subject Alternative Name \(SAN\)](https://tools.ietf.org/html/rfc4985) and configuration with url\(s\) that would match are a way to keep the flexibility of dynamic cluster growth without configuration changes in other clusters.*

Khi `verify_cert_and_check_known_urls` được chỉ định, cần có record SAN `DNS`. Để kết nối thành công, phải có sự trùng khớp giữa các record `DNS` trong certificate và các URL đã config. Nếu cluster tăng trưởng động và dùng certificate mới, route hoặc gateway mà server kết nối đến phải được cấu hình lại để bao gồm URL của server mới — chỉ khi đó server mới mới có thể kết nối. Nếu record `DNS` là wildcard, việc so khớp theo [rfc6125](https://tools.ietf.org/html/rfc6125#section-6.4.1) sẽ được thực hiện. Dùng certificate có wildcard SAN kết hợp với config URL phù hợp là cách giữ linh hoạt cho cluster tăng trưởng động mà không cần thay đổi config ở các cluster khác.

#### Sai Key Usage

> 🇬🇧 *When generating your certificate you need to make sure to include the right purpose for which you want to use the certificate. This is encoded in [key usage](https://tools.ietf.org/html/rfc5280#section-4.2.1.3) and [extended key usage](https://tools.ietf.org/html/rfc5280#section-4.2.1.12). The necessary values for key usage depend on the ciphers used. `Digital Signature` and `Key Encipherment` are an interoperable choice.*

Khi tạo certificate, cần đảm bảo bao gồm đúng mục đích sử dụng, được mã hóa trong [key usage](https://tools.ietf.org/html/rfc5280#section-4.2.1.3) và [extended key usage](https://tools.ietf.org/html/rfc5280#section-4.2.1.12). Các giá trị cần thiết cho key usage phụ thuộc vào cipher đang dùng. `Digital Signature` và `Key Encipherment` là lựa chọn có tính tương thích tốt.

> 🇬🇧 *With respect to NATS the relevant values for extended key usage are:*

Với NATS, các giá trị extended key usage liên quan gồm:

* `TLS WWW server authentication` — Xác thực với tư cách server cho kết nối đến. NATS server cần certificate chứa giá trị này.
* `TLS WWW client authentication` — Xác thực với tư cách client cho kết nối đi ra. Chỉ cần khi kết nối đến server có `verify`, `verify_and_map` hoặc `verify_cert_and_check_known_urls`. Trong các trường hợp đó, NATS client cần certificate với giá trị này.
  * Kết nối [Leaf node](../leafnodes) có thể config với `verify`. Khi đó NATS server kết nối đến cũng phải trình bày certificate với giá trị này. Certificate chứa cả hai giá trị là một lựa chọn.
  * Kết nối [Cluster](../clustering) luôn bật `verify`. Server nào đóng vai client hay server phụ thuộc vào thời điểm, không thể config riêng. Certificate chứa cả hai giá trị là bắt buộc.
  * Kết nối [Gateway](../gateways) luôn bật `verify`. Khác với cluster, kết nối đi ra của gateway có thể chỉ định cert riêng. Certificate chứa cả hai giá trị giúp giảm phức tạp trong config.

> 🇬🇧 *Note that it's common practice for non-web protocols to use the `TLS WWW` authentication fields, as a matter of history those have become embedded as generic options.*

Lưu ý rằng các non-web protocol thường dùng các trường xác thực `TLS WWW` — theo lịch sử, chúng đã trở thành các tùy chọn chung.

### Tạo Self-Signed Certificates Cho Kiểm Thử

> 🇬🇧 *The simplest way to generate a CA as well as client and server certificates is [mkcert](https://github.com/FiloSottile/mkcert). This zero config tool generates and installs the CA into your **local** system trust store\(s\) and makes providing SAN straight forward. Check its [documentation](https://github.com/FiloSottile/mkcert/blob/master/README.md) for installation and your system's trust store. Here is a simple example:*

Cách đơn giản nhất để tạo CA cùng với client và server certificate là dùng [mkcert](https://github.com/FiloSottile/mkcert). Công cụ zero-config này tạo và cài CA vào **local** system trust store, đồng thời giúp khai báo SAN dễ dàng. Xem [tài liệu](https://github.com/FiloSottile/mkcert/blob/master/README.md) để biết cách cài đặt và cấu hình trust store. Ví dụ đơn giản:

> 🇬🇧 *Generate a CA as well as a certificate, valid for server authentication by `localhost` and the IP `::1`\(`-cert-file` and `-key-file` overwrite default file names\). Then start a NATS server using the generated certificate.*

Tạo CA và certificate hợp lệ cho server authentication với `localhost` và IP `::1` \(`-cert-file` và `-key-file` ghi đè tên file mặc định\). Sau đó khởi động NATS server với certificate được tạo ra.

```bash
mkcert -install
mkcert -cert-file server-cert.pem -key-file server-key.pem localhost ::1
nats-server --tls --tlscert=server-cert.pem --tlskey=server-key.pem -ms 8222
```

> 🇬🇧 *Now you should be able to access the monitoring endpoint `https://localhost:8222` with your browser. `https://127.0.0.1:8222` however should result in an error as `127.0.0.1` is not listed as SAN. You will not be able to establish a connection from another computer either. For that to work you have to provide appropriate DNS and/or IP [SAN\(s\)](./tls.md#missing-subject-alternative-name)*

Lúc này bạn có thể truy cập monitoring endpoint `https://localhost:8222` bằng browser. Tuy nhiên `https://127.0.0.1:8222` sẽ báo lỗi vì `127.0.0.1` không được liệt kê trong SAN. Bạn cũng không thể kết nối từ máy tính khác. Để làm được điều đó, cần cung cấp [SAN](./tls.md#missing-subject-alternative-name) DNS và/hoặc IP phù hợp.

> 🇬🇧 *To generate certificates that work with `verify` and [`cluster`](../clustering)/[`gateway`](../gateways)/[`leaf_nodes`](../leafnodes) provide the `-client` option. It will cause the appropriate key usage for client authentication to be added. This example also adds a SAN email for usage as user name in `verify_and_map`.*

Để tạo certificate hoạt động với `verify` và [`cluster`](../clustering)/[`gateway`](../gateways)/[`leaf_nodes`](../leafnodes), hãy dùng tùy chọn `-client`. Nó sẽ thêm key usage phù hợp cho client authentication. Ví dụ này cũng thêm SAN email để dùng làm user name trong `verify_and_map`.

```bash
mkcert -client -cert-file client-cert.pem -key-file client-key.pem localhost ::1 email@localhost
```

> 🇬🇧 *Please note:*
>
> * *That client refers to connecting process, not necessarily a NATS client.*
> * *`mkcert -client` will generate a certificate with key usage suitable for client **and** server authentication.*

Lưu ý:

* Client ở đây chỉ tiến trình kết nối, không nhất thiết là NATS client.
* `mkcert -client` sẽ tạo certificate với key usage phù hợp cho cả client **và** server authentication.

> 🇬🇧 *Examples in this document make use of the certificates generated so far. To simplify examples using the CA certificate, copy `rootCA.pem` into the same folder where the certificates were generated. To obtain the CA certificate's location use this command:*

Các ví dụ trong tài liệu này dùng các certificate đã tạo ở trên. Để đơn giản hóa các ví dụ dùng CA certificate, copy `rootCA.pem` vào cùng thư mục với các certificate đã tạo. Dùng lệnh sau để lấy đường dẫn CA certificate:

```bash
mkcert -CAROOT
```

> 🇬🇧 *Once you are done testing, remove the CA from your **local** system trust store\(s\).*

Khi kiểm thử xong, hãy xóa CA khỏi **local** system trust store.

```text
mkcert -uninstall
```

> 🇬🇧 *Alternatively, you can also use [openssl](https://www.openssl.org/) to [generate certificates](https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs). This tool allows a lot more customization of the generated certificates. It is **more complex** and does **not manage** installation into the system trust store\(s\).*

Ngoài ra, có thể dùng [openssl](https://www.openssl.org/) để [tạo certificate](https://www.digitalocean.com/community/tutorials/openssl-essentials-working-with-ssl-certificates-private-keys-and-csrs). Công cụ này cho phép tùy chỉnh nhiều hơn nhưng **phức tạp hơn** và **không tự quản lý** việc cài vào system trust store.

> 🇬🇧 *However, for inspecting certificates it is quite handy. To inspect the certificates from the above example execute these commands:*

Tuy nhiên, nó rất tiện để kiểm tra certificate. Dùng các lệnh sau để kiểm tra certificate từ ví dụ trên:

```bash
openssl x509 -noout -text -in server-cert.pem
openssl x509 -noout -text -in client-cert.pem
```

## TLS-Terminating Reverse Proxy

> 🇬🇧 *Using a [TLS-terminating reverse proxy](https://en.wikipedia.org/wiki/TLS_termination_proxy) with NATS requires some specific configuration on the server. In a typical proxy scenario, the client to proxy communication is secured and the proxy to server is insecure. This causes a "mismatch" because the server appears to be insecure but the client is told to connect securely. To fix this, the server must be configured as "tls available". This is done via an empty `tls` block and the `allow_non_tls` flag.*

Khi dùng [TLS-terminating reverse proxy](https://en.wikipedia.org/wiki/TLS_termination_proxy) với NATS, server cần một số config đặc biệt. Trong proxy thông thường, kết nối từ client đến proxy được bảo mật còn từ proxy đến server thì không. Điều này gây ra "sự không khớp" vì server có vẻ không bảo mật nhưng client lại được yêu cầu kết nối bảo mật. Để khắc phục, server phải được config ở chế độ "tls available" — thực hiện qua một block `tls` rỗng và cờ `allow_non_tls`.

```
tls {}
allow_non_tls: true
```

> 🇬🇧 *Once this is configured, your client can connect to the proxy with normal (language specific) tls configuration. Please make sure you are using the appropriate version of your language specific client.*

Sau khi config xong, client có thể kết nối đến proxy với TLS config thông thường (theo từng ngôn ngữ). Hãy đảm bảo dùng đúng phiên bản client cho ngôn ngữ của bạn.

| Client | Version |
| --- | --- |
| nats.go | v1.31.0 |
| nats.js | 2024.1.2 |
| nats.java | 2.18.0  |
| nats.rs | 0.33 |
| nats.net.v2 | 2.0.0 |
| nats.net (v1) | 1.1.5 |
|||

### nats.js

See: <https://github.com/nats-io/nats.js/issues/369>

### nats.rs

See: <https://github.com/nats-io/nats.rs/blob/main/async-nats/src/connector.rs>

### nats.net (v1)

See: <https://github.com/nats-io/nats.net.v1/tree/main/src/Samples/TlsVariationsExample>

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **deploy**: triển khai
- **node**: một server trong cluster
- **permission**: quyền truy cập
- **timeout**: thời gian chờ tối đa
- **TLS**: mã hóa TLS