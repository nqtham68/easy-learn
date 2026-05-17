---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/feature_comparison
title: So Sánh Tính Năng
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

## So Sánh Tính Năng NATS

> 🇬🇧 *This feature comparison is a summary of a few of the major components in several of the popular messaging technologies of today. This is by no means an exhaustive list and each technology should be investigated thoroughly to decide which will work best for your implementation.*

Bảng so sánh tính năng này tóm tắt một số thành phần chính của các công nghệ messaging phổ biến hiện nay. Đây không phải danh sách đầy đủ — mỗi công nghệ cần được nghiên cứu kỹ trước khi đưa vào triển khai thực tế.

> 🇬🇧 *This comparison features NATS, Apache Kafka, RabbitMQ, Apache Pulsar, and gRPC.*

Bảng so sánh bao gồm: NATS, Apache Kafka, RabbitMQ, Apache Pulsar và gRPC.


<table>
    <tr>
        <td rowspan="5" valign="top"><b>
            Hỗ trợ ngôn ngữ và nền tảng
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            Core NATS: 48 loại client được biết đến, 11 do maintainer hỗ trợ, 18 do cộng đồng đóng góp. NATS Streaming: 7 loại client do maintainer hỗ trợ, 4 do cộng đồng đóng góp. NATS server có thể biên dịch trên các kiến trúc mà Golang hỗ trợ. NATS cung cấp bản phân phối dạng binary.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            18 loại client được cộng đồng và Confluent hỗ trợ. Kafka server chạy trên nền tảng hỗ trợ Java — hỗ trợ rất rộng rãi.
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            Ít nhất 10 nền tảng client do maintainer hỗ trợ, cùng hơn 50 loại do cộng đồng đóng góp. Server chạy trên: Linux, Windows, NT.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            7 ngôn ngữ client, 5 client bên thứ ba — đã kiểm thử trên macOS và Linux.
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            13 ngôn ngữ client.
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            Pattern tích hợp sẵn
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            Stream (luồng message lưu trữ liên tục) và service thông qua publish/subscribe, request-reply và load balanced queue subscriber tích hợp sẵn. Hỗ trợ phân quyền request động và ẩn danh hóa subject của request.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            Stream thông qua publish/subscribe. Cân bằng tải có thể thực hiện qua consumer group. Application code phải tự ghép request với reply trên nhiều topic để tạo pattern service (request-reply).
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            Stream thông qua publish/subscribe, và service với tính năng direct reply-to. Cân bằng tải có thể thực hiện qua Work Queue. Application phải tự ghép request với reply trên nhiều topic để tạo pattern service (request-reply).
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            Stream thông qua publish/subscribe. Nhiều pattern competing consumer hỗ trợ cân bằng tải. Application code phải tự ghép request với reply trên nhiều topic để tạo pattern service (request-reply).
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            Một service trên mỗi channel, có thể sử dụng streaming. Cân bằng tải cho service có thể thực hiện ở phía client hoặc thông qua proxy.
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            Đảm bảo delivery
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            At most once, at least once và exactly once đều có sẵn trong JetStream.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            At least once, exactly once.
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            At most once, at least once.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            At most once, at least once và exactly once.
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            At most once.
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            Multi-tenancy và chia sẻ dữ liệu
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            NATS hỗ trợ multi-tenancy thực sự và bảo mật phi tập trung thông qua account, cho phép định nghĩa stream và service được chia sẻ.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            Không hỗ trợ multi-tenancy.
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            Multi-tenancy được hỗ trợ thông qua vhost; không hỗ trợ chia sẻ dữ liệu.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            Multi-tenancy được triển khai qua tenant; không hỗ trợ chia sẻ dữ liệu tích hợp sẵn giữa các tenant. Mỗi tenant có thể có scheme authentication và authorization riêng.
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            N/A
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            AuthN (Xác thực)
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            NATS hỗ trợ TLS, NATS credentials, NKEYS (NATS ED25519 keys), username/password hoặc token đơn giản.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            Hỗ trợ Kerberos và TLS. Hỗ trợ JAAS và một implementation authorizer sẵn có sử dụng ZooKeeper để lưu trữ thông tin kết nối và subject.
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            TLS, SASL, username/password và pluggable authorization.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            TLS Authentication, Athenz, Kerberos, JSON Web Token Authentication.
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            TLS, ALT, Token, channel và call credential, cùng cơ chế plug-in.
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            AuthZ (Phân quyền)
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            Giới hạn account bao gồm: số kết nối, kích thước message, số lượng import/export. Permission publish và subscribe ở cấp user, giới hạn kết nối, giới hạn địa chỉ CIDR và giới hạn theo thời gian trong ngày.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            Hỗ trợ JAAS và ACL cho nhiều loại tài nguyên Kafka bao gồm topic, cluster, group và các loại khác.
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            ACL kiểm soát permission cho các thao tác configure, write và read trên các tài nguyên như exchange, queue, transaction và các loại khác. Authentication có thể mở rộng qua plugin.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            Permission có thể cấp cho từng role cụ thể cho danh sách các thao tác như produce và consume.
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            Người dùng có thể cấu hình call credential để phân quyền chi tiết cho từng lời gọi riêng lẻ trên service.
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            Lưu trữ và bền vững hóa message
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            Hỗ trợ lưu trữ trên memory, file và database. Message có thể replay theo thời gian, số lượng hoặc sequence number, và hỗ trợ durable subscription. Với NATS streaming, script có thể lưu trữ các log segment cũ vào cold storage.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            Hỗ trợ lưu trữ dựa trên file. Message có thể replay bằng cách chỉ định offset, và hỗ trợ durable subscription. Hỗ trợ log compaction cũng như KSQL.
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            Hỗ trợ lưu trữ dựa trên file. RabbitMQ sử dụng ngữ nghĩa queue (thay vì log) nên không có tính năng replay message.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            Hỗ trợ tiered storage gồm file, Amazon S3 hoặc Google Cloud Storage (GCS). Pulsar có thể replay message từ vị trí cụ thể và hỗ trợ durable subscription. Hỗ trợ Pulsar SQL, topic compaction và Pulsar functions.
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            N/A
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            High Availability / Fault Tolerance
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            Core NATS hỗ trợ full mesh clustering (cụm nhiều server chạy chung) với tính năng tự phục hồi để đảm bảo tính sẵn sàng cao cho client. NATS streaming có warm failover backup server với hai chế độ (FT và full clustering). JetStream hỗ trợ scale ngang với tính năng mirroring tích hợp.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            Các thành viên cluster được replicate đầy đủ và điều phối qua Zookeeper.
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            Hỗ trợ clustering với replication dữ liệu đầy đủ qua federation plugin. Cluster yêu cầu mạng độ trễ thấp và hiếm khi bị phân vùng mạng.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            Pulsar hỗ trợ clustered broker với geo-replication.
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            N/A. gRPC phụ thuộc vào tài nguyên bên ngoài để đảm bảo HA/FT.
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            Triển khai
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            NATS server là một binary tĩnh nhỏ gọn, có thể triển khai từ các instance lớn trên cloud đến thiết bị hạn chế tài nguyên như Raspberry Pi.
NATS hỗ trợ kiến trúc Adaptive Edge cho phép triển khai linh hoạt quy mô lớn. Single server, leaf node, cluster và supercluster (cluster của các cluster) có thể kết hợp theo bất kỳ cách nào, phù hợp với cloud, on-premise, edge và IoT. Client không cần biết về topology và có thể kết nối với bất kỳ NATS server nào trong hệ thống.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            Kafka hỗ trợ clustering với mirroring tới các remote cluster ghép lỏng. Client bị gắn với partition được định nghĩa trong cluster. Kafka server yêu cầu JVM, 8 core, 64–128 GB RAM, từ hai đĩa SAS/SSD 8 TB trở lên và card mạng 10 Gig.<sup>1</sup>
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            RabbitMQ hỗ trợ cluster và lan truyền message giữa các cluster qua federation plugin. Client không cần biết về topology và có thể kết nối với bất kỳ cluster nào. Server yêu cầu Erlang VM và các dependency đi kèm.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            Pulsar hỗ trợ clustering và geo-replication tích hợp sẵn giữa các cluster. Client có thể kết nối với bất kỳ cluster nào có tenant và namespace được cấu hình phù hợp. Pulsar yêu cầu JVM và ít nhất 6 máy Linux hoặc VM: 3 chạy ZooKeeper, 3 chạy Pulsar broker và BookKeeper bookie.<sup>2</sup>
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            gRPC là point-to-point và không có server hay broker để triển khai hay quản lý, nhưng luôn cần thêm các thành phần bổ sung cho môi trường production.
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            Giám sát
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            NATS hỗ trợ export dữ liệu giám sát sang Prometheus và có dashboard Grafana để theo dõi và cấu hình cảnh báo. Có các công cụ giám sát phát triển như nats-top. Hỗ trợ cả mô hình side car và mô hình kết nối-và-xem đơn giản qua NATS surveyor.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            Kafka có nhiều công cụ và console quản lý bao gồm Confluent Control Center, Kafka, Kafka Web Console, Kafka Offset Monitor.
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            Công cụ CLI, hệ thống quản lý dựa trên plugin với dashboard và các công cụ bên thứ ba.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            Công cụ CLI, dashboard theo từng topic và các công cụ bên thứ ba.
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            Cần các thành phần bên ngoài như service mesh để giám sát gRPC.
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            Quản lý
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            NATS tách biệt vận hành khỏi bảo mật. Quản lý user và account trong hệ thống có thể phi tập trung và thực hiện qua CLI. Cấu hình server (thành phần mạng) được tách khỏi bảo mật bằng command line và file config, cho phép reload khi đang chạy.
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            Kafka có nhiều công cụ và console quản lý bao gồm Confluent Control Center, Kafka, Kafka Web Console, Kafka Offset Monitor.
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            Công cụ CLI, hệ thống quản lý dựa trên plugin với dashboard và các công cụ bên thứ ba.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            Công cụ CLI, dashboard theo từng topic và các công cụ bên thứ ba.
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            Cần các thành phần bên ngoài như service mesh để quản lý gRPC.
        </td>
    </tr>
    <tr>
        <td rowspan="5" valign="top"><b>
            Tích hợp
            </b>
        </td>
        <td><b>
            NATS
            </b>
        </td>
        <td>
            NATS hỗ trợ WebSockets, Kafka bridge, IBM MQ Bridge, Redis Connector, Apache Spark, Apache Flink, CoreOS, Elastic, Elasticsearch, Prometheus, Telegraf, Logrus, Fluent Bit, Fluentd, OpenFAAS, HTTP và MQTT (sắp ra mắt).
        </td>
    </tr>
    <tr>
        <td><b>
            Kafka
            </b>
        </td>
        <td>
            Kafka có hệ sinh thái tích hợp phong phú, bao gồm xử lý stream (Storm, Samza, Flink), Hadoop, database (JDBC, Oracle Golden Gate), Search và Query (ElasticSearch, Hive) cùng nhiều tích hợp logging và các loại khác.
        </td>
    </tr>
    <tr>
        <td><b>
            Rabbit
            </b>
        </td>
        <td>
            RabbitMQ có nhiều plugin, bao gồm các giao thức (MQTT, STOMP), WebSockets và nhiều plugin authorization/authentication.
        </td>
    </tr>
    <tr>
        <td><b>
            Pulsar
            </b>
        </td>
        <td>
            Pulsar có nhiều tích hợp, bao gồm ActiveMQ, Cassandra, Debezium, Flume, Elasticsearch, Kafka, Redis và các hệ thống khác.
        </td>
    </tr>
    <tr>
        <td><b>
            gRPC
            </b>
        </td>
        <td>
            Có một số tích hợp bên thứ ba bao gồm HTTP, JSON, Prometheus, Grift và các hệ thống khác.<sup>3</sup>
        </td>
    </tr>
    
</table>
<h3>Tài liệu tham khảo</h3>
<p><sup>1</sup> <a href="https://docs.cloudera.com/HDPDocuments/HDF3/HDF-3.1.0/bk_planning-your-deployment/content/ch_hardware-sizing.html#:~:text=Kafka%20Broker%20Node%3A%20eight%20cores,and%20a%2010%2D%20Gige%20Nic%20.&text=75%20MB%2Fsec%20per%20node,therefore%2010GB%20Nic%20is%20required%20"><a href="https://docs.cloudera.com/HDPDocuments/HDF3/HDF-3.1.0/bk_planning-your-deployment/content/ch_hardware-sizing.html#:~:text=Kafka%20Broker%20Node%3A%20eight%20cores,and%20a%2010%2D%20Gige%20Nic%20.&text=75%20MB%2Fsec%20per%20node,therefore%2010GB%20Nic%20is%20required%20">https://docs.cloudera.com/HDPDocuments/HDF3/HDF-3.1.0/bk_planning-your-deployment/content/ch_hardware-sizing.html#:~:text=Kafka%20Broker%20Node%3A%20eight%20cores,and%20a%2010%2D%20Gige%20Nic%20.&text=75%20MB%2Fsec%20per%20node,therefore%2010GB%20Nic%20is%20required%20</a></a></p>
<p><sup>2</sup> <a href="https://pulsar.apache.org/docs/v1.21.0-incubating/deployment/cluster/"><a href="https://pulsar.apache.org/docs/v1.21.0-incubating/deployment/cluster/">https://pulsar.apache.org/docs/v1.21.0-incubating/deployment/cluster/</a></a> </p>
<p><sup>3</sup> <a href="https://github.com/grpc-ecosystem"><a href="https://github.com/grpc-ecosystem">https://github.com/grpc-ecosystem</a></a></p>


## Thuật ngữ trong bài

- **broker**: trung gian truyền message
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **credential**: thông tin đăng nhập
- **permission**: quyền truy cập
- **queue**: hàng đợi message
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **token**: chuỗi xác thực
- **topic**: chủ đề phân loại message
- **WebSocket**: giao thức WebSocket