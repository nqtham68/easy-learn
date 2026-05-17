---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/security/userpass
title: Xác thực bằng Tên người dùng và Mật khẩu
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Xác thực bằng Tên người dùng và Mật khẩu

> 🇬🇧 *For this example, start the server using:*

Để thử ví dụ này, khởi động server bằng lệnh:

```bash
nats-server --user myname --pass password
```

> 🇬🇧 *You can encrypt passwords to pass to `nats-server` using the simple [NATS CLI tool:](https://docs.nats.io/using-nats/nats-tools/nats\_cli)*

Bạn có thể mã hóa mật khẩu trước khi truyền vào `nats-server` bằng [NATS CLI tool:](https://docs.nats.io/using-nats/nats-tools/nats\_cli)

```bash
nats server passwd
```

```
? Enter password [? for help] **********************
? Reenter password [? for help] **********************

$2a$11$qbtrnb0mSG2eV55xoyPqHOZx/lLBlryHRhU3LK2oOPFRwGF/5rtGK
```

> 🇬🇧 *and use the hashed password in the server config. The client still uses the plain text version.*

Sau đó dùng mật khẩu đã băm trong config (cấu hình) của server. Client vẫn sử dụng mật khẩu dạng plain text.

> 🇬🇧 *The code uses localhost:4222 so that you can start the server on your machine to try them out.*

Các đoạn code dùng `localhost:4222` để bạn có thể khởi động server ngay trên máy cá nhân và thử nghiệm.

## Kết nối với User/Password

> 🇬🇧 *When logging in with a password `nats-server` will take either a plain text password or an encrypted password.*

Khi đăng nhập bằng mật khẩu, `nats-server` chấp nhận cả mật khẩu plain text lẫn mật khẩu đã được mã hóa.

#### Go

```go
// Set a user and plain text password
nc, err := nats.Connect("127.0.0.1", nats.UserInfo("myname", "password"))
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
Options options = new Options.Builder()
    .server("nats://localhost:4222")
    .userInfo("myname","password") // Set a user and plain text password
    .build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
 const nc = await connect({
      port: ns.port,
      user: "byname",
      pass: "password",
});
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://myname:password@demo.nats.io:4222"])

# Do something with the connection.
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using NATS.Client.Core;

await using var client = new NatsClient(new NatsOpts
{
    Url = "nats://localhost:4222",
    AuthOpts = new NatsAuthOpts
    {
        Username = "myname",
        Password = "password",
    }
});
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(servers:["nats://myname:password@127.0.0.1:4222"], name: "my-connection") do |nc|
   nc.on_error do |e|
    puts "Error: #{e}"
  end

   nc.on_reconnect do
    puts "Got reconnected to #{nc.connected_server}"
  end

  nc.on_disconnect do |reason|
    puts "Got disconnected! #{reason}"
  end

  nc.close
end
```

#### C

```c
natsConnection      *conn      = NULL;
natsOptions         *opts      = NULL;
natsStatus          s          = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_SetUserInfo(opts, "myname", "password");
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Kết nối với User/Password trong URL

> 🇬🇧 *Most clients make it easy to pass the user name and password by accepting them in the URL for the server. This standard format is:*

Hầu hết các client đều hỗ trợ truyền credential (thông tin đăng nhập) trực tiếp trong URL kết nối tới server. Định dạng chuẩn là:

> nats://_user_:_password_@server:port

> 🇬🇧 *Using this format, you can connect to a server using authentication as easily as you connected with a URL:*

Với định dạng này, việc kết nối có xác thực đơn giản như kết nối thông thường bằng URL:

#### Go

```go
// Set a user and plain text password
nc, err := nats.Connect("myname:password@127.0.0.1")
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
Connection nc = Nats.connect("nats://myname:password@localhost:4222");

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
// JavaScript clients don't support username/password in urls use `user` and `pass` options.
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://myname:password@demo.nats.io:4222"])

# Do something with the connection.
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using NATS.Client.Core;

await using var nc = new NatsClient(new NatsOpts
{
    // .NET client doesn't support username/password in URLs
    // use `Username` and `Password` options.
    Url = "nats://demo.nats.io:4222",
    AuthOpts = new NatsAuthOpts
    {
        Username = "myname",
        Password = "password",
    }
});
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(servers:["nats://myname:password@127.0.0.1:4222"], name: "my-connection") do |nc|
   nc.on_error do |e|
    puts "Error: #{e}"
  end

   nc.on_reconnect do
    puts "Got reconnected to #{nc.connected_server}"
  end

  nc.on_disconnect do |reason|
    puts "Got disconnected! #{reason}"
  end

  nc.close
end
```

#### C

```c
natsConnection      *conn      = NULL;
natsOptions         *opts      = NULL;
natsStatus          s          = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_SetURL(opts, "nats://myname:password@127.0.0.1:4222");
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **server**: máy chủ