---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/nats_admin/upgrading_cluster
title: Nâng cấp Cluster
translated: true
translated_at: '2026-05-17T00:00:00+00:00'
---

# Nâng cấp Cluster

> 🇬🇧 *Repeat this procedure for all nodes of the cluster, one at a time:*
> 1. *Stop the server by putting it into [Lame Duck Mode](./lame_duck_mode.md)*
> 2. *Replace the binary or Docker image with the new version.*
> 3. *Restart the server.*
> 4. *Wait until the `/healthz` endpoint returns `HTTP 200 OK` before moving on to the next cluster node.*

Lặp lại quy trình sau cho từng node (một server trong cluster) trong cluster (cụm nhiều server chạy chung), từng node một:
1. Dừng server bằng cách chuyển sang [Lame Duck Mode](./lame_duck_mode.md)
2. Thay thế binary (file chương trình đã biên dịch) hoặc Docker image bằng phiên bản mới.
3. Khởi động lại server.
4. Chờ đến khi endpoint (địa chỉ API cụ thể) `/healthz` trả về `HTTP 200 OK` trước khi chuyển sang node tiếp theo trong cluster.

### Hạ cấp (Downgrading)

> 🇬🇧 *Although the NATS server goes through rigorous testing for each release, there may be a need to revert to the previous version if you observe a performance regression for your workload. The support policy for the server is the current release as well as one patch version release prior. For example, if the latest is 2.8.4, a downgrade to 2.8.3 is supported. Downgrades to earlier versions may work, but is not recommended.*

Dù NATS server trải qua kiểm thử nghiêm ngặt cho mỗi bản phát hành, đôi khi vẫn cần phải quay lại phiên bản trước nếu bạn nhận thấy hiệu suất giảm với workload của mình. Chính sách hỗ trợ của server bao gồm bản release hiện tại và một bản patch liền trước. Ví dụ, nếu phiên bản mới nhất là 2.8.4 thì có thể hạ cấp xuống 2.8.3. Hạ cấp xuống các phiên bản cũ hơn có thể hoạt động nhưng không được khuyến nghị.

> 🇬🇧 *Fortunately, the downgrade path is the same as the upgrade path as noted above. Swap the binary and do a rolling restart.*

May mắn thay, quy trình hạ cấp giống hệt quy trình nâng cấp đã mô tả ở trên — thay thế binary và thực hiện rolling restart.

## Thuật ngữ trong bài

- **binary**: file chương trình đã biên dịch
- **cluster**: cụm nhiều server chạy chung
- **endpoint**: địa chỉ API cụ thể
- **node**: một server trong cluster
- **server**: máy chủ