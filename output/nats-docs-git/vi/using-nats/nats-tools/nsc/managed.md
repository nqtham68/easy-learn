---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/nats-tools/nsc/managed
title: Managed Operators
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Managed Operators

> 🇬🇧 *You can use `nsc` to administer multiple operators. Operators can be thought of as the owners of nats-servers, and fall into two categories: local and managed. The key difference is that managed operators are ones which you don't have the nkey for. An example of a managed operator is Synadia's [NGS](https://www.synadia.com/cloud?utm_source=nats_docs&utm_medium=nats).*

Bạn có thể dùng `nsc` để quản lý nhiều operator. Operator có thể hiểu là chủ sở hữu của các nats-server, và chia thành hai loại: local và managed. Điểm khác biệt chính là managed operator là operator mà bạn không có nkey của họ. Một ví dụ điển hình là [NGS](https://www.synadia.com/cloud?utm_source=nats_docs&utm_medium=nats) của Synadia.

> 🇬🇧 *Accounts, as represented by their JWTs, are signed by the operator. Some operators may use local copies of JWTs (i.e. using the memory resolver), but most should use the NATS account resolver built-in to 'nats-server' to manage their JWTs. Synadia uses a custom server for their JWTs that works similarly to the open-sourced account server.*

Account được đại diện bởi JWT và phải được operator ký. Một số operator dùng bản sao JWT cục bộ (tức là dùng memory resolver), nhưng hầu hết sẽ dùng NATS account resolver tích hợp sẵn trong `nats-server` để quản lý JWT. Synadia dùng một server (máy chủ) riêng cho JWT, hoạt động tương tự account server mã nguồn mở.

> 🇬🇧 *There are a few special commands when dealing with server based operators:*

Có một vài lệnh đặc biệt khi làm việc với server-based operator:

* Account JWT có thể được đẩy lên server bằng `nsc push`
* Account JWT có thể được kéo từ server xuống bằng `nsc pull`

> 🇬🇧 *For managed operators this push/pull behavior is built into `nsc`. Each time you edit your account JWT `nsc` will push the change to a managed operator's server and pull the signed response. If this fails the JWT on disk may not match the value on the server. You can always push or pull the account again without editing it. Note - push only works if the operator JWT was configured with an account server URL.*

Với managed operator, hành vi push/pull này đã được tích hợp vào `nsc`. Mỗi khi bạn chỉnh sửa account JWT, `nsc` sẽ push thay đổi lên server của managed operator và kéo về phản hồi đã ký. Nếu thao tác này thất bại, JWT trên đĩa có thể không khớp với giá trị trên server. Bạn có thể push hoặc pull lại account bất cứ lúc nào mà không cần chỉnh sửa. Lưu ý: push chỉ hoạt động nếu operator JWT đã được cấu hình với account server URL.

> 🇬🇧 *The managed operator will not only sign your account JWT with its key, but may also edit the JWT to include limits to constrain your access to their NATS servers. Some operators may also add demonstration or standard imports. Generally you can remove these, although the operator gets the final call on all Account edits. As with any deployment, the managed operator doesn't track user JWTs.*

Managed operator không chỉ ký account JWT của bạn bằng khóa của họ, mà còn có thể chỉnh sửa JWT để thêm các giới hạn nhằm kiểm soát quyền truy cập vào NATS server của họ. Một số operator cũng có thể thêm các import demo hoặc import tiêu chuẩn. Nhìn chung bạn có thể xóa những import này, nhưng operator có quyền quyết định cuối cùng đối với mọi chỉnh sửa Account. Như với bất kỳ deployment nào, managed operator không theo dõi user JWT.

> 🇬🇧 *To start using a managed operator you need to tell `nsc` about it. There are a couple ways to do this. First you can manually tell `nsc` to download the operator JWT using the `add operator` command:*

Để bắt đầu dùng một managed operator, bạn cần thông báo cho `nsc` biết về nó. Có một vài cách để thực hiện. Cách đầu tiên là thủ công báo cho `nsc` tải operator JWT xuống bằng lệnh `add operator`:

```bash
nsc add operator -i
```

> 🇬🇧 *The operator JWT (or details) should be provided to you by the operator. The second way to add a managed operator is with the `init` command:*

Operator JWT (hoặc thông tin chi tiết) sẽ do operator cung cấp cho bạn. Cách thứ hai để thêm managed operator là dùng lệnh `init`:

```bash
nsc init -o synadia -n MyFirstAccount
```

> 🇬🇧 *You can use the name of an existing operator, or a well known one \(currently only "synadia"\).*

Bạn có thể dùng tên của một operator hiện có, hoặc một operator đã được biết đến rộng rãi (hiện tại chỉ có "synadia").

> 🇬🇧 *Once you add a managed operator you can add accounts to it normally, with the caveat that new accounts are pushed and pulled as described above.*

Khi đã thêm managed operator, bạn có thể thêm account vào đó bình thường, với lưu ý là các account mới sẽ được push và pull như mô tả ở trên.

## Định nghĩa "Well Known Operators"

> 🇬🇧 *To define a well known operator, you would tell `nsc` about an operator that you want people in your environment to use by name with a simple environment variable of the form `nsc_<operator name>_operator` the value of this environment variable should be the URL for getting the operator JWT. For example:*

Để định nghĩa một well known operator, bạn thông báo cho `nsc` về một operator mà mọi người trong môi trường của bạn có thể dùng theo tên, thông qua một biến môi trường có dạng `nsc_<operator name>_operator`. Giá trị của biến môi trường này là URL để lấy operator JWT. Ví dụ:

```bash
export nsc_zoom_operator=https://account-server-host/jwt/v1/operator
```

> 🇬🇧 *will tell `nsc` that there is a well known operator named zoom with its JWT at `https://account-server-host/jwt/v1/operator`. With this definition you can now use the `-u` flag with the name "zoom" to add the operator to an `nsc` store directory.*

sẽ thông báo cho `nsc` biết có một well known operator tên là zoom với JWT tại `https://account-server-host/jwt/v1/operator`. Với định nghĩa này, bạn có thể dùng flag `-u` với tên "zoom" để thêm operator vào thư mục store của `nsc`.

> 🇬🇧 *The operator JWT should have its account JWT server property set to point to the appropriate URL. For our example this would be:*

Operator JWT cần có thuộc tính account JWT server được trỏ đến URL phù hợp. Trong ví dụ của chúng ta, đó là:

```bash
nsc edit operator -u https://account-server-host/jwt/v1
```

> 🇬🇧 *You can also set one or more service urls. These allow the `nsc tool` actions like pub and sub to work. For example:*

Bạn cũng có thể đặt một hoặc nhiều service (dịch vụ) URL. Những URL này cho phép các hành động của `nsc tool` như pub và sub hoạt động được. Ví dụ:

```bash
nsc edit operator -n nats://localhost:4222
nsc tool pub hello world
```

## Thuật ngữ trong bài

- **server**: máy chủ
- **service**: dịch vụ