---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nsc/signing_keys
title: Signing Keys
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Signing Keys

> 🇬🇧 *As previously discussed, NKEYs are identities, and if someone gets a hold of an account or operator nkey they can do everything you can do as you.*

Như đã đề cập, NKEY là định danh — nếu ai đó lấy được account hoặc operator nkey của bạn, họ có thể làm mọi thứ với quyền hạn của bạn.

> 🇬🇧 *NATS has strategies to let you deal with scenarios where your private keys escape out in the wild.*

NATS cung cấp các chiến lược để xử lý tình huống private key bị lộ.

> 🇬🇧 *The first and most important line of defense is _Signing Keys_. _Signing Keys_ allow you have multiple NKEY identities of the same kind \(Operator or Account\) that have the same degree of trust as the standard _Issuer_ nkey.*

Tuyến phòng thủ đầu tiên và quan trọng nhất là _Signing Keys_. Signing Keys cho phép bạn có nhiều NKEY identity cùng loại (Operator hoặc Account) với mức độ tin cậy tương đương nkey _Issuer_ tiêu chuẩn.

> 🇬🇧 *The concept behind the signing key is that you can issue a JWT for an operator or an account that lists multiple nkeys. Typically the issuer will match the _Subject_ of the entity issuing the JWT. With SigningKeys, a JWT is considered valid if it is signed by the _Subject_ of the _Issuer_ or one of its signing keys. This enables guarding the private key of the Operator or Account more closely while allowing _Accounts_, _Users_ or _Activation Tokens_ be signed using alternate private keys.*

Ý tưởng đằng sau signing key là bạn có thể phát hành một JWT cho operator hoặc account, trong đó liệt kê nhiều nkey. Thông thường, issuer sẽ khớp với _Subject_ (chuỗi định danh message) của entity phát hành JWT. Với SigningKeys, một JWT được coi là hợp lệ nếu được ký bởi _Subject_ của _Issuer_ hoặc một trong các signing key của nó. Điều này giúp bảo vệ chặt chẽ hơn private key của Operator hoặc Account, đồng thời cho phép _Accounts_, _Users_ hoặc _Activation Tokens_ được ký bằng các private key thay thế.

> 🇬🇧 *If an issue should arise where somehow a signing key escapes into the wild, you would remove the compromised signing key from the entity, add a new one, and reissue the entity. When a JWT is validated, if the signing key is missing, the operation is rejected. You are also on the hook to re-issue all JWTs \(accounts, users, activation tokens\) that were signed with the compromised signing key.*

Khi một signing key bị lộ, bạn cần xóa signing key đó khỏi entity, thêm một key mới, và phát hành lại entity. Khi JWT được xác thực, nếu signing key không tồn tại thì thao tác bị từ chối. Bạn cũng phải phát hành lại tất cả JWT (accounts, users, activation tokens) đã được ký bằng signing key bị lộ.

> 🇬🇧 *This is effectively a large hammer. You can mitigate the process a bit by having a larger number of signing keys and then rotating the signing keys to get a distribution you can easily handle in case of a compromise. In a future release, we'll have a revocation process were you can invalidate a single JWT by its unique JWT ID \(JTI\). For now a sledge hammer you have.*

Đây thực chất là một biện pháp khá nặng tay. Bạn có thể giảm thiểu tác động bằng cách dùng nhiều signing key và luân chuyển chúng để dễ xử lý khi có sự cố. Trong phiên bản tương lai sẽ có cơ chế revocation cho phép vô hiệu hóa từng JWT riêng lẻ thông qua JWT ID (JTI) duy nhất của nó. Hiện tại, đây vẫn là cách duy nhất.

> 🇬🇧 *With greater security process, there's greater complexity. With that said, `nsc` doesn't track public or private signing keys. As these are only identities that when in use presume a manual use. That means that you the user will have to track and manage your private keys more closely.*

Bảo mật cao hơn đồng nghĩa với phức tạp hơn. Cần lưu ý rằng `nsc` không theo dõi public hay private signing key vì đây chỉ là các identity được sử dụng thủ công. Điều đó có nghĩa là bạn phải tự quản lý và theo dõi các private key của mình chặt chẽ hơn.

> 🇬🇧 *Let's get a feel for the workflow. We are going to:*
> 🇬🇧 *- Create an operator with a signing key*
> 🇬🇧 *- Create an account with a signing key*
> 🇬🇧 *- The account will be signed using the operator's signing key*
> 🇬🇧 *- Create an user with the account's signing key*

Hãy làm quen với workflow. Chúng ta sẽ:

* Tạo operator với một signing key
* Tạo account với một signing key
* Account sẽ được ký bằng signing key của operator
* Tạo user với signing key của account

> 🇬🇧 *All signing key operations revolve around the global `nsc` flag `-K` or `--private-key`. Whenever you want to modify an entity, you have to supply the parent key so that the JWT is signed. Normally this happens automatically but in the case of signing keys, you'll have to supply the flag by hand.*

Mọi thao tác liên quan đến signing key đều xoay quanh flag toàn cục `nsc` là `-K` hoặc `--private-key`. Mỗi khi muốn chỉnh sửa một entity, bạn phải cung cấp parent key để JWT được ký. Thông thường việc này diễn ra tự động, nhưng với signing key bạn phải cung cấp flag thủ công.

Tạo operator:

```shell
nsc add operator O2
```
```
[ OK ] generated and stored operator key "OABX3STBZZRBHMWMIMVHNQVNUG2O3D54BMZXX5LMBYKSAPDSHIWPMMFY"
[ OK ] added operator "O2"
```

> 🇬🇧 *To add a signing key we have to first generate one with `nsc`:*

Để thêm một signing key, trước tiên phải tạo một key bằng `nsc`:

```shell
nsc generate nkey --operator --store
```

```
SOAEW6Z4HCCGSLZJYZQMGFQY2SY6ZKOPIAKUQ5VZY6CW23WWYRNHTQWVOA
OAZBRNE7DQGDYT5CSAGWDMI5ENGKOEJ57BXVU6WUTHFEAO3CU5GLQYF5
operator key stored ~/.nkeys/keys/O/AZ/OAZBRNE7DQGDYT5CSAGWDMI5ENGKOEJ57BXVU6WUTHFEAO3CU5GLQYF5.nk
```

> 🇬🇧 *On a production environment private keys should be saved to a file and always referenced from the secured file.*

> Trên môi trường production, private key nên được lưu vào file và luôn tham chiếu từ file được bảo mật đó.

> 🇬🇧 *Now we are going to edit the operator by adding a signing key with the `--sk` flag providing the generated operator public key \(the one starting with `O`\):*

Tiếp theo, chỉnh sửa operator bằng cách thêm signing key với flag `--sk`, cung cấp public key của operator vừa tạo (key bắt đầu bằng `O`):

```shell
nsc edit operator --sk OAZBRNE7DQGDYT5CSAGWDMI5ENGKOEJ57BXVU6WUTHFEAO3CU5GLQYF5
```

```
[ OK ] added signing key "OAZBRNE7DQGDYT5CSAGWDMI5ENGKOEJ57BXVU6WUTHFEAO3CU5GLQYF5"
[ OK ] edited operator "O2"
```

> 🇬🇧 *Check our handy work:*

Kiểm tra kết quả:

```shell
nsc describe operator
```

```
╭─────────────────────────────────────────────────────────────────────────╮
│                            Operator Details                             │
├──────────────┬──────────────────────────────────────────────────────────┤
│ Name         │ O2                                                       │
│ Operator ID  │ OABX3STBZZRBHMWMIMVHNQVNUG2O3D54BMZXX5LMBYKSAPDSHIWPMMFY │
│ Issuer ID    │ OABX3STBZZRBHMWMIMVHNQVNUG2O3D54BMZXX5LMBYKSAPDSHIWPMMFY │
│ Issued       │ 2019-12-05 14:36:16 UTC                                  │
│ Expires      │                                                          │
├──────────────┼──────────────────────────────────────────────────────────┤
│ Signing Keys │ OAZBRNE7DQGDYT5CSAGWDMI5ENGKOEJ57BXVU6WUTHFEAO3CU5GLQYF5 │
╰──────────────┴──────────────────────────────────────────────────────────╯
```

> 🇬🇧 *Now let's create an account called `A` and sign it with the generated operator private signing key. To sign it with the key specify the `-K` flag and the private key or a path to the private key:*

Tạo một account tên `A` và ký bằng private signing key của operator. Để ký với key đó, chỉ định flag `-K` cùng với private key hoặc đường dẫn đến file chứa private key:

```shell
nsc add account A -K ~/.nkeys/keys/O/AZ/OAZBRNE7DQGDYT5CSAGWDMI5ENGKOEJ57BXVU6WUTHFEAO3CU5GLQYF5.nk
```

```
[ OK ] generated and stored account key "ACDXQQ6KD5MVSFMK7GNF5ARK3OJC6PEICWCH5PQ7HO27VKGCXQHFE33B"
[ OK ] added account "A"
```

> 🇬🇧 *Let's generate an account signing key, again we use `nk`:*

Tạo signing key cho account, lại dùng `nk`:

```bash
nsc generate nkey --account --store
```

```
SAAA4BVFTJMBOW3GAYB3STG3VWFSR4TP4QJKG2OCECGA26SKONPFGC4HHE
ADUQTJD4TF4O6LTTHCKDKSHKGBN2NECCHHMWFREPKNO6MPA7ZETFEEF7
account key stored ~/.nkeys/keys/A/DU/ADUQTJD4TF4O6LTTHCKDKSHKGBN2NECCHHMWFREPKNO6MPA7ZETFEEF7.nk
```

> 🇬🇧 *Let's add the signing key to the account, and remember to sign the account with the operator signing key:*

Thêm signing key vào account — nhớ ký account bằng signing key của operator:

```shell
nsc edit account --sk ADUQTJD4TF4O6LTTHCKDKSHKGBN2NECCHHMWFREPKNO6MPA7ZETFEEF7 -K ~/.nkeys/keys/O/AZ/OAZBRNE7DQGDYT5CSAGWDMI5ENGKOEJ57BXVU6WUTHFEAO3CU5GLQYF5.nk
```

```
[ OK ] added signing key "ADUQTJD4TF4O6LTTHCKDKSHKGBN2NECCHHMWFREPKNO6MPA7ZETFEEF7"
[ OK ] edited account "A"
```

> 🇬🇧 *Let's take a look at the account*

Xem thông tin account:

```shell
nsc describe account
```

```
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                   Account Details                                    │
├───────────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                      │ A                                                        │
│ Account ID                │ ACDXQQ6KD5MVSFMK7GNF5ARK3OJC6PEICWCH5PQ7HO27VKGCXQHFE33B │
│ Issuer ID                 │ OAZBRNE7DQGDYT5CSAGWDMI5ENGKOEJ57BXVU6WUTHFEAO3CU5GLQYF5 │
│ Issued                    │ 2019-12-05 14:48:22 UTC                                  │
│ Expires                   │                                                          │
├───────────────────────────┼──────────────────────────────────────────────────────────┤
│ Signing Keys              │ ADUQTJD4TF4O6LTTHCKDKSHKGBN2NECCHHMWFREPKNO6MPA7ZETFEEF7 │
├───────────────────────────┼──────────────────────────────────────────────────────────┤
│ Max Connections           │ Unlimited                                                │
│ Max Leaf Node Connections │ Unlimited                                                │
│ Max Data                  │ Unlimited                                                │
│ Max Exports               │ Unlimited                                                │
│ Max Imports               │ Unlimited                                                │
│ Max Msg Payload           │ Unlimited                                                │
│ Max Subscriptions         │ Unlimited                                                │
│ Exports Allows Wildcards  │ True                                                     │
├───────────────────────────┼──────────────────────────────────────────────────────────┤
│ Imports                   │ None                                                     │
│ Exports                   │ None                                                     │
╰───────────────────────────┴──────────────────────────────────────────────────────────╯
```

> 🇬🇧 *We can see that the signing key `ADUQTJD4TF4O6LTTHCKDKSHKGBN2NECCHHMWFREPKNO6MPA7ZETFEEF7` was added to the account. Also the issuer is the operator signing key \(specified by the `-K`\).*

Có thể thấy signing key `ADUQTJD4TF4O6LTTHCKDKSHKGBN2NECCHHMWFREPKNO6MPA7ZETFEEF7` đã được thêm vào account. Issuer cũng là operator signing key (được chỉ định bởi `-K`).

> 🇬🇧 *Now let's create a user and sign it with the account signing key starting with `ADUQTJD4TF4O`.*

Tạo user và ký bằng account signing key bắt đầu bằng `ADUQTJD4TF4O`:

```shell
nsc add user U -K ~/.nkeys/keys/A/DU/ADUQTJD4TF4O6LTTHCKDKSHKGBN2NECCHHMWFREPKNO6MPA7ZETFEEF7.nk
```

```
[ OK ] generated and stored user key "UD47TOTKVDY4IQRGI6D7XMLZPHZVNV5FCD4CNQICLV3FXLQBY72A4UXL"
[ OK ] generated user creds file "~/.nkeys/creds/O2/A/U.creds"
[ OK ] added user "U" to account "A"
```

> 🇬🇧 *Check the user*

Kiểm tra user:

```shell
nsc describe user
```

```
╭─────────────────────────────────────────────────────────────────────────────────╮
│                                      User                                       │
├──────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                 │ U                                                        │
│ User ID              │ UD47TOTKVDY4IQRGI6D7XMLZPHZVNV5FCD4CNQICLV3FXLQBY72A4UXL │
│ Issuer ID            │ ADUQTJD4TF4O6LTTHCKDKSHKGBN2NECCHHMWFREPKNO6MPA7ZETFEEF7 │
│ Issuer Account       │ ACDXQQ6KD5MVSFMK7GNF5ARK3OJC6PEICWCH5PQ7HO27VKGCXQHFE33B │
│ Issued               │ 2019-12-05 14:50:07 UTC                                  │
│ Expires              │                                                          │
├──────────────────────┼──────────────────────────────────────────────────────────┤
│ Response Permissions │ Not Set                                                  │
├──────────────────────┼──────────────────────────────────────────────────────────┤
│ Max Messages         │ Unlimited                                                │
│ Max Msg Payload      │ Unlimited                                                │
│ Network Src          │ Any                                                      │
│ Time                 │ Any                                                      │
╰──────────────────────┴──────────────────────────────────────────────────────────╯
```

> 🇬🇧 *As expected, the issuer is now the signing key we generated earlier. To map the user to the actual account, an `Issuer Account` field was added to the JWT that identifies the public key of account _A_.*

Như mong đợi, issuer giờ là signing key đã tạo trước đó. Để ánh xạ user về account thực sự, một trường `Issuer Account` được thêm vào JWT, xác định public key của account _A_.

## Scoped Signing Keys

> 🇬🇧 *Scoped Signing Keys simplify user permission management. Previously if you wanted to limit the permissions of users, you had to specify permissions on a per-user basis. With scoped signing keys, you associate a signing key with a set of permissions. This configuration lives on the account JWT and is managed with the `nsc edit signing-key` command. You can add as many scoped signing keys as necessary.*

Scoped Signing Keys đơn giản hóa việc quản lý permission (quyền truy cập) của user. Trước đây, nếu muốn giới hạn permission của user, bạn phải chỉ định từng user riêng lẻ. Với scoped signing keys, bạn gắn một signing key với một tập permission cụ thể. Cấu hình này nằm trong account JWT và được quản lý bằng lệnh `nsc edit signing-key`. Bạn có thể thêm bao nhiêu scoped signing key tùy ý.

> 🇬🇧 *To issue a user with a set of permissions, simply sign the user with the signing key having the permission set you want. The user configuration must _not_ have any permissions assigned to it.*

Để cấp một tập permission cho user, chỉ cần ký user bằng signing key chứa tập permission mong muốn. Cấu hình của user đó _không_ được có bất kỳ permission nào được gán trực tiếp.

> 🇬🇧 *On connect, the nats-server will assign the permissions associated with that signing key to the user. If you update the permissions associated with a signing key, the server will immediately update permissions for users signed with that key.*

Khi kết nối, nats-server sẽ gán các permission liên kết với signing key đó cho user. Nếu bạn cập nhật permission của một signing key, server sẽ lập tức cập nhật permission cho tất cả user đã được ký bằng key đó.

```shell
nsc add account A
```

```
[ OK ] generated and stored account key "ADLGEVANYDKDQ6WYXPNBEGVUURXZY4LLLK5BJPOUDN6NGNXLNH4ATPWR"
[ OK ] push jwt to account server:
       [ OK ] pushed account jwt to the account server
       > NGS created a new free billing account for your JWT, A [ADLGEVANYDKD].
       > Use the 'ngs' command to manage your billing plan.
       > If your account JWT is *not* in ~/.nsc, use the -d flag on ngs commands to locate it.
[ OK ] pull jwt from account server
[ OK ] added account "A"
```

> 🇬🇧 *Generate the signing key*

Tạo signing key:

```shell
nsc edit account -n A --sk generate
```

```
[ OK ] added signing key "AAZQXKDPOTGUCOCOGDW7HWWVR5WEGF3KYL7EKOEHW2XWRS2PT5AOTRH3"
[ OK ] push jwt to account server
[ OK ] pull jwt from account server
[ OK ] account server modifications:
       > allow wildcard exports changed from true to false
[ OK ] edited account "A"
```

> 🇬🇧 *Add a service to the account*

Thêm service vào account:

```shell
nsc edit signing-key --account A --role service --sk AAZQXKDPOTGUCOCOGDW7HWWVR5WEGF3KYL7EKOEHW2XWRS2PT5AOTRH3 --allow-sub "q.>" --deny-pub ">" --allow-pub-response
```

```
[ OK ] set max responses to 1
[ OK ] added deny pub ">"
[ OK ] added sub "q.>"
[ OK ] push jwt to account server
[ OK ] pull jwt from account server
[ OK ] edited signing key "AAZQXKDPOTGUCOCOGDW7HWWVR5WEGF3KYL7EKOEHW2XWRS2PT5AOTRH3"
```

> 🇬🇧 *Since the signing key has a unique role name within an account, it can be subsequently used for easier referencing.*

Vì signing key có tên role duy nhất trong account, nó có thể được dùng để tham chiếu dễ dàng hơn sau này.

```shell
nsc add user U -K service
```

```
[ OK ] generated and stored user key "UBFRJ6RNBYJWSVFBS7O4ZW5MM6J3EPE75II3ULPVUWOUH7K7A23D3RQE"
[ OK ] generated user creds file `~/test/issue-2621/keys/creds/synadia/A/U.creds`
[ OK ] added user "U" to account "A"
```

> 🇬🇧 *To see the permissions for the user enter `nsc describe user` - you will see in the report that the user is scoped, and has the permissions listed. You can inspect and modify the scoped permissions with `nsc edit signing-key` - pushing updates to the account will reassign user permissions.*

Để xem permission của user, dùng `nsc describe user` — trong báo cáo bạn sẽ thấy user đang được scoped và danh sách permission tương ứng. Có thể kiểm tra và chỉnh sửa scoped permission với `nsc edit signing-key` — đẩy cập nhật lên account sẽ gán lại permission cho user.

### Template functions

> 🇬🇧 *Available as of NATS 2.9.0*

*Có sẵn từ NATS 2.9.0*

> 🇬🇧 *Although scoped signing keys are very useful and improve security, by limiting the scope of a particular signing key, the permissions that are set may be too rigid in multi-user setups. For example, given two users `pam` and `joe`, we may want to allow them to subscribe to their own namespaced subject in order to service requests, e.g. `pam.>` and `joe.>`. The permission _structure_ is the same between these users, but they differ in the concrete subjects which are further scoped to some property about that user.*

Mặc dù scoped signing keys rất hữu ích và tăng cường bảo mật, việc giới hạn phạm vi của một signing key cụ thể có thể khiến permission trở nên quá cứng nhắc trong các môi trường nhiều user. Ví dụ, với hai user `pam` và `joe`, ta muốn cho phép họ subscribe vào subject (chuỗi định danh message) có namespace riêng để xử lý request, chẳng hạn `pam.>` và `joe.>`. _Cấu trúc_ permission của hai user này giống nhau, nhưng khác nhau ở subject cụ thể — được scope theo thuộc tính riêng của từng user.

> 🇬🇧 *Template functions can be used to declare the structure within a scope signing key, but utilize basic templating so that each user that is created with the signing key has user-specific subjects.*

Template functions cho phép khai báo cấu trúc trong một scoped signing key, sử dụng cơ chế templating cơ bản để mỗi user được tạo với signing key đó có subject riêng.

> 🇬🇧 *The following template functions will expand when a user is created.*

Các template function sau sẽ được mở rộng khi user được tạo:

- `{{name()}}` - mở rộng thành tên của user, ví dụ `pam`
- `{{subject()}}` - mở rộng thành giá trị public nkey của user, ví dụ `UAC...`
- `{{account-name()}}` - mở rộng thành tên account ký, ví dụ `sales`
- `{{account-subject()}}` - mở rộng thành giá trị public nkey của account, ví dụ `AXU...`
- `{{tag(key)}}` - mở rộng `key:value` tags liên kết với signing key

> 🇬🇧 *For example, given a scoped signing key with a templated `--allow-sub` subject:*

Ví dụ, với một scoped signing key có subject `--allow-sub` dùng template:

```
nsc edit signing-key \
  --account sales \
  --role team-service \
  --sk AXUQXKDPOTGUCOCOGDW7HWWVR5WEGF3KYL7EKOEHW2XWRS2PT5AOTRH3 \
  --allow-sub "{{account-name()}}.{{tag(team)}}.{{name()}}.>" \
  --allow-pub-response
```

> 🇬🇧 *We can create two users in different teams.*

Ta có thể tạo hai user thuộc các team khác nhau:

```
nsc add user pam -K team-service --tag team:support
nsc add user joe -K team-service --tag team:leads
```

> 🇬🇧 *The resulting `--allow-sub` permission per user would be expanded to:*

Permission `--allow-sub` của từng user sau khi mở rộng sẽ là:

```
sales.support.pam.>
```

và

```
sales.leads.joe.>
```

## Thuật ngữ trong bài

- **credential**: thông tin đăng nhập
- **permission**: quyền truy cập
- **scope**: phạm vi quyền
- **subject**: chuỗi định danh message (giống topic)
- **token**: chuỗi xác thực