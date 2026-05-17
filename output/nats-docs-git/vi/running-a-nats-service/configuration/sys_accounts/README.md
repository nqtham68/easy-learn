---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/sys_accounts
title: Sự Kiện Hệ Thống
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Sự Kiện Hệ Thống

> 🇬🇧 *NATS servers leverage [Accounts](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/accounts) support and generate events such as: account connect/disconnect, authentication errors, server shutdown, server stat summary.*

NATS server tận dụng hỗ trợ [Accounts](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/accounts) để tạo ra các event (sự kiện) sau:

* account connect/disconnect
* lỗi xác thực
* server shutdown
* tóm tắt thống kê server

> 🇬🇧 *In addition the server supports a limited number of requests that can be used to query for account connections, server stat summaries, and pinging servers in the cluster.*

Ngoài ra, server còn hỗ trợ một số request (yêu cầu) giới hạn dùng để truy vấn kết nối của account, tóm tắt thống kê server, và ping các server trong cluster (cụm nhiều server chạy chung).

> 🇬🇧 *These events are enabled by configuring `system_account` and [subscribing/requesting](.#available-events-and-services) using a _system account_ user.*

Các event này được bật bằng cách cấu hình `system_account` và [đăng ký/gửi request](.#available-events-and-services) thông qua một user thuộc _system account_.

> 🇬🇧 *[Accounts](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/accounts) are used so that subscriptions from your applications, say `>`, do not receive system events and vice versa. Using accounts requires either:*
> *- [Configuring authentication locally](.#local-configuration) and listing one of the accounts in `system_account`*
> *- Or by using decentralized authentication and authorization via [jwt](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/jwt) as shown in this [Tutorial](https://docs.nats.io/running-a-nats-service/configuration/sys_accounts/sys\_accounts). In this case `system_account` contains the account public key.*

[Accounts](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/accounts) được dùng để subscription từ ứng dụng của bạn, ví dụ `>`, không nhận event hệ thống và ngược lại. Để sử dụng accounts, cần một trong hai cách:

* [Cấu hình xác thực cục bộ](.#local-configuration) và liệt kê một trong các account trong `system_account`
* Hoặc dùng xác thực và phân quyền phi tập trung qua [jwt](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/jwt) như hướng dẫn trong [Tutorial](https://docs.nats.io/running-a-nats-service/configuration/sys_accounts/sys\_accounts) này. Trong trường hợp này, `system_account` chứa public key của account.

> 🇬🇧 *N.B. The default global account `$G` does not publish advisories.*

Lưu ý: Account global mặc định `$G` không phát hành advisory.

## Các Event và Service Có Sẵn

### System Account

> 🇬🇧 *The system account publishes messages under well known subject patterns.*

System account publish message theo các subject (chuỗi định danh message) pattern đã được định nghĩa sẵn.

> 🇬🇧 *Server initiated events:*

Event do server khởi tạo:

* `$SYS.ACCOUNT.<id>.CONNECT` (client kết nối)
* `$SYS.ACCOUNT.<id>.DISCONNECT` (client ngắt kết nối)
* `$SYS.ACCOUNT.<id>.SERVER.CONNS` (số kết nối của một account thay đổi)
* `$SYS.SERVER.<id>.CLIENT.AUTH.ERR` (lỗi xác thực)
* `$SYS.SERVER.<id>.STATSZ` (tóm tắt thống kê)

> 🇬🇧 *In addition other tools with system account privileges, can initiate requests (Examples can be found [here](https://docs.nats.io/running-a-nats-service/configuration/sys_accounts/sys\_accounts#system-services)):*

Ngoài ra, các tool có quyền system account cũng có thể khởi tạo request (ví dụ được liệt kê [tại đây](https://docs.nats.io/running-a-nats-service/configuration/sys_accounts/sys\_accounts#system-services)):

* `$SYS.REQ.SERVER.<id>.STATSZ` (lấy tóm tắt thống kê server)
* `$SYS.REQ.SERVER.PING` (khám phá server - trả về nhiều message)

> 🇬🇧 *[Monitoring endpoints](../monitoring.md) as listed in the table below are accessible as system services using the following subject pattern:*

Các [monitoring endpoint](../monitoring.md) (địa chỉ API cụ thể) trong bảng dưới đây có thể truy cập dưới dạng system service theo pattern subject:

* `$SYS.REQ.SERVER.<id>.<endpoint-name>` (lấy monitoring endpoint của server theo tên endpoint)
* `$SYS.REQ.SERVER.PING.<endpoint-name>` (từ tất cả server, lấy monitoring endpoint theo tên - trả về nhiều message)

| Endpoint                                                                  | Endpoint Name |
| ------------------------------------------------------------------------- | ------------- |
| [General Server Information](../monitoring.md#general-information)        | `VARZ`        |
| [Connections](../monitoring.md#connection-information)                    | `CONNZ`       |
| [Routing](../monitoring.md#route-information)                             | `ROUTEZ`      |
| [Gateways](../monitoring.md#gateway-information)                          | `GATEWAYZ`    |
| [Leaf Nodes](../monitoring.md#leaf-nodes-information)                     | `LEAFZ`       |
| [Subscription Routing](../monitoring.md#subscription-routing-information) | `SUBSZ`       |
| [JetStream](../monitoring.md#jetstream-information)                       | `JSZ`         |
| [Accounts](../monitoring.md#account-information)                          | `ACCOUNTZ`    |
| [Health](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring#health)                            | `HEALTHZ`     |

* `"$SYS.REQ.ACCOUNT.<account-id>.<endpoint-name>`(từ tất cả server, lấy monitoring endpoint của account cụ thể theo account id và tên endpoint - trả về nhiều message)

| Endpoint                                                                  | Endpoint Name |
| ------------------------------------------------------------------------- | ------------- |
| [Connections](../monitoring.md#connection-information)                    | `CONNZ`       |
| [Leaf Nodes](../monitoring.md#leaf-nodes-information)                     | `LEAFZ`       |
| [Subscription Routing](../monitoring.md#subscription-routing-information) | `SUBSZ`       |
| [JetStream](../monitoring.md#jetstream-information)                       | `JSZ`         |
| [Account](../monitoring.md#account-information)                           | `INFO`        |

> 🇬🇧 *Servers like `nats-account-server` publish system account messages when a claim is updated, the nats-server listens for them, and updates its account information accordingly:*

Các server như `nats-account-server` publish message system account khi một claim được cập nhật, nats-server lắng nghe và cập nhật thông tin account tương ứng:

* `$SYS.ACCOUNT.<id>.CLAIMS.UPDATE`

> 🇬🇧 *With these few messages you can build useful monitoring tools:*

Với một số message này, bạn có thể xây dựng các công cụ monitoring hữu ích:

* health/load của server
* client kết nối/ngắt kết nối
* kết nối của account
* lỗi xác thực

## Cấu Hình Cục Bộ

> 🇬🇧 *To make use of System events, just using accounts, your configuration can look like this:*

Để sử dụng System event với accounts, config có thể trông như sau:

```
accounts: {
    USERS: {
        users: [
            {user: a, password: a}
        ]
    },
    SYS: { 
        users: [
            {user: admin, password: changeit}
           ]
    },
}
system_account: SYS
```

> 🇬🇧 *Please note that applications now have to authenticate such that a connection can be associated with an account. In this example username and password were chosen for simplicity of the demonstration. Subscribe to all system events like this `nats sub -s nats://admin:changeit@localhost:4222 ">"` and observe what happens when you do something like `nats pub -s "nats://a:a@localhost:4222" foo bar`. Examples on how to use system services can be found [here](https://docs.nats.io/running-a-nats-service/configuration/sys_accounts/sys\_accounts#system-services).*

Lưu ý rằng các ứng dụng giờ phải xác thực để kết nối được liên kết với một account. Ví dụ này dùng username và password cho đơn giản. Subscribe tất cả system event như `nats sub -s nats://admin:changeit@localhost:4222 ">"` và quan sát kết quả khi thực hiện thao tác như `nats pub -s "nats://a:a@localhost:4222" foo bar`. Ví dụ về cách dùng system service có thể tìm thấy [tại đây](https://docs.nats.io/running-a-nats-service/configuration/sys_accounts/sys\_accounts#system-services).

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **endpoint**: địa chỉ API cụ thể
- **event**: sự kiện
- **message**: gói dữ liệu được gửi đi
- **request**: yêu cầu
- **service**: dịch vụ
- **subject**: chuỗi định danh message (giống topic)