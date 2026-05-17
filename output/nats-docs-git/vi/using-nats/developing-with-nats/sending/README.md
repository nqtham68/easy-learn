---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/sending
title: Gửi Message
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Gửi Message

> 🇬🇧 *NATS sends and receives messages using a protocol that includes a target subject, an optional reply subject and an array of bytes. Some libraries may provide helpers to convert other data formats to and from bytes, but the NATS server will treat all messages as opaque byte arrays.*

NATS gửi và nhận message (gói dữ liệu được gửi đi) thông qua một giao thức bao gồm subject (chuỗi định danh message) đích, một reply subject tùy chọn, và một mảng byte. Một số thư viện có thể cung cấp hàm tiện ích để chuyển đổi các định dạng dữ liệu khác sang/từ byte, nhưng NATS server sẽ xử lý tất cả message như mảng byte thô.

> 🇬🇧 *All of the NATS clients are designed to make sending a message simple. For example, to send the string "All is Well" to the "updates" subject as a UTF-8 string of bytes you would do:*

Tất cả NATS client đều được thiết kế để việc gửi message trở nên đơn giản. Ví dụ, để gửi chuỗi "All is Well" đến subject "updates" dưới dạng chuỗi byte UTF-8, bạn làm như sau:

#### Go

```go
nc, err := nats.Connect("demo.nats.io", nats.Name("API PublishBytes Example"))
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

if err := nc.Publish("updates", []byte("All is Well")); err != nil {
    log.Fatal(err)
}
```

#### Java

```java
Connection nc = Nats.connect("nats://demo.nats.io:4222");

nc.publish("updates", "All is Well".getBytes(StandardCharsets.UTF_8));
```

#### JavaScript

```javascript
const sc = StringCodec();
nc.publish("updates", sc.encode("All is Well"));
```

#### Python

```python
nc = NATS()

await nc.connect(servers=["nats://demo.nats.io:4222"])

await nc.publish("updates", b'All is Well')
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;

await using var client = new NatsClient(url: "demo.nats.io", name: "API Publish String Example");

// The default serializer uses UTF-8 encoding for strings
await client.PublishAsync<string>(subject: "updates", data: "All is Well");
```

#### Ruby

```ruby
require 'nats/client'

NATS.start(servers:["nats://127.0.0.1:4222"]) do |nc|
  nc.publish("updates", "All is Well")
end
```

## Thuật ngữ trong bài

- **message**: gói dữ liệu được gửi đi
- **subject**: chuỗi định danh message (giống topic)