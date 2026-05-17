---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/js/context
title: JetStream context
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# JetStream context

> 🇬🇧 *You will need the *JetStream context* to make any JetStream enabled operation. Some client libraries (e.g. Java) also have a *JetStream Management context* (which you will only need if your application needs to create/purge/delete/manage streams and consumers), while some client libraries (e.g. Golang) only have the JetStream context that you use for all operations (including stream management).*

Mọi thao tác JetStream đều yêu cầu *JetStream context*. Một số thư viện client (ví dụ Java) cung cấp thêm *JetStream Management context* — chỉ cần dùng khi ứng dụng cần tạo/xóa/quản lý stream (luồng message lưu trữ liên tục) và consumer (bên xử lý dữ liệu từ stream). Một số thư viện khác (ví dụ Golang) chỉ có duy nhất JetStream context dùng cho mọi thao tác, bao gồm cả quản lý stream.

> 🇬🇧 *You obtain a JetStream context simply from your connection object (and you can optionally specify some JetStream options, most notably the JetStream operation timeout value). You also obtain the JetStream Management context from the connection.*

JetStream context được lấy trực tiếp từ đối tượng kết nối (connection object). Có thể tùy chọn truyền thêm các tham số JetStream, đáng chú ý nhất là giá trị timeout (thời gian chờ tối đa) cho các thao tác JetStream. JetStream Management context cũng được lấy tương tự từ connection.

#### Go

```go
// A JetStreamContext is the composition of a JetStream and JetStreamManagement interfaces.
// In case of only requiring publishing/consuming messages, can create a context that
// only uses the JetStream interface.
func ExampleJetStreamContext() {
nc, _ := nats.Connect("localhost")

var js nats.JetStream
var jsm nats.JetStreamManager
var jsctx nats.JetStreamContext

// JetStream that can publish/subscribe but cannot manage streams.
js, _ = nc.JetStream()
js.Publish("foo", []byte("hello"))

// JetStream context that can manage streams/consumers but cannot produce messages.
jsm, _ = nc.JetStream()
jsm.AddStream(&nats.StreamConfig{Name: "FOO"})

// JetStream context that can both manage streams/consumers
// as well as publish/subscribe.
jsctx, _ = nc.JetStream()
jsctx.AddStream(&nats.StreamConfig{Name: "BAR"})
jsctx.Publish("bar", []byte("hello world"))
}
```

#### Java

```java
// Getting the JetStream context
JetStream js = nc.jetStream();
// Getting the JetStream management context
JetStreamManagement jsm = nc.jetStreamManagement();
```

#### JavaScript

```javascript
const nc = await connect();
// Getting the JetStream context
const js = nc.jetstream();
// Getting the JetStream management context
const jsm = await nc.jetstreamManager();
```

#### Python

```Python
async def main():
    nc = await nats.connect("localhost")

    # Create JetStream context.
    js = nc.jetstream()
    
if __name__ == '__main__':
asyncio.run(main())
```

#### C

```C
int main(int argc, char **argv)
{
    natsConnection      *conn  = NULL;
    natsOptions         *opts  = NULL;
    jsCtx               *js    = NULL;
    jsOptions           jsOpts;
    jsErrCode           jerr   = 0;
    volatile int        errors = 0;

    opts = parseArgs(argc, argv, usage);
    dataLen = (int) strlen(payload);

    s = natsConnection_Connect(&conn, opts);

    if (s == NATS_OK)
        s = jsOptions_Init(&jsOpts);

    if (s == NATS_OK)
    {
        if (async)
        {
            jsOpts.PublishAsync.ErrHandler           = _jsPubErr;
            jsOpts.PublishAsync.ErrHandlerClosure    = (void*) &errors;
        }
        s = natsConnection_JetStream(&js, conn, &jsOpts);
    }
    
    // Destroy all our objects to avoid report of memory leak
    jsCtx_Destroy(js);
    natsConnection_Destroy(conn);
    natsOptions_Destroy(opts);

    // To silence reports of memory still in used with valgrind
    nats_Close();

    return 0;
}
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **consumer**: bên xử lý dữ liệu từ stream
- **stream**: luồng message lưu trữ liên tục
- **timeout**: thời gian chờ tối đa