---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/jetstream_admin/disaster_recovery
title: Khôi Phục Thảm Họa
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Khôi Phục Thảm Họa

> 🇬🇧 *In the event of unrecoverable JetStream message persistence on one (or more) server nodes, there are two recovery scenarios:*

Khi JetStream không thể khôi phục dữ liệu trên một hoặc nhiều server node, có hai kịch bản phục hồi:

* Tự động phục hồi từ các quorum node còn nguyên vẹn
* Phục hồi thủ công từ snapshot (bản sao lưu) đã có

> **🚨 Danger:**
> For R1 streams, data is persisted on one server node only. If that server node is unrecoverable then recovery from
> backup is the sole option.

> **🚨 Nguy hiểm:**
> Với stream (luồng message lưu trữ liên tục) R1, dữ liệu chỉ lưu trên một server node duy nhất. Nếu node đó không thể phục hồi, backup là lựa chọn duy nhất.

## Tự Động Phục Hồi

> 🇬🇧 *NATS will create replacement stream replicas automatically under the following conditions:*

NATS sẽ tự động tạo replica (bản sao dữ liệu) thay thế cho stream khi đáp ứng đủ các điều kiện sau:

* Stream bị ảnh hưởng có cấu hình replica R3 trở lên
* Các node còn nguyên vẹn đáp ứng quorum tối thiểu của RAFT: floor(R/2) + 1
* Có node khả dụng trong cluster (cụm nhiều server chạy chung) của stream để tạo replica mới
* Các node bị ảnh hưởng đã được loại khỏi RAFT Meta group của domain (ví dụ: `nats server cluster peer-remove`)

## Phục Hồi Thủ Công

> 🇬🇧 *Snapshots (also known as backups) can pro-actively be made of any stream regardless of replication configuration.*

Snapshot (bản sao lưu) có thể được tạo chủ động cho bất kỳ stream nào, bất kể cấu hình replication.

> 🇬🇧 *The backup includes (by default):*

Backup bao gồm (theo mặc định):

* Cấu hình và trạng thái của stream
* Cấu hình và trạng thái của durable consumer
* Toàn bộ payload của message, bao gồm metadata như timestamp và header

### Backup

> 🇬🇧 *The `nats stream backup` CLI command is used to create snapshots of a stream and its durable consumers.*

Lệnh CLI `nats stream backup` dùng để tạo snapshot cho stream và các durable consumer (bên xử lý dữ liệu từ stream) của nó.

> **ℹ️ Info:**
> As an account owner, if you wish to make a backup of ALL streams in your account, you may use `nats account backup` instead.

> **ℹ️ Thông tin:**
> Nếu bạn là chủ tài khoản và muốn backup TẤT CẢ stream trong tài khoản, hãy dùng `nats account backup`.

> **⚠️ Warning:**
> Memory storage streams do not support snapshots. Only file-based storage streams can be backed up.

> **⚠️ Cảnh báo:**
> Stream lưu trữ trên memory không hỗ trợ snapshot. Chỉ stream lưu trữ dạng file mới có thể backup.

```shell
nats stream backup ORDERS '/data/js-backup/backup1'
```
Output
```text
Starting backup of Stream "ORDERS" with 13 data blocks

2.4 MiB/s [====================================================================] 100%

Received 13 MiB bytes of compressed data in 3368 chunks for stream "ORDERS" in 1.223428188s, 813 MiB uncompressed
```

> 🇬🇧 *During a backup operation, the stream is placed in a status where it's configuration cannot change and no data will be evicted based on stream retention policies.*

Trong quá trình backup, stream được đặt vào trạng thái không thể thay đổi cấu hình và dữ liệu sẽ không bị xóa theo retention policy.

> **ℹ️ Info:**
> Progress using the terminal bar can be disabled using `--no-progress`, it will then issue log lines instead.

> **ℹ️ Thông tin:**
> Có thể tắt thanh tiến trình trên terminal bằng `--no-progress`; khi đó tiến trình sẽ được hiển thị dưới dạng log.

### Restore

> 🇬🇧 *An existing backup (as above) can be restored to the same or a new NATS server (or cluster) using the `nats stream restore` command.*

Backup đã tạo có thể được phục hồi vào cùng một hoặc NATS server (hay cluster) khác bằng lệnh `nats stream restore`.

> **ℹ️ Info:**
> `nats stream restore` restores a single stream from one backup directory. To restore all streams at once, use `nats account restore` as described below.

> **ℹ️ Thông tin:**
> `nats stream restore` phục hồi một stream từ một thư mục backup. Để phục hồi tất cả stream cùng lúc, dùng `nats account restore` như mô tả bên dưới.

```shell
nats stream restore '/data/js-backup/backup1'
```
Output
```text
Starting restore of Stream "ORDERS" from file "/data/js-backup/backup1"

13 MiB/s [====================================================================] 100%

Restored stream "ORDERS" in 937.071149ms

Information for Stream ORDERS

Configuration:

             Subjects: ORDERS.>
...
```

> 🇬🇧 *Progress using the terminal bar can be disabled using `--no-progress`, it will then issue log lines instead.*

Có thể tắt thanh tiến trình trên terminal bằng `--no-progress`; khi đó tiến trình sẽ hiển thị dưới dạng log.

## Backup và Restore Cấp Tài Khoản

> 🇬🇧 *In environments where the `nats` CLI is used interactively to configure the server you do not have a desired state to recreate the server from. This is not the ideal way to administer the server, we recommend Configuration Management, but many will use this approach.*

Trong các môi trường dùng `nats` CLI theo kiểu tương tác để cấu hình server, bạn không có trạng thái mong muốn để tái tạo server từ đó. Đây không phải cách quản trị lý tưởng — chúng tôi khuyến nghị dùng Configuration Management — nhưng nhiều người vẫn sử dụng cách này.

> 🇬🇧 *The `nats account backup` and `nats account restore` commands allow you to back up and restore all streams in an account at once, including their configuration, consumer state, and all message data.*

Lệnh `nats account backup` và `nats account restore` cho phép backup và restore tất cả stream trong một tài khoản cùng lúc, bao gồm cấu hình, trạng thái consumer và toàn bộ dữ liệu message.

### Account Backup

```shell
nats account backup /data/js-backup
```
Output
```text
Performing backup of all streams to /data/js-backup

    Streams: 3
       Size: 14 KiB
  Consumers: 2

Starting backup of Stream "EVENTS" with 0 B
Received 1.5 KiB compressed data in 2 chunks for stream "EVENTS" in 0s, 16 KiB uncompressed

Starting backup of Stream "ORDERS" with 55 B
Received 976 B compressed data in 2 chunks for stream "ORDERS" in 1ms, 9.5 KiB uncompressed

Starting backup of Stream "WORK" with 7.3 KiB
Received 7.3 KiB compressed data in 2 chunks for stream "WORK" in 0s, 30 KiB uncompressed
```

> 🇬🇧 *This creates a subdirectory per stream inside `/data/js-backup`, each containing the full stream snapshot (configuration, consumer state, and message data) in the same format as `nats stream backup`.*

Lệnh này tạo một thư mục con cho mỗi stream bên trong `/data/js-backup`, mỗi thư mục chứa snapshot đầy đủ (cấu hình, trạng thái consumer và dữ liệu message) theo cùng định dạng với `nats stream backup`.

> 🇬🇧 *Available flags for `nats account backup`:*

Các flag khả dụng cho `nats account backup`:

| Flag | Description |
| :--- | :--- |
| `--consumers` | Include consumer configuration and state |
| `--check` | Check backup integrity |
| `--force` | Force overwrite of existing backup directory |
| `--critical-warnings` | Treat warnings as critical errors |

| Flag | Mô tả |
| :--- | :--- |
| `--consumers` | Bao gồm cấu hình và trạng thái consumer |
| `--check` | Kiểm tra tính toàn vẹn của backup |
| `--force` | Ghi đè thư mục backup hiện có |
| `--critical-warnings` | Coi cảnh báo là lỗi nghiêm trọng |

### Account Restore

```shell
nats account restore /data/js-backup
```
Output
```text
Restoring backup of all 3 streams in directory "/data/js-backup"

Starting restore of Stream "EVENTS" from file "/data/js-backup/EVENTS"
Restored stream "EVENTS" in 0s
...

Starting restore of Stream "ORDERS" from file "/data/js-backup/ORDERS"
Restored stream "ORDERS" in 1ms
...

Starting restore of Stream "WORK" from file "/data/js-backup/WORK"
Restored stream "WORK" in 0s
...
```

> 🇬🇧 *This restores all stream subdirectories found in `/data/js-backup`, including their full message data and consumer state.*

Lệnh này phục hồi tất cả thư mục con của stream tìm thấy trong `/data/js-backup`, bao gồm toàn bộ dữ liệu message và trạng thái consumer.

> 🇬🇧 *Available flags for `nats account restore`:*

Các flag khả dụng cho `nats account restore`:

| Flag | Description |
| :--- | :--- |
| `--cluster` | Target cluster for restored streams |
| `--tag` | Placement tag for restored streams |

| Flag | Mô tả |
| :--- | :--- |
| `--cluster` | Cluster đích để phục hồi stream |
| `--tag` | Tag đặt vị trí cho stream được phục hồi |

> **⚠️ Warning:**
> `nats account restore` will fail if a stream with the same name already exists. You must remove the existing stream before restoring from backup.

> **⚠️ Cảnh báo:**
> `nats account restore` sẽ thất bại nếu đã tồn tại stream cùng tên. Bạn phải xóa stream hiện có trước khi phục hồi từ backup.

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **payload**: nội dung chính của message
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục