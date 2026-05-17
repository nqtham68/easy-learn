---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/security
title: Quản lý Bảo mật NATS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Quản lý Bảo mật NATS

> 🇬🇧 *If you are using the [JWT](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/jwt) model of authentication to secure your NATS infrastructure or implementing an [Auth callout](../configuration/securing_nats/auth_callout.md) service, you can administer authentication and authorization without having to change the servers' configuration files.*

Nếu bạn đang dùng mô hình xác thực [JWT](https://docs.nats.io/running-a-nats-service/configuration/securing\_nats/jwt) để bảo vệ hạ tầng NATS, hoặc triển khai service (dịch vụ) [Auth callout](../configuration/securing_nats/auth_callout.md), bạn có thể quản lý authentication và authorization mà không cần thay đổi config (cấu hình) file của server.

> 🇬🇧 *You can use the [`nsc`](../../using-nats/nats-tools/nsc) CLI tool to manage identities. Identities take the form of nkeys. Nkeys are a public-key signature system based on Ed25519 for the NATS ecosystem. The nkey identities are associated with NATS configuration in the form of a JSON Web Token (JWT). The JWT is digitally signed by the private key of an issuer forming a chain of trust. The nsc tool creates and manages these identities and allows you to deploy them to a JWT account server, which in turn makes the configurations available to nats-servers.*

Bạn có thể dùng CLI tool [`nsc`](../../using-nats/nats-tools/nsc) để quản lý các identity. Mỗi identity có dạng nkey — một hệ thống chữ ký public key dựa trên Ed25519, được thiết kế cho hệ sinh thái NATS. Các nkey identity được liên kết với NATS config thông qua JSON Web Token (JWT) — một token (chuỗi xác thực) được ký số bằng private key của issuer, tạo thành chuỗi tin cậy (chain of trust). Công cụ nsc giúp tạo và quản lý các identity này, đồng thời cho phép deploy chúng lên JWT account server — server này sẽ phân phối config đến các nats-server.

> 🇬🇧 *You can also use [`nk`](https://github.com/nats-io/nkeys#readme) CLI tool and library to manage keys.*

Bạn cũng có thể dùng CLI tool và library [`nk`](https://github.com/nats-io/nkeys#readme) để quản lý key.

## Tạo, cập nhật và quản lý JWT theo chương trình

> 🇬🇧 *You can create, update and delete accounts and users programmatically using the following libraries:*

Bạn có thể tạo, cập nhật và xóa account cũng như user theo chương trình bằng các library sau:

* Golang: xem [NKEYS](https://github.com/nats-io/nkeys) và [JWT](https://github.com/nats-io/jwt/tree/main/v2).
* Java: xem [NKey.java](https://github.com/nats-io/nats.java/blob/main/src/main/java/io/nats/client/NKey.java) và [JwtUtils.java](https://github.com/nats-io/nats.java/blob/main/src/main/java/io/nats/client/support/JwtUtils.java)

## Tích hợp với hệ thống authentication/authorization hiện có

> 🇬🇧 *You can integrate NATS with your existing authentication/authorization system or create your own custom authentication using the [Auth callout](../configuration/securing_nats/auth_callout.md).*

Bạn có thể tích hợp NATS với hệ thống authentication/authorization hiện có, hoặc xây dựng authentication tùy chỉnh bằng [Auth callout](../configuration/securing_nats/auth_callout.md).

### Ví dụ

> 🇬🇧 *See [NATS by Example](https://natsbyexample.com/) under "Authentication and Authorization" for JWT and Auth callout server implementation examples.*

Xem [NATS by Example](https://natsbyexample.com/) mục "Authentication and Authorization" để tham khảo các ví dụ triển khai JWT và Auth callout server.

#### User JWT

[Tạo user trong Golang](./jwt.md#automated-sign-up-services---jwt-and-nkey-libraries)

#### Account JWT

Ví dụ Golang từ <a href="https://natsbyexample.com/examples/auth/nkeys-jwts/go">https://natsbyexample.com/examples/auth/nkeys-jwts/go</a>

```
package main

import (
	"flag"
	"fmt"
	"log"

	"github.com/nats-io/jwt/v2"
	"github.com/nats-io/nkeys"
)

func main() {
	log.SetFlags(0)

	var (
		accountSeed  string
		operatorSeed string
		name         string
	)

	flag.StringVar(&operatorSeed, "operator", "", "Operator seed for creating an account.")
	flag.StringVar(&accountSeed, "account", "", "Account seed for creating a user.")
	flag.StringVar(&name, "name", "", "Account or user name to be created.")

	flag.Parse()

	if accountSeed != "" && operatorSeed != "" {
		log.Fatal("operator and account cannot both be provided")
	}

	var (
		jwt string
		err error
	)

	if operatorSeed != "" {
		jwt, err = createAccount(operatorSeed, name)
	} else if accountSeed != "" {
		jwt, err = createUser(accountSeed, name)
	} else {
		flag.PrintDefaults()
		return
	}
	if err != nil {
		log.Fatalf("error creating account JWT: %v", err)
	}

	fmt.Println(jwt)
}

func createAccount(operatorSeed, accountName string) (string, error) {
	akp, err := nkeys.CreateAccount()
	if err != nil {
		return "", fmt.Errorf("unable to create account using nkeys: %w", err)
	}

	apub, err := akp.PublicKey()
	if err != nil {
		return "", fmt.Errorf("unable to retrieve public key: %w", err)
	}

	ac := jwt.NewAccountClaims(apub)
	ac.Name = accountName

	// Load operator key pair
	okp, err := nkeys.FromSeed([]byte(operatorSeed))
	if err != nil {
		return "", fmt.Errorf("unable to create operator key pair from seed: %w", err)
	}

	// Sign the account claims and convert it into a JWT string
	ajwt, err := ac.Encode(okp)
	if err != nil {
		return "", fmt.Errorf("unable to sign the claims: %w", err)
	}

	return ajwt, nil
}

func createUser(accountSeed, userName string) (string, error) {
	ukp, err := nkeys.CreateUser()
	if err != nil {
		return "", fmt.Errorf("unable to create user using nkeys: %w", err)
	}

	upub, err := ukp.PublicKey()
	if err != nil {
		return "", fmt.Errorf("unable to retrieve public key: %w", err)
	}

	uc := jwt.NewUserClaims(upub)
	uc.Name = userName

	// Load account key pair
	akp, err := nkeys.FromSeed([]byte(accountSeed))
	if err != nil {
		return "", fmt.Errorf("unable to create account key pair from seed: %w", err)
	}

	// Sign the user claims and convert it into a JWT string
	ujwt, err := uc.Encode(akp)
	if err != nil {
		return "", fmt.Errorf("unable to sign the claims: %w", err)
	}

	return ujwt, nil
}
```

### Lưu ý

> 🇬🇧 *You can see the key (and any signing keys) of your operator using `nsc list keys --show-seeds`, you should use a 'signing key' to create the account JWTs (as singing keys can be revoked/rotated easily)*

Bạn có thể xem key (và các signing key) của operator bằng `nsc list keys --show-seeds`. Nên dùng "signing key" khi tạo account JWT vì signing key có thể thu hồi hoặc xoay vòng dễ dàng.

> 🇬🇧 *To delete accounts use the `"$SYS.REQ.CLAIMS.DELETE"` (see [reference](./jwt.md#subjects-available-when-using-nats-based-resolver)) and make sure to enable JWT deletion in your nats-server resolver (`config allow_delete: true` in the `resolver` stanza of the server configuration).*

Để xóa account, dùng `"$SYS.REQ.CLAIMS.DELETE"` (xem [tài liệu tham khảo](./jwt.md#subjects-available-when-using-nats-based-resolver)) và đảm bảo đã bật tính năng xóa JWT trong resolver của nats-server (`config allow_delete: true` trong stanza `resolver` của server configuration).

> 🇬🇧 *The system is just like any other account, the only difference is that it is listed as system account in the operator's JWT (and the server config).*

System account về bản chất giống như bất kỳ account nào khác — điểm khác biệt duy nhất là nó được khai báo là system account trong JWT của operator (và trong server config).

## Thuật ngữ trong bài

- **CLI**: công cụ dòng lệnh
- **config**: cấu hình
- **deploy**: triển khai
- **service**: dịch vụ
- **token**: chuỗi xác thực