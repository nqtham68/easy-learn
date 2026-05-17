---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/running/windows_srv
title: Windows Service
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Windows Service

> 🇬🇧 *The NATS server supports running as a Windows service. In fact, this is the recommended way of running NATS on Windows. There is currently no installer; users should use `sc.exe` to install the service:*

NATS server hỗ trợ chạy dưới dạng Windows service. Đây là cách được khuyến nghị để chạy NATS trên Windows. Hiện chưa có bộ cài đặt sẵn; người dùng cần dùng `sc.exe` để cài service:

```shell
sc.exe create nats-server binPath= "%NATS_PATH%\nats-server.exe [nats-server flags]"
sc.exe start nats-server
```

> 🇬🇧 *The above will create and start a `nats-server` service. Note the nats-server flags should be provided when creating the service. This allows for the running multiple NATS server configurations on a single Windows server by using a 1:1 service instance per installed NATS server service. Once the service is running, it can be controlled using `sc.exe` or `nats-server.exe --signal`:*

Lệnh trên sẽ tạo và khởi động service `nats-server`. Lưu ý rằng các flag của nats-server cần được truyền vào lúc tạo service. Cách này cho phép chạy nhiều config (cấu hình) NATS khác nhau trên cùng một Windows server bằng cách tạo mỗi service instance tương ứng với một NATS server. Sau khi service đang chạy, có thể điều khiển nó qua `sc.exe` hoặc `nats-server.exe --signal`:

```shell
REM Reload server configuration
nats-server.exe --signal reload

REM Reopen log file for log rotation
nats-server.exe --signal reopen

REM Stop the server
nats-server.exe --signal stop
```

> 🇬🇧 *The above commands will default to controlling the `nats-server` service. If the service is another name, it can be specified:*

Các lệnh trên mặc định điều khiển service `nats-server`. Nếu service có tên khác, có thể chỉ định tên đó:

```shell
nats-server.exe --signal stop=<service name>
```

> 🇬🇧 *For a complete list of signals, see [process signaling](../nats_admin/signals.md).*

Để xem danh sách đầy đủ các signal, tham khảo [process signaling](../nats_admin/signals.md).

## Quyền truy cập

> 🇬🇧 *The default user in the above example will be `System`, which has local administrator permissions and write access to almost all files on disk.*

User mặc định trong ví dụ trên là `System`, vốn có permission (quyền truy cập) quản trị viên cục bộ và quyền ghi lên hầu hết các file trên ổ đĩa.

> 🇬🇧 *If you change the service user, e.g. to the more restricted `NetworkService`, make sure permissions have been set. The server at a minimum will need read access to the config file and when using Jetstream, write access to the JetStream store directory.*

Nếu đổi user của service, ví dụ sang `NetworkService` với quyền hạn chế hơn, cần đảm bảo đã thiết lập đủ permission. Tối thiểu, server cần quyền đọc file config và — khi dùng JetStream — quyền ghi vào thư mục lưu trữ của JetStream.

```shell
sc config "nats-server" obj= "NT AUTHORITY\NetworkService" password= ""
```

> 🇬🇧 *Nats-server will write log entries to the default console when no log file is configured. Console logging is not permitted for all users (e.g. not for NetworkService).*

Khi không cấu hình file log, nats-server sẽ ghi log ra console mặc định. Không phải mọi user đều được phép ghi log ra console (ví dụ: NetworkService thì không).

> **ℹ️ Info:**
> To ease debugging, it is recommended to run a NATS service with an explicit log file and carefully check write permissions for the configured user.

> **ℹ️ Ghi chú:**
> Để dễ debug hơn, nên chạy NATS service với một file log được chỉ định rõ ràng và kiểm tra kỹ quyền ghi cho user đã cấu hình.

```shell
sc.exe create nats-server binPath= "%NATS_PATH%\nats-server.exe --log C:\temp\nats-server.log [other flags]"
```

## Cài đặt đặc thù cho Windows Service

### Biến môi trường `NATS_STARTUP_DELAY`

> 🇬🇧 *The Windows service system requires communication with programs that run as Windows services. One important signal from the program is the initial "ready" signal, where the program informs Windows that it is running as expected.*

Hệ thống Windows service yêu cầu giao tiếp với các chương trình chạy dưới dạng Windows service. Một signal quan trọng từ chương trình là signal "ready" ban đầu, nơi chương trình thông báo cho Windows biết nó đang chạy bình thường.

> 🇬🇧 *By default `nats-server` allows itself up to 10 seconds to send this signal. If the server is not ready after this time, the server will signal a failure to start. This delay can be adjusted by setting the `NATS_STARTUP_DELAY` environment variable to a suitable duration (e.g. "20s" for 20 seconds, "1m" for one minute).*

Mặc định, `nats-server` cho phép bản thân tối đa 10 giây để gửi signal này. Nếu server chưa sẵn sàng sau khoảng thời gian đó, server sẽ báo lỗi khởi động. Có thể điều chỉnh thời gian này bằng cách đặt biến môi trường `NATS_STARTUP_DELAY` với giá trị phù hợp (ví dụ: "20s" cho 20 giây, "1m" cho một phút).

> 🇬🇧 ***Please Note***
> * For the environment variable `NATS_STARTUP_DELAY` to be accessible from the NATS service, it is recommended to set it as a SYSTEM variable.
> * `NATS_STARTUP_DELAY=30s` will make the NATS server wait **up to 30s**, but will report the service as RUNNING as soon as the server is ready to accept connections. To **test** the extended time startup timeout you may need to slow down server startup, e.g. by using a very large stream (10s of GB) or placing Jetstream storage on a slow network device.

**Lưu ý**
* Để biến môi trường `NATS_STARTUP_DELAY` có thể truy cập được từ NATS service, nên đặt nó là biến SYSTEM.
* `NATS_STARTUP_DELAY=30s` sẽ khiến NATS server chờ **tối đa 30 giây**, nhưng sẽ báo trạng thái service là RUNNING ngay khi server sẵn sàng chấp nhận kết nối. Để **kiểm thử** timeout khởi động mở rộng này, có thể cần làm chậm quá trình khởi động server, ví dụ bằng cách dùng một stream (luồng message lưu trữ liên tục) rất lớn (hàng chục GB) hoặc đặt storage của JetStream trên thiết bị mạng chậm.

> 🇬🇧 *This adjustment can be necessary in cases where NATS is correctly running from command line, but takes longer than 10s to recover JetStream stream state and connect to its cluster peers.*

Việc điều chỉnh này cần thiết trong các trường hợp NATS chạy đúng từ command line nhưng mất hơn 10 giây để khôi phục trạng thái stream của JetStream và kết nối với các node (một server trong cluster) trong cluster (cụm nhiều server chạy chung).

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **node**: một server trong cluster
- **permission**: quyền truy cập
- **server**: máy chủ
- **stream**: luồng message lưu trữ liên tục