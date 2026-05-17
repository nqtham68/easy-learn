---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/security/token
title: Xác thực bằng Token
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Xác thực bằng Token

> 🇬🇧 *Tokens are basically random strings, much like a password, and can provide a simple authentication mechanism in some situations. However, tokens are only as safe as they are secret so other authentication schemes can provide more security in large installations. It is highly recommended to use one of the other NATS authentication mechanisms.*

Token (chuỗi xác thực) về bản chất là chuỗi ngẫu nhiên, tương tự như password, và có thể cung cấp cơ chế xác thực đơn giản trong một số tình huống. Tuy nhiên, token chỉ an toàn khi còn được giữ bí mật, vì vậy các cơ chế xác thực khác có thể đảm bảo bảo mật tốt hơn trong các hệ thống lớn. Khuyến nghị mạnh mẽ là nên dùng một trong các cơ chế xác thực NATS khác.

> 🇬🇧 *For this example, start the server using:*

Để chạy ví dụ này, khởi động server bằng lệnh sau:

```bash
nats-server --auth mytoken
```

> 🇬🇧 *The code uses localhost:4222 so that you can start the server on your machine to try them out.*

Các đoạn code dùng localhost:4222 để bạn có thể chạy server trực tiếp trên máy và thử nghiệm.

## Kết nối bằng Token

#### Go

```go
// Set a token
nc, err := nats.Connect("127.0.0.1", nats.Name("API Token Example"), nats.Token("mytoken"))
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
Options options = new Options.Builder()
    .server("nats://demo.nats.io:4222")
    .token("mytoken") // Set a token
    .build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
const nc = await connect({
  port: ns.port,
  token: "aToK3n",
});
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://demo.nats.io:4222"], token="mytoken")

# Do something with the connection.
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using NATS.Client.Core;

await using var client = new NatsClient(new NatsOpts
{
    Url = "127.0.0.1",
    Name = "API Token Example",
    AuthOpts = new NatsAuthOpts
    {
        Token = "mytoken"
    }
});
```

#### Ruby

```ruby
NATS.start(token: "mytoken") do |nc|
  puts "Connected using token"
end
```

#### C

```c
natsConnection      *conn      = NULL;
natsOptions         *opts      = NULL;
natsStatus          s          = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_SetToken(opts, "mytoken");
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Kết nối bằng Token trong URL

> 🇬🇧 *Some client libraries will allow you to pass the token as part of the server URL using the form:*

Một số thư viện client cho phép truyền token trực tiếp trong URL kết nối theo dạng:

> nats://_token_@server:port

> 🇬🇧 *Again, once you construct this URL you can connect as if this was a normal URL.*

Sau khi tạo URL theo dạng trên, bạn kết nối bình thường như với một URL thông thường.

#### Go

```go
// Token in URL
nc, err := nats.Connect("mytoken@localhost")
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
Connection nc = Nats.connect("nats://mytoken@localhost:4222");//Token in URL

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
  // JavaScript doesn't support tokens in urls use the `token` option
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://mytoken@demo.nats.io:4222"])

# Do something with the connection.
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using NATS.Client.Core;

await using var client = new NatsClient(new NatsOpts
{
    // .NET client doesn't support tokens in URLs
    // use Token option instead.
    AuthOpts = new NatsAuthOpts
    {
        Token = "mytoken"
    }
});
```

#### Ruby

```ruby
NATS.start("mytoken@127.0.0.1:4222") do |nc|
  puts "Connected using token!"
end
```

#### C

```c
natsConnection      *conn      = NULL;
natsOptions         *opts      = NULL;
natsStatus          s          = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_SetURL(opts, "nats://mytoken@127.0.0.1:4222");
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **port**: cổng kết nối
- **server**: máy chủ
- **token**: chuỗi xác thực