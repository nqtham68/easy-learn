---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/jetstream_admin/encryption_at_rest
title: Mã hóa dữ liệu lưu trữ
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Mã hóa dữ liệu lưu trữ

*Hỗ trợ từ NATS server phiên bản 2.3.0*

*TPM được hỗ trợ trên Windows từ NATS Server phiên bản 2.11.0*

> **⚠️ Cảnh báo:**
> Mặc dù tính năng mã hóa dữ liệu lưu trữ của NATS server được hỗ trợ đầy đủ, chúng tôi khuyến nghị sử dụng mã hóa ở tầng file system khi có thể.
>
> Mã hóa file system, đặc biệt khi được cung cấp bởi các dịch vụ Cloud, được tối ưu cho throughput, không gây áp lực lên NATS server và loại bỏ nhu cầu quản lý secret khỏi cài đặt NATS.

> 🇬🇧 *The NATS server can be configured to encrypt message blocks which includes message headers and payloads. Other metadata files are encrypted as well, such as the stream metadata file and consumer metadata files.*

NATS server có thể được cấu hình để mã hóa các khối message (bao gồm header và payload). Các file metadata khác cũng được mã hóa, chẳng hạn như file metadata của stream (luồng message lưu trữ liên tục) và consumer (bên xử lý dữ liệu từ stream).

> 🇬🇧 *Two choices of ciphers are currently supported:*

Hiện có hai cipher được hỗ trợ:

- `chachapoly` - [ChaCha20-Poly1305](https://pkg.go.dev/golang.org/x/crypto/chacha20poly1305)
- `aes` - [AES-GCM](https://pkg.go.dev/crypto/aes)

> 🇬🇧 *Enabling encryption is done through the `jetstream` [configuration block](../../configuration/README.md#jetstream) on the server.*

Bật mã hóa thông qua khối config (cấu hình) `jetstream` trên server.

```text
jetstream : {
  cipher: chachapoly
  key : "6dYfBV0zzEkR3vxZCNjxmnVh/aIqgid1"
}
```

> 🇬🇧 *It is recommended to provide the encryption key through an environment variable at runtime, such as `$JS_KEY`, so it will not be persisted in a file.*

Nên cung cấp khóa mã hóa qua biến môi trường tại runtime, ví dụ `$JS_KEY`, để khóa không bị lưu vào file.

```text
jetstream : {
  cipher: chachapoly
  key: $JS_KEY
}
```

> 🇬🇧 *The variable can be exported in the environment or passed when the server starts up.*

Biến này có thể được export trong môi trường hoặc truyền vào khi server khởi động.

```shell
JS_KEY="mykey" nats-server -c js.conf
```

## TPM (chỉ dành cho Windows)

````
jetstream {
  store_dir: nats
  max_file_store: 10G
  tpm {
          keys_file: "keys"
          encryption_password: "pwd"
  }
}
````
| Property                  | Description                                                                                                                                                                               | Default                 | Version |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------- | :------ |
| `keys_file`                     |  Specifies the file where encryption keys are stored. This option is required, otherwise TPM will not be active. If the file does NOT EXIST, a new key will be dynamically created and stored in the `pcr`  | required | 2.11.0  |
| `encryption_password`                     | Password used for decrypting data in the keys file. OR, the password used to seal the dynamically created key in the TPM store. | required  | 2.11.0  |
| `srk_password`                     |  The Storage Root Key (SRK) password is used to access the TPM's storage root key. The srk password is optional in TPM 2.0. | not set  | 2.11.0  |
| `pcr`                     |  Platform Configuration Registers (PCRs). 0-16 are reserved. Pick a value from 17 to 23. |  22  | 2.11.0  | 
| `cipher`                     |   `chacha`/`chachapoly` or `aes`.                    | `chachapoly` | 2.11.0  |  

## Thay đổi cài đặt mã hóa

### Bật mã hóa khi đã có dữ liệu

> 🇬🇧 *Enabling encryption on a server with existing data is supported. Do note that existing unencrypted message blocks will not be re-encrypted, however any new blocks that are stored _will_ be encrypted going forward.*

Việc bật mã hóa trên server đang có dữ liệu là được hỗ trợ. Lưu ý rằng các khối message chưa được mã hóa sẽ không bị re-encrypt, tuy nhiên mọi khối mới được lưu _sẽ_ được mã hóa từ đó về sau.

> 🇬🇧 *If it is desired to encrypt the existing blocks, the stream can be backed up and restored (which decrypts on backup and then re-encrypts when restoring it).*

Nếu muốn mã hóa các khối hiện có, có thể backup và restore stream (quá trình backup sẽ giải mã, còn restore sẽ mã hóa lại).

### Tắt mã hóa hoặc thay đổi khóa

> 🇬🇧 *If encryption was enabled on the server and the server is restarted with a different key or disabled all together, the server will fail to decrypt messages when attempting to load them from the store. If this happens, you'll see log messages like the following:*

Nếu mã hóa đã được bật và server được khởi động lại với khóa khác hoặc tắt mã hóa hoàn toàn, server sẽ không thể giải mã message khi cố tải chúng từ store. Khi điều này xảy ra, bạn sẽ thấy các log như sau:

```text
Error decrypting our stream metafile: chacha20poly1305: message authentication failed
```

> 🇬🇧 *Note, that this will impact JetStream functionality, but the server will still support core NATS functionality.*

Lưu ý rằng điều này sẽ ảnh hưởng đến chức năng JetStream, nhưng server vẫn hỗ trợ các chức năng NATS cốt lõi.

### Thay đổi cipher

> 🇬🇧 *It is possible to change the `cipher`, however the same key must be used. The server will properly encrypt new message blocks with the new cipher and decrypt existing messages blocks with the existing cipher.*

Có thể thay đổi `cipher`, nhưng phải dùng cùng một khóa. Server sẽ mã hóa các khối message mới bằng cipher mới và giải mã các khối cũ bằng cipher cũ.

## Cân nhắc về hiệu năng

> 🇬🇧 *Performance considerations: As expected, encryption is likely to decrease performance, but by how much is hard to define. In some performance tests on a MacbookPro 2.8 GHz Intel Core i7 with SSD, we have observed as little as 1% decrease to more than 30%. In addition to CPU cycles required for encryption, the encrypted files may be larger, which results in more data being stored or read.*

Như kỳ vọng, mã hóa có thể làm giảm hiệu năng, nhưng mức độ giảm khó xác định chính xác. Trong một số bài kiểm thử hiệu năng trên MacbookPro 2.8 GHz Intel Core i7 với SSD, mức giảm ghi nhận từ chỉ 1% đến hơn 30%. Ngoài chi phí CPU cho mã hóa, các file được mã hóa có thể lớn hơn, dẫn đến nhiều dữ liệu phải lưu trữ hoặc đọc hơn.

## Thuật ngữ trong bài

- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **log**: bản ghi sự kiện
- **payload**: nội dung chính của message
- **stream**: luồng message lưu trữ liên tục