---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/jwt/resolver
title: Tra cứu Account bằng Resolver
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Tra cứu Account bằng Resolver

> 🇬🇧 *The `resolver` configuration option is used in conjunction with [NATS JWT Authentication](.) and [nsc](../../../../using-nats/nats-tools/nsc). The `resolver` option specifies a URL where the nats-server can retrieve an account JWT. There are 3 resolver implementations:*

Tùy chọn config `resolver` được dùng kết hợp với [NATS JWT Authentication](.) và [nsc](../../../../using-nats/nats-tools/nsc). Tùy chọn `resolver` chỉ định URL để nats-server lấy về account JWT. Có 3 cách triển khai resolver:

* [NATS Based Resolver](./resolver.md#nats-based-resolver) — lựa chọn ưu tiên và nên dùng mặc định
* [`MEMORY`](./resolver.md#memory) — nếu muốn khai báo tĩnh các account trong file config của server
* [`URL`](./resolver.md#url-Resolver) — nếu muốn tự xây dựng account service, thường để tích hợp bảo mật NATS với hệ thống bảo mật bên ngoài

> If the operator JWT specified in `operator` contains an account resolver URL, `resolver` only needs to be specified in order to overwrite that default.

Nếu operator JWT được chỉ định trong `operator` đã chứa URL của account resolver, thì `resolver` chỉ cần khai báo khi muốn ghi đè giá trị mặc định đó.

## NATS Based Resolver

> 🇬🇧 *The NATS based resolver is the preferred and easiest way to enable account lookup for the nats servers. It is built-in into `nats-server` and stores the account JWTs in a local (not shared) directory that the server has access to (i.e. you can't have more than one `nats-server`s using the same directory. All the servers in the cluster or super-cluster must be configured to use it, and they implement an 'eventually consistent' mechanism via NATS and the system account to synchronize (or lookup) the account data between themselves.*

NATS based resolver là cách dễ nhất và được ưu tiên để bật tính năng tra cứu account trên các nats-server. Resolver này được tích hợp sẵn vào `nats-server` và lưu trữ account JWT trong một thư mục cục bộ (không dùng chung) mà server có quyền truy cập — tức là không thể có nhiều hơn một `nats-server` dùng chung cùng thư mục. Tất cả server trong cluster (cụm nhiều server chạy chung) hoặc super-cluster phải được cấu hình để sử dụng resolver này; chúng triển khai cơ chế "eventually consistent" thông qua NATS và system account để đồng bộ (hoặc tra cứu) dữ liệu account với nhau.

> 🇬🇧 *In order to avoid having to store all account JWT on every `nats-server` (i.e. if you have a _lot_ of accounts), this resolver has two sub types `full` and `cache`.*

Để tránh phải lưu toàn bộ account JWT trên mỗi `nats-server` (khi số lượng account rất lớn), resolver này có hai kiểu con: `full` và `cache`.

> 🇬🇧 *In this mode of operation administrators typically use the [`nsc`](../../../../using-nats/nats-tools/nsc) CLI tool to create/manage the JWTs locally, and use `nsc push` to push new JWTs to the nats-servers' built-in resolvers, `nsc pull` to refresh their local copy of account JWTs, and `nsc revocations` to revoke them.*

Trong chế độ này, quản trị viên thường dùng CLI `nsc` để tạo/quản lý JWT cục bộ, dùng `nsc push` để đẩy JWT mới lên các built-in resolver của nats-server, `nsc pull` để làm mới bản sao account JWT cục bộ, và `nsc revocations` để thu hồi chúng.

### Full

> 🇬🇧 *The Full resolver means that the `nats-server` stores all JWTs and exchanges them in an eventually consistent way with other resolvers of the same type.*

Kiểu Full resolver có nghĩa là `nats-server` lưu toàn bộ JWT và trao đổi chúng theo cơ chế eventually consistent với các resolver cùng kiểu.

```yaml
resolver: {
    type: full
    # Directory in which account jwt will be stored
    dir: './jwt'
    # In order to support jwt deletion, set to true
    # If the resolver type is full delete will rename the jwt.
    # This is to allow manual restoration in case of inadvertent deletion.
    # To restore a jwt, remove the added suffix .delete and restart or send a reload signal.
    # To free up storage you must manually delete files with the suffix .delete.
    allow_delete: false
    # Interval at which a nats-server with a nats based account resolver will compare
    # it's state with one random nats based account resolver in the cluster and if needed,
    # exchange jwt and converge on the same set of jwt.
    interval: "2m"
    # limit on the number of jwt stored, will reject new jwt once limit is hit.
    limit: 1000
}
```

> 🇬🇧 *This resolver type also supports `resolver_preload`. When present, JWTs are listed and stored in the resolver. There, they may be subject to updates. Restarts of the `nats-server` will hold on to these more recent versions.*

Kiểu resolver này cũng hỗ trợ `resolver_preload`. Khi có, các JWT được liệt kê và lưu trong resolver, có thể được cập nhật. Khi `nats-server` khởi động lại, các phiên bản mới hơn này được giữ nguyên.

> 🇬🇧 *Not every server in a cluster needs to be set to `full`. You need enough to still serve your workload adequately, while some servers are offline.*

Không nhất thiết mọi server trong cluster đều phải đặt thành `full`. Chỉ cần đủ số lượng để phục vụ workload khi một số server offline.

### Cache

> 🇬🇧 *The Cache resolver means that the `nats-server` only stores a subset of the JWTs and evicts others based on an LRU scheme. The cache relies on (a) `full` NATS-based resolver(s) to retrieve accounts not present in the cache. A cache resolver does NOT accept account push messages from nsc and therefore is not suitable for stand-alone operation without a full resolver present.*

Cache resolver có nghĩa là `nats-server` chỉ lưu một tập con các JWT và loại bỏ các JWT còn lại theo cơ chế LRU. Cache dựa vào `full` NATS-based resolver để lấy các account chưa có trong cache. Cache resolver KHÔNG chấp nhận message push account từ nsc, do đó không phù hợp để hoạt động độc lập khi không có full resolver.

```yaml
resolver: {
    type: cache
    # Directory in which account jwt will be store
    dir: "./"
    # limit on the number of jwt stored, will evict old jwt once limit is hit.
    limit: 1000
    # How long to hold on to a jwt before discarding it. 
    ttl: "2m"
}
```

### NATS-Based Resolver - Tích hợp

> 🇬🇧 *The NATS-based resolver utilizes the system account for lookup and upload of account JWTs. If your application requires tighter integration you can make use of these subjects for tighter integration.*

NATS-based resolver sử dụng system account để tra cứu và tải lên account JWT. Nếu ứng dụng cần tích hợp chặt chẽ hơn, bạn có thể dùng các subject (chuỗi định danh message) sau.

> 🇬🇧 *To upload or update any generated account JWT without [`nsc`](../../../../using-nats/nats-tools/nsc), send it as a request to `$SYS.REQ.CLAIMS.UPDATE`. Each participating `full` NATS-based account resolver will respond with a message detailing success or failure.*

Để tải lên hoặc cập nhật account JWT mà không dùng [`nsc`](../../../../using-nats/nats-tools/nsc), hãy gửi nó dưới dạng request tới `$SYS.REQ.CLAIMS.UPDATE`. Mỗi `full` NATS-based account resolver tham gia sẽ phản hồi với message mô tả kết quả thành công hay thất bại.

> 🇬🇧 *To serve a requested account JWT yourself and essentially implement an account server, subscribe to `$SYS.REQ.ACCOUNT.*.CLAIMS.LOOKUP` and respond with the account JWT corresponding to the requested account id (wildcard).*

Để tự phục vụ account JWT được yêu cầu — về bản chất là tự triển khai account server — hãy subscribe vào `$SYS.REQ.ACCOUNT.*.CLAIMS.LOOKUP` và phản hồi bằng account JWT tương ứng với account id được yêu cầu (wildcard).

### Migrate dữ liệu account

> 🇬🇧 *To migrate account data when you change from using the standalone (REST) account server to the built-in NATS account resolver (or between NATS environments, or account servers) you can use `nsc`:*

Để migrate dữ liệu account khi chuyển từ standalone (REST) account server sang NATS account resolver tích hợp sẵn (hoặc giữa các môi trường NATS, hoặc giữa các account server), bạn có thể dùng `nsc`:

1. Chạy `nsc pull` để đảm bảo có bản sao toàn bộ dữ liệu account từ server về máy cục bộ
2. Cấu hình lại server để dùng nats resolver thay vì URL resolver
3. Thay đổi cài đặt 'account server URL' trong operator từ REST URL cũ sang nats URL: chỉ cần sao chép nats URL từ cài đặt 'service URLs' của operator vào account server URLs. `nsc edit operator --account-jwt-server-url <nats://...>`
4. Chạy `nsc push -A` để đẩy dữ liệu account lên nats-server qua built-in nats account resolver

> 🇬🇧 *You can also pass the account server URLs directly as a flag to the `nsc pull` and `nsc push` commands.*

Bạn cũng có thể truyền account server URLs trực tiếp dưới dạng flag cho lệnh `nsc pull` và `nsc push`.

## MEMORY

> 🇬🇧 *The `MEMORY` resolver is statically configured in the server's configuration file. You would use this mode if you would rather manage the account resolving 'by hand' through the `nat-server`s' configuration files. The memory resolver makes use of the `resolver_preload` directive, which specifies a map of public keys to account JWTs:*

`MEMORY` resolver được cấu hình tĩnh trong file config của server. Dùng chế độ này khi muốn quản lý thủ công việc phân giải account thông qua file config của `nat-server`. Memory resolver sử dụng directive `resolver_preload` — ánh xạ từ public key sang account JWT:

```yaml
resolver: MEMORY
resolver_preload: {
ACSU3Q6LTLBVLGAQUONAGXJHVNWGSKKAUA7IY5TB4Z7PLEKSR5O6JTGR: eyJ0eXAiOiJqd3QiLCJhbGciOiJlZDI1NTE5In0.eyJqdGkiOiJPRFhJSVI2Wlg1Q1AzMlFJTFczWFBENEtTSDYzUFNNSEZHUkpaT05DR1RLVVBISlRLQ0JBIiwiaWF0IjoxNTU2NjU1Njk0LCJpc3MiOiJPRFdaSjJLQVBGNzZXT1dNUENKRjZCWTRRSVBMVFVJWTRKSUJMVTRLM1lERzNHSElXQlZXQkhVWiIsIm5hbWUiOiJBIiwic3ViIjoiQUNTVTNRNkxUTEJWTEdBUVVPTkFHWEpIVk5XR1NLS0FVQTdJWTVUQjRaN1BMRUtTUjVPNkpUR1IiLCJ0eXBlIjoiYWNjb3VudCIsIm5hdHMiOnsibGltaXRzIjp7InN1YnMiOi0xLCJjb25uIjotMSwibGVhZiI6LTEsImltcG9ydHMiOi0xLCJleHBvcnRzIjotMSwiZGF0YSI6LTEsInBheWxvYWQiOi0xLCJ3aWxkY2FyZHMiOnRydWV9fX0._WW5C1triCh8a4jhyBxEZZP8RJ17pINS8qLzz-01o6zbz1uZfTOJGvwSTS6Yv2_849B9iUXSd-8kp1iMXHdoBA
}
```

> 🇬🇧 *The `MEMORY` resolver is recommended when the server has a small number of accounts that don't change very often.*

`MEMORY` resolver phù hợp khi server có ít account và chúng ít thay đổi.

> 🇬🇧 *For more information on how to configure a memory resolver, see [this tutorial](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/jwt/mem\_resolver).*

Xem thêm cách cấu hình memory resolver tại [hướng dẫn này](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/jwt/mem\_resolver).

## URL Resolver

> 🇬🇧 ***NOTE:** The [standalone NATS Account JWT Server](https://nats-io.gitbook.io/legacy-nats-docs/nats-account-server) is now _legacy_, please use the [NATS Based Resolver](./resolver.md#nats-based-resolver) instead. However, the URL resolver option is still available in case you want to implement your own version of an account resolver*

**LƯU Ý:** [Standalone NATS Account JWT Server](https://nats-io.gitbook.io/legacy-nats-docs/nats-account-server) hiện đã là _legacy_ — hãy dùng [NATS Based Resolver](./resolver.md#nats-based-resolver) thay thế. Tuy nhiên, tùy chọn URL resolver vẫn còn khả dụng nếu bạn muốn tự triển khai phiên bản account resolver của mình.

> 🇬🇧 *The `URL` resolver specifies a URL where the server can append an account public key to retrieve that account's JWT. Convention for standalone NATS Account JWT Servers is to serve JWTs at: `http://localhost:9090/jwt/v1/accounts/`. For such a configuration, you would specify the resolver as follows:*

`URL` resolver chỉ định URL mà server có thể ghép thêm public key của account để lấy JWT tương ứng. Theo quy ước, standalone NATS Account JWT Server phục vụ JWT tại: `http://localhost:9090/jwt/v1/accounts/`. Với cấu hình như vậy, khai báo resolver như sau:

```yaml
resolver: URL(http://localhost:9090/jwt/v1/accounts/)
```

> Note that if you are not using a nats-account-server, the URL can be anything as long as by appending the public key for an account, the requested JWT is returned.

Lưu ý: nếu không dùng nats-account-server, URL có thể là bất kỳ thứ gì, miễn là khi ghép thêm public key của account vào, JWT được yêu cầu sẽ được trả về.

> 🇬🇧 *If the server used requires client authentication, or you want to specify which CA is trusted for the lookup of account information, specify `resolver_tls`. This [`tls` configuration map](../tls.md) lets you further restrict TLS to the resolver.*

Nếu server yêu cầu xác thực client, hoặc bạn muốn chỉ định CA nào được tin cậy khi tra cứu thông tin account, hãy khai báo `resolver_tls`. [`tls` configuration map](../tls.md) này cho phép giới hạn thêm TLS đối với resolver.

## Thuật ngữ trong bài

- **cache**: bộ nhớ đệm
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **node**: một server trong cluster
- **permission**: quyền truy cập
- **request**: yêu cầu
- **service**: dịch vụ
- **subject**: chuỗi định danh message (giống topic)
- **token**: chuỗi xác thực