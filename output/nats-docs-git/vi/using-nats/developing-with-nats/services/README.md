---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/services
title: Xây dựng Services
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Xây dựng Services

> 🇬🇧 *Recently we have agreed upon an [initial specification](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-32.md) for a services protocol so that we can add first-class services support to NATS clients and support this in our tooling. This services protocol is an agreement between clients and tooling and doesn't require any special functionality from the NATS server or JetStream.*

Chúng tôi vừa thống nhất một [đặc tả ban đầu](https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-32.md) cho services protocol (giao thức dịch vụ), nhằm bổ sung hỗ trợ service (dịch vụ) bậc nhất vào NATS client và tích hợp vào các công cụ hiện có. Services protocol là thỏa thuận giữa client và tooling, không yêu cầu chức năng đặc biệt nào từ NATS server hay JetStream.

> 🇬🇧 *To check if the NATS client in your favorite language supports the new services API, make sure you check the docs and GitHub repository for that client. The services API is relatively new and not all clients may support it yet.*

Để kiểm tra xem NATS client cho ngôn ngữ bạn đang dùng có hỗ trợ services API (giao diện lập trình) mới không, hãy xem tài liệu và repository GitHub của client đó. Services API còn khá mới và chưa phải tất cả client đều hỗ trợ.

> 🇬🇧 *To see the services API in action in different languages, take a look at the [NATS By Example](https://natsbyexample.com/examples/services/intro/go) samples.*

Để xem services API hoạt động thực tế trên nhiều ngôn ngữ khác nhau, tham khảo các mẫu tại [NATS By Example](https://natsbyexample.com/examples/services/intro/go).

## Các Khái Niệm

> 🇬🇧 *There are a few high level concepts in the services API worth understanding before you start developing your own services.*

Trước khi bắt đầu xây dựng service, cần nắm một số khái niệm cốt lõi trong services API.

### Service

> 🇬🇧 *The service is the highest level abstraction and refers to a group of logically related functionality. Services are required to have names and versions that conform to the [semver](https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string) rules. Services are discoverable within a NATS system.*

Service là lớp trừu tượng cao nhất, đại diện cho một nhóm chức năng liên quan về mặt logic. Mỗi service bắt buộc phải có tên và phiên bản tuân theo quy tắc [semver](https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string). Các service có thể được khám phá (discoverable) trong hệ thống NATS.

### Endpoint

> 🇬🇧 *A service endpoint is the entity with which clients interact. You can think of an endpoint as a single operation within a service. All services must have at least 1 endpoint.*

Endpoint (địa chỉ API cụ thể) là đơn vị mà client tương tác trực tiếp — tương đương một thao tác đơn lẻ trong service. Mỗi service phải có ít nhất 1 endpoint.

### Group

> 🇬🇧 *A group is a collection of endpoints. These are optional and can provide a logical association between endpoints as well as an optional common subject prefix for all endpoints.*

Group là tập hợp các endpoint. Group là tùy chọn, dùng để nhóm các endpoint có liên quan và có thể định nghĩa một subject (chuỗi định danh message) prefix chung cho tất cả các endpoint trong nhóm.

## Các Thao Tác của Service

> 🇬🇧 *The services API supports 3 operations for discoverability and observability. While the NATS client will take care of responding on these subjects, it is still the developer's responsibility to respond to requests made the service's actual endpoints.*

Services API hỗ trợ 3 thao tác phục vụ khả năng khám phá và quan sát. NATS client sẽ tự xử lý phản hồi trên các subject này; tuy nhiên developer vẫn phải tự xử lý các request gửi đến các endpoint thực tế của service.

* `PING` - Các request gửi lên subject `$SRV.PING.>` thu thập phản hồi từ các service đang chạy, hỗ trợ tooling liệt kê danh sách service.
* `STATS` - Các request gửi lên subject `$SRV.STATS.>` truy vấn số liệu thống kê từ service, bao gồm tổng số request, tổng số lỗi và tổng thời gian xử lý.
* `INFO` - Các request gửi lên subject `$SRV.INFO.>` lấy định nghĩa và metadata của service, bao gồm các group, endpoint, v.v.

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **endpoint**: địa chỉ API cụ thể
- **request**: yêu cầu
- **service**: dịch vụ
- **subject**: chuỗi định danh message (giống topic)