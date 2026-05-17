---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/running/nats_docker/docker_swarm
title: Docker Swarm
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Docker Swarm

### Bước 1:

> 🇬🇧 *Create an overlay network for the cluster (in this example, `nats-cluster-example`), and instantiate an initial NATS server.*

Tạo một overlay network cho cluster (cụm nhiều server chạy chung) (trong ví dụ này là `nats-cluster-example`), sau đó khởi tạo NATS server ban đầu.

> 🇬🇧 *First create an overlay network:*

Trước tiên, tạo overlay network:

```bash
docker network create --driver overlay nats-cluster-example
```

> 🇬🇧 *Next instantiate an initial "seed" server for a NATS cluster listening for other servers to join route to it on port 6222:*

Tiếp theo, khởi tạo server "seed" ban đầu cho một NATS cluster — server này lắng nghe các server khác kết nối vào qua port 6222:

```bash
docker service create --network nats-cluster-example --name nats-cluster-node-1 nats:1.0.0 -cluster nats://0.0.0.0:6222 -DV
```

### Bước 2:

> 🇬🇧 *The 2nd step is to create another service which connects to the NATS server within the overlay network. Note that we connect to to the server at `nats-cluster-node-1`:*

Bước 2 là tạo thêm một service kết nối đến NATS server trong overlay network. Lưu ý rằng chúng ta kết nối đến server tại `nats-cluster-node-1`:

```bash
docker service create --name ruby-nats --network nats-cluster-example wallyqs/ruby-nats:ruby-2.3.1-nats-v0.8.0 -e '
  NATS.on_error do |e|
    puts "ERROR: #{e}"
  end
  NATS.start(:servers => ["nats://nats-cluster-node-1:4222"]) do |nc|
    inbox = NATS.create_inbox
    puts "[#{Time.now}] Connected to NATS at #{nc.connected_server}, inbox: #{inbox}"

    nc.subscribe(inbox) do |msg, reply|
      puts "[#{Time.now}] Received reply - #{msg}"
    end

    nc.subscribe("hello") do |msg, reply|
      next if reply == inbox
      puts "[#{Time.now}] Received greeting - #{msg} - #{reply}"
      nc.publish(reply, "world")
    end

    EM.add_periodic_timer(1) do
      puts "[#{Time.now}] Saying hi (servers in pool: #{nc.server_pool}"
      nc.publish("hello", "hi", inbox)
    end
  end'
```

### Bước 3:

> 🇬🇧 *Now you can add more nodes to the Swarm cluster via more docker services, referencing the seed server in the `-routes` parameter:*

Lúc này có thể thêm nhiều node (một server trong cluster) vào Swarm cluster bằng cách thêm các docker service, tham chiếu đến seed server qua tham số `-routes`:

```bash
docker service create --network nats-cluster-example --name nats-cluster-node-2 nats:1.0.0 -cluster nats://0.0.0.0:6222 -routes nats://nats-cluster-node-1:6222 -DV
```

> 🇬🇧 *In this case, `nats-cluster-node-1` is seeding the rest of the cluster through the autodiscovery feature. Now NATS servers `nats-cluster-node-1` and `nats-cluster-node-2` are clustered together.*

Ở đây, `nats-cluster-node-1` đóng vai trò seed cho phần còn lại của cluster thông qua tính năng autodiscovery. Lúc này NATS server `nats-cluster-node-1` và `nats-cluster-node-2` đã được cluster lại với nhau.

> 🇬🇧 *Add in more replicas of the subscriber:*

Thêm nhiều replica của subscriber (bên đăng ký nhận message):

```bash
docker service scale ruby-nats=3
```

> 🇬🇧 *Then confirm the distribution on the Docker Swarm cluster:*

Sau đó xác nhận cách phân phối trên Docker Swarm cluster:

```bash
docker service ps ruby-nats
```
```text
ID                         NAME         IMAGE                                     NODE    DESIRED STATE  CURRENT STATE          ERROR
25skxso8honyhuznu15e4989m  ruby-nats.1  wallyqs/ruby-nats:ruby-2.3.1-nats-v0.8.0  node-1  Running        Running 2 minutes ago  
0017lut0u3wj153yvp0uxr8yo  ruby-nats.2  wallyqs/ruby-nats:ruby-2.3.1-nats-v0.8.0  node-1  Running        Running 2 minutes ago  
2sxl8rw6vm99x622efbdmkb96  ruby-nats.3  wallyqs/ruby-nats:ruby-2.3.1-nats-v0.8.0  node-2  Running        Running 2 minutes ago
```

> 🇬🇧 *The sample output after adding more NATS server nodes to the cluster, is below - and notice that the client is _dynamically_ aware of more nodes being part of the cluster via auto discovery!*

Ví dụ output sau khi thêm nhiều NATS server node vào cluster — lưu ý rằng client _tự động_ nhận biết các node mới gia nhập cluster nhờ tính năng auto discovery!

```text
[2016-08-15 12:51:52 +0000] Saying hi (servers in pool: [{:uri=>#<URI::Generic nats://10.0.1.3:4222>, :was_connected=>true, :reconnect_attempts=>0}]
[2016-08-15 12:51:53 +0000] Saying hi (servers in pool: [{:uri=>#<URI::Generic nats://10.0.1.3:4222>, :was_connected=>true, :reconnect_attempts=>0}]
[2016-08-15 12:51:54 +0000] Saying hi (servers in pool: [{:uri=>#<URI::Generic nats://10.0.1.3:4222>, :was_connected=>true, :reconnect_attempts=>0}]
[2016-08-15 12:51:55 +0000] Saying hi (servers in pool: [{:uri=>#<URI::Generic nats://10.0.1.3:4222>, :was_connected=>true, :reconnect_attempts=>0}, {:uri=>#<URI::Generic nats://10.0.1.7:4222>, :reconnect_attempts=>0}, {:uri=>#<URI::Generic nats://10.0.1.6:4222>, :reconnect_attempts=>0}]
```

> 🇬🇧 *Sample output after adding more workers which can reply back (since ignoring own responses):*

Ví dụ output sau khi thêm nhiều worker có khả năng phản hồi (do bỏ qua response của chính mình):

```text
[2016-08-15 16:06:26 +0000] Received reply - world
[2016-08-15 16:06:26 +0000] Received reply - world
[2016-08-15 16:06:27 +0000] Received greeting - hi - _INBOX.b8d8c01753d78e562e4dc561f1
[2016-08-15 16:06:27 +0000] Received greeting - hi - _INBOX.4c35d18701979f8c8ed7e5f6ea
```

## Và tiếp tục...

> 🇬🇧 *From here you can experiment adding to the NATS cluster by simply adding servers with new service names, that route to the seed server `nats-cluster-node-1`. As you've seen above, clients will automatically be updated to know that new servers are available in the cluster.*

Từ đây bạn có thể thử nghiệm mở rộng NATS cluster bằng cách thêm server với tên service mới, định tuyến về seed server `nats-cluster-node-1`. Như đã thấy ở trên, client sẽ tự động được cập nhật để biết rằng có thêm server mới trong cluster.

```bash
docker service create --network nats-cluster-example --name nats-cluster-node-3 nats:1.0.0 -cluster nats://0.0.0.0:6222 -routes nats://nats-cluster-node-1:6222 -DV
```

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **node**: một server trong cluster
- **replica**: bản sao dữ liệu
- **service**: dịch vụ
- **subscriber**: bên đăng ký nhận message