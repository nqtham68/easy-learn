---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/running/nats_docker/nats-docker-tutorial
title: Hướng dẫn thực hành NATS Docker
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Hướng dẫn thực hành NATS Docker

> 🇬🇧 *In this tutorial you run the [NATS server Docker image](https://hub.docker.com/_/nats/). The Docker image provides an instance of the NATS Server. Synadia actively maintains and supports the nats-server Docker image. The NATS image is only 6 MB in size.*

Trong hướng dẫn này, bạn sẽ chạy [NATS server Docker image](https://hub.docker.com/_/nats/). Docker image cung cấp một instance của NATS server (máy chủ). Synadia chủ động duy trì và hỗ trợ nats-server Docker image. Image NATS chỉ có kích thước 6 MB.

**1. Set up Docker.**

> 🇬🇧 *See [Get Started with Docker](http://docs.docker.com/mac/started/) for guidance.*

Xem [Get Started with Docker](http://docs.docker.com/mac/started/) để được hướng dẫn.

> 🇬🇧 *The easiest way to run Docker is to use the [Docker Toolbox](http://docs.docker.com/mac/step_one/).*

Cách đơn giản nhất để chạy Docker là dùng [Docker Toolbox](http://docs.docker.com/mac/step_one/).

**2. Run the nats-server Docker image.**

```bash
docker run -p 4222:4222 -p 8222:8222 -p 6222:6222 --name nats-server -ti nats:latest
```

**3. Verify that the NATS server is running.**

> 🇬🇧 *You should see the following:*

Bạn sẽ thấy kết quả sau:

```text
Unable to find image 'nats:latest' locally
latest: Pulling from library/nats
2d3d00b0941f: Pull complete 
24bc6bd33ea7: Pull complete 
Digest: sha256:47b825feb34e545317c4ad122bd1a752a3172bbbc72104fc7fb5e57cf90f79e4
Status: Downloaded newer image for nats:latest
```

> 🇬🇧 *Followed by this, indicating that the NATS server is running:*

Tiếp theo là dòng xác nhận NATS server đang chạy:

```text
[1] 2019/06/01 18:34:19.605144 [INF] Starting nats-server version 2.0.0
[1] 2019/06/01 18:34:19.605191 [INF] Starting http monitor on 0.0.0.0:8222
[1] 2019/06/01 18:34:19.605286 [INF] Listening for client connections on 0.0.0.0:4222
[1] 2019/06/01 18:34:19.605312 [INF] Server is ready
[1] 2019/06/01 18:34:19.608756 [INF] Listening for route connections on 0.0.0.0:6222
```

> 🇬🇧 *Notice how quickly the NATS server Docker image downloads. It is a mere 6 MB in size.*

Hãy chú ý tốc độ tải xuống Docker image rất nhanh — dung lượng chỉ vỏn vẹn 6 MB.

**4. Test the NATS server to verify it is running.**

> 🇬🇧 *An easy way to test the client connection port (cổng kết nối) is through using telnet.*

Cách đơn giản để kiểm tra port (cổng kết nối) kết nối client là dùng telnet.

```bash
telnet localhost 4222
```

> 🇬🇧 *Expected result:*

Kết quả mong đợi:

```text
Trying ::1...
Connected to localhost.
Escape character is '^]'.
INFO {"server_id":"NDP7NP2P2KADDDUUBUDG6VSSWKCW4IC5BQHAYVMLVAJEGZITE5XP7O5J","version":"2.0.0","proto":1,"go":"go1.11.10","host":"0.0.0.0","port":4222,"max_payload":1048576,"client_id":13249}
```

> 🇬🇧 *You can also test the monitoring endpoint, viewing `http://localhost:8222` with a browser.*

Bạn cũng có thể kiểm tra monitoring endpoint (địa chỉ API cụ thể), xem `http://localhost:8222` bằng trình duyệt.

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **endpoint**: địa chỉ API cụ thể
- **port**: cổng kết nối
- **server**: máy chủ