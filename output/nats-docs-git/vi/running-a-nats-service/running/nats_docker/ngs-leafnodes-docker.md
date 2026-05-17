---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/running/nats_docker/ngs-leafnodes-docker
title: Chạy leaf node Synadia Cloud (NGS) trong Docker
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Chạy leaf node Synadia Cloud (NGS) trong Docker

> 🇬🇧 *This mini-tutorial shows how to run 2 NATS server in local Docker containers interconnected via [Synadia Cloud Platform](https://cloud.synadia.com?utm_source=nats_docs&utm_medium=nats). NGS is a global managed NATS network of NATS, and the local containers will connect to it as leaf nodes.*

Hướng dẫn này mô tả cách chạy 2 NATS server trong Docker container cục bộ, kết nối với nhau thông qua [Synadia Cloud Platform](https://cloud.synadia.com?utm_source=nats_docs&utm_medium=nats). NGS là mạng NATS toàn cầu được quản lý, và các container cục bộ sẽ kết nối vào đó dưới dạng leaf node (bên đăng ký nhận message từ mạng toàn cầu).

> 🇬🇧 *Start by creating a free account on [https://cloud.synadia.com/](https://cloud.synadia.com?utm_source=nats_docs&utm_medium=nats).*

Bắt đầu bằng cách tạo tài khoản miễn phí tại [https://cloud.synadia.com/](https://cloud.synadia.com?utm_source=nats_docs&utm_medium=nats).

> 🇬🇧 *Once you are logged in, go into the `default` account (you can manage multiple isolated NGS account within your Synadia Cloud account).*

Sau khi đăng nhập, truy cập vào account `default` (bạn có thể quản lý nhiều NGS account độc lập trong cùng một Synadia Cloud account).

> 🇬🇧 *In `Settings` > `Limits`, increase `Leaf Nodes` to 2. Save the configuration change. (Your free account comes with up to 2 leaf connection, but the account is configured to use at most 1 initially).*

Vào `Settings` > `Limits`, tăng `Leaf Nodes` lên 2 rồi lưu thay đổi config (bên đăng ký nhận message) lại.
(Tài khoản miễn phí hỗ trợ tối đa 2 kết nối leaf, nhưng mặc định chỉ cấu hình dùng 1.)

> 🇬🇧 *Now navigate to the `Users` section of your `default` account and create 2 users, `red` and `blue`. (Users are another way you can isolate parts of your systems customizing permissions, access to data, limits and more)*

Tiếp theo, vào mục `Users` trong account `default` và tạo 2 user: `red` và `blue`.
(User là cách để phân tách phạm vi hệ thống, cho phép tuỳ chỉnh permission (quyền truy cập), quyền truy cập dữ liệu, giới hạn và nhiều thứ khác.)

> 🇬🇧 *For each of the two users, select `Get Connected` and `Download Credentials`.*

Với mỗi user, chọn `Get Connected` và `Download Credentials`.

> 🇬🇧 *You should now have 2 files on your computer: `default-red.creds` and `default-blue.creds`.*

Lúc này bạn sẽ có 2 file credential (thông tin đăng nhập) trên máy: `default-red.creds` và `default-blue.creds`.

> 🇬🇧 *Create a minimal NATS Server configuration file `leafnode.conf`, it will work for both leaf nodes:*

Tạo file config NATS Server tối giản `leafnode.conf`, dùng chung cho cả hai leaf node:

```
leafnodes {
    remotes = [
        {
          url: "tls://connect.ngs.global"
          credentials: "ngs.creds"
        },
    ]
}
```

> 🇬🇧 *Let's start the first leafnode (for user `red`) with:*

Khởi động leaf node đầu tiên (cho user `red`) bằng lệnh:

```shell
docker run  -p 4222:4222 -v leafnode.conf:/leafnode.conf -v /etc/ssl/cert.pem:/etc/ssl/cert.pem -v default-red.creds:/ngs.creds  nats:latest -c /leafnode.conf
```

> 🇬🇧 *`-p 4222:4222` maps the server port 4222 inside the container to your local port 4222. `-v leafnode.conf:/leafnode.conf` mounts the configuration file created above at location `/leafnode.conf` in the container. `-v /etc/ssl/cert.pem:/etc/ssl/cert.pem` installs root certificates in the container, since the `nats` image does not bundle them, and they are required to verify the TLS certificate presented by NGS. `-v default-red.creds:/ngs.creds` installs the credentials for user `red` at location `/ngs.creds` inside the container. `-c /leafnode.conf` are arguments passed to the container entry point (`nats-server`).*

`-p 4222:4222` ánh xạ port 4222 bên trong container ra port 4222 trên máy cục bộ.
`-v leafnode.conf:/leafnode.conf` mount file config tạo ở trên vào vị trí `/leafnode.conf` trong container.
`-v /etc/ssl/cert.pem:/etc/ssl/cert.pem` cài root certificate vào container, vì image `nats` không đi kèm sẵn và cần dùng để xác thực TLS certificate của NGS.
`-v default-red.creds:/ngs.creds` cài credential của user `red` vào vị trí `/ngs.creds` trong container.
`-c /leafnode.conf` là các tham số truyền vào entry point của container (`nats-server`).

> 🇬🇧 *Launching the container, you should see the NATS server starting successfully:*

Khởi chạy container, bạn sẽ thấy NATS server khởi động thành công:

```
[1] 2024/06/14 18:03:51.810719 [INF] Server is ready
[1] 2024/06/14 18:03:52.075951 [INF] 34.159.142.0:7422 - lid:5 - Leafnode connection created for account: $G
[1] 2024/06/14 18:03:52.331354 [INF] 34.159.142.0:7422 - lid:5 - JetStream using domains: local "", remote "ngs"
```

> 🇬🇧 *Now start the second leaf nodes with two minor tweaks to the command:*

Tiếp theo, khởi động leaf node thứ hai với hai thay đổi nhỏ trong lệnh:

```
docker run  -p 4333:4222 -v leafnode.conf:/leafnode.conf -v /etc/ssl/cert.pem:/etc/ssl/cert.pem -v default-blue.creds:/ngs.creds  nats:latest -c /leafnode.conf
```

> 🇬🇧 *Notice we bind to local port `4333` (since `4222`) is busy, and we mount `blue` credentials.*

Lưu ý: ta bind vào port cục bộ `4333` (vì `4222` đã bận), và mount credential `blue`.

> 🇬🇧 *Congratulations, you have 2 leaf nodes connected to the NGS global network. Despite this being a global shared environment, your account is completely isolated from the rest of the traffic, and vice versa.*

Chúc mừng, bạn đã có 2 leaf node kết nối vào mạng NGS toàn cầu. Dù đây là môi trường dùng chung toàn cầu, account của bạn hoàn toàn cách ly với phần còn lại của traffic, và ngược lại.

> 🇬🇧 *Now let's make 2 clients connected to the 2 leaf nodes talk to each other.*

Bây giờ hãy để 2 client kết nối vào 2 leaf node giao tiếp với nhau.

> 🇬🇧 *Let us start a simple service on the Leafnode of user `red`:*

Khởi động một service đơn giản trên leaf node của user `red`:

```shell
nats -s localhost:4222 reply docker-leaf-test "At {{Time}}, I received your request: {{Request}}"
```

> 🇬🇧 *Using the LeafNode run by user `blue`, let's send a request:*

Dùng leaf node của user `blue` để gửi một request:

```shell
$ nats -s localhost:4333 request docker-leaf-test "Hello World"

At 8:15PM, I received your request: Hello World
```

> 🇬🇧 *Congratulations, you just connected 2 Leaf nodes to the global NGS network and used them to send a request and receive a response.*

Chúc mừng, bạn vừa kết nối 2 leaf node vào mạng NGS toàn cầu và dùng chúng để gửi request và nhận response.

> 🇬🇧 *Your messages were routed transparently with millions of others, but they were not visible to anyone outside of your Synadia Cloud account.*

Message của bạn được định tuyến trong suốt cùng hàng triệu message khác, nhưng không ai ngoài Synadia Cloud account của bạn có thể nhìn thấy chúng.

### Tài liệu liên quan và hữu ích

 * Official [Docker image for the NATS server on GitHub](https://github.com/nats-io/nats-docker) và [issues](https://github.com/nats-io/nats-docker/issues)
 * [`nats` images on DockerHub](https://hub.docker.com/_/nats)
 * [`nats` CLI tool](/using-nats/nats-tools/nats\_cli/) và [`nats bench`](/using-nats/nats-tools/nats\_cli/natsbench)
 * [Cấu hình Leaf Nodes](../../configuration/leafnodes)

## Thuật ngữ trong bài

- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **permission**: quyền truy cập
- **request**: yêu cầu
- **response**: phản hồi
- **service**: dịch vụ
- **TLS**: mã hóa TLS