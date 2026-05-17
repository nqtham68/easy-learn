---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/clustering
title: Clustering - Cụm Server NATS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Clustering - Cụm Server NATS

## Cụm Server NATS

> 🇬🇧 *NATS supports running each server in clustered mode. You can cluster servers together for high volume messaging systems and resiliency and high availability.*

NATS hỗ trợ chạy từng server ở chế độ cluster (cụm nhiều server chạy chung). Bạn có thể gom nhiều server vào một cluster để phục vụ hệ thống messaging tải cao, tăng khả năng chịu lỗi và đảm bảo high availability.

> 🇬🇧 *NATS servers achieve this by gossiping about and connecting to, all of the servers they know, thus dynamically forming a full mesh. Once clients [connect](../../../using-nats/developing-with-nats/connecting/cluster.md) or [re-connect](../../../using-nats/developing-with-nats/reconnect) to a particular server, they are informed about current cluster members. Because of this behavior, a cluster can grow, shrink and self heal. The full mesh does not necessarily have to be explicitly configured either.*

Các server NATS thực hiện điều này bằng cách gossip và kết nối với tất cả các server mà chúng biết, từ đó tự động hình thành full mesh. Khi client kết nối hoặc kết nối lại tới một server cụ thể, chúng sẽ được thông báo về các thành viên hiện tại của cluster. Nhờ cơ chế này, cluster có thể tự mở rộng, thu nhỏ và tự phục hồi mà không nhất thiết phải cấu hình full mesh một cách tường minh.

> 🇬🇧 *Note that NATS clustered servers have a forwarding limit of one hop. This means that each `nats-server` instance will **only** forward messages that it has received **from a client** to the immediately adjacent `nats-server` instances to which it has routes. Messages received **from** a route will only be distributed to local clients.*

Lưu ý: các server trong cluster NATS có giới hạn chuyển tiếp là một hop. Mỗi instance `nats-server` **chỉ** chuyển tiếp các message (gói dữ liệu được gửi đi) nhận được **từ client** sang các instance `nats-server` kề cạnh mà nó có route. Message nhận được **từ** một route chỉ được phân phối tới các client cục bộ.

> 🇬🇧 *For the cluster to successfully form a full mesh and NATS to function as intended and described throughout the documentation - temporary errors permitting - it is necessary that servers can connect to each other and that clients can connect to each server in the cluster.*

Để cluster hình thành full mesh thành công và NATS hoạt động đúng như mô tả trong tài liệu — trừ các lỗi tạm thời — điều kiện cần là các server có thể kết nối với nhau và các client có thể kết nối được tới từng server trong cluster.

## Cluster URLs

> 🇬🇧 *In addition to a port to listen for clients, `nats-server` listens on a "cluster" URL \(the `-cluster` option\). Additional `nats-server` servers can then add that URL to their `-routes` argument to join the cluster. These options can also be specified in a [config file](./cluster_config.md), but only the command-line version is shown in this overview for simplicity.*

Ngoài port (cổng kết nối) lắng nghe client, `nats-server` còn lắng nghe trên một "cluster" URL (tùy chọn `-cluster`). Các server `nats-server` khác có thể thêm URL đó vào tham số `-routes` để gia nhập cluster. Các tùy chọn này cũng có thể khai báo trong [config file](./cluster_config.md) (cấu hình) của server, nhưng phần tổng quan này chỉ trình bày qua dòng lệnh cho ngắn gọn.

## Chạy Cluster Đơn Giản

> 🇬🇧 *Here is a simple cluster running on the same machine:*

Dưới đây là ví dụ một cluster đơn giản chạy trên cùng một máy:

Server A - 'seed server'

```bash
nats-server -p 4222 -cluster nats://localhost:4248 --cluster_name test-cluster
```

Server B

```shell
nats-server -p 5222 -cluster nats://localhost:5248 -routes nats://localhost:4248 --cluster_name test-cluster
```

> 🇬🇧 *Check the output of the server for the selected client and route ports.*

Kiểm tra output của server để xem các port client và route đã được chọn.

Server C

```shell
nats-server -p 6222 -cluster nats://localhost:6248 -routes nats://localhost:4248 --cluster_name test-cluster
```

> 🇬🇧 *Check the output of the server for the selected client and route ports.*

Kiểm tra output của server để xem các port client và route đã được chọn.

> 🇬🇧 *Each server has a client and cluster port specified. Servers with the routes option establish a route to the _seed server_. Because the clustering protocol gossips members of the cluster, all servers are able to discover other server in the cluster. When a server is discovered, the discovering server will automatically attempt to connect to it in order to form a _full mesh_. Typically only one instance of the server will run per machine, so you can reuse the client port \(4222\) and the cluster port \(4248\), and simply the route to the host/port of the seed server.*

Mỗi server được chỉ định một port cho client và một port cho cluster. Các server có tùy chọn routes sẽ thiết lập route tới _seed server_. Vì giao thức clustering gossip danh sách thành viên, tất cả server đều có thể tìm thấy nhau trong cluster. Khi phát hiện một server mới, server đó sẽ tự động cố gắng kết nối để hình thành _full mesh_. Thông thường, mỗi máy chỉ chạy một instance server, nên bạn có thể dùng lại port client (4222) và port cluster (4248), chỉ cần trỏ route tới host/port của seed server.

> 🇬🇧 *Similarly, clients connecting to any server in the cluster will discover other servers in the cluster. If the connection to the server is interrupted, the client will attempt to connect to all other known servers.*

Tương tự, client kết nối vào bất kỳ server nào trong cluster cũng sẽ tự khám phá các server còn lại. Nếu kết nối bị gián đoạn, client sẽ thử kết nối lại với tất cả các server khác đã biết.

> 🇬🇧 *There is no explicit configuration for _seed server_. They simply serve as the starting point for server discovery by other members of the cluster as well as clients. As such these are the servers that clients have in their list of connect urls and cluster members have in their list of routes. They reduce configuration as not every server needs to be in these lists. But the ability for other server and clients to successfully connect depends on _seed server_ running. If multiple _seed server_ are used, they make use of the routes option as well, so they can establish routes to one another.*

_Seed server_ không có config riêng biệt. Chúng chỉ đóng vai trò điểm khởi đầu để các thành viên trong cluster và client tìm kiếm nhau. Vì vậy, đây là các server mà client đặt trong danh sách URL kết nối, còn các thành viên cluster đặt trong danh sách route. Điều này giúp giảm bớt cấu hình vì không phải mọi server đều cần có trong các danh sách đó. Tuy nhiên, khả năng kết nối của server và client phụ thuộc vào việc _seed server_ đang chạy. Nếu dùng nhiều _seed server_, chúng cũng sử dụng tùy chọn routes để thiết lập route với nhau.

## Tùy Chọn Dòng Lệnh

> 🇬🇧 *The following cluster options are supported:*

Các tùy chọn cluster sau được hỗ trợ:

```text
--routes [rurl-1, rurl-2]     Routes to solicit and connect
--cluster nats://host:port    Cluster URL for solicited routes
```

> 🇬🇧 *When a NATS server routes to a specified URL, it will advertise its own cluster URL to all other servers in the route effectively creating a routing mesh to all other servers.*

Khi một server NATS tạo route tới một URL cụ thể, nó sẽ quảng bá cluster URL của mình tới tất cả các server khác trong route, qua đó tạo thành routing mesh tới toàn bộ các server.

> 🇬🇧 ***Note:** when using the `-routes` option, you must also specify a `-cluster` option.*

**Lưu ý:** khi dùng tùy chọn `-routes`, bạn phải chỉ định thêm tùy chọn `-cluster`.

> 🇬🇧 *Clustering can also be configured using the server [config file](./cluster_config.md).*

Clustering cũng có thể được cấu hình qua [config file](./cluster_config.md) của server.

## Ví Dụ Cluster Ba Server

> 🇬🇧 *The following example demonstrates how to run a cluster of 3 servers on the same host. We will start with the seed server and use the `-D` command line parameter to produce debug information.*

Ví dụ dưới đây minh họa cách chạy cluster gồm 3 server trên cùng một host. Chúng ta bắt đầu với seed server và dùng tham số dòng lệnh `-D` để xuất thông tin debug.

```bash
nats-server -p 4222 -cluster nats://localhost:4248 -D
```

> 🇬🇧 *Alternatively, you could use a configuration file, let's call it `seed.conf`, with a content similar to this:*

Hoặc bạn có thể dùng config file, đặt tên là `seed.conf`, với nội dung tương tự như sau:

```text
# Cluster Seed Node

listen: 127.0.0.1:4222
http: 8222

cluster {
  listen: 127.0.0.1:4248
}
```

> 🇬🇧 *And start the server like this:*

Rồi khởi động server như sau:

```bash
nats-server -config ./seed.conf -D
```

> 🇬🇧 *This will produce an output similar to:*

Output sẽ trông giống như sau:

```text
[83329] 2020/02/12 16:04:52.369039 [INF] Starting nats-server version 2.1.4
[83329] 2020/02/12 16:04:52.369130 [DBG] Go build version go1.13.6
[83329] 2020/02/12 16:04:52.369133 [INF] Git commit [not set]
[83329] 2020/02/12 16:04:52.369360 [INF] Starting http monitor on 127.0.0.1:8222
[83329] 2020/02/12 16:04:52.369436 [INF] Listening for client connections on 127.0.0.1:4222
[83329] 2020/02/12 16:04:52.369441 [INF] Server id is NDSGCS74MG5ZUMBOVWOUJ5S3HIOW
[83329] 2020/02/12 16:04:52.369443 [INF] Server is ready
[83329] 2020/02/12 16:04:52.369534 [INF] Listening for route connections on 127.0.0.1:4248
```

> 🇬🇧 *It is also possible to specify the hostname and port independently. At the minimum, the port is required. If you leave the hostname off it will bind to all the interfaces \('0.0.0.0'\).*

Bạn cũng có thể chỉ định hostname và port riêng biệt. Tối thiểu phải có port. Nếu bỏ qua hostname, server sẽ bind trên tất cả các interface ('0.0.0.0').

```text
cluster {
  host: 127.0.0.1
  port: 4248
}
```

> 🇬🇧 *Now let's start two more servers, each one connecting to the seed server.*

Bây giờ hãy khởi động thêm hai server nữa, mỗi server kết nối tới seed server.

```bash
nats-server -p 5222 -cluster nats://localhost:5248 -routes nats://localhost:4248 -D
```

> 🇬🇧 *When running on the same host, we need to pick different ports for the client connections `-p`, and for the port used to accept other routes `-cluster`. Note that `-routes` points to the `-cluster` address of the seed server \(`localhost:4248`\).*

Khi chạy trên cùng một host, ta cần chọn các port khác nhau cho kết nối client (`-p`) và cho port chấp nhận các route khác (`-cluster`). Lưu ý rằng `-routes` trỏ tới địa chỉ `-cluster` của seed server (`localhost:4248`).

> 🇬🇧 *Here is the log produced. See how it connects and registers a route to the seed server \(`...GzM`\).*

Đây là log được tạo ra. Hãy chú ý cách nó kết nối và đăng ký route tới seed server (`...GzM`).

```text
[83330] 2020/02/12 16:05:09.661047 [INF] Starting nats-server version 2.1.4
[83330] 2020/02/12 16:05:09.661123 [DBG] Go build version go1.13.6
[83330] 2020/02/12 16:05:09.661125 [INF] Git commit [not set]
[83330] 2020/02/12 16:05:09.661341 [INF] Listening for client connections on 0.0.0.0:5222
[83330] 2020/02/12 16:05:09.661347 [INF] Server id is NAABC2CKRVPZBIECMLZZA6L3PK
[83330] 2020/02/12 16:05:09.661349 [INF] Server is ready
[83330] 2020/02/12 16:05:09.662429 [INF] Listening for route connections on localhost:5248
[83330] 2020/02/12 16:05:09.662676 [DBG] Trying to connect to route on localhost:4248
[83330] 2020/02/12 16:05:09.663308 [DBG] 127.0.0.1:4248 - rid:1 - Route connect msg sent
[83330] 2020/02/12 16:05:09.663370 [INF] 127.0.0.1:4248 - rid:1 - Route connection created
[83330] 2020/02/12 16:05:09.663537 [DBG] 127.0.0.1:4248 - rid:1 - Registering remote route "NDSGCS74MG5ZUMBOVWOUJ5S3HIOW"
[83330] 2020/02/12 16:05:09.663549 [DBG] 127.0.0.1:4248 - rid:1 - Sent local subscriptions to route
```

> 🇬🇧 *From the seed's server log, we see that the route is indeed accepted:*

Từ log của seed server, ta thấy route đã được chấp nhận:

```text
[83329] 2020/02/12 16:05:09.663386 [INF] 127.0.0.1:62941 - rid:1 - Route connection created
[83329] 2020/02/12 16:05:09.663665 [DBG] 127.0.0.1:62941 - rid:1 - Registering remote route "NAABC2CKRVPZBIECMLZZA6L3PK"
[83329] 2020/02/12 16:05:09.663681 [DBG] 127.0.0.1:62941 - rid:1 - Sent local subscriptions to route
```

> 🇬🇧 *Finally, let's start the third server:*

Cuối cùng, khởi động server thứ ba:

```bash
nats-server -p 6222 -cluster nats://localhost:6248 -routes nats://localhost:4248 -D
```

> 🇬🇧 *Again, notice that we use a different client port and cluster address, but still point to the same seed server at the address `nats://localhost:4248`:*

Một lần nữa, lưu ý rằng ta dùng port client và địa chỉ cluster khác nhau, nhưng vẫn trỏ tới cùng seed server tại địa chỉ `nats://localhost:4248`.

```text
[83331] 2020/02/12 16:05:12.838022 [INF] Listening for client connections on 0.0.0.0:6222
[83331] 2020/02/12 16:05:12.838029 [INF] Server id is NBE7SLUDLFIMHS2U6347N3DQEJ
[83331] 2020/02/12 16:05:12.838031 [INF] Server is ready
...
[83331] 2020/02/12 16:05:12.839203 [INF] Listening for route connections on localhost:6248
[83331] 2020/02/12 16:05:12.839453 [DBG] Trying to connect to route on localhost:4248
[83331] 2020/02/12 16:05:12.840112 [DBG] 127.0.0.1:4248 - rid:1 - Route connect msg sent
[83331] 2020/02/12 16:05:12.840198 [INF] 127.0.0.1:4248 - rid:1 - Route connection created
[83331] 2020/02/12 16:05:12.840324 [DBG] 127.0.0.1:4248 - rid:1 - Registering remote route "NDSGCS74MG5ZUMBOVWOUJ5S3HIOW"
[83331] 2020/02/12 16:05:12.840342 [DBG] 127.0.0.1:4248 - rid:1 - Sent local subscriptions to route
[83331] 2020/02/12 16:05:12.840717 [INF] 127.0.0.1:62946 - rid:2 - Route connection created
[83331] 2020/02/12 16:05:12.840906 [DBG] 127.0.0.1:62946 - rid:2 - Registering remote route "NAABC2CKRVPZBIECMLZZA6L3PK"
[83331] 2020/02/12 16:05:12.840915 [DBG] 127.0.0.1:62946 - rid:2 - Sent local subscriptions to route
```

> 🇬🇧 *First a route is created to the seed server \(`...IOW`\) and after that, a route from `...3PK` - which is the ID of the second server - is accepted.*

Đầu tiên, route tới seed server (`...IOW`) được tạo, sau đó route từ `...3PK` — ID của server thứ hai — được chấp nhận.

> 🇬🇧 *The log from the seed server shows that it accepted the route from the third server:*

Log từ seed server cho thấy nó đã chấp nhận route từ server thứ ba:

```text
[83329] 2020/02/12 16:05:12.840111 [INF] 127.0.0.1:62945 - rid:2 - Route connection created
[83329] 2020/02/12 16:05:12.840350 [DBG] 127.0.0.1:62945 - rid:2 - Registering remote route "NBE7SLUDLFIMHS2U6347N3DQEJ"
[83329] 2020/02/12 16:05:12.840363 [DBG] 127.0.0.1:62945 - rid:2 - Sent local subscriptions to route
```

> 🇬🇧 *And the log from the second server shows that it connected to the third.*

Và log từ server thứ hai cho thấy nó đã kết nối tới server thứ ba.

```text
[83330] 2020/02/12 16:05:12.840529 [DBG] Trying to connect to route on 127.0.0.1:6248
[83330] 2020/02/12 16:05:12.840684 [DBG] 127.0.0.1:6248 - rid:2 - Route connect msg sent
[83330] 2020/02/12 16:05:12.840695 [INF] 127.0.0.1:6248 - rid:2 - Route connection created
[83330] 2020/02/12 16:05:12.840814 [DBG] 127.0.0.1:6248 - rid:2 - Registering remote route "NBE7SLUDLFIMHS2U6347N3DQEJ"
[83330] 2020/02/12 16:05:12.840827 [DBG] 127.0.0.1:6248 - rid:2 - Sent local subscriptions to route
```

> 🇬🇧 *At this point, there is a full mesh cluster of NATS servers.*

Tới đây, cluster NATS đã hình thành full mesh hoàn chỉnh.

### Kiểm Tra Cluster

> 🇬🇧 *Now, the following should work: make a subscription to the first server \(port 4222\). Then publish to each server \(ports 4222, 5222, 6222\). You should be able to receive messages without problems.*

Bây giờ hãy thử: subscribe vào server đầu tiên (port 4222), sau đó publish tới từng server (port 4222, 5222, 6222). Bạn sẽ nhận được message bình thường.

Testing server A

```bash
nats sub -s "nats://127.0.0.1:4222" hello &
nats pub -s "nats://127.0.0.1:4222" hello world_4222
```

```text
23:34:45 Subscribing on hello
23:34:45 Published 10 bytes to "hello"

[#1] Received on "hello"
world_4222
```

Testing server B

```shell
nats pub -s "nats://127.0.0.1:5222" hello world_5222
```

```text
[#2] Received on "hello"
23:36:09 Published 10 bytes to "hello"
world_5222
```

Testing server C

```shell
nats pub -s "nats://127.0.0.1:6222" hello world_6222
```

```text
23:38:40 Published 10 bytes to "hello"
[#3] Received on "hello"
world_6222
```

Testing using seed (i.e. A, B and C) server URLs

```shell
nats pub -s "nats://127.0.0.1:4222,nats://127.0.0.1:5222,nats://127.0.0.1:6222" hello whole_world
```

```text
[#4] Received on "hello"
23:39:16 Published 11 bytes to "hello"
whole_world
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **host**: máy chủ vật lý/ảo
- **message**: gói dữ liệu được gửi đi
- **port**: cổng kết nối
- **server**: máy chủ