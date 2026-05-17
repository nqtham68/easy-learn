---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/monitoring
title: Bật Tính Năng Monitoring
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Bật Tính Năng Monitoring

## Giám Sát NATS Server

> 🇬🇧 *To monitor the NATS messaging system, `nats-server` provides a lightweight HTTP server on a dedicated monitoring port. The monitoring server provides several endpoints, providing statistics and other information.*

Để giám sát hệ thống messaging NATS, `nats-server` cung cấp một HTTP server nhẹ chạy trên một port riêng dành cho monitoring. Server này cung cấp nhiều endpoint (địa chỉ API cụ thể) trả về số liệu thống kê và các thông tin liên quan.

> 🇬🇧 *The [NATS monitoring endpoints](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring) support [JSONP](https://en.wikipedia.org/wiki/JSONP) and [CORS](https://en.wikipedia.org/wiki/Cross-origin\_resource\_sharing#How\_CORS\_works), making it easy to create single page monitoring web applications.*

Các [NATS monitoring endpoint](https://docs.nats.io/running-a-nats-service/nats\_admin/monitoring) hỗ trợ [JSONP](https://en.wikipedia.org/wiki/JSONP) và [CORS](https://en.wikipedia.org/wiki/Cross-origin\_resource\_sharing#How\_CORS\_works), giúp dễ dàng xây dựng ứng dụng web monitoring dạng single-page.

> 🇬🇧 *Warning: `nats-server` does not have authentication/authorization for the monitoring endpoint. When you plan to open your `nats-server` to the internet make sure to not expose the monitoring port as well. By default monitoring binds to every interface `0.0.0.0` so consider setting monitoring to `localhost` or have appropriate firewall rules.*

> Cảnh báo: `nats-server` không có authentication/authorization cho monitoring endpoint. Khi mở `nats-server` ra internet, hãy đảm bảo không để lộ monitoring port. Mặc định, monitoring bind vào tất cả các interface `0.0.0.0`, vì vậy hãy cân nhắc giới hạn monitoring về `localhost` hoặc thiết lập firewall rules phù hợp.

### Bật Monitoring Từ Command Line

> 🇬🇧 *To enable the monitoring server, start the NATS server with the monitoring flag `-m` and the monitoring port, or turn it on in the [configuration file](./monitoring.md#enable-monitoring-from-the-configuration-file).*

Để bật monitoring server, khởi động NATS server với flag `-m` kèm monitoring port, hoặc bật qua [configuration file](./monitoring.md#enable-monitoring-from-the-configuration-file).

```
-m, --http_port PORT             HTTP PORT for monitoring
-ms,--https_port PORT            Use HTTPS PORT for monitoring
```

Ví dụ:

```bash
nats-server -m 8222
```

```
[4528] 2019/06/01 20:09:58.572939 [INF] Starting nats-server version 2.0.0
[4528] 2019/06/01 20:09:58.573007 [INF] Starting http monitor on port 8222
[4528] 2019/06/01 20:09:58.573071 [INF] Listening for client connections on 0.0.0.0:4222
[4528] 2019/06/01 20:09:58.573090 [INF] nats-server is ready
```

> 🇬🇧 *To test, run `nats-server -m 8222`, then go to [http://localhost:8222/](http://localhost:8222/)*

Để kiểm tra, chạy `nats-server -m 8222`, sau đó truy cập [http://localhost:8222/](http://localhost:8222/).

### Bật Monitoring Từ Configuration File

> 🇬🇧 *You can also enable monitoring using the configuration file as follows:*

Bạn cũng có thể bật monitoring qua configuration file như sau:

```yaml
http_port: 8222
```

> 🇬🇧 *Binding to `localhost` as well:*

Bind thêm vào `localhost`:

```yaml
http: localhost:8222
```

> 🇬🇧 *For example, to monitor this server locally, the endpoint would be [http://localhost:8222/varz](http://localhost:8222/varz). It reports various general statistics.*

Ví dụ, để giám sát server cục bộ, endpoint sẽ là [http://localhost:8222/varz](http://localhost:8222/varz). Endpoint này trả về các metric (số liệu đo lường) thống kê tổng quát.

## Monitoring Tools

> 🇬🇧 *In addition to writing custom monitoring tools, you can monitor nats-server in Prometheus. The [Prometheus NATS Exporter](https://github.com/nats-io/prometheus-nats-exporter) allows you to configure the metrics you want to observe and store in Prometheus. There's a sample [Grafana](https://grafana.com) dashboard that you can use to visualize the server metrics.*

Ngoài việc tự viết monitoring tools, bạn có thể giám sát nats-server qua Prometheus. [Prometheus NATS Exporter](https://github.com/nats-io/prometheus-nats-exporter) cho phép cấu hình các metric cần thu thập và lưu trữ trong Prometheus. Đã có sẵn một dashboard [Grafana](https://grafana.com) mẫu để trực quan hóa các metric của server.

## Thuật ngữ trong bài

- **endpoint**: địa chỉ API cụ thể
- **metric**: số liệu đo lường
- **port**: cổng kết nối
- **server**: máy chủ