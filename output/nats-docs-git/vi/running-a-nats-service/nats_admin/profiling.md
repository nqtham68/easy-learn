---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/profiling
title: Profiling NATS
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Profiling NATS

> 🇬🇧 *When investigating and debugging a performance issue with the NATS Server (i.e. unexpectedly high CPU or RAM utilisation), it may be necessary for you to collect and provide profiles from your deployment for troublshooting. These profiles are crucial to understand where CPU time and memory are being spent.*

Khi điều tra và debug sự cố hiệu năng trên NATS Server (chẳng hạn CPU hoặc RAM tăng bất thường), bạn có thể cần thu thập và cung cấp các profile từ deployment của mình để phục vụ quá trình troubleshooting. Các profile này rất quan trọng để xác định CPU time và bộ nhớ đang được sử dụng ở đâu.

> 🇬🇧 *Note that profiling is an advanced operation for development purposes only. Server operators should use the [monitoring port](./monitoring) instead for monitoring day-to-day runtime statistics.*

Lưu ý rằng profiling là thao tác nâng cao, chỉ dành cho mục đích phát triển. Operator của server nên dùng [monitoring port](./monitoring) để theo dõi các số liệu vận hành hằng ngày.

### Thông qua NATS CLI

> 🇬🇧 *The NATS CLI can request profiles from the NATS Server **when connected to the system account only**. Profiles will be written out to the current working directory by default as files, which can then either be sent onwards or inspected using [`go tool pprof`](https://pkg.go.dev/net/http/pprof).*

NATS CLI (công cụ dòng lệnh) có thể yêu cầu profile từ NATS Server **chỉ khi kết nối vào system account**. Các profile mặc định được ghi ra thư mục làm việc hiện tại dưới dạng file, sau đó có thể gửi đi hoặc kiểm tra bằng [`go tool pprof`](https://pkg.go.dev/net/http/pprof).

#### Memory profile

> 🇬🇧 *The `--name`, `--tags` and `--cluster` selectors can be used either individually or combined in order to request profiles from specific servers. Memory profiles are returned instantly. Examples include:*

Các selector `--name`, `--tags` và `--cluster` có thể dùng riêng lẻ hoặc kết hợp để yêu cầu profile từ các server cụ thể. Memory profile được trả về ngay lập tức. Ví dụ:

| Command                                                    | Description                                                                                   |
|------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| `nats server request profile allocs`                       | Yêu cầu memory profile từ tất cả server trong hệ thống                                       |
| `nats server request profile allocs ./profiles`            | Yêu cầu memory profile từ tất cả server trong hệ thống và ghi vào thư mục `profiles` |
| `nats server request profile allocs --name=servername1`    | Yêu cầu memory profile từ `servername1` duy nhất                                              |
| `nats server request profile allocs --tags=aws`            | Yêu cầu memory profile từ tất cả server được gắn tag `aws`                                     |
| `nats server request profile allocs --cluster=aws-useast2` | Yêu cầu memory profile từ tất cả server trong cluster (cụm nhiều server chạy chung) có tên `aws-useast2` |

#### CPU profile

> 🇬🇧 *The `--name`, `--tags` and `--cluster` selectors can be used either individually or combined in order to request profiles from specific servers. The `--timeout` option can also be provided as a means of specifying how long the CPU profile should run for. The default is 5 seconds. Examples include:*

Các selector `--name`, `--tags` và `--cluster` có thể dùng riêng lẻ hoặc kết hợp để yêu cầu profile từ các server cụ thể. Tùy chọn `--timeout` cho phép chỉ định thời gian chạy của CPU profile — mặc định là 5 giây. Ví dụ:

| Command                                                    | Description                                                                                |
|------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| `nats server request profile cpu`                          | Yêu cầu CPU profile từ tất cả server trong hệ thống                                       |
| `nats server request profile cpu ./profiles`               | Yêu cầu CPU profile từ tất cả server trong hệ thống và ghi vào thư mục `profiles` |
| `nats server request profile cpu --timeout=10s`            | Yêu cầu CPU profile từ tất cả server trong hệ thống trong khoảng 10 giây               |
| `nats server request profile cpu --name=servername1`       | Yêu cầu CPU profile từ `servername1` duy nhất                                              |
| `nats server request profile cpu --tags=aws`               | Yêu cầu CPU profile từ tất cả server được gắn tag `aws`                                     |
| `nats server request profile cpu --cluster=aws-useast2`    | Yêu cầu CPU profile từ tất cả server trong cluster có tên `aws-useast2` |

### Thông qua Profiling Port

> **⚠️ Cảnh báo:**
> `nats-server` does not have authentication/authorization for the profiling endpoint. When you plan to open your `nats-server` to the internet make sure to not expose the profiling port as well. By default, profiling binds to every interface `0.0.0.0` so consider setting profiling to `localhost` or have appropriate firewall rules.

> 🇬🇧 *The NATS Server can expose a HTTP `pprof` profiling port, although it must be enabled by setting the `prof_port` in your NATS Server configuration file. Note that the profiling port is not authenticated and should not be exposed to clients, to the internet etc. For example, to enable the profiling port on TCP/65432:*

NATS Server có thể mở một profiling port HTTP `pprof`, nhưng cần bật tính năng này bằng cách thiết lập `prof_port` trong file config (cấu hình) của NATS Server. Lưu ý rằng profiling port không được xác thực và không nên để lộ ra phía client hay internet. Ví dụ, để bật profiling port trên TCP/65432:

```
prof_port = 65432
```

> 🇬🇧 *Note that this option does not support [configuration-reloading](../configuration#configuration-reloading), so the server must be restarted for the config change to take effect.*

Lưu ý rằng tùy chọn này không hỗ trợ [configuration-reloading](../configuration#configuration-reloading), vì vậy server phải được khởi động lại để áp dụng thay đổi config.

> 🇬🇧 *Once the profiling port has been enabled, you can download profiles as per the following sections. These profiles can be inspected using [`go tool pprof`](https://pkg.go.dev/net/http/pprof).*

Sau khi profiling port được bật, bạn có thể tải xuống các profile theo hướng dẫn ở các phần dưới đây. Các profile này có thể được kiểm tra bằng [`go tool pprof`](https://pkg.go.dev/net/http/pprof).

> 🇬🇧 *To see all available profiles, open [http://localhost:65432/debug/pprof/](http://localhost:65432/debug/pprof/)*

Để xem tất cả profile có sẵn, mở [http://localhost:65432/debug/pprof/](http://localhost:65432/debug/pprof/)

#### Memory profile

> 🇬🇧 *`http://localhost:65432/debug/pprof/allocs`*

`http://localhost:65432/debug/pprof/allocs`

> 🇬🇧 *This endpoint will return instantly.*

Endpoint (địa chỉ API cụ thể) này trả về kết quả ngay lập tức.

> 🇬🇧 *For example, to download an allocation profile from NATS running on the same machine:*

Ví dụ, để tải allocation profile từ NATS đang chạy trên cùng máy:

```shell
curl -o mem.prof http://localhost:65432/debug/pprof/allocs
```

> 🇬🇧 *The profile will be saved into `mem.prof`.*

Profile sẽ được lưu vào `mem.prof`.

#### CPU profile

> 🇬🇧 *`http://localhost:65432/debug/pprof/profile?seconds=30`*

`http://localhost:65432/debug/pprof/profile?seconds=30`

> 🇬🇧 *This endpoint will block for the specified duration and then return. You can specify a different duration by adjusting `?seconds=` in the URL if you want to sample a shorter or longer period of time.*

Endpoint này sẽ block trong khoảng thời gian đã chỉ định rồi mới trả về. Bạn có thể thay đổi thời gian lấy mẫu bằng cách điều chỉnh `?seconds=` trong URL.

> 🇬🇧 *For example, to download a CPU profile from NATS running on the same machine with a 30 second window:*

Ví dụ, để tải CPU profile từ NATS đang chạy trên cùng máy với cửa sổ 30 giây:

```shell
curl -o cpu.prof http://localhost:65432/debug/pprof/profile?seconds=30
```

> 🇬🇧 *The profile will be saved into `cpu.prof`.*

Profile sẽ được lưu vào `cpu.prof`.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **endpoint**: địa chỉ API cụ thể