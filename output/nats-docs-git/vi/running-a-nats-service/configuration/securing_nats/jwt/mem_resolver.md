---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/jwt/mem_resolver
title: Hướng Dẫn Memory Resolver
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Hướng Dẫn Memory Resolver

> 🇬🇧 *The `MEMORY` resolver is a server built-in resolver for account JWTs. If there are a small number of accounts, or they do not change too often this can be a simpler configuration that does not require an external account resolver. Server configuration reload is supported, meaning the preloads can be updated in the server configuration and reloaded without a server restart.*

`MEMORY` resolver là trình phân giải JWT tích hợp sẵn trong server, dùng để xử lý account JWT. Khi số lượng account ít hoặc không thay đổi thường xuyên, đây là lựa chọn config (cấu hình) đơn giản hơn, không cần triển khai external account resolver riêng. Server hỗ trợ reload config mà không cần khởi động lại — chỉ cần cập nhật phần preload trong file config rồi reload là xong.

> 🇬🇧 *The basic configuration for the server requires:*

Config cơ bản cho server cần có:

* Operator JWT
* `resolver` đặt thành `MEMORY`
* `resolver_preload` là một object ánh xạ public key của account sang account JWT tương ứng.

## Tạo Các Thực Thể Cần Thiết

> 🇬🇧 *Let's create the setup:*

Tiến hành thiết lập:

```shell
nsc add operator -n memory
```
```
Generated operator key - private key stored "~/.nkeys/memory/memory.nk"
Success! - added operator "memory"
```

> 🇬🇧 *Add an account 'A'*

Thêm account 'A':

```shell
nsc add account --name A
```
```
Generated account key - private key stored "~/.nkeys/memory/accounts/A/A.nk"
Success! - added account "A"
```

> 🇬🇧 *Describe the account*

Xem thông tin account:

```shell
nsc describe account -W
```
```
╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                   Account Details                                    │
├───────────────────────────┬──────────────────────────────────────────────────────────┤
│ Name                      │ A                                                        │
│ Account ID                │ ACSU3Q6LTLBVLGAQUONAGXJHVNWGSKKAUA7IY5TB4Z7PLEKSR5O6JTGR │
│ Issuer ID                 │ ODWZJ2KAPF76WOWMPCJF6BY4QIPLTUIY4JIBLU4K3YDG3GHIWBVWBHUZ │
│ Issued                    │ 2019-04-30 20:21:34 UTC                                  │
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
│ Exports                   │ None                                                     │
╰───────────────────────────┴──────────────────────────────────────────────────────────╯
```

> 🇬🇧 *Create a new user 'TA'*

Tạo user mới 'TA':

```shell
nsc add user --name TA
```
```
Generated user key - private key stored "~/.nkeys/memory/accounts/A/users/TA.nk"
Generated user creds file "~/.nkeys/memory/accounts/A/users/TA.creds"
Success! - added user "TA" to "A"
```

## Tạo File Config cho Server

> 🇬🇧 *The `nsc` tool can generate a configuration file automatically. You provide a path to the server configuration. The `nsc` tool will generate the server config for you:*

Tool `nsc` có thể tự động tạo file config cho server. Chỉ cần cung cấp đường dẫn đến file config, tool `nsc` sẽ sinh ra nội dung config phù hợp:

```shell
nsc generate config --mem-resolver --config-file /tmp/server.conf 
```

> 🇬🇧 *If you require additional settings, you may want to consider using [`include`](../../README.md#include-directive) in your main configuration, to reference the generated files. Otherwise, you can start a server and reference the generated configuration:*

Nếu cần thêm các tùy chỉnh khác, có thể dùng [`include`](../../README.md#include-directive) trong file config chính để tham chiếu đến các file được sinh ra. Nếu không, có thể khởi động server trực tiếp với file config đó:

```shell
nats-server -c /tmp/server.conf
```

> 🇬🇧 *You can then [test it](./mem_resolver.md#testing-the-configuration).*

Sau đó có thể [kiểm tra cấu hình](./mem_resolver.md#testing-the-configuration).

## Config Thủ Công cho Server

> 🇬🇧 *While generating a configuration file is easy, you may want to craft one by hand to know the details. With the entities created, and a standard location for the `.nsc` directory. You can reference the operator JWT and the account JWT in a server configuration or the JWT string directly. Remember that your configuration will be in `$NSC_HOME/nats/<operator_name>/<operator_name>.jwt` for the operator. The account JWT will be in `$NSC_HOME/nats/<operator_name>/accounts/<account_name>/<account_name>.jwt`*

Dù việc tự động sinh file config rất tiện, đôi khi bạn muốn tự viết tay để nắm rõ từng chi tiết. Sau khi đã tạo đủ các thực thể và xác định vị trí thư mục `.nsc` theo chuẩn, bạn có thể tham chiếu operator JWT và account JWT trực tiếp trong file config server (hoặc dán thẳng chuỗi JWT). Lưu ý: credential (thông tin đăng nhập) của operator nằm trong `$NSC_HOME/nats/<operator_name>/<operator_name>.jwt`, còn account JWT nằm trong `$NSC_HOME/nats/<operator_name>/accounts/<account_name>/<account_name>.jwt`.

> 🇬🇧 *For the configuration you'll need:*

Config cần có:

* Đường dẫn đến operator JWT
* Nội dung file account JWT

> 🇬🇧 *The format of the file is:*

Định dạng file như sau:

```
operator: <path to the operator jwt or jwt itself>
resolver: MEMORY
resolver_preload: {
    <public key for an account>: <contents of the account jwt>
    ### add as many accounts as you want
    ...
}
```

> 🇬🇧 *In this example this translates to:*

Trong ví dụ này, config tương ứng là:

```
operator: /Users/synadia/.nsc/nats/memory/memory.jwt
resolver: MEMORY
resolver_preload: {
ACSU3Q6LTLBVLGAQUONAGXJHVNWGSKKAUA7IY5TB4Z7PLEKSR5O6JTGR: eyJ0eXAiOiJqd3QiLCJhbGciOiJlZDI1NTE5In0.eyJqdGkiOiJPRFhJSVI2Wlg1Q1AzMlFJTFczWFBENEtTSDYzUFNNSEZHUkpaT05DR1RLVVBISlRLQ0JBIiwiaWF0IjoxNTU2NjU1Njk0LCJpc3MiOiJPRFdaSjJLQVBGNzZXT1dNUENKRjZCWTRRSVBMVFVJWTRKSUJMVTRLM1lERzNHSElXQlZXQkhVWiIsIm5hbWUiOiJBIiwic3ViIjoiQUNTVTNRNkxUTEJWTEdBUVVPTkFHWEpIVk5XR1NLS0FVQTdJWTVUQjRaN1BMRUtTUjVPNkpUR1IiLCJ0eXBlIjoiYWNjb3VudCIsIm5hdHMiOnsibGltaXRzIjp7InN1YnMiOi0xLCJjb25uIjotMSwibGVhZiI6LTEsImltcG9ydHMiOi0xLCJleHBvcnRzIjotMSwiZGF0YSI6LTEsInBheWxvYWQiOi0xLCJ3aWxkY2FyZHMiOnRydWV9fX0._WW5C1triCh8a4jhyBxEZZP8RJ17pINS8qLzz-01o6zbz1uZfTOJGvwSTS6Yv2_849B9iUXSd-8kp1iMXHdoBA
}
```

> 🇬🇧 *Save the config at server.conf and start the server:*

Lưu config vào `server.conf` rồi khởi động server:

```shell
nats-server -c server.conf
```

> 🇬🇧 *You can then [test it](./mem_resolver.md#testing-the-configuration).*

Sau đó có thể [kiểm tra cấu hình](./mem_resolver.md#testing-the-configuration).

## Kiểm Tra Cấu Hình

> 🇬🇧 *To test the configuration, simply use one of the standard tools:*

Để kiểm tra config, dùng một trong các tool chuẩn sau:

```shell
nats pub --creds ~/.nkeys/creds/memory/A/TA.creds hello world
```

## Thuật ngữ trong bài

- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **permission**: quyền truy cập
- **stream**: luồng message lưu trữ liên tục