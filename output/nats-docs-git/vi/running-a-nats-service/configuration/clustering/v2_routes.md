---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/clustering/v2_routes
title: Routes v2
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Routes v2

_Giới thiệu trong NATS v2.10.0_

## Connection pooling

> 🇬🇧 *Before the v2.10.0 release, two servers in a cluster had only one connection to transmit all messages for all accounts, which could lead to slow down and increased memory usage when data was not transmitted fast enough.*

Trước phiên bản v2.10.0, hai server trong cùng một cluster (cụm nhiều server chạy chung) chỉ dùng một kết nối duy nhất để truyền tất cả message cho mọi account. Điều này có thể khiến hệ thống chậm lại và tốn thêm bộ nhớ khi dữ liệu không được truyền đi kịp thời.

> 🇬🇧 *The v2.10.0 release introduces the ability to have multiple route connections between two servers. By default, without any configuration change, clustering two v2.10.0+ servers together will create 3 route connections. This can of course be configured to a different value by explicitly configuring the pool size.*

Phiên bản v2.10.0 cho phép tạo nhiều route connection giữa hai server. Theo mặc định, khi kết nối hai server v2.10.0+ với nhau thành cluster, hệ thống sẽ tạo 3 route connection. Giá trị này có thể thay đổi bằng cách config (cấu hình) pool size một cách tường minh.

```
cluster {
  pool_size: 3
}
```

### Yêu cầu về pool size

> 🇬🇧 *Each of those connections will handle a specific subset of the accounts, and the assignment of an account to a specific connection index in the pool is the same in any server in the cluster. It is required that each server in the cluster have the same pool size value, otherwise, clustering will fail to be established with an error similar to:*

Mỗi connection trong pool sẽ xử lý một tập hợp account nhất định. Việc phân công account vào index nào trong pool là giống nhau ở mọi server trong cluster. Tất cả các server trong cluster phải có cùng giá trị pool size — nếu không, quá trình thiết lập cluster sẽ thất bại với lỗi tương tự như:

```
[ERR] 127.0.0.1:6222 - rid:6 - Mismatch route pool size: 3 vs 4
```

### Xử lý khi mất kết nối

> 🇬🇧 *In the event that a given connection of the pool breaks, automatic reconnection occurs as usual. However, while the disconnection is happening, traffic for accounts handled by that connection is stopped (that is, traffic is not routed through other connections), the same way that it was when there was a single route connection.*

Khi một connection trong pool bị đứt, hệ thống sẽ tự động reconnect như thông thường. Tuy nhiên, trong thời gian mất kết nối, traffic của các account do connection đó xử lý sẽ bị dừng lại — tức là traffic không được chuyển sang các connection khác, giống như hành vi khi chỉ có một route connection duy nhất.

### Configuration reload

> 🇬🇧 *Note that although the cluster's `pool_size` configuration parameter can be changed through a configuration reload, connections between servers will likely break since there will be a mismatch between servers. It is possible though to do a rolling reload by setting the same value on all servers. Client and other connections (including dedicated account routes - see next section) will not be closed.*

Lưu ý rằng dù tham số config `pool_size` của cluster có thể thay đổi qua configuration reload, các kết nối giữa các server rất có thể sẽ bị ngắt do sự không đồng nhất giữa các server. Tuy nhiên, có thể thực hiện rolling reload bằng cách cập nhật cùng một giá trị trên tất cả các server. Các kết nối client và các kết nối khác (bao gồm dedicated account route — xem phần tiếp theo) sẽ không bị đóng.

### Monitoring

> 🇬🇧 *When monitoring is enabled, you will see that the `/routez` page now has more connections than before, which is expected.*

Khi bật monitoring, trang `/routez` sẽ hiển thị nhiều connection hơn trước — đây là hành vi bình thường.

### Tắt connection pooling

> 🇬🇧 *It is possible to disable route connection pooling by setting the `pool_size` configuration parameter to the value `-1`. When that is the case, a server will behave as a server pre-v2.10.0 and create a single route connection between its peers.*

Có thể tắt connection pooling bằng cách đặt tham số config `pool_size` thành giá trị `-1`. Khi đó, server sẽ hoạt động như phiên bản trước v2.10.0 và chỉ tạo một route connection duy nhất với mỗi peer.

> 🇬🇧 *Note that in that mode, no `accounts` list can be defined (see "Accounts Pinning" below).*

Lưu ý rằng trong chế độ này, không thể định nghĩa danh sách `accounts` (xem mục "Accounts Pinning" bên dưới).

## Account pinning

> 🇬🇧 *In addition to connection pooling, the release v2.10.0 has introduced the ability to configure a list of accounts that will have a dedicated route connection.*

Ngoài connection pooling, phiên bản v2.10.0 còn giới thiệu khả năng config danh sách các account có route connection riêng.

```
cluster {
  accounts: [acc1, acc2]
}
```

> 🇬🇧 *Note that by default, the server will create a dedicated route for the system account (no specific configuration is needed).*

Theo mặc định, server sẽ tự tạo một dedicated route cho system account mà không cần config thêm.

> 🇬🇧 *Having a dedicated route improves performance and reduces latency, but another benefit is that since the route is dedicated to an account, the account name does not need to be added to the message route protocols. Since account names can be quite long, this reduces the number of bytes that need to be transmitted in all other cases.*

Sử dụng dedicated route giúp cải thiện hiệu năng và giảm latency. Một lợi ích khác là vì route dành riêng cho một account, tên account không cần thêm vào giao thức route của message. Do tên account có thể khá dài, điều này giúp giảm số byte cần truyền trong tất cả các trường hợp còn lại.

### Xử lý khi mất kết nối

> 🇬🇧 *In the event that an account route connection breaks, automatic reconnection occurs as usual. However, while the disconnection is happening, traffic for this account is stopped.*

Khi một account route connection bị đứt, hệ thống sẽ tự động reconnect như thông thường. Tuy nhiên, trong thời gian mất kết nối, traffic của account đó sẽ bị dừng lại.

### Configuration reload

> 🇬🇧 *The `accounts` list can be modified and a configuration signal be sent to the server. All servers need to have the same list, however, it is possible to perform a rolling configuration reload.*

Danh sách `accounts` có thể được chỉnh sửa và gửi tín hiệu configuration reload đến server. Tất cả các server cần có cùng danh sách, nhưng vẫn có thể thực hiện rolling configuration reload.

> 🇬🇧 *For instance, adding an account to the list of server `A` and issuing a configuration reload will not produce an error, even though the other server in the cluster does not have that account in the list yet. A dedicated connection will not yet be established, but traffic for this account in the pooled connection currently handling it will stop. When the configuration reload happens on the other server, a dedicated connection will then be established and this account's traffic will resume.*

Ví dụ, thêm một account vào danh sách của server `A` và thực hiện configuration reload sẽ không sinh lỗi, dù server còn lại trong cluster chưa có account đó trong danh sách. Lúc này chưa có dedicated connection nào được tạo, nhưng traffic của account đó trên pooled connection đang xử lý nó sẽ bị dừng. Khi configuration reload được thực hiện trên server còn lại, dedicated connection mới được thiết lập và traffic của account sẽ tiếp tục.

> 🇬🇧 *When removing an account from the list and issuing a configuration reload, the connection for this account will be closed, and traffic for this account will stop. Other server(s) that still have this account configured with a dedicated connection will fail to reconnect. When they are also sent the configuration reload (with updated `accounts` configuration), the account traffic will now be handled by a connection in the pool.*

Khi xóa một account khỏi danh sách và thực hiện configuration reload, connection của account đó sẽ bị đóng và traffic của nó sẽ dừng lại. Các server khác vẫn còn config dedicated connection cho account này sẽ không thể reconnect. Khi chúng cũng nhận được configuration reload (với config `accounts` đã cập nhật), traffic của account sẽ được xử lý bởi một connection trong pool.

> 🇬🇧 *Note that configuration reload of changes in the `accounts` list do not affect existing pool connections, and therefore should not affect traffic for other accounts.*

Lưu ý rằng việc reload config thay đổi trong danh sách `accounts` không ảnh hưởng đến các pool connection hiện tại, và do đó cũng không ảnh hưởng đến traffic của các account khác.

### Monitoring

> 🇬🇧 *When monitoring is enabled, the route connection's information now has a new field called `account` that displays the name of the account this route is for.*

Khi bật monitoring, thông tin route connection sẽ có thêm trường mới là `account` hiển thị tên account mà route đó phục vụ.

### Tắt connection pooling

> 🇬🇧 *As indicated in the connection pooling section, if `pool_size` is set to `-1`, the `accounts` list cannot be configured nor would be in use.*

Như đã đề cập trong phần connection pooling, nếu `pool_size` được đặt thành `-1`, danh sách `accounts` sẽ không thể config và cũng sẽ không có hiệu lực.

### Kết nối với server phiên bản cũ

> 🇬🇧 *Although it is recommended that all servers part of the same cluster be at the same version number, a v2.10.0 server will be able to connect to an older server and in that case create a single route to that server. This allows for an easy deployment of a v2.10.0 release into an existing cluster running an older release.*

Dù khuyến nghị tất cả các server trong cùng cluster nên chạy cùng phiên bản, server v2.10.0 vẫn có thể kết nối với server phiên bản cũ hơn và trong trường hợp đó chỉ tạo một route duy nhất đến server đó. Điều này cho phép deploy (triển khai) phiên bản v2.10.0 vào cluster đang chạy phiên bản cũ một cách dễ dàng.

## Compression

> 🇬🇧 *Release v2.10.0 introduces the ability to configure compression between servers having route connections. The current compression algorithm used is [S2, an extension of Snappy](https://github.com/klauspost/compress/tree/master/s2#s2-compression). By default, routes do not use compression and it needs to be explicitly enabled.*

Phiên bản v2.10.0 giới thiệu khả năng config compression giữa các server có route connection. Thuật toán compression hiện tại được sử dụng là [S2, phần mở rộng của Snappy](https://github.com/klauspost/compress/tree/master/s2#s2-compression). Theo mặc định, route không dùng compression và cần được bật tường minh.

```
cluster {
  compression: {
    mode: accept
  }
}
```

### Các chế độ Compression

> 🇬🇧 *There are several modes of compression and there is no requirement to have the same mode between routed servers.*

Có nhiều chế độ compression khác nhau và các server được route đến nhau không cần phải dùng cùng một chế độ.

- `off` - Tắt hoàn toàn compression cho mọi route giữa server và peer.
- `accept` (mặc định) - Không khởi tạo compression, nhưng chấp nhận chế độ compression của peer kết nối đến.
- `s2_fast` - Bật compression, ưu tiên tốc độ hơn tỉ lệ nén.
- `s2_better` - Bật compression, cân bằng giữa tốc độ và tỉ lệ nén.
- `s2_best` - Bật compression, ưu tiên tỉ lệ nén hơn tốc độ.
- `s2_auto` - Tự chọn chế độ `s2_*` phù hợp dựa trên round-trip time (RTT) đo được giữa server và peer. Xem `rtt_thresholds` bên dưới.

### Ngưỡng round-trip time

> 🇬🇧 *When `s2_auto` compression is used, it relies on a `rtt_thresholds` option, which is a list of three latency thresholds that dictate increasing or decreasing the compression mode.*

Khi dùng compression `s2_auto`, hệ thống dựa vào tùy chọn `rtt_thresholds` — một danh sách ba ngưỡng latency xác định việc tăng hoặc giảm chế độ compression.

```
cluster {
  compression: {
    mode: s2_auto
    rtt_thresholds: [10ms, 50ms, 100ms]
  }
}
```

> 🇬🇧 *The default `rtt_thresholds` value is `[10ms, 50ms, 100ms]`. The way to read this is that if the RTT is under 10ms, no compression is applied. Once 10ms is reached, `s2_fast` is applied and so on with the remaining two thresholds for `s2_better` and `s2_best`.*

Giá trị mặc định của `rtt_thresholds` là `[10ms, 50ms, 100ms]`. Cách hiểu: nếu RTT dưới 10ms thì không áp dụng compression; khi đạt 10ms thì áp dụng `s2_fast`, và tương tự với hai ngưỡng còn lại cho `s2_better` và `s2_best`.

### Configuration reload

> 🇬🇧 *The `compression` configuration can be changed through configuration reload. If the value is changed from `off` to anything else, then connections are closed and recreated, same as if the compression mode was set to something and disabled by setting it to `off`.*

Config `compression` có thể thay đổi thông qua configuration reload. Nếu giá trị thay đổi từ `off` sang bất kỳ giá trị nào khác, các connection sẽ bị đóng và tạo lại — tương tự như khi compression mode được bật rồi tắt bằng cách đặt thành `off`.

> 🇬🇧 *For all other compression modes, the mode is changed dynamically without a need to close the route connections.*

Đối với tất cả các chế độ compression khác, chế độ được thay đổi động mà không cần đóng route connection.

### Monitoring

> 🇬🇧 *When monitoring is enabled, the route connection's information now has a new field called `compression` that displays the current compression mode. It can be `off` or any other mode described above. Note that `s2_auto` is not displayed, instead, what will be displayed is the _current mode_, say `s2_best` or `s2_uncompressed`.*

Khi bật monitoring, thông tin route connection sẽ có thêm trường mới là `compression` hiển thị chế độ compression hiện tại. Giá trị có thể là `off` hoặc bất kỳ chế độ nào đã mô tả ở trên. Lưu ý rằng `s2_auto` sẽ không được hiển thị; thay vào đó sẽ hiển thị _chế độ hiện tại_, ví dụ `s2_best` hoặc `s2_uncompressed`.

> 🇬🇧 *If connected to an older server, the `compression` field will display `not supported`.*

Nếu kết nối đến server phiên bản cũ hơn, trường `compression` sẽ hiển thị `not supported`.

### Kết nối với server phiên bản cũ

> 🇬🇧 *It is possible to have a v2.10.0+ server, with a compression mode configured, connect to an older server that does not support compression. The connection will simply not use compression.*

Server v2.10.0+ đã config compression mode vẫn có thể kết nối với server phiên bản cũ không hỗ trợ compression. Khi đó, kết nối đơn giản sẽ không dùng compression.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **deploy**: triển khai
- **node**: một server trong cluster
- **server**: máy chủ