---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/misc
title: Các tính năng kết nối bổ sung
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Các tính năng kết nối bổ sung

> 🇬🇧 *This section contains miscellaneous functionalities and options for connect.*

Phần này tổng hợp các tính năng và tùy chọn bổ sung khi thiết lập kết nối.

## Lấy kích thước Payload tối đa

> 🇬🇧 *While the client can't control the maximum payload size, clients may provide a way for applications to obtain the configured [`max_payload`](../../../running-a-nats-service/configuration/README.md#limits) after the connection is made. This will allow the application to chunk or limit data as needed to pass through the server.*

Mặc dù client không thể kiểm soát kích thước payload (nội dung chính của message) tối đa, một số client cho phép ứng dụng đọc giá trị [`max_payload`](../../../running-a-nats-service/configuration/README.md#limits) đã được cấu hình sau khi kết nối. Nhờ đó, ứng dụng có thể chia nhỏ hoặc giới hạn dữ liệu trước khi gửi qua server.

#### Go

```go
nc, err := nats.Connect("demo.nats.io")
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

mp := nc.MaxPayload()
log.Printf("Maximum payload is %v bytes", mp)

// Do something with the max payload
```

#### Java

```java
Connection nc = Nats.connect("nats://demo.nats.io:4222");

long mp = nc.getMaxPayload();
System.out.println("max payload for the server is " + mp + " bytes");
```

#### JavaScript

```javascript
t.log(`max payload for the server is ${nc.info.max_payload} bytes`);
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://demo.nats.io:4222"])

print("Maximum payload is %d bytes" % nc.max_payload)

# Do something with the max payload.
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;

await using var client = new NatsClient("nats://demo.nats.io:4222");

// Make sure we connect to a server to receive the server info,
// since connecting to servers is lazy in .NET client.
await client.ConnectAsync();

Console.WriteLine($"MaxPayload = {client.Connection.ServerInfo.MaxPayload}");
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(max_outstanding_pings: 5) do |nc|
  nc.on_reconnect do
    puts "Got reconnected to #{nc.connected_server}"
  end

  nc.on_disconnect do |reason|
    puts "Got disconnected! #{reason}"
  end

  # Do something with the max_payload
  puts "Maximum Payload is #{nc.server_info[:max_payload]} bytes"
end
```

#### C

```c
natsConnection      *conn    = NULL;
natsStatus          s        = NATS_OK;

s = natsConnection_ConnectTo(&conn, NATS_DEFAULT_URL);
if (s == NATS_OK)
{
    int64_t mp = natsConnection_GetMaxPayload(conn);
    printf("Max payload: %d\n", (int) mp);
}

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
```

## Bật Pedantic Mode

> 🇬🇧 *The NATS server provides a _pedantic_ mode that performs extra checks on the protocol.*

NATS server cung cấp chế độ _pedantic_ để thực hiện thêm các kiểm tra trên protocol.

> 🇬🇧 *One example of such a check is if a subject used for publishing contains a [wildcard](../../../nats-concepts/subjects.md#wildcards) character. The server will not use it as wildcard and therefore omits this check.*

Một ví dụ điển hình: nếu subject (chuỗi định danh message) dùng để publish chứa ký tự [wildcard](../../../nats-concepts/subjects.md#wildcards), server sẽ không xử lý nó như wildcard và bỏ qua bước kiểm tra này.

> 🇬🇧 *By default, this setting is off but you can turn it on to test your application:*

Mặc định, tùy chọn này bị tắt. Bạn có thể bật lên để kiểm thử ứng dụng:

#### Go

```go
opts := nats.GetDefaultOptions()
opts.Url = "demo.nats.io"
// Turn on Pedantic
opts.Pedantic = true
nc, err := opts.Connect()
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
Options options = new Options.Builder().
                            server("nats://demo.nats.io:4222").
                            pedantic(). // Turn on pedantic
                            build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
// the pedantic option is useful for developing nats clients.
// the javascript clients also provide `debug` which will
// print to the console all the protocol interactions
// with the server
const nc = await connect({
    pedantic: true,
    servers: ["demo.nats.io:4222"],
    debug: true,
});
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://demo.nats.io:4222"], pedantic=True)

# Do something with the connection.
```

#### C#

```csharp
// Not available in the NATS .NET client
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(pedantic: true) do |nc|
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
natsConnection      *conn    = NULL;
natsOptions         *opts    = NULL;
natsStatus          s        = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_SetPedantic(opts, true);
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Đặt kích thước Control Line tối đa

> 🇬🇧 *The protocol between the client and the server is fairly simple and relies on a control line and sometimes a body. The control line contains the operations being sent, like PING or PONG, followed by a carriage return and line feed, CRLF or "\r\n". The server has a [`max_control_line`](../../../running-a-nats-service/configuration/README.md#limits) option that can limit the maximum size of a control line. For PING and PONG this doesn't come into play, but for messages that contain subject names and possibly queue group names, the control line length can be important as it effectively limits the possibly combined length. Some clients will try to limit the control line size internally to prevent an error from the server. These clients may or may not allow you to set the size being used, but if they do, the size should be set to match the server configuration.*

Protocol giữa client và server khá đơn giản: gồm một control line và đôi khi có phần body. Control line chứa lệnh được gửi (như PING hoặc PONG), theo sau là CRLF (`\r\n`). Server có tùy chọn [`max_control_line`](../../../running-a-nats-service/configuration/README.md#limits) để giới hạn kích thước tối đa của control line. Với PING/PONG thì không ảnh hưởng, nhưng với các message chứa tên subject và tên queue group (nhóm subscribers chia sẻ tải), độ dài control line trở nên quan trọng vì nó giới hạn tổng độ dài kết hợp. Một số client sẽ tự giới hạn kích thước control line nội bộ để tránh lỗi từ server. Nếu client cho phép cấu hình giá trị này, hãy đặt khớp với cấu hình server.

> It is not recommended to set this to a value that is higher than the one of other clients or the nats-server.

> 🇬🇧 *For example, to set the maximum control line size to 2k:*

Ví dụ, để đặt kích thước control line tối đa là 2k:

#### Go

```go
// This does not apply to the NATS Go Client
```

#### Java

```java
Options options = new Options.Builder().
                            server("nats://demo.nats.io:4222").
                            maxControlLine(2 * 1024). // Set the max control line to 2k
                            build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
// the max control line is determined automatically by the client
```

#### Python

```python
# Asyncio NATS client does not allow custom control lines.
```

#### C#

```csharp
// control line is not configurable on NATS .NET client.
// required memory is allocated dynamically from the array pool.
```

#### Ruby

```ruby
# There is no need to customize this in the Ruby NATS client.
```

#### C

```c
// control line is not configurable on C NATS client.
```

## Bật/Tắt Verbose Mode

> 🇬🇧 *Clients can request _verbose_ mode from NATS server. When requested by a client, the server will reply to every message from that client with either a +OK or an error -ERR. However, the client will not block and wait for a response. Errors will be sent without verbose mode as well and client libraries handle them as documented.*

Client có thể yêu cầu chế độ _verbose_ từ NATS server. Khi bật, server sẽ phản hồi mỗi message từ client bằng `+OK` hoặc `-ERR`. Tuy nhiên, client sẽ không chờ phản hồi đó. Lỗi vẫn được gửi ngay cả khi không bật verbose mode, và các thư viện client xử lý chúng theo tài liệu.

> This functionality is only used for debugging the client library or the nats-server themselves. By default the server sets it to on, but every client turns it off.

> 🇬🇧 *To turn on verbose mode:*

Để bật verbose mode:

#### Go

```go
opts := nats.GetDefaultOptions()
opts.Url = "demo.nats.io"
// Turn on Verbose
opts.Verbose = true
nc, err := opts.Connect()
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
Options options = new Options.Builder().
                            server("nats://demo.nats.io:4222").
                            verbose(). // Turn on verbose
                            build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
const nc = await connect({
    verbose: true,
    servers: ["demo.nats.io:4222"],
});
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://demo.nats.io:4222"], verbose=True)

# Do something with the connection.
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(verbose: true) do |nc|
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
natsConnection      *conn    = NULL;
natsOptions         *opts    = NULL;
natsStatus          s        = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_SetVerbose(opts, true);
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **queue group**: nhóm subscribers chia sẻ tải
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)