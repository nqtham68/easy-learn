---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/connecting/security/tls
title: Mã hóa kết nối với TLS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Mã hóa kết nối với TLS

> 🇬🇧 *While authentication limits which clients can connect, TLS can be used to encrypt traffic between client/server and check the server's identity. Additionally - in the most secure version of TLS with NATS - the server can be configured to verify the client's identity, thus authenticating it. When started in [TLS mode](../../../../running-a-nats-service/configuration/securing_nats/tls.md), a `nats-server` will require all clients to connect with TLS. Moreover, if configured to connect with TLS, client libraries will fail to connect to a server without TLS.*

Authentication kiểm soát client nào được phép kết nối, còn TLS (mã hóa TLS) mã hóa toàn bộ traffic giữa client và server, đồng thời xác minh danh tính của server. Trong cấu hình bảo mật cao nhất của NATS với TLS, server có thể được thiết lập để xác minh danh tính của client, qua đó thực hiện xác thực hai chiều. Khi khởi động ở chế độ [TLS mode](../../../../running-a-nats-service/configuration/securing_nats/tls.md), `nats-server` sẽ yêu cầu tất cả client kết nối qua TLS. Ngược lại, nếu client được cấu hình dùng TLS mà server không hỗ trợ, thư viện client sẽ từ chối kết nối.

## Kết nối với TLS và xác minh danh tính client

> 🇬🇧 *Using TLS to connect to a server that verifies the client's identity is straightforward. The client has to provide a certificate and private key. The NATS client will use these to prove it's identity to the server. For the client to verify the server's identity, the CA certificate is provided as well.*

Kết nối TLS có xác minh danh tính client khá đơn giản. Client cần cung cấp certificate và private key — NATS client dùng chúng để chứng minh danh tính với server. Để client xác minh ngược lại danh tính của server, CA certificate cũng cần được cung cấp.

> 🇬🇧 *Use example certificates created in [self signed certificates for testing](../../../../running-a-nats-service/configuration/securing_nats/tls.md#creating-self-signed-certificates-for-testing).*

Sử dụng certificate mẫu được tạo theo hướng dẫn [self signed certificates for testing](../../../../running-a-nats-service/configuration/securing_nats/tls.md#creating-self-signed-certificates-for-testing).

```bash
nats-server --tls --tlscert=server-cert.pem --tlskey=server-key.pem --tlscacert rootCA.pem --tlsverify
```

#### Go

```go
nc, err := nats.Connect("localhost",
    nats.ClientCert("client-cert.pem", "client-key.pem"),
    nats.RootCAs("rootCA.pem"))
if err != nil {
    log.Fatal(err)
}
defer nc.Close()

// Do something with the connection
```

#### Java

```java
// This examples requires certificates to be in the java keystore format (.jks).
// To do so openssl is used to generate a pkcs12 file (.p12) from client-cert.pem and client-key.pem.
// The resulting file is then imported int a java keystore named keystore.jks using keytool which is part of java jdk.
// keytool is also used to import the CA certificate rootCA.pem into truststore.jks.  
// 
// openssl pkcs12 -export -out keystore.p12 -inkey client-key.pem -in client-cert.pem -password pass:password
// keytool -importkeystore -srcstoretype PKCS12 -srckeystore keystore.p12 -srcstorepass password -destkeystore keystore.jks -deststorepass password
//
// keytool -importcert -trustcacerts -file rootCA.pem -storepass password -noprompt -keystore truststore.jks
class SSLUtils {
    public static String KEYSTORE_PATH = "keystore.jks";
    public static String TRUSTSTORE_PATH = "truststore.jks";
    public static String STORE_PASSWORD = "password";
    public static String KEY_PASSWORD = "password";
    public static String ALGORITHM = "SunX509";

    public static KeyStore loadKeystore(String path) throws Exception {
        KeyStore store = KeyStore.getInstance("JKS");
        BufferedInputStream in = new BufferedInputStream(new FileInputStream(path));
        try {
            store.load(in, STORE_PASSWORD.toCharArray());
        } finally {
            in.close();
        }

        return store;
    }

    public static KeyManager[] createTestKeyManagers() throws Exception {
        KeyStore store = loadKeystore(KEYSTORE_PATH);
        KeyManagerFactory factory = KeyManagerFactory.getInstance(ALGORITHM);
        factory.init(store, KEY_PASSWORD.toCharArray());
        return factory.getKeyManagers();
    }

    public static TrustManager[] createTestTrustManagers() throws Exception {
        KeyStore store = loadKeystore(TRUSTSTORE_PATH);
        TrustManagerFactory factory = TrustManagerFactory.getInstance(ALGORITHM);
        factory.init(store);
        return factory.getTrustManagers();
    }

    public static SSLContext createSSLContext() throws Exception {
        SSLContext ctx = SSLContext.getInstance(Options.DEFAULT_SSL_PROTOCOL);
        ctx.init(createTestKeyManagers(), createTestTrustManagers(), new SecureRandom());
        return ctx;
    }
}

public class ConnectTLS {
    public static void main(String[] args) {

        try {
            SSLContext ctx = SSLUtils.createSSLContext();
            Options options = new Options.Builder()
                .server("nats://localhost:4222")
                .sslContext(ctx) // Set the SSL context
                .build();
            Connection nc = Nats.connect(options);

            // Do something with the connection

            nc.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

#### JavaScript

```javascript
// tls options available depend on the javascript
// runtime, please verify the readme for the
// client you are using for specific details
// this example showing the node library
const nc = await connect({
  port: ns.port,
  debug: true,
  tls: {
    caFile: caCertPath,
    keyFile: clientKeyPath,
    certFile: clientCertPath,
  },
});
```

#### Python

```python
nc = NATS()

ssl_ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
ssl_ctx.load_verify_locations('rootCA.pem')
ssl_ctx.load_cert_chain(certfile='client-cert.pem',
                        keyfile='client-key.pem')
await nc.connect(io_loop=loop, tls=ssl_ctx)

await nc.connect(servers=["nats://demo.nats.io:4222"], tls=ssl_ctx)

# Do something with the connection.
```

#### C#

```csharp
// dotnet add package NATS.Net
using NATS.Net;
using NATS.Client.Core;

await using var client = new NatsClient(new NatsOpts
{
    TlsOpts = new NatsTlsOpts
    {
        CaFile = "rootCA.pem",
        KeyFile = "client-key.pem",
        CertFile = "client-cert.pem",
    }
});
```

#### Ruby

```ruby
EM.run do

  options = {
    :servers => [
      'nats://localhost:4222',
    ],
    :tls => {
      :private_key_file => 'client-key.pem',
      :cert_chain_file  => 'client-cert.pem',
      :ca_file => 'rootCA.pem'
    }
  }

  NATS.connect(options) do |nc|
    puts "#{Time.now.to_f} - Connected to NATS at #{nc.connected_server}"

    nc.subscribe("hello") do |msg|
      puts "#{Time.now.to_f} - Received: #{msg}"
    end

    nc.flush do
      nc.publish("hello", "world")
    end

    EM.add_periodic_timer(0.1) do
      next unless nc.connected?
      nc.publish("hello", "hello")
    end

    # Set default callbacks
    nc.on_error do |e|
      puts "#{Time.now.to_f } - Error: #{e}"
    end

    nc.on_disconnect do |reason|
      puts "#{Time.now.to_f} - Disconnected: #{reason}"
    end

    nc.on_reconnect do |nc|
      puts "#{Time.now.to_f} - Reconnected to NATS server at #{nc.connected_server}"
    end

    nc.on_close do
      puts "#{Time.now.to_f} - Connection to NATS closed"
      EM.stop
    end
  end
end
```

#### C

```c
natsConnection      *conn      = NULL;
natsOptions         *opts      = NULL;
natsStatus          s          = NATS_OK;

s = natsOptions_Create(&opts);
if (s == NATS_OK)
    s = natsOptions_LoadCertificatesChain(opts, "client-cert.pem", "client-key.pem");
if (s == NATS_OK)
    s = natsOptions_LoadCATrustedCertificates(opts, "rootCA.pem");
if (s == NATS_OK)
    s = natsConnection_Connect(&conn, opts);

(...)

// Destroy objects that were created
natsConnection_Destroy(conn);
natsOptions_Destroy(opts);
```

## Kết nối qua TLS Protocol

> 🇬🇧 *Clients \(such as Go, Java, Javascript, Ruby and Type Script\) support providing a URL containing the `tls` protocol to the NATS connect call. This will turn on TLS without the need for further code changes. However, in that case there is likely some form of default or environmental settings to allow the TLS libraries of your programming language to find certificate and trusted CAs. Unless these settings are taken into accounts or otherwise modified, this way of connecting is very likely to fail.*

Một số client (như Go, Java, Javascript, Ruby và TypeScript) hỗ trợ truyền URL chứa protocol `tls` vào lệnh kết nối NATS để bật TLS mà không cần thay đổi code. Tuy nhiên, cách này phụ thuộc vào các cài đặt mặc định hoặc biến môi trường để thư viện TLS của ngôn ngữ lập trình tìm được certificate và CA đáng tin cậy. Nếu các cài đặt này chưa được cấu hình đúng, kết nối sẽ thất bại.

# Xem thêm
* [OSCP Stapling in Java](https://nats.io/blog/java-ocsp-stapling/)

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **server**: máy chủ
- **TLS**: mã hóa TLS