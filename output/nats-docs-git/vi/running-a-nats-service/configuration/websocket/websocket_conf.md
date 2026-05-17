---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
description: WebSocket Configuration Example
source_url: https://docs.nats.io/running-a-nats-service/configuration/websocket/websocket_conf
title: Cấu hình WebSocket
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Cấu hình WebSocket

> 🇬🇧 *To enable WebSocket support in the server, add a `websocket` configuration block in the server's configuration file like the following:*

Để bật hỗ trợ WebSocket trên server, thêm block config (cấu hình) `websocket` vào file cấu hình của server như sau:

```text
websocket {
    # Specify a host and port to listen for websocket connections
    #
    # listen: "host:port"

    # It can also be configured with individual parameters,
    # namely host and port.
    #
    # host: "hostname"
    port: 443

    # This will optionally specify what host:port for websocket
    # connections to be advertised in the cluster.
    #
    # advertise: "host:port"

    # TLS configuration is required by default
    #
    tls {
      cert_file: "/path/to/cert.pem"
      key_file: "/path/to/key.pem"
    }

    # For test environments, you can disable the need for TLS
    # by explicitly setting this option to `true`
    #
    # no_tls: true

    # [Cross-origin resource sharing option](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).
    #
    # IMPORTANT! This option is used only when the http request presents an Origin
    # header, which is the case for web browsers. If no Origin header is present,
    # this check will not be performed.
    #
    # When set to `true`, the HTTP origin header must match the request’s hostname.
    # The default is `false`.
    #
    # same_origin: true

    # [Cross-origin resource sharing option](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).
    #
    # IMPORTANT! This option is used only when the http request presents an Origin
    # header, which is the case for web browsers. If no Origin header is present,
    # this check will not be performed.
    #
    # List of accepted origins. When empty, and `same_origin` is `false`, clients from any origin are allowed to connect.
    # This list specifies the only accepted values for the client's request Origin header. The scheme,
    # host and port must match. By convention, the absence of TCP port in the URL will be port 80
    # for an "http://" scheme, and 443 for "https://".
    #
    # allowed_origins [
    #    "http://www.example.com"
    #    "https://www.other-example.com"
    # ]

    # This enables support for compressed websocket frames
    # in the server. For compression to be used, both server
    # and client have to support it.
    #
    # compression: true

    # This is the total time allowed for the server to
    # read the client request and write the response back
    # to the client. This includes the time needed for the
    # TLS handshake.
    #
    # handshake_timeout: "2s"

    # Name for an HTTP cookie, that if present will be used as a client JWT.
    # If the client specifies a JWT in the CONNECT protocol, this option is ignored.
    # The cookie should be set by the HTTP server as described [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#restrict_access_to_cookies).
    # This setting is useful when generating NATS `Bearer` client JWTs as the
    # result of some authentication mechanism. The HTTP server after correct
    # authentication can issue a JWT for the user, that is set securely preventing
    # access by unintended scripts. Note these JWTs must be [NATS JWTs](https://docs.nats.io/nats-server/configuration/securing_nats/jwt).
    #
    # jwt_cookie: "my_jwt_cookie_name"

    # If no user name is provided when a websocket client connects, will default
    # this user name in the authentication phase. If specified, this will
    # override, for websocket clients, any `no_auth_user` value defined in the
    # main configuration file.
    # Note that this is not compatible with running the server in operator mode.
    #
    # no_auth_user: "my_username_for_apps_not_providing_credentials"

    # See below to know what is the normal way of limiting websocket clients
    # to specific users.
    # If there are no users specified in the configuration, this simple authorization
    # block allows you to override the values that would be configured in the
    # equivalent block in the main section.
    #
    # authorization {
    #     # If this is specified, the client has to provide the same username
    #     # and password to be able to connect.
    #     # username: "my_user_name"
    #     # password: "my_password"
    #
    #     # If this is specified, the password field in the CONNECT has to
    #     # match this token.
    #     # token: "my_token"
    #
    #     # This overrides the main's authorization timeout. For consistency
    #     # with the main's authorization configuration block, this is expressed
    #     # as a number of seconds.
    #     # timeout: 2.0
    #}
}
```

## Phân quyền cho WebSocket Users

### Xác thực (Authentication)

> 🇬🇧 *NATS supports different forms of authentication for clients connecting over WebSocket:*

NATS hỗ trợ nhiều hình thức xác thực cho client (bên gọi phía người dùng) kết nối qua WebSocket:

- username/password
- token
- NKEYS
- client certificates
- JWTs

> 🇬🇧 *You can get some more information about how applications connecting over WebSocket can use those different forms of authentication [here](https://github.com/nats-io/nats.ws#authentication)*

Xem thêm cách ứng dụng kết nối qua WebSocket sử dụng các hình thức xác thực này [tại đây](https://github.com/nats-io/nats.ws#authentication).

### Giới hạn loại kết nối

> 🇬🇧 *A new field when configuring users allows you to restrict which type of connections are allowed for a specific user.*

Một trường mới trong config người dùng cho phép giới hạn loại kết nối được chấp nhận cho từng user cụ thể.

> 🇬🇧 *Consider this configuration:*

Xét cấu hình sau:

```text
authorization {
  users [
    {user: foo password: foopwd, permission: {...}}
    {user: bar password: barpwd, permission: {...}}
  ]
}
```

> 🇬🇧 *If a WebSocket client were to connect and use the username `foo` and password `foopwd`, it would be accepted. Now suppose that you would want the WebSocket client to only be accepted if it connected using the username `bar` and password `barpwd`, then you would use the option `allowed_connection_types` to restrict which type of connections can bind to this user.*

Nếu một WebSocket client kết nối với username `foo` và password `foopwd`, kết nối sẽ được chấp nhận. Giả sử bạn muốn chỉ chấp nhận WebSocket client kết nối bằng username `bar` và password `barpwd`, hãy dùng tùy chọn `allowed_connection_types` để giới hạn loại kết nối được phép gắn với user này.

```text
authorization {
  users [
    {user: foo password: foopwd, permission: {...}}
    {user: bar password: barpwd, permission: {...}, allowed_connection_types: ["WEBSOCKET"]}
  ]
}
```

> 🇬🇧 *The option `allowed_connection_types` \(also can be named `connection_types` or `clients`\) as you can see is a list, and you can allow several types of clients. Suppose you want the user `bar` to accept both standard NATS clients and WebSocket clients, you would configure the user like this:*

Tùy chọn `allowed_connection_types` \(cũng có thể đặt tên là `connection_types` hoặc `clients`\) là một danh sách, cho phép nhiều loại client. Nếu muốn user `bar` chấp nhận cả NATS client thông thường lẫn WebSocket client, cấu hình như sau:

```text
authorization {
  users [
    {user: foo password: foopwd, permission: {...}}
    {user: bar password: barpwd, permission: {...}, allowed_connection_types: ["STANDARD", "WEBSOCKET"]}
  ]
}
```

> 🇬🇧 *The absence of `allowed_connection_types` means that all types of connections are allowed \(the default behavior\).*

Khi không có `allowed_connection_types`, tất cả loại kết nối đều được phép \(hành vi mặc định\).

> 🇬🇧 *The possible values are currently:*

Các giá trị hiện được hỗ trợ:

* `STANDARD`
* `WEBSOCKET`
* `LEAFNODE`
* `MQTT`

## Kết nối Leaf Node

> 🇬🇧 *You can configure remote Leaf node connections so that they connect to the Websocket port instead of the Leaf node port. See [Leafnode](../leafnodes/leafnode_conf.md#connecting-using-websocket-protocol) section.*

Có thể cấu hình remote Leaf node (một server trong cluster) để kết nối qua cổng WebSocket thay vì cổng Leaf node thông thường. Xem phần [Leafnode](../leafnodes/leafnode_conf.md#connecting-using-websocket-protocol).

## Docker

> 🇬🇧 *When running on Docker, WebSocket is not enabled by default, so you'll have to create a configuration file with the minimal entries, such as:*

Khi chạy trên Docker, WebSocket không được bật mặc định. Bạn cần tạo file cấu hình với các mục tối thiểu, ví dụ:

```text
websocket 
{
     port: 8080
     no_tls: true
}
```

> 🇬🇧 *Assuming the configuration was stored in `/tmp/nats.conf`, you can start docker as follows:*

Giả sử cấu hình được lưu tại `/tmp/nats.conf`, khởi động Docker như sau:

```bash
docker run -it --rm  -v /tmp:/container -p 8080:8080 nats -c /container/nats.conf
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **config**: cấu hình
- **node**: một server trong cluster
- **server**: máy chủ
- **token**: chuỗi xác thực