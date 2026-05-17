---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats-on-kubernetes/nats-kubernetes
title: Giới thiệu
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Giới thiệu

> 🇬🇧 *The recommended way to deploy NATS on Kubernetes is using [Helm](https://helm.sh/) with the official NATS Helm Chart.*

Cách được khuyến nghị để deploy NATS trên Kubernetes là dùng [Helm](https://helm.sh/) với NATS Helm Chart chính thức.

## Helm repo

> 🇬🇧 *To register the NATS Helm chart run:*

Để đăng ký NATS Helm chart, chạy lệnh sau:

```sh
helm repo add nats https://nats-io.github.io/k8s/helm/charts/
```

## Config values

> 🇬🇧 *The default configuration values of the chart will deploy a single NATS server as a `StatefulSet` and a single replica [nats-box](https://github.com/nats-io/nats-box) `Deployment`.*

Cấu hình mặc định của chart sẽ deploy một NATS server dưới dạng `StatefulSet` và một replica (bản sao dữ liệu) [nats-box](https://github.com/nats-io/nats-box) `Deployment`.

> 🇬🇧 *The [ArtifactHub page](https://artifacthub.io/packages/helm/nats/nats) provides the list of Helm configuration values and examples for the current release.*

[Trang ArtifactHub](https://artifacthub.io/packages/helm/nats/nats) cung cấp danh sách các giá trị config và ví dụ cho phiên bản hiện tại.

> 🇬🇧 *For tracking the development version, refer to the [source repo](https://github.com/nats-io/k8s/tree/main/helm/charts/nats#nats-server).*

_Để theo dõi phiên bản development, tham khảo [source repo](https://github.com/nats-io/k8s/tree/main/helm/charts/nats#nats-server)._

> 🇬🇧 *Once the desired configuration is created, install the chart:*

Sau khi tạo xong cấu hình mong muốn, cài đặt chart:

```sh
helm install nats nats/nats
```

## Validate connectivity

> 🇬🇧 *Once the pods are up, validate by accessing the `nats-box` container and running a CLI command.*

Sau khi các pod (pod Kubernetes) khởi động, kiểm tra kết nối bằng cách truy cập container (container đóng gói app) `nats-box` và chạy lệnh CLI.

```sh
kubectl exec -it deployment/nats-box -- nats pub test hi
```

> 🇬🇧 *The output should indicate a successful publish to NATS.*

Kết quả đầu ra cho thấy đã publish thành công lên NATS.

```
16:17:00 Published 2 bytes to "test"
```

## Commercial Options

> 🇬🇧 *Synadia offers [Deploy for Kubernetes](https://www.synadia.com/deploy-for-kubernetes/), a self-service, bring-your-own Kubernetes deployment option that includes NATS and additional components.*

Synadia cung cấp [Deploy for Kubernetes](https://www.synadia.com/deploy-for-kubernetes/) — tùy chọn deployment (triển khai) tự quản lý trên Kubernetes của riêng bạn, bao gồm NATS và các thành phần bổ sung.

## Thuật ngữ trong bài

- **container**: container (đóng gói app)
- **deploy**: triển khai
- **deployment**: triển khai (Kubernetes)
- **pod**: pod Kubernetes
- **replica**: bản sao dữ liệu