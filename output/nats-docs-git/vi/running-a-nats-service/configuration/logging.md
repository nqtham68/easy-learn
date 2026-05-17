---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration/logging
title: Cấu hình Logging
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Cấu hình Logging

## Cấu hình Logging

> 🇬🇧 *The NATS server provides various logging options that you can set via the command line or the configuration file.*

NATS server (máy chủ) cung cấp nhiều tùy chọn logging có thể thiết lập qua command line hoặc file config (cấu hình).

### Tùy chọn Command Line

> 🇬🇧 *The following logging operations are supported:*

Các tùy chọn logging sau được hỗ trợ:

```
-l, --log FILE                   File to redirect log output.
-T, --logtime                    Timestamp log entries (default is true).
-s, --syslog                     Enable syslog as log method.
-r, --remote_syslog              Syslog server address.
-D, --debug                      Enable debugging output.
-V, --trace                      Trace the raw protocol.
-VV                              Verbose trace (traces system account as well)
-DV                              Debug and Trace.
-DVV                             Debug and verbose trace (traces system account as well)
```

#### Debug và trace

> 🇬🇧 *The `-DV` flag enables trace and debug for the server.*

Flag `-DV` bật chế độ trace và debug cho server.

```bash
nats-server -DV -m 8222 -user foo -pass bar
```

#### Chuyển hướng file log

```bash
nats-server -DV -m 8222 -l nats.log
```

#### Timestamp

> 🇬🇧 *If `-T false` then log entries are not timestamped. Default is true.*

Nếu `-T false` thì các dòng log sẽ không có timestamp. Mặc định là true.

#### Syslog

> 🇬🇧 *You can configure syslog with `UDP`:*

Có thể cấu hình syslog bằng `UDP`:

```bash
nats-server -r udp://localhost:514
```

> 🇬🇧 *or `syslog:`*

hoặc `syslog:`

```bash
nats-server -r syslog://<hostname>:<port>
```

> 🇬🇧 *For example:*

Ví dụ:

```bash
syslog://logs.papertrailapp.com:26900
```

### Sử dụng File Config

> 🇬🇧 *All of these settings are available in the configuration file as well.*

Tất cả các thiết lập trên đều có thể khai báo trong file config.

```
debug:   false
trace:   true
logtime: false
logfile_size_limit: 1GB
logfile_max_num: 100
log_file: "/tmp/nats-server.log"
```

### Log Rotation

> 🇬🇧 *Introduced in NATS Server v2.1.4, NATS allows for auto-rotation of log files when the size is greater than the configured limit set in `logfile_size_limit`. The backup files will have the same name as the original log file with the suffix .yyyy.mm.dd.hh.mm.ss.micros.*

Từ NATS Server v2.1.4, NATS hỗ trợ tự động xoay vòng (auto-rotation) file log khi kích thước vượt quá giới hạn được đặt trong `logfile_size_limit`. File backup sẽ có cùng tên với file log gốc, kèm hậu tố `.yyyy.mm.dd.hh.mm.ss.micros`.

> 🇬🇧 *You can also use NATS-included mechanisms with [logrotate](https://github.com/logrotate/logrotate), a simple standard Linux utility to rotate logs available on most distributions like Debian, Ubuntu, RedHat (CentOS), etc., to make log rotation simple.*

Ngoài ra, NATS còn tích hợp hỗ trợ [logrotate](https://github.com/logrotate/logrotate) — tiện ích Linux phổ biến để xoay vòng log, có trên hầu hết các bản phân phối như Debian, Ubuntu, RedHat (CentOS), v.v.

> 🇬🇧 *For example, you could configure `logrotate` with:*

Ví dụ, có thể cấu hình `logrotate` như sau:

```
/path/to/nats-server.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
    postrotate
        kill -SIGUSR1 `cat /var/run/nats-server.pid`
    endscript
}
```

> 🇬🇧 *The first line specifies the location that the subsequent lines will apply to.*

Dòng đầu tiên chỉ định đường dẫn mà các thiết lập bên dưới sẽ áp dụng.

> 🇬🇧 *The rest of the file specifies that the logs will rotate daily ("daily" option) and that 30 older copies will be preserved ("rotate" option). Other options are described in [logrorate documentation](https://linux.die.net/man/8/logrotate).*

Phần còn lại cấu hình log xoay vòng theo ngày (tùy chọn "daily") và giữ lại 30 bản cũ (tùy chọn "rotate"). Các tùy chọn khác được mô tả trong [tài liệu logrotate](https://linux.die.net/man/8/logrotate).

> 🇬🇧 *The "postrotate" section tells NATS server to reload the log files once the rotation is complete. The command `` `kill -SIGUSR1 ``cat /var/run/nats-server.pid\`\`\` does not kill the NATS server process, but instead sends it a signal causing it to reload its log files. This will cause new requests to be logged to the refreshed log file.*

Phần "postrotate" yêu cầu NATS server tải lại file log sau khi hoàn tất xoay vòng. Lệnh `` `kill -SIGUSR1 ``cat /var/run/nats-server.pid\`\`\` không dừng tiến trình NATS server, mà gửi tín hiệu để server tải lại file log. Từ đó, các request (yêu cầu) mới sẽ được ghi vào file log mới.

> 🇬🇧 *The `/var/run/nats-server.pid` file is where NATS server stores the master process's pid.*

File `/var/run/nats-server.pid` là nơi NATS server lưu PID của tiến trình chính.

## Một số Lưu ý về Logging

> 🇬🇧 *The NATS server, in verbose mode, will log the receipt of `UNSUB` messages, but this does not indicate the subscription is gone, only that the message was received. The `DELSUB` message in the log can be used to determine when the actual subscription removal has taken place.*

Ở chế độ verbose, NATS server sẽ log việc nhận message `UNSUB`, nhưng điều này không có nghĩa là subscription đã bị huỷ — chỉ đơn thuần là message đã được nhận. Dòng log `DELSUB` mới là dấu hiệu cho biết subscription đã thực sự bị gỡ bỏ.

## Thuật ngữ trong bài

- **config**: cấu hình
- **log**: bản ghi sự kiện
- **message**: gói dữ liệu được gửi đi
- **request**: yêu cầu
- **server**: máy chủ