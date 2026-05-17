---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/clustering/jetstream_clustering/administration
title: Quản trị JetStream Cluster
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Quản trị JetStream Cluster

> 🇬🇧 *Once a JetStream cluster is operating interactions with the CLI and with `nats` CLI is the same as before. For these examples, lets assume we have a 5 server cluster, n1-n5 in a cluster named C1.*

Khi JetStream cluster (cụm nhiều server chạy chung) đã hoạt động, tương tác qua CLI và `nats` CLI vẫn như cũ. Trong các ví dụ dưới đây, giả sử ta có một cluster 5 server từ n1 đến n5, đặt tên là C1.

## Cấp tài khoản

> 🇬🇧 *Within an account there are operations and reports that show where users data is placed and which allow them some basic interactions with the RAFT system.*

Trong phạm vi tài khoản, có các thao tác và báo cáo cho thấy dữ liệu người dùng được đặt ở đâu, đồng thời cho phép thực hiện một số thao tác cơ bản với hệ thống RAFT.

## Tạo stream phân cụm

> 🇬🇧 *When adding a stream using the `nats` CLI the number of replicas will be asked, when you choose a number more than 1, \(we suggest 1, 3 or 5\), the data will be stored on multiple nodes in your cluster using the RAFT protocol as above.*

Khi thêm stream (luồng message lưu trữ liên tục) qua `nats` CLI, bạn sẽ được hỏi số lượng replica (bản sao dữ liệu). Nếu chọn số lớn hơn 1 (khuyến nghị là 1, 3 hoặc 5), dữ liệu sẽ được lưu trữ trên nhiều node trong cluster theo giao thức RAFT như đã mô tả ở trên.

```shell
nats stream add ORDERS --replicas 3
```
Example output extract:
```text
....
Information for Stream ORDERS created 2021-02-05T12:07:34+01:00
....
Configuration:
....
             Replicas: 3

Cluster Information:

                 Name: C1
               Leader: n1-c1
              Replica: n4-c1, current, seen 0.07s ago
              Replica: n3-c1, current, seen 0.07s ago
```

> 🇬🇧 *Above you can see that the cluster information will be reported in all cases where Stream info is shown such as after add or using `nats stream info`.*

Thông tin cluster sẽ được hiển thị trong mọi trường hợp xem Stream info, chẳng hạn sau khi thêm stream hoặc dùng `nats stream info`.

> 🇬🇧 *Here we have a stream in the NATS cluster `C1`, its current leader is a node `n1-c1` and it has 2 followers - `n4-c1` and `n3-c1`.*

Ở đây, stream nằm trong NATS cluster `C1`, leader (server chính trong nhóm replica) hiện tại là node `n1-c1` và có 2 follower là `n4-c1` và `n3-c1`.

> 🇬🇧 *The `current` indicates that followers are up to date and have all the messages, here both cluster peers were seen very recently.*

`current` cho biết các follower đã cập nhật đầy đủ và có toàn bộ message. Trong ví dụ này, cả hai cluster peer đều được ghi nhận rất gần đây.

> 🇬🇧 *The replica count can be edited once configured.*

Số lượng replica có thể chỉnh sửa sau khi đã cấu hình.

### Xem vị trí và thống kê Stream

> 🇬🇧 *Users can get overall statistics about their streams and also where these streams are placed:*

Người dùng có thể xem thống kê tổng thể về các stream và vị trí đặt chúng:

```shell
nats stream report
```
```text
Obtaining Stream stats
+----------+-----------+----------+--------+---------+------+---------+----------------------+
| Stream   | Consumers | Messages | Bytes  | Storage | Lost | Deleted | Cluster              |
+----------+-----------+----------+--------+---------+------+---------+----------------------+
| ORDERS   | 4         | 0        | 0 B    | File    | 0    | 0       | n1-c1*, n2-c1, n3-c1 |
| ORDERS_3 | 4         | 0        | 0 B    | File    | 0    | 0       | n1-c1*, n2-c1, n3-c1 |
| ORDERS_4 | 4         | 0        | 0 B    | File    | 0    | 0       | n1-c1*, n2-c1, n3-c1 |
| ORDERS_5 | 4         | 0        | 0 B    | File    | 0    | 0       | n1-c1, n2-c1, n3-c1* |
| ORDERS_2 | 4         | 1,385    | 13 MiB | File    | 0    | 1       | n1-c1, n2-c1, n3-c1* |
| ORDERS_0 | 4         | 1,561    | 14 MiB | File    | 0    | 0       | n1-c1, n2-c1*, n3-c1 |
+----------+-----------+----------+--------+---------+------+---------+----------------------+
```

#### Kích hoạt bầu chọn leader cho Stream và Consumer

> 🇬🇧 *Every RAFT group has a leader that's elected by the group when needed. Generally there is no reason to interfere with this process, but you might want to trigger a leader change at a convenient time. Leader elections will represent short interruptions to the stream so if you know you will work on a node later it might be worth moving leadership away from it ahead of time.*

Mỗi nhóm RAFT đều có một leader được bầu chọn khi cần. Thông thường không cần can thiệp vào quá trình này, nhưng đôi khi bạn muốn kích hoạt thay đổi leader vào thời điểm thuận tiện. Việc bầu chọn lại leader gây gián đoạn ngắn trên stream, vì vậy nếu biết trước sẽ bảo trì một node, nên chuyển leadership khỏi node đó trước.

> 🇬🇧 *Moving leadership away from a node does not remove it from the cluster and does not prevent it from becoming a leader again, this is merely a triggered leader election.*

Chuyển leadership khỏi một node không xóa node đó khỏi cluster và không ngăn node đó trở thành leader lại sau này — đây chỉ là bầu chọn leader được kích hoạt thủ công.

```shell
nats stream cluster step-down ORDERS
```
```text
14:32:17 Requesting leader step down of "n1-c1" in a 3 peer RAFT group
14:32:18 New leader elected "n4-c1"

Information for Stream ORDERS created 2021-02-05T12:07:34+01:00
...
Cluster Information:

                 Name: c1
               Leader: n4-c1
              Replica: n1-c1, current, seen 0.12s ago
              Replica: n3-c1, current, seen 0.12s ago
```

> 🇬🇧 *The same is true for consumers, `nats consumer cluster step-down ORDERS NEW`.*

Tương tự đối với consumer (bên xử lý dữ liệu từ stream), `nats consumer cluster step-down ORDERS NEW`.

## Cấp hệ thống

> 🇬🇧 *Systems users can view state of the Meta Group - but not individual Stream or Consumers.*

Người dùng hệ thống có thể xem trạng thái của Meta Group, nhưng không thể xem từng Stream hoặc Consumer riêng lẻ.

### Xem trạng thái cluster

> 🇬🇧 *We have a high level report of cluster state:*

Có thể xem báo cáo tổng quan trạng thái cluster:

```shell
nats server report jetstream --user admin --password s3cr3t!
```
```text
+--------------------------------------------------------------------------------------------------+
|                                        JetStream Summary                                         |
+--------+---------+---------+-----------+----------+--------+--------+--------+---------+---------+
| Server | Cluster | Streams | Consumers | Messages | Bytes  | Memory | File   | API Req | API Err |
+--------+---------+---------+-----------+----------+--------+--------+--------+---------+---------+
| n3-c2  | c2      | 0       | 0         | 0        | 0 B    | 0 B    | 0 B    | 1       | 0       |
| n3-c1  | c1      | 6       | 24        | 2,946    | 27 MiB | 0 B    | 27 MiB | 3       | 0       |
| n2-c2  | c2      | 0       | 0         | 0        | 0 B    | 0 B    | 0 B    | 3       | 0       |
| n1-c2  | c2      | 0       | 0         | 0        | 0 B    | 0 B    | 0 B    | 14      | 2       |
| n2-c1  | c1      | 6       | 24        | 2,946    | 27 MiB | 0 B    | 27 MiB | 15      | 0       |
| n1-c1* | c1      | 6       | 24        | 2,946    | 27 MiB | 0 B    | 27 MiB | 31      | 0       |
+--------+---------+---------+-----------+----------+--------+--------+--------+---------+---------+
|        |         | 18      | 72        | 8,838    | 80 MiB | 0 B    | 80 MiB | 67      | 2       |
+--------+---------+---------+-----------+----------+--------+--------+--------+---------+---------+
+---------------------------------------------------+
|            RAFT Meta Group Information            |
+-------+--------+---------+---------+--------+-----+
| Name  | Leader | Current | Offline | Active | Lag |
+-------+--------+---------+---------+--------+-----+
| n1-c1 | yes    | true    | false   | 0.00s  | 0   |
| n1-c2 |        | true    | false   | 0.05s  | 0   |
| n2-c1 |        | false   | true    | 9.00s  | 2   |
| n2-c2 |        | true    | false   | 0.05s  | 0   |
| n3-c1 |        | true    | false   | 0.05s  | 0   |
| n3-c2 |        | true    | false   | 0.05s  | 0   |
+-------+--------+---------+---------+--------+-----+
```

> 🇬🇧 *This is a full cluster wide report, the report can be limited to a specific account using `--account`.*

Đây là báo cáo toàn cluster. Có thể giới hạn phạm vi theo tài khoản cụ thể bằng `--account`.

> 🇬🇧 *Here we see the distribution of streams, messages, api calls etc by across 2 super clusters and an overview of the RAFT meta group.*

Báo cáo thể hiện phân bổ stream, message, lời gọi API, v.v. trên 2 super cluster và tổng quan về RAFT meta group.

> 🇬🇧 *In the Meta Group report the server `n2-c1` is not current and has not been seen for 9 seconds, it's also behind by 2 raft operations.*

Trong báo cáo Meta Group, server `n2-c1` không cập nhật và không được ghi nhận trong 9 giây, đồng thời đang bị trễ 2 thao tác RAFT.

> 🇬🇧 *This report is built using raw data that can be obtained from the monitor port on the `/jsz` url, or over nats using:*

Báo cáo này được xây dựng từ dữ liệu thô, có thể lấy từ monitor port tại URL `/jsz`, hoặc qua NATS:

```shell
nats server req jetstream --user admin --password s3cr3t! --help
```
```text
usage: nats server request jetstream [<flags>] [<wait>]

Show JetStream details

Flags:
  -h, --help                    Show context-sensitive help (also try --help-long and --help-man).
      --version                 Show application version.
  -s, --server=NATS_URL         NATS server urls
      --user=NATS_USER          Username or Token
      --password=NATS_PASSWORD  Password
      --creds=NATS_CREDS        User credentials
      --nkey=NATS_NKEY          User NKEY
      --tlscert=NATS_CERT       TLS public certificate
      --tlskey=NATS_KEY         TLS private key
      --tlsca=NATS_CA           TLS certificate authority chain
      --timeout=NATS_TIMEOUT    Time to wait on responses from NATS
      --js-api-prefix=PREFIX    Subject prefix for access to JetStream API
      --js-event-prefix=PREFIX  Subject prefix for access to JetStream Advisories
      --js-domain=DOMAIN        JetStream domain to access
      --context=CONTEXT         Configuration context
      --trace                   Trace API interactions
      --limit=2048              Limit the responses to a certain amount of records
      --offset=0                Start at a certain record
      --name=NAME               Limit to servers matching a server name
      --host=HOST               Limit to servers matching a server host name
      --cluster=CLUSTER         Limit to servers matching a cluster name
      --tags=TAGS ...           Limit to servers with these configured tags
      --account=ACCOUNT         Show statistics scoped to a specific account
      --accounts                Include details about accounts
      --streams                 Include details about Streams
      --consumer                Include details about Consumers
      --config                  Include details about configuration
      --leader                  Request a response from the Meta-group leader only
      --all                     Include accounts, streams, consumers and configuration

Args:
  [<wait>]  Wait for a certain number of responses
```

```shell
nats server req jetstream --user admin --password s3cr3t! --leader
```

> 🇬🇧 *This will produce a wealth of raw information about the current state of your cluster - here requesting it from the leader only.*

Lệnh này trả về lượng lớn thông tin thô về trạng thái hiện tại của cluster — trong ví dụ này chỉ yêu cầu từ leader.

#### Kích hoạt bầu chọn leader cho Meta Group

> 🇬🇧 *Similar to Streams and Consumers above the Meta Group allows leader stand down. The Meta Group is cluster wide and spans all accounts, therefore to manage the meta group you have to use a `SYSTEM` user.*

Tương tự Stream và Consumer, Meta Group cũng hỗ trợ yêu cầu leader nhường quyền. Meta Group có phạm vi toàn cluster và bao gồm mọi tài khoản, do đó để quản lý meta group cần dùng user `SYSTEM`.

```shell
nats server cluster step-down --user admin --password s3cr3t!
```
```text
17:44:24 Current leader: n2-c2
17:44:24 New leader: n1-c2
```

### Loại bỏ peer

> 🇬🇧 *Generally when shutting down NATS, including using Lame Duck Mode, the cluster will notice this and continue to function.*

Thông thường khi tắt NATS — kể cả dùng Lame Duck Mode — cluster sẽ tự nhận biết và tiếp tục hoạt động.

> 🇬🇧 *There might be a case though where you know a node will never return, and you want to signal to JetStream that the node will not return. A peer-remove will remove that node from the Stream in question and all its Consumers.*

Tuy nhiên, nếu biết một node sẽ không bao giờ quay lại, bạn cần báo cho JetStream biết điều này. Thao tác peer-remove sẽ xóa node đó khỏi Stream liên quan và tất cả Consumer của nó.

> 🇬🇧 *After the node is removed the cluster will notice that the replica count of a stream is not honored anymore and will immediately pick a new node and start replicating data to it. The new node will be selected using the same placement rules as the existing stream.*

Sau khi xóa node, cluster sẽ nhận ra số lượng replica của stream không còn đủ và lập tức chọn một node mới để bắt đầu sao chép dữ liệu. Node mới được chọn theo cùng quy tắc đặt chỗ của stream hiện tại.

```shell
nats server cluster peer-remove n4-c1 --user admin --password s3cr3t!
```
```text
? Really remove offline peer n4-c1 (y/N)
```

> **Cảnh báo:**
> Thao tác peer-remove node khỏi cluster là không thể hoàn tác và làm giảm kích thước cluster.
> Node cần peer-remove lý tưởng nên đã offline. Có thể thực hiện với node còn online, nhưng trong trường hợp đó JetStream sẽ bị vô hiệu hóa trên những node này. Node nên được tắt và không khởi động lại; nếu buộc phải khởi động lại, hãy tắt JetStream trước.
> Server có thể không trở lại với cùng `server_name` nếu đã bị peer-remove và xóa disk. Điều này có nghĩa là `server_name` đã cấu hình cần được đổi sang giá trị mới trước khi khởi động lại.

> 🇬🇧 *Alternatively, if you're intending for the node to remain and only move a stream off of a specific node, you can peer-remove a node on the stream-level.*

Ngoài ra, nếu muốn giữ node nhưng chỉ di chuyển một stream ra khỏi node đó, có thể peer-remove ở cấp stream.

```shell
nats stream cluster peer-remove ORDERS
```
```text
? Select a Peer n4-c1
14:38:50 Removing peer "n4-c1"
14:38:50 Requested removal of peer "n4-c1"
```

> 🇬🇧 *At this point the stream and all consumers will have removed `n4-c1` from the group. A new node will be selected, and data will be replicated to it. In this case `n2-c1` is selected as a new peer.*

Sau thao tác này, stream và tất cả consumer sẽ loại `n4-c1` khỏi nhóm. Một node mới sẽ được chọn và dữ liệu sẽ được sao chép đến đó. Trong ví dụ này, `n2-c1` được chọn làm peer mới.

```shell
$ nats stream info ORDERS
```
```text
....
Cluster Information:

                 Name: c1
               Leader: n3-c1
              Replica: n1-c1, current, seen 0.02s ago
              Replica: n2-c1, outdated, seen 0.42s ago
```

> 🇬🇧 *We can see a new replica was picked, the stream is back to replication level of 3 and `n4-c1` is not active any more in this Stream or any of its Consumers.*

Ta có thể thấy một replica mới được chọn, stream trở lại mức replication là 3 và `n4-c1` không còn hoạt động trong Stream này hoặc bất kỳ Consumer nào của nó.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **follower**: server phụ trong nhóm replica
- **leader**: server chính trong nhóm replica
- **message**: gói dữ liệu được gửi đi
- **node**: một server trong cluster
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục