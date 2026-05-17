---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/gateways
title: Super-cluster với Gateways
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Super-cluster với Gateways

## Gateways

> 🇬🇧 *Gateways enable connecting one or more clusters together into a full mesh; they allow the formation of superclusters from smaller clusters. Cluster and Gateway protocols listen on different ports. Clustering is used for adjacent servers; gateways are for joining clusters together.*

Gateway cho phép kết nối một hoặc nhiều cluster (cụm nhiều server chạy chung) lại thành một full mesh, tạo nên các supercluster từ các cluster nhỏ hơn. Cluster và Gateway lắng nghe trên các port khác nhau. Clustering dùng cho các server liền kề; gateway dùng để nối các cluster lại với nhau.

> 🇬🇧 *Gateway configuration is similar to clustering:*

Cấu hình Gateway tương tự clustering:

* gateways có một port riêng để lắng nghe các gateway request
* gateways gossip các gateway node và các gateway được phát hiện từ xa

> 🇬🇧 *Unlike clusters, gateways:*

Khác với cluster, gateways:

* có tên, xác định cluster mà chúng thuộc về
* không tạo full mesh giữa các gateway node, mà tạo full mesh giữa các cluster
* bị ràng buộc bởi các kết nối một chiều (uni-directional)
* không gossip các gateway node tới client

> 🇬🇧 *Gateways exist to:*

Gateways được tạo ra để:

* giảm số lượng kết nối cần thiết giữa các server
* tối ưu hóa việc lan truyền interest graph

> 🇬🇧 *If gateways are to be used in a cluster, **all** servers of this cluster need to have a gateway configuration with the **same name**. Furthermore, every gateway node needs to be able to **connect to any** other gateway node and vice versa. Everything else is considered a misconfiguration.*

Nếu dùng gateway trong một cluster, **tất cả** server của cluster đó phải có cấu hình gateway với **cùng tên**. Ngoài ra, mỗi gateway node phải có khả năng **kết nối với bất kỳ** gateway node nào khác và ngược lại. Mọi trường hợp khác đều được xem là cấu hình sai.

## Kết nối Gateway

> 🇬🇧 *A nats-server in a gateway role will specify a port where it will accept gateway connections. If the configuration specifies other _external_ `gateways`, the gateway will create one outbound gateway connection for each gateway in its configuration. It will also gossip other gateways it knows or discovers. Fewer _external_ `gateways` mean less configuration. Yet, the ability to discover more gateways and gateway nodes depends on these servers running. This is similar to _seed server_ in cluster. It is recommended to have all _seed server_ of a cluster listed in the `gateways` section.*

Một nats-server ở vai trò gateway sẽ chỉ định một port để chấp nhận các gateway connection. Nếu config chỉ định các _external_ `gateways` khác, gateway sẽ tạo một outbound gateway connection cho mỗi gateway trong config của nó. Nó cũng sẽ gossip các gateway mà nó biết hoặc khám phá được. Càng ít _external_ `gateways` thì càng ít cấu hình. Tuy nhiên, khả năng khám phá thêm gateway và gateway node phụ thuộc vào việc các server đó có đang chạy hay không. Điều này tương tự _seed server_ trong cluster. Nên liệt kê tất cả _seed server_ của một cluster trong phần `gateways`.

> 🇬🇧 *If the local cluster has three gateway nodes, this means there will be three outbound connections from the local cluster to each external gateway cluster.*

Nếu cluster nội bộ có ba gateway node, sẽ có ba outbound connection từ cluster nội bộ tới mỗi external gateway cluster.

![Gateway Connections](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/simple.svg)

> Trong ví dụ trên, cluster _A_ đã cấu hình gateway connection tới _B_ (đường liền). _B_ đã phát hiện gateway connection tới _A_ (đường chấm). Lưu ý số outgoing connection luôn khớp với số gateway cùng tên.

![Gateway Discovered Gateways](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/three_gw.svg)

> Trong ví dụ thứ hai, các kết nối đã cấu hình hiển thị bằng đường liền, các gateway connection được phát hiện hiển thị bằng đường chấm. Gateway _A_ và _C_ đều được phát hiện qua gossiping; _B_ phát hiện _A_ và _A_ phát hiện _C_.

> 🇬🇧 *A key point in the description above is that each node in the cluster will make a connection to a single node in every remote cluster — a difference from the clustering protocol, where every node is directly connected to all other nodes.*

Điểm quan trọng trong mô tả trên là mỗi node trong cluster chỉ kết nối tới một node trong mỗi remote cluster — khác với clustering protocol, nơi mọi node đều kết nối trực tiếp với tất cả node còn lại.

> 🇬🇧 *For those mathematically inclined, cluster connections are `N(N-1)/2` where _N_ is the number of nodes in the cluster. On gateway configurations, outbound connections are the summation of `Ni(M-1)` where Ni is the number of nodes in a gateway _i_, and _M_ is the total number of gateways. Inbound connections are the summation of `U-Ni` where U is the sum of all gateway nodes in all gateways, and N is the number of nodes in a gateway _i_. It works out that both inbound and outbound connection counts are the same.*

Về mặt toán học, số kết nối trong cluster là `N(N-1)/2` với _N_ là số node trong cluster. Với cấu hình gateway, số outbound connection là tổng của `Ni(M-1)` trong đó Ni là số node trong gateway _i_ và _M_ là tổng số gateway. Số inbound connection là tổng của `U-Ni` trong đó U là tổng tất cả gateway node trong mọi gateway và N là số node trong gateway _i_. Kết quả là số inbound và outbound connection bằng nhau.

> 🇬🇧 *The number of connections required to join clusters using clustering vs. gateways is apparent very quickly. For 3 clusters, with N nodes:*

Sự khác biệt về số kết nối khi dùng clustering so với gateway thể hiện rõ nhanh chóng. Với 3 cluster, N node mỗi cluster:

| Nodes per Cluster | Full Mesh Conns | Gateway Conns |
| ---: | ---: | ---: |
| 1 | 3 | 6 |
| 2 | 15 | 12 |
| 3 | 36 | 18 |
| 4 | 66 | 24 |
| 5 | 105 | 30 |
| 30 | 4005 | 180 |

> 🇬🇧 *A cluster section is not needed for gateways, they work with single server as well. Yet, they start to be useful when participating cluster consist of more than one server and they reduce the number of connections.*

Gateway không yêu cầu phần cấu hình cluster, chúng hoạt động được ngay cả với một server đơn lẻ. Tuy nhiên, gateway thực sự hữu ích khi cluster tham gia có nhiều hơn một server và giúp giảm số lượng kết nối.

## Lan Truyền Interest

> 🇬🇧 *Messages from clients directly connected to a gateway node will be sent along outgoing gateway connections according to the following two interest propagation mechanisms:*

Các message từ client kết nối trực tiếp tới gateway node sẽ được gửi qua các outgoing gateway connection theo hai cơ chế lan truyền interest sau:

* Interest-only Mode
* Queue Subscriptions

> 🇬🇧 *Local interest permitting, the receiving gateway node sends the messages directly to its subscribing clients as well as the server within the cluster.*

Nếu local interest cho phép, gateway node nhận sẽ gửi message trực tiếp tới các client đang subscribe cũng như server trong cluster.

### Interest-only Mode

> 🇬🇧 *Gateway _A_ sends messages only for subjects that gateway _B_ has explicitly expressed interest in. As subscriptions come and go on _B_, _B_ will update its subject interest with _A_.*

Gateway _A_ chỉ gửi message cho các subject (chuỗi định danh message) mà gateway _B_ đã thể hiện interest rõ ràng. Khi subscription trên _B_ thay đổi, _B_ sẽ cập nhật subject interest của mình với _A_.

### Queue Subscriptions

> 🇬🇧 *When a queue subscriber creates a new subscription, the gateway propagates the subscription interest to other gateways. The subscription interest is only propagated _once_ per _Account_ and subject. When the last queue subscriber is gone, the cluster interest is removed.*

Khi một queue subscriber tạo subscription mới, gateway lan truyền subscription interest tới các gateway khác. Subscription interest chỉ được lan truyền _một lần_ cho mỗi _Account_ và subject. Khi queue subscriber cuối cùng ngắt kết nối, cluster interest sẽ bị xóa.

> 🇬🇧 *Queue subscriptions work on _Interest-only Mode_ to honor NATS' queue semantics across the _Super Cluster_. For each queue group, a message is only delivered to a single queue subscriber. If the same queue group exists in multiple clusters, the server will pick one member from the queue group in its cluster, only sending to a different cluster if there is no interest in its cluster. In other words, a server will always try to serve local queue subscribers first and only failover when a local queue subscriber is not found. The server will pick the cluster with the lowest RTT.*

Queue subscription hoạt động theo _Interest-only Mode_ để tuân thủ ngữ nghĩa queue của NATS trong toàn bộ _Super Cluster_. Với mỗi queue group (nhóm subscribers chia sẻ tải), một message chỉ được giao tới một queue subscriber duy nhất. Nếu cùng queue group tồn tại ở nhiều cluster, server sẽ chọn một thành viên từ queue group trong cluster của mình, chỉ gửi sang cluster khác khi không có interest ở cluster nội bộ. Nói cách khác, server luôn ưu tiên phục vụ queue subscriber nội bộ trước, chỉ failover khi không tìm thấy. Server sẽ chọn cluster có RTT thấp nhất.

### Cấu hình Gateway

> 🇬🇧 *The [Gateway Configuration](./gateway.md) document describes all the options available to gateways.*

Tài liệu [Gateway Configuration](./gateway.md) mô tả tất cả các tùy chọn có sẵn cho gateway.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **message**: gói dữ liệu được gửi đi
- **node**: một server trong cluster
- **queue group**: nhóm subscribers chia sẻ tải
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message