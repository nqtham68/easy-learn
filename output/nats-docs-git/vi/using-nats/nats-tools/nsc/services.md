---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nsc/services
title: Services (Dịch vụ)
translated: true
translated_at: '2026-05-13T00:00:00Z'
---

# Services (Dịch vụ)

> 🇬🇧 *To share services that other accounts can reach via request reply, you have to _Export_ a _Service_. _Services_ are associated with the account performing the replies and are advertised in the exporting accounts' JWT.*

Để chia sẻ service (dịch vụ) mà các account khác có thể truy cập qua cơ chế request-reply, bạn cần _Export_ một _Service_. Service gắn liền với account đóng vai trò trả lời và được quảng bá trong JWT của account thực hiện export.

## Thêm Public Service Export

> 🇬🇧 *To add a service to your account:*

Để thêm một service vào account:

```bash
nsc add export --name help --subject help --service
```
```text
[ OK ] added public service export "help"
```

> 🇬🇧 *To review the service export:*

Để xem lại service export:

```bash
nsc describe account
```
```text
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                   Account Details                                    │
├───────────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                      │ A                                                        │
│ Account ID                │ ADETPT36WBIBUKM3IBCVM4A5YUSDXFEJPW4M6GGVBYCBW7RRNFTV5NGE │
│ Issuer ID                 │ OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG │
│ Issued                    │ 2019-12-04 18:20:42 UTC                                  │
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

╭────────────────────────────────────────────────────────────╮
│                          Exports                           │
├──────┬─────────┬─────────┬────────┬─────────────┬──────────┤
│ Name │ Type    │ Subject │ Public │ Revocations │ Tracking │
├──────┼─────────┼─────────┼────────┼─────────────┼──────────┤
│ help │ Service │ help    │ Yes    │ 0           │ -        │
╰──────┴─────────┴─────────┴────────┴─────────────┴──────────╯
```

## Import một Service

> 🇬🇧 *Importing a service enables you to send requests to the remote _Account_. To import a Service, you have to create an _Import_. To create an import you need to know:*

Import một service cho phép gửi request đến _Account_ từ xa. Để tạo một import, bạn cần biết:

* Public key của account đang export
* Subject (chuỗi định danh message (giống topic)) mà service đang lắng nghe
* Có thể ánh xạ subject của service sang subject khác
* Không thể tự import chính mình; chỉ import service từ account khác.

> 🇬🇧 *To learn how to inspect a JWT from an account server, [check this article](https://docs.nats.io/legacy/nas/inspecting_jwts).*

Để tìm hiểu cách kiểm tra JWT từ account server, [xem bài viết này](https://docs.nats.io/legacy/nas/inspecting_jwts).

> 🇬🇧 *First let's create a second account to import the service into:*

Đầu tiên, tạo một account thứ hai để import service vào:

```bash
nsc add account B
```
```text
[ OK ] generated and stored account key "AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H"
[ OK ] added account "B"
```

> 🇬🇧 *Add the import of the subject 'help'*

Thêm import cho subject 'help':

```shell
nsc add import --src-account ADETPT36WBIBUKM3IBCVM4A5YUSDXFEJPW4M6GGVBYCBW7RRNFTV5NGE --remote-subject help --service
```
```text
[ OK ] added service import "help"
```

> 🇬🇧 *Verifying our work:*

Kiểm tra kết quả:

```bash
nsc describe account
```
```text
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                   Account Details                                    │
├───────────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                      │ B                                                        │
│ Account ID                │ AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │
│ Issuer ID                 │ OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG │
│ Issued                    │ 2019-12-04 20:12:42 UTC                                  │
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

╭──────────────────────────────────────────────────────────────────────────╮
│                                 Imports                                  │
├──────┬─────────┬────────┬──────────────┬─────────┬──────────────┬────────┤
│ Name │ Type    │ Remote │ Local/Prefix │ Expires │ From Account │ Public │
├──────┼─────────┼────────┼──────────────┼─────────┼──────────────┼────────┤
│ help │ Service │ help   │ help         │         │ A            │ Yes    │
╰──────┴─────────┴────────┴──────────────┴─────────┴──────────────┴────────╯
```

> 🇬🇧 *Let's also add a user to make requests from the service:*

Thêm một user để gửi request đến service:

```bash
nsc add user b
```
```text
[ OK ] generated and stored user key "UDKNTNEL5YD66U2FZZ2B3WX2PLJFKEFHAPJ3NWJBFF44PT76Y2RAVFVE"
[ OK ] generated user creds file "~/.nkeys/creds/O/B/b.creds"
[ OK ] added user "b" to account "B"
```

### Đẩy thay đổi lên các NATS server

> 🇬🇧 *If your nats servers are configured to use the built-in NATS resolver, remember that you need to 'push' any account changes you may have done (locally) using `nsc add` to the servers for those changes to take effect.*

Nếu các NATS server được cấu hình dùng built-in NATS resolver, hãy nhớ 'push' mọi thay đổi account đã thực hiện cục bộ bằng `nsc add` lên server để các thay đổi có hiệu lực.

> 🇬🇧 *e.g. `nsc push -i` or `nsc push -a B -u nats://localhost`*

Ví dụ: `nsc push -i` hoặc `nsc push -a B -u nats://localhost`

### Kiểm tra Service

> 🇬🇧 *To test the service, we can install the ['nats'](../nats_cli) CLI tool:*

Để kiểm tra service, cài đặt công cụ CLI ['nats'](../nats_cli):

> 🇬🇧 *Set up a process to handle the request. This process will run from account 'A' using user 'U':*

Khởi chạy một tiến trình để xử lý request. Tiến trình này chạy từ account 'A' với user 'U':

```shell
nats reply --creds ~/.nkeys/creds/O/A/U.creds help "I will help"                
```

> 🇬🇧 *Remember you can also do:*

Cũng có thể dùng cách sau:

```shell
nsc reply --account A --user U help "I will help"
```

> 🇬🇧 *Send the request:*

Gửi request:

```shell
nats request --creds ~/.nkeys/creds/O/B/b.creds help me
```

> 🇬🇧 *The service receives the request:*

Service nhận được request:

```text
Received on [help]: 'me'
```

> 🇬🇧 *And the response is received by the requestor:*

Và bên gửi request nhận được response:

```text
Received  [_INBOX.v6KAX0v1bu87k49hbg3dgn.StIGJF0D] : 'I will help'
```

> 🇬🇧 *Or more simply:*

Hoặc ngắn gọn hơn:

```bash
nsc reply --account A --user U help "I will help"
nsc req --account B --user b help me
```
```text
published request: [help] : 'me'
received reply: [_INBOX.GCJltVq1wRSb5FoJrJ6SE9.w8utbBXR] : 'I will help'
```

## Bảo mật Service

> 🇬🇧 *If you want to create a service that is only accessible to accounts you designate you can create a _private_ service. The export will be visible in your account, but subscribing accounts will require an authorization token that must be created by you and generated specifically for the requesting account. The authorization token is simply a JWT signed by your account where you authorize the client account to import your service.*

Để tạo service chỉ cho phép các account do bạn chỉ định truy cập, hãy tạo service _private_. Export vẫn hiển thị trong account của bạn, nhưng các account muốn subscribe cần có authorization token (chuỗi xác thực) do bạn tạo ra và cấp riêng cho từng account yêu cầu. Token này là một JWT được ký bởi account của bạn, xác nhận quyền cho client account import service.

### Tạo Private Service Export

```shell
nsc add export --subject "private.help.*" --private --service --account A
```
```text
[ OK ] added private service export "private.help.*"
```

> 🇬🇧 *As before, we declared an export, but this time we added the `--private` flag. The other thing to note is that the subject for the request has a wildcard. This enables the account to map specific subjects to specifically authorized accounts.*

Tương tự như trước, chúng ta khai báo một export, nhưng lần này thêm flag `--private`. Điểm cần lưu ý là subject cho request có chứa wildcard, cho phép account ánh xạ các subject cụ thể đến các account đã được cấp quyền riêng.

```bash
nsc describe account A
```
```text
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                   Account Details                                    │
├───────────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                      │ A                                                        │
│ Account ID                │ ADETPT36WBIBUKM3IBCVM4A5YUSDXFEJPW4M6GGVBYCBW7RRNFTV5NGE │
│ Issuer ID                 │ OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG │
│ Issued                    │ 2019-12-04 20:19:19 UTC                                  │
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

╭─────────────────────────────────────────────────────────────────────────────╮
│                                   Exports                                   │
├────────────────┬─────────┬────────────────┬────────┬─────────────┬──────────┤
│ Name           │ Type    │ Subject        │ Public │ Revocations │ Tracking │
├────────────────┼─────────┼────────────────┼────────┼─────────────┼──────────┤
│ help           │ Service │ help           │ Yes    │ 0           │ -        │
│ private.help.* │ Service │ private.help.* │ No     │ 0           │ -        │
╰────────────────┴─────────┴────────────────┴────────┴─────────────┴──────────╯
```

### Tạo Activation Token

> 🇬🇧 *For the foreign account to _import_ a private service and be able to send requests, you have to generate an activation token. The activation token in addition to granting permission to the account allows you to subset the service's subject:*

Để account bên ngoài có thể _import_ private service và gửi request, bạn phải tạo một activation token. Ngoài việc cấp permission (quyền truy cập), token này còn cho phép giới hạn phạm vi subject của service:

> 🇬🇧 *To generate a token, you'll need to know the public key of the account importing the service. We can easily find the public key for account B by running:*

Để tạo token, cần biết public key của account sẽ import service. Tìm public key của account B bằng lệnh:

```bash
nsc list keys --account B
```
```text
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

```shell
nsc generate activation --account A --target-account AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H --subject private.help.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H -o /tmp/activation.jwt
```
```text
[ OK ] generated "private.help.*" activation for account "AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H"
[ OK ] wrote account description to "/tmp/activation.jwt"
```

> 🇬🇧 *The command took the account that has the export \('A'\), the public key of account B, the subject where requests from account B will be handled, and an output file where the token can be stored. The subject for the export allows the service to handle all requests coming in on private.help.\*, but account B can only request from a specific subject.*

Lệnh trên nhận vào: account sở hữu export ('A'), public key của account B, subject nơi các request từ account B được xử lý, và file đầu ra để lưu token. Subject của export cho phép service xử lý tất cả request đến trên `private.help.*`, nhưng account B chỉ được phép request trên một subject cụ thể.

> 🇬🇧 *For completeness, the contents of the JWT file looks like this:*

Để tham khảo, nội dung file JWT có dạng như sau:

```bash
cat /tmp/activation.jwt
```
```text
-----BEGIN NATS ACTIVATION JWT-----
eyJ0eXAiOiJqd3QiLCJhbGciOiJlZDI1NTE5In0.eyJqdGkiOiJUS01LNEFHT1pOVERDTERGUk9QTllNM0hHUVRDTEJTUktNQUxXWTVSUUhFVEVNNE1VTDdBIiwiaWF0IjoxNTc1NDkxNjEwLCJpc3MiOiJBREVUUFQzNldCSUJVS00zSUJDVk00QTVZVVNEWEZFSlBXNE02R0dWQllDQlc3UlJORlRWNU5HRSIsIm5hbWUiOiJwcml2YXRlLmhlbHAuQUFNNDZFM1lGNVdPWlNFNVdOWVdITjNZWUlTVlpPU0k2WEhURjJRNjRFQ1BYU0ZRWlJPSk1QMkgiLCJzdWIiOiJBQU00NkUzWUY1V09aU0U1V05ZV0hOM1lZSVNWWk9TSTZYSFRGMlE2NEVDUFhTRlFaUk9KTVAySCIsInR5cGUiOiJhY3RpdmF0aW9uIiwibmF0cyI6eyJzdWJqZWN0IjoicHJpdmF0ZS5oZWxwLkFBTTQ2RTNZRjVXT1pTRTVXTllXSE4zWVlJU1ZaT1NJNlhIVEYyUTY0RUNQWFNGUVpST0pNUDJIIiwidHlwZSI6InNlcnZpY2UifX0.4tFx_1UzPUwbV8wFNIJsQYu91K9hZaGRLE10nOphfHGetvMPv1384KC-1AiNdhApObSDFosdDcpjryD0QxaDCQ
------END NATS ACTIVATION JWT------
```

> 🇬🇧 *When decoded it looks like this:*

Khi giải mã, nội dung trông như sau:

```shell
nsc describe jwt -f /tmp/activation.jwt
```
```text
╭─────────────────────────────────────────────────────────────────────────────────────────╮
│                                       Activation                                        │
├─────────────────┬───────────────────────────────────────────────────────────────────────┤
│ Name            │ private.help.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │
│ Account ID      │ AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H              │
│ Issuer ID       │ ADETPT36WBIBUKM3IBCVM4A5YUSDXFEJPW4M6GGVBYCBW7RRNFTV5NGE              │
│ Issued          │ 2019-12-04 20:33:30 UTC                                               │
│ Expires         │                                                                       │
├─────────────────┼───────────────────────────────────────────────────────────────────────┤
│ Hash ID         │ DD6BZKI2LTQKAJYD5GTSI4OFUG72KD2BF74NFVLUNO47PR4OX64Q====              │
├─────────────────┼───────────────────────────────────────────────────────────────────────┤
│ Import Type     │ Service                                                               │
│ Import Subject  │ private.help.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │
├─────────────────┼───────────────────────────────────────────────────────────────────────┤
│ Max Messages    │ Unlimited                                                             │
│ Max Msg Payload │ Unlimited                                                             │
│ Network Src     │ Any                                                                   │
│ Time            │ Any                                                                   │
╰─────────────────┴───────────────────────────────────────────────────────────────────────╯
```

> 🇬🇧 *The token can be shared directly with the client account.*

Token có thể được chia sẻ trực tiếp với client account.

> If you manage many tokens for many accounts, you may want to host activation tokens on a web server and share the URL with the account. The benefit to the hosted approach is that any updates to the token would be available to the importing account whenever their account is updated, provided the URL you host them in is stable. When using a JWT account server, the tokens can be stored right on the server and shared by an URL that is printed when the token is generated.

> Nếu bạn quản lý nhiều token cho nhiều account, có thể host các activation token trên web server và chia sẻ URL với account. Lợi thế của cách này là mọi cập nhật token sẽ sẵn sàng cho account import bất cứ khi nào account của họ được cập nhật, miễn là URL host ổn định. Khi dùng JWT account server, token có thể lưu trực tiếp trên server và chia sẻ qua URL được in ra lúc tạo token.

## Import Private Service

> 🇬🇧 *Importing a private service is more natural than a public one because the activation token stores all the necessary details. Again, the token can be an actual file path or a remote URL.*

Import private service đơn giản hơn public service vì activation token đã chứa đủ thông tin cần thiết. Token có thể là đường dẫn file thực tế hoặc một URL từ xa.

```shell
nsc add import --account B -u /tmp/activation.jwt --local-subject private.help --name private.help
```
```text
[ OK ] added service import "private.help.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H"
```

> 🇬🇧 *Describe account B*

Xem mô tả account B:

```shell
nsc describe account B
```
```text
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                   Account Details                                    │
├───────────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                      │ B                                                        │
│ Account ID                │ AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │
│ Issuer ID                 │ OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG │
│ Issued                    │ 2019-12-04 20:38:06 UTC                                  │
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

╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                     Imports                                                                     │
├──────────────┬─────────┬───────────────────────────────────────────────────────────────────────┬──────────────┬─────────┬──────────────┬────────┤
│ Name         │ Type    │ Remote                                                                │ Local/Prefix │ Expires │ From Account │ Public │
├──────────────┼─────────┼───────────────────────────────────────────────────────────────────────┼──────────────┼─────────┼──────────────┼────────┤
│ help         │ Service │ help                                                                  │ help         │         │ A            │ Yes    │
│ private.help │ Service │ private.help.AAM46E3YF5WOZSE5WNYWHN3YYISVZOSI6XHTF2Q64ECPXSFQZROJMP2H │ private.help │         │ A            │ No     │
╰──────────────┴─────────┴───────────────────────────────────────────────────────────────────────┴──────────────┴─────────┴──────────────┴────────╯
```

> 🇬🇧 *When importing a service, you can specify the local subject you want to use to make requests. The local subject in this case is `private.help`. However when the request is forwarded by NATS, the request is sent on the remote subject.*

Khi import service, bạn có thể chỉ định local subject dùng để gửi request. Local subject trong trường hợp này là `private.help`. Tuy nhiên khi NATS chuyển tiếp request, nó sẽ được gửi đi trên remote subject.

### Kiểm tra Private Service

> 🇬🇧 *Testing a private service is no different than a public one:*

Kiểm tra private service không khác gì public service:

```bash
nsc reply --account A --user U "private.help.*" "help is here"
nsc req --account B --user b private.help help_me
```
```text
published request: [private.help] : 'help_me'
received reply: [_INBOX.3MhS0iCHfqO8wUl1x59bHB.jpE2jvEj] : 'help is here'
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **permission**: quyền truy cập
- **request**: yêu cầu
- **response**: phản hồi
- **service**: dịch vụ
- **subject**: chuỗi định danh message (giống topic)
- **token**: chuỗi xác thực