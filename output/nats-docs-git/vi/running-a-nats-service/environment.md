---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/environment
title: Các lưu ý về môi trường triển khai
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Các lưu ý về môi trường triển khai

## Networking

### Load balancers

> 🇬🇧 *It is possible to deploy a load balancer between the client applications and the cluster servers (or even between servers in a cluster or between clusters in a super-cluster), but you don't need to: NATS already has its own mechanisms to balance the connections between the seeds in the connection URL (including the clients randomizing the returned DNS A records) and to automatically re-establish dropped connections. If you have a cluster with 3 seed nodes you often get more network throughput than going through a load balancer (cloud provider load balancers can be woefully under-powered, not to mention it costs you more money as the load balancer is typically billed by the amount of data going through it). Finally, if you want to use TLS for authentication you do not want the load balancer to be the TLS termination point.*

Hoàn toàn có thể đặt load balancer giữa các ứng dụng client và các server trong cluster (hoặc thậm chí giữa các server trong một cluster hay giữa các cluster trong super-cluster), nhưng thực ra không cần thiết: NATS đã có cơ chế riêng để cân bằng kết nối giữa các seed node trong connection URL (bao gồm việc client ngẫu nhiên hóa các bản ghi DNS A được trả về) và tự động kết nối lại khi mất kết nối. Nếu cluster (cụm nhiều server chạy chung) có 3 seed node, thông lượng mạng thường cao hơn so với đi qua load balancer (load balancer của các cloud provider thường yếu, chưa kể chi phí cũng tăng vì thường tính theo lượng dữ liệu đi qua). Ngoài ra, nếu dùng TLS để xác thực, không nên để load balancer là điểm kết thúc TLS.

> 🇬🇧 *⚠️ Warning: If you decide to use load balancers with NATS you need to understand the client and cluster connection and auto-discovery behavior.*
>
> *Client connections and routes are permanent. Therefore a load balancer will not distribute messages from one client connections between servers, or worse (which is common when deploying on auto-config environments), you end up with redundant, but disconnected (non-clustered) servers to which the clients will randomly connect. [Advertising needs to be switched off](./configuration/clustering/cluster_config.md) or configured to point to the load balancer address through the [`advertise` server config](./configuration/clustering/cluster_config.md) option.*
>
> *Load balancers can also cause issues through improperly configured idle detection, protocol problems due to packet inspection, and ephemeral port problems at high scale.*
>
> *If routes or gateway connections go through load balancers, you could very well have the kind of problems mentioned above, which could results in JetStream lost quorum periods and create undue re-synchronization and protocol overhead traffic.*

> **⚠️ Cảnh báo:**
> Nếu quyết định dùng load balancer với NATS, cần hiểu rõ hành vi kết nối và auto-discovery của client lẫn cluster.
>
> Kết nối client và các route là cố định (permanent). Do đó load balancer sẽ không phân phối message từ một kết nối client sang nhiều server — hoặc tệ hơn (phổ biến trong môi trường auto-config), bạn sẽ có các server dư thừa nhưng bị ngắt kết nối khỏi cluster, và client sẽ kết nối ngẫu nhiên vào chúng. Cần [tắt advertising](./configuration/clustering/cluster_config.md) hoặc cấu hình trỏ về địa chỉ load balancer qua tùy chọn [`advertise` server config](./configuration/clustering/cluster_config.md).
>
> Load balancer cũng có thể gây ra sự cố do cấu hình idle detection không đúng, vấn đề giao thức do packet inspection, và ephemeral port khi tải cao.
>
> Nếu các route hoặc kết nối gateway đi qua load balancer, rất có thể xảy ra các vấn đề trên, dẫn đến JetStream mất quorum trong một khoảng thời gian và tạo ra lưu lượng re-synchronization cùng protocol overhead không cần thiết.

> 🇬🇧 *There are some sensible use cases for running client connections through load balancers. If the balanced NATS servers are setup as clusters (or superclusters), which provide transparent message routing, the load balancer can simplify the client config by presenting a single port of entry, or automatically connect to the geographically closed cluster node.*

Vẫn có những trường hợp hợp lý để chạy kết nối client qua load balancer. Nếu các NATS server được cân bằng tải đã được cấu hình thành cluster (hoặc supercluster) — vốn cung cấp routing message trong suốt — thì load balancer có thể đơn giản hóa config của client bằng cách cung cấp một điểm vào duy nhất, hoặc tự động kết nối đến node trong cluster gần về mặt địa lý nhất.

## Ảo hóa và Container hóa

> 🇬🇧 *NATS is 'cloud native' and expected to be deployed in virtual environments and/or containers.*

NATS là hệ thống "cloud native" và được thiết kế để triển khai (deploy) trong môi trường ảo hóa và/hoặc container.

> 🇬🇧 *However, when it comes to ensuring the highest possible level of performance that NATS can provide it is good to keep a few things in mind.*

Tuy nhiên, để đảm bảo NATS hoạt động ở mức hiệu năng cao nhất, cần lưu ý một số điểm sau.

> 🇬🇧 *Think of Core NATS servers as a software equivalent of network switches. Enable JetStream, and they also become a new kind of DB server as well.*

Hãy xem Core NATS server như tương đương phần mềm của các network switch. Bật JetStream lên, chúng còn trở thành một loại DB server mới.

> 🇬🇧 *What you need to remember is that when selecting the instance types and storage options for your NATS server host instances that in public clouds: you get what you pay for.*

Điều cần nhớ khi chọn loại instance và tùy chọn lưu trữ cho các host instance chạy NATS server trên public cloud là: **bạn trả tiền bao nhiêu thì nhận được chất lượng bấy nhiêu**.

> 🇬🇧 *For example non network optimized instances may give you 10 Gb/s of network bandwidth... but only for some period of time (like 30 minutes), after which the available bandwidth may drop down dramatically (like to 5 Gb/s) for another period of time. So select network optimized instances types instead if you always need the advertised bandwidth.*

Ví dụ, các instance không được tối ưu hóa mạng có thể cho băng thông 10 Gb/s... nhưng chỉ trong một khoảng thời gian nhất định (khoảng 30 phút), sau đó băng thông có thể giảm mạnh (xuống còn 5 Gb/s) trong một khoảng thời gian tiếp theo. Vì vậy, hãy chọn loại instance tối ưu hóa mạng nếu cần băng thông ổn định liên tục.

> 🇬🇧 *It's the same when it comes to storage options: local SSDs instance types can provide the best latency, while using a network attached block storage, e.g. Elastic Block Storage from AWS), can provide the highest overall throughput. When using EBS again you get what you pay for: general purpose storage type may give you a certain number of IOPS, but you can sustain those rates only for some period of time after which the number can drop down dramatically. So select IO optimized storage types if you want to continuously sustain the same max number of IOPS (e.g. [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)).*

Tương tự với tùy chọn lưu trữ: loại instance dùng local SSD cho độ trễ thấp nhất, trong khi block storage gắn qua mạng (ví dụ Elastic Block Storage của AWS) lại cho throughput tổng thể cao nhất. Khi dùng EBS, nguyên tắc "tiền nào của đó" vẫn áp dụng: loại general purpose có thể cho một số IOPS nhất định, nhưng chỉ duy trì được trong một thời gian rồi giảm mạnh. Hãy chọn loại IO optimized nếu muốn duy trì số IOPS tối đa liên tục (xem thêm tại [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)).

### Giới hạn tài nguyên

> 🇬🇧 *Be careful when setting resource limits for the nats-server containers. The nats-server processes use resources in proportion to the load traffic generated by all the client applications, if the NATS (and JetStream) usage is high or in bursts (nats-server is very fast and can process sharp bursts in traffic), then you will need to set the container resource limits accordingly, or the container orchestration system will kill the server's container. The nats-server will automatically detect number of available cores, but it will try to use all host memory, not the resource limits set for the container, unless you specify GOMEMLIMIT. GOMEMLIMIT is an available option in official NATS helm charts.*

Cần thận trọng khi đặt giới hạn tài nguyên cho các container nats-server. Tiến trình nats-server sử dụng tài nguyên tỉ lệ với lưu lượng tải do tất cả ứng dụng client tạo ra — nếu mức sử dụng NATS (và JetStream) cao hoặc đến theo từng đợt bùng phát (nats-server rất nhanh và xử lý được các đợt bùng phát đột ngột), bạn cần đặt giới hạn tài nguyên container phù hợp, nếu không hệ thống container orchestration sẽ kill container của server. nats-server tự động phát hiện số core khả dụng, nhưng sẽ cố dùng toàn bộ bộ nhớ của host chứ không phải giới hạn tài nguyên đặt cho container, trừ khi bạn chỉ định `GOMEMLIMIT`. `GOMEMLIMIT` là một tùy chọn có sẵn trong NATS helm charts chính thức.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **container**: container (đóng gói app)
- **deploy**: triển khai
- **host**: máy chủ vật lý/ảo
- **message**: gói dữ liệu được gửi đi
- **node**: một server trong cluster
- **route**: đường dẫn URL
- **stream**: luồng message lưu trữ liên tục
- **TLS**: mã hóa TLS