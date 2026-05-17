---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/configuring_subject_mapping
title: Subject Mapping và Định Hình Lưu Lượng
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Subject Mapping và Định Hình Lưu Lượng

_Hỗ trợ từ NATS Server phiên bản 2.2_

> 🇬🇧 *Subject mapping is a very powerful feature of the NATS server, useful for canary deployments, A/B testing, chaos testing, and migrating to a new subject namespace.*

Subject mapping (chuỗi định danh message) là tính năng mạnh mẽ của NATS server, hữu ích cho canary deployment, A/B testing, chaos testing, và chuyển đổi sang namespace subject mới.

## Cấu hình subject mapping

> 🇬🇧 *Subject mappings are defined and applied at the account level. If you are using static account security you will need to edit the server configuration file, however if you are using JWT Security (Operator Mode), then you need to use nsc or customer tools to edit and push changes to you account.*

Subject mapping được định nghĩa và áp dụng ở cấp account. Nếu dùng static account security, bạn cần chỉnh sửa file config (cấu hình) của server. Nếu dùng JWT Security (Operator Mode), bạn cần dùng `nsc` hoặc công cụ tùy chỉnh để chỉnh sửa và đẩy thay đổi lên account.

> 🇬🇧 *NOTE: You can also use subject mapping as part of defining imports and exports between accounts*

NOTE: _Bạn cũng có thể dùng subject mapping khi định nghĩa imports và exports giữa các account._

### Static authentication

> 🇬🇧 *In any of the static authentication modes the mappings are defined in the server configuration file, any changes to mappings in the configuration file will take effect as soon as a reload signal is sent to the server process (e.g. use `nats-server --signal reload`).*

Trong tất cả các chế độ static authentication, mapping được định nghĩa trong file config của server. Mọi thay đổi sẽ có hiệu lực ngay khi gửi reload signal đến server process (ví dụ: dùng `nats-server --signal reload`).

> 🇬🇧 *The `mappings` stanza can occur at the top level to apply to the global account or be scoped within a specific account.*

Stanza `mappings` có thể đặt ở top level để áp dụng cho global account, hoặc thu hẹp phạm vi vào một account cụ thể.

```text
mappings = {

  # Simple direct mapping.  Messages published to foo are mapped to bar.
  foo: bar

  # remapping tokens can be done with $<N> representing token position.
  # In this example bar.a.b would be mapped to baz.b.a.
  bar.*.*: baz.$2.$1

  # You can scope mappings to a particular cluster
  foo.cluster.scoped : [
    { destination: bar.cluster.scoped, weight:100%, cluster: us-west-1 }
  ]

  # Use weighted mapping for canary testing or A/B testing.  Change dynamically
  # at any time with a server reload.
  myservice.request: [
    { destination: myservice.request.v1, weight: 90% },
    { destination: myservice.request.v2, weight: 10% }
  ]

  # A testing example of wildcard mapping balanced across two subjects.
  # 20% of the traffic is mapped to a service in QA coded to fail.
  myservice.test.*: [
    { destination: myservice.test.$1, weight: 80% },
    { destination: myservice.test.fail.$1, weight: 20% }
  ]

  # A chaos testing trick that introduces 50% artificial message loss of
  # messages published to foo.loss
  foo.loss.>: [ { destination: foo.loss.>, weight: 50% } ]
}
```

### JWT authentication

> 🇬🇧 *When using the JWT authentication mode, the mappings are defined in the account's JWT. Account JWTs can be created or modified either through the [JWT API](https://github.com/nats-io/jwt) or using the `nsc` CLI too. For more detailed information see `nsc add mapping --help`, `nsc delete mapping --help`. Subject mapping changes take effect as soon as the modified account JWT is pushed to the nats servers (i.e. `nsc push`).*

Khi dùng JWT authentication, mapping được định nghĩa trong JWT của account. Account JWT có thể tạo hoặc chỉnh sửa qua [JWT API](https://github.com/nats-io/jwt) hoặc CLI `nsc`. Để biết thêm chi tiết, xem `nsc add mapping --help`, `nsc delete mapping --help`. Thay đổi subject mapping có hiệu lực ngay khi JWT đã chỉnh sửa được đẩy lên NATS server (tức `nsc push`).

> 🇬🇧 *Examples of using `nsc` to manage mappings:*

Ví dụ dùng `nsc` để quản lý mapping:

* Thêm mapping mới: `nsc add mapping --from "a" --to "b"`
* Sửa một entry, ví dụ đặt weight sau khi đã tạo: `nsc add mapping --from "a" --to "b" --weight 50`
* Thêm hai entry từ một subject, đặt weight và chạy nhiều lần: `nsc add mapping --from "a" --to "c" --weight 50`
* Xóa một mapping: `nsc delete mapping --from "a"`

## Simple Mapping

> 🇬🇧 *The example of `foo:bar` is straightforward. All messages the server receives on subject `foo` are remapped and can be received by clients subscribed to `bar`.*

Ví dụ `foo:bar` rất đơn giản. Tất cả message mà server nhận trên subject `foo` đều được remap và có thể nhận bởi client đã subscribe vào `bar`.

## Sắp xếp lại Subject Token

> 🇬🇧 *Wildcard tokens may be referenced via `$<position>`. For example, the first wildcard token is $1, the second is $2, etc. Referencing these tokens can allow for reordering.*

Wildcard token có thể được tham chiếu qua `$<position>`. Ví dụ: wildcard đầu tiên là $1, thứ hai là $2, v.v. Tham chiếu các token này cho phép sắp xếp lại thứ tự.

> 🇬🇧 *With this mapping:*

Với mapping này:

```text
  bar.*.*: baz.$2.$1
```

> 🇬🇧 *Messages that were originally published to `bar.a.b` are remapped in the server to `baz.b.a`. Messages arriving at the server on `bar.one.two` would be mapped to `baz.two.one`, and so forth.*

Message gốc được publish lên `bar.a.b` sẽ được remap thành `baz.b.a` trên server. Message đến trên `bar.one.two` sẽ được map thành `baz.two.one`, và cứ thế tiếp tục.

## Weighted Mapping cho A/B Testing hoặc Canary Release

> 🇬🇧 *Traffic can be split by percentage from one subject to multiple subjects. Here's an example for canary deployments, starting with version 1 of your service.*

Lưu lượng có thể được chia theo phần trăm từ một subject sang nhiều subject khác. Dưới đây là ví dụ cho canary deployment, bắt đầu với phiên bản 1 của service (dịch vụ).

> 🇬🇧 *Applications would make requests of a service at `myservice.requests`. The responders doing the work of the server would subscribe to `myservice.requests.v1`. Your configuration would look like this:*

Các ứng dụng gửi request đến service tại `myservice.requests`. Các responder xử lý công việc sẽ subscribe (bên đăng ký nhận message) vào `myservice.requests.v1`. Config sẽ trông như sau:

```text
  myservice.requests: [
    { destination: myservice.requests.v1, weight: 100% }
  ]
```

> 🇬🇧 *All requests to `myservice.requests` will go to version 1 of your service.*

Tất cả request đến `myservice.requests` sẽ được chuyển đến phiên bản 1 của service.

> 🇬🇧 *When version 2 comes along, you'll want to test it with a canary deployment. Version 2 would subscribe to `myservice.requests.v2`. Launch instances of your service (don't forget about queue subscribers and load balancing).*

Khi phiên bản 2 ra đời, bạn muốn kiểm thử bằng canary deployment. Phiên bản 2 sẽ subscribe vào `myservice.requests.v2`. Khởi chạy các instance của service (đừng quên queue subscriber và load balancing).

> 🇬🇧 *Update the configuration file to redirect some portion of the requests made to `myservice.requests` to version 2 of your service. In this case we'll use 2%.*

Cập nhật file config để chuyển một phần request đến `myservice.requests` sang phiên bản 2. Ở đây ta dùng 2%.

```text
  myservice.requests: [
    { destination: myservice.requests.v1, weight: 98% },
    { destination: myservice.requests.v2, weight: 2% }
  ]
```

> 🇬🇧 *You can [reload](../nats_admin/signals.md) the server at this point to make the changes with zero downtime. After reloading, 2% of your requests will be serviced by the new version.*

Bạn có thể [reload](../nats_admin/signals.md) server để áp dụng thay đổi mà không mất downtime. Sau khi reload, 2% request sẽ được xử lý bởi phiên bản mới.

> 🇬🇧 *Once you've determined Version 2 stable switch 100% of the traffic over and reload the server with a new configuration.*

Khi xác định phiên bản 2 ổn định, chuyển 100% lưu lượng sang và reload server với config mới.

```text
  myservice.requests: [
    { destination: myservice.requests.v2, weight: 100% }
  ]
```

> 🇬🇧 *Now shutdown the version 1 instances of your service.*

Lúc này hãy tắt các instance phiên bản 1 của service.

## Định Hình Lưu Lượng trong Testing

> 🇬🇧 *Traffic shaping is useful in testing. You might have a service that runs in QA that simulates failure scenarios which could receive 20% of the traffic to test the service requestor.*

Định hình lưu lượng (traffic shaping) rất hữu ích trong testing. Bạn có thể có một service chạy trong môi trường QA để mô phỏng các tình huống lỗi, nhận 20% lưu lượng để kiểm thử service requestor.

```text
  myservice.requests.*: [
    { destination: myservice.requests.$1, weight: 80% },
    { destination: myservice.requests.fail.$1, weight: 20% }
  ]
```

## Mô Phỏng Mất Gói

> 🇬🇧 *Alternatively, introduce loss into your system for chaos testing by mapping a percentage of traffic to the same subject. In this drastic example, 50% of the traffic published to `foo.loss.a` would be artificially dropped by the server.*

Ngoài ra, bạn có thể giả lập mất gói trong hệ thống cho chaos testing bằng cách map một phần trăm lưu lượng về chính subject đó. Trong ví dụ cực đoan này, 50% lưu lượng được publish lên `foo.loss.a` sẽ bị server loại bỏ giả tạo.

```text
  foo.loss.>: [ { destination: foo.loss.>, weight: 50% } ]
```

> 🇬🇧 *You can both split and introduce loss for testing. Here, 90% of requests would go to your service, 8% would go to a service simulating failure conditions, and the unaccounted for 2% would simulate message loss.*

Bạn có thể vừa phân tách lưu lượng vừa giả lập mất gói trong testing. Ở đây, 90% request đến service của bạn, 8% đến service mô phỏng lỗi, và 2% còn lại mô phỏng mất message.

```text
  myservice.requests: [
    { destination: myservice.requests.v3, weight: 90% },
    { destination: myservice.requests.v3.fail, weight: 8% }
    # the remaining 2% is "lost"
  ]
```

## Thuật ngữ trong bài

- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **publisher**: bên gửi message
- **service**: dịch vụ
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message