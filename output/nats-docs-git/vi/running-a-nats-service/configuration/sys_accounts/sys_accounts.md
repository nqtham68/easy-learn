---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/sys_accounts/sys_accounts
title: System Events & Hướng Dẫn Decentralized JWT
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# System Events & Hướng Dẫn Decentralized JWT

## Bật System Events với Decentralized Authentication/Authorization

> 🇬🇧 *To enable and access system events, you'll have to:*
> *- Create an Operator, Account and User*
> *- Run a NATS Account Server (or Memory Resolver)*

Để bật và truy cập system events, bạn cần:

- Tạo Operator, Account và User
- Chạy NATS Account Server (hoặc Memory Resolver)

### Tạo Operator, Account, User

> 🇬🇧 *Let's create an operator, system account and system account user:*

Hãy tạo operator, system account và user cho system account:

```shell
nsc add operator -n SAOP
```

```text
Generated operator key - private key stored "~/.nkeys/SAOP/SAOP.nk"
Success! - added operator "SAOP"
```

> 🇬🇧 *Add the system account*

Thêm system account

```shell
nsc add account -n SYS
```

```text
Generated account key - private key stored "~/.nkeys/SAOP/accounts/SYS/SYS.nk"
Success! - added account "SYS"
```

> 🇬🇧 *Add a system account user*

Thêm user cho system account

```shell
nsc add user -n SYSU
```

```text
Generated user key - private key stored "~/.nkeys/SAOP/accounts/SYS/users/SYSU.nk"
Generated user creds file "~/.nkeys/SAOP/accounts/SYS/users/SYSU.creds"
Success! - added user "SYSU" to "SYS"
```

> 🇬🇧 *By default, the operator JWT can be found in `~/.nsc/nats/<operator_name>/<operator.name>.jwt`.*

Mặc định, operator JWT được lưu tại `~/.nsc/nats/<operator_name>/<operator.name>.jwt`.

### NATS-Account-Server

> 🇬🇧 *To vend the credentials to the nats-server, we'll use a [nats-account-server](https://docs.nats.io/legacy/nas). Let's start a nats-account-server to serve the JWT credentials:*

Để cung cấp credential (thông tin đăng nhập) cho nats-server, ta dùng [nats-account-server](https://docs.nats.io/legacy/nas). Khởi động nats-account-server để phục vụ JWT credentials:

```shell
nats-account-server -nsc ~/.nsc/nats/SAOP
```

> 🇬🇧 *The server will by default vend JWT configurations on the an endpoint at: `http(s)://<server_url>/jwt/v1/accounts/`.*

Mặc định, server sẽ cung cấp JWT configurations qua endpoint tại: `http(s)://<server_url>/jwt/v1/accounts/`.

### Cấu Hình NATS Server

> 🇬🇧 *The server configuration will need:*
> *- The operator JWT - (`~/.nsc/nats/<operator_name>/<operator.name>.jwt`)*
> *- The URL where the server can resolve accounts (`http://localhost:9090/jwt/v1/accounts/`)*
> *- The public key of the `system_account`*

Config của server cần có:

- Operator JWT - \(`~/.nsc/nats/<operator_name>/<operator.name>.jwt`\)
- URL để server resolve accounts \(`http://localhost:9090/jwt/v1/accounts/`\)
- Public key của `system_account`

> 🇬🇧 *The only thing we don't have handy is the public key for the system account. We can get it easy enough:*

Thứ duy nhất chưa có sẵn là public key của system account. Lấy nó như sau:

```shell
nsc list accounts
```

```text
╭─────────────────────────────────────────────────────────────────╮
│                            Accounts                             │
├──────┬──────────────────────────────────────────────────────────┤
│ Name │ Public Key                                               │
├──────┼──────────────────────────────────────────────────────────┤
│ SYS  │ ADWJVSUSEVC2GHL5GRATN2LOEOQOY2E6Z2VXNU3JEIK6BDGPWNIW3AXF │
╰──────┴──────────────────────────────────────────────────────────╯
```

> 🇬🇧 *Because the server has additional resolver implementations, you need to enclose the server url like: `URL(<url>)`.*

Do server có các resolver implementation bổ sung, bạn cần bao URL của server như sau: `URL(<url>)`.

> 🇬🇧 *Let's create server config with the following contents and save it to `server.conf`:*

Tạo server config với nội dung sau và lưu vào `server.conf`:

```text
operator: /Users/synadia/.nsc/nats/SAOP/SAOP.jwt
system_account: ADWJVSUSEVC2GHL5GRATN2LOEOQOY2E6Z2VXNU3JEIK6BDGPWNIW3AXF
resolver: URL(http://localhost:9090/jwt/v1/accounts/)
```

> 🇬🇧 *Let's start the nats-server:*

Khởi động nats-server:

```shell
nats-server -c server.conf
```

## Kiểm Tra Server Events

> 🇬🇧 *Let's add a subscriber for all the events published by the system account:*

Thêm một subscriber (bên đăng ký nhận message) để lắng nghe tất cả events được publish bởi system account:

```shell
nats sub --creds ~/.nkeys/SAOP/accounts/SYS/users/SYSU.creds ">"
```

> 🇬🇧 *Very quickly we'll start seeing messages from the server as they are published by the NATS server. As should be expected, the messages are just JSON, so they can easily be inspected even if just using a simple `nats sub` to read them.*

Chỉ trong chốc lát, bạn sẽ thấy các message từ server được NATS server publish. Như kỳ vọng, các message đều ở dạng JSON nên có thể dễ dàng kiểm tra, kể cả chỉ dùng `nats sub` đơn giản để đọc chúng.

> 🇬🇧 *To see an account update:*

Để xem một account update:

```shell
nats pub --creds ~/.nkeys/SAOP/accounts/SYS/users/SYSU.creds foo bar
```

> 🇬🇧 *The subscriber will print the connect and disconnect:*

Subscriber sẽ in ra sự kiện connect và disconnect:

```json
{
  "server": {
    "host": "0.0.0.0",
    "id": "NBTGVY3OKDKEAJPUXRHZLKBCRH3LWCKZ6ZXTAJRS2RMYN3PMDRMUZWPR",
    "ver": "2.0.0-RC5",
    "seq": 32,
    "time": "2019-05-03T14:53:15.455266-05:00"
  },
  "acc": "ADWJVSUSEVC2GHL5GRATN2LOEOQOY2E6Z2VXNU3JEIK6BDGPWNIW3AXF",
  "conns": 1,
  "total_conns": 1
}
{
  "server": {
    "host": "0.0.0.0",
    "id": "NBTGVY3OKDKEAJPUXRHZLKBCRH3LWCKZ6ZXTAJRS2RMYN3PMDRMUZWPR",
    "ver": "2.0.0-RC5",
    "seq": 33,
    "time": "2019-05-03T14:53:15.455304-05:00"
  },
  "client": {
    "start": "2019-05-03T14:53:15.453824-05:00",
    "host": "127.0.0.1",
    "id": 6,
    "acc": "ADWJVSUSEVC2GHL5GRATN2LOEOQOY2E6Z2VXNU3JEIK6BDGPWNIW3AXF",
    "user": "UACPEXCAZEYWZK4O52MEGWGK4BH3OSGYM3P3C3F3LF2NGNZUS24IVG36",
    "name": "NATS Sample Publisher",
    "lang": "go",
    "ver": "1.7.0",
    "stop": "2019-05-03T14:53:15.45526-05:00"
  },
  "sent": {
    "msgs": 1,
    "bytes": 3
  },
  "received": {
    "msgs": 0,
    "bytes": 0
  },
  "reason": "Client Closed"
}
```

## User Services

### `$SYS.REQ.USER.INFO` - Lấy Thông Tin User Đang Kết Nối

> 🇬🇧 *For the active connection, get basic user information including the account name, permissions, and expiry, if applicable. Note, this works with any connected user, not just a system account user.*

Với kết nối đang hoạt động, lấy thông tin cơ bản của user bao gồm tên account, permission (quyền truy cập) và thời hạn hết hạn nếu có. Lưu ý: service này hoạt động với bất kỳ user nào đang kết nối, không chỉ user của system account.

```shell
nats request --creds ~/.nkeys/SAOP/accounts/SYS/users/SYSU.creds \$SYS.REQ.USER.INFO ""
```

```text
Published [$SYS.REQ.USER.INFO] : ''
Received  [_INBOX.DQD44ugVt0O4Ur3pWIOOD1.WQOBevoq] : '{
  "user": "UACPEXCAZEYWZK4O52MEGWGK4BH3OSGYM3P3C3F3LF2NGNZUS24IVG36",
  "account": "ADWJVSUSEVC2GHL5GRATN2LOEOQOY2E6Z2VXNU3JEIK6BDGPWNIW3AXF"
}'
```

## System Services

### `$SYS.REQ.SERVER.PING.IDZ` - Khám Phá Các Server

> 🇬🇧 *To discover servers in the cluster to get their ID and name, publish a request to `$SYS.REQ.SERVER.PING.IDZ`.*

Để khám phá các server trong cluster (cụm nhiều server chạy chung) và lấy ID cùng tên của chúng, publish một request tới `$SYS.REQ.SERVER.PING.IDZ`.

```shell
nats request --creds ~/.nkeys/SAOP/accounts/SYS/users/SYSU.creds \$SYS.REQ.SERVER.PING.IDZ ""
```

```text
Published [$SYS.REQ.SERVER.PING.IDZ] : ''
Received  [_INBOX.DQD44ugVt0O4Ur3pWIOOD1.WQOBevoq] : '{
  "host": "0.0.0.0",
  "id": "NC7AKPQRC6CIZGWRJOTVFIGVSL7VW7WXTQCTUJFNG7HTCMCKQTGE5PUL",
  "name": "n1"
}'
```

### `$SYS.REQ.SERVER.PING` - Khám Phá Server + Stats

> 🇬🇧 *To discover servers in the cluster, and get a small health summary, publish a request to `$SYS.REQ.SERVER.PING`. Note that while the example below uses `nats-req`, only the first answer for the request will be printed. You can easily modify the example to wait until no additional responses are received for a specific amount of time, thus allowing for all responses to be collected.*

Để khám phá server trong cluster và lấy tóm tắt health check, publish request tới `$SYS.REQ.SERVER.PING`. Lưu ý: ví dụ dưới đây dùng `nats-req` nhưng chỉ in ra response đầu tiên. Bạn có thể chỉnh sửa để chờ đến khi không còn response nào mới trong một khoảng thời gian nhất định, qua đó thu thập toàn bộ response.

```shell
nats request --creds ~/.nkeys/SAOP/accounts/SYS/users/SYSU.creds \$SYS.REQ.SERVER.PING ""
```

```text
Published [$SYS.REQ.SERVER.PING] : ''
Received  [_INBOX.G5mbsf0k7l7nb4eWHa7GTT.omklmvnm] : '{
  "server": {
    "host": "0.0.0.0",
    "id": "NCZQDUX77OSSTGN2ESEOCP4X7GISMARX3H4DBGZBY34VLAI4TQEPK6P6",
    "ver": "2.0.0-RC9",
    "seq": 47,
    "time": "2019-05-02T14:02:46.402166-05:00"
  },
  "statsz": {
    "start": "2019-05-02T13:41:01.113179-05:00",
    "mem": 12922880,
    "cores": 20,
    "cpu": 0,
    "connections": 2,
    "total_connections": 2,
    "active_accounts": 1,
    "subscriptions": 10,
    "sent": {
      "msgs": 7,
      "bytes": 2761
    },
    "received": {
      "msgs": 0,
      "bytes": 0
    },
    "slow_consumers": 0
  }
}'
```

### `$SYS.REQ.SERVER.<id>.STATSZ` - Lấy Stats Summary của Server

> 🇬🇧 *If you know the server id for a particular server (such as from a response to `$SYS.REQ.SERVER.PING`), you can query the specific server for its health information:*

Nếu biết server id của một server cụ thể (chẳng hạn từ response của `$SYS.REQ.SERVER.PING`), bạn có thể truy vấn thông tin health của server đó:

```shell
nats request --creds ~/.nkeys/SAOP/accounts/SYS/users/SYSU.creds \$SYS.REQ.SERVER.NC7AKPQRC6CIZGWRJOTVFIGVSL7VW7WXTQCTUJFNG7HTCMCKQTGE5PUL.STATSZ ""
```

```text
Published [$SYS.REQ.SERVER.NC7AKPQRC6CIZGWRJOTVFIGVSL7VW7WXTQCTUJFNG7HTCMCKQTGE5PUL.STATSZ] : ''
Received  [_INBOX.DQD44ugVt0O4Ur3pWIOOD1.WQOBevoq] : '{
  "server": {
    "host": "0.0.0.0",
    "id": "NC7AKPQRC6CIZGWRJOTVFIGVSL7VW7WXTQCTUJFNG7HTCMCKQTGE5PUL",
    "ver": "2.0.0-RC5",
    "seq": 25,
    "time": "2019-05-03T14:34:02.066077-05:00"
  },
  "statsz": {
    "start": "2019-05-03T14:32:19.969037-05:00",
    "mem": 11874304,
    "cores": 20,
    "cpu": 0,
    "connections": 2,
    "total_connections": 4,
    "active_accounts": 1,
    "subscriptions": 10,
    "sent": {
      "msgs": 26,
      "bytes": 9096
    },
    "received": {
      "msgs": 2,
      "bytes": 0
    },
    "slow_consumers": 0
  }
}'
```

### `$SYS.REQ.SERVER.<id>.PROFILEZ` - Lấy Thông Tin Profiling

> 🇬🇧 *If profiling is enabled for a server, this service enables requesting it from the server. The request payload must specify the name of the profile being requested with an optional debug level, including:*

Nếu profiling được bật cho server, service này cho phép request thông tin profiling từ server. payload (nội dung chính của message) của request phải chỉ định tên profile cần lấy cùng debug level tùy chọn, bao gồm:

- `allocs` - 0, 1
- `block` - 0
- `goroutine` - 0, 1, 2
- `heap` - 0, 1
- `mutex` - 0
- `threadcount` - 0

```shell
nats request --creds ~/.nkeys/SAOP/accounts/SYS/users/SYSU.creds \$SYS.REQ.SERVER.NC7AKPQRC6CIZGWRJOTVFIGVSL7VW7WXTQCTUJFNG7HTCMCKQTGE5PUL.PROFILEZ '{"name": "heap", "debug": 1}'
```

```text
Published [$SYS.REQ.SERVER.NC7AKPQRC6CIZGWRJOTVFIGVSL7VW7WXTQCTUJFNG7HTCMCKQTGE5PUL.PROFILEZ] : '{
  "name": "heap",
  "debug": 1
}'
Received  [_INBOX.DQD44ugVt0O4Ur3pWIOOD1.WQOBevoq] : '{
  "profile": "<base64-encoded profile output>"
}'
```

### `$SYS.REQ.SERVER.<id>.RELOAD` - Hot Reload Cấu Hình

> 🇬🇧 *Sending a request to this service will attempt to hot reload the server configuration, akin to `nats-server --signal reload`. If there are errors with the new configuration, they will be returned in an `error` field in the response.*

Gửi request tới service này sẽ thực hiện hot reload config của server, tương tự như `nats-server --signal reload`. Nếu config mới có lỗi, chúng sẽ được trả về trong trường `error` của response.

```shell
nats request --creds ~/.nkeys/SAOP/accounts/SYS/users/SYSU.creds \$SYS.REQ.SERVER.NC7AKPQRC6CIZGWRJOTVFIGVSL7VW7WXTQCTUJFNG7HTCMCKQTGE5PUL.RELOAD ''
```

```text
Published [$SYS.REQ.SERVER.NC7AKPQRC6CIZGWRJOTVFIGVSL7VW7WXTQCTUJFNG7HTCMCKQTGE5PUL.RELOAD] : ''
Received  [_INBOX.DQD44ugVt0O4Ur3pWIOOD1.WQOBevoq] : '{
  "server": {
    "host": "0.0.0.0",
    "id": "NC7AKPQRC6CIZGWRJOTVFIGVSL7VW7WXTQCTUJFNG7HTCMCKQTGE5PUL",
    "ver": "2.10.0-RC5",
    "seq": 25,
    "time": "2023-09-19T14:34:02.066077-04:00"
  }
}'
```

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **endpoint**: địa chỉ API cụ thể
- **payload**: nội dung chính của message
- **permission**: quyền truy cập
- **request**: yêu cầu
- **response**: phản hồi
- **service**: dịch vụ
- **subscriber**: bên đăng ký nhận message