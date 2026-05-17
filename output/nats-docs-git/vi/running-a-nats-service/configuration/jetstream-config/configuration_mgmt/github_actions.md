---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/jetstream-config/configuration_mgmt/github_actions
title: GitHub Actions cho JetStream
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# GitHub Actions

> 🇬🇧 *We have a pack of GitHub Actions that let you manage an already running JetStream Server, useful for managing releases or standing up test infrastructure.*

Chúng tôi cung cấp một bộ GitHub Actions cho phép quản lý JetStream Server (stream (luồng message lưu trữ liên tục) server) đang chạy, hữu ích khi quản lý release hoặc dựng hạ tầng test.

> 🇬🇧 *Full details and examples are in the [jetstream-gh-actions](https://github.com/nats-io/jetstream-gh-action) repository, here's an example.*

Chi tiết đầy đủ và ví dụ có trong repository [jetstream-gh-actions](https://github.com/nats-io/jetstream-gh-action). Dưới đây là một ví dụ minh họa.

```yaml
on: push
name: orders
jobs:

  # First we delete the ORDERS stream and consumer if they already exist
  clean_orders:
    runs-on: ubuntu-latest
    steps:
      - name: orders_stream
        uses: nats-io/jetstream-gh-action/delete/stream@master
        with:
          missing_ok: 1
          stream: ORDERS
          server: js.example.net

  # Now we create the Stream and Consumers using the same configuration files the 
  # nats CLI utility would use as shown above
  create_orders:
    runs-on: ubuntu-latest
    needs: clean_orders
    steps:
      - uses: actions/checkout@master
      - name: orders_stream
        uses: nats-io/jetstream-gh-action/create/stream@master
        with:
          config: ORDERS.json
          server: js.example.net
      - name: orders_new_consumer
        uses: nats-io/jetstream-gh-action/create/consumer@master
        with:
          config: ORDERS_NEW.json
          stream: ORDERS
          server: js.example.net

  # We publish a message to a specific Subject, perhaps some consumer is 
  # waiting there for it to kick off tests
  publish_message:
    runs-on: ubuntu-latest
    needs: create_orders
    steps:
      - uses: actions/checkout@master
      - name: orders_new_consumer
        uses: nats-io/jetstream-gh-action@master
        with:
          subject: ORDERS.deployment
          message: Published new deployment via "${{ github.event_name }}" in "${{ github.repository }}"
          server: js.example.net
```

## Thuật ngữ trong bài

- **stream**: luồng message lưu trữ liên tục