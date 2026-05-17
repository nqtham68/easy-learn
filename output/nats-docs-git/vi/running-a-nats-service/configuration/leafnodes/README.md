---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/leafnodes
title: Leaf Nodes (Nút Lá)
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Leaf Nodes (Nút Lá)

> 🇬🇧 *A _Leaf Node_ extends an existing NATS system of any size, optionally bridging both operator and security domains. A leafnode server will transparently route messages as needed from local clients to one or more remote NATS system(s) and vice versa. The leaf node authenticates and authorizes clients using a local policy. Messages are allowed to flow to the cluster or into the leaf node based on leaf node connection permissions of either.*

Leaf Node mở rộng một hệ thống NATS hiện có ở bất kỳ quy mô nào, đồng thời có thể kết nối liền mạch giữa hai operator và security domain. Server leaf node sẽ tự động định tuyến message đến một hoặc nhiều hệ thống NATS từ xa và ngược lại. Leaf node xác thực và phân quyền client theo policy cục bộ. Message được phép lưu thông lên cluster (cụm nhiều server chạy chung) hoặc vào trong leaf node dựa trên permission (quyền truy cập) kết nối leaf node của từng phía.

> 🇬🇧 *Leaf nodes are useful in IoT and edge scenarios and when the local server traffic should be low RTT and local unless routed to the super cluster. NATS' queue semantics are honored across leaf connections by serving local queue consumers first.*

Leaf node phù hợp cho các tình huống IoT và edge, khi traffic nội bộ cần độ trễ thấp và chỉ định tuyến ra ngoài khi cần thiết. Ngữ nghĩa queue của NATS được đảm bảo xuyên suốt các kết nối leaf — consumer cục bộ luôn được ưu tiên phục vụ trước.

> 🇬🇧 *- Clients to leaf nodes authenticate locally (or just connect if authentication is not required)*
> *- Traffic between the leaf node and the cluster assumes the restrictions of the user configuration used to create the leaf connection.*
> *  - Subjects that the user is allowed to publish are exported to the cluster.*
> *  - Subjects the user is allowed to subscribe to, are imported into the leaf node.*

- Client kết nối đến leaf node được xác thực cục bộ (hoặc kết nối trực tiếp nếu không yêu cầu xác thực).
- Traffic giữa leaf node và cluster tuân theo các giới hạn của user config dùng để tạo kết nối leaf.
  - Những subject (chuỗi định danh message) mà user được phép publish sẽ được export lên cluster.
  - Những subject mà user được phép subscribe sẽ được import vào leaf node.

> 🇬🇧 *Unlike [cluster](../clustering) or [gateway](../gateways) nodes, leaf nodes do not need to be reachable themselves and can be used to explicitly configure any acyclic graph topologies.*

Khác với [cluster](../clustering) hay [gateway](../gateways), leaf node không cần phải tự mình có thể được kết nối đến từ ngoài, và có thể dùng để cấu hình bất kỳ cấu trúc đồ thị phi chu trình nào một cách tường minh.

> 🇬🇧 *If a leaf node connects to a cluster, it is recommended to configure it with knowledge of **all** _seed servers_ and have **each** _seed server_ accept connections from leaf nodes. Should the remote cluster's configuration change, the discovery protocol will gossip peers capable of accepting leaf connections. A leaf node can have multiple remotes, each connecting to a different cluster. Each URL in a remote needs to point to the same cluster. If one node in a cluster is configured as leaf node, **all** nodes need to. Likewise, if one server in a cluster accepts leaf node connections, **all** servers need to.*

Khi leaf node kết nối đến một cluster, nên cấu hình để nó biết **tất cả** các _seed server_ và để **mỗi** _seed server_ chấp nhận kết nối từ leaf node. Nếu config của remote cluster thay đổi, discovery protocol sẽ gossip danh sách peer có khả năng chấp nhận leaf connection. Một leaf node có thể có nhiều remote, mỗi remote kết nối đến một cluster khác nhau. Mỗi URL trong một remote phải trỏ đến cùng một cluster. Nếu một node trong cluster được cấu hình là leaf node thì **tất cả** các node đều phải vậy. Tương tự, nếu một server trong cluster chấp nhận kết nối leaf node thì **tất cả** các server đều phải chấp nhận.

> 🇬🇧 *Leaf Nodes are an important component as a way to bridge traffic between local NATS servers you control and servers that are managed by a third-party. [Synadia's NGS](https://www.synadia.com/cloud) allows accounts to use leaf nodes, but gain accessibility to the global network to inexpensively connect geographically distributed servers or small clusters.*

Leaf Node là thành phần quan trọng để kết nối traffic giữa NATS server nội bộ do bạn quản lý và server do bên thứ ba vận hành. [Synadia's NGS](https://www.synadia.com/cloud) cho phép tài khoản sử dụng leaf node, qua đó tiếp cận mạng lưới toàn cầu để kết nối các server hoặc cluster phân tán về mặt địa lý với chi phí thấp.

[LeafNode Configuration Options](./leafnode_conf.md)

## Hướng Dẫn Cấu Hình LeafNode

> 🇬🇧 *The main server is just a standard NATS server. Clients to the main cluster are just using token authentication, but any kind of authentication can be used. The server allows leaf node connections at port 7422 (default port):*

Server chính là một NATS server tiêu chuẩn. Client kết nối đến cluster chính sử dụng token authentication, tuy nhiên bất kỳ cơ chế xác thực nào cũng được. Server cho phép kết nối leaf node tại port 7422 (port mặc định):

```
leafnodes {
    port: 7422
}
accounts: {
    app: { 
        users: [
            {user: appuser, password: s3cr3t},
            {user: leafuser, password: s3cr3t}
           ]
    }  
}
```

> 🇬🇧 *Start the server:*

Khởi động server:

```bash
nats-server -c /tmp/server.conf
```

> 🇬🇧 *Output extract*

Trích xuất output

```text
...
[5774] 2019/12/09 11:11:23.064276 [INF] Listening for leafnode connections on 0.0.0.0:7422
...
```

> 🇬🇧 *We create a replier on the server to listen for requests on 'q', which it will aptly respond with '42':*

Tạo một replier trên server để lắng nghe request trên subject 'q' và phản hồi bằng '42':

```bash
nats reply -s nats://appuser:s3cr3t@localhost q 42
```

> 🇬🇧 *The leaf node, allows local clients to connect to through port 4111, and doesn't require any kind of authentication. The configuration specifies where the remote cluster is located, and specifies how to connect to it (just a simple token in this case):*

Leaf node cho phép client cục bộ kết nối qua port 4111 và không yêu cầu xác thực. Config chỉ định vị trí remote cluster và cách kết nối (dùng token đơn giản trong trường hợp này):

```
listen: "127.0.0.1:4111"
leafnodes {
    remotes = [
        {
          url: "nats://leafuser:s3cr3t@localhost"
        },
    ]
}
```

> 🇬🇧 *In the case where the remote leaf connection is connecting with `tls`:*

Trong trường hợp remote leaf connection kết nối bằng `tls`:

```
listen: "127.0.0.1:4111"
leafnodes {
    remotes = [
        {
          url: "tls://leafuser:s3cr3t@localhost"
        },
    ]
}
```

> 🇬🇧 *Note the leaf node configuration lists a number of `remotes`. The `url` specifies the port on the server where leaf node connections are allowed.*

Lưu ý rằng config của leaf node liệt kê một số `remotes`. `url` chỉ định port trên server nơi các kết nối leaf node được cho phép.

> 🇬🇧 *Start the leaf node server:*

Khởi động leaf node server:

```bash
nats-server -c /tmp/leaf.conf
```

> 🇬🇧 *Output extract*

Trích xuất output

```text
....
[3704] 2019/12/09 09:55:31.548308 [INF] Listening for client connections on 127.0.0.1:4111
...
[3704] 2019/12/09 09:55:31.549404 [INF] Connected leafnode to "localhost"
```

> 🇬🇧 *Connect a client to the leaf server and make a request to 'q':*

Kết nối client đến leaf server và thực hiện request đến 'q':

```bash
nats req -s nats://127.0.0.1:4111 q ""
```

```text
Published [q] : ''
Received  [_INBOX.Ua82OJamRdWof5FBoiKaRm.gZhJP6RU] : '42'
```

## Ví Dụ Leaf Node Kết Nối Đến Global Service Từ Xa

> 🇬🇧 *In this example, we connect a leaf node to Synadia's [NGS](https://www.synadia.com/cloud). Leaf nodes are supported on free developer and paid accounts. To use NGS, ensure that you've signed up and have an account loaded on your local system. It takes less than 30 seconds to grab yourself a free account to follow along if you don't have one already!*

Trong ví dụ này, chúng ta kết nối leaf node đến [NGS](https://www.synadia.com/cloud) của Synadia. Leaf node được hỗ trợ trên cả tài khoản developer miễn phí lẫn tài khoản trả phí. Để sử dụng NGS, hãy đảm bảo bạn đã đăng ký và có tài khoản được nạp vào hệ thống cục bộ. Chỉ mất chưa đến 30 giây để tạo tài khoản miễn phí nếu bạn chưa có!

> 🇬🇧 *The `nsc` tool can operate with many accounts and operators, so it's essential to make sure you're working with the right operator and account. You can set the account using the `nsc` tool like below. The `DELETE_ME` account is used as an example, which is registered with NGS as a free account.*

Tool `nsc` có thể làm việc với nhiều tài khoản và operator, vì vậy cần đảm bảo bạn đang dùng đúng operator và account. Bạn có thể đặt tài khoản bằng tool `nsc` như dưới đây. Tài khoản `DELETE_ME` được dùng làm ví dụ — đây là tài khoản miễn phí đã đăng ký với NGS.

```bash
❯ nsc env -a DELETE_ME
❯ nsc describe account
+--------------------------------------------------------------------------------------+
|                                   Account Details                                    |
+---------------------------+----------------------------------------------------------+
| Name                      | DELETE_ME                                                |
| Account ID                | ABF3NX7FJLDCUO5QXBH56PV6EU4PR5HFCUJBXAG57AKSDUBTGORDFOLI |
| Issuer ID                 | ODSKBNDIT3LTZWFSRAWOBXSBZ7VZCDQVU6TBJX3TQGYXUWRU46ANJJS4 |
| Issued                    | 2023-03-02 18:18:42 UTC                                  |
| Expires                   |                                                          |
+---------------------------+----------------------------------------------------------+
| Max Connections           | 10                                                       |
| Max Leaf Node Connections | Not Allowed                                              |
| Max Data                  | 1.0 GB (1000000000 bytes)                                |
| Max Exports               | 2                                                        |
| Max Imports               | 7                                                        |
| Max Msg Payload           | 1.0 kB (1000 bytes)                                      |
| Max Subscriptions         | 10                                                       |
| Exports Allows Wildcards  | True                                                     |
| Disallow Bearer Token     | False                                                    |
| Response Permissions      | Not Set                                                  |
+---------------------------+----------------------------------------------------------+
| Jetstream                 | Disabled                                                 |
+---------------------------+----------------------------------------------------------+
| Exports                   | None                                                     |
+---------------------------+----------------------------------------------------------+
```

> 🇬🇧 *The `nsc` tool is aware of the account, so let's proceed to create a user for our example.*

Tool `nsc` đã biết về tài khoản này, hãy tiến hành tạo user cho ví dụ của chúng ta.

```bash
nsc add user leaftestuser
```

```text
[ OK ] generated and stored user key "UB5QBEU4LU7OR26JEYSG27HH265QVUFGXYVBRD7SVKQJMEFSZTGFU62F"
[ OK ] generated user creds file "~/.nkeys/creds/synadia/leaftest/leaftestuser.creds"
[ OK ] added user "leaftestuser" to account "leaftest"
```

> 🇬🇧 *Let's craft a leaf node connection much like we did earlier:*

Tạo cấu hình kết nối leaf node tương tự như trước:

```
leafnodes {
    remotes = [
        {
          url: "tls://connect.ngs.global"
          credentials: "/Users/alberto/.nkeys/creds/synadia/leaftest/leaftestuser.creds"
        },
    ]
}
```

> 🇬🇧 *The default port for leaf nodes is 7422, so we don't have to specify it.*

Port mặc định cho leaf node là 7422, nên không cần chỉ định thêm.

> 🇬🇧 *Let's start the leaf server:*

Khởi động leaf server:

```bash
nats-server -c /tmp/ngs_leaf.conf
```

```text
...
[4985] 2023/03/03 10:55:51.577569 [INF] Listening for client connections on 0.0.0.0:4222
...
[4985] 2023/03/03 10:55:51.918781 [INF] Connected leafnode to "connect.ngs.global"
```

> 🇬🇧 *Again, let's connect a replier, but this time to Synadia's NGS. NSC connects specifying the credentials file:*

Lần này kết nối một replier đến NGS của Synadia. NSC kết nối bằng cách chỉ định file credential (thông tin đăng nhập):

```bash
nsc reply q 42
```

> 🇬🇧 *And now let's make the request from the local host:*

Bây giờ thực hiện request từ host cục bộ:

```bash
nats-req q ""
```

```text
Published [q] : ''
Received  [_INBOX.hgG0zVcVcyr4G5KBwOuyJw.uUYkEyKr] : '42'
```

## Leaf Authorization

> 🇬🇧 *In some cases you may want to restrict what messages can be exported from the leaf node or imported from the leaf connection. You can specify restrictions by limiting what the leaf connection client can publish and subscribe to. See [NATS Authorization](../securing_nats/authorization.md) for how you can do this.*

Trong một số trường hợp, bạn có thể muốn giới hạn message nào được export ra khỏi leaf node hoặc import vào từ leaf connection. Bạn có thể đặt giới hạn bằng cách hạn chế những gì client của leaf connection được phép publish và subscribe. Xem [NATS Authorization](../securing_nats/authorization.md) để biết cách thực hiện.

## TLS-first Handshake

> 🇬🇧 *_As of NATS v2.10.0_*

_Từ NATS v2.10.0_

> 🇬🇧 *Leafnode connections follow the model where when a TCP connection is created to the server, the server will immediately send an [INFO protocol message](../../../reference/nats-protocol/nats-protocol#info) in clear text. This INFO protocol provides metadata, including whether the server requires a secure connection.*

Kết nối leafnode theo mô hình: khi TCP connection được tạo đến server, server sẽ ngay lập tức gửi một [INFO protocol message](../../../reference/nats-protocol/nats-protocol#info) dạng văn bản thuần. INFO protocol này cung cấp metadata, bao gồm thông tin về việc server có yêu cầu kết nối bảo mật hay không.

> 🇬🇧 *Some environments prefer not to want a server that is configured to accept TLS connections for leafnodes having any traffic sent in clear text. It was possible to by-pass this using a websocket connection. However, if websocket is not desired, the accepting and remote servers can be [configured](./leafnode_conf.md#tls-block) to perform a TLS handshake before sending the INFO protocol message.*

Một số môi trường không muốn có bất kỳ traffic nào gửi dạng văn bản thuần khi server được cấu hình chấp nhận kết nối TLS cho leafnode. Trước đây có thể bỏ qua điều này bằng WebSocket. Tuy nhiên, nếu không muốn dùng WebSocket, cả server chấp nhận lẫn remote server đều có thể được [cấu hình](./leafnode_conf.md#tls-block) để thực hiện TLS handshake trước khi gửi INFO protocol message.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **permission**: quyền truy cập
- **subject**: chuỗi định danh message (giống topic)
- **token**: chuỗi xác thực