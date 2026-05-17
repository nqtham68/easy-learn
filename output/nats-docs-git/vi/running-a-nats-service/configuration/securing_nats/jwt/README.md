---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/jwt
title: Xác thực/Phân quyền JWT Phi tập trung
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Xác thực/Phân quyền JWT Phi tập trung

> 🇬🇧 *With other authentication mechanisms, configuration for identifying a user and [Account](../accounts.md), is in the server configuration file. JWT authentication leverages [JSON Web Tokens \(JWT\)](https://jwt.io/) to describe the various entities supported. When a client connects, servers verify the authenticity of the request using [NKeys](../auth_intro/nkey_auth.md), download account information and validate a trust chain. Users are not directly tracked by the server, but rather verified as and belonging to an [Account](../accounts.md). This enables the management of users, without requiring server configuration updates.*

Với các cơ chế xác thực khác, cấu hình để nhận diện người dùng và [Account](../accounts.md) nằm trong file config của server. Xác thực JWT tận dụng [JSON Web Tokens \(JWT\)](https://jwt.io/) — tức là token (chuỗi xác thực) — để mô tả các thực thể được hỗ trợ. Khi client kết nối, server xác minh tính hợp lệ của request bằng [NKeys](../auth_intro/nkey_auth.md), tải thông tin account và kiểm tra chuỗi tin cậy (trust chain). Người dùng không bị server theo dõi trực tiếp mà được xác minh là thành viên của một [Account](../accounts.md). Điều này cho phép quản lý người dùng mà không cần cập nhật config server.

> 🇬🇧 *Effectively, JWTs improve accounts and provide for a **distributed configuration paradigm**. Previously each user \(or client\) needed to be known and authorized a priori in the server's configuration requiring an administrator to modify and update server configurations. These chores are eliminated. User creation can even be performed by different entities altogether.*

JWT cải thiện accounts và mang lại một **mô hình cấu hình phân tán**. Trước đây, mỗi người dùng (hay client) phải được khai báo và cấp quyền trước trong config server, buộc quản trị viên phải liên tục sửa và cập nhật cấu hình. JWT loại bỏ hoàn toàn gánh nặng này. Thậm chí việc tạo người dùng có thể do các tổ chức hoàn toàn khác nhau thực hiện.

> 🇬🇧 *Note: This scheme improves [accounts](../accounts.md). Functionalities like [isolation](../accounts.md) or defining [exports/imports](../accounts.md#exporting-and-importing) between accounts remain! It moves configuration of accounts, exports/imports or users and their permissions away from the server into several trusted [JSON Web Token \(JWT\)](https://jwt.io/) that are managed separately, therefore removing the need to configure these entities in each and every server. It furthermore adds functionalities like expiration and revocation fore decentralized account management*

> Lưu ý: Mô hình này cải thiện [accounts](../accounts.md). Các tính năng như [isolation](../accounts.md) hay định nghĩa [exports/imports](../accounts.md#exporting-and-importing) giữa các account vẫn còn nguyên! Mô hình này chuyển việc cấu hình accounts, exports/imports, người dùng và permission (quyền truy cập) của họ ra khỏi server vào các [JSON Web Token \(JWT\)](https://jwt.io/) đáng tin cậy được quản lý riêng biệt, do đó không cần cấu hình các thực thể này trên từng server. Ngoài ra còn bổ sung tính năng hết hạn và thu hồi quyền cho việc quản lý account phi tập trung.

## JSON Web Tokens

> 🇬🇧 *[JSON Web Tokens \(JWT\)](https://jwt.io/) are an open and industry standard [RFC7519](https://tools.ietf.org/html/rfc7519) method for representing claims securely between two parties.*

[JSON Web Tokens \(JWT\)](https://jwt.io/) là phương thức mở và chuẩn công nghiệp [RFC7519](https://tools.ietf.org/html/rfc7519) để biểu diễn các claim một cách an toàn giữa hai bên.

> 🇬🇧 *Claims are a fancy way of asserting information on a _subject_. In this context, a _subject_ is the entity being described \(not a messaging subject\). Standard JWT claims are typically digitally signed and verified.*

Claim là cách khai báo thông tin về một _subject_ (chuỗi định danh message). Trong ngữ cảnh này, _subject_ là thực thể được mô tả (không phải subject nhắn tin). Các claim JWT tiêu chuẩn thường được ký số và xác minh.

> 🇬🇧 *NATS further restricts JWTs by requiring that JWTs be:*
>
> * *Digitally signed _always_ and only using [Ed25519](https://ed25519.cr.yp.to/).*
> * *NATS adopts the convention that all _Issuer_ and _Subject_ fields in a JWT claim must be a public [NKEY](../auth_intro/nkey_auth.md).*
> * *_Issuer_ and _Subject_ must match specific roles depending on the claim [NKeys](https://github.com/nats-io/nkeys).*

NATS áp đặt thêm các ràng buộc với JWT:

* Luôn ký số, chỉ dùng [Ed25519](https://ed25519.cr.yp.to/).
* Tất cả các trường _Issuer_ và _Subject_ trong JWT claim phải là public [NKEY](../auth_intro/nkey_auth.md).
* _Issuer_ và _Subject_ phải khớp với các role cụ thể tùy theo claim [NKeys](https://github.com/nats-io/nkeys).

### Các Role NKey

> 🇬🇧 *[NKeys](../auth_intro/nkey_auth.md) Roles are:*
>
> * *Operators*
> * *Accounts*
> * *Users*

Các role của [NKeys](../auth_intro/nkey_auth.md) gồm:

* Operators
* Accounts
* Users

> 🇬🇧 *Roles are hierarchical and form a chain of trust. Operators issue Accounts which in turn issue Users. Servers trust specific Operators. If an account is issued by an operator that is trusted, account users are trusted.*

Các role có thứ bậc và tạo thành chuỗi tin cậy. Operators cấp phát Accounts, Accounts lại cấp phát Users. Server tin tưởng các Operator cụ thể. Nếu một account được cấp bởi operator đáng tin, người dùng trong account đó cũng được tin tưởng.

## Quá trình Xác thực

> 🇬🇧 *When a _User_ connects to a server, it presents a JWT issued by its _Account_. The user proves its identity by signing a server-issued cryptographic challenge with its private key. The signature verification validates that the signature is attributable to the user's public key. Next, the server retrieves the associated account JWT that issued the user. It verifies the _User_ issuer matches the referenced account. Finally, the server checks that a trusted _Operator_ - one the server is configured with - issued the _Account_, completing the trust chain verification.*

Khi _User_ kết nối tới server, nó trình một JWT do _Account_ của mình cấp. Người dùng chứng minh danh tính bằng cách ký một thử thách mật mã do server phát hành bằng private key của mình. Xác minh chữ ký xác nhận chữ ký đó thuộc về public key của người dùng. Tiếp theo, server lấy account JWT đã cấp cho người dùng và kiểm tra _User_ issuer khớp với account được tham chiếu. Cuối cùng, server kiểm tra một _Operator_ đáng tin — operator đã được cấu hình trong server — đã cấp _Account_ đó, hoàn tất quá trình xác minh chuỗi tin cậy.

## Quá trình Phân quyền

> 🇬🇧 *From an authorization point of view, the account provides information on messaging subjects that are imported from other accounts \(including any ancillary related authorization\) as well as messaging subjects exported to other accounts. Accounts can also bear limits, such as the maximum number of connections they may have. A user JWT can express restrictions on the messaging subjects to which it can publish or subscribe.*

Về mặt phân quyền, account cung cấp thông tin về các subject nhắn tin được import từ account khác (kèm các quyền liên quan) cũng như các subject được export cho account khác. Account cũng có thể mang các giới hạn, ví dụ số kết nối tối đa. Một user JWT có thể biểu đạt các giới hạn về subject mà người dùng được phép publish hoặc subscribe.

> 🇬🇧 *When a new user is added to an account, the account configuration need not change, as each user can and should have its own user JWT that can be verified by simply resolving its parent account.*

Khi thêm người dùng mới vào account, cấu hình account không cần thay đổi vì mỗi người dùng có và nên có user JWT riêng, có thể xác minh chỉ bằng cách truy xuất account cha.

## JWT và Quyền riêng tư

> 🇬🇧 *One crucial detail to keep in mind is that while in other systems JWTs are used as sessions or proof of authentication, NATS JWTs are only used as configuration describing:*
>
> * *the public ID of the entity*
> * *the public ID of the entity that issued it*
> * *capabilities of the entity*

Một điểm quan trọng cần lưu ý: trong các hệ thống khác, JWT được dùng như session hoặc bằng chứng xác thực, nhưng NATS JWT chỉ được dùng như cấu hình mô tả:

* ID công khai của thực thể
* ID công khai của thực thể đã cấp phát nó
* Khả năng (capabilities) của thực thể

> 🇬🇧 *Authentication is a public key cryptographic process — a client signs a nonce proving identity while the trust chain and configuration provides the authorization.*

Xác thực là quá trình mật mã khóa công khai — client ký một nonce để chứng minh danh tính, trong khi chuỗi tin cậy và cấu hình cung cấp phân quyền.

> 🇬🇧 *The server is never aware of private keys but can verify that a signer or issuer indeed matches a specified or known public key.*

Server không bao giờ biết private key nhưng có thể xác minh rằng signer hay issuer thực sự khớp với public key đã được chỉ định hoặc biết trước.

> 🇬🇧 *Lastly, all NATS JWTs \(Operators, Accounts, Users and others\) are expected to be signed using the [Ed25519](https://ed25519.cr.yp.to/) algorithm. If they are not, they are rejected by the system.*

Cuối cùng, tất cả NATS JWT (Operators, Accounts, Users và các loại khác) đều phải được ký bằng thuật toán [Ed25519](https://ed25519.cr.yp.to/). Nếu không, hệ thống sẽ từ chối chúng.

## Xác thực và Phân quyền Phi tập trung - Cấu hình và nsc

> 🇬🇧 *There is very little to configure on the nats-server to enable operator JWT security, once the servers have been initially configured the authentication and authorization tasks are typically done by using the `nsc` administration tool locally and synchronizing with the account resolvers built into the nats-server.*

Cần rất ít cấu hình trên nats-server để bật bảo mật operator JWT. Sau khi server được cấu hình ban đầu, các tác vụ xác thực và phân quyền thường được thực hiện bằng công cụ quản trị `nsc` cục bộ và đồng bộ với các account resolver tích hợp trong nats-server.

> 🇬🇧 *Configuration is broken up into separate steps. Depending on organizational needs these are performed by the same or different entities.*

Cấu hình được chia thành các bước riêng biệt. Tùy nhu cầu tổ chức, các bước này có thể do cùng một hoặc các thực thể khác nhau thực hiện.

> 🇬🇧 *Practically, JWT configuration is done using the [`nsc` tool](../../../../using-nats/nats-tools/nsc). It can be set up to issue [NKeys](../auth_intro/nkey_auth.md) and corresponding JWTs for all [nkey roles](#nkey-roles): Operator/Account/User \([Example usage](../../../../using-nats/nats-tools/nsc/basics.md#creating-an-operator-account-and-user)\). Despite Account and User creation not happening in server configuration, this model is a centralized authentication and authorization setup.*

Trong thực tế, cấu hình JWT được thực hiện bằng [công cụ `nsc`](../../../../using-nats/nats-tools/nsc). Công cụ này có thể cấp [NKeys](../auth_intro/nkey_auth.md) và JWT tương ứng cho tất cả [nkey roles](#nkey-roles): Operator/Account/User ([Ví dụ sử dụng](../../../../using-nats/nats-tools/nsc/basics.md#creating-an-operator-account-and-user)). Mặc dù Account và User không được tạo trong config server, mô hình này vẫn là một thiết lập xác thực và phân quyền tập trung.

> 🇬🇧 *Provided institutional trust, it is also possible to use nsc to import account or user public [NKeys](../auth_intro/nkey_auth.md) and issue corresponding JWTs. This way an operator can issue account JWTs and a separate entity can issue JWTs for user associated with it's account. Neither entity has to be aware of the other's private Nkey. This not only allows users to be configured some place other than servers, but also by different organizations altogether. Say administrators of a NATS installation controlling operators, issuing account JWTs to individual prod/dev teams managing their own user. This is a fully decentralized authorization setup!*

Với sự tin cậy tổ chức, nsc cũng có thể import public NKeys của account hoặc user và cấp JWT tương ứng. Nhờ đó, một operator có thể cấp account JWT trong khi một thực thể khác cấp JWT cho user thuộc account của mình. Hai bên không cần biết private Nkey của nhau. Điều này không chỉ cho phép cấu hình người dùng ngoài server, mà còn cho phép các tổ chức hoàn toàn khác nhau thực hiện. Ví dụ: quản trị viên cài đặt NATS kiểm soát operator, cấp account JWT cho từng nhóm prod/dev để họ tự quản lý user. Đây là một thiết lập phân quyền hoàn toàn phi tập trung!

> 🇬🇧 *With an Operator JWT in place, the server needs to be configured to trust it by specifying `operator`. Furthermore the server needs a way to obtain account JWTs. This done by either defaulting to the resolver specified in the operator jwt or by manually specifying the [resolver](./resolver.md). Depending on your configuration an [account server](../../../../using-nats/nats-tools/nsc/basics.md#account-server-configuration) needs to be in place*

Khi đã có Operator JWT, server cần được cấu hình để tin tưởng nó bằng cách chỉ định `operator`. Ngoài ra, server cần cách lấy account JWT — có thể dùng resolver mặc định trong operator JWT hoặc chỉ định thủ công [resolver](./resolver.md). Tùy cấu hình, có thể cần một [account server](../../../../using-nats/nats-tools/nsc/basics.md#account-server-configuration).

> It is possible to [mix](./jwt_nkey_auth.md) JWT and [NKEY](../auth_intro/nkey_auth.md)/[Account](../accounts.md) based Authentication/Authorization.

> Có thể [kết hợp](./jwt_nkey_auth.md) xác thực/phân quyền dựa trên JWT và [NKEY](../auth_intro/nkey_auth.md)/[Account](../accounts.md).

# Quản lý xác thực JWT

> 🇬🇧 *A lot more information is available in the [In Depth Guide](../../../nats_admin/jwt.md).*

Có nhiều thông tin chi tiết hơn trong [Hướng dẫn chuyên sâu](../../../nats_admin/jwt.md).

## Thuật ngữ trong bài

- **credential**: thông tin đăng nhập
- **permission**: quyền truy cập
- **scope**: phạm vi quyền
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)
- **token**: chuỗi xác thực