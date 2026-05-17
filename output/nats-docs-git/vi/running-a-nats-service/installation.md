---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/installation
title: Cài đặt NATS Server
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Cài đặt NATS Server

> 🇬🇧 *NATS philosophy is simplicity. Installation is just decompressing a zip file and copying the binary to an appropriate directory; you can also use your favorite package manager. Here's a list of different ways you can install or run NATS:*

Triết lý của NATS là sự đơn giản. Để cài đặt, chỉ cần giải nén file zip và copy binary vào thư mục phù hợp; hoặc dùng package manager tùy thích. Dưới đây là các cách cài đặt hoặc chạy NATS:

* [Command Line](./installation.md#getting-the-binary-from-the-command-line)
* [Docker](./installation.md#installing-via-docker)
* [Kubernetes](./nats-on-kubernetes/nats-kubernetes.md)
* [Package Manager](./installation.md#installing-via-a-package-manager)
* [Release Zip](./installation.md#downloading-a-release-build)
* [Development Build](./installation.md#installing-from-the-source)

Xem thêm [cài đặt NATS client](./clients.md#installing-the-nats-cli-tool)

## Hệ điều hành và kiến trúc được hỗ trợ

> 🇬🇧 *The following table indicates the current supported NATS server build combinations for operating systems and architectures.*

Bảng dưới đây liệt kê các kết hợp hệ điều hành và kiến trúc mà NATS server hiện hỗ trợ.

| Operating System | Architectures                                  | Status       |
| ---------------- | ---------------------------------------------- | ------------ |
| Darwin (macOS)   | amd64, arm64                                   | Stable       |
| Linux            | amd64, 386, arm6, arm7, arm64, mips64le, s390x | Stable       |
| Windows          | amd64, 386, arm6, arm7, arm64                  | Stable       |
| FreeBSD          | amd64                                          | Stable       |
| NetBSD           | -                                              | Experimental |
| IBM z/OS         | -                                              | Experimental |

_Lưu ý: không phải tất cả các phương thức cài đặt đều có bản phân phối cho mọi tổ hợp OS và kiến trúc._

## Yêu cầu phần cứng

> 🇬🇧 *The NATS server itself has minimal hardware requirements to support small edge devices, but can take advantage of more resources if available.*

NATS server có yêu cầu phần cứng tối thiểu rất thấp, phù hợp ngay cả với các thiết bị edge nhỏ, nhưng cũng có thể tận dụng tài nguyên lớn hơn nếu có.

> 🇬🇧 *CPU should be considered in accepting TLS connections. After a network partition, every disconnected client will attempt to connect to a NATS server in the cluster simultaneously, so CPU on those servers will momentarily spike. When there are many clients this can be mitigated with reconnect jitter settings, and errors can be reduced with longer TLS timeouts, and scaling up cluster sizes.*

CPU cần được cân nhắc khi xử lý kết nối TLS (mã hóa TLS). Sau khi xảy ra network partition, tất cả client bị ngắt kết nối sẽ đồng loạt kết nối lại vào cluster (cụm nhiều server chạy chung), khiến CPU tăng đột biến trong thời gian ngắn. Với số lượng client lớn, có thể giảm thiểu tình trạng này bằng cài đặt reconnect jitter, đồng thời tăng TLS timeout và mở rộng kích thước cluster để giảm lỗi.

> 🇬🇧 *We highly recommend testing to see if smaller, cheaper machines suffice for your workload - often they do! We suggest starting here and adjusting resources after load testing specific to your environment. When using cloud provider instance types make sure the node has a sufficient NIC to support the required bandwidth for the application needs.*

Chúng tôi khuyến nghị chạy thử nghiệm để xem liệu máy nhỏ hơn, rẻ hơn có đủ dùng cho workload của bạn không — thường là có! Hãy bắt đầu từ cấu hình nhỏ và điều chỉnh sau khi load test theo môi trường thực tế. Khi dùng instance type của cloud provider, hãy đảm bảo node (một server trong cluster) có NIC đủ băng thông cho nhu cầu ứng dụng.

> 🇬🇧 *For high throughput use cases, the network interface card (NIC) or the available bandwidth are often the bottleneck, so ensure the hardware or cloud provider instance types are sufficient for your needs.*

Với các trường hợp cần throughput cao, NIC hoặc băng thông thường là điểm nghẽn — hãy đảm bảo phần cứng hoặc instance type của cloud provider đáp ứng đủ nhu cầu.

### Core NATS

> 🇬🇧 *The tables below outline the **minimum number of cores and memory** for stable cluster performance with different combinations of publishers, subscribers, and message rates. Stability is defined as the system avoiding slowdowns or running out of memory. These tests were conducted inside containers with `GOMEMLIMIT` set to 90% of the memory allocation, utilizing a 2021-era CPU and SSD for JetStream storage. Note that these are **minimum configurations**, and actual production environments may require additional resources.*

Các bảng dưới đây mô tả **số core và bộ nhớ tối thiểu** để cluster hoạt động ổn định với các tổ hợp publisher, subscriber và tốc độ message khác nhau. Ổn định được định nghĩa là hệ thống không bị chậm hoặc hết bộ nhớ. Các bài kiểm tra được thực hiện trong container với `GOMEMLIMIT` đặt ở 90% dung lượng bộ nhớ cấp phát, sử dụng CPU và SSD thế hệ 2021 cho JetStream storage. Lưu ý đây là **cấu hình tối thiểu** — môi trường production thực tế có thể cần thêm tài nguyên.

| Cluster Size | CPU cores | Memory | Subscribers | Publishers | Publish Rate msg/s | Total Message Rate msg/s|
| -----------: | --------: | -----: | ----------: | ---------: | -----------------: | ----------------------: |
|            1 |         1 | 32 MiB |           1 |        100 |               1000 |                 100,000 |
|            1 |         1 | 64 MiB |           1 |       1000 |                100 |                 100,000 |
|            3 |         1 | 32 MiB |           1 |       1000 |                100 |                 100,000 |
|            3 |         1 | 64 MiB |           1 |       1000 |                100 |                 100,000 |

### Với JetStream

> 🇬🇧 *This table follows the same pattern, with published messages received by a stream using file storage. For a cluster size of three, the stream uses three replicas. Subscribers rely on a "pull consumer" for fetching messages.*

Bảng này theo cùng cấu trúc, nhưng message được nhận vào một stream (luồng message lưu trữ liên tục) dùng file storage. Với cluster 3 node, stream sử dụng 3 replica (bản sao dữ liệu). Subscriber dùng "pull consumer" để lấy message.

| Cluster Size | CPU cores |  Memory | Subscribers | Publishers | Publish Rate msg/s | Total Message Rate msg/s |
| -----------: | --------: | ------: | ----------: | ---------: | -----------------: | -----------------------: |
|            1 |         1 |  32 MiB |           1 |         10 |                100 |                    1,000 |
|            1 |         1 |  32 MiB |           1 |        100 |                 10 |                    1,000 |
|            1 |         1 |  64 MiB |           1 |        100 |                100 |                   10,000 |
|            1 |         1 |  64 MiB |           1 |       1000 |                 10 |                   10,000 |
|            3 |         1 |  32 MiB |           1 |        100 |                 10 |                    1,000 |
|            3 |         1 |  64 MiB |           1 |        100 |                100 |                   10,000 |
|            3 |         1 |  64 MiB |           1 |       1000 |                 10 |                   10,000 |
|            3 |         1 | 256 MiB |           1 |       1000 |                100 |                  100,000 |

> 🇬🇧 *For **production deployment** of JetStream, we recommend starting with **at least 4 CPU cores and 8 GiB of memory** to reduce the risk of resource-related issues.*

Đối với **production deployment** của JetStream, chúng tôi khuyến nghị bắt đầu với **ít nhất 4 CPU core và 8 GiB bộ nhớ** để giảm nguy cơ gặp sự cố tài nguyên.

> 🇬🇧 *For recommendations on configuring limits in Kubernetes, see: <a href="https://github.com/nats-io/k8s/tree/main/helm/charts/nats#nats-container-resources*">https://github.com/nats-io/k8s/tree/main/helm/charts/nats#nats-container-resources*</a>

Để biết khuyến nghị cấu hình giới hạn tài nguyên trong Kubernetes, xem: <a href="https://github.com/nats-io/k8s/tree/main/helm/charts/nats#nats-container-resources">https://github.com/nats-io/k8s/tree/main/helm/charts/nats#nats-container-resources</a>

## Tải binary từ command line

> 🇬🇧 *The simplest way to get the `nats-server` binary for your machine is to use the following shell command.*

Cách đơn giản nhất để tải binary `nats-server` về máy là dùng lệnh shell sau.

> 🇬🇧 *For example, to get the binary for version 2.11.6:*

Ví dụ, để tải binary phiên bản 2.11.6:

```shell
curl -fsSL https://binaries.nats.dev/nats-io/nats-server/v2@v2.11.6 | sh
```

> 🇬🇧 *To get the latest released version, use `@latest`. You can also use `@main` to get the tip, or use a tag, specific branch, or commit hash after the `@`.*

Để lấy phiên bản release mới nhất, dùng `@latest`. Có thể dùng `@main` để lấy bản tip, hoặc chỉ định tag, branch cụ thể hay commit hash sau `@`.

## Cài đặt qua Docker

> 🇬🇧 *With Docker, you can install the server easily without scattering binaries and other artifacts on your system. The only pre-requisite is to [install docker](https://docs.docker.com/install).*

Docker cho phép cài đặt server dễ dàng mà không để lại binary hay artifact rải rác trên hệ thống. Yêu cầu duy nhất là [cài đặt Docker](https://docs.docker.com/install).

```shell
docker pull nats:latest
```

> 🇬🇧 *To run NATS on Docker:*

Để chạy NATS trên Docker:

```shell
docker run -p 4222:4222 -ti nats:latest
```

```
[1] 2019/05/24 15:42:58.228063 [INF] Starting nats-server version #.#.#
[1] 2019/05/24 15:42:58.228115 [INF] Git commit [#######]
[1] 2019/05/24 15:42:58.228201 [INF] Starting http monitor on 0.0.0.0:8222
[1] 2019/05/24 15:42:58.228740 [INF] Listening for client connections on 0.0.0.0:4222
[1] 2019/05/24 15:42:58.228765 [INF] Server is ready
```

> 🇬🇧 *More information on [containerized NATS is available here](./running/nats_docker).*

Thông tin thêm về [NATS chạy trong container có tại đây](./running/nats_docker).

## Cài đặt qua Package Manager

> 🇬🇧 *On Windows, using [scoop.sh](https://scoop.sh):*

Trên Windows, dùng [scoop.sh](https://scoop.sh):

```shell
scoop install main/nats-server
```

> 🇬🇧 *On Mac OS:*

Trên Mac OS:

```shell
brew install nats-server
```

> 🇬🇧 *Arch Linux: For Arch users, there is an [AUR package](https://aur.archlinux.org/packages/nats-server) that you can install with:*

Arch Linux: Người dùng Arch có thể cài qua [AUR package](https://aur.archlinux.org/packages/nats-server):

```shell
yay -S nats-server
```

> 🇬🇧 *To test your installation (provided the executable is visible to your shell): Typing `nats-server` should output something like*

Để kiểm tra cài đặt (với điều kiện executable đã nằm trong PATH của shell): gõ `nats-server` sẽ cho kết quả tương tự như sau:

```
[41634] 2019/05/13 09:42:11.745919 [INF] Starting nats-server version 2.*.*
[41634] 2019/05/13 09:42:11.746240 [INF] Listening for client connections on 0.0.0.0:4222
...
[41634] 2019/05/13 09:42:11.746249 [INF] Server id is NBNYNR4ZNTH4N2UQKSAAKBAFLDV3PZO4OUYONSUIQASTQT7BT4ZF6WX7
[41634] 2019/05/13 09:42:11.746252 [INF] Server is ready
```

## Tải Release Build

> 🇬🇧 *You can find the latest release of nats-server on [the nats-io/nats-server GitHub releases page](https://github.com/nats-io/nats-server/releases/).*

Tìm bản release mới nhất của nats-server tại [trang GitHub releases của nats-io/nats-server](https://github.com/nats-io/nats-server/releases/).

> 🇬🇧 *From the releases page, copy the link to the release archive file of your choice and download it using `curl -L`.*

Từ trang releases, copy link đến file archive phù hợp và tải xuống bằng `curl -L`.

> 🇬🇧 *For example, assuming version X.Y.Z of the server and a Linux AMD64:*

Ví dụ với server phiên bản X.Y.Z trên Linux AMD64:

```shell
curl -L https://github.com/nats-io/nats-server/releases/download/vX.Y.Z/nats-server-vX.Y.Z-linux-amd64.tar.gz -o nats-server.tar.gz
```

```shell
tar -xvzf nats-server.tar.gz
```

```shell
Archive:  nats-server.zip
   creating: nats-server-vX.Y.Z-linux-amd64/
...
```

> 🇬🇧 *and finally:*

và cuối cùng:

```shell
sudo cp nats-server-vX.Y.Z-linux-amd64/nats-server /usr/bin
```

## Cài đặt từ Source

> 🇬🇧 *If you have [Go installed](https://go.dev/doc/install), installing the binary is easy:*

Nếu đã [cài Go](https://go.dev/doc/install), cài đặt binary rất đơn giản:

```shell
go install github.com/nats-io/nats-server/v2@main
```

> 🇬🇧 *This mechanism will install a build of the [main](https://github.com/nats-io/nats-server) branch, which almost certainly will not be a released version. If you are a developer and want to play with the latest, this is the easiest way.*

Cách này sẽ cài build từ nhánh [main](https://github.com/nats-io/nats-server), hầu như chắc chắn không phải bản release chính thức. Đây là cách dễ nhất nếu bạn là developer muốn thử nghiệm với phiên bản mới nhất.

> 🇬🇧 *To test your installation (provided $GOPATH/bin is in your path) by typing `nats-server` which should output something like*

Kiểm tra cài đặt (với điều kiện `$GOPATH/bin` đã trong PATH) bằng cách gõ `nats-server` — kết quả sẽ tương tự như:

```
[2397474] 2023/09/27 10:32:02.709019 [INF] Starting nats-server
[2397474] 2023/09/27 10:32:02.709165 [INF]   Version:  2.11.0-dev
[2397474] 2023/09/27 10:32:02.709182 [INF]   Git:      [not set]
[2397474] 2023/09/27 10:32:02.709185 [INF]   Name:     NDQU7SGA4ECW4PHL4KNBY42AFQEZDAPMMQZVSQDKGTARZI5JHJV6KO2N
[2397474] 2023/09/27 10:32:02.709187 [INF]   ID:       NDQU7SGA4ECW4PHL4KNBY42AFQEZDAPMMQZVSQDKGTARZI5JHJV6KO2N
[2397474] 2023/09/27 10:32:02.709795 [INF] Listening for client connections on 0.0.0.0:4222
[2397474] 2023/09/27 10:32:02.710173 [INF] Server is ready
```

## Build từ Source

> 🇬🇧 *We use goreleaser to build assets published on [GitHub releases](https://github.com/nats-io/nats-server/releases). Our builds are fully reproducible, so with Go installed, one can execute the following commands to build from source:*

Chúng tôi dùng goreleaser để build các artifact đăng lên [GitHub releases](https://github.com/nats-io/nats-server/releases). Build hoàn toàn reproducible — với Go đã cài, chạy các lệnh sau để build từ source:

```
go install github.com/goreleaser/goreleaser/v2@latest

git clone git@github.com:nats-io/nats-server.git
cd nats-server
git checkout v2.12.0 
[[ `git status --porcelain` ]] && echo "Must have repo in clean state before building"

goreleaser release --skip=announce,publish,validate --clean -f .goreleaser.yml
```

> 🇬🇧 *And to verify SHASUMs against our release:*

Và để xác minh SHASUM so với bản release:

```
wget https://github.com/nats-io/nats-server/releases/download/v2.12.0/SHA256SUMS
diff --color --minimal --context=0 SHA256SUMS dist/SHA256SUMS
```

## Thuật ngữ trong bài

- **binary**: file chương trình đã biên dịch
- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **container**: container (đóng gói app)
- **deployment**: triển khai (Kubernetes)
- **node**: một server trong cluster
- **publisher**: bên gửi message
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục
- **subscriber**: bên đăng ký nhận message
- **TLS**: mã hóa TLS
- **timeout**: thời gian chờ tối đa