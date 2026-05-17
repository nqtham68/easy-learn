---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/overview
title: Tổng quan
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Tổng quan

> 🇬🇧 *__What is NATS?__ NATS is a connective technology that powers modern distributed systems. A connective technology is responsible for addressing, discovery and exchanging of messages that drive the common patterns in distributed systems; asking and answering questions, aka services/microservices, and making and processing statements, or stream processing.*

**NATS là gì?**
NATS là một công nghệ kết nối (connective technology) phục vụ các hệ thống phân tán hiện đại. Công nghệ kết nối chịu trách nhiệm định địa chỉ, khám phá (discovery) và trao đổi message (gói dữ liệu được gửi đi) — những yếu tố dẫn dắt các mô hình phổ biến trong hệ thống phân tán: hỏi-đáp (tức service/microservice) và tạo-xử lý dữ liệu (tức stream processing).

> 🇬🇧 *__Challenges faced by modern distributed systems__ Modern distributed systems are defined by an ever increasing number of hyper-connected moving parts and the additional data they generate. They employ both services and streams to drive business value. They are also being defined by location independence and mobility, and not just for things we would typically recognize as front end technologies. Today's systems and the backend processes, microservices and stream processing are being asked to be location independent and mobile as well, all while being secure.*

**Thách thức của hệ thống phân tán hiện đại**
Hệ thống phân tán hiện đại được định nghĩa bởi số lượng thành phần siêu kết nối ngày càng tăng và lượng dữ liệu chúng tạo ra. Chúng sử dụng cả service lẫn stream (luồng message lưu trữ liên tục) để tạo ra giá trị kinh doanh. Ngoài ra, chúng còn được định nghĩa bởi tính độc lập vị trí và tính di động — không chỉ với các công nghệ front end quen thuộc. Các tiến trình backend, microservice và stream processing ngày nay cũng được yêu cầu hoạt động độc lập vị trí, linh động và bảo mật.

> 🇬🇧 *These modern systems present challenges to technologies that have been used to connect mobile front ends to fairly static backends. These incumbent technologies typically manage addressing and discovery via hostname (DNS) or IP and port, utilize a 1:1 communication pattern, and have multiple different security patterns for authentication and authorization. Although not perfect, incumbent technologies have been good enough in many situations, but times are changing quickly. As microservices, functions, and stream processing are being asked to move to the edge, these technologies and the assumptions they make are being challenged.*

Các hệ thống hiện đại này đặt ra thách thức cho những công nghệ vốn dùng để kết nối front end di động với backend tương đối tĩnh. Các công nghệ truyền thống thường quản lý địa chỉ và discovery qua hostname (DNS) hoặc IP và port, sử dụng mô hình giao tiếp 1:1, và có nhiều cơ chế bảo mật khác nhau cho authentication và authorization. Dù không hoàn hảo, chúng vẫn đủ dùng trong nhiều tình huống — nhưng thời cuộc đang thay đổi nhanh chóng. Khi microservice, function và stream processing được yêu cầu chạy tại edge, các công nghệ này và những giả định của chúng đang bị thách thức.

## NATS khác biệt như thế nào với hệ thống hiện đại?

> 🇬🇧 *__Effortless M:N connectivity:__ NATS manages addressing and discovery based on subjects and not hostname and ports. Defaulting to M:N communications, which is a superset of 1:1, meaning it can do 1:1 but can also do so much more. If you have a 1:1 system that is successful in development, ask how many other moving parts are required for production to work around the assumption of 1:1? Things like load balancers, log systems, and network security models, as well as proxies and sidecars. If your production system requires all of these things just to get around the fact that the connective technology being used, e.g. HTTP or gRPC, is 1:1, it's time to give NATS.io a look.*

**Kết nối M:N dễ dàng:** NATS quản lý địa chỉ và discovery dựa trên subject (chuỗi định danh message) thay vì hostname và port. Mặc định là giao tiếp M:N — bao gồm cả 1:1 nhưng còn làm được nhiều hơn thế. Nếu bạn có hệ thống 1:1 hoạt động tốt ở môi trường dev, hãy tự hỏi cần bao nhiêu thành phần phụ để hệ thống production vận hành: load balancer, log system, mô hình bảo mật mạng, proxy, sidecar... Nếu production cần tất cả những thứ đó chỉ để bù đắp cho giới hạn 1:1 của HTTP hay gRPC, đã đến lúc nhìn vào NATS.io.

> 🇬🇧 *__Deploy anywhere:__ NATS can be deployed nearly anywhere; on bare metal, in a VM, as a container, inside K8S, on a device, or whichever environment you choose. NATS runs well within deployment frameworks or without.*

**Deploy ở bất kỳ đâu:** NATS có thể deploy trên bare metal, VM, container, bên trong K8S, trên thiết bị, hoặc bất kỳ môi trường nào bạn chọn. NATS hoạt động tốt dù có hay không có deployment framework.

> 🇬🇧 *__Secure:__ Similarly, NATS is secure by default and makes no requirements on network perimeter security models. When you start considering mobilizing your backend microservices and stream processors, many times the biggest roadblock is security.*

**Bảo mật:** NATS bảo mật theo mặc định và không yêu cầu mô hình bảo mật vành đai mạng. Khi bắt đầu triển khai di động hóa backend microservice và stream processor, rào cản lớn nhất thường là bảo mật — NATS giải quyết điều đó ngay từ đầu.

### Triển khai có khả năng mở rộng và bền vững

> 🇬🇧 *NATS infrastructure and clients communicate all topology changes in real-time. This means that NATS clients do not need to change when NATS deployments change. Having to change clients with deployments would be like having to reboot your phone every time your cell provider added or changed a cell tower. This sounds ridiculous of course, but think about how many systems today have their front ends tied so closely to the backend, that any change requires a complete front end reboot or at least a reconfiguration. NATS clients and applications need no such change when backend servers are added and removed and changed. Even DNS is only used to bootstrap first contact, after that, NATS handles endpoint locations transparently.*

Hạ tầng và client của NATS giao tiếp tất cả thay đổi topology theo thời gian thực. Điều này có nghĩa là NATS client không cần thay đổi khi deployment thay đổi. Phải thay đổi client theo deployment cũng giống như phải khởi động lại điện thoại mỗi khi nhà mạng thêm hoặc thay đổi trạm phát sóng — nghe vô lý, nhưng hãy nghĩ xem có bao nhiêu hệ thống hiện nay gắn chặt front end với backend đến mức mọi thay đổi đều yêu cầu khởi động lại hoặc cấu hình lại toàn bộ front end. NATS client và ứng dụng không cần thay đổi khi backend server được thêm, xóa hay chỉnh sửa. Thậm chí DNS chỉ được dùng để thiết lập kết nối đầu tiên; sau đó NATS tự xử lý vị trí endpoint (địa chỉ API cụ thể) một cách minh bạch.

### Triển khai hybrid

> 🇬🇧 *Another advantage to utilizing a NATS is that it allows a hybrid mix of SaaS/Utility computing with separately owned and operated systems. Meaning you can have a shared NATS service with core microservices, streams and stream processing be extended by groups or individuals who have a need to run their own NATS infrastructure. You are not forced to choose one or the other.*

Một lợi thế khác của NATS là cho phép kết hợp hybrid giữa SaaS/Utility computing và các hệ thống vận hành độc lập. Nghĩa là bạn có thể có một NATS service chia sẻ với các microservice lõi, stream và stream processing, đồng thời cho phép các nhóm hoặc cá nhân muốn chạy hạ tầng NATS riêng tự mở rộng. Bạn không bị ép buộc phải chọn một trong hai.

### Khả năng thích nghi

> 🇬🇧 *Today's systems will fall short with new demands. As modern systems continue to evolve and utilize more components and process more data, supporting patterns beyond 1:1 communications, with addressing and discovery tied to DNS is critical. Foundational technologies like NATS promise the most return on investment. Incumbent technologies will not work as modern systems unify cloud, Edge, IoT and beyond. NATS does.*

Các hệ thống hiện tại sẽ không đáp ứng được nhu cầu mới. Khi hệ thống hiện đại tiếp tục phát triển, sử dụng nhiều thành phần hơn và xử lý nhiều dữ liệu hơn, việc hỗ trợ các mô hình giao tiếp vượt ngoài 1:1 với địa chỉ và discovery gắn với DNS là điều cốt lõi. Các công nghệ nền tảng như NATS mang lại lợi nhuận đầu tư cao nhất. Các công nghệ truyền thống sẽ không theo kịp khi hệ thống hiện đại thống nhất cloud, Edge, IoT và xa hơn. NATS thì có thể.

### Các trường hợp sử dụng

> 🇬🇧 *NATS can run anywhere, from large servers and cloud instances, through edge gateways and even IoT devices. Use cases for NATS include:*

NATS có thể chạy ở bất kỳ đâu: từ server lớn và cloud instance, qua edge gateway đến cả thiết bị IoT. Các trường hợp sử dụng của NATS bao gồm:

* Cloud Messaging
    * Services \(microservices, service mesh\)
    * Event/Data Streaming \(observability, analytics, ML/AI\)
* Command and Control
    * IoT and Edge
    * Telemetry / Sensor Data / Command and Control
* Augmenting or Replacing Legacy Messaging Systems

## Thuật ngữ trong bài

- **endpoint**: địa chỉ API cụ thể
- **message**: gói dữ liệu được gửi đi
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)