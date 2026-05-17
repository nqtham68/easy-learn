---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/accounts
title: Multi-Tenancy sử dụng Accounts
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Multi-Tenancy sử dụng Accounts

> 🇬🇧 *In modern microservice architecture it is common to share infrastructure - such as NATS - between services. [Accounts](./accounts.md#accounts) are securely isolated communication contexts that allow multi-tenancy in a NATS deployment. They allow users to bifurcate technology from business driven use cases, where data silos are created by design, not software limitations. Furthermore, they facilitate the [controlled exchange](./accounts.md#exporting-and-importing) of information between those data silos/Tenants/Accounts.*

Trong kiến trúc microservice hiện đại, việc chia sẻ hạ tầng — chẳng hạn NATS — giữa các service là điều phổ biến. [Accounts](./accounts.md#accounts) là các ngữ cảnh giao tiếp được cô lập an toàn, cho phép triển khai NATS theo mô hình multi-tenancy. Accounts giúp tách biệt công nghệ khỏi các use case nghiệp vụ, tạo ra các data silo theo thiết kế chứ không phải do giới hạn phần mềm. Ngoài ra, chúng hỗ trợ [trao đổi thông tin có kiểm soát](./accounts.md#exporting-and-importing) giữa các data silo/Tenant/Account với nhau.

## Accounts

> 🇬🇧 *Accounts expand on the authorization foundation. With traditional authorization, all clients can publish and subscribe to anything unless explicitly configured otherwise. To protect clients and information, you have to carve the subject space and permission clients carefully.*

Accounts mở rộng nền tảng authorization. Với authorization truyền thống, mọi client đều có thể publish và subscribe bất kỳ thứ gì trừ khi được cấu hình rõ ràng. Để bảo vệ client và dữ liệu, bạn phải phân chia subject (chuỗi định danh message) space và permission (quyền truy cập) cho từng client một cách cẩn thận.

> 🇬🇧 *Accounts allow the grouping of clients, isolating them from clients in other accounts, thus enabling multi-tenancy in the server. With accounts, the subject space is not globally shared, greatly simplifying the messaging environment. Instead of devising complicated subject name carving patterns, clients can use short subjects without explicit authorization rules. [System Events](../sys_accounts) are an example of this isolation at work.*

Accounts cho phép nhóm các client lại, cô lập chúng khỏi client ở các account khác, từ đó hỗ trợ multi-tenancy trên server. Với accounts, subject space không còn được chia sẻ toàn cục, giúp môi trường messaging đơn giản hơn nhiều. Thay vì phải nghĩ ra các pattern phân chia tên subject phức tạp, client có thể dùng subject ngắn gọn mà không cần authorization rule tường minh. [System Events](../sys_accounts) là ví dụ điển hình của cơ chế cô lập này.

> 🇬🇧 *Accounts configuration is done in `accounts` map. The contents of an account entry includes:*

Cấu hình accounts được thực hiện trong map `accounts`. Mỗi account entry bao gồm:

| Property | Description |
| :--- | :--- |
| `users` | danh sách [user configuration maps](./auth_intro#user-configuration-map) |
| `exports` | danh sách [export maps](./accounts.md#export-configuration-map) |
| `imports` | danh sách [import maps](./accounts.md#import-configuration-map) |

> 🇬🇧 *The `accounts` list is a map, where the keys on the map are an account name.*

List `accounts` là một map, trong đó các key là tên account.

```text
accounts: {
    A: {
        users: [
            {user: a, password: a}
        ]
    },
    B: {
        users: [
            {user: b, password: b}
        ]
    },
}
```

> 🇬🇧 *In the most straightforward configuration above you have an account named `A` which has a single user identified by the username `a` and the password `a`, and an account named `B` with a user identified by the username `b` and the password `b`.*
>
> *These two accounts are isolated from each other. Messages published by users in `A` are not visible to users in `B`.*
>
> *The user configuration map is the same as any other NATS [user configuration map](./auth_intro#user-configuration-map). You can use: username/password, nkeys, and add permissions.*
>
> *While the name account implies one or more users, it is much simpler and enlightening to think of one account as a messaging container for one application. Users in the account are simply the minimum number of services that must work together to provide some functionality. In simpler terms, more accounts with few (even one) clients is a better design topology than a large account with many users with complex authorization configuration.*

Ở cấu hình đơn giản nhất trên, có một account tên `A` với một user dùng username `a` và password `a`, và một account tên `B` với user dùng username `b` và password `b`.

Hai account này được cô lập hoàn toàn. Message do user trong `A` publish sẽ không hiển thị đối với user trong `B`.

User configuration map giống với bất kỳ [user configuration map](./auth_intro#user-configuration-map) NATS nào. Bạn có thể dùng: username/password, nkeys, và thêm permission.

Mặc dù tên gọi _account_ hàm ý có một hoặc nhiều user, nhưng sẽ đơn giản và dễ hiểu hơn nếu coi một account là một messaging container cho một ứng dụng. User trong account chỉ là tập hợp tối thiểu các service phải hoạt động cùng nhau để cung cấp một chức năng nào đó. Nói ngắn gọn, nhiều account nhỏ (kể cả chỉ một client) là topology thiết kế tốt hơn so với một account lớn với nhiều user và cấu hình authorization phức tạp.

## Exporting và Importing

> 🇬🇧 *Messaging exchange between different accounts is enabled by exporting streams and services from one account and importing them into another. Each account controls what is exported and imported.*

Trao đổi message giữa các account khác nhau được thực hiện bằng cách export stream (luồng message lưu trữ liên tục) và service từ account này rồi import vào account khác. Mỗi account tự kiểm soát những gì được export và import.

* **Streams** là các message mà ứng dụng của bạn publish. Ứng dụng import sẽ không thể gửi request đến ứng dụng của bạn nhưng có thể tiêu thụ message bạn tạo ra.
* **Services** là các message mà ứng dụng của bạn có thể tiêu thụ và xử lý, cho phép các account khác gửi request để account của bạn thực hiện.

> 🇬🇧 *The term `stream` in the context of import and export account configuration does not refer to and should not be confused with a JetStream stream (unfortunate collision of terms as the import/export between accounts predates JetStream), it is just a 'stream of (Core NATS) messages'*

> **ℹ️ Lưu ý:**
> Thuật ngữ `stream` trong ngữ cảnh cấu hình import/export account *không* chỉ đến và không nên nhầm lẫn với JetStream stream (sự trùng lặp thuật ngữ đáng tiếc vì tính năng import/export giữa accounts có trước JetStream) — đây đơn giản là một 'luồng message (Core NATS)'.

> 🇬🇧 *The `exports` configuration list enable you to define the services and streams that others can import. Exported services and streams are expressed as an [Export configuration map](./accounts.md#export-configuration-map). The `imports` configuration lists the services and streams that an Account imports. Imported services and streams are expressed as an [Import configuration map](./accounts.md#import-configuration-map).*

List cấu hình `exports` cho phép định nghĩa các service và stream mà account khác có thể import. Service và stream được export biểu diễn dưới dạng [Export configuration map](./accounts.md#export-configuration-map). List cấu hình `imports` liệt kê các service và stream mà một Account import. Service và stream được import biểu diễn dưới dạng [Import configuration map](./accounts.md#import-configuration-map).

### Export Configuration Map

> 🇬🇧 *The export configuration map binds a subject for use as a `service` or `stream` and optionally defines specific accounts that can import the stream or service. Here are the supported configuration properties:*

Export configuration map gắn một subject với vai trò là `service` hoặc `stream`, và tùy chọn xác định những account cụ thể có thể import stream hoặc service đó. Dưới đây là các thuộc tính cấu hình được hỗ trợ:

| Property | Description |
| :--- | :--- |
| `stream` | Một subject hoặc subject có wildcard mà account sẽ publish. \(loại trừ `service`\) |
| `service` | Một subject hoặc subject có wildcard mà account sẽ subscribe. \(loại trừ `stream`\) |
| `accounts` | Danh sách tên account có thể import stream hoặc service. Nếu không chỉ định, service hoặc stream là public và bất kỳ account nào cũng có thể import. |
| `response_type` | Cho biết response của một request `service` gồm một `single` hay nhiều `stream` message. Các giá trị có thể: `single` hoặc `stream`. \(Mặc định là `singleton`\) |

> 🇬🇧 *Here are some example exports:*

Dưới đây là một số ví dụ export:

```text
accounts: {
    A: {
        users: [
            {user: a, password: a}
        ]
        exports: [
            {stream: puba.>}
            {service: pubq.>}
            {stream: b.>, accounts: [B]}
            {service: q.b, accounts: [B]}
        ]
    }
    ...
}
```

> 🇬🇧 *Here's what `A` is exporting: a public stream on the wildcard subject `puba.>`, a public service on the wildcard subject `pubq.>`, a stream to account `B` on the wildcard subject `b.>`, a service to account `B` on the subject `q.b`.*

`A` đang export:

* một public stream trên wildcard subject `puba.>`
* một public service trên wildcard subject `pubq.>`
* một stream đến account `B` trên wildcard subject `b.>`
* một service đến account `B` trên subject `q.b`

### Import Configuration Map

> 🇬🇧 *An import enables an account to consume streams published by another account or make requests to services implemented by another account. All imports require a corresponding export on the exporting account. Accounts cannot do self-imports.*

Import cho phép một account tiêu thụ stream do account khác publish hoặc gửi request đến service mà account khác cài đặt. Mọi import đều yêu cầu một export tương ứng ở phía account export. Accounts không thể tự import từ chính mình.

| Property | Description |
| :--- | :--- |
| `stream` | [Source configuration](./accounts.md#source-configuration-map) cho stream import. \(loại trừ `service`\) |
| `service` | [Source configuration](./accounts.md#source-configuration-map) cho service import. \(loại trừ `stream`\) |
| `prefix` | Tiền tố subject mapping cục bộ cho stream được import. \(áp dụng cho `stream`\) |
| `to` | Subject mapping cục bộ cho service được import. \(áp dụng cho `service`\) |

> 🇬🇧 *The `prefix` and `to` options are optional and allow you to remap the subject that is used locally to receive stream messages from or publish service requests to. This way the importing account does not depend on naming conventions picked by another. Currently, a service import can not make use of wildcards, which is why the import subject can be rewritten. A stream import may make use of wildcards. To retain information contained in the subject, it can thus only be prefixed with `prefix`...*

Tùy chọn `prefix` và `to` là không bắt buộc, cho phép remap subject được dùng cục bộ để nhận message từ stream hoặc publish request đến service. Nhờ vậy, account import không phụ thuộc vào quy ước đặt tên của account khác. Hiện tại, service import không thể dùng wildcard, vì vậy subject import có thể được viết lại. Stream import có thể dùng wildcard. Để giữ thông tin trong subject, stream import chỉ có thể được thêm tiền tố bằng `prefix`...

#### Source Configuration Map

> 🇬🇧 *The source configuration map describes an export from a remote account by specifying the `account` and `subject` of the export being imported. This map is embedded in the [import configuration map](./accounts.md#import-configuration-map):*

Source configuration map mô tả một export từ account từ xa bằng cách chỉ định `account` và `subject` của export cần import. Map này được nhúng trong [import configuration map](./accounts.md#import-configuration-map):

| Property | Description |
| :--- | :--- |
| `account` | Tên account sở hữu export. |
| `subject` | Subject mà stream hoặc service được cung cấp cho account import. |

### Ví dụ Import/Export

```text
accounts: {
    A: {
        users: [
            {user: a, password: a}
        ]
        exports: [
            {stream: puba.>}
            {service: pubq.>}
            {stream: b.>, accounts: [B]}
            {service: q.b, accounts: [B]}
        ]
    },
    B: {
        users: [
            {user: b, password: b}
        ]
        imports: [
            {stream: {account: A, subject: b.>}}
            {service: {account: A, subject: q.b}}
        ]
    }
    C: {
        users: [
            {user: c, password: c}
        ]
        imports: [
            {stream: {account: A, subject: puba.>}, prefix: from_a}
            {service: {account: A, subject: pubq.C}, to: Q}
        ]
    }
}
```

> 🇬🇧 *Account `B` imports: the private stream from `A` that only `B` can receive on `b.>`, the private service from `A` that only `B` can send requests on `q.b`.*

Account `B` import:

* private stream từ `A` mà chỉ `B` có thể nhận trên `b.>`
* private service từ `A` mà chỉ `B` có thể gửi request trên `q.b`

> 🇬🇧 *Account `C` imports the public service and stream from `A`, but also: remaps the `puba.>` stream to be locally available under `from_a.puba.>`. The messages will have their original subjects prefixed by `from_a`. Remaps the `pubq.C` service to be locally available under `Q`. Account `C` only needs to publish to `Q` locally.*

Account `C` import public service và stream từ `A`, nhưng còn:

* remap stream `puba.>` để truy cập cục bộ dưới tên `from_a.puba.>`. Các message sẽ có subject gốc được thêm tiền tố `from_a`.
* remap service `pubq.C` để truy cập cục bộ dưới tên `Q`. Account `C` chỉ cần publish đến `Q` cục bộ.

> 🇬🇧 *It is important to reiterate that: stream `puba.>` from `A` is visible to all external accounts that imports the stream. Service `pubq.>` from `A` is available to all external accounts so long as they know the full subject of where to send the request. Typically an account will export a wildcard service but then coordinate with a client account on specific subjects where requests will be answered. On our example, account `C` access the service on `pubq.C` (but has mapped it for simplicity to `Q`). Stream `b.>` is private, only account `B` can receive messages from the stream. Service `q.b` is private; only account `B` can send requests to the service. When `C` publishes a request to `Q`, local `C` clients will see `Q` messages. However, the server will remap `Q` to `pubq.C` and forward the requests to account `A`.*

Cần nhắc lại một số điểm quan trọng:

* Stream `puba.>` từ `A` hiển thị với tất cả external account đã import stream đó.
* Service `pubq.>` từ `A` khả dụng với mọi external account miễn là họ biết subject đầy đủ để gửi request. Thông thường, một account sẽ export wildcard service rồi phối hợp với account client về các subject cụ thể nơi request được xử lý. Trong ví dụ này, account `C` truy cập service trên `pubq.C` \(nhưng đã remap để tiện thành `Q`\).
* Stream `b.>` là private, chỉ account `B` có thể nhận message từ stream đó.
* Service `q.b` là private, chỉ account `B` có thể gửi request đến service đó.
* Khi `C` publish một request đến `Q`, các client `C` cục bộ sẽ thấy message `Q`. Tuy nhiên, server sẽ remap `Q` thành `pubq.C` và chuyển tiếp request đến account `A`.

## No Auth User

> 🇬🇧 *Clients connecting without authentication can be associated with a particular user within an account.*

Client kết nối mà không xác thực có thể được liên kết với một user cụ thể trong một account.

```text
accounts: {
    A: {
        users: [
            {user: a, password: a}
        ]
    },
    B: {
        users: [
            {user: b, password: b}
        ]
    }
}
no_auth_user: a
```

> 🇬🇧 *The above example shows how clients without authentication can be associated with the user `a` within account `A`.*

Ví dụ trên minh họa cách client không xác thực có thể được liên kết với user `a` trong account `A`.

> 🇬🇧 *Please note that the `no_auth_user` will not work with nkeys or bcrypted passwords. The user referenced can also be part of the [authorization](./authorization.md) block.*
>
> *Despite `no_auth_user` being set, clients still need to communicate that they will not be using credentials. The [authentication timeout](./auth_intro/auth_timeout.md) applies to this process as well. When your connection is slow, you may run into this timeout and the resulting `Authentication Timeout` error, despite not providing credentials.*

> Lưu ý rằng `no_auth_user` sẽ không hoạt động với nkeys hoặc bcrypted password. User được tham chiếu cũng có thể là một phần của block [authorization](./authorization.md).
>
> Dù `no_auth_user` đã được thiết lập, client vẫn cần thông báo rằng họ sẽ không dùng credential. [Authentication timeout](./auth_intro/auth_timeout.md) cũng áp dụng cho quá trình này. Khi kết nối chậm, bạn có thể gặp timeout này và lỗi `Authentication Timeout` kèm theo, dù không cung cấp credential.

## Exporting và Importing JetStream streams giữa các accounts

> 🇬🇧 *It is possible to import/export messages stored in JetStream streams between accounts. While it is possible to allow a client application in one account to access a stream located in another account, in most use cases people want a setup where a stream in one account is mirrored or sourced in another account (and the applications in that other account simply use that mirrored/sourced stream in their account), as this is a more 'locked-down' way to share messages in streams between accounts, compared to letting the client applications directly use a stream in another account.*

Có thể import/export message được lưu trong JetStream stream giữa các account. Mặc dù có thể cho phép ứng dụng client ở một account truy cập trực tiếp stream ở account khác, nhưng trong hầu hết trường hợp, người dùng muốn thiết lập stream ở một account được mirror hoặc source sang account khác (và các ứng dụng ở account đó đơn giản dùng stream đã được mirror/source trong account của họ). Đây là cách chia sẻ message trong stream giữa các account an toàn hơn so với việc để client trực tiếp dùng stream ở account khác.

> 🇬🇧 *There are two resources documenting and giving examples of how to do this:*

Có hai tài nguyên ghi lại và cung cấp ví dụ về cách thực hiện:

* [Cross account JetStream sourcing](https://github.com/synadia-labs/cross-account-jetstream-sourcing) giải thích và có ví dụ thực hành về cách thực hiện với static security đơn giản (có thể là điểm khởi đầu tốt nhất), và
* [Connect Streams Cross Accounts](https://github.com/nats-io/jetstream-leaf-nodes-demo#connect-streams-cross-accounts) giải thích cách thực hiện tương tự khi dùng chế độ bảo mật dựa trên 'operator' JWT.

# Xem thêm

* [Multi-tenancy and resource management](https://docs.nats.io/running-a-nats-service/configuration/resource_management#multi-tenancy-and-resource-mgmt)

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **message**: gói dữ liệu được gửi đi
- **permission**: quyền truy cập
- **request**: yêu cầu
- **response**: phản hồi
- **server**: máy chủ
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)