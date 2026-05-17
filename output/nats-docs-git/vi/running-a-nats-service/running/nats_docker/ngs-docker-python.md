---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/running/nats_docker/ngs-docker-python
title: Python và NGS chạy trong Docker
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Python và NGS chạy trong Docker

> 🇬🇧 *Start a lightweight Docker container:*

Khởi động một Docker container nhẹ:

```shell
docker run --entrypoint /bin/bash -it python:3.8-slim-buster
```

> 🇬🇧 *Or you can also mount local creds via a volume:*

Hoặc bạn cũng có thể mount credential (thông tin đăng nhập) local vào container qua một volume:

```shell
docker run --entrypoint /bin/bash -v $HOME/.nkeys/creds/synadia/NGS/:/creds -it python:3.8-slim-buster
```

> 🇬🇧 *Install nats.py and dependencies to install nkeys:*

Cài đặt nats.py và các dependency để cài nkeys:

```shell
apt-get update && apt-get install -y build-essential curl
pip install asyncio-nats-client[nkeys]
```

> 🇬🇧 *Get the Python examples using curl:*

Tải các ví dụ Python bằng curl:

```shell
curl -o nats-pub.py -O -L https://raw.githubusercontent.com/nats-io/nats.py/master/examples/nats-pub/__main__.py
curl -o nats-sub.py -O -L https://raw.githubusercontent.com/nats-io/nats.py/master/examples/nats-sub/__main__.py
```

> 🇬🇧 *Create a subscription that lingers:*

Tạo một subscription (bên đăng ký nhận message) chạy liên tục:

```shell
python nats-sub.py --creds /creds/NGS.creds  -s tls://connect.ngs.global:4222 hello &
```

> 🇬🇧 *Publish a message:*

Publish (gửi) một message:

```shell
python nats-pub.py --creds /creds/NGS.creds  -s tls://connect.ngs.global:4222 hello -d world
```

## Thuật ngữ trong bài

- **credential**: thông tin đăng nhập
- **message**: gói dữ liệu được gửi đi
- **subscriber**: bên đăng ký nhận message