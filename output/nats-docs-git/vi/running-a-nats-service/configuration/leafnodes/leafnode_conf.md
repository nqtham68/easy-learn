---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/leafnodes/leafnode_conf
title: Cấu hình Leaf Node
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Cấu hình Leaf Node

## Block Cấu hình `leafnodes`

> 🇬🇧 *The leaf node configuration block is used to configure incoming as well as outgoing leaf node connections. Most properties are for the configuration of incoming connections. The properties `remotes` and `reconnect` are for outgoing connections.*

Block config (cấu hình) của leaf node dùng để thiết lập kết nối leaf node theo cả hai chiều: đến và đi. Hầu hết các thuộc tính phục vụ cho kết nối đến (incoming). Hai thuộc tính `remotes` và `reconnect` dành cho kết nối đi (outgoing).

| Property        | Description                                                                                                                                                                                |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `host`          | Interface nơi server lắng nghe kết nối leafnode đến.                                                                                                                  |
| `port`          | Port nơi server lắng nghe kết nối leafnode đến (mặc định là 7422).                                                                                                     |
| `listen`        | Kết hợp `host` và `port` thành `<host>:<port>`                                                                                                                                              |
| `tls`           | Block cấu hình TLS (giống với [cấu hình `tls`](../securing_nats/tls.md) của nats-server).                                                     |
| `advertise`     | Hostport `<host>:<port>` để quảng bá cách leaf node liên lạc với server này. Hữu ích khi triển khai cluster có NAT.                                                           |
| `no_advertise`  | Nếu `true`, server sẽ không được quảng bá đến các leaf node.                                                                                                                                |
| `authorization` | Block Authorization. [**Xem phần Authorization Block bên dưới**](./leafnode_conf.md#authorization-block).                                                                                    |
| `remotes`       | Danh sách các entry [`remote`](./leafnode_conf.md#leafnode-remotes-entry-block) chỉ định server mà leafnode client có thể kết nối tới.                                                 |
| `reconnect`     | Khoảng thời gian (giây) giữa các lần thử kết nối lại đến remote server.                                                                                                               |
| `compression`   | Cấu hình nén kết nối leafnode tương tự [cluster routes](../clustering/v2_routes.md). Mặc định là `s2_auto`. Xem chi tiết [tại đây](../clustering/v2_routes.md#compression). |

## Block TLS

_Kể từ NATS v2.10.0_

> 🇬🇧 *The `tls` block for `leafnodes` configuration has an additional field enabling a _TLS-first handshake_ between the remote and the accepting server.*

Block `tls` trong cấu hình `leafnodes` có thêm một trường mới cho phép thực hiện _TLS-first handshake_ giữa remote và server chấp nhận kết nối.

| Property          | Description                                                                                                                   |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `handshake_first` | Nếu `true` ở phía chấp nhận (accepting), các remote leafnode cũng phải có cấu hình này trong phần `remotes`. |

### Phía chấp nhận (Accepting side)

> 🇬🇧 *Since Leafnodes can connect to a variety of servers, the ability to indicate if the TLS handshake should be done first is configured in 2 places. The _accepting_ side is in the `tls` block of the `leafnodes` block.*

Vì Leafnode có thể kết nối đến nhiều loại server khác nhau, việc chỉ định TLS handshake thực hiện trước hay không được cấu hình ở 2 chỗ. Phía _accepting_ nằm trong block `tls` của block `leafnodes`.

```
leafnodes {
  port: 7422
  tls {
    handshake_first: true
    # other TLS fields...
  }
}
```

> 🇬🇧 *With the above configuration, an older server, or a server that does not have the remote configuration also configured with `handshake_first: true`, will fail to create a leafnode connection because the accepting-side server will initiate the TLS handshake while the soliciting side will wait for the INFO protocol to be received.*

Với cấu hình trên, một server cũ hơn, hoặc server chưa có `handshake_first: true` trong cấu hình remote, sẽ không thể tạo kết nối leafnode — vì phía accepting sẽ khởi động TLS handshake trong khi phía soliciting vẫn đang chờ nhận INFO protocol.

### Phía remote (Remote side)

> 🇬🇧 *To indicate that a leafnode connection should perform the TLS handshake first, it needs to be configured in the remote configuration:*

Để chỉ định rằng kết nối leafnode cần thực hiện TLS handshake trước, cần thiết lập trong cấu hình remote:

```
leafnodes {
  remotes [
    {
      urls: ["tls://example:7422"]
      tls: {
         handshake_first: true
         # other TLS fields...
      }
    }
  ]
}
```

> 🇬🇧 *If the remote is configured as such but the server it is connecting to does not have `handshake_first: true` configured, the connection will fail since the solicit side is performing a TLS handshake but will receive an INFO protocol in clear.*

Nếu remote đã cấu hình như trên nhưng server nhận kết nối chưa có `handshake_first: true`, kết nối sẽ thất bại — phía solicit thực hiện TLS handshake nhưng lại nhận INFO protocol dạng plain text.

## Block Authorization

> **ℹ️ Info:**
> A leaf node can authenticate against any user account on the hub (the incoming side of the connection), including those defined in the accounts themselves. This authorization block is therefore optional if appropriate account users already exist.
>
> Whether configuring users in the account or in this dedicated authorization block is more convenient will depend on your deployment style.

> 🇬🇧 *A leaf node can authenticate against any user account on the hub (the incoming side of the connection), including those defined in the accounts themselves. This authorization block is therefore optional if appropriate account users already exist. Whether configuring users in the account or in this dedicated authorization block is more convenient will depend on your deployment style.*

Leaf node có thể xác thực với bất kỳ user account nào trên hub (phía incoming), kể cả những account được định nghĩa trực tiếp trong account đó. Block authorization này là tùy chọn nếu các account user phù hợp đã tồn tại. Việc chọn cấu hình user trong account hay trong block authorization riêng này phụ thuộc vào cách triển khai của bạn.

| Property   | Description                                                                                                                         |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `user`     | Tên người dùng cho kết nối leaf node.                                                                                              |
| `password` | Mật khẩu cho user entry.                                                                                                        |
| `account`  | [Account](../securing_nats/accounts.md) mà kết nối leaf node này sẽ được gán vào.                                               |
| `timeout`  | Số giây tối đa chờ xác thực leaf node.                                                                                     |
| `users`    | Danh sách credential và account gán cho kết nối leaf node. [**Xem phần Users Block bên dưới**](./leafnode_conf.md#users-block). |

### Users Block

| Property   | Description                                                                           |
| ---------- | ------------------------------------------------------------------------------------- |
| `user`     | Tên người dùng cho kết nối leaf node.                                                |
| `password` | Mật khẩu cho user entry.                                                          |
| `account`  | [Account](../securing_nats/accounts.md) mà kết nối leaf node này sẽ được gán vào. |

> 🇬🇧 *Here are some examples of using basic user/password authentication for leaf nodes (note while this is using accounts it is not using JWTs)*

Dưới đây là một số ví dụ về xác thực bằng username/password cơ bản cho leaf node (lưu ý: dùng account nhưng không dùng JWT):

Chế độ singleton:

```
leafnodes {
  port: ...
  authorization {
    user: leaf
    password: secret
    account: TheAccount
  }
}
```

> 🇬🇧 *With above configuration, if a soliciting server creates a Leafnode connection with url: `nats://leaf:secret@host:port`, then the accepting server will bind the leafnode connection to the account "TheAccount". This account needs to exist otherwise the connection will be rejected.*

Với cấu hình trên, nếu server gọi đến tạo kết nối Leafnode với url `nats://leaf:secret@host:port`, server chấp nhận sẽ gán kết nối leafnode vào account "TheAccount". Account này phải tồn tại, nếu không kết nối sẽ bị từ chối.

Chế độ multi-users:

```
leafnodes {
  port: ...
  authorization {
    users = [
      {user: leaf1, password: secret, account: account1}
      {user: leaf2, password: secret, account: account2}
    ]
  }
}
```

> 🇬🇧 *With the above, if a server connects using `leaf1:secret@host:port`, then the accepting server will bind the connection to account `account1`. If using `leaf2` user, then the accepting server will bind to connection to `account2`.*

Với cấu hình trên, nếu server kết nối bằng `leaf1:secret@host:port`, server chấp nhận sẽ gán kết nối vào account `account1`. Nếu dùng user `leaf2`, kết nối sẽ được gán vào `account2`.

> 🇬🇧 *If username/password (either singleton or multi-users) is defined, then the connecting server MUST provide the proper credentials otherwise the connection will be rejected.*

Khi đã định nghĩa username/password (dù singleton hay multi-users), server kết nối BẮT BUỘC phải cung cấp credential (thông tin đăng nhập) đúng, nếu không kết nối sẽ bị từ chối.

> 🇬🇧 *If no username/password is provided, it is still possible to provide the account the connection should be associated with:*

Nếu không có username/password, vẫn có thể chỉ định account mà kết nối sẽ được gán vào:

```
leafnodes {
  port: ...
  authorization {
    account: TheAccount
  }
}
```

> 🇬🇧 *With the above, a connection without credentials will be bound to the account "TheAccount".*

Với cấu hình trên, một kết nối không có credential sẽ được gán vào account "TheAccount".

> 🇬🇧 *If other form of credentials are used (jwt, nkey or other), then the server will attempt to authenticate and if successful associate to the account for that specific user. If the user authentication fails (wrong password, no such user, etc..) the connection will be also rejected.*

Nếu dùng các dạng credential khác (jwt, nkey hoặc loại khác), server sẽ thử xác thực và nếu thành công sẽ gán kết nối vào account của user đó. Nếu xác thực thất bại (sai mật khẩu, không tìm thấy user, v.v.), kết nối cũng sẽ bị từ chối.

## Block Entry LeafNode `remotes`

| Property         | Description                                                                                                                                                                                                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`            | URL của Leafnode (scheme nên là `nats-leaf`).                                                                                                                                                                                                                        |
| `urls`           | Mảng URL của Leafnode. Hỗ trợ nhiều URL để discovery, ví dụ: urls: \[ "nats-leaf://host1:7422", "nats-leaf://host2:7422" ]                                                                                                                                             |
| `no_randomize`   | Nếu true, luôn thử kết nối theo thứ tự các URL trong danh sách. Mặc định là xáo trộn danh sách URL và bắt đầu kết nối từ một URL ngẫu nhiên.                                                                                              |
| `account`        | Tên [Account](../securing_nats/accounts.md) hoặc JWT public key xác định account cục bộ được gán vào remote server này. Mọi traffic trên account này sẽ được chuyển tiếp đến remote server.                                                                   |
| `deny_imports`    | Danh sách subject (chuỗi định danh message) sẽ không được import qua kết nối leaf node này. Subscription đến các subject đó sẽ không được lan truyền lên hub.                                                                                                                           |
| `deny_exports`    | Danh sách subject sẽ không được export qua kết nối leaf node này. Subscription đến các subject đó sẽ không được lan truyền vào leaf node.                                                                                      |
| `credentials`    | File credential dùng để kết nối đến leafnode server.                                                                                                                |
| `nkey`    | Nkey dùng để kết nối đến leafnode server.                                                                                                                            |
| `tls`            | Block [cấu hình TLS](./leafnode_conf.md#tls-configuration-block). Leafnode client sẽ dùng chứng chỉ TLS được chỉ định khi kết nối/xác thực.                                                                                                                |
| `ws_compression` | Khi kết nối bằng giao thức [WebSocket](./leafnode_conf.md#connecting-using-websocket-protocol), boolean này (`true` hoặc `false`) báo cho remote server biết muốn dùng nén. Mặc định là `false`.                                                 |
| `ws_no_masking`  | Khi kết nối bằng giao thức [WebSocket](./leafnode_conf.md#connecting-using-websocket-protocol), boolean này báo remote server không muốn mask các WebSocket frame gửi đi. Mặc định là `false`, tức là frame gửi đi sẽ được mask. |
| `compression`   | Cấu hình nén kết nối leafnode tương tự [cluster routes](../clustering/v2_routes.md). Mặc định là `s2_auto`. Xem chi tiết [tại đây](../clustering/v2_routes.md#compression). |
| `hub`   | Mặc định là false. Nếu đặt true, vai trò của leaf node và hub sẽ bị đảo ngược, cho phép hub khởi tạo kết nối leaf node đến leaf. |
| `first_info_timeout`   | Mặc định `1s`. Thông tin đầu tiên hub (phía incoming) gửi về sẽ là metadata của server. Client chỉ chờ `first_info_timeout` trước khi bỏ cuộc. Hữu ích khi có khả năng port phía bên kia không phải NATS server hoặc không phải port chấp nhận kết nối leaf node — trong trường hợp đó client sẽ chờ mãi để nhận metadata. |


### Signature Handler

> 🇬🇧 *As of NATS Server v.2.9.0, for users embedding the NATS Server, it is possible to replace the use of the credentials file by a signature callback which will sign the `nonce` and provide the JWT in the `CONNECT` protocol. The `RemoteLeafOpts` has a new field:*

Từ NATS Server v.2.9.0, với người dùng nhúng NATS Server, có thể thay thế file credential bằng một signature callback — callback này sẽ ký `nonce` và cung cấp JWT trong protocol `CONNECT`. `RemoteLeafOpts` có thêm một trường mới:

```go
SignatureCB  SignatureHandler
```

> 🇬🇧 *The callback definition is:*

Định nghĩa của callback là:

```go
// SignatureHandler is used to sign a nonce from the server while
// authenticating with Nkeys. The callback should sign the nonce and
// return the JWT and the raw signature.
type SignatureHandler func([]byte) (string, []byte, error)
```

> 🇬🇧 *And example of how to use it can be found [here](https://github.com/nats-io/nats-server/blob/7baf7bd8870a0719e3692e6523b09a14653f717d/server/leafnode_test.go#L4402)*

Ví dụ cách sử dụng có thể xem [tại đây](https://github.com/nats-io/nats-server/blob/7baf7bd8870a0719e3692e6523b09a14653f717d/server/leafnode_test.go#L4402).

### Kết nối bằng giao thức WebSocket

> 🇬🇧 *Since NATS 2.2.0, Leaf nodes support outbound WebSocket connections by specifying `ws` as the scheme component of the remote server URLs:*

Từ NATS 2.2.0, Leaf node hỗ trợ kết nối WebSocket chiều ra bằng cách chỉ định `ws` làm scheme trong URL của remote server:

```
leafnodes {
  remotes [
    {urls: ["ws://hostname1:443", "ws://hostname2:443"]}
  ]
}
```

> 🇬🇧 *Note that if a URL has the `ws` scheme, all URLs the list must be `ws`. You cannot mix and match. Therefore this would be considered an invalid configuration:*

Lưu ý: nếu một URL có scheme `ws`, tất cả URL trong danh sách đều phải là `ws`. Không thể dùng lẫn lộn. Vì vậy cấu hình sau sẽ bị coi là không hợp lệ:

```
  remotes [
    # Invalid configuration that will prevent the server from starting
    {urls: ["ws://hostname1:443", "nats://hostname2:7422"]}
  ]
```

> 🇬🇧 *Note that the decision to make a TLS connection is not based on `wss://` (as opposed to `ws://`) but instead in the presence of a TLS configuration in the `leafnodes{}` or the specific remote configuration block.*

Lưu ý: quyết định dùng kết nối TLS không dựa trên `wss://` (khác với `ws://`) mà dựa vào việc có block cấu hình TLS trong `leafnodes{}` hoặc trong block cấu hình remote cụ thể.

> 🇬🇧 *To configure Websocket in the remote server, check the [Websocket](../websocket) section.*

Để cấu hình WebSocket trên remote server, xem phần [Websocket](../websocket).

### Block Cấu hình `tls`

| Property            | Description                                                                                                                |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `cert_file`         | File chứng chỉ TLS.                                                                                                      |
| `key_file`          | File key của chứng chỉ TLS.                                                                                                  |
| `ca_file`           | File CA (Certificate Authority) TLS.                                                                                            |
| `insecure`          | Bỏ qua xác minh chứng chỉ.                                                                                             |
| `verify`            | Nếu `true`, yêu cầu và xác minh chứng chỉ client.                                                                         |
| `verify_and_map`    | Nếu `true`, yêu cầu, xác minh chứng chỉ client và dùng giá trị từ chứng chỉ cho mục đích xác thực.       |
| `cipher_suites`     | Khi được đặt, chỉ các TLS cipher suite được chỉ định mới được phép. Giá trị phải khớp với phiên bản golang dùng để build server. |
| `curve_preferences` | Danh sách TLS cipher curve sử dụng theo thứ tự.                                                                                 |
| `timeout`           | Timeout của TLS handshake tính bằng giây (hỗ trợ phần thập phân).                                                               |

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **handler**: hàm xử lý
- **node**: một server trong cluster
- **port**: cổng kết nối
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)
- **timeout**: thời gian chờ tối đa
- **TLS**: mã hóa TLS