---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/monitoring
title: Giám sát (Monitoring)
translated: true
translated_at: '2026-05-13T00:00:00Z'
---

# Giám sát (Monitoring)

## Giám sát NATS

> 🇬🇧 *To monitor the NATS messaging system, `nats-server` provides a lightweight HTTP server on a dedicated monitoring port. The monitoring server provides several endpoints, providing statistics and other information about the following:*

Để giám sát hệ thống NATS, `nats-server` cung cấp một HTTP server nhẹ trên một port giám sát riêng. Server giám sát này cung cấp nhiều endpoint (địa chỉ API cụ thể) trả về số liệu thống kê và thông tin về các mục sau:

* [Thông tin Server tổng quát (`/varz`)](#general-information-varz)
* [Kết nối (`/connz`)](#connection-information-connz)
* [Routing (`/routez`)](#route-information-routez)
* [Gateway (`/gatewayz`)](#gateway-information-gatewayz)
* [Leaf Nodes (`/leafz`)](#leaf-node-information-leafz)
* [Subscription Routing (`/subsz`)](#subscription-routing-information-subsz)
* [Thông tin Account (`/accountz`)](#account-information-accountz)
* [Thống kê Account (`/accstatz`)](#account-statistics-accstatz)
* [Thông tin JetStream (`/jsz`)](#jetstream-information-jsz)
* [Health (`/healthz`)](#health-healthz)

> 🇬🇧 *All endpoints return a JSON object.*

Tất cả các endpoint đều trả về một JSON object.

> 🇬🇧 *Note that info from these monitoring endpoints is also available through [System services](../../configuration/sys_accounts#system-account)*

Lưu ý: thông tin từ các monitoring endpoint này cũng có thể truy cập qua [System services](../../configuration/sys_accounts#system-account).

> 🇬🇧 *The NATS monitoring endpoints support [JSONP](https://en.wikipedia.org/wiki/JSONP) and [CORS](https://en.wikipedia.org/wiki/Cross-origin\_resource\_sharing#How\_CORS\_works), making it easy to create single page monitoring web applications. Part of the NATS ecosystem is a tool called [nats-top](https://docs.nats.io/using-nats/nats-tools/nats\_top) that visualizes data from these endpoints on the command line.*

Các monitoring endpoint của NATS hỗ trợ [JSONP](https://en.wikipedia.org/wiki/JSONP) và [CORS](https://en.wikipedia.org/wiki/Cross-origin\_resource\_sharing#How\_CORS\_works), giúp dễ dàng xây dựng ứng dụng web giám sát dạng single page. Trong hệ sinh thái NATS còn có công cụ [nats-top](https://docs.nats.io/using-nats/nats-tools/nats\_top) để hiển thị dữ liệu từ các endpoint này ngay trên command line.

> **⚠️ Cảnh báo:**
> `nats-server` không có authentication/authorization cho monitoring endpoint. Khi có kế hoạch mở `nats-server` ra internet, hãy đảm bảo không để lộ monitoring port. Mặc định, monitoring bind vào tất cả các interface `0.0.0.0`, vì vậy hãy cân nhắc giới hạn về `localhost` hoặc thiết lập firewall phù hợp.

### Bật tính năng giám sát

> 🇬🇧 *Monitoring can be enabled in [server configuration](../../configuration#monitoring-and-tracing) or as a server [command-line option](../../running/flags.md#server-options). The conventional port is `8222`.*

Có thể bật monitoring qua [cấu hình server](../../configuration#monitoring-and-tracing) hoặc qua [tùy chọn dòng lệnh](../../running/flags.md#server-options). Port thông thường là `8222`.

Cấu hình trong file server config:

```yaml
http_port: 8222
```

Dùng tùy chọn dòng lệnh:

```bash
nats-server -m 8222
```

> 🇬🇧 *Once the server is running using one of the two methods, go to <http://localhost:8222> to browse the available endpoints detailed below.*

Sau khi server khởi động bằng một trong hai cách trên, truy cập <http://localhost:8222> để duyệt các endpoint được mô tả chi tiết bên dưới.

> 🇬🇧 *Alternatively, if you have System account enabled, monitoring endpoints available as ["System services"](../../configuration/sys_accounts#system-account)*

Ngoài ra, nếu đã bật System account, các monitoring endpoint cũng có thể dùng qua ["System services"](../../configuration/sys_accounts#system-account).

## Các Monitoring Endpoint

### Thông tin Server tổng quát `(/varz)`

> 🇬🇧 *The `/varz` endpoint returns general information about the server state and configuration.*

Endpoint `/varz` trả về thông tin tổng quát về trạng thái và config của server.

| Kết quả    | Return Code       |
| ---------- | ----------------- |
| Thành công | 200 (OK)          |
| Lỗi        | 400 (Bad Request) |

#### Tham số

N/A

#### Ví dụ

[https://demo.nats.io:8222/varz](https://demo.nats.io:8222/varz)

#### Response

```json
{
  "server_id": "NACDVKFBUW4C4XA24OOT6L4MDP56MW76J5RJDFXG7HLABSB46DCMWCOW",
  "version": "2.0.0",
  "proto": 1,
  "go": "go1.12",
  "host": "0.0.0.0",
  "port": 4222,
  "max_connections": 65536,
  "ping_interval": 120000000000,
  "ping_max": 2,
  "http_host": "0.0.0.0",
  "http_port": 8222,
  "https_port": 0,
  "auth_timeout": 1,
  "max_control_line": 4096,
  "max_payload": 1048576,
  "max_pending": 67108864,
  "cluster": {},
  "gateway": {},
  "leaf": {},
  "tls_timeout": 0.5,
  "write_deadline": 2000000000,
  "start": "2019-06-24T14:24:43.928582-07:00",
  "now": "2019-06-24T14:24:46.894852-07:00",
  "uptime": "2s",
  "mem": 9617408,
  "cores": 4,
  "gomaxprocs": 4,
  "cpu": 0,
  "connections": 0,
  "total_connections": 0,
  "routes": 0,
  "remotes": 0,
  "leafnodes": 0,
  "in_msgs": 0,
  "out_msgs": 0,
  "in_bytes": 0,
  "out_bytes": 0,
  "slow_consumers": 2,
  "subscriptions": 0,
  "http_req_stats": {
    "/": 0,
    "/connz": 0,
    "/gatewayz": 0,
    "/routez": 0,
    "/subsz": 0,
    "/varz": 1
  },
  "config_load_time": "2019-06-24T14:24:43.928582-07:00",
  "slow_consumer_stats": {
    "clients": 1,
    "routes": 1,
    "gateways": 0,
    "leafs": 0
  }
}
```

### Thông tin kết nối (`/connz`)

> 🇬🇧 *The `/connz` endpoint reports more detailed information on current and recently closed connections. It uses a paging mechanism which defaults to 1024 connections.*

Endpoint `/connz` cung cấp thông tin chi tiết về các kết nối đang hoạt động và đã đóng gần đây. Endpoint này dùng cơ chế phân trang với mặc định 1024 kết nối.

| Kết quả    | Return Code       |
| ---------- | ----------------- |
| Thành công | 200 (OK)          |
| Lỗi        | 400 (Bad Request) |

#### Tham số

| Tham số      | Giá trị                       | Mô tả                                                                                                                              |
| ------------ | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| sort         | (_xem tùy chọn sort_)         | Sắp xếp kết quả. Mặc định theo connection ID.                                                                                      |
| auth         | true, 1, false, 0             | Bao gồm username. Mặc định là false.                                                                                               |
| subs         | true, 1, false, 0 or `detail` | Bao gồm subscriptions. Mặc định là false. Khi đặt thành `detail`, danh sách thông tin subscription chi tiết hơn sẽ được trả về. |
| offset       | number > 0                    | Offset phân trang. Mặc định là 0.                                                                                                  |
| limit        | number > 0                    | Số kết quả trả về. Mặc định là 1024.                                                                                               |
| cid          | number, valid id              | Trả về kết nối theo ID của nó.                                                                                                     |
| state        | open, \*closed, any           | Trả về kết nối theo trạng thái. Mặc định là open.                                                                                  |
| mqtt\_client | string                        | Lọc kết nối theo MQTT client ID này.                                                                                               |

_Server mặc định lưu giữ 10.000 kết nối đã đóng gần nhất._

**Tùy chọn Sort**

| Tùy chọn    | Sắp xếp theo                                            |
| ----------- | ------------------------------------------------------- |
| cid         | Connection ID                                           |
| start       | Thời điểm bắt đầu kết nối, tương đương CID             |
| subs        | Số lượng subscription                                   |
| pending     | Lượng dữ liệu (bytes) chờ gửi đến client               |
| msgs\_to    | Số message đã gửi                                       |
| msgs\_from  | Số message đã nhận                                      |
| bytes\_to   | Số bytes đã gửi                                         |
| bytes\_from | Số bytes đã nhận                                        |
| last        | Hoạt động gần nhất                                      |
| idle        | Thời gian không hoạt động                               |
| uptime      | Thời gian tồn tại của kết nối                           |
| stop        | Thời điểm dừng của kết nối đã đóng                      |
| reason      | Lý do đóng kết nối                                      |
| rtt         | Round trip time                                         |

#### Ví dụ

Lấy tối đa 1024 kết nối: [https://demo.nats.io:8222/connz](https://demo.nats.io:8222/connz)

Kiểm soát limit và offset: [https://demo.nats.io:8222/connz?limit=16\&offset=128](https://demo.nats.io:8222/connz?limit=16\&offset=128).

Xem thông tin kết nối đã đóng: [https://demo.nats.io:8222/connz?state=closed](https://demo.nats.io:8222/connz?state=closed).

Có thể xem thông tin subscription chi tiết theo từng kết nối với `subs=1`. Ví dụ: [https://demo.nats.io:8222/connz?limit=1\&offset=1\&subs=1](https://demo.nats.io:8222/connz?limit=1\&offset=1\&subs=1).

#### Response

```json
{
  "server_id": "NACDVKFBUW4C4XA24OOT6L4MDP56MW76J5RJDFXG7HLABSB46DCMWCOW",
  "now": "2019-06-24T14:28:16.520365-07:00",
  "num_connections": 2,
  "total": 2,
  "offset": 0,
  "limit": 1024,
  "connections": [
    {
      "cid": 5,
      "kind": "Client",
      "type": "nats",
      "ip": "127.0.0.1",
      "port": 62714,
      "start": "2021-09-09T23:16:43.040862Z",
      "last_activity": "2021-09-09T23:16:43.042364Z",
      "rtt": "95µs",
      "uptime": "5s",
      "idle": "5s",
      "pending_bytes": 0,
      "in_msgs": 0,
      "out_msgs": 0,
      "in_bytes": 0,
      "out_bytes": 0,
      "subscriptions": 1,
      "name": "NATS Benchmark",
      "lang": "go",
      "version": "1.12.1"
    },
    {
      "cid": 6,
      "kind": "Client",
      "type": "nats",
      "ip": "127.0.0.1",
      "port": 62715,
      "start": "2021-09-09T23:16:43.042557Z",
      "last_activity": "2021-09-09T23:16:43.042811Z",
      "rtt": "100µs",
      "uptime": "5s",
      "idle": "5s",
      "pending_bytes": 0,
      "in_msgs": 0,
      "out_msgs": 0,
      "in_bytes": 0,
      "out_bytes": 0,
      "subscriptions": 1,
      "name": "NATS Benchmark",
      "lang": "go",
      "version": "1.12.1"
    },
    {
      "cid": 7,
      "kind": "Client",
      "type": "mqtt",
      "ip": "::1",
      "port": 62718,
      "start": "2021-09-09T23:16:45.391459Z",
      "last_activity": "2021-09-09T23:16:45.395869Z",
      "rtt": "0s",
      "uptime": "2s",
      "idle": "2s",
      "pending_bytes": 0,
      "in_msgs": 0,
      "out_msgs": 0,
      "in_bytes": 0,
      "out_bytes": 0,
      "subscriptions": 2,
      "mqtt_client": "mqtt_sub"
    }
  ]
}
```

### Thông tin Route (`/routez`)

> 🇬🇧 *The `/routez` endpoint reports information on active routes for a cluster. Routes are expected to be low, so there is no paging mechanism with this endpoint.*

Endpoint `/routez` cung cấp thông tin về các route đang hoạt động trong cluster (cụm nhiều server chạy chung). Số lượng route thường ít nên endpoint này không có cơ chế phân trang.

| Kết quả    | Return Code       |
| ---------- | ----------------- |
| Thành công | 200 (OK)          |
| Lỗi        | 400 (Bad Request) |

#### Tham số

| Tham số | Giá trị                       | Mô tả                                                                                                                              |
| ------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| subs    | true, 1, false, 0 or `detail` | Bao gồm subscriptions. Mặc định là false. Khi đặt thành `detail`, danh sách thông tin subscription chi tiết hơn sẽ được trả về. |

> 🇬🇧 *As noted above, the `routez` endpoint does support the `subs` argument from the `/connz` endpoint. For example: [https://demo.nats.io:8222/routez?subs=1](https://demo.nats.io:8222/routez?subs=1)*

Như đã đề cập, endpoint `routez` hỗ trợ tham số `subs` từ endpoint `/connz`. Ví dụ: [https://demo.nats.io:8222/routez?subs=1](https://demo.nats.io:8222/routez?subs=1)

#### Ví dụ

* Xem thông tin route: [https://demo.nats.io:8222/routez?subs=1](https://demo.nats.io:8222/routez?subs=1)

#### Response

```json
{
  "server_id": "NACDVKFBUW4C4XA24OOT6L4MDP56MW76J5RJDFXG7HLABSB46DCMWCOW",
  "now": "2019-06-24T14:29:16.046656-07:00",
  "num_routes": 1,
  "routes": [
    {
      "rid": 1,
      "remote_id": "de475c0041418afc799bccf0fdd61b47",
      "did_solicit": true,
      "ip": "127.0.0.1",
      "port": 61791,
      "pending_size": 0,
      "in_msgs": 0,
      "out_msgs": 0,
      "in_bytes": 0,
      "out_bytes": 0,
      "subscriptions": 0
    }
  ]
}
```

### Thông tin Gateway (`/gatewayz`)

> 🇬🇧 *The `/gatewayz` endpoint reports information about gateways used to create a NATS supercluster. Like routes, the number of gateways are expected to be low, so there is no paging mechanism with this endpoint.*

Endpoint `/gatewayz` cung cấp thông tin về các gateway dùng để tạo NATS supercluster. Tương tự route, số lượng gateway thường ít nên không có cơ chế phân trang.

| Kết quả    | Return Code       |
| ---------- | ----------------- |
| Thành công | 200 (OK)          |
| Lỗi        | 400 (Bad Request) |

#### Tham số

| Tham số   | Giá trị           | Mô tả                                              |
| --------- | ----------------- | -------------------------------------------------- |
| accs      | true, 1, false, 0 | Bao gồm thông tin account. Mặc định là false.      |
| gw\_name  | string            | Chỉ trả về remote gateway có tên này.              |
| acc\_name | string            | Giới hạn danh sách account theo tên account này.  |

#### Ví dụ

* Xem thông tin Gateway: [https://demo.nats.io:8222/gatewayz](https://demo.nats.io:8222/gatewayz)

#### Response

```json
{
  "server_id": "NANVBOU62MDUWTXWRQ5KH3PSMYNCHCEUHQV3TW3YH7WZLS7FMJE6END6",
  "now": "2019-07-24T18:02:55.597398-06:00",
  "name": "region1",
  "host": "2601:283:4601:1350:1895:efda:2010:95a1",
  "port": 4501,
  "outbound_gateways": {
    "region2": {
      "configured": true,
      "connection": {
        "cid": 7,
        "ip": "127.0.0.1",
        "port": 5500,
        "start": "2019-07-24T18:02:48.765621-06:00",
        "last_activity": "2019-07-24T18:02:48.765621-06:00",
        "uptime": "6s",
        "idle": "6s",
        "pending_bytes": 0,
        "in_msgs": 0,
        "out_msgs": 0,
        "in_bytes": 0,
        "out_bytes": 0,
        "subscriptions": 0,
        "name": "NCXBIYWT7MV7OAQTCR4QTKBN3X3HDFGSFWTURTCQ22ZZB6NKKJPO7MN4"
      }
    },
    "region3": {
      "configured": true,
      "connection": {
        "cid": 5,
        "ip": "::1",
        "port": 6500,
        "start": "2019-07-24T18:02:48.764685-06:00",
        "last_activity": "2019-07-24T18:02:48.764685-06:00",
        "uptime": "6s",
        "idle": "6s",
        "pending_bytes": 0,
        "in_msgs": 0,
        "out_msgs": 0,
        "in_bytes": 0,
        "out_bytes": 0,
        "subscriptions": 0,
        "name": "NCVS7Q65WX3FGIL2YQRLI77CE6MQRWO2Y453HYVLNMBMTVLOKMPW7R6K"
      }
    }
  },
  "inbound_gateways": {
    "region2": [
      {
        "configured": false,
        "connection": {
          "cid": 9,
          "ip": "::1",
          "port": 52029,
          "start": "2019-07-24T18:02:48.76677-06:00",
          "last_activity": "2019-07-24T18:02:48.767096-06:00",
          "uptime": "6s",
          "idle": "6s",
          "pending_bytes": 0,
          "in_msgs": 0,
          "out_msgs": 0,
          "in_bytes": 0,
          "out_bytes": 0,
          "subscriptions": 0,
          "name": "NCXBIYWT7MV7OAQTCR4QTKBN3X3HDFGSFWTURTCQ22ZZB6NKKJPO7MN4"
        }
      }
    ],
    "region3": [
      {
        "configured": false,
        "connection": {
          "cid": 4,
          "ip": "::1",
          "port": 52025,
          "start": "2019-07-24T18:02:48.764577-06:00",
          "last_activity": "2019-07-24T18:02:48.764994-06:00",
          "uptime": "6s",
          "idle": "6s",
          "pending_bytes": 0,
          "in_msgs": 0,
          "out_msgs": 0,
          "in_bytes": 0,
          "out_bytes": 0,
          "subscriptions": 0,
          "name": "NCVS7Q65WX3FGIL2YQRLI77CE6MQRWO2Y453HYVLNMBMTVLOKMPW7R6K"
        }
      },
      {
        "configured": false,
        "connection": {
          "cid": 8,
          "ip": "127.0.0.1",
          "port": 52026,
          "start": "2019-07-24T18:02:48.766173-06:00",
          "last_activity": "2019-07-24T18:02:48.766999-06:00",
          "uptime": "6s",
          "idle": "6s",
          "pending_bytes": 0,
          "in_msgs": 0,
          "out_msgs": 0,
          "in_bytes": 0,
          "out_bytes": 0,
          "subscriptions": 0,
          "name": "NCKCYK5LE3VVGOJQ66F65KA27UFPCLBPX4N4YOPOXO3KHGMW24USPCKN"
        }
      }
    ]
  }
}
```

### Thông tin Leaf Node (`/leafz`)

> 🇬🇧 *The `/leafz` endpoint reports detailed information about the leaf node connections.*

Endpoint `/leafz` cung cấp thông tin chi tiết về các kết nối leaf node.

| Kết quả    | Return Code       |
| ---------- | ----------------- |
| Thành công | 200 (OK)          |
| Lỗi        | 400 (Bad Request) |

#### Tham số

| Tham số | Giá trị           | Mô tả                                                     |
| ------- | ----------------- | --------------------------------------------------------- |
| subs    | true, 1, false, 0 | Bao gồm các internal subscription. Mặc định là false.    |

> 🇬🇧 *As noted above, the `leafz` endpoint does support the `subs` argument from the `/connz` endpoint. For example: [https://demo.nats.io:8222/leafz?subs=1](https://demo.nats.io:8222/leafz?subs=1)*

Như đã đề cập, endpoint `leafz` hỗ trợ tham số `subs` từ endpoint `/connz`. Ví dụ: [https://demo.nats.io:8222/leafz?subs=1](https://demo.nats.io:8222/leafz?subs=1)

#### Ví dụ

* Xem thông tin leaf node: [https://demo.nats.io:8222/leafz?subs=1](https://demo.nats.io:8222/leafz?subs=1)

#### Response

```json
{
  "server_id": "NC2FJCRMPBE5RI5OSRN7TKUCWQONCKNXHKJXCJIDVSAZ6727M7MQFVT3",
  "now": "2019-08-27T09:07:05.841132-06:00",
  "leafnodes": 1,
  "leafs": [
    {
      "account": "$G",
      "ip": "127.0.0.1",
      "port": 6223,
      "rtt": "200µs",
      "in_msgs": 0,
      "out_msgs": 10000,
      "in_bytes": 0,
      "out_bytes": 1280000,
      "subscriptions": 1,
      "subscriptions_list": ["foo"]
    }
  ]
}
```

### Thông tin Subscription Routing (`/subsz`)

> 🇬🇧 *The `/subsz` endpoint reports detailed information about the current subscriptions and the routing data structure. It is not normally used.*

Endpoint `/subsz` cung cấp thông tin chi tiết về các subscription hiện tại và cấu trúc dữ liệu routing. Endpoint này thường ít được dùng.

| Kết quả    | Return Code       |
| ---------- | ----------------- |
| Thành công | 200 (OK)          |
| Lỗi        | 400 (Bad Request) |

#### Tham số

| Tham số | Giá trị           | Mô tả                                                    |
| ------- | ----------------- | -------------------------------------------------------- |
| subs    | true, 1, false, 0 | Bao gồm subscriptions. Mặc định là false.               |
| offset  | integer > 0       | Offset phân trang. Mặc định là 0.                        |
| limit   | integer > 0       | Số kết quả trả về. Mặc định là 1024.                     |
| test    | subject           | Kiểm tra xem một subscription có tồn tại hay không.     |

#### Ví dụ

* Xem thông tin subscription routing: [https://demo.nats.io:8222/subsz](https://demo.nats.io:8222/subsz)

#### Response

```json
{
  "num_subscriptions": 2,
  "num_cache": 0,
  "num_inserts": 2,
  "num_removes": 0,
  "num_matches": 0,
  "cache_hit_rate": 0,
  "max_fanout": 0,
  "avg_fanout": 0
}
```

### Thông tin Account (`/accountz`)

> 🇬🇧 *The `/accountz` endpoint reports information on a server's active accounts. The default behavior is to return a list of all accounts known to the server.*

Endpoint `/accountz` trả về thông tin về các account đang hoạt động trên server. Mặc định, endpoint này trả về danh sách tất cả các account mà server biết đến.

| Kết quả    | Return Code       |
| ---------- | ----------------- |
| Thành công | 200 (OK)          |
| Lỗi        | 400 (Bad Request) |

| Tham số | Giá trị      | Mô tả                                                                                                              |
| ------- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| acc     | account name | Bao gồm số liệu cho account chỉ định. Mặc định để trống — khi không đặt, danh sách tất cả account được trả về.   |

#### Ví dụ

* Xem danh sách tất cả account: [https://demo.nats.io:8222/accountz](https://demo.nats.io:8222/accountz)
* Xem chi tiết account cụ thể `$G`: [https://demo.nats.io:8222/accountz?acc=$G](https://demo.nats.io:8222/accountz?acc=$G)

#### Response

Mặc định:

```json
{
  "server_id": "NAB2EEQ3DLS2BHU4K2YMXMPIOOOAOFOAQAC5NQRIEUI4BHZKFBI4ZU4A",
  "now": "2021-02-08T17:31:29.551146-05:00",
  "system_account": "AAAXAUVSGK7TCRHFIRAS4SYXVJ76EWDMNXZM6ARFGXP7BASNDGLKU7A5",
  "accounts": ["AAAXAUVSGK7TCRHFIRAS4SYXVJ76EWDMNXZM6ARFGXP7BASNDGLKU7A5", "$G"]
}
```

Xem account cụ thể:

```json
{
  "server_id": "NAB2EEQ3DLS2BHU4K2YMXMPIOOOAOFOAQAC5NQRIEUI4BHZKFBI4ZU4A",
  "now": "2021-02-08T17:37:55.80856-05:00",
  "system_account": "AAAXAUVSGK7TCRHFIRAS4SYXVJ76EWDMNXZM6ARFGXP7BASNDGLKU7A5",
  "account_detail": {
    "account_name": "AAAXAUVSGK7TCRHFIRAS4SYXVJ76EWDMNXZM6ARFGXP7BASNDGLKU7A5",
    "update_time": "2021-02-08T17:31:22.390334-05:00",
    "is_system": true,
    "expired": false,
    "complete": true,
    "jetstream_enabled": false,
    "leafnode_connections": 0,
    "client_connections": 0,
    "subscriptions": 42,
    "exports": [
      {
        "subject": "$SYS.DEBUG.SUBSCRIBERS",
        "type": "service",
        "response_type": "Singleton"
      }
    ],
    "jwt": "eyJ0eXAiOiJqd3QiLCJhbGciOiJlZDI1NTE5In0.eyJqdGkiOiJVVlU2VEpXRU8zS0hYWTZVMkgzM0RCVklET1A3U05DTkJPMlM0M1dPNUM2T1RTTDNVSUxBIiwiaWF0IjoxNjAzNDczNzg4LCJpc3MiOiJPQlU1TzVGSjMyNFVEUFJCSVZSR0Y3Q05FT0hHTFBTN0VZUEJUVlFaS1NCSElJWklCNkhENjZKRiIsIm5hbWUiOiJTWVMiLCJzdWIiOiJBQUFYQVVWU0dLN1RDUkhGSVJBUzRTWVhWSjc2RVdETU5YWk02QVJGR1hQN0JBU05ER0xLVTdBNSIsInR5cGUiOiJhY2NvdW50IiwibmF0cyI6eyJsaW1pdHMiOnsic3VicyI6LTEsImNvbm4iOi0xLCJsZWFmIjotMSwiaW1wb3J0cyI6LTEsImV4cG9ydHMiOi0xLCJkYXRhIjotMSwicGF5bG9hZCI6LTEsIndpbGRjYXJkcyI6dHJ1ZX19fQ.CeGo16i5oD0b1uBJ8UdGmLH-l9dL8yNqXHggkAt2T5c88fM7k4G08wLguMAnlvzrdlYvdZvOx_5tHLuDZmGgCg",
    "issuer_key": "OBU5O5FJ324UDPRBIVRGF7CNEOHGLPS7EYPBTVQZKSBHIIZIB6HD66JF",
    "name_tag": "SYS",
    "decoded_jwt": {
      "jti": "UVU6TJWEO3KHXY6U2H33DBVIDOP7SNCNBO2S43WO5C6OTSL3UILA",
      "iat": 1603473788,
      "iss": "OBU5O5FJ324UDPRBIVRGF7CNEOHGLPS7EYPBTVQZKSBHIIZIB6HD66JF",
      "name": "SYS",
      "sub": "AAAXAUVSGK7TCRHFIRAS4SYXVJ76EWDMNXZM6ARFGXP7BASNDGLKU7A5",
      "nats": {
        "limits": {
          "subs": -1,
          "data": -1,
          "payload": -1,
          "imports": -1,
          "exports": -1,
          "wildcards": true,
          "conn": -1,
          "leaf": -1
        },
        "default_permissions": {
          "pub": {},
          "sub": {}
        },
        "type": "account",
        "version": 1
      }
    },
    "sublist_stats": {
      "num_subscriptions": 42,
      "num_cache": 6,
      "num_inserts": 42,
      "num_removes": 0,
      "num_matches": 6,
      "cache_hit_rate": 0,
      "max_fanout": 1,
      "avg_fanout": 0.8333333333333334
    }
  }
}
```

### Thống kê Account (`/accstatz`)

> 🇬🇧 *The `/accstatz` endpoint reports per-account statistics such as the number of connections, messages/bytes in/out, etc.*

Endpoint `/accstatz` trả về số liệu thống kê theo từng account như số lượng kết nối, số message/bytes gửi vào và gửi ra, v.v.

| Kết quả    | Return Code       |
| ---------- | ----------------- |
| Thành công | 200 (OK)          |
| Lỗi        | 400 (Bad Request) |

#### Tham số

| Tham số | Giá trị           | Mô tả                                                                                       |
| ------- | ----------------- | ------------------------------------------------------------------------------------------- |
| unused  | true, 1, false, 0 | Nếu true, bao gồm cả các account không có kết nối nào hiện tại. Mặc định là false.        |

#### Ví dụ

* Các account có kết nối đang hoạt động - <https://demo.nats.io:8222/accstatz>
* Bao gồm cả account không có kết nối (trong trường hợp này là `$SYS`) - <https://demo.nats.io:8222/accstatz?unused=1>

#### Response

```json
{
  "server_id": "NDJ5M4F5WAIBUA26NJ3QMH532AQPN7QNTJP3Y4SBHSHL4Y7QUAKNJEAF",
  "now": "2022-10-19T17:16:20.881296749Z",
  "account_statz": [
    {
      "acc": "default",
      "conns": 31,
      "leafnodes": 2,
      "total_conns": 33,
      "num_subscriptions": 45,
      "sent": {
        "msgs": 1876970,
        "bytes": 246705616
      },
      "received": {
        "msgs": 1347454,
        "bytes": 219438308
      },
      "slow_consumers": 29
    },
    {
      "acc": "$G",
      "conns": 1,
      "leafnodes": 0,
      "total_conns": 1,
      "num_subscriptions": 3,
      "sent": {
        "msgs": 0,
        "bytes": 0
      },
      "received": {
        "msgs": 107,
        "bytes": 1094
      },
      "slow_consumers": 0
    }
  ]
}
```

### Thông tin JetStream (`/jsz`)

> 🇬🇧 *The `/jsz` endpoint reports more detailed information on JetStream. For accounts, it uses a paging mechanism that defaults to 1024 connections.*

Endpoint `/jsz` cung cấp thông tin chi tiết về JetStream. Với accounts, endpoint này dùng cơ chế phân trang với mặc định 1024 kết nối.

> **Lưu ý:** Trong môi trường cluster, nên truy vấn thông tin từ leader của stream (luồng message lưu trữ liên tục) để lấy dữ liệu chính xác và cập nhật nhất.

| Kết quả    | Return Code       |
| ---------- | ----------------- |
| Thành công | 200 (OK)          |
| Lỗi        | 400 (Bad Request) |

#### Tham số

| Tham số     | Giá trị           | Mô tả                                                                                              |
| ----------- | ----------------- | -------------------------------------------------------------------------------------------------- |
| acc         | account name      | Bao gồm số liệu cho account chỉ định. Mặc định chưa đặt.                                          |
| accounts    | true, 1, false, 0 | Bao gồm thông tin JetStream theo từng account. Mặc định là false.                                 |
| streams     | true, 1, false, 0 | Bao gồm streams. Khi đặt, ngầm định bật `accounts=true`. Mặc định là false.                       |
| consumers   | true, 1, false, 0 | Bao gồm consumer. Khi đặt, ngầm định bật `streams=true`. Mặc định là false.                       |
| config      | true, 1, false, 0 | Khi yêu cầu stream hoặc consumer, bao gồm cấu hình tương ứng của chúng. Mặc định là false.       |
| leader-only | true, 1, false, 0 | Chỉ leader phản hồi. Mặc định là false.                                                           |
| offset      | number > 0        | Offset phân trang. Mặc định là 0.                                                                 |
| limit       | number > 0        | Số kết quả trả về. Mặc định là 1024.                                                              |
| raft        | true, 1, false, 0 | Bao gồm thông tin chi tiết về Raft group. Mặc định là false.                                      |

#### Ví dụ

Xem thông tin JetStream cơ bản: [https://demo.nats.io:8222/jsz](https://demo.nats.io:8222/jsz)

Yêu cầu accounts kèm kiểm soát limit và offset: [https://demo.nats.io:8222/jsz?accounts=true\&limit=16\&offset=128](https://demo.nats.io:8222/jsz?accounts=true\&limit=16\&offset=128).

Có thể xem thông tin consumer (bên xử lý dữ liệu từ stream) chi tiết theo từng kết nối với `consumer=true`. Ví dụ: [https://demo.nats.io:8222/jsz?consumers=true](https://demo.nats.io:8222/jsz?consumers=true).

#### Response

```json
{
  "server_id": "NCVIDODSZ45C5OD67ZD7EJUIJPQDP6CM74SJX6TJIF2G7NLYS5LCVYHS",
  "now": "2021-02-08T19:08:30.555533-05:00",
  "config": {
    "max_memory": 10485760,
    "max_storage": 10485760,
    "store_dir": "/var/folders/9h/6g_c9l6n6bb8gp331d_9y0_w0000gn/T/srv_7500251552558",
    "unique_tag": "az"
  },
  "memory": 0,
  "storage": 66,
  "api": {
    "total": 5,
    "errors": 0
  },
  "total_streams": 1,
  "total_consumers": 1,
  "total_messages": 1,
  "total_message_bytes": 33,
  "meta_cluster": {
    "name": "cluster_name",
    "replicas": [
      {
        "name": "server_5500",
        "current": false,
        "active": 2932926000
      }
    ]
  },
  "account_details": [
    {
      "name": "BCC_TO_HAVE_ONE_EXTRA",
      "id": "BCC_TO_HAVE_ONE_EXTRA",
      "memory": 0,
      "storage": 0,
      "api": {
        "total": 0,
        "errors": 0
      }
    },
    {
      "name": "ACC",
      "id": "ACC",
      "memory": 0,
      "storage": 66,
      "api": {
        "total": 5,
        "errors": 0
      },
      "stream_detail": [
        {
          "name": "my-stream-replicated",
          "cluster": {
            "name": "cluster_name",
            "replicas": [
              {
                "name": "server_5500",
                "current": false,
                "active": 2931517000
              }
            ]
          },
          "state": {
            "messages": 1,
            "bytes": 33,
            "first_seq": 1,
            "first_ts": "2021-02-09T00:08:27.623735Z",
            "last_seq": 1,
            "last_ts": "2021-02-09T00:08:27.623735Z",
            "consumer_count": 1
          },
          "consumer_detail": [
            {
              "stream_name": "my-stream-replicated",
              "name": "my-consumer-replicated",
              "created": "2021-02-09T00:08:27.427631Z",
              "delivered": {
                "consumer_seq": 0,
                "stream_seq": 0
              },
              "ack_floor": {
                "consumer_seq": 0,
                "stream_seq": 0
              },
              "num_ack_pending": 0,
              "num_redelivered": 0,
              "num_waiting": 0,
              "num_pending": 1,
              "cluster": {
                "name": "cluster_name",
                "replicas": [
                  {
                    "name": "server_5500",
                    "current": false,
                    "active": 2933232000
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

### Health (`/healthz`)

> 🇬🇧 *The `/healthz` endpoint returns OK if the server is able to accept connections.*

Endpoint `/healthz` trả về OK nếu server có thể chấp nhận kết nối.

| Kết quả    | Return Code       |
| ---------- | ----------------- |
| Thành công | 200 (OK)          |
| Lỗi        | 400 (Bad Request) |

#### Tham số

| Tham số         | Giá trị | Mô tả                                                                                      |
| --------------- | ------- | ------------------------------------------------------------------------------------------ |
| js-enabled-only | true, 1 | Trả về lỗi nếu JetStream bị tắt.                                                          |
| js-server-only  | true, 1 | Bỏ qua kiểm tra health của accounts, streams, và consumers.                               |
| js-enabled      | true, 1 | Trả về lỗi nếu JetStream bị tắt. (**Deprecated**: dùng `js-enabled-only` thay thế).  |

#### Ví dụ

* Mặc định - <https://demo.nats.io:8222/healthz>
* Yêu cầu JetStream - <https://demo.nats.io:8222/healthz?js-enabled-only=true>

#### Response

```json
{ "status": "ok" }
```

## Xây dựng Ứng dụng Giám sát

> 🇬🇧 *NATS monitoring endpoints support [JSONP](https://en.wikipedia.org/wiki/JSONP) and [CORS](https://en.wikipedia.org/wiki/Cross-origin\_resource\_sharing#How\_CORS\_works). You can easily create single page web applications for monitoring. To do this you simply pass the `callback` query parameter to any endpoint.*

Các monitoring endpoint của NATS hỗ trợ [JSONP](https://en.wikipedia.org/wiki/JSONP) và [CORS](https://en.wikipedia.org/wiki/Cross-origin\_resource\_sharing#How\_CORS\_works), giúp dễ dàng xây dựng ứng dụng web giám sát dạng single page. Chỉ cần truyền query parameter `callback` vào bất kỳ endpoint nào.

Ví dụ:

```
https://demo.nats.io:8222/connz?callback=cb
```

Ví dụ triển khai bằng JQuery:

```javascript
$.getJSON("https://demo.nats.io:8222/connz?callback=?", function (data) {
  console.log(data);
});
```

## Công cụ Giám sát

> 🇬🇧 *In addition to writing custom monitoring tools, you can monitor nats-server in Prometheus. The [Prometheus NATS Exporter](https://github.com/nats-io/prometheus-nats-exporter) allows you to configure the metrics you want to observe and store in Prometheus, and there are Grafana dashboards available for you to visualize the server metrics.*

Ngoài việc tự viết công cụ giám sát, bạn có thể theo dõi nats-server qua Prometheus. [Prometheus NATS Exporter](https://github.com/nats-io/prometheus-nats-exporter) cho phép cấu hình các metric (số liệu đo lường) muốn thu thập và lưu trữ trong Prometheus, đồng thời có sẵn các Grafana dashboard để trực quan hóa số liệu server.

> 🇬🇧 *See the [Walkthrough of Monitoring NATS with Prometheus and Grafana](https://github.com/nats-io/prometheus-nats-exporter/tree/main/walkthrough) for more details.*

Xem [Walkthrough of Monitoring NATS with Prometheus and Grafana](https://github.com/nats-io/prometheus-nats-exporter/tree/main/walkthrough) để biết thêm chi tiết.

### Tùy chọn Thương mại

> 🇬🇧 *If you want a "batteries-included" approach to high-cardinality NATS monitoring and observability, try the standalone [Synadia Insights](https://www.synadia.com/insights).*

Nếu cần giải pháp giám sát NATS high-cardinality theo kiểu "dùng ngay không cần cấu hình", hãy thử [Synadia Insights](https://www.synadia.com/insights).

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **endpoint**: địa chỉ API cụ thể
- **leader**: server chính trong nhóm replica
- **message**: gói dữ liệu được gửi đi
- **metric**: số liệu đo lường
- **node**: một server trong cluster
- **port**: cổng kết nối
- **request**: yêu cầu
- **server**: máy chủ
- **stream**: luồng message lưu trữ liên tục