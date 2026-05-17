---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nsc/streams
title: Streams
translated: true
translated_at: '2026-05-13T00:00:00+00:00'
---

# Streams

> 🇬🇧 *To share messages you publish with other accounts, you have to _Export_ a _Stream_. _Exports_ are associated with the account performing the export and advertised in exporting account's JWT.*

Để chia sẻ message với các account khác, bạn phải _Export_ một _Stream_ (luồng dữ liệu lưu trữ liên tục). Mỗi _Export_ gắn với account thực hiện export và được khai báo trong JWT của account đó.

### Thêm Public Stream Export

> 🇬🇧 *To add a stream to your account:*

Để thêm một stream vào account của bạn:

```shell
nsc add export --name abc --subject "a.b.c.>"
```

```
  [ OK ] added public stream export "abc"
```

> Note that we have exported stream with a subject that contains a wildcard. Any subject that matches the pattern will be exported.

> Lưu ý rằng chúng ta đã export stream với subject (chuỗi định danh message) chứa wildcard. Bất kỳ subject nào khớp với pattern đó đều sẽ được export.

> 🇬🇧 *To review the stream export:*

Để xem lại stream export:

```shell
nsc describe account
```

```
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                   Account Details                                    │
├───────────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                      │ A                                                        │
│ Account ID                │ ADETPT36WBIBUKM3IBCVM4A5YUSDXFEJPW4M6GGVBYCBW7RRNFTV5NGE │
│ Issuer ID                 │ OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG │
│ Issued                    │ 2019-12-05 13:35:42 UTC                                  │
│ Expires                   │                                                          │
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
╰───────────────────────────┴──────────────────────────────────────────────────────────╯

╭───────────────────────────────────────────────────────────╮
│                          Exports                          │
├──────┬────────┬─────────┬────────┬─────────────┬──────────┤
│ Name │ Type   │ Subject │ Public │ Revocations │ Tracking │
├──────┼────────┼─────────┼────────┼─────────────┼──────────┤
│ abc  │ Stream │ a.b.c.> │ Yes    │ 0           │ N/A      │
╰──────┴────────┴─────────┴────────┴─────────────┴──────────╯
```

> 🇬🇧 *Messages this account publishes on `a.b.c.>` will be forwarded to all accounts that import this stream.*

Các message mà account này publish lên `a.b.c.>` sẽ được chuyển tiếp đến tất cả các account import stream này.

### Import Stream

> 🇬🇧 *Importing a stream enables you to receive messages that are published by a different _Account_. To import a Stream, you have to create an _Import_. To create an _Import_ you need to know:*

Import một stream cho phép nhận message được publish từ một _Account_ khác. Để tạo _Import_, bạn cần biết:

* The exporting account's public key
* The subject where the stream is published
* You can map the stream's subject to a different subject
* Self-imports are not valid; you can only import streams from other accounts.

> 🇬🇧 *With the required information, we can add an import to the public stream.*

Với các thông tin trên, ta có thể thêm import vào public stream.

```bash
nsc add account B
```

```
[ OK ] generated and stored account key "AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H"
[ OK ] added account "B"
```

```shell
nsc add import --src-account ADETPT36WBIBUKM3IBCVM4A5YUSDXFEJPW4M6GGVBYCBW7RRNFTV5NGE --remote-subject "a.b.c.>"
```

```
[ OK ] added stream import "a.b.c.>"
```

> Notice that messages published by the remote account will be received on the same subject as they are originally published. Sometimes you would like to prefix messages received from a stream. To add a prefix specify `--local-subject`. Subscribers in our account can listen to `abc.>`. For example if `--local-subject abc`, The message will be received as `abc.a.b.c.>`.

> Lưu ý rằng các message do account từ xa publish sẽ được nhận trên cùng subject như khi được publish ban đầu. Đôi khi bạn muốn thêm prefix cho các message nhận từ một stream. Để thêm prefix, hãy chỉ định `--local-subject`. Subscriber (bên đăng ký nhận message) trong account của chúng ta có thể lắng nghe `abc.>`. Ví dụ nếu `--local-subject abc`, message sẽ được nhận dưới dạng `abc.a.b.c.>`.

> 🇬🇧 *And verifying it:*

Và xác minh lại:

```shell
nsc describe account
```

```
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                   Account Details                                    │
├───────────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                      │ B                                                        │
│ Account ID                │ AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │
│ Issuer ID                 │ OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG │
│ Issued                    │ 2019-12-05 13:39:55 UTC                                  │
│ Expires                   │                                                          │
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
│ Exports                   │ None                                                     │
╰───────────────────────────┴──────────────────────────────────────────────────────────╯

╭─────────────────────────────────────────────────────────────────────────────╮
│                                   Imports                                   │
├─────────┬────────┬─────────┬──────────────┬─────────┬──────────────┬────────┤
│ Name    │ Type   │ Remote  │ Local/Prefix │ Expires │ From Account │ Public │
├─────────┼────────┼─────────┼──────────────┼─────────┼──────────────┼────────┤
│ a.b.c.> │ Stream │ a.b.c.> │              │         │ A            │ Yes    │
╰─────────┴────────┴─────────┴──────────────┴─────────┴──────────────┴────────╯
```

> 🇬🇧 *Let's also add a user to make requests from the service:*

Hãy thêm một user để gửi request đến service:

```bash
nsc add user b
```

```
[ OK ] generated and stored user key "UDKNTNEL5YD66U2FZZ2B3WX2PLJFKEFHAPJ3NWJBFF44PT76Y2RAVFVE"
[ OK ] generated user creds file "~/.nkeys/creds/O/B/b.creds"
[ OK ] added user "b" to account "B"
```

### Đẩy thay đổi lên NATS servers

> 🇬🇧 *If your NATS servers are configured to use the built-in NATS resolver, remember that you need to 'push' any account changes you may have done locally using `nsc add` to the servers for those changes to take effect.*

Nếu NATS server của bạn được cấu hình dùng built-in NATS resolver, hãy nhớ 'push' mọi thay đổi account đã thực hiện cục bộ bằng `nsc add` lên server để các thay đổi có hiệu lực.

> 🇬🇧 *e.g. `nsc push -i` or `nsc push -a B -u nats://localhost`*

Ví dụ: `nsc push -i` hoặc `nsc push -a B -u nats://localhost`

### Kiểm thử Stream

```bash
nsc sub --account B --user b "a.b.c.>"
```

then

```shell
nsc pub --account A --user U a.b.c.hello world
```

## Bảo mật Streams

> 🇬🇧 *If you want to create a stream that is only accessible to accounts you designate, you can create a _private_ stream. The export will be visible in your account, but _subscribing_ accounts will require an authorization token that must be created by you and generated specifically for the subscribing account.*

Nếu muốn tạo stream chỉ cho phép các account do bạn chỉ định truy cập, bạn có thể tạo _private_ stream. Export sẽ hiển thị trong account của bạn, nhưng các account muốn subscribe sẽ cần một authorization token (chuỗi xác thực) do bạn tạo và cấp riêng cho từng account đó.

> 🇬🇧 *The authorization token is simply a JWT signed by your account where you authorize the client account to import your export.*

Authorization token thực chất là một JWT được ký bởi account của bạn, trong đó bạn cấp quyền cho account client import export của bạn.

### Tạo Private Stream Export

```shell
nsc add export --subject "private.abc.*" --private --account A
```

> 🇬🇧 *This is similar to when we defined an export, but this time we added the `--private` flag. The other thing to note is that the subject for the request has a wildcard. This enables the account to map specific subjects to specifically authorized accounts.*

Cách này tương tự khi định nghĩa export trước đó, nhưng lần này ta thêm flag `--private`. Điểm cần lưu ý là subject của request có chứa wildcard, cho phép account ánh xạ từng subject cụ thể đến các account được cấp quyền tương ứng.

```shell
nsc describe account A
```

```
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                   Account Details                                    │
├───────────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                      │ A                                                        │
│ Account ID                │ ADETPT36WBIBUKM3IBCVM4A5YUSDXFEJPW4M6GGVBYCBW7RRNFTV5NGE │
│ Issuer ID                 │ OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG │
│ Issued                    │ 2019-12-05 14:24:02 UTC                                  │
│ Expires                   │                                                          │
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
╰───────────────────────────┴──────────────────────────────────────────────────────────╯

╭──────────────────────────────────────────────────────────────────────────╮
│                                 Exports                                  │
├───────────────┬────────┬───────────────┬────────┬─────────────┬──────────┤
│ Name          │ Type   │ Subject       │ Public │ Revocations │ Tracking │
├───────────────┼────────┼───────────────┼────────┼─────────────┼──────────┤
│ abc           │ Stream │ a.b.c.>       │ Yes    │ 0           │ N/A      │
│ private.abc.* │ Stream │ private.abc.* │ No     │ 0           │ N/A      │
╰───────────────┴────────┴───────────────┴────────┴─────────────┴──────────╯
```

### Tạo Activation Token

> 🇬🇧 *For a foreign account to _import_ a private stream, you have to generate an activation token. In addition to granting permissions to the account, the activation token also allows you to subset the exported stream's subject.*

Để một account khác có thể _import_ private stream, bạn phải tạo activation token. Ngoài việc cấp permission (quyền truy cập) cho account đó, activation token còn cho phép bạn giới hạn phạm vi subject của stream được export.

> 🇬🇧 *To generate a token, you'll need to know the public key of the account importing the service. We can easily find the public key for account B by running:*

Để tạo token, bạn cần biết public key của account sẽ import service. Bạn có thể dễ dàng tìm public key của account B bằng lệnh:

```bash
nsc list keys --account B
```

```
╭──────────────────────────────────────────────────────────────────────────────────────────╮
│                                           Keys                                           │
├────────┬──────────────────────────────────────────────────────────┬─────────────┬────────┤
│ Entity │ Key                                                      │ Signing Key │ Stored │
├────────┼──────────────────────────────────────────────────────────┼─────────────┼────────┤
│ O      │ OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG │             │ *      │
│  B     │ AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │             │ *      │
│   b    │ UDKNTNEL5YD66U2FZZ2B3WX2PLJFKEFHAPJ3NWJBFF44PT76Y2RAVFVE │             │ *      │
╰────────┴──────────────────────────────────────────────────────────┴─────────────┴────────╯
```

```bash
nsc generate activation --account A --target-account AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H --subject private.abc.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H -o /tmp/activation.jwt
```

```
[ OK ] generated "private.abc.*" activation for account "AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H"
[ OK ] wrote account description to "/tmp/activation.jwt"
```

> 🇬🇧 *The command took the account that has the export ('A'), the public key of account B, the subject where the stream will publish to account B.*

Lệnh trên nhận vào account có export ('A'), public key của account B, và subject mà stream sẽ publish đến account B.

> 🇬🇧 *For completeness, the contents of the JWT file look like this:*

Để đầy đủ hơn, nội dung file JWT trông như sau:

```shell
cat /tmp/activation.jwt
```

```
-----BEGIN NATS ACTIVATION JWT-----
eyJ0eXAiOiJqd3QiLCJhbGciOiJlZDI1NTE5In0.eyJqdGkiOiJIS1FPQU9aQkVKS1JYNFJRUVhXS0xYSVBVTlNOSkRRTkxXUFBTSTQ3NkhCVVNYT0paVFFRIiwiaWF0IjoxNTc1NTU1OTczLCJpc3MiOiJBREVUUFQzNldCSUJVS00zSUJDVk00QTVZVVNEWEZFSlBXNE02R0dWQllDQlc3UlJORlRWNU5HRSIsIm5hbWUiOiJwcml2YXRlLmFiYy5BQU00NkUzWUY1V09aU0U1V05ZV0hOM1lZSVNWWk9TSTZYSFRGMlE2NEVDUFhTRlFaUk9KTVAySCIsInN1YiI6IkFBTTQ2RTNZRjVXT1pTRTVXTllXSE4zWVlJU1ZaT1NJNlhIVEYyUTY0RUNQWFNGUVpST0pNUDJIIiwidHlwZSI6ImFjdGl2YXRpb24iLCJuYXRzIjp7InN1YmplY3QiOiJwcml2YXRlLmFiYy5BQU00NkUzWUY1V09aU0U1V05ZV0hOM1lZSVNWWk9TSTZYSFRGMlE2NEVDUFhTRlFaUk9KTVAySCIsInR5cGUiOiJzdHJlYW0ifX0.yD2HWhRQYUFy5aQ7zNV0YjXzLIMoTKnnsBB_NsZNXP-Qr5fz7nowyz9IhoP7UszkN58m__ovjIaDKI9ml0l9DA
------END NATS ACTIVATION JWT------
```

> 🇬🇧 *When decoded it looks like this:*

Khi giải mã, nội dung trông như sau:

```shell
nsc describe jwt -f /tmp/activation.jwt 
```

```
╭────────────────────────────────────────────────────────────────────────────────────────╮
│                                       Activation                                       │
├─────────────────┬──────────────────────────────────────────────────────────────────────┤
│ Name            │ private.abc.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │
│ Account ID      │ AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H             │
│ Issuer ID       │ ADETPT36WBIBUKM3IBCVM4A5YUSDXFEJPW4M6GGVBYCBW7RRNFTV5NGE             │
│ Issued          │ 2019-12-05 14:26:13 UTC                                              │
│ Expires         │                                                                      │
├─────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Hash ID         │ GWIS5YCSET4EXEOBXVMQKXAR4CLY4IIXFV4MEMRUXPSQ7L4YTZ4Q====             │
├─────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Import Type     │ Stream                                                               │
│ Import Subject  │ private.abc.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │
├─────────────────┼──────────────────────────────────────────────────────────────────────┤
│ Max Messages    │ Unlimited                                                            │
│ Max Msg Payload │ Unlimited                                                            │
│ Network Src     │ Any                                                                  │
│ Time            │ Any                                                                  │
╰─────────────────┴──────────────────────────────────────────────────────────────────────╯
```

> 🇬🇧 *The token can be shared directly with the client account.*

Token có thể được chia sẻ trực tiếp với account client.

> If you manage many tokens for many accounts, you may want to host activation tokens on a web server and share the URL with the account. The benefit to the hosted approach is that any updates to the token would be available to the importing account whenever their account is updated, provided the URL you host them in is stable.

> Nếu bạn quản lý nhiều token cho nhiều account, bạn có thể host các activation token trên một web server và chia sẻ URL với account đó. Lợi ích của cách này là mọi cập nhật token sẽ có sẵn cho account import mỗi khi account của họ được cập nhật, miễn là URL dùng để host ổn định.

## Import Private Stream

> 🇬🇧 *Importing a private stream is more natural than a public one as the activation token given to you already has all of the necessary details. Note that the token can be an actual file path or a remote URL.*

Import một private stream đơn giản hơn public stream vì activation token được cung cấp đã chứa đầy đủ thông tin cần thiết. Lưu ý rằng token có thể là đường dẫn file thực tế hoặc một remote URL.

```shell
nsc add import --account B --token /tmp/activation.jwt
```

```
[ OK ] added stream import "private.abc.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H"
```

> 🇬🇧 *Describe account B*

Xem mô tả account B:

```shell
nsc describe account B
```

```
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                   Account Details                                    │
├───────────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                      │ B                                                        │
│ Account ID                │ AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │
│ Issuer ID                 │ OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG │
│ Issued                    │ 2019-12-05 14:29:16 UTC                                  │
│ Expires                   │                                                          │
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
│ Exports                   │ None                                                     │
╰───────────────────────────┴──────────────────────────────────────────────────────────╯

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                Imports                                                                                                │
├──────────────────────────────────────────────────────────────────────┬────────┬──────────────────────────────────────────────────────────────────────┬──────────────┬─────────┬──────────────┬────────┤
│ Name                                                                 │ Type   │ Remote                                                               │ Local/Prefix │ Expires │ From Account │ Public │
├──────────────────────────────────────────────────────────────────────┼────────┼──────────────────────────────────────────────────────────────────────┼──────────────┼─────────┼──────────────┼────────┤
│ a.b.c.>                                                              │ Stream │ a.b.c.>                                                              │              │         │ A            │ Yes    │
│ private.abc.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │ Stream │ private.abc.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │              │         │ A            │ No     │
╰──────────────────────────────────────────────────────────────────────┴────────┴──────────────────────────────────────────────────────────────────────┴──────────────┴─────────┴──────────────┴────────╯
```

### Kiểm thử Private Stream

> 🇬🇧 *Testing a private stream is no different than testing a public one:*

Kiểm thử private stream không khác gì kiểm thử public stream:

```bash
nsc tools sub --account B --user b private.abc.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H
```

then

```shell
nsc tools pub --account A --user U private.abc.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H hello
```

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **permission**: quyền truy cập
- **stream**: luồng dữ liệu lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **token**: chuỗi xác thực