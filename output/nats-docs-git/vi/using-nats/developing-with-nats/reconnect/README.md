---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/reconnect
title: Tự động Kết nối lại (Automatic Reconnections)
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Tự động Kết nối lại

> 🇬🇧 *All the client libraries maintained on the [nats.io GitHub page](https://github.com/nats-io) will automatically attempt to re-connect if their current server connection gets disconnected for any reason. Upon re-connection the client library will automatically re-establish all the subscriptions, there is nothing for the application programmer to do.*

Toàn bộ thư viện client được duy trì trên [trang GitHub nats.io](https://github.com/nats-io) đều tự động thử kết nối lại khi mất kết nối đến server vì bất kỳ lý do nào. Sau khi kết nối lại, thư viện sẽ tự động khôi phục tất cả các subscription mà không cần lập trình viên can thiệp.

> 🇬🇧 *Unless specifically [disabled](./disable.md) client will try to re-connect to one of the servers it knows about, either through the URLs provided in the `connect` call or the URLs provided by the NATS system during earlier connects. This feature allows NATS applications and the NATS system itself to self-heal and reconfigure itself with no additional configuration or intervention.*

Trừ khi bị [tắt đi](./disable.md), client sẽ thử kết nối lại đến một trong các server mà nó biết — thông qua URL truyền vào lời gọi `connect` hoặc URL do hệ thống NATS cung cấp trong các lần kết nối trước. Tính năng này cho phép ứng dụng NATS và bản thân hệ thống NATS tự phục hồi và tự cấu hình lại mà không cần thêm cấu hình hay tác động thủ công.

> 🇬🇧 *You can adjust the [wait time](./wait.md) between connections attempts, the [maximum](./max.md) number of reconnection attempts, and adjust the size of the reconnection [buffer](./buffer.md).*

Bạn có thể điều chỉnh [thời gian chờ](./wait.md) giữa các lần thử kết nối lại, [số lần tối đa](./max.md) được phép thử lại, và kích thước buffer (vùng đệm tạm) dành cho [reconnect](./buffer.md).

## Thông báo sự kiện (Advisories)

> 🇬🇧 *Your application can register callback to receive [events](./events.md) to be notified about the following connection events:*

Ứng dụng có thể đăng ký callback (hàm được gọi lại) để nhận [event](./events.md) thông báo về các sự kiện kết nối sau:

* `ClosedCB ConnHandler`

> 🇬🇧 *The ClosedCB handler is called when a client will no longer be connected.*

Handler `ClosedCB` được gọi khi client sẽ không còn kết nối nữa.

* `DisconnectedCB ConnHandler`

> 🇬🇧 *The DisconnectedCB handler is called whenever the connection is disconnected. It will not be called if DisconnectedErrCB is set*
> 🇬🇧 ***DEPRECATED**: Use DisconnectedErrCB instead which passes error that caused the disconnect event.*

Handler `DisconnectedCB` được gọi mỗi khi kết nối bị ngắt. Sẽ không được gọi nếu `DisconnectedErrCB` đã được thiết lập.
**DEPRECATED**: Hãy dùng `DisconnectedErrCB` thay thế — handler này truyền thêm lỗi gây ra sự kiện ngắt kết nối.

* `DisconnectedErrCB ConnErrHandler`

> 🇬🇧 *The DisconnectedErrCB handler is called whenever the connection is disconnected. Disconnected error could be nil, for instance when user explicitly closes the connection.*
> 🇬🇧 ***NOTE**: DisconnectedCB will not be called if DisconnectedErrCB is set*

Handler `DisconnectedErrCB` được gọi mỗi khi kết nối bị ngắt. Lỗi truyền vào có thể là nil, ví dụ khi người dùng chủ động đóng kết nối.
**LƯU Ý**: `DisconnectedCB` sẽ không được gọi nếu `DisconnectedErrCB` đã được thiết lập.

* `ReconnectedCB ConnHandler`

> 🇬🇧 *The ReconnectedCB handler is called whenever the connection is successfully reconnected.*

Handler `ReconnectedCB` được gọi mỗi khi kết nối lại thành công.

* `DiscoveredServersCB ConnHandler`

> 🇬🇧 *The DiscoveredServersCB handler is called whenever a new server has joined the cluster.*

Handler `DiscoveredServersCB` được gọi mỗi khi có server mới gia nhập cluster.

* `AsyncErrorCB ErrHandler`

> 🇬🇧 *The AsyncErrorCB handler is called whenever asynchronous connection errors happen (e.g. slow consumer errors)*

Handler `AsyncErrorCB` được gọi khi xảy ra lỗi kết nối bất đồng bộ (ví dụ: lỗi slow consumer).

## Thuộc tính timeout kết nối

* `Timeout time.Duration`

> 🇬🇧 *Timeout sets the timeout for a Dial operation on a connection. Default is `2 * time.Second`*

`Timeout` thiết lập timeout (thời gian chờ tối đa) cho thao tác Dial khi kết nối. Mặc định là `2 * time.Second`

* `PingInterval time.Duration`

> 🇬🇧 *PingInterval is the period at which the client will be sending ping commands to the server, disabled if 0 or negative. Default is `2 * time.Minute`*

`PingInterval` là khoảng thời gian client gửi lệnh ping đến server, bị vô hiệu hóa nếu bằng 0 hoặc âm. Mặc định là `2 * time.Minute`

* `MaxPingsOut int`

> 🇬🇧 *MaxPingsOut is the maximum number of pending ping commands that can be awaiting a response before raising an ErrStaleConnection error. Default is `2`*

`MaxPingsOut` là số lệnh ping tối đa có thể chờ phản hồi trước khi phát sinh lỗi `ErrStaleConnection`. Mặc định là `2`

## Thuộc tính kết nối lại

> 🇬🇧 *Besides the error and advisory callbacks mentioned above you can also set a few reconnection attributes in the connection options:*

Ngoài các callback thông báo lỗi đã đề cập, bạn còn có thể thiết lập một số thuộc tính kết nối lại trong connection options:

* `AllowReconnect bool`

> 🇬🇧 *AllowReconnect enables reconnection logic to be used when we encounter a disconnect from the current server. Default is `true`*

`AllowReconnect` bật logic kết nối lại khi client bị ngắt khỏi server hiện tại. Mặc định là `true`

* `MaxReconnect int`

> 🇬🇧 *MaxReconnect sets the number of reconnect attempts that will be tried before giving up. If negative, then it will never give up trying to reconnect. Default is `60`*

`MaxReconnect` thiết lập số lần thử kết nối lại tối đa trước khi bỏ cuộc. Nếu là số âm, client sẽ thử mãi mãi. Mặc định là `60`

* `ReconnectWait time.Duration`

> 🇬🇧 *ReconnectWait sets the time to backoff after attempting to (and failing to) reconnect. Default is `2 * time.Second`*

`ReconnectWait` thiết lập thời gian backoff (chiến lược chờ tăng dần giữa các lần retry) sau mỗi lần thử kết nối lại thất bại. Mặc định là `2 * time.Second`

* `CustomReconnectDelayCB ReconnectDelayHandler`

> 🇬🇧 *CustomReconnectDelayCB is invoked after the library tried every URL in the server list and failed to reconnect. It passes to the user the current number of attempts. This function returns the amount of time the library will sleep before attempting to reconnect again. It is strongly recommended that this value contains some jitter to prevent all connections to attempt reconnecting at the same time.*

`CustomReconnectDelayCB` được gọi sau khi thư viện đã thử toàn bộ URL trong danh sách server mà vẫn không kết nối lại được. Hàm nhận vào số lần thử hiện tại và trả về khoảng thời gian thư viện sẽ chờ trước khi thử lại. Rất khuyến nghị thêm jitter vào giá trị trả về để tránh tình trạng tất cả các kết nối đồng loạt thử lại cùng một lúc.

* `ReconnectJitter time.Duration`

> 🇬🇧 *ReconnectJitter sets the upper bound for a random delay added to *ReconnectWait* during a reconnect when no TLS is used. Note that any jitter is capped with ReconnectJitterMax. Default is `100 * time.Millisecond`*

`ReconnectJitter` thiết lập giới hạn trên cho độ trễ ngẫu nhiên cộng thêm vào *ReconnectWait* khi kết nối lại mà không dùng TLS. Lưu ý rằng jitter bị giới hạn bởi `ReconnectJitterMax`. Mặc định là `100 * time.Millisecond`

* `ReconnectJitterTLS time.Duration`

> 🇬🇧 *ReconnectJitterTLS sets the upper bound for a random delay added to *ReconnectWait* during a reconnect when TLS is used. Note that any jitter is capped with ReconnectJitterMax. Default is `1 * time.Second`*

`ReconnectJitterTLS` thiết lập giới hạn trên cho độ trễ ngẫu nhiên cộng thêm vào *ReconnectWait* khi kết nối lại có dùng TLS. Lưu ý rằng jitter bị giới hạn bởi `ReconnectJitterMax`. Mặc định là `1 * time.Second`

* `ReconnectBufSize int`

> 🇬🇧 *ReconnectBufSize is the size of the backing bufio during reconnect. Once this has been exhausted publish operations will return an error. Default is `8 * 1024 * 1024`*

`ReconnectBufSize` là kích thước buffer bufio dùng khi đang kết nối lại. Khi buffer này đầy, các thao tác publish sẽ trả về lỗi. Mặc định là `8 * 1024 * 1024`

* `RetryOnFailedConnect bool`

> 🇬🇧 *RetryOnFailedConnect sets the connection in reconnecting state right away if it can't connect to a server in the initial set. The *MaxReconnect* and *ReconnectWait* options are used for this process, similarly to when an established connection is disconnected. If a ReconnectHandler is set, it will be invoked on the first successful reconnect attempt (if the initial connect fails), and if a ClosedHandler is set, it will be invoked if it fails to connect (after exhausting the MaxReconnect attempts). Default is `false`*

`RetryOnFailedConnect` đưa kết nối vào trạng thái reconnecting ngay lập tức nếu không thể kết nối đến bất kỳ server nào trong danh sách ban đầu. Quá trình này sử dụng các tùy chọn *MaxReconnect* và *ReconnectWait*, tương tự như khi một kết nối đang hoạt động bị ngắt. Nếu đã thiết lập `ReconnectHandler`, nó sẽ được gọi khi lần thử kết nối lại đầu tiên thành công; nếu đã thiết lập `ClosedHandler`, nó sẽ được gọi khi client thất bại hoàn toàn (sau khi hết số lần `MaxReconnect`). Mặc định là `false`

## Thuật ngữ trong bài

- **backoff**: chiến lược chờ tăng dần giữa các lần retry
- **buffer**: vùng đệm tạm
- **callback**: hàm được gọi lại
- **client**: bên gọi (phía người dùng)
- **cluster**: cụm nhiều server chạy chung
- **event**: sự kiện
- **server**: máy chủ
- **timeout**: thời gian chờ tối đa
- **TLS**: mã hóa TLS