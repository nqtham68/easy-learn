---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nsc/revocation
title: Thu hồi quyền truy cập (Revocation)
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Thu hồi quyền truy cập

> 🇬🇧 *NATS supports two types of revocations. Both of these are stored in the Account JWT, so that the nats-server can see the revocations and apply them.*

NATS hỗ trợ hai loại revocation. Cả hai đều được lưu trong Account JWT để nats-server có thể đọc và áp dụng chúng.

> 🇬🇧 *Users are revoked by public key and time. Access to an export, called an activation, can be revoked for a specific account at a specific time. The use of time here can be confusing, but is designed to support the primary uses of revocation.*

User bị thu hồi theo public key và thời gian. Quyền truy cập vào một export — gọi là activation — có thể bị thu hồi cho một account cụ thể tại một thời điểm cụ thể. Việc dùng thời gian ở đây có thể gây khó hiểu, nhưng cách thiết kế này nhằm hỗ trợ các trường hợp sử dụng revocation phổ biến nhất.

> 🇬🇧 *When a user or activation is revoked at time T, it means that any user JWT or activation token created before that time is invalid. If a new user JWT or new activation token is created after T it can be used. This allows an account owner to revoke a user and renew their access at the same time.*

Khi một user hoặc activation bị thu hồi tại thời điểm T, mọi user JWT hoặc activation token (chuỗi xác thực) được tạo trước thời điểm đó đều không hợp lệ. Nếu user JWT hoặc activation token mới được tạo sau T, chúng vẫn có thể sử dụng bình thường. Điều này cho phép chủ account thu hồi quyền của một user và cấp lại quyền mới cùng lúc.

> 🇬🇧 *Let's look at an example. Suppose you created a user JWT with access to the subject "billing". Later you decide you don't want that user to have access to "billing". Revoke the user, say at noon on May 1st 2019, and create a new user JWT without access to "billing". The user can no longer log in with the old JWT because it is revoked, but they can log in with the new JWT because it was created after noon May 1st 2019.*

Ví dụ: giả sử bạn tạo một user JWT cho phép truy cập vào subject (chuỗi định danh message) `"billing"`. Sau đó bạn muốn thu hồi quyền truy cập đó. Hãy revoke user này vào trưa ngày 1 tháng 5 năm 2019, rồi tạo user JWT mới không có quyền truy cập `"billing"`. User không thể đăng nhập bằng JWT cũ vì đã bị thu hồi, nhưng có thể đăng nhập bằng JWT mới vì nó được tạo sau thời điểm revocation.

> 🇬🇧 *`nsc` provides a number of commands to create, remove or list revocations:*

`nsc` cung cấp một số lệnh để tạo, xóa hoặc liệt kê các revocation:

```bash
nsc revocations -h
```
```text
Manage revocation for users and activations from an account

Usage:
  nsc revocations [command]

Available Commands:
  add-user          Revoke a user
  add_activation    Revoke an accounts access to an export
  delete-user       Remove a user revocation
  delete_activation Remove an account revocation from an export
  list-users        List users revoked in an account
  list_activations  List account revocations for an export

Flags:
  -h, --help   help for revocations

Global Flags:
  -i, --interactive          ask questions for various settings
  -K, --private-key string   private key

Use "nsc revocations [command] --help" for more information about a command.
```

> 🇬🇧 *Both add commands take the flag `--at` which defaults to 0, for now, which can be used to set the unix timestamp as described above. By default revocations are at the current time, but you can set them in the past for situations where you know when a problem occurred and was fixed.*

Cả hai lệnh `add` đều nhận flag `--at`, mặc định là `0` (tức là thời điểm hiện tại), cho phép đặt unix timestamp như mô tả ở trên. Theo mặc định, revocation áp dụng tại thời điểm hiện tại, nhưng bạn có thể đặt về quá khứ nếu biết chính xác thời điểm sự cố xảy ra và đã được khắc phục.

> 🇬🇧 *Deleting a revocation is permanent and can allow an old activation or user JWT to be valid again. Therefore delete should only be used if you are sure the tokens in question have expired.*

Xóa một revocation là vĩnh viễn và có thể khiến activation hoặc user JWT cũ trở nên hợp lệ trở lại. Vì vậy, chỉ dùng `delete` khi bạn chắc chắn rằng các token liên quan đã hết hạn.

## Đẩy thay đổi lên nats-server

> 🇬🇧 *If your nats servers are configured to use the built-in NATS resolver, remember that you need to 'push' any account changes you may have done (locally) using `nsc revocations` to the servers for those changes to take effect.*

Nếu nats-server được cấu hình dùng NATS resolver tích hợp sẵn, bạn cần 'push' mọi thay đổi account đã thực hiện cục bộ bằng `nsc revocations` lên server để các thay đổi có hiệu lực.

> 🇬🇧 *i.e. `nsc push -i` or `nsc push -a B -u nats://localhost`*

Ví dụ: `nsc push -i` hoặc `nsc push -a B -u nats://localhost`

> 🇬🇧 *If there are any clients currently connected with as a user that gets added to the revocations, their connections will be immediately terminated as soon as you 'push' your revocations to a nats server.*

Nếu có client nào đang kết nối với tư cách user bị thêm vào danh sách revocation, kết nối của họ sẽ bị ngắt ngay khi bạn 'push' revocation lên nats-server.

## Thuật ngữ trong bài

- **client**: bên gọi (phía người dùng)
- **server**: máy chủ
- **subject**: chuỗi định danh message (giống topic)
- **token**: chuỗi xác thực