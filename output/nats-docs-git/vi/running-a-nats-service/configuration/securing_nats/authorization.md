---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/authorization
title: Phân Quyền
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Phân Quyền

> 🇬🇧 *The NATS server supports authorization using subject-level permissions on a per-user basis. Permission-based authorization is available with multi-user authentication via the `users` list.*

NATS server hỗ trợ phân quyền theo subject (chuỗi định danh message) ở cấp độ từng user. Permission (quyền truy cập) dạng này khả dụng khi dùng xác thực đa user thông qua danh sách `users`.

> 🇬🇧 *Each permission specifies the subjects the user can publish to and subscribe to. The parser is generous at understanding what the intent is, so both arrays and singletons are processed. For more complex configuration, you can specify a `permission` object which explicitly allows or denies subjects. The specified subjects can specify wildcards as well. Permissions can make use of [variables](./authorization.md#variables).*

Mỗi permission xác định các subject mà user được phép publish (bên gửi message) và subscribe (bên đăng ký nhận message). Parser xử lý được cả mảng lẫn giá trị đơn lẻ. Với cấu hình phức tạp hơn, có thể dùng object `permission` để cho phép hoặc từ chối subject tường minh. Subject cũng hỗ trợ wildcard. Permission có thể dùng [variables](./authorization.md#variables).

> 🇬🇧 *A special field inside the authorization map is `default_permissions`. When present, it contains permissions that apply to users that do not have permissions associated with them.*

Trường đặc biệt `default_permissions` trong authorization map chứa các permission áp dụng cho những user chưa được gán permission cụ thể.

## Cấu Hình Permission Map

> 🇬🇧 *The `permissions` map specify subjects that can be subscribed to or published by the specified client.*

Map `permissions` xác định các subject mà client được phép subscribe hoặc publish.

| Property          | Description                                                                                                                                                                                                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `publish`         | subject, list of subjects, or [permission map](./authorization.md#permission-map) the client can publish                                                                                                                                                                                                 |
| `subscribe`       | subject, list of subjects, or [permission map](./authorization.md#permission-map) the client can subscribe to. In this context it is possible to provide an optional queue name: `<subject> <queue>` to express queue group permissions. These permissions can also use wildcards such as `v2.*` or `>`. |
| `allow_responses` | boolean or [responses map](./authorization.md#allow-responses-map), default is `false`. Enabling this implicitly denies publish to other subjects, however an explicit `publish` allow on a subject will override this implicit deny for that subject.                                                   |

## Permission Map

> 🇬🇧 *The `permission` map provides additional properties for configuring a `permissions` map. Instead of providing a list of allowable subjects and optional queues, the `permission` map allows you to explicitly list those you want to`allow` or `deny`. Both lists can be provided. In case of overlap `deny` has priority.*

Map `permission` cung cấp thêm thuộc tính cho cấu hình map `permissions`. Thay vì liệt kê danh sách subject được phép và queue tùy chọn, map `permission` cho phép khai báo tường minh những gì muốn `allow` hoặc `deny`. Có thể cung cấp cả hai danh sách; khi trùng nhau, `deny` được ưu tiên.

| Property | Description                                          |
| -------- | ---------------------------------------------------- |
| `allow`  | List of subject names that are allowed to the client |
| `deny`   | List of subjects that are denied to the client       |

> 🇬🇧 ***Important Note** It is important to not break request-reply patterns. In some cases (as shown [below](./authorization.md#variables)) you need to add rules for the `_INBOX.>` pattern. If an unauthorized client publishes or attempts to subscribe to a subject that has not been _allow listed_, the action fails and is logged at the server, and an error message is returned to the client. The [allow responses](./authorization.md#allow-responses-map) option can simplify this.*

**Lưu ý quan trọng:** Cần tránh phá vỡ các pattern request-reply. Trong một số trường hợp (như ví dụ [bên dưới](./authorization.md#variables)), cần thêm rule cho pattern `_INBOX.>`. Nếu client không được phân quyền publish hoặc cố subscribe vào subject chưa có trong danh sách cho phép, hành động sẽ thất bại, được ghi log tại server và trả về thông báo lỗi cho client. Tùy chọn [allow responses](./authorization.md#allow-responses-map) có thể đơn giản hóa việc này.

## Allow Responses Map

> 🇬🇧 *The `allow_responses` option dynamically allows publishing to reply subjects and is designed for [service](../../../nats-concepts/core-nats/request-reply/reqreply.md) responders. When set to `true`, an implicit _publish allow_ permission is enforced which enables the service to have temporary permission to publish to the `reply` subject during a request-reply exchange. If `true`, the client supports a one-time `publish`. If `allow_responses` is a map, it allows you to configure a maximum number of responses and how long the permission is valid.*

Tùy chọn `allow_responses` cho phép publish động đến reply subject, được thiết kế cho các [service](../../../nats-concepts/core-nats/request-reply/reqreply.md) phản hồi. Khi đặt thành `true`, một permission _publish allow_ ngầm định được áp dụng, cho phép service tạm thời publish đến subject `reply` trong quá trình trao đổi request-reply. Nếu `true`, client hỗ trợ một lần `publish` duy nhất. Nếu `allow_responses` là một map, có thể cấu hình số lượng response tối đa và thời gian permission có hiệu lực.

> 🇬🇧 *Note, when `allow_responses` is enabled, the reply subject is not constrained to the `publish` allow or deny list. The implication of this is that a reply subject can be provided by a client to a service (responder) that does not have permission to explicitly publish on that subject, but is temporarily allowed given this option. If explicit control over which subjects a client is allowed to reply to, do not use `allow_responses` and instead define allow/deny lists under the `publish` permission map.*

> **Nguy hiểm:** Khi `allow_responses` được bật, reply subject không bị ràng buộc bởi danh sách allow/deny của `publish`. Điều này có nghĩa là client có thể cung cấp reply subject cho một service (responder) vốn không có permission publish tường minh lên subject đó, nhưng được cho phép tạm thời nhờ tùy chọn này. Nếu cần kiểm soát chặt subject mà client được phép reply, không dùng `allow_responses` mà hãy định nghĩa danh sách allow/deny trong permission map `publish`.

| Property  | Description                                                                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `max`     | The maximum number of response messages that can be published.                                                                                                |
| `expires` | The amount of time the permission is valid. Values such as `1s`, `1m`, `1h` (1 second, minute, hour) etc can be specified. Default doesn't have a time limit. |

> 🇬🇧 *When `allow_responses` is set to `true`, it defaults to the equivalent of `{ max: 1 }` and no time limit.*

Khi `allow_responses` được đặt thành `true`, mặc định tương đương với `{ max: 1 }` và không giới hạn thời gian.

> 🇬🇧 ***Important Note** When using `nsc` to configure your users, you can specify the `--allow-pub-response` and `--response-ttl` to control these settings.*

**Lưu ý quan trọng:** Khi dùng `nsc` để cấu hình user, có thể chỉ định `--allow-pub-response` và `--response-ttl` để kiểm soát các thiết lập này.

## Ví Dụ

### Variables

> 🇬🇧 *Here is an example authorization configuration that uses _variables_ which defines four users, three of whom are assigned explicit permissions.*

Đây là ví dụ cấu hình authorization dùng _variables_, định nghĩa bốn user, trong đó ba user được gán permission tường minh.

```
authorization {
  default_permissions = {
    publish = "SANDBOX.*"
    subscribe = ["PUBLIC.>", "_INBOX.>"]
  }
  ADMIN = {
    publish = ">"
    subscribe = ">"
  }
  REQUESTOR = {
    publish = ["req.a", "req.b"]
    subscribe = "_INBOX.>"
  }
  RESPONDER = {
    subscribe = ["req.a", "req.b"]
    publish = "_INBOX.>"
  }
  users = [
    {user: admin,   password: $ADMIN_PASS, permissions: $ADMIN}
    {user: client,  password: $CLIENT_PASS, permissions: $REQUESTOR}
    {user: service,  password: $SERVICE_PASS, permissions: $RESPONDER}
    {user: other, password: $OTHER_PASS}
  ]
}
```

> 🇬🇧 *`default_permissions` is a special entry. If defined, it applies to all users that don't have specific permissions set.*

`default_permissions` là entry đặc biệt. Nếu được định nghĩa, nó áp dụng cho mọi user chưa có permission cụ thể.

> 🇬🇧 ** _admin_ has `ADMIN` permissions and can publish/subscribe on any subject. We use the wildcard `>` to match any subject.*
> 🇬🇧 ** _client_ is a `REQUESTOR` and can publish requests on subjects `req.a` or `req.b`, and subscribe to anything that is a response (`_INBOX.>`).*
> 🇬🇧 ** _service_ is a `RESPONDER` to `req.a` and `req.b` requests, so it needs to be able to subscribe to the request subjects and respond to clients that can publish requests to `req.a` and `req.b`. The reply subject is an inbox. Typically inboxes start with the prefix `_INBOX.` followed by a generated string. The `_INBOX.>` subject matches all subjects that begin with `_INBOX.`.*
> 🇬🇧 ** _other_ has no permissions granted and therefore inherits the default permission set.*

* _admin_ có permission `ADMIN` và có thể publish/subscribe trên mọi subject. Wildcard `>` khớp với bất kỳ subject nào.
* _client_ là `REQUESTOR` và có thể publish request lên subject `req.a` hoặc `req.b`, đồng thời subscribe nhận bất kỳ response nào (`_INBOX.>`).
* _service_ là `RESPONDER` để xử lý request `req.a` và `req.b`, nên cần subscribe vào các request subject và có thể reply lại cho client publish đến `req.a` và `req.b`. Reply subject là một inbox — thường bắt đầu bằng prefix `_INBOX.` theo sau là chuỗi được tạo ngẫu nhiên. Subject `_INBOX.>` khớp với mọi subject bắt đầu bằng `_INBOX.`.
* _other_ không được cấp permission nào và kế thừa bộ permission mặc định.

> 🇬🇧 *Note that in the above example, any client with permission to subscribe to `_INBOX.>` can receive _all_ responses published. More sensitive installations will want to add or subset the prefix to further limit subjects that a client can subscribe. Alternatively, [_Accounts_](./accounts.md) allow complete isolation limiting what members of an account can see.*

Lưu ý rằng trong ví dụ trên, bất kỳ client nào có permission subscribe vào `_INBOX.>` đều có thể nhận _tất cả_ response được publish. Với các hệ thống nhạy cảm hơn, nên thu hẹp hoặc bổ sung prefix để giới hạn subject mà client có thể subscribe. Ngoài ra, [_Accounts_](./accounts.md) cung cấp khả năng cô lập hoàn toàn, giới hạn những gì thành viên trong account có thể thấy.

### Allow/Deny Cụ Thể

> 🇬🇧 *Here's an example without variables, where the `allow` and `deny` options are specified:*

Ví dụ không dùng variables, trong đó chỉ định tường minh các tùy chọn `allow` và `deny`:

```
authorization: {
    users = [
        {
            user: admin
            password: secret
            permissions: {
                publish: ">"
                subscribe: ">"
            }
        }
        {
            user: test
            password: test
            permissions: {
                publish: {
                    deny: ">"
                },
                subscribe: {
                    allow: "client.>"
                }
            }
        }
    ]
}
```

### allow\_responses

> 🇬🇧 *Here's an example with `allow_responses`:*

Ví dụ sử dụng `allow_responses`:

```
authorization: {
    users: [
        { user: a, password: a },
        { user: b, password: b, permissions: {subscribe: "q", allow_responses: true } },
        { user: c, password: c, permissions: {subscribe: "q", allow_responses: { max: 5, expires: "1m" } } }
        { user: d, password: d, permissions: {subscribe: "q", publish: "x", allow_responses: true } }
    ]
}
```

> 🇬🇧 ** User `a` has no restrictions.*
> 🇬🇧 ** User `b` can listen on `q` for requests and can only publish once to reply subjects. _All other publish subjects are denied implicitly when `allow_responses` is set._*
> 🇬🇧 ** User `c` can listen on `q` for requests, but is able to return at most 5 reply messages, and the reply subject can be published at most for `1` minute.*
> 🇬🇧 ** User `d` has the same behavior as user `b`, except that it can explicitly publish to subject `x` as well, which overrides the implicit deny from `allow_responses`.*

* User `a` không có giới hạn nào.
* User `b` có thể lắng nghe request trên `q` và chỉ được publish một lần đến reply subject. _Tất cả publish subject khác đều bị từ chối ngầm định khi bật `allow_responses`._
* User `c` có thể lắng nghe request trên `q`, nhưng chỉ được trả tối đa 5 reply message, và reply subject chỉ được publish trong tối đa `1` phút.
* User `d` có hành vi giống user `b`, ngoại trừ việc có thể publish tường minh đến subject `x`, điều này ghi đè lệnh từ chối ngầm định từ `allow_responses`.

### Queue Permissions

> 🇬🇧 *User `a` can only subscribe to `foo` as part of the queue subscriptions `queue`. User `b` has permissions for queue subscriptions as well as plain subscriptions. You can allow plain subscriptions on `foo` but constrain the queues to which a client can join, as well as preventing any service from using a queue subscription with the name `*.prod`:*

User `a` chỉ có thể subscribe vào `foo` trong phạm vi queue group (nhóm subscribers chia sẻ tải) `queue`. User `b` có permission cho cả queue subscription lẫn plain subscription. Có thể cho phép plain subscription trên `foo` nhưng giới hạn queue mà client được tham gia, đồng thời ngăn bất kỳ service nào dùng queue subscription với tên `*.prod`:

```
users = [
  {
    user: "a", password: "a", permissions: {
      sub: {
        allow: ["foo queue"]
     }
  }
  {
    user: "b", password: "b", permissions: {
      sub: {
        # Allow plain subscription foo, but only v1 groups or *.dev queue groups
        allow: ["foo", "foo v1", "foo v1.>", "foo *.dev"]

        # Prevent queue subscriptions on prod groups
        deny: ["> *.prod"]
     }
  }
]
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **config**: cấu hình
- **permission**: quyền truy cập
- **publisher**: bên gửi message
- **queue group**: nhóm subscribers chia sẻ tải
- **request**: yêu cầu
- **response**: phản hồi
- **service**: dịch vụ
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message