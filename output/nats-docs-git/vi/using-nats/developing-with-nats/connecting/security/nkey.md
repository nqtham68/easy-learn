---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/security/nkey
title: Xác thực bằng NKey
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Xác thực bằng NKey

> 🇬🇧 *The 2.0 version of NATS server introduces a new challenge response authentication option. This challenge response is based on a wrapper we call [NKeys](../../../../running-a-nats-service/configuration/securing_nats/auth_intro/nkey_auth.md). The server can use these keys in several ways for authentication. The simplest is for the server to be configured with a list of known public keys and for the clients to respond to the challenge by signing it with its private key. \(A printable private NKey is referred to as seed\). This challenge-response ensures security by ensuring that the client has the private key, but also protects the private key from the server, which never has access to it!*

NATS server phiên bản 2.0 giới thiệu cơ chế xác thực challenge-response mới, dựa trên một lớp bọc được gọi là [NKeys](../../../../running-a-nats-service/configuration/securing_nats/auth_intro/nkey_auth.md). Server có thể dùng các key này theo nhiều cách để xác thực. Cách đơn giản nhất là cấu hình server với danh sách public key đã biết, sau đó client (bên gọi phía người dùng) phản hồi challenge bằng cách ký bằng private key của mình. \(Private NKey ở dạng in được gọi là seed\). Cơ chế challenge-response này đảm bảo bảo mật: client phải có private key để ký, nhưng private key đó không bao giờ được gửi lên server, nghĩa là server không bao giờ có quyền truy cập vào nó.

> 🇬🇧 *Handling challenge response may require more than just a setting in the connection options, depending on the client library.*

Việc xử lý challenge-response có thể yêu cầu nhiều hơn là chỉ thiết lập một tùy chọn trong connection options — tùy thuộc vào client library được sử dụng.

#### Go

```go
opt, err := nats.NkeyOptionFromSeed("seed.txt")
if err != nil {
    log.Fatal(err)
}
nc, err := nats.Connect("127.0.0.1", opt)
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
NKey theNKey = NKey.createUser(null); // really should load from somewhere
Options options = new Options.Builder()
    .server("nats://localhost:4222")
    .authHandler(new AuthHandler(){
        public char[] getID() {
            try {
                return theNKey.getPublicKey();
            } catch (GeneralSecurityException|IOException|NullPointerException ex) {
                return null;
            }
        }

        public byte[] sign(byte[] nonce) {
            try {
                return theNKey.sign(nonce);
            } catch (GeneralSecurityException|IOException|NullPointerException ex) {
                return null;
            }
        }

        public char[] getJWT() {
            return null;
        }
    })
    .build();
Connection nc = Nats.connect(options);

// Do something with the connection

nc.close();
```

#### JavaScript

```javascript
// seed should be stored and treated like a secret
const seed = new TextEncoder().encode(
  "SUAEL6GG2L2HIF7DUGZJGMRUFKXELGGYFMHF76UO2AYBG3K4YLWR3FKC2Q",
);
const nc = await connect({
  port: ns.port,
  authenticator: nkeyAuthenticator(seed),
});
```

#### Python

```python
nc = NATS()

async def error_cb(e):
    print("Error:", e)

await nc.connect("nats://localhost:4222",
                 nkeys_seed="./path/to/nkeys/user.nk",
                 error_cb=error_cb,
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
    Url = "127.0.0.1",
    Name = "API NKey Example",
    AuthOpts = new NatsAuthOpts
    {
        NKeyFile = "/path/to/nkeys/user.nk"
    }
});
```

#### C

```c
static natsStatus
sigHandler(
    char            **customErrTxt,
    unsigned char   **signature,
    int             *signatureLength,
    const char      *nonce,
    void            *closure)
{
    // Sign the given `nonce` and return the signature as `signature`.
    // This needs to allocate memory. The length of the signature is
    // returned as `signatureLength`.
    // If an error occurs the user can return specific error text through
    // `customErrTxt`. The library will free this pointer.

    return NATS_OK;
}

(...)

natsConnection      *conn      = NULL;
natsOptions         *opts      = NULL;
natsStatus          s          = NATS_OK;
const char          *pubKey    = "my public key......";

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_SetNKey(opts, pubKey, sigHandler, NULL);
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **server**: máy chủ