---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/service_infrastructure
title: Hạ tầng dịch vụ NATS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Hạ tầng dịch vụ NATS

> 🇬🇧 *NATS is a client/server system in the fact that you have 'NATS client applications' (applications using one of the NATS client libraries) that connect to 'NATS servers' that provide the NATS service. The NATS servers work together to provide a NATS service infrastructure to their client applications.*

NATS là hệ thống client/server: các NATS client application (ứng dụng dùng một trong các thư viện NATS client) kết nối đến NATS server để sử dụng dịch vụ. Các NATS server phối hợp với nhau để cung cấp hạ tầng dịch vụ NATS cho client application.

> 🇬🇧 *NATS is extremely flexible and scalable and allows the service infrastructure to be as small as a single process running locally on your local machine and as large as an 'Internet of NATS' of Leaf Nodes, and Leaf Node clusters all interconnected in a secure way over a global shared NATS super-cluster.*

NATS cực kỳ linh hoạt và có khả năng mở rộng cao. Hạ tầng dịch vụ có thể nhỏ gọn chỉ là một process chạy trên máy local, hoặc lớn tới mức trở thành "Internet of NATS" bao gồm các Leaf Node và Leaf Node cluster (cụm nhiều server chạy chung) kết nối với nhau một cách bảo mật qua một NATS super-cluster toàn cầu.

> 🇬🇧 *Regardless of the size and complexity of the NATS service infrastructure being used, the only configuration needed by the client applications being the location (NATS URLs) of one or more NATS servers and depending on the required security, their credentials.*

Dù hạ tầng lớn hay nhỏ, phức tạp hay đơn giản, client application chỉ cần một thứ duy nhất để cấu hình: địa chỉ (NATS URLs) của một hoặc nhiều NATS server, và tùy theo yêu cầu bảo mật, kèm theo credential (thông tin đăng nhập) tương ứng.

> 🇬🇧 *Note that if your application is written in Golang then you even have the option of embedding the NATS server functionality into the application itself (however you need to then configure your application instances with nats-server configuration information).*

Nếu ứng dụng viết bằng Golang, bạn còn có tùy chọn nhúng luôn chức năng NATS server vào trong ứng dụng (tuy nhiên khi đó bạn cần cấu hình từng instance ứng dụng bằng thông tin config của nats-server).

> 🇬🇧 *You do not actually need to run your NATS service infrastructure, instead you can instead make use of a public NATS infrastructure offered by a NATS Service Provider such as [Synadia Cloud](https://www.synadia.com/cloud?utm_source=nats_docs&utm_medium=nats), think of Synadia Cloud as being an 'Internet of NATS' (literally an "InterNATS") and of Synadia as being an "InterNATS Service Provider".*

Bạn không nhất thiết phải tự vận hành hạ tầng NATS. Thay vào đó, bạn có thể sử dụng hạ tầng NATS công cộng từ các nhà cung cấp như [Synadia Cloud](https://www.synadia.com/cloud?utm_source=nats_docs&utm_medium=nats) — hãy coi Synadia Cloud như một "Internet of NATS" (hay "InterNATS") và Synadia là "InterNATS Service Provider".

## Sự phát triển của hạ tầng dịch vụ NATS

> 🇬🇧 *You will typically start by running a single instance of nats-server on your local development machine, and have your applications connect to it while you do your application development and local testing.*

Thông thường bạn sẽ bắt đầu bằng cách chạy một instance nats-server trên máy development local, rồi để các ứng dụng kết nối vào đó trong quá trình phát triển và kiểm thử.

> 🇬🇧 *Next you will probably want to start testing and running those applications and servers in a VPC, or a region or in some on-prem location, so you will deploy either single NATS server or clusters of NATS servers in your VPCs/regions/on-prem/etc... locations and in each location have the applications connect their local nats-server or nats-server cluster. You can then connect those local nats-servers or local nats-server clusters together by making them leaf nodes connecting to a 'backbone' cluster or super-cluster, or by connecting them directly together via gateway connections.*

Tiếp theo, bạn sẽ muốn chạy ứng dụng trong môi trường VPC, theo region, hoặc on-prem. Khi đó, deploy một hoặc nhiều NATS server cluster tại mỗi vị trí và để ứng dụng kết nối vào nats-server hoặc nats-server cluster cục bộ. Sau đó, bạn có thể kết nối các nats-server hoặc cluster cục bộ lại với nhau bằng cách biến chúng thành leaf node (node (một server trong cluster) kết nối vào một "backbone" cluster hoặc super-cluster), hoặc kết nối trực tiếp qua gateway connection.

> 🇬🇧 *If you have many client applications (e.g., applications deployed on end-user devices all over the Internet, or for example many IoT devices) or many servers in a lot of locations you will then scale your NATS service infrastructure by deploying clusters of NATS servers in multiple locations and multiple cloud providers and VPCs. You will then need to connect those clusters into a global super-cluster and then devise a scheme to intelligently direct your client applications to the right 'closest' NATS server cluster.*

Khi số lượng client application tăng lớn (ví dụ: ứng dụng deploy trên thiết bị người dùng cuối khắp Internet, hay hàng loạt thiết bị IoT) hoặc khi bạn có nhiều server trải rộng ở nhiều nơi, hãy mở rộng hạ tầng bằng cách deploy cluster NATS server ở nhiều vị trí, nhiều cloud provider và VPC. Sau đó kết nối các cluster đó thành một super-cluster toàn cầu và thiết kế cơ chế điều hướng client application đến cluster NATS server "gần nhất" một cách thông minh.

## Tự vận hành hạ tầng dịch vụ NATS

> 🇬🇧 *You can deploy and run your own NATS service infrastructure of nats-server instances, composed of servers, clusters of servers, super-cluster and leaf node NATS servers.*

Bạn có thể tự deploy và vận hành hạ tầng NATS với các nats-server instance, bao gồm server đơn lẻ, cluster, super-cluster và leaf node NATS server.

### Lưu ý về ảo hóa và container hóa

> 🇬🇧 *If using Kubernetes we recommend you use the [Helm charts](https://github.com/nats-io/k8s/tree/main/helm/charts/nats).*

Nếu dùng Kubernetes, chúng tôi khuyến nghị sử dụng [Helm charts](https://github.com/nats-io/k8s/tree/main/helm/charts/nats).

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **cluster**: cụm nhiều server chạy chung
- **credential**: thông tin đăng nhập
- **deploy**: triển khai
- **node**: một server trong cluster
- **server**: máy chủ