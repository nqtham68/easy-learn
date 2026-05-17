---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_intro/nkey_auth
title: NKeys
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# NKeys

> 🇬🇧 *NKeys are a new, highly secure public-key signature system based on [Ed25519](https://ed25519.cr.yp.to/).*

NKeys là hệ thống chữ ký public-key mới, bảo mật cao, dựa trên [Ed25519](https://ed25519.cr.yp.to/).

> 🇬🇧 *With NKeys the server can verify identities without ever storing or ever seeing private keys. The authentication system works by requiring a connecting client to provide its public key and digitally sign a challenge with its private key. The server generates a random challenge with every connection request, making it immune to playback attacks. The generated signature is validated against the provided public key, thus proving the identity of the client. If the public key is known to the server, authentication succeeds.*

Với NKeys, server có thể xác minh danh tính mà không cần lưu trữ hay nhìn thấy private key. Cơ chế xác thực hoạt động bằng cách yêu cầu client (bên gọi) cung cấp public key và ký số một challenge bằng private key của mình. Server tạo ra một challenge ngẫu nhiên cho mỗi yêu cầu kết nối, giúp hệ thống miễn nhiễm với các cuộc tấn công replay. Chữ ký được tạo ra sẽ được xác thực với public key được cung cấp, qua đó chứng minh danh tính của client. Nếu public key đã được server biết đến, xác thực thành công.

> 🇬🇧 *NKey is an excellent replacement for token authentication because a connecting client will have to prove it controls the private key for the authorized public key.*

> NKey là lựa chọn thay thế tuyệt vời cho xác thực bằng token (chuỗi xác thực), vì client kết nối phải chứng minh rằng nó kiểm soát private key tương ứng với public key được ủy quyền.

> 🇬🇧 *To generate nkeys, you'll need the [`nk` tool](../../../../using-nats/nats-tools/nk.md).*

Để tạo nkeys, bạn cần công cụ [`nk`](../../../../using-nats/nats-tools/nk.md).

## Tạo NKeys và Cấu hình Server

> 🇬🇧 *To generate a _User_ NKEY:*

Để tạo một NKEY cho _User_:

```shell
nk -gen user -pubout
```
```text
SUACSSL3UAHUDXKFSNVUZRF5UHPMWZ6BFDTJ7M6USDXIEDNPPQYYYCU3VY
UDXU4RCSJNZOIQHZNWXHXORDPRTGNJAHAHFRGZNEEJCPQTT2M7NLCNF4
```

> 🇬🇧 *The first output line starts with the letter `S` for _Seed_. The second letter, `U` stands for _User_. Seeds are private keys; you should treat them as secrets and guard them with care.*

Dòng output đầu tiên bắt đầu bằng ký tự `S` đại diện cho _Seed_. Ký tự thứ hai, `U` đại diện cho _User_. Seed chính là private key — hãy coi chúng như secret (chuỗi bí mật) và bảo vệ cẩn thận.

> 🇬🇧 *The second line starts with the letter `U` for _User_ and is a public key which can be safely shared.*

Dòng thứ hai bắt đầu bằng ký tự `U` đại diện cho _User_ và là public key có thể chia sẻ công khai.

> 🇬🇧 *To use nkey authentication, add a user, and set the `nkey` property to the public key of the user you want to authenticate:*

Để sử dụng xác thực nkey, thêm một user và đặt thuộc tính `nkey` thành public key của user cần xác thực:

```text
authorization: {
  users: [
    { nkey: UDXU4RCSJNZOIQHZNWXHXORDPRTGNJAHAHFRGZNEEJCPQTT2M7NLCNF4 }
  ]
}
```

> 🇬🇧 *Note that the user section sets the `nkey` property \(user/password/token properties are not needed\). Add `permission` sections as required.*

Lưu ý rằng phần user chỉ cần đặt thuộc tính `nkey` (không cần các thuộc tính user/password/token). Thêm các phần `permission` khi cần.

## Cấu hình Client

> 🇬🇧 *Now that you have a user nkey, let's configure a [client](../../../../using-nats/developing-with-nats/connecting/security/nkey.md) to use it for authentication. As an example, here are the connect options for the node client:*

Sau khi đã có user nkey, hãy cấu hình [client](../../../../using-nats/developing-with-nats/connecting/security/nkey.md) để sử dụng nó cho xác thực. Dưới đây là ví dụ về các tùy chọn kết nối cho node client:

```javascript
const NATS = require('nats');
const nkeys = require('ts-nkeys');

const nkey_seed = ‘SUACSSL3UAHUDXKFSNVUZRF5UHPMWZ6BFDTJ7M6USDXIEDNPPQYYYCU3VY’;
const nc = NATS.connect({
  port: PORT,
  nkey: 'UDXU4RCSJNZOIQHZNWXHXORDPRTGNJAHAHFRGZNEEJCPQTT2M7NLCNF4',
  sigCB: function (nonce) {
    // client loads seed safely from a file
    // or some constant like `nkey_seed` defined in
    // the program
    const sk = nkeys.fromSeed(Buffer.from(nkey_seed));
    return sk.sign(nonce);
   }
});
...
```

> 🇬🇧 *The client provides a function that it uses to parse the seed \(the private key\) and sign the connection challenge.*

Client cung cấp một hàm dùng để phân tích seed (private key) và ký challenge kết nối.

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **credential**: thông tin đăng nhập
- **secret**: chuỗi bí mật
- **server**: máy chủ
- **token**: chuỗi xác thực