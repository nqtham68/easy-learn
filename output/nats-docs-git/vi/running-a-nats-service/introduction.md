---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/introduction
title: Giới thiệu
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

> 🇬🇧 *The NATS Server is highly optimized and its binary is very compact (less than 20 MB), it can run on any machine from a lowly Raspberry Pi to the largest of servers, in the cloud, on premise or at the edge, on bare metal, on VMs or in containers.*

NATS Server được tối ưu hóa cao, với binary (file chương trình đã biên dịch) chỉ khoảng 20 MB. Server có thể chạy trên mọi loại máy, từ Raspberry Pi cho đến server mạnh nhất, dù là trên cloud, on-premise, edge, bare metal, VM hay container.

> 🇬🇧 *NATS Servers can cluster together to provide fault-tolerance and scalability. NATS servers can run as Leaf Nodes connecting to a cluster transparently proxying and expanding NATS and JetStream service to any location, be it a VPC, a VLAN, a remote office, a single machine at home or even an edge location with partial connectivity.*

Nhiều NATS Server có thể tạo thành cluster (cụm nhiều server chạy chung) để đảm bảo khả năng chịu lỗi và mở rộng. Server cũng có thể chạy ở chế độ Leaf Node, kết nối vào một cluster và mở rộng dịch vụ NATS cùng JetStream đến bất kỳ vị trí nào — VPC, VLAN, văn phòng từ xa, máy tính cá nhân hay thậm chí edge location với kết nối không ổn định.

> 🇬🇧 *NATS clusters in different regions or cloud providers can be connected together by gateways that filter unneeded traffic and allow for disaster recovery and queued distributed processing with geo-location affinity.*

Các cluster ở nhiều khu vực hoặc cloud provider khác nhau có thể liên kết với nhau qua gateway. Gateway lọc traffic không cần thiết, hỗ trợ disaster recovery và xử lý phân tán có ưu tiên theo vị trí địa lý.

> 🇬🇧 *Even better, if you have build your application with NATS you don't need to run your own server, cluster, or super-cluster and can simply leverage Synadia's [NGS](https://www.synadia.com/cloud), the global NATS super-cluster service provided by [Synadia](https://www.synadia.com?utm_source=nats_docs&utm_medium=nats).*

Tốt hơn nữa, nếu ứng dụng của bạn đã xây dựng trên NATS, bạn không cần tự vận hành server, cluster hay super-cluster. Thay vào đó, hãy sử dụng [NGS](https://www.synadia.com/cloud) của Synadia — dịch vụ NATS super-cluster toàn cầu do [Synadia](https://www.synadia.com?utm_source=nats_docs&utm_medium=nats) cung cấp.

> 🇬🇧 *This section of the documentation explains how to install, deploy, run, configure, orchestrate, test and manage NATS servers.*

Phần tài liệu này hướng dẫn cách cài đặt, deploy (triển khai), chạy, cấu hình, điều phối, kiểm thử và quản lý NATS server.

## Thuật ngữ trong bài

- **binary**: file chương trình đã biên dịch
- **cluster**: cụm nhiều server chạy chung
- **container**: container (đóng gói app)
- **deploy**: triển khai
- **service**: dịch vụ