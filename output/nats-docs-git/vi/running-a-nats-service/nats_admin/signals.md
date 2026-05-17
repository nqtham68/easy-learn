---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/signals
title: Signals (Tín hiệu hệ thống)
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Signals (Tín hiệu hệ thống)

## Command Line

> 🇬🇧 *On Unix systems, the NATS server responds to the following signals. You can send these using the standard Unix `kill` command, or use the `nats-server --signal` command for convenience.*

Trên hệ thống Unix, NATS server lắng nghe các signal sau. Có thể gửi signal bằng lệnh Unix chuẩn `kill`, hoặc dùng lệnh `nats-server --signal` cho tiện.

| nats-server command | Unix Signal | Description                                                    |
| :------------------ | :---------- | :------------------------------------------------------------- |
| `--signal ldm`      | `SIGUSR2`   | Tắt server từ từ, di chuyển client dần dần \([lame duck mode](./lame_duck_mode.md)\) |
| `--signal quit`     | `SIGINT`    | Dừng server theo cách graceful                                 |
| `--signal term`     | `SIGTERM`   | Dừng server theo cách graceful                                 |
| `--signal stop`     | `SIGKILL`   | Kết thúc tiến trình ngay lập tức                               |
| `--signal reload`   | `SIGHUP`    | Tải lại file config của server                                 |
| `--signal reopen`   | `SIGUSR1`   | Mở lại file log để thực hiện log rotation                      |
| _(kill only)_       | `SIGQUIT`   | Kết thúc tiến trình ngay lập tức và thực hiện [stack dump](https://pkg.go.dev/os/signal#hdr-Default_behavior_of_signals_in_Go_programs) |

### Cách sử dụng

> 🇬🇧 *To send a signal to a running nats-server:*

Để gửi signal tới nats-server đang chạy:

```shell
nats-server --signal <command>
```

> 🇬🇧 *For example, to gracefully stop the server with lame duck mode:*

Ví dụ, để dừng server theo lame duck mode:

```shell
nats-server --signal ldm
```

### Nhiều tiến trình

> 🇬🇧 *If there are multiple `nats-server` processes running, or if `pgrep` isn't available, you must either specify a PID or the absolute path to a PID file:*

Nếu có nhiều tiến trình `nats-server` đang chạy, hoặc `pgrep` không khả dụng, cần chỉ định PID hoặc đường dẫn tuyệt đối tới file PID:

```shell
nats-server --signal stop=<pid>
```

```shell
nats-server --signal stop=/path/to/pidfile
```

> 🇬🇧 *As of NATS v2.10.0, a glob expression can be used to match one or more process IDs, such as:*

Từ NATS v2.10.0, có thể dùng glob expression để khớp một hoặc nhiều process ID, ví dụ:

```shell
nats-server --signal ldm=12*
```

## Windows

> 🇬🇧 *See the [Windows Service](../running/windows_srv.md) section for information on signaling the NATS server on Windows.*

Xem mục [Windows Service](../running/windows_srv.md) để biết cách gửi signal tới NATS server trên Windows.

## Thuật ngữ trong bài

- **config**: cấu hình
- **log**: bản ghi sự kiện
- **server**: máy chủ