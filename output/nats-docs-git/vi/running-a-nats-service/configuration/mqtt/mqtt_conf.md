---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/mqtt/mqtt_conf
title: Cấu hình MQTT
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Cấu hình MQTT

> 🇬🇧 *To enable MQTT support in the server, add a `mqtt` configuration block in the server's configuration file like the following:*

Để bật hỗ trợ MQTT trên server, thêm block config (cấu hình) `mqtt` vào file cấu hình của server như sau:

```
mqtt {
    # Specify a host and port to listen for websocket connections
    #
    # listen: "host:port"
    # It can also be configured with individual parameters,
    # namely host and port.
    #
    # host: "hostname"
    port: 1883

    # TLS configuration.
    #
    tls {
        cert_file: "/path/to/cert.pem"
        key_file: "/path/to/key.pem"

        # Root CA file
        #
        # ca_file: "/path/to/ca.pem"

        # If true, require and verify client certificates.
        #
        # verify: true

        # TLS handshake timeout in fractional seconds.
        #
        # timeout: 2.0

        # If true, require and verify client certificates and map certificate
        # values for authentication purposes.
        #
        # verify_and_map: true
    }

    # If no user name is provided when an MQTT client connects, will default
    # this user name in the authentication phase. If specified, this will
    # override, for MQTT clients, any `no_auth_user` value defined in the
    # main configuration file.
    # Note that this is not compatible with running the server in operator mode.
    #
    # no_auth_user: "my_username_for_apps_not_providing_credentials"

    # See below to know what is the normal way of limiting MQTT clients
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
    #     # If this is specified, the password field in the CONNECT packet has to
    #     # match this token.
    #     # token: "my_token"
    #
    #     # This overrides the main's authorization timeout. For consistency
    #     # with the main's authorization configuration block, this is expressed
    #     # as a number of seconds.
    #     # timeout: 2.0
    #}

    # This is the amount of time after which a QoS 1 message sent to
	# a client is redelivered as a DUPLICATE if the server has not
	# received the PUBACK packet on the original Packet Identifier.
	# The value has to be positive.
	# Zero will cause the server to use the default value (30 seconds).
	# Note that changes to this option is applied only to new MQTT subscriptions.
    #
    # Expressed as a time duration, with "s", "m", "h" indicating seconds,
    # minutes and hours respectively. For instance "10s" for 10 seconds,
    # "1m" for 1 minute, etc...
    #
    # ack_wait: "1m"

    # This is the amount of QoS 1 messages the server can send to
	# a subscription without receiving any PUBACK for those messages.
    # The valid range is [0..65535].
    #
	# The total of subscriptions' max_ack_pending on a given session cannot
	# exceed 65535. Attempting to create a subscription that would bring
	# the total above the limit would result in the server returning 0x80
	# in the SUBACK for this subscription.
	# Due to how the NATS Server handles the MQTT "#" wildcard, each
	# subscription ending with "#" will use 2 times the max_ack_pending value.
	# Note that changes to this option is applied only to new subscriptions.
    #
    # max_ack_pending: 100
}
```

## Phân quyền cho MQTT Users

> 🇬🇧 *A new field when configuring users allows you to restrict which type of connections are allowed for a specific user.*

Khi cấu hình user, có thể dùng một field mới để giới hạn loại kết nối được phép với từng user cụ thể.

> 🇬🇧 *Consider this configuration:*

Xem xét config sau:

```
authorization {
  users [
    {user: foo password: foopwd, permission: {...}}
    {user: bar password: barpwd, permission: {...}}
  ]
}
```

> 🇬🇧 *If an MQTT client were to connect and use the username `foo` and password `foopwd`, it would be accepted. Now suppose that you would want an MQTT client to only be accepted if it connected using the username `bar` and password `barpwd`, then you would use the option `allowed_connection_types` to restrict which type of connections can bind to this user.*

Nếu một MQTT client kết nối với username `foo` và password `foopwd`, kết nối sẽ được chấp nhận. Giả sử muốn chỉ MQTT client mới được phép kết nối bằng username `bar` và password `barpwd`, thì dùng option `allowed_connection_types` để giới hạn loại kết nối nào có thể bind vào user này.

```
authorization {
  users [
    {user: foo password: foopwd, permission: {...}}
    {user: bar password: barpwd, permission: {...}, allowed_connection_types: ["MQTT"]}
  ]
}
```

> 🇬🇧 *The option `allowed_connection_types` (also can be named `connection_types` or `clients`) as you can see is a list, and you can allow several type of clients. Suppose you want the user `bar` to accept both standard NATS clients and MQTT clients, you would configure the user like this:*

Option `allowed_connection_types` (cũng có thể đặt tên là `connection_types` hoặc `clients`) là một danh sách, cho phép nhiều loại client. Nếu muốn user `bar` chấp nhận cả NATS client thông thường lẫn MQTT client, cấu hình như sau:

```
authorization {
  users [
    {user: foo password: foopwd, permission: {...}}
    {user: bar password: barpwd, permission: {...}, allowed_connection_types: ["STANDARD", "MQTT"]}
  ]
}
```

> 🇬🇧 *The absence of `allowed_connection_types` means that all type of connections are allowed (the default behavior).*

Khi không có `allowed_connection_types`, mọi loại kết nối đều được phép (hành vi mặc định).

> 🇬🇧 *The possible values are currently:*

Các giá trị hiện có:
* `STANDARD`
* `WEBSOCKET`
* `LEAFNODE`
* `MQTT`

### Quyền đặc biệt

> 🇬🇧 *When an MQTT client creates a QoS 1 subscription, this translates to the creation of a JetStream durable subscription. To receive messages for this durable, the NATS Server creates a subscription with a subject such as `$MQTT.sub.<nuid>` and sets it as the JetStream durable's delivery subject.*

Khi MQTT client tạo một QoS 1 subscription, thao tác này tương đương với việc tạo một JetStream durable subscription. Để nhận message cho durable đó, NATS Server tạo một subscription với subject (chuỗi định danh message) chẳng hạn `$MQTT.sub.<nuid>` và gán nó làm delivery subject của JetStream durable.

> 🇬🇧 *Therefore, if you have set some permissions for the MQTT user, you need to allow subscribe permissions on `$MQTT.sub.>`.*

Do đó, nếu đã thiết lập permission (quyền truy cập) cho MQTT user, cần cấp quyền subscribe trên `$MQTT.sub.>`.

> 🇬🇧 *Here is an example of a basic configuration that sets some permissions to a user named "mqtt". As you can see, the subscribe permission `$MQTT.sub.>` is added to allow this client to create QoS 1 subscriptions.*

Dưới đây là ví dụ config cơ bản thiết lập một số permission cho user tên "mqtt". Như có thể thấy, subscribe permission `$MQTT.sub.>` được thêm vào để cho phép client này tạo QoS 1 subscription.

```
    listen: 127.0.0.1:4222
    jetstream: enabled
    authorization {
        mqtt_perms = {
            publish = ["baz"]
            subscribe = ["foo", "bar", "$MQTT.sub.>"]
        }
        users = [
            {user: mqtt, password: pass, permissions: $mqtt_perms, allowed_connection_types: ["MQTT"]}
        ]
    }
    mqtt {
        listen: 127.0.0.1:1883
    }
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **permission**: quyền truy cập
- **server**: máy chủ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message