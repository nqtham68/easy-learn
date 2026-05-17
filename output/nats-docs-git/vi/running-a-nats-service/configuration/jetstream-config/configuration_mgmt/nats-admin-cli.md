---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/jetstream-config/configuration_mgmt/nats-admin-cli
title: CLI Quản trị NATS
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# CLI Quản trị NATS

## nats Admin CLI

> 🇬🇧 *The [`nats` CLI](https://github.com/nats-io/natscli?tab=readme-ov-file#installation) can be used to manage Streams and Consumers easily using it's `--config` flag, for example:*

[`nats` CLI](https://github.com/nats-io/natscli?tab=readme-ov-file#installation) có thể dùng để quản lý Stream (luồng message lưu trữ liên tục) và Consumer (bên xử lý dữ liệu từ stream) một cách dễ dàng thông qua flag `--config`, ví dụ:

## Thêm Stream mới

> 🇬🇧 *This creates a new Stream based on `orders.json`. The `orders.json` file can be extracted from an existing stream using `nats stream info ORDERS -j | jq .config`*

Lệnh này tạo một Stream mới dựa trên `orders.json`. File `orders.json` có thể được trích xuất từ một stream đã có bằng `nats stream info ORDERS -j | jq .config`.

```shell
nats str add ORDERS --config orders.json
```

## Chỉnh sửa Stream hiện có

> 🇬🇧 *This edits an existing stream ensuring it complies with the configuration in `orders.json`*

Lệnh này chỉnh sửa một stream hiện có, đảm bảo stream tuân theo config (cấu hình) trong `orders.json`.

```shell
nats str edit ORDERS --config orders.json
```

## Thêm Consumer mới

> 🇬🇧 *This creates a new Consumer based on `orders_new.json`. The `orders_new.json` file can be extracted from an existing stream using `nats con info ORDERS NEW -j | jq .config`*

Lệnh này tạo một Consumer mới dựa trên `orders_new.json`. File `orders_new.json` có thể được trích xuất từ một stream đã có bằng `nats con info ORDERS NEW -j | jq .config`.

```shell
nats con add ORDERS NEW --config orders_new.json
```

## Thuật ngữ trong bài

- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **stream**: luồng message lưu trữ liên tục