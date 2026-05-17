---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/jetstream-config/configuration_mgmt/kubernetes_controller
title: Kubernetes Controller
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Kubernetes Controller

> 🇬🇧 *The JetStream controllers allow you to manage NATS JetStream Streams and Consumers via K8S CRDs. You can find more info on how to deploy and usage [here](https://github.com/nats-io/nack#getting-started). Below you can find an example of how to create a stream and a couple of consumers:*

JetStream controller cho phép quản lý NATS JetStream Stream (luồng message lưu trữ liên tục) và Consumer (bên xử lý dữ liệu từ stream) thông qua K8S CRDs. Xem thêm hướng dẫn deploy và cách sử dụng [tại đây](https://github.com/nats-io/nack#getting-started). Dưới đây là ví dụ tạo một stream và một vài consumer:

```yaml
---
apiVersion: jetstream.nats.io/v1beta1
kind: Stream
metadata:
  name: mystream
spec:
  name: mystream
  subjects: ["orders.*"]
  storage: memory
  maxAge: 1h
---
apiVersion: jetstream.nats.io/v1beta1
kind: Consumer
metadata:
  name: my-push-consumer
spec:
  streamName: mystream
  durableName: my-push-consumer
  deliverSubject: my-push-consumer.orders
  deliverPolicy: last
  ackPolicy: none
  replayPolicy: instant
---
apiVersion: jetstream.nats.io/v1beta1
kind: Consumer
metadata:
  name: my-pull-consumer
spec:
  streamName: mystream
  durableName: my-pull-consumer
  deliverPolicy: all
  filterSubject: orders.received
  maxDeliver: 20
  ackPolicy: explicit
```

> 🇬🇧 *Once the CRDs are installed you can use `kubectl` to manage the streams and consumers as follows:*

Sau khi cài đặt CRDs, dùng `kubectl` để quản lý stream và consumer như sau:

```bash
$ kubectl get streams
NAME       STATE     STREAM NAME   SUBJECTS
mystream   Created   mystream      [orders.*]

$ kubectl get consumers
NAME               STATE     STREAM     CONSUMER           ACK POLICY
my-pull-consumer   Created   mystream   my-pull-consumer   explicit
my-push-consumer   Created   mystream   my-push-consumer   none

# If you end up in an Errored state, run kubectl describe for more info.
#     kubectl describe streams mystream
#     kubectl describe consumers my-pull-consumer
```

## Thuật ngữ trong bài

- **consumer**: bên xử lý dữ liệu từ stream
- **deploy**: triển khai
- **stream**: luồng message lưu trữ liên tục