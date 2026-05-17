---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/adaptive_edge_deployment
title: Các Kiến Trúc Triển Khai Linh Hoạt của NATS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Các Kiến Trúc Triển Khai Linh Hoạt của NATS

> 🇬🇧 *From a single process to a global super-cluster with leaf node servers, you can always adapt your NATS service deployment to your needs. From servers and VPCs in many clouds, to partially connected small edge devices and everything in between, you can always easily extend and scale your NATS service as your needs grow.*

Từ một process đơn lẻ cho đến một super-cluster toàn cầu với các leaf node server, bạn luôn có thể điều chỉnh cách triển khai NATS service cho phù hợp với nhu cầu. Dù là server và VPC trên nhiều cloud, hay các thiết bị edge kết nối không liên tục, bạn đều có thể mở rộng và scale NATS service dễ dàng khi nhu cầu tăng lên.

## Một server đơn lẻ

> 🇬🇧 *The simplest version of a NATS service infrastructure is a single `nats-server` process. The `nats-server` binary is highly optimized, very lightweight and extremely efficient in its resources' usage.*

Phiên bản đơn giản nhất của hạ tầng NATS service là một process `nats-server` duy nhất. Binary `nats-server` được tối ưu cao, rất nhẹ và sử dụng tài nguyên cực kỳ hiệu quả.

> 🇬🇧 *Client applications establish a connection to the URL of that nats-server process (e.g. `"nats://localhost"`).*

Các ứng dụng client kết nối đến URL của process nats-server đó (ví dụ: `"nats://localhost"`).

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/single-server.svg)

## Một cluster server

> 🇬🇧 *If you need a fault-tolerant NATS service or if you need to scale your service capacity, you can cluster a set of nats-server processes together in a cluster.*

Khi cần NATS service có khả năng chịu lỗi hoặc cần scale capacity, bạn có thể gom nhiều process nats-server lại thành một cluster (cụm nhiều server chạy chung).

> 🇬🇧 *Client applications establish and maintain a connection to (one of) the nats server URL(s) composing the cluster (e.g. `"nats://server1","nats://server2",...`).*

Các ứng dụng client kết nối và duy trì kết nối đến một trong các URL nats-server tạo nên cluster đó (ví dụ: `"nats://server1","nats://server2",...`).

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/server-cluster.svg)

## Một super-cluster

> 🇬🇧 *You can go further than a single cluster and have disaster recovery and get global deployments (e.g. on multiple locations or regions, multiple VPCs or multiple Cloud providers) by deploying multiple clusters and connecting them together via gateway connections (which are interest pruned).*

Vượt ra ngoài một cluster đơn lẻ, bạn có thể triển khai nhiều cluster và kết nối chúng lại qua gateway connection (có interest pruning) để đạt được khả năng disaster recovery và deploy toàn cầu — chẳng hạn trên nhiều location, nhiều region, nhiều VPC hoặc nhiều Cloud provider.

> 🇬🇧 *Client applications establish a connection to (one of) the nats server URL(s) of one of the clusters (e.g. `"nats://us-west-1.company.com","nats://us-west-2.company.com",...`).*

Các ứng dụng client kết nối đến một trong các URL nats-server thuộc một cluster bất kỳ trong super-cluster (ví dụ: `"nats://us-west-1.company.com","nats://us-west-2.company.com",...`).

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/super_cluster.svg)

## Với Leaf Node

> 🇬🇧 *You can easily 'extend' the NATS service provided by a cluster or super-cluster by deploying 'locally' one or more **leaf node** nats servers that proxy and route traffic between their client applications and the NATS service infrastructure. The context of 'locality' in this case is not just physical: it could mean a location, an edge device or a single development machine, but it could also service a VPC, a group of server processes for a specific application or different accounts, or even a business unit. Leaf node NATS servers can be configured to connect to their cluster over a WebSocket connection (rather than TLS or plain TCP).*

Bạn có thể dễ dàng "mở rộng" NATS service của một cluster hoặc super-cluster bằng cách deploy "cục bộ" một hoặc nhiều **leaf node** nats-server — các server này hoạt động như proxy, định tuyến traffic giữa ứng dụng client và hạ tầng NATS. "Cục bộ" ở đây không chỉ là vật lý: có thể là một location, một thiết bị edge, một máy development, nhưng cũng có thể là một VPC, một nhóm process cho ứng dụng cụ thể, các account khác nhau, hay thậm chí một đơn vị kinh doanh. Leaf node NATS server có thể được cấu hình để kết nối với cluster qua WebSocket (giao thức WebSocket) thay vì TLS hoặc TCP thuần.

> 🇬🇧 *Leaf nodes appear to the cluster as a single account connection. Leaf nodes can provide continuous NATS service for their clients, even while being temporarily disconnected from the cluster(s). You can even enable JetStream on the leaf nodes in order to create local streams that are mirrored (mirroring is store and forward and therefore can recover from connectivity outages) to global streams in the upstream cluster(s).*

Đối với cluster, leaf node hiện ra như một kết nối account đơn lẻ. Leaf node có thể cung cấp NATS service liên tục cho client ngay cả khi tạm thời bị ngắt kết nối khỏi cluster. Bạn còn có thể bật JetStream trên leaf node để tạo các stream (luồng message lưu trữ liên tục) cục bộ và mirror chúng lên stream toàn cầu ở cluster upstream — quá trình mirror theo kiểu store-and-forward nên có thể phục hồi sau sự cố kết nối.

> 🇬🇧 *Client applications are configured with the URLs of their 'local' leaf node server(s) and establish a connection to (one of) the leaf node server(s) (e.g. `"nats://leaf-node-1","nats://leaf-node-2",...`).*

Các ứng dụng client được cấu hình với URL của leaf node server "cục bộ" và kết nối đến một trong các leaf node server đó (ví dụ: `"nats://leaf-node-1","nats://leaf-node-2",...`).

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/leaf_nodes.svg)

## Xem thêm

NATS Clusters&#x20;

[Clusters](https://youtu.be/srARy0m9SdI)

NATS Super-clusters&#x20;

[Super-clusters](https://youtu.be/6O_sNSJ2p70)

NATS Leaf Nodes&#x20;

[Leaf Nodes](https://youtu.be/WH55czo1BNk)

NATS Service Geo-affinity in Queues&#x20;

[Geo-affinity in Queues](https://youtu.be/jLTVhP08Tq0?t=190)

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **deploy**: triển khai
- **node**: một server trong cluster
- **stream**: luồng message lưu trữ liên tục
- **TLS**: mã hóa TLS
- **WebSocket**: giao thức WebSocket