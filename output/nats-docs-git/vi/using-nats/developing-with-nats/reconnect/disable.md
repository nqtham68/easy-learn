---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/reconnect/disable
title: Tắt tính năng Reconnect
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Tắt tính năng Reconnect

> 🇬🇧 *You can disable automatic reconnect with connection options:*

Bạn có thể tắt tính năng tự động reconnect thông qua các tùy chọn kết nối (connection options):

#### Go

```go
// Disable reconnect attempts
nc, err := nats.Connect("demo.nats.io", nats.NoReconnect())
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
    .noReconnect() // Disable reconnect attempts
    .build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
 const nc = await connect({
    reconnect: false,
    servers: ["demo.nats.io"],
});
```

#### Python

```python
nc = NATS()
await nc.connect(
   servers=[
      "nats://demo.nats.io:1222",
      "nats://demo.nats.io:1223",
      "nats://demo.nats.io:1224"
      ],
   allow_reconnect=False,
   )

# Do something with the connection

await nc.close()
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using NATS.Client.Core;

await using var client = new NatsClient(new NatsOpts
{
    Url = "nats://demo.nats.io:4222",
    
    // .NET client does not support disabling reconnects,
    // but you can set the maximum number of reconnect attempts
    MaxReconnectRetry = 1,
});
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(servers: ["nats://127.0.0.1:1222", "nats://127.0.0.1:1223", "nats://127.0.0.1:1224"], reconnect: false) do |nc|
   # Do something with the connection

   # Close the connection
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
    s = natsOptions_SetAllowReconnect(opts, false);
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```