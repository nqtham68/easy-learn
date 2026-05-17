---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/gateways/gateway
title: Cấu hình Gateway
translated: true
translated_at: '2026-05-13T00:00:00Z'
---

# Cấu hình Gateway

> 🇬🇧 *The `gateway` [configuration block](./gateway.md#gateway-configuration-block) is similar to a [`cluster`](https://docs.nats.io/running-a-nats-service/configuration/clustering/cluster\_config) block:*

Khối config (cấu hình) `gateway` có cấu trúc tương tự khối [`cluster`](https://docs.nats.io/running-a-nats-service/configuration/clustering/cluster\_config):

```
gateway {
    name: "A"
    listen: "localhost:7222"
    authorization {
        user: gwu
        password: gwp
    }

    gateways: [
        {name: "A", url: "nats://gwu:gwp@localhost:7222"},
        {name: "B", url: "nats://gwu:gwp@localhost:7333"},
        {name: "C", url: "nats://gwu:gwp@localhost:7444"},
    ]
}
```

> 🇬🇧 *One difference is that instead of `routes` you specify `gateways`. As expected _self-gateway_ connections are ignored, so you can share gateway configurations with minimal fuss.*

Điểm khác biệt là thay vì `routes` bạn chỉ định `gateways`. Các kết nối _self-gateway_ sẽ bị bỏ qua như mong đợi, vì vậy có thể chia sẻ cấu hình gateway mà không cần lo lắng thêm.

> 🇬🇧 *Starting a server:*

Khởi động server:

```shell
nats-server -c A.conf
```

```
[85803] 2019/05/07 10:50:55.902474 [INF] Starting nats-server version 2.0.0
[85803] 2019/05/07 10:50:55.903669 [INF] Gateway name is A
[85803] 2019/05/07 10:50:55.903684 [INF] Listening for gateways connections on localhost:7222
[85803] 2019/05/07 10:50:55.903696 [INF] Address for gateway "A" is localhost:7222
[85803] 2019/05/07 10:50:55.903909 [INF] Listening for client connections on 0.0.0.0:4222
[85803] 2019/05/07 10:50:55.903914 [INF] Server id is NBHUDBF3TVJSWCDPG2HSKI4I2SBSPDTNYEXEMOFAZUZYXVA2IYRUGPZU
[85803] 2019/05/07 10:50:55.903917 [INF] Server is ready
[85803] 2019/05/07 10:50:56.830669 [INF] 127.0.0.1:50892 - gid:2 - Processing inbound gateway connection
[85803] 2019/05/07 10:50:56.830673 [INF] 127.0.0.1:50891 - gid:1 - Processing inbound gateway connection
[85803] 2019/05/07 10:50:56.831079 [INF] 127.0.0.1:50892 - gid:2 - Inbound gateway connection from "C" (NBHWDFO3KHANNI6UCEUL27VNWL7NWD2MC4BI4L2C7VVLFBSMZ3CRD7HE) registered
[85803] 2019/05/07 10:50:56.831211 [INF] 127.0.0.1:50891 - gid:1 - Inbound gateway connection from "B" (ND2UJB3GFUHXOQ2UUMZQGOCL4QVR2LRJODPZH7MIPGLWCQRARJBU27C3) registered
[85803] 2019/05/07 10:50:56.906103 [INF] Connecting to explicit gateway "B" (localhost:7333) at 127.0.0.1:7333
[85803] 2019/05/07 10:50:56.906104 [INF] Connecting to explicit gateway "C" (localhost:7444) at 127.0.0.1:7444
[85803] 2019/05/07 10:50:56.906404 [INF] 127.0.0.1:7333 - gid:3 - Creating outbound gateway connection to "B"
[85803] 2019/05/07 10:50:56.906444 [INF] 127.0.0.1:7444 - gid:4 - Creating outbound gateway connection to "C"
[85803] 2019/05/07 10:50:56.906647 [INF] 127.0.0.1:7444 - gid:4 - Outbound gateway connection to "C" (NBHWDFO3KHANNI6UCEUL27VNWL7NWD2MC4BI4L2C7VVLFBSMZ3CRD7HE) registered
[85803] 2019/05/07 10:50:56.906772 [INF] 127.0.0.1:7333 - gid:3 - Outbound gateway connection to "B" (ND2UJB3GFUHXOQ2UUMZQGOCL4QVR2LRJODPZH7MIPGLWCQRARJBU27C3) registered
```

> 🇬🇧 *Once all the gateways are up, these clusters of one will forward messages as expected:*

Khi tất cả các gateway đã hoạt động, các cluster (cụm nhiều server chạy chung) đơn lẻ này sẽ chuyển tiếp message (gói dữ liệu được gửi đi) như mong đợi:

```shell
nats sub -s localhost:4333 ">"
```

> 🇬🇧 *On a different session...*

Trên một session khác...

```shell
nats pub -s localhost:4444 foo bar
```

> 🇬🇧 *The subscriber should print*

Subscriber (bên đăng ký nhận message) sẽ in ra

```
[#1] Received on [foo] : 'bar'
```

## Khối Config `Gateway`

| Property                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Version |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------|
| `name`                   | Tên cho cluster này; tất cả các gateway thuộc cùng một cluster phải chỉ định cùng tên.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |         |
| `reject_unknown_cluster` | Nếu `true`, gateway sẽ từ chối kết nối từ các cluster không được cấu hình trong `gateways`. Điều này được thực hiện bằng cách kiểm tra xem tên cluster do kết nối đến cung cấp có tồn tại dưới dạng named gateway hay không. Cơ chế này vô hiệu hóa gossip về cluster mới, nhưng không ngăn cluster đã được cấu hình mở rộng động.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |         |
| `gateways`               | Danh sách các [entry](./gateway.md#gateway-entry) của Gateway — xem bên dưới.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |         |
| `host`                   | Interface nơi gateway lắng nghe các kết nối gateway đến.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |         |
| `port`                   | Port nơi gateway lắng nghe các kết nối gateway đến.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |         |
| `listen`                 | Kết hợp `host` và `port` thành `<host>:<port>`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |         |
| `tls`                    | Một [bản đồ cấu hình `tls`](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/tls) để bảo mật các kết nối gateway. `verify` luôn được bật. Trừ khi được chỉ định khác trong [`gateway`](./gateway.md#gateway-entry), `cert_file` sẽ là client certificate mặc định. [Các lưu ý về Certificate](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/tls).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |         |
| `advertise`              | Hostport `<host>:<port>` để quảng bá cách server này có thể được liên hệ bởi các thành viên gateway khác. Hữu ích trong môi trường có NAT, hoặc trên cloud khi được expose qua Network Load Balancer.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |         |
| `connect_retries`        | Số lần thử kết nối thất bại tối đa trước khi từ bỏ thiết lập kết nối đến một gateway được phát hiện. Mặc định là `0`, không retry. Khi được bật, sẽ thử lại mỗi giây. Không áp dụng cho các gateway được cấu hình tường minh.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |         |
| `connect_backoff`        | Bật backoff (chiến lược chờ tăng dần giữa các lần retry) theo hàm mũ cho các lần reconnect. Nếu là `true`, sẽ bắt đầu từ 1 giây và tăng dần lên tối đa 30 giây.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | 2.12.0  |
| `authorization`          | Bản đồ [Authorization](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/auth\_intro#authorization-map) cho các gateway. Khi dùng một `username`/`password` duy nhất, nó xác định cơ chế xác thực mà server này yêu cầu, đồng thời dùng để server tự xác thực khi kết nối đến gateway được _phát hiện_. Cấu hình này không áp dụng cho các gateway khai báo tường minh trong [`gateways`](./gateway.md#gateway-entry) — với những gateway đó, credential (thông tin đăng nhập) phải được cung cấp trong URL. Với chế độ này, hãy dùng cùng credential trên toàn hệ thống hoặc khai báo tường minh từng gateway trên mỗi server. Nếu bản đồ cấu hình `tls` chỉ định `verify_and_map`, chỉ cung cấp `username` tương ứng. Có thể dùng certificate khác nhau nhưng phúng phải ánh xạ về cùng `username`. Bản đồ authorization cũng cho phép `timeout`, được tuân thủ, nhưng cấu hình `users` và `token` không được hỗ trợ và sẽ ngăn server khởi động. Block `permissions` bị bỏ qua. |         |

### Entry `Gateway`

> 🇬🇧 *The `gateways` configuration block is a list of gateway entries with the following properties:*

Khối config `gateways` là danh sách các gateway entry với các thuộc tính sau:

| Property | Description                                                                                                                                                                                                                                                                                                                                                   |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`   | Tên gateway.                                                                                                                                                                                                                                                                                                                                                 |
| `url`    | Hostport `<host>:<port>` mô tả địa chỉ của remote gateway. Nếu có nhiều IP được trả về, một địa chỉ sẽ được chọn ngẫu nhiên.                                                                                                                                                                                                                          |
| `urls`   | Danh sách các chuỗi `url`.                                                                                                                                                                                                                                                                                                                                      |
| `tls`    | Một [bản đồ cấu hình `tls`](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/tls) để thiết lập kết nối gateway bảo mật. Nếu block TLS cấp cao nhất `gateway{}` có certificate phục vụ cả mục đích client lẫn server, có thể bỏ qua block này — server sẽ dùng certificate từ phần `gateway{tls{}}`. Xem thêm hướng dẫn bên dưới trong TLS Entry. |

> 🇬🇧 *By using `urls` and an array, you can specify a list of endpoints that form part of a cluster as below. A NATS Server will pick one of those addresses randomly and only establish a single outbound gateway connection to one of the members from another cluster:*

Bằng cách dùng `urls` kèm một mảng, bạn có thể khai báo danh sách các endpoint (địa chỉ API cụ thể) tạo thành một phần của cluster. NATS Server sẽ chọn ngẫu nhiên một trong các địa chỉ đó và chỉ thiết lập một kết nối gateway outbound duy nhất đến một thành viên từ cluster khác:

```
gateway {
    name: "DC-A"
    listen: "localhost:7222"

    gateways: [
        {name: "DC-A", urls: ["nats://localhost:7222", "nats://localhost:7223", "nats://localhost:7224"]},
        {name: "DC-B", urls: ["nats://localhost:7332", "nats://localhost:7333", "nats://localhost:7334"]},
        {name: "DC-C", urls: ["nats://localhost:7442", "nats://localhost:7333", "nats://localhost:7335"]}
    ]
}
```

### TLS Entry

> 🇬🇧 *In addition to the normal TLS configuration advice, bear in mind that TLS keys and certificates for multiple clusters, or servers in different locations, rarely rotate at the exact same time and that Certificate Authorities do roll between multiple Intermediate certificates.*

Ngoài các hướng dẫn cấu hình TLS thông thường, cần lưu ý rằng TLS key và certificate cho nhiều cluster, hoặc server ở các vị trí khác nhau, hiếm khi rotate đồng thời và các Certificate Authority có thể luân chuyển qua nhiều Intermediate certificate.

> 🇬🇧 *If using a certificate bundle which accompanied the issuance of a certificate then the CA in that bundle will typically be for just that certificate. Using _only_ that CA as the CA for gateway authentication is ill-advised. You should ensure that you allow for rolling between Certificate Authorities, even if only between multiple CAs from the same organization entity, and use a separate certificate bundle for _verification_ of peers. This way when DC-B rolls before DC-A, it will not be cut off from your supercluster.*

Nếu dùng certificate bundle đi kèm khi cấp certificate, CA trong bundle đó thường chỉ dành cho certificate đó. Việc dùng _duy nhất_ CA đó để xác thực gateway là không được khuyến nghị. Hãy đảm bảo cho phép luân chuyển giữa các Certificate Authority — dù chỉ là giữa nhiều CA của cùng một tổ chức — và dùng một certificate bundle riêng để _xác minh_ peer. Cách này giúp khi DC-B rotate trước DC-A, nó sẽ không bị cắt đứt khỏi supercluster của bạn.

### Gateway đằng sau Load Balancer

> 🇬🇧 *When running in a private network ( such as VPC in the cloud ), you'd probably want to setup a Load Balancer to expose the gateway port. In this case, it's important to set the `advertise` value of each NATS server to the Load Balancer hostname and port serving them. Otherwise, they will advertise their own private IP and port, and can generate failures and downtime if any reconnection is required.*

Khi chạy trong mạng private (chẳng hạn VPC trên cloud), bạn thường muốn đặt Load Balancer để expose port gateway. Trong trường hợp này, cần thiết lập giá trị `advertise` của mỗi NATS server thành hostname và port của Load Balancer phục vụ chúng. Nếu không, các server sẽ quảng bá IP private và port của chính mình, có thể gây lỗi và downtime khi cần reconnect.

## Thuật ngữ trong bài

- **backoff**: chiến lược chờ tăng dần giữa các lần retry
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **endpoint**: địa chỉ API cụ thể
- **message**: gói dữ liệu được gửi đi
- **permission**: quyền truy cập
- **port**: cổng kết nối
- **retry**: thử lại khi fail
- **server**: máy chủ
- **subscriber**: bên đăng ký nhận message
- **TLS**: mã hóa TLS