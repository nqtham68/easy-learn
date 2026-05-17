---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth_callout
title: Auth Callout - Ủy quyền xác thực
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Auth Callout - Ủy quyền xác thực

_Từ NATS v2.10.0_

> 🇬🇧 *Auth Callout is an opt-in extension for delegating client authentication and authorization to an application-defined NATS service.*

Auth Callout là extension tùy chọn cho phép ủy quyền xác thực và phân quyền client (bên gọi phía người dùng) cho một NATS service do ứng dụng tự định nghĩa.

> 🇬🇧 *The motivation for this extension is to support applications using an alternate identity and access management (IAM) backend as the source of truth for managing users/applications/machines credentials and permissions. This could be services that implement standard protocols such as LDAP, SAML, and OAuth, an ad-hoc database, or even a file on disk.*

Extension này ra đời để hỗ trợ các ứng dụng dùng IAM backend thay thế làm nguồn sự thật duy nhất để quản lý credential (thông tin đăng nhập) và permission (quyền truy cập) của user, ứng dụng hay máy. Backend đó có thể là service triển khai các giao thức chuẩn như LDAP, SAML, OAuth, một database tùy chỉnh, hoặc thậm chí một file trên disk.

<figure><img src="../../../.gitbook/assets/auth-callout-light.png" alt=""><figcaption><p>Auth Callout</p></figcaption></figure>

> 🇬🇧 *Both centralized and decentralized authentication models are supported with slightly different considerations and semantics.*

Cả hai mô hình xác thực tập trung (centralized) và phi tập trung (decentralized) đều được hỗ trợ, với một số điểm khác biệt nhỏ về cách dùng và ngữ nghĩa.

> 🇬🇧 *There are three phases to leveraging auth callout:*

Có ba giai đoạn để sử dụng auth callout:

* service implementation
* migration considerations
* setup and configuration

> **ℹ️ Info:**
> Note, the setup and configuration is deliberately _last_ since enabling the configuration before deploying a service could cause issues for existing systems.

> **ℹ️ Info:**
> Lưu ý, setup và configuration được để cuối cùng là có chủ ý — bật config trước khi deploy service có thể gây sự cố cho hệ thống hiện tại.

## Xác thực tập trung (Centralized Auth)

> 🇬🇧 *Centralized auth refers to all authentication and authorization mechanisms that are server config file-based.*

Centralized auth là các cơ chế xác thực và phân quyền dựa hoàn toàn vào file config của server.

### Triển khai service

> 🇬🇧 *Refer to the [end-to-end example](https://natsbyexample.com/examples/auth/callout/cli) to get oriented with a basic service implementation.*

Tham khảo [ví dụ end-to-end](https://natsbyexample.com/examples/auth/callout/cli) để nắm được cách triển khai service cơ bản.

> 🇬🇧 *There are three key data structures:*

Có ba cấu trúc dữ liệu chính:

* [authorization request claims](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth\_callout#authorization-request-claims)
* [authorization response claims](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth\_callout#authorization-response-claims)
* [user claims](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth\_callout#user-claims)

> **ℹ️ Info:**
> Language support for these structures currently exists for Go in the [nats-io/jwt](https://pkg.go.dev/github.com/nats-io/jwt/v2) package.

> **ℹ️ Info:**
> Hiện tại, các cấu trúc này được hỗ trợ cho Go thông qua package [nats-io/jwt](https://pkg.go.dev/github.com/nats-io/jwt/v2).

### Cân nhắc khi migration

> 🇬🇧 *In this context, migration refers to the considerations and steps required to enable auth callout for an existing system without causing interruption.*

Trong ngữ cảnh này, migration là các bước cần thiết để bật auth callout cho hệ thống đang chạy mà không gây gián đoạn.

> 🇬🇧 *In the centralized model, existing users defined in the config file will be ignored. The auth service will need to handle authenticating all users as well as assigning the target account and permissions. This includes the system account user(s) and an implicit "no auth" user.*

Trong mô hình tập trung, các user đã định nghĩa trong file config sẽ bị bỏ qua. Auth service cần xử lý toàn bộ việc xác thực user và gán account, permission cho từng user — bao gồm cả user thuộc system account và user "no auth" ngầm định.

> 🇬🇧 *As a result, prior to enabling auth callout, existing users and permissions must be ported to the target backend. Once the service is deployed, the `auth_callout` configuration can be enabled at which point client authentication will be delegated to the auth service. Assuming the credentials are the same, clients should not experience interruption on reconnect.*

Do đó, trước khi bật auth callout, cần chuyển toàn bộ user và permission sang backend mới. Sau khi service được deploy, config `auth_callout` mới được bật — lúc này việc xác thực client sẽ được ủy quyền cho auth service. Nếu credential không thay đổi, client sẽ không bị gián đoạn khi reconnect.

### Setup và configuration

> 🇬🇧 *For centralized auth callout, configuration is declared in the `auth_callout` block under the top-level `authorization` block.*

Với centralized auth callout, config được khai báo trong block `auth_callout` nằm bên trong block `authorization` ở cấp cao nhất.

```
authorization {
  auth_callout {
    ...
  }
}
```

> 🇬🇧 *The available properties in the `auth_callout` block include:*

Các thuộc tính có thể dùng trong block `auth_callout` gồm:

| Property     | Description                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------------- |
| `issuer`     | The public key of the designated NKey used for signing authorization payloads.                                    |
| `auth_users` | The list of user names or nkeys under `account` that are designated auth callout users.                                    |
| `account`    | The account containing the users that are designated _auth callout_ users. Defaults to the global account (`$G`). |
| `xkey`       | Optional. The public key of a designated XKey (x25519) used for encrypting authorization payloads.                |

> 🇬🇧 *To generate the account issuer NKey, the [nsc](https://github.com/nats-io/nsc) tool can be used.*

Dùng công cụ [nsc](https://github.com/nats-io/nsc) để tạo NKey cho account issuer.

```
$ nsc generate nkey --account
SAANDLKMXL6CUS3CP52WIXBEDN6YJ545GDKC65U5JZPPV6WH6ESWUA6YAI
ABJHLOVMPA4CI6R5KLNGOB4GSLNIY7IOUPAJC4YFNDLQVIOBYQGUWVLA
```

> **ℹ️ Info:**
> ☝️ Be sure to generate your own keypair! Don't use this in production.

> **ℹ️ Info:**
> ☝️ Hãy tự tạo keypair của bạn! Đừng dùng keypair mẫu này trên môi trường production.

```
authorization {
  users: [ { user: auth, password: auth } ]
  auth_callout {
    issuer: ABJHLOVMPA4CI6R5KLNGOB4GSLNIY7IOUPAJC4YFNDLQVIOBYQGUWVLA
    auth_users: [ auth ]
  }
}
```

> 🇬🇧 *This minimum configuration would use the implicit default account `$G`.*

Config tối thiểu này sẽ dùng account mặc định ngầm định `$G`.

#### Nhiều account

> 🇬🇧 *If an existing system using multiple accounts is being migrated to auth callout, then the existing `accounts` configuration should remain with the `users` property removed (since it will no longer be used after being ported).*

Nếu hệ thống hiện tại dùng nhiều account và đang migration sang auth callout, giữ nguyên config `accounts` hiện có nhưng bỏ thuộc tính `users` (vì thuộc tính này không còn cần thiết sau khi đã chuyển sang backend mới).

> 🇬🇧 *For new setups, it is recommended to use explicit accounts, such as the following configuration having the `AUTH` account for auth callout, `APP` (could be more) for application account (instead of relying on the `$G` account), and `SYS` for the system account.*

Với hệ thống mới, nên dùng account tường minh. Ví dụ: account `AUTH` dành cho auth callout, `APP` (có thể có thêm) làm application account (thay vì dùng account `$G`), và `SYS` làm system account.

```
accounts {
  AUTH: {
    users: [ { user: auth, password: auth } ]
  }
  APP: {}
  SYS: {}
}
system_account: SYS

authorization {
  auth_callout {
    issuer: ABJHLOVMPA4CI6R5KLNGOB4GSLNIY7IOUPAJC4YFNDLQVIOBYQGUWVLA
    auth_users: [ auth ]
    account: AUTH
  }
}
```

#### Mã hóa

> 🇬🇧 *The `xkey` property enables encrypting the request payloads. This is recommended as a security best practice, but not required.*

Thuộc tính `xkey` cho phép mã hóa payload (nội dung chính của message) trong request. Đây là best practice bảo mật được khuyến nghị nhưng không bắt buộc.

> 🇬🇧 *To generate an XKey, `nsc` can be used again.*

Để tạo XKey, dùng lại `nsc`.

```
$ nsc generate nkey --curve
SXANPB47UINQR7EXT3BRP26A4LY2CMCDLTY2KX6BU3EGK2VZYREJ4IJRCE
XAMHJVPKHHPYZQQM2IVWXKJH36KDDZZMSJ32QKSQBUODFX4I4HARO4GL
```

> **ℹ️ Info:**
> ☝️ Again, don't use this and be sure to generate your own and keep the seed secret!

> **ℹ️ Info:**
> ☝️ Một lần nữa, đừng dùng XKey mẫu này — tự tạo keypair riêng và giữ bí mật seed!

> 🇬🇧 *Incorporating the `xkey`, we have the following config:*

Khi tích hợp `xkey`, config sẽ như sau:

```
accounts {
  AUTH: {
    users: [ { user: auth, password: auth } ]
  }
  APP: {}
  SYS: {}
}
system_account: SYS

authorization {
  auth_callout {
    issuer: ABJHLOVMPA4CI6R5KLNGOB4GSLNIY7IOUPAJC4YFNDLQVIOBYQGUWVLA
    auth_users: [ auth ]
    account: AUTH
    xkey: XAMHJVPKHHPYZQQM2IVWXKJH36KDDZZMSJ32QKSQBUODFX4I4HARO4GL
  }
}
```

## Xác thực phi tập trung (Decentralized Auth)

Coming soon!

## Tài liệu tham khảo

### Mã hóa

> 🇬🇧 *When encryption is enabled, the server will generate a one-time use XKey keypair per client connection/reconnect. The public key is included in the authorization request claims which enables the auth callout service to encrypt the authorization response payload when sending it back to the NATS server.*

Khi bật mã hóa, server sẽ tạo một XKey keypair dùng một lần cho mỗi kết nối/reconnect của client. Public key được đưa vào authorization request claims, nhờ đó auth callout service có thể mã hóa authorization response payload trước khi gửi lại cho NATS server.

> **ℹ️ Info:**
> The one-time use keypair prevents replay attacks since the public key will be thrown away after the first response was received by the server or the timeout was reached.

> **ℹ️ Info:**
> Keypair dùng một lần giúp ngăn replay attack vì public key bị hủy ngay sau khi server nhận được response đầu tiên hoặc khi timeout hết hạn.

> 🇬🇧 *Once the authorization request is prepared, it is encoded and encrypted using the configured `xkey` public key. Once encrypted, the message is published for the auth service to receive.*

Sau khi authorization request được chuẩn bị, nó được encode và mã hóa bằng public key của `xkey` đã cấu hình. Sau đó, message được publish để auth service nhận.

> 🇬🇧 *The auth service is expected to have the private key to decrypt the authorization request before using the claims data. When preparing the response, the server-provided one-time public xkey will be used to encrypt the response before sending back to the server.*

Auth service cần có private key để giải mã authorization request trước khi xử lý claims. Khi chuẩn bị response, one-time public xkey do server cung cấp sẽ được dùng để mã hóa response trước khi gửi lại.

### Schema

#### Authorization request claims

> 🇬🇧 *The claims is a standard JWT structure with a nested object named `nats` containing the following top-level fields:*

Claims là cấu trúc JWT chuẩn với object lồng nhau tên `nats`, chứa các trường cấp cao nhất sau:

* `server_id` - An object describing the NATS server, include the `id` field needed to be used in the authorization response.
* `user_nkey` - A user public NKey generated by the NATS server which is used as the _subject_ of the authorization response.
* `client_info` - An object describing the client attempting to connect.
* `connect_opts` - An object containing the data sent by client in the `CONNECT` message.
* `client_tls` - An object containing any client certificates, if applicable.

<details>

<summary>Full JSON schema</summary>

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "authorization-request-claims",
  "properties": {
    "aud": {
      "type": "string"
    },
    "exp": {
      "type": "integer"
    },
    "jti": {
      "type": "string"
    },
    "iat": {
      "type": "integer"
    },
    "iss": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "nbf": {
      "type": "integer"
    },
    "sub": {
      "type": "string"
    },
    "nats": {
      "properties": {
        "server_id": {
          "properties": {
            "name": {
              "type": "string"
            },
            "host": {
              "type": "string"
            },
            "id": {
              "type": "string"
            },
            "version": {
              "type": "string"
            },
            "cluster": {
              "type": "string"
            },
            "tags": {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            "xkey": {
              "type": "string"
            }
          },
          "additionalProperties": false,
          "type": "object",
          "required": [
            "name",
            "host",
            "id"
          ]
        },
        "user_nkey": {
          "type": "string"
        },
        "client_info": {
          "properties": {
            "host": {
              "type": "string"
            },
            "id": {
              "type": "integer"
            },
            "user": {
              "type": "string"
            },
            "name": {
              "type": "string"
            },
            "tags": {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            "name_tag": {
              "type": "string"
            },
            "kind": {
              "type": "string"
            },
            "type": {
              "type": "string"
            },
            "mqtt_id": {
              "type": "string"
            },
            "nonce": {
              "type": "string"
            }
          },
          "additionalProperties": false,
          "type": "object"
        },
        "connect_opts": {
          "properties": {
            "jwt": {
              "type": "string"
            },
            "nkey": {
              "type": "string"
            },
            "sig": {
              "type": "string"
            },
            "auth_token": {
              "type": "string"
            },
            "user": {
              "type": "string"
            },
            "pass": {
              "type": "string"
            },
            "name": {
              "type": "string"
            },
            "lang": {
              "type": "string"
            },
            "version": {
              "type": "string"
            },
            "protocol": {
              "type": "integer"
            }
          },
          "additionalProperties": false,
          "type": "object",
          "required": [
            "protocol"
          ]
        },
        "client_tls": {
          "properties": {
            "version": {
              "type": "string"
            },
            "cipher": {
              "type": "string"
            },
            "certs": {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            "verified_chains": {
              "items": {
                "items": {
                  "type": "string"
                },
                "type": "array"
              },
              "type": "array"
            }
          },
          "additionalProperties": false,
          "type": "object"
        },
        "request_nonce": {
          "type": "string"
        },
        "tags": {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        "type": {
          "type": "string"
        },
        "version": {
          "type": "integer"
        }
      },
      "additionalProperties": false,
      "type": "object",
      "required": [
        "server_id",
        "user_nkey",
        "client_info",
        "connect_opts"
      ]
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "nats"
  ]
}
```

</details>

#### Authorization response claims

> 🇬🇧 *The claims is a standard JWT structure with a nested object named `nats` containing the following top-level fields:*

Claims là cấu trúc JWT chuẩn với object lồng nhau tên `nats`, chứa các trường cấp cao nhất sau:

* `jwt` - The encoded [user claims](https://docs.nats.io/running-a-nats-service/configuration/securing_nats/auth\_callout#user-claims) JWT which will be used by the NATS server for the duration of the client connection.
* `error` - An error message sent back to the NATS server if authorization failed. This will be included log output.
* `issuer_account` - The public Nkey of the issuing account. If set, this indicates the claim was issued by a signing key.

<details>

<summary>Full JSON schema</summary>

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/nats-io/jwt/v2/authorization-response-claims",
  "properties": {
    "aud": {
      "type": "string"
    },
    "exp": {
      "type": "integer"
    },
    "jti": {
      "type": "string"
    },
    "iat": {
      "type": "integer"
    },
    "iss": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "nbf": {
      "type": "integer"
    },
    "sub": {
      "type": "string"
    },
    "nats": {
      "properties": {
        "jwt": {
          "type": "string"
        },
        "error": {
          "type": "string"
        },
        "issuer_account": {
          "type": "string"
        },
        "tags": {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        "type": {
          "type": "string"
        },
        "version": {
          "type": "integer"
        }
      },
      "additionalProperties": false,
      "type": "object"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "nats"
  ]
}
```

</details>

#### User claims

> 🇬🇧 *The claims is a standard JWT structure with a nested object named `nats` containing the following, notable, top-level fields:*

Claims là cấu trúc JWT chuẩn với object lồng nhau tên `nats`, chứa các trường đáng chú ý sau:

* `issuer_account` - The public Nkey of the issuing account. If set, this indicates the claim was issued by a signing key.

<details>

<summary>Full JSON schema</summary>

```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/nats-io/jwt/v2/user-claims",
  "properties": {
    "aud": {
      "type": "string"
    },
    "exp": {
      "type": "integer"
    },
    "jti": {
      "type": "string"
    },
    "iat": {
      "type": "integer"
    },
    "iss": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "nbf": {
      "type": "integer"
    },
    "sub": {
      "type": "string"
    },
    "nats": {
      "properties": {
        "pub": {
          "properties": {
            "allow": {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            "deny": {
              "items": {
                "type": "string"
              },
              "type": "array"
            }
          },
          "additionalProperties": false,
          "type": "object"
        },
        "sub": {
          "properties": {
            "allow": {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            "deny": {
              "items": {
                "type": "string"
              },
              "type": "array"
            }
          },
          "additionalProperties": false,
          "type": "object"
        },
        "resp": {
          "properties": {
            "max": {
              "type": "integer"
            },
            "ttl": {
              "type": "integer"
            }
          },
          "additionalProperties": false,
          "type": "object",
          "required": [
            "max",
            "ttl"
          ]
        },
        "src": {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        "times": {
          "items": {
            "properties": {
              "start": {
                "type": "string"
              },
              "end": {
                "type": "string"
              }
            },
            "additionalProperties": false,
            "type": "object"
          },
          "type": "array"
        },
        "times_location": {
          "type": "string"
        },
        "subs": {
          "type": "integer"
        },
        "data": {
          "type": "integer"
        },
        "payload": {
          "type": "integer"
        },
        "bearer_token": {
          "type": "boolean"
        },
        "allowed_connection_types": {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        "issuer_account": {
          "type": "string"
        },
        "tags": {
          "items": {
            "type": "string"
          },
          "type": "array"
        },
        "type": {
          "type": "string"
        },
        "version": {
          "type": "integer"
        }
      },
      "additionalProperties": false,
      "type": "object"
    }
  },
  "additionalProperties": false,
  "type": "object"
}
```

</details>

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **config**: cấu hình
- **credential**: thông tin đăng nhập
- **log**: bản ghi sự kiện
- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **permission**: quyền truy cập
- **request**: yêu cầu
- **response**: phản hồi
- **schema**: cấu trúc dữ liệu
- **server**: máy chủ
- **service**: dịch vụ
- **timeout**: thời gian chờ tối đa
- **token**: chuỗi xác thực