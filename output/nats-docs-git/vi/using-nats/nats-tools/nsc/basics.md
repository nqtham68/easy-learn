---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nsc/basics
title: Kiến thức cơ bản về NSC
translated: true
translated_at: '2026-05-13T00:00:00Z'
---

# Kiến thức cơ bản về NSC

> 🇬🇧 *NSC allows you to manage identities. Identities take the form of _nkeys_. Nkeys are a public-key signature system based on Ed25519 for the NATS ecosystem.*

NSC giúp quản lý các identity. Các identity được biểu diễn dưới dạng _nkeys_ — hệ thống chữ ký public-key dựa trên Ed25519 dành cho hệ sinh thái NATS.

> 🇬🇧 *The nkey identities are associated with NATS configuration in the form of a JSON Web Token \(JWT\). The JWT is digitally signed by the private key of an issuer forming a chain of trust. The `nsc` tool creates and manages these identities and allows you to deploy them to a JWT account server, which in turn makes the configurations available to nats-servers.*

Các nkey identity được liên kết với cấu hình NATS dưới dạng JSON Web Token (JWT). JWT được ký số bằng private key của issuer, tạo thành chuỗi tin cậy (chain of trust). Công cụ `nsc` tạo và quản lý các identity này, đồng thời cho phép triển khai chúng lên JWT account server để nats-server có thể sử dụng.

> 🇬🇧 *There's a logical hierarchy to the entities:*

Các thực thể được tổ chức theo cấp bậc logic:

* `Operators` chịu trách nhiệm vận hành nats-server và phát hành account JWT. Operator đặt giới hạn cho account, như số lượng kết nối, giới hạn dữ liệu, v.v.
* `Accounts` chịu trách nhiệm phát hành user JWT. Account định nghĩa các stream (luồng message lưu trữ liên tục) và service có thể export sang account khác, đồng thời import stream và service từ account khác.
* `Users` được phát hành bởi account và mã hóa các giới hạn về mức sử dụng và permission (quyền truy cập) trên không gian subject (chuỗi định danh message) của account đó.

> 🇬🇧 *NSC allows you to create, edit, and delete these entities, and will be central to all account-based configuration.*

NSC cho phép tạo, chỉnh sửa và xóa các thực thể này, đây là công cụ trung tâm cho mọi cấu hình dựa trên account.

> 🇬🇧 *In this guide, you'll run end-to-end on some of the configuration scenarios:*

Hướng dẫn này sẽ đưa bạn qua các kịch bản cấu hình từ đầu đến cuối:

* Tạo NKey identity và các JWT tương ứng
* Cung cấp JWT cho nats-server
* Cấu hình nats-server sử dụng JWT

> 🇬🇧 *Let's run through the process of creating some identities and JWTs and work through the process.*

Hãy cùng đi qua quy trình tạo identity và JWT.

## Tạo Operator, Account và User

> 🇬🇧 *Let's create an operator called `MyOperator`.*

Tạo một operator có tên `MyOperator`.

> 🇬🇧 *_There is an additional switch `--sys` that sets up the system account which is required for interacting with the NATS server. You can create and set the system account later._*

_Có thêm switch `--sys` để thiết lập system account — thứ cần thiết khi tương tác với NATS server. Bạn có thể tạo và gán system account này sau._

```bash
nsc add operator MyOperator
```
```text
[ OK ] generated and stored operator key "ODSWWTKZLRDFBPXNMNAY7XB2BIJ45SV756BHUT7GX6JQH6W7AHVAFX6C"
[ OK ] added operator "MyOperator"
[ OK ] When running your own nats-server, make sure they run at least version 2.2.0
```

> 🇬🇧 *With the above command, the tool generated an NKEY for the operator, stored the private key safely in its keystore.*

Lệnh trên tạo một NKEY cho operator và lưu private key an toàn vào keystore.

> 🇬🇧 *Lets add a service URL to the operator. Service URLs specify where the nats-server is listening. Tooling such as `nsc` can make use of that configuration:*

Thêm service URL vào operator. Service URL chỉ định địa chỉ nats-server đang lắng nghe. Các công cụ như `nsc` có thể tận dụng cấu hình này:

```bash
nsc edit operator --service-url nats://localhost:4222
```
```text
[ OK ] added service url "nats://localhost:4222"
[ OK ] edited operator "MyOperator"
```

> 🇬🇧 *Creating an account is just as easy:*

Tạo account cũng đơn giản tương tự:

```bash
nsc add account MyAccount
```
```text
[ OK ] generated and stored account key "AD2M34WBNGQFYK37IDX53DPRG74RLLT7FFWBOBMBUXMAVBCVAU5VKWIY"
[ OK ] added account "MyAccount"
```

> 🇬🇧 *As expected, the tool generated an NKEY representing the account and stored the private key safely in the keystore.*

Công cụ tạo một NKEY đại diện cho account và lưu private key an toàn vào keystore.

> 🇬🇧 *Finally, let's create a user:*

Cuối cùng, tạo một user:

```bash
nsc add user MyUser
```
```text
[ OK ] generated and stored user key "UAWBXLSZVZHNDIURY52F6WETFCFZLXYUEFJAHRXDW7D2K4445IY4BVXP"
[ OK ] generated user creds file `~/.nkeys/creds/MyOperator/MyAccount/MyUser.creds`
[ OK ] added user "MyUser" to account "MyAccount"
```

> 🇬🇧 *As expected, the tool generated an NKEY representing the user, and stored the private key safely in the keystore. In addition, the tool generated a _credentials_ file. A credentials file contains the JWT for the user and the private key for the user. Credential files are used by NATS clients to identify themselves to the system. The client will extract and present the JWT to the nats-server and use the private key to verify its identity.*

Công cụ tạo NKEY đại diện cho user và lưu private key vào keystore. Ngoài ra, công cụ còn tạo file _credentials_ (thông tin đăng nhập). File credential chứa JWT của user và private key tương ứng. NATS client dùng file này để xác thực với hệ thống: client trích xuất JWT và gửi lên nats-server, sau đó dùng private key để chứng minh danh tính.

### Tài nguyên NSC

> 🇬🇧 *NSC manages three different directories:*

NSC quản lý ba thư mục khác nhau:

* Thư mục NSC home lưu dữ liệu liên quan đến nsc. Mặc định nằm tại `~/.nsc`, có thể thay đổi qua biến môi trường `$NSC_HOME`.
* Thư mục _nkeys_ lưu toàn bộ private key. Mặc định nằm tại `~/.nkeys`, có thể thay đổi qua biến môi trường `$NKEYS_PATH`. Nội dung thư mục nkeys phải được bảo vệ như secret (chuỗi bí mật).
* Thư mục _stores_ chứa các JWT đại diện cho các thực thể. Thư mục này nằm tại `$NSC_HOME/nats`, có thể thay đổi bằng lệnh `nsc env -s <dir>`. Thư mục stores có thể đưa vào version control vì các JWT không chứa secret.

#### Thư mục Stores của NSC

> 🇬🇧 *The stores directory contains a number of directories. Each named by an operator in question, which in turn contains all accounts and users:*

Thư mục stores gồm nhiều thư mục con, mỗi thư mục được đặt tên theo operator tương ứng và chứa toàn bộ account cùng user:

```bash
tree ~/.nsc/nats
```
```text
/Users/myusername/.nsc/nats
└── MyOperator
    ├── MyOperator.jwt
    └── accounts
        └── MyAccount
            ├── MyAccount.jwt
            └── users
                └── MyUser.jwt
```

> 🇬🇧 *These JWTs are the same artifacts that the NATS servers will use to check the validity of an account, its limits, and the JWTs that are presented by clients when they connect to the nats-server.*

Đây chính là các JWT mà NATS server dùng để kiểm tra tính hợp lệ của account, giới hạn của nó, và các JWT do client xuất trình khi kết nối.

#### Thư mục NKEYS

> 🇬🇧 *The nkeys directory contains all the private keys and credential files. As mentioned before, care must be taken to keep these files secure.*

Thư mục nkeys chứa toàn bộ private key và credential file. Như đã đề cập, cần đặc biệt chú ý bảo mật các file này.

> 🇬🇧 *The structure keys directory is machine friendly. All keys are sharded by their kind `O` for operators, `A` for accounts, `U` for users. These prefixes are also part of the public key. The second and third letters in the public key are used to create directories where other like-named keys are stored.*

Cấu trúc thư mục keys được thiết kế thân thiện với máy. Các key được phân mảnh theo loại: `O` cho operator, `A` cho account, `U` cho user. Các tiền tố này cũng là một phần của public key. Ký tự thứ hai và thứ ba trong public key được dùng để tạo các thư mục chứa các key cùng loại.

```shell
tree ~/.nkeys
```
```text
/Users/myusername/.nkeys
├── creds
│   └── MyOperator
│       └── MyAccount
│           └── MyUser.creds
└── keys
    ├── A
    │   └── DE
    │       └── ADETPT36WBIBUKM3IBCVM4A5YUSDXFEJPW4M6GGVBYCBW7RRNFTV5NGE.nk
    ├── O
    │   └── AF
    │       └── OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG.nk
    └── U
        └── DB
            └── UDBD5FNQPSLIO6CDMIS5D4EBNFKYWVDNULQTFTUZJXWFNYLGFF52VZN7.nk
```

> 🇬🇧 *The `nk` files themselves are named after the complete public key, and stored in a single string - the private key in question:*

Các file `nk` được đặt tên theo public key đầy đủ và chứa một chuỗi duy nhất là private key tương ứng:

```bash
cat ~/.nkeys/keys/U/DB/UDBD5FNQPSLIO6CDMIS5D4EBNFKYWVDNULQTFTUZJXWFNYLGFF52VZN7.nk 
```
```text
SUAG35IAY2EF5DOZRV6MUSOFDGJ6O2BQCZHSRPLIK6J3GVCX366BFAYSNA
```

> 🇬🇧 *The private keys are encoded into a string, and always begin with an `S` for _seed_. The second letter starts with the type of key in question. `O` for operators, `A` for accounts, `U` for users.*

Private key được mã hóa thành chuỗi và luôn bắt đầu bằng `S` (viết tắt của _seed_). Chữ cái thứ hai cho biết loại key: `O` cho operator, `A` cho account, `U` cho user.

> 🇬🇧 *In addition to containing keys, the nkeys directory contains a `creds` directory. This directory is organized in a way friendly to humans. It stores user credential files or `creds` files for short. A credentials file contains a copy of the user JWT and the private key for the user. These files are used by NATS clients to connect to a NATS server:*

Ngoài key, thư mục nkeys còn chứa thư mục `creds` được tổ chức theo cách thân thiện với người dùng. Thư mục này lưu credential file của user (hay file `creds`). Mỗi credential file chứa bản sao JWT của user và private key. NATS client dùng các file này để kết nối với NATS server:

```bash
cat ~/.nkeys/creds/MyOperator/MyAccount/MyUser.creds
```
```text
-----BEGIN NATS USER JWT-----
eyJ0eXAiOiJKV1QiLCJhbGciOiJlZDI1NTE5LW5rZXkifQ.eyJqdGkiOiI0NUc3MkhIQUVCRFBQV05ZWktMTUhQNUFYWFRSSUVDQlNVQUI2VDZRUjdVM1JZUFZaM05BIiwiaWF0IjoxNjM1Mzc1NTYxLCJpc3MiOiJBRDJNMzRXQk5HUUZZSzM3SURYNTNEUFJHNzRSTExUN0ZGV0JPQk1CVVhNQVZCQ1ZBVTVWS1dJWSIsIm5hbWUiOiJNeVVzZXIiLCJzdWIiOiJVQVdCWExTWlZaSE5ESVVSWTUyRjZXRVRGQ0ZaTFhZVUVGSkFIUlhEVzdEMks0NDQ1SVk0QlZYUCIsIm5hdHMiOnsicHViIjp7fSwic3ViIjp7fSwic3VicyI6LTEsImRhdGEiOi0xLCJwYXlsb2FkIjotMSwidHlwZSI6InVzZXIiLCJ2ZXJzaW9uIjoyfX0.CGymhGYHfdZyhUeucxNs9TthSjy_27LVZikqxvm-pPLili8KNe1xyOVnk_w-xPWdrCx_t3Se2lgXmoy3wBcVCw
------END NATS USER JWT------

************************* IMPORTANT *************************
NKEY Seed printed below can be used to sign and prove identity.
NKEYs are sensitive and should be treated as secrets.

-----BEGIN USER NKEY SEED-----
SUAP2AY6UAWHOXJBWDNRNKJ2DHNC5VA2DFJZTF6C6PMLKUCOS2H2E2BA2E
------END USER NKEY SEED------

*************************************************************
```

### Liệt kê Key

> 🇬🇧 *You can list the current entities you are working with by doing:*

Xem danh sách các thực thể hiện tại:

```bash
nsc list keys
```
```text
+----------------------------------------------------------------------------------------------+
|                                             Keys                                             |
+------------+----------------------------------------------------------+-------------+--------+
| Entity     | Key                                                      | Signing Key | Stored |
+------------+----------------------------------------------------------+-------------+--------+
| MyOperator | ODSWWTKZLRDFBPXNMNAY7XB2BIJ45SV756BHUT7GX6JQH6W7AHVAFX6C |             | *      |
|  MyAccount | AD2M34WBNGQFYK37IDX53DPRG74RLLT7FFWBOBMBUXMAVBCVAU5VKWIY |             | *      |
|   MyUser   | UAWBXLSZVZHNDIURY52F6WETFCFZLXYUEFJAHRXDW7D2K4445IY4BVXP |             | *      |
+------------+----------------------------------------------------------+-------------+--------+
```

> 🇬🇧 *The different entity names are listed along with their public key, and whether the key is stored. Stored keys are those that are found in the nkeys directory.*

Kết quả hiển thị tên từng thực thể, public key của nó, và trạng thái lưu trữ. Key được coi là "stored" khi có mặt trong thư mục nkeys.

> 🇬🇧 *In some cases you may want to view the private keys:*

Trong một số trường hợp, bạn muốn xem cả private key:

```shell
nsc list keys --show-seeds
```
```text
+---------------------------------------------------------------------------------------+
|                                      Seeds Keys                                       |
+------------+------------------------------------------------------------+-------------+
| Entity     | Private Key                                                | Signing Key |
+------------+------------------------------------------------------------+-------------+
| MyOperator | SOAJ3JDZBE6JKJO277CQP5RIAA7I7HBI44RDCMTIV3TQRYQX35OTXSMHAE |             |
|  MyAccount | SAAACXWSQIKJ4L2SEAUZJR3BCNSRCN32V5UJSABCSEP35Q7LQRPV6F4JPI |             |
|   MyUser   | SUAP2AY6UAWHOXJBWDNRNKJ2DHNC5VA2DFJZTF6C6PMLKUCOS2H2E2BA2E |             |
+------------+------------------------------------------------------------+-------------+
[ ! ] seed is not stored
[ERR] error reading seed
```

> 🇬🇧 *If you don't have the seed \(perhaps you don't control the operator\), nsc will decorate the row with a `!`. If you have more than one account, you can show them all by specifying the `--all` flag.*

Nếu không có seed (ví dụ bạn không kiểm soát operator), nsc sẽ đánh dấu dòng đó bằng `!`. Nếu có nhiều account, dùng flag `--all` để hiện tất cả.

## JWT của Operator

> 🇬🇧 *You can view a human readable version of the JWT by using `nsc`:*

Xem nội dung JWT ở dạng dễ đọc bằng `nsc`:

```bash
nsc describe operator
```
```text
+----------------------------------------------------------------------------------+
|                                 Operator Details                                 |
+-----------------------+----------------------------------------------------------+
| Name                  | MyOperator                                               |
| Operator ID           | ODSWWTKZLRDFBPXNMNAY7XB2BIJ45SV756BHUT7GX6JQH6W7AHVAFX6C |
| Issuer ID             | ODSWWTKZLRDFBPXNMNAY7XB2BIJ45SV756BHUT7GX6JQH6W7AHVAFX6C |
| Issued                | 2021-10-27 22:58:28 UTC                                  |
| Expires               |                                                          |
| Operator Service URLs | nats://localhost:4222                                    |
| Require Signing Keys  | false                                                    |
+-----------------------+----------------------------------------------------------+
```

> 🇬🇧 *Since the operator JWT is just a JWT you can use other tools, such as jwt.io to decode a JWT and inspect its contents. All JWTs have a header, payload, and signature:*

Vì operator JWT là JWT thông thường, bạn có thể dùng các công cụ khác như jwt.io để giải mã và kiểm tra nội dung. Mọi JWT đều có header, payload và signature:

```text
{
  "typ": "jwt",
  "alg": "ed25519"
}
{
  "jti": "ZP2X3T2R57SLXD2U5J3OLLYIVW2LFBMTXRPMMGISQ5OF7LANUQPQ",
  "iat": 1575468772,
  "iss": "OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG",
  "name": "O",
  "sub": "OAFEEYZSYYVI4FXLRXJTMM32PQEI3RGOWZJT7Y3YFM4HB7ACPE4RTJPG",
  "type": "operator",
  "nats": {
    "operator_service_urls": [
      "nats://localhost:4222"
    ]
  }
}
```

> 🇬🇧 *All NATS JWTs will use the `algorithm` ed25519 for signature. The payload will list different things. On our basically empty operator, we will only have standard JWT `claim` fields:*

Mọi NATS JWT đều dùng `algorithm` ed25519 để ký. Payload liệt kê nhiều thông tin khác nhau. Với operator gần như trống, chỉ có các trường JWT chuẩn `claim`:

> 🇬🇧 *`jti` - a jwt id `iat` - the timestamp when the JWT was issued in UNIX time `iss` - the issuer of the JWT, in this case the operator's public key `sub` - the subject or identity represented by the JWT, in this case the same operator `type` - since this is an operator JWT, `operator` is the type*

`jti` — JWT id; `iat` — thời điểm JWT được phát hành (dạng UNIX time); `iss` — issuer của JWT, trong trường hợp này là public key của operator; `sub` — subject hay identity được JWT đại diện, ở đây chính là operator; `type` — vì đây là operator JWT nên `operator` là loại.

> 🇬🇧 *NATS specific is the `nats` object, which is where we add NATS specific JWT configuration to the JWT claim.*

Đặc thù của NATS là object `nats`, nơi các cấu hình JWT riêng của NATS được thêm vào JWT claim.

> 🇬🇧 *Because the issuer and subject are one and the same, this JWT is self-signed.*

Vì issuer và subject là cùng một thực thể, JWT này là self-signed (tự ký).

### JWT của Account

> 🇬🇧 *Again we can inspect the account:*

Tương tự, có thể kiểm tra account:

```bash
nsc describe account
```
```text
+--------------------------------------------------------------------------------------+
|                                   Account Details                                    |
+---------------------------+----------------------------------------------------------+
| Name                      | MyAccount                                                |
| Account ID                | AD2M34WBNGQFYK37IDX53DPRG74RLLT7FFWBOBMBUXMAVBCVAU5VKWIY |
| Issuer ID                 | ODSWWTKZLRDFBPXNMNAY7XB2BIJ45SV756BHUT7GX6JQH6W7AHVAFX6C |
| Issued                    | 2021-10-27 22:59:01 UTC                                  |
| Expires                   |                                                          |
+---------------------------+----------------------------------------------------------+
| Max Connections           | Unlimited                                                |
| Max Leaf Node Connections | Unlimited                                                |
| Max Data                  | Unlimited                                                |
| Max Exports               | Unlimited                                                |
| Max Imports               | Unlimited                                                |
| Max Msg Payload           | Unlimited                                                |
| Max Subscriptions         | Unlimited                                                |
| Exports Allows Wildcards  | True                                                     |
| Response Permissions      | Not Set                                                  |
+---------------------------+----------------------------------------------------------+
| Jetstream                 | Disabled                                                 |
+---------------------------+----------------------------------------------------------+
| Imports                   | None                                                     |
| Exports                   | None                                                     |
+---------------------------+----------------------------------------------------------+
```

### JWT của User

> 🇬🇧 *Finally the user JWT:*

Cuối cùng là user JWT:

```bash
nsc describe user MyUser
```
```text
+---------------------------------------------------------------------------------+
|                                      User                                       |
+----------------------+----------------------------------------------------------+
| Name                 | MyUser                                                   |
| User ID              | UAWBXLSZVZHNDIURY52F6WETFCFZLXYUEFJAHRXDW7D2K4445IY4BVXP |
| Issuer ID            | AD2M34WBNGQFYK37IDX53DPRG74RLLT7FFWBOBMBUXMAVBCVAU5VKWIY |
| Issued               | 2021-10-27 22:59:21 UTC                                  |
| Expires              |                                                          |
| Bearer Token         | No                                                       |
| Response Permissions | Not Set                                                  |
+----------------------+----------------------------------------------------------+
| Max Msg Payload      | Unlimited                                                |
| Max Data             | Unlimited                                                |
| Max Subs             | Unlimited                                                |
| Network Src          | Any                                                      |
| Time                 | Any                                                      |
+----------------------+----------------------------------------------------------+
```

> 🇬🇧 *The user id is the public key for the user, the issuer is the account. This user can publish and subscribe to anything, as no limits are set.*

User id là public key của user, issuer là account. User này có thể publish và subscribe mọi thứ vì chưa có giới hạn nào được đặt.

> 🇬🇧 *When a user connects to a nats-server, it presents it's user JWT and signs a nonce using its private key. The server verifies if the user is who they say they are by validating that the nonce was signed using the private key associated with the public key, representing the identify of the user. Next, the server fetches the issuer account and validates that the account was issued by a trusted operator completing the chain of trust verification.*

Khi user kết nối tới nats-server, nó xuất trình user JWT và ký một nonce bằng private key. Server xác minh danh tính bằng cách kiểm tra nonce được ký bằng private key khớp với public key của user. Tiếp theo, server lấy issuer account và xác nhận rằng account đó được phát hành bởi operator đáng tin cậy, hoàn thành quá trình xác minh chuỗi tin cậy.

> 🇬🇧 *Let's put all of this together, and create a simple server configuration that accepts sessions from `U`.*

Hãy kết hợp tất cả lại và tạo cấu hình server đơn giản chấp nhận session từ `U`.

## Cấu hình Account Server

> 🇬🇧 *To configure a server to use accounts, you need to configure it to select the type of _account resolver_ it will use. The preferred option being to configure the server to use the built-in [NATS Based Resolver](../../../running-a-nats-service/configuration/securing_nats/jwt/resolver.md#nats-based-resolver).*

Để cấu hình server sử dụng account, cần chỉ định loại _account resolver_. Lựa chọn được khuyến nghị là dùng [NATS Based Resolver](../../../running-a-nats-service/configuration/securing_nats/jwt/resolver.md#nats-based-resolver) tích hợp sẵn.

## Cấu hình NATS Server

> 🇬🇧 *If you don't have a nats-server installed, let's do that now:*

Nếu chưa cài nats-server, hãy cài ngay:

```shell
go get github.com/nats-io/nats-server
```

> 🇬🇧 *Let's create a configuration that references our operator JWT and the nats-account-server as a resolver. You can use `nsc` itself to generate the security part of the server configuration that you can just add to your `nats-server` config file.*

Tạo cấu hình tham chiếu đến operator JWT và nats-account-server làm resolver. Bạn có thể dùng `nsc` để tự sinh phần bảo mật của server config rồi thêm vào file `nats-server`.

> 🇬🇧 *For example to use the NATS resolver (which is the recommended resolver configuration) use `nsc generate config --nats-resolver`.*

Ví dụ, để dùng NATS resolver (cấu hình được khuyến nghị), dùng `nsc generate config --nats-resolver`.

> 🇬🇧 *Edit this generated configuration as needed (e.g. adjust the location where the server will store the JWTs in `resolver.dir`) and paste it into your nats-server configuration (or save it to a file and import that file from within you server config file).*

Chỉnh sửa cấu hình được tạo ra nếu cần (ví dụ: điều chỉnh vị trí lưu JWT trong `resolver.dir`) rồi dán vào file cấu hình nats-server (hoặc lưu ra file riêng và import từ file server config).

> 🇬🇧 *At minimum, the server requires the `operator` JWT, which we have pointed at directly, and a resolver.*

Tối thiểu, server cần JWT `operator` được trỏ trực tiếp và một resolver.

e.g.
```shell
nsc generate config --nats-resolver > resolver.conf
```

> 🇬🇧 *And example server config `myconfig.cfg`*

Ví dụ file cấu hình server `myconfig.cfg`:

```
server_name: servertest
listen: 127.0.0.1:4222
http: 8222

jetstream: enabled

include resolver.conf
```

> 🇬🇧 *Now start this local test server using `nats-server -c myconfig.cfg`*

Khởi động server test cục bộ bằng `nats-server -c myconfig.cfg`.

> 🇬🇧 *The nats-server requires a designated account for operations and monitoring of the server, cluster, or supercluster. If you see this error message:*

nats-server yêu cầu một account chỉ định để vận hành và giám sát server, cluster, hoặc supercluster. Nếu thấy thông báo lỗi sau:

`nats-server: using nats based account resolver - the system account needs to be specified in configuration or the operator jwt`&#x20;

> 🇬🇧 *Then there is no system account to interact with the server and you need to add one to the configuration or operator JWT. Let's add one to the operator JWT using `nsc`:*

Thì chưa có system account để tương tác với server — bạn cần thêm vào cấu hình hoặc operator JWT. Thêm vào operator JWT bằng `nsc`:

```shell
nsc add account -n SYS`
nsc edit operator --system-account SYS
```
(và tạo lại `resolver.conf`)

> 🇬🇧 *Now start the local test server using: `nats-server -c myconfig.cfg`*

Khởi động server test cục bộ bằng: `nats-server -c myconfig.cfg`

## Đẩy thay đổi nsc cục bộ lên NATS server

> 🇬🇧 *In order for the nats servers to know about the account(s) you have created or changes to the attributes for those accounts, you need to push any new accounts or any changes to account attributes you may have done locally using `nsc` into the built-in account resolver of the nats-server. You can do this using `nsc push`:*

Để nats-server nhận biết account mới tạo hoặc thay đổi thuộc tính account, bạn cần đẩy các thay đổi cục bộ (thực hiện qua `nsc`) vào built-in account resolver của nats-server bằng `nsc push`:

> 🇬🇧 *For example to push the account named 'MyAccount' that you have just created into the nats server running locally on your machine use:*

Ví dụ, để đẩy account 'MyAccount' vừa tạo lên nats-server đang chạy cục bộ:

```shell
nsc push -a MyAccount -u nats://localhost
```

> 🇬🇧 *You can also use `nsc pull -u nats://localhost` to pull the view of the accounts that the local NATS server has into your local nsc copy (i.e. in `~/.nsc`)*

Bạn cũng có thể dùng `nsc pull -u nats://localhost` để kéo trạng thái account từ NATS server cục bộ về bản sao nsc cục bộ (tức là vào `~/.nsc`).

> 🇬🇧 *As soon as you 'push' an the account JWT to the server (that server's built-in NATS account resolver will take care of distributing that new (or new version of) the account JWT to the other nats servers in the cluster) then the changes will take effect and for example any users you may have created with that account will then be able to connect to any of the nats server in the cluster using the user's JWT.*

Ngay khi bạn 'push' account JWT lên server, built-in NATS account resolver sẽ tự phân phối JWT đó (hoặc phiên bản mới của nó) tới các nats-server khác trong cluster. Các thay đổi có hiệu lực ngay lập tức — ví dụ, mọi user được tạo trong account đó đều có thể kết nối tới bất kỳ nats-server nào trong cluster bằng user JWT của họ.

## Kiểm tra Client

> 🇬🇧 *Install the `nats` CLI Tool if you haven't already.*

Cài CLI tool `nats` nếu chưa có.

> 🇬🇧 *Create a subscriber:*

Tạo một subscriber:

```shell
nats sub --creds ~/.nkeys/creds/MyOperator/MyAccount/MyUser.creds ">"
```

> 🇬🇧 *Publish a message:*

Publish một message:

```shell
nats pub --creds ~/.nkeys/creds/MyOperator/MyAccount/MyUser.creds hello NATS 
```

> 🇬🇧 *Subscriber shows:*

Subscriber hiển thị:

```text
Received on [hello]: ’NATS’
```

### Tạo context `nats`

> 🇬🇧 *If you are going to use those credentials with `nats` you should create a context so you don't have to pass the connection and authentication arguments each time:*

Nếu dùng credentials với `nats`, hãy tạo context để không phải truyền các tham số kết nối và xác thực mỗi lần:

```shell
nats context add myuser --creds ~/.nkeys/creds/MyOperator/MyAccount/MyUser.creds
```

### NSC tích hợp sẵn công cụ NATS

> 🇬🇧 *To make it easier to work, you can use the NATS clients built right into NSC. These tools know how to find the credential files in the keyring. For convenience, the tools are aliased to `sub`, `pub`, `req`, `reply`:*

Để tiện làm việc, bạn có thể dùng NATS client được tích hợp sẵn trong NSC. Các công cụ này tự động tìm credential file trong keyring. Chúng được aliased thành `sub`, `pub`, `req`, `reply`:

```bash
nsc sub --user MyUser ">"
...

nsc pub --user MyUser hello NATS
...
```

> 🇬🇧 *See `nsc tool -h` for more detailed information.*

Xem `nsc tool -h` để biết thêm chi tiết.

## Phân quyền User

> 🇬🇧 *User authorization, as expected, also works with JWT authentication. With `nsc` you can specify authorization for specific subjects to which the user can or cannot publish or subscribe. By default a user doesn't have any limits on the subjects that it can publish or subscribe to. Any message stream or message published in the account is subscribable by the user. The user can also publish to any subject or imported service. Note that authorization, if configured, must be specified on a per user basis.*

Phân quyền user hoạt động bình thường với xác thực JWT. Dùng `nsc` để chỉ định permission cho các subject cụ thể mà user được hoặc không được publish/subscribe. Mặc định, user không bị giới hạn subject nào — có thể subscribe mọi stream hoặc message trong account, và publish tới bất kỳ subject hay imported service nào. Lưu ý: nếu cấu hình phân quyền, phải chỉ định riêng cho từng user.

> 🇬🇧 *When specifying limits it is important to remember that clients by default use generated "inboxes" to allow publish requests. When specifying subscribe and publish permissions, you need to enable clients to subscribe and publish to `_INBOX.>`. You can further restrict it, but you'll be responsible for segmenting the subject space so as to not break request-reply communications between clients.*

Khi đặt giới hạn, cần nhớ rằng client mặc định dùng "inbox" tự sinh để xử lý publish request. Khi cấu hình permission subscribe và publish, phải cho phép client subscribe và publish tới `_INBOX.>`. Bạn có thể hạn chế thêm, nhưng cần tự đảm bảo phân vùng subject space sao cho không phá vỡ giao tiếp request-reply giữa các client.

> 🇬🇧 *Let's say you have a service that your account clients can make requests to under `q`. To enable the service to receive and respond to requests it requires permissions to subscribe to `q` and publish permissions under `_INBOX.>`:*

Giả sử bạn có service mà account client gửi request tới qua `q`. Để service nhận và phản hồi request, nó cần permission subscribe tới `q` và permission publish dưới `_INBOX.>`:

```bash
nsc add user s --allow-pub "_INBOX.>" --allow-sub q
```
```text
[ OK ] added pub pub "_INBOX.>"
[ OK ] added sub "q"
[ OK ] generated and stored user key "UDYQFIF75SQU2NU3TG4JXJ7C5LFCWAPXX5SSRB276YQOOFXHFIGHXMEL"
[ OK ] generated user creds file `~/.nkeys/creds/MyOperator/MyAccount/s.creds`
[ OK ] added user "s" to account "MyAccount"
```

```shell
nsc describe user s
```
```text
+---------------------------------------------------------------------------------+
|                                      User                                       |
+----------------------+----------------------------------------------------------+
| Name                 | s                                                        |
| User ID              | UDYQFIF75SQU2NU3TG4JXJ7C5LFCWAPXX5SSRB276YQOOFXHFIGHXMEL |
| Issuer ID            | AD2M34WBNGQFYK37IDX53DPRG74RLLT7FFWBOBMBUXMAVBCVAU5VKWIY |
| Issued               | 2021-10-27 23:23:16 UTC                                  |
| Expires              |                                                          |
| Bearer Token         | No                                                       |
+----------------------+----------------------------------------------------------+
| Pub Allow            | _INBOX.>                                                 |
| Sub Allow            | q                                                        |
| Response Permissions | Not Set                                                  |
+----------------------+----------------------------------------------------------+
| Max Msg Payload      | Unlimited                                                |
| Max Data             | Unlimited                                                |
| Max Subs             | Unlimited                                                |
| Network Src          | Any                                                      |
| Time                 | Any                                                      |
+----------------------+----------------------------------------------------------+
```

> 🇬🇧 *As you can see, this client is now limited to publishing responses to `_INBOX.>` addresses and subscribing to the service's request subject.*

Client này hiện chỉ được publish response tới địa chỉ `_INBOX.>` và subscribe subject request của service.

> 🇬🇧 *Similarly, we can limit a client:*

Tương tự, có thể giới hạn một client:

```bash
nsc add user c --allow-pub q --allow-sub "_INBOX.>"
```
```text
[ OK ] added pub pub "q"
[ OK ] added sub "_INBOX.>"
[ OK ] generated and stored user key "UDIRTIVVHCW2FLLDHTS27ENXLVNP4EO4Z5MR7FZUNXFXWREPGQJ4BRRE"
[ OK ] generated user creds file `~/.nkeys/creds/MyOperator/MyAccount/c.creds`
[ OK ] added user "c" to account "MyAccount"
```

> 🇬🇧 *Lets look at that new user*

Xem user mới:

```shell
nsc describe user c
```
```text
+---------------------------------------------------------------------------------+
|                                      User                                       |
+----------------------+----------------------------------------------------------+
| Name                 | c                                                        |
| User ID              | UDIRTIVVHCW2FLLDHTS27ENXLVNP4EO4Z5MR7FZUNXFXWREPGQJ4BRRE |
| Issuer ID            | AD2M34WBNGQFYK37IDX53DPRG74RLLT7FFWBOBMBUXMAVBCVAU5VKWIY |
| Issued               | 2021-10-27 23:26:09 UTC                                  |
| Expires              |                                                          |
| Bearer Token         | No                                                       |
+----------------------+----------------------------------------------------------+
| Pub Allow            | q                                                        |
| Sub Allow            | _INBOX.>                                                 |
| Response Permissions | Not Set                                                  |
+----------------------+----------------------------------------------------------+
| Max Msg Payload      | Unlimited                                                |
| Max Data             | Unlimited                                                |
| Max Subs             | Unlimited                                                |
| Network Src          | Any                                                      |
| Time                 | Any                                                      |
+----------------------+----------------------------------------------------------+
```

> 🇬🇧 *The client has the opposite permissions of the service. It can publish on the request subject `q`, and receive replies on an inbox.*

Client có permission ngược lại với service: publish trên subject request `q` và nhận reply qua inbox.

## Môi trường NSC

> 🇬🇧 *As your projects become more involved, you may work with one or more accounts. NSC tracks your current operator and account. If you are not in a directory containing an operator, account or user, it will use the last operator/account context.*

Khi dự án phức tạp hơn, bạn có thể làm việc với nhiều account. NSC theo dõi operator và account hiện tại. Nếu bạn không ở trong thư mục chứa operator, account hay user, NSC sẽ dùng context operator/account gần nhất.

> 🇬🇧 *To view your current environment:*

Xem môi trường hiện tại:

```shell
nsc env
```
```text
+------------------------------------------------------------------------------------------------------+
|                                           NSC Environment                                            |
+--------------------+-----+---------------------------------------------------------------------------+
| Setting            | Set | Effective Value                                                           |
+--------------------+-----+---------------------------------------------------------------------------+
| $NSC_CWD_ONLY      | No  | If set, default operator/account from cwd only                            |
| $NSC_NO_GIT_IGNORE | No  | If set, no .gitignore files written                                       |
| $NKEYS_PATH        | No  | ~/.nkeys                                                                  |
| $NSC_HOME          | No  | ~/.nsc                                                                    |
| Config             |     | ~/.nsc/nsc.json                                                           |
| $NATS_CA           | No  | If set, root CAs in the referenced file will be used for nats connections |
|                    |     | If not set, will default to the system trust store                        |
+--------------------+-----+---------------------------------------------------------------------------+
| From CWD           |     | No                                                                        |
| Stores Dir         |     | ~/.nsc/nats                                                               |
| Default Operator   |     | MyOperator                                                                |
| Default Account    |     | MyAccount                                                                 |
| Root CAs to trust  |     | Default: System Trust Store                                               |
+--------------------+-----+---------------------------------------------------------------------------+
```

> 🇬🇧 *If you have multiple accounts, you can use `nsc env --account <account name>` to set the account as the current default. If you have defined `NKEYS_PATH` or `NSC_HOME` in the environment, you'll also see their current effective values. Finally, if you want to set the stores directory to anything other than the default, you can do `nsc env --store <dir containing an operator>`. If you have multiple accounts, you can try having multiple terminals, each in a directory for a different account.*

Nếu có nhiều account, dùng `nsc env --account <account name>` để đặt account mặc định hiện tại. Nếu đã định nghĩa `NKEYS_PATH` hoặc `NSC_HOME` trong môi trường, bạn cũng sẽ thấy giá trị hiệu lực của chúng. Nếu muốn đặt stores directory khác mặc định, dùng `nsc env --store <dir containing an operator>`. Với nhiều account, có thể mở nhiều terminal, mỗi terminal ở trong thư mục của một account khác nhau.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **credential**: thông tin đăng nhập
- **message**: gói dữ liệu được gửi đi
- **permission**: quyền truy cập
- **publisher**: bên gửi message
- **secret**: chuỗi bí mật
- **server**: máy chủ
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **subscriber**: bên đăng ký nhận message
- **token**: chuỗi xác thực