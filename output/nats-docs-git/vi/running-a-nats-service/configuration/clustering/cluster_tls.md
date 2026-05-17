---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/clustering/cluster_tls
title: Xác thực TLS trong Cluster
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Xác thực TLS trong Cluster

> 🇬🇧 *When setting up clusters, all servers in the cluster, if using TLS, will both verify the connecting endpoints and the server responses. So certificates are checked in [both directions](../securing_nats/tls.md#wrong-key-usage). Certificates can be configured only for the server's cluster identity, keeping client and server certificates separate from cluster formation.*

Khi thiết lập cluster (cụm nhiều server chạy chung), tất cả server trong cluster đều sẽ xác minh cả endpoint kết nối lẫn phản hồi từ server — nếu sử dụng TLS (mã hóa TLS). Vì vậy, certificate được kiểm tra theo [cả hai chiều](../securing_nats/tls.md#wrong-key-usage). Certificate có thể được cấu hình riêng cho danh tính cluster của server, tách biệt hoàn toàn khỏi certificate dùng cho client và server thông thường.

> 🇬🇧 *TLS Mutual Authentication _is the only way_ of securing routes.*

TLS Mutual Authentication _là cách duy nhất_ để bảo mật các route (đường dẫn URL).

```
cluster {
  listen: 127.0.0.1:4244

  tls {
    # Route cert
    cert_file: "./configs/certs/srva-cert.pem"
    # Private key
    key_file:  "./configs/certs/srva-key.pem"
    # Optional certificate authority verifying connected routes
    # Required when we have self-signed CA, etc.
    ca_file:   "./configs/certs/ca.pem"
  }
  # Routes are actively solicited and connected to from this server.
  # Other servers can connect to us if they supply the correct credentials
  # in their routes definitions from above.
  routes = [
    nats://127.0.0.1:4246
  ]
}
```

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **client**: bên gọi (phía người dùng)
- **endpoint**: địa chỉ API cụ thể
- **route**: đường dẫn URL
- **server**: máy chủ
- **TLS**: mã hóa TLS