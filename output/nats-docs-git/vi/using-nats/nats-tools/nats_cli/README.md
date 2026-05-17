---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nats_cli
title: Công cụ dòng lệnh nats
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Công cụ dòng lệnh nats

> 🇬🇧 *A command line utility to interact with and manage NATS.*

Đây là CLI (công cụ dòng lệnh) để tương tác và quản lý NATS.

> 🇬🇧 *This utility replaces various past tools that were named in the form `nats-sub` and `nats-pub`, adds several new capabilities and supports full JetStream management.*

Tiện ích này thay thế các công cụ cũ có tên dạng `nats-sub` và `nats-pub`, bổ sung nhiều tính năng mới và hỗ trợ quản lý JetStream đầy đủ.

> 🇬🇧 *Check out the repo for all the details: [github.com/nats-io/natscli](https://github.com/nats-io/natscli).*

Xem toàn bộ chi tiết tại: [github.com/nats-io/natscli](https://github.com/nats-io/natscli).

## Cài đặt `nats`

> 🇬🇧 *Please refer to the [installation section in the readme](https://github.com/nats-io/natscli?tab=readme-ov-file#installation).*

Tham khảo [phần cài đặt trong readme](https://github.com/nats-io/natscli?tab=readme-ov-file#installation).

> 🇬🇧 *You can read about execution policies [here](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies).*

Tìm hiểu về execution policies [tại đây](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies).

> 🇬🇧 *Binaries are also available as [GitHub Releases](https://github.com/nats-io/natscli/releases).*

Binary (file chương trình đã biên dịch) cũng có sẵn dưới dạng [GitHub Releases](https://github.com/nats-io/natscli/releases).

## Sử dụng `nats`

### Tìm kiếm trợ giúp

* [NATS Command Line Interface README](https://github.com/nats-io/natscli#readme)
* `nats help`
* `nats help [<command>...]` hoặc `nats [<command>...] --help`
* Nhớ xem các cheat sheet!
  * `nats cheat`
  * `nats cheat --sections`
  * `nats cheat <section>>`

### Tương tác với NATS

* `nats context`
* `nats account`
* `nats pub`
* `nats sub`
* `nats request`
* `nats reply`
* `nats bench`

### Giám sát NATS

* `nats events`
* `nats rtt`
* `nats server`
* `nats latency`
* `nats governor`

### Quản lý và tương tác với stream

* `nats stream`
* `nats consumer`
* `nats backup`
* `nats restore`

### Quản lý và tương tác với K/V Store

* `nats kv`

### Xem thông tin tham chiếu

* `nats errors`
* `nats schema`

## Configuration Contexts

> 🇬🇧 *The CLI has a number of configuration settings that can be passed either as command line arguments or set in environment variables.*

CLI có nhiều cài đặt config (cấu hình) có thể truyền qua tham số dòng lệnh hoặc đặt trong biến môi trường.

```shell
nats --help
```

Output extract

```
...
  -s, --server=URL              NATS server urls ($NATS_URL)
      --user=USER               Username or Token ($NATS_USER)
      --password=PASSWORD       Password ($NATS_PASSWORD)
      --creds=FILE              User credentials ($NATS_CREDS)
      --nkey=FILE               User NKEY ($NATS_NKEY)
      --tlscert=FILE            TLS public certificate ($NATS_CERT)
      --tlskey=FILE             TLS private key ($NATS_KEY)
      --tlsca=FILE              TLS certificate authority chain ($NATS_CA)
      --socks-proxy=PROXY       SOCKS5 proxy for connecting to NATS server
                                ($NATS_SOCKS_PROXY)
      --colors=SCHEME           Sets a color scheme to use ($NATS_COLOR)
      --timeout=DURATION        Time to wait on responses from NATS
                                ($NATS_TIMEOUT)
      --context=NAME            Configuration context ($NATS_CONTEXT)
...
```

> 🇬🇧 *The server URL can be set using the `--server` CLI flag, or the `NATS_URL` environment variable, or using [NATS Contexts](.#nats-contexts).*

URL của server có thể được đặt qua cờ CLI `--server`, biến môi trường `NATS_URL`, hoặc dùng [NATS Contexts](.#nats-contexts).

> 🇬🇧 *The password can be set using the `--password` CLI flag, or the `NATS_PASSWORD` environment variable, or using [NATS Contexts](.#nats-contexts). For example: if you want to create a script that prompts the user for the system user password (so that for example it doesn't appear in `ps` or `history` or maybe you don't want it stored in the profile) and then execute one or more `nats` commands you do something like:*

Password có thể đặt qua cờ CLI `--password`, biến môi trường `NATS_PASSWORD`, hoặc dùng [NATS Contexts](.#nats-contexts). Ví dụ: để tạo script yêu cầu người dùng nhập password của system user (tránh hiển thị trong `ps` hay `history`, hoặc không muốn lưu vào profile) rồi thực thi một hay nhiều lệnh `nats`, bạn làm như sau:

```shell
#!/bin/bash
echo "-n" "system user password: "
read -s NATS_PASSWORD
export NATS_PASSWORD
nats server report jetstream --user system
```

### NATS Contexts

> 🇬🇧 *A context is a named configuration that stores all of these settings. You can designate a default context and switch between contexts.*

Một context là một config được đặt tên, lưu trữ tất cả các cài đặt trên. Bạn có thể chỉ định context mặc định và chuyển đổi giữa các context.

> 🇬🇧 *A context can be created with `nats context create my_context_name` and then modified with`nats context edit my_context_name`:*

Context có thể tạo bằng `nats context create my_context_name` và chỉnh sửa bằng `nats context edit my_context_name`:

```json
{
  "description": "",
  "url": "nats://127.0.0.1:4222",
  "token": "",
  "user": "",
  "password": "",
  "creds": "",
  "nkey": "",
  "cert": "",
  "key": "",
  "ca": "",
  "nsc": "",
  "jetstream_domain": "",
  "jetstream_api_prefix": "",
  "jetstream_event_prefix": "",
  "inbox_prefix": "",
  "user_jwt": ""
}
```

> 🇬🇧 *This context is stored in the file `~/.config/nats/context/my_context_name.json`.*

Context này được lưu trong file `~/.config/nats/context/my_context_name.json`.

> 🇬🇧 *A context can also be created by specifying settings with `nats context save`*

Context cũng có thể tạo bằng cách chỉ định các cài đặt với `nats context save`

```shell
nats context save example --server nats://nats.example.net:4222 --description 'Example.Net Server'
nats context save local --server nats://localhost:4222 --description 'Local Host' --select 
```

List your contexts

```shell
nats context ls
```

```
Known contexts:

   example             Example.Net Server
   local*              Local Host
```

> 🇬🇧 *We passed `--select` to the `local` one meaning it will be the default when nothing is set.*

Ta truyền `--select` vào `local`, nghĩa là context này sẽ là mặc định khi không có gì được đặt.

Select a context

```shell
nats context select
```

> 🇬🇧 *Check the round trip time to the server (using the currently selected context)*

Kiểm tra round trip time tới server (dùng context đang được chọn)

```shell
nats rtt
```

```
nats://localhost:4222:

   nats://127.0.0.1:4222: 245.115µs
       nats://[::1]:4222: 390.239µs
```

> 🇬🇧 *You can also specify a context directly*

Bạn cũng có thể chỉ định context trực tiếp

```shell
nats rtt --context example
```

```
nats://nats.example.net:4222:

   nats://192.0.2.10:4222: 41.560815ms
   nats://192.0.2.11:4222: 41.486609ms
   nats://192.0.2.12:4222: 41.178009ms
```

> 🇬🇧 *All `nats` commands are context aware and the `nats context` command has various commands to view, edit and remove contexts.*

Tất cả lệnh `nats` đều nhận biết context, và lệnh `nats context` cung cấp các lệnh con để xem, chỉnh sửa và xóa context.

> 🇬🇧 *Server URLs and Credential paths can be resolved via the `nsc` command by specifying an URL, for example to find user `new` within the `orders` account of the `acme` operator you can use this:*

URL server và đường dẫn credential (thông tin đăng nhập) có thể được phân giải qua lệnh `nsc` bằng cách chỉ định URL. Ví dụ, để tìm user `new` trong account `orders` của operator `acme`, dùng lệnh:

```shell
nats context save example --description 'Example.Net Server' --nsc nsc://acme/orders/new
```

> 🇬🇧 *The server list and credentials path will now be resolved via `nsc`, if these are specifically set in the context, the specific context configuration will take precedence.*

Danh sách server và đường dẫn credentials sẽ được phân giải qua `nsc`; nếu các giá trị này được đặt riêng trong context, cấu hình context cụ thể sẽ được ưu tiên.

## Tạo bcrypted passwords

> 🇬🇧 *The server supports hashing of passwords and authentication tokens using `bcrypt`. To take advantage of this, simply replace the plaintext password in the configuration with its `bcrypt` hash, and the server will automatically utilize `bcrypt` as needed. See also: [Bcrypted Passwords](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/auth\_intro/username\_password#bcrypted-passwords).*

Server hỗ trợ băm password và token (chuỗi xác thực) xác thực bằng `bcrypt`. Để dùng tính năng này, chỉ cần thay password dạng plaintext trong config bằng hash `bcrypt` tương ứng, server sẽ tự động sử dụng `bcrypt` khi cần. Xem thêm: [Bcrypted Passwords](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/auth\_intro/username\_password#bcrypted-passwords).

> 🇬🇧 *The `nats` utility has a command for creating `bcrypt` hashes. This can be used for a password or a token in the configuration.*

Tiện ích `nats` có lệnh để tạo hash `bcrypt`. Lệnh này dùng được cho cả password lẫn token trong config.

```shell
nats server passwd
```

```
? Enter password [? for help] **********************
? Reenter password [? for help] **********************

$2a$11$3kIDaCxw.Glsl1.u5nKa6eUnNDLV5HV9tIuUp7EHhMt6Nm9myW1aS
```

> 🇬🇧 *To use the password on the server, add the hash into the server configuration file's authorization section.*

Để dùng password trên server, thêm hash vào phần authorization trong file config của server.

```
  authorization {
    user: derek
    password: $2a$11$3kIDaCxw.Glsl1.u5nKa6eUnNDLV5HV9tIuUp7EHhMt6Nm9myW1aS
  }
```

> 🇬🇧 *Note the client will still have to provide the plain text version of the password, the server however will only store the hash to verify that the password is correct when supplied.*

Lưu ý: client vẫn phải cung cấp password dạng plain text, còn server chỉ lưu hash để xác minh tính đúng đắn khi được cung cấp.

## Xem thêm

> 🇬🇧 *Publish-subscribe pattern using the NATS CLI*

Pattern publish-subscribe sử dụng NATS CLI

[Publish-subscribe Pattern using NATS CLI](https://www.youtube.com/watch?v=jLTVhP08Tq0)

## Thuật ngữ trong bài

- **binary**: file chương trình đã biên dịch
- **CLI**: công cụ dòng lệnh
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **stream**: luồng message lưu trữ liên tục
- **token**: chuỗi xác thực