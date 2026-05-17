---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/clustering/jetstream_clustering
title: JetStream Clustering
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# JetStream Clustering

> 🇬🇧 *Clustering in JetStream is required for a highly available and scalable system. Behind clustering is RAFT. There's no need to understand RAFT in depth to use clustering, but knowing a little explains some of the requirements behind setting up JetStream clusters.*

Clustering (cụm nhiều server chạy chung) trong JetStream là yêu cầu bắt buộc để xây dựng hệ thống có tính sẵn sàng cao và khả năng mở rộng. Nền tảng của clustering là thuật toán RAFT. Không cần hiểu sâu về RAFT để sử dụng clustering, nhưng nắm được cơ bản sẽ giúp hiểu lý do đằng sau các yêu cầu khi thiết lập JetStream cluster.

## RAFT

> 🇬🇧 *JetStream uses a NATS optimized RAFT algorithm for clustering. Typically RAFT generates a lot of traffic, but the NATS server optimizes this by combining the data plane for replicating messages with the messages RAFT would normally use to ensure consensus. Each server participating requires an unique `server_name` (only applies within the same domain).*

JetStream sử dụng thuật toán RAFT được tối ưu hóa cho NATS. Thông thường RAFT tạo ra lượng traffic lớn, nhưng NATS server tối ưu bằng cách kết hợp data plane để replicate message với các message RAFT dùng để đảm bảo consensus. Mỗi server tham gia cluster cần một `server_name` duy nhất (chỉ áp dụng trong cùng một domain).

### RAFT Groups

> 🇬🇧 *The RAFT groups include API handlers, streams, consumers, and an internal algorithm designates which servers handle which streams and consumers.*

Các RAFT group bao gồm API handler, stream (luồng message lưu trữ liên tục), consumer (bên xử lý dữ liệu từ stream), và một thuật toán nội bộ xác định server nào xử lý stream và consumer nào.

> 🇬🇧 *The RAFT algorithm has a few requirements:*
> 🇬🇧 ** A log to persist state*
> 🇬🇧 ** A quorum for consensus*

Thuật toán RAFT có một số yêu cầu:

* Một log để lưu trữ state
* Một quorum để đạt consensus

### The Quorum

> 🇬🇧 *In order to ensure data consistency across complete restarts, a quorum of servers is required. A quorum is ½ cluster size + 1. This is the minimum number of nodes to ensure at least one node has the most recent data and state after a catastrophic failure. So for a cluster size of 3, you'll need at least two JetStream enabled NATS servers available to store new messages. For a cluster size of 5, you'll need at least 3 NATS servers, and so forth.*

Để đảm bảo tính nhất quán dữ liệu khi khởi động lại toàn bộ hệ thống, cần có một quorum các server. Quorum bằng ½ kích thước cluster + 1 — đây là số node (một server trong cluster) tối thiểu để đảm bảo ít nhất một node có dữ liệu và state mới nhất sau sự cố nghiêm trọng. Với cluster 3 node, cần ít nhất 2 NATS server có bật JetStream để lưu message mới. Với cluster 5 node, cần ít nhất 3 server, và tương tự cho các kích thước lớn hơn.

### RAFT Groups

> 🇬🇧 ***Meta Group** - all servers join the Meta Group and the JetStream API is managed by this group. A leader is elected and this owns the API and takes care of server placement.*

**Meta Group** — tất cả server tham gia Meta Group và API (giao diện lập trình) JetStream được quản lý bởi group này. Một leader (server chính trong nhóm replica) được bầu chọn, nắm quyền sở hữu API và phụ trách việc đặt server.

![Meta Group](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/meta-group.png)

> 🇬🇧 ***Stream Group** - each Stream creates a RAFT group, this group synchronizes state and data between its members. The elected leader handles ACKs and so forth, if there is no leader the stream will not accept messages.*

**Stream Group** — mỗi stream tạo một RAFT group riêng, group này đồng bộ state và dữ liệu giữa các thành viên. Leader được bầu sẽ xử lý ACK và các tác vụ liên quan; nếu không có leader, stream sẽ không chấp nhận message.

![Stream Groups](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/stream-groups.png)

> 🇬🇧 ***Consumer Group** - each Consumer creates a RAFT group, this group synchronizes consumer state between its members. The group will live on the machines where the Stream Group is and handle consumption ACKs etc. Each Consumer will have their own group.*

**Consumer Group** — mỗi consumer tạo một RAFT group riêng, group này đồng bộ trạng thái consumer giữa các thành viên. Group này nằm trên các máy chạy Stream Group và xử lý các ACK tiêu thụ. Mỗi consumer có group riêng của mình.

![Consumer Groups](https://raw.githubusercontent.com/nats-io/nats.docs/master/.gitbook/assets/consumer-groups.png)

### Cluster Size

> 🇬🇧 *Generally, we recommend 3 or 5 JetStream enabled servers in a NATS cluster. This balances scalability with a tolerance for failure. For example, if 5 servers are JetStream enabled you would want two servers in one "zone", two servers in another, and the remaining server in a third. This means you can lose any one "zone" at any time and continue operating.*

Thông thường, nên dùng 3 hoặc 5 server có bật JetStream trong một NATS cluster. Cách này cân bằng giữa khả năng mở rộng và khả năng chịu lỗi. Ví dụ, với 5 server JetStream, nên đặt 2 server ở một "zone", 2 server ở zone khác, và server còn lại ở zone thứ ba — để mất bất kỳ zone nào hệ thống vẫn tiếp tục hoạt động.

### Mixing JetStream enabled servers with standard NATS servers

> 🇬🇧 *This is possible and even recommended in some cases. By mixing server types you can dedicate certain machines optimized for storage for Jetstream and others optimized solely for compute for standard NATS servers, reducing operational expense. With the right configuration, the standard servers would handle non-persistent NATS traffic and the JetStream enabled servers would handle JetStream traffic.*

Việc kết hợp server JetStream với NATS server thông thường là hoàn toàn khả thi và thậm chí được khuyến nghị trong một số trường hợp. Bằng cách kết hợp hai loại server, có thể dành riêng các máy tối ưu cho storage cho JetStream và các máy tối ưu cho compute cho NATS server thông thường, giảm chi phí vận hành. Với config phù hợp, các server thông thường sẽ xử lý traffic NATS không cần lưu trữ, còn các server JetStream xử lý traffic JetStream.

## Configuration

> 🇬🇧 *To configure JetStream clusters, just configure clusters as you normally would by specifying a cluster block in the configuration. Any JetStream enabled servers in the list of clusters will automatically chatter and set themselves up. Unlike core NATS clustering though, each JetStream node **must specify** a server name and cluster name.*

Để cấu hình JetStream cluster, chỉ cần cấu hình cluster như thông thường bằng cách khai báo một `cluster` block trong config. Các server có bật JetStream trong danh sách cluster sẽ tự động giao tiếp và tự thiết lập. Tuy nhiên, khác với core NATS clustering, mỗi JetStream node **bắt buộc phải chỉ định** server name và cluster name.

> 🇬🇧 *Below are explicitly listed server configuration for a three-node cluster across three machines, `n1-c1`, `n2-c1`, and `n3-c1`.*

Dưới đây là cấu hình tường minh cho cluster 3 node trên ba máy: `n1-c1`, `n2-c1`, và `n3-c1`.

### Server password configuration

> 🇬🇧 *A user and password under the [system account ($SYS)](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts#system-account) should be configured. The following configuration uses a [bcrypted password](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/auth\_intro/username\_password): `a very long s3cr3t! password`.*

Nên cấu hình user và password trong [system account ($SYS)](https://docs.nats.io/running-a-nats-service/configuration/sys\_accounts#system-account). Cấu hình sau sử dụng [bcrypted password](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/auth\_intro/username\_password): `a very long s3cr3t! password`.

### Server 1 (host\_a)

```
server_name=n1-c1
listen=4222

accounts {
  $SYS {
    users = [
      { user: "admin",
        pass: "$2a$11$DRh4C0KNbNnD8K/hb/buWe1zPxEHrLEiDmuq1Mi0rRJiH/W25Qidm"
      }
    ]
  }
}

jetstream {
   store_dir=/nats/storage
}

cluster {
  name: C1
  listen: 0.0.0.0:6222
  routes: [
    nats://host_b:6222
    nats://host_c:6222
  ]
}
```

### Server 2 (host\_b)

```
server_name=n2-c1
listen=4222

accounts {
  $SYS {
    users = [
      { user: "admin",
        pass: "$2a$11$DRh4C0KNbNnD8K/hb/buWe1zPxEHrLEiDmuq1Mi0rRJiH/W25Qidm"
      }
    ]
  }
}

jetstream {
   store_dir=/nats/storage
}

cluster {
  name: C1
  listen: 0.0.0.0:6222
  routes: [
    nats://host_a:6222
    nats://host_c:6222
  ]
}
```

### Server 3 (host\_c)

```
server_name=n3-c1
listen=4222

accounts {
  $SYS {
    users = [
      { user: "admin",
        pass: "$2a$11$DRh4C0KNbNnD8K/hb/buWe1zPxEHrLEiDmuq1Mi0rRJiH/W25Qidm"
      }
    ]
  }
}

jetstream {
   store_dir=/nats/storage
}

cluster {
  name: C1
  listen: 0.0.0.0:6222
  routes: [
    nats://host_a:6222
    nats://host_b:6222
  ]
}
```

> 🇬🇧 *Add nodes as necessary. Choose a data directory that makes sense for your environment, ideally a fast SSD, and launch each server. After two servers are running you'll be ready to use JetStream.*

Thêm node tùy theo nhu cầu. Chọn thư mục dữ liệu phù hợp với môi trường của bạn — lý tưởng nhất là SSD nhanh — rồi khởi động từng server. Sau khi có ít nhất 2 server chạy, bạn đã sẵn sàng sử dụng JetStream.

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **leader**: server chính trong nhóm replica
- **node**: một server trong cluster
- **server**: máy chủ
- **stream**: luồng message lưu trữ liên tục