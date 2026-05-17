---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/default_server
title: Kết nối đến Server Mặc định
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Kết nối đến Server Mặc định

> 🇬🇧 *Some libraries also provide a special way to connect to a _default_ url, which is generally `nats://localhost:4222`:*

Một số library còn cung cấp cách kết nối đặc biệt đến URL mặc định, thường là `nats://localhost:4222`:

#### Go

```go
nc, err := nats.Connect(nats.DefaultURL)
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
Connection nc = Nats.connect();

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
const nc = await connect();
// Do something with the connection
doSomething();
// When done close it
await nc.close();
```

#### Python

```python
nc = NATS()
await nc.connect()

# Do something with the connection

await nc.close()
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;

await using var client = new NatsClient();

// It's optional to call ConnectAsync()
// as it will be called when needed automatically
await client.ConnectAsync();
```

#### Ruby

```ruby
require 'nats/client'

NATS.start do |nc|
   # Do something with the connection

   # Close the connection
   nc.close
end
```

#### C

```c
natsConnection      *conn = NULL;
natsStatus          s;

s = natsConnection_ConnectTo(&conn, NATS_DEFAULT_URL);
if (s != NATS_OK)
  // handle error

// Destroy connection, no-op if conn is NULL.
natsConnection_Destroy(conn);
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **server**: máy chủ