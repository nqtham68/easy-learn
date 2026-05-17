---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/release_notes/whats_new_20
title: NATS 2.0 - Tính năng mới
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# NATS 2.0

> 🇬🇧 *NATS 2.0 was the largest feature release since the original code base for the server was released. NATS 2.0 was created to allow a new way of thinking about NATS as a shared utility, solving problems at scale through distributed security, multi-tenancy, larger networks, and secure sharing of data.*

NATS 2.0 là bản phát hành tính năng lớn nhất kể từ khi server ra đời. NATS 2.0 được tạo ra để mang đến cách tư duy mới về NATS như một tiện ích dùng chung, giải quyết các vấn đề ở quy mô lớn thông qua bảo mật phân tán, multi-tenancy, mạng lưới rộng hơn và chia sẻ dữ liệu an toàn.

## Lý do ra đời

> 🇬🇧 *NATS 2.0 was created to address problems in large scale distributed computing.*

NATS 2.0 được tạo ra để giải quyết các vấn đề trong hệ thống tính toán phân tán quy mô lớn.

> 🇬🇧 *It is difficult at best to combine identity management end-to-end (or end-to-edge), with data sharing, while adhering to policy and compliance. Current distributed systems increase significantly in operational complexity as they scale upward. Problems arise around service discovery, connectivity, scaling for volume, and application onboarding and updates. Disaster recovery is difficult, especially as systems have evolved to operate in silos defined by technology rather than business needs. As complexity increases, systems become expensive to operate in terms of time and money. They become fragile making it difficult to deploy services and applications hindering innovation, increasing time to value and total cost of ownership.*

Việc kết hợp quản lý danh tính end-to-end (hoặc end-to-edge) với chia sẻ dữ liệu trong khi vẫn tuân thủ chính sách và quy định là điều rất khó. Các hệ thống phân tán hiện tại tăng đáng kể về độ phức tạp vận hành khi mở rộng quy mô. Các vấn đề nảy sinh xung quanh service discovery, kết nối, mở rộng theo lưu lượng, và việc onboarding cũng như cập nhật ứng dụng. Disaster recovery rất khó khăn, đặc biệt khi các hệ thống đã phát triển theo hướng hoạt động trong các silo do công nghệ định nghĩa thay vì nhu cầu kinh doanh. Khi độ phức tạp tăng lên, hệ thống trở nên tốn kém về thời gian và tiền bạc. Chúng trở nên dễ vỡ khiến việc deploy service và ứng dụng khó khăn hơn, cản trở đổi mới, kéo dài time-to-value và tăng tổng chi phí sở hữu.

> 🇬🇧 *We decided to:*
>
> *- **Reduce total cost of ownership**: Users want reduced TCO for their distributed systems. This is addressed by an easy to use technology that can operate at global scale with simple configuration and a resilient and cloud-native architecture.*
>
> *- **Decrease Time to Value**: As systems scale, time to value increases. Operations resist change due to risk in touching a complex and fragile system. Providing isolation contexts can help mitigate this.*
>
> *- **Support manageable large scale deployments**: No data silos defined by software, instead easily managed through software to provide exactly what the business needs. We wanted to provide easy to configure disaster recovery.*
>
> *- **Decentralize security**: Provide security supporting one technology end-to-end where organizations may self-manage making it easier to support a massive number of endpoints.*

Chúng tôi đã quyết định:

* **Giảm tổng chi phí sở hữu**: Người dùng muốn giảm TCO cho các hệ thống phân tán. Điều này được giải quyết bằng một công nghệ dễ sử dụng, có thể hoạt động ở quy mô toàn cầu với cấu hình đơn giản và kiến trúc cloud-native linh hoạt.

* **Giảm Time to Value**: Khi hệ thống mở rộng, time-to-value tăng theo. Đội vận hành ngại thay đổi vì rủi ro khi can thiệp vào hệ thống phức tạp và dễ vỡ. Cung cấp các isolation context có thể giúp giảm thiểu điều này.

* **Hỗ trợ triển khai quy mô lớn dễ quản lý**: Không có data silo do phần mềm định nghĩa; thay vào đó, được quản lý dễ dàng qua phần mềm để đáp ứng đúng nhu cầu kinh doanh. Chúng tôi muốn cung cấp disaster recovery dễ cấu hình.

* **Phân tán bảo mật**: Cung cấp bảo mật hỗ trợ một công nghệ end-to-end, nơi các tổ chức có thể tự quản lý, giúp dễ dàng hỗ trợ số lượng lớn endpoint.

> 🇬🇧 *To achieve this, we added a number of new features that are transparent to existing clients with 100% backward client compatibility.*

Để đạt được điều này, chúng tôi đã thêm nhiều tính năng mới hoàn toàn trong suốt với các client hiện có, đảm bảo 100% tương thích ngược.

## Accounts

> 🇬🇧 *Accounts are securely isolated communication contexts that allow multi-tenancy spanning a NATS deployment. Accounts allow users to bifurcate technology from business driven use cases, where data silos are created by design, not software limitations. When a client connects, it specifies an account or will default to authentication with a global account.*

Account là các ngữ cảnh giao tiếp được cách ly bảo mật, cho phép multi-tenancy trên toàn bộ NATS deployment. Account giúp tách biệt công nghệ khỏi các trường hợp sử dụng theo hướng kinh doanh, nơi các data silo được tạo ra theo thiết kế, không phải do giới hạn phần mềm. Khi client kết nối, nó chỉ định một account hoặc mặc định xác thực với global account.

> 🇬🇧 *At least some services need to share data outside of their account. Data can be securely shared between accounts with secure services and streams. Only mutual agreement between account owners permit data flow, and the import account has complete control over its own subject space.*

Ít nhất một số service cần chia sẻ dữ liệu ra ngoài account của chúng. Dữ liệu có thể được chia sẻ an toàn giữa các account thông qua service và stream (luồng message lưu trữ liên tục) an toàn. Chỉ khi cả hai bên chủ account đồng ý thì luồng dữ liệu mới được cho phép, và account nhập có toàn quyền kiểm soát không gian subject (chuỗi định danh message) của mình.

> 🇬🇧 *This means within an account, limitations may be set and subjects can be used without worry of collisions with other groups or organizations. Development groups choose any subjects without affecting the rest of the system, and open up accounts to export or import only the services and streams they need.*

Nghĩa là trong một account, có thể đặt giới hạn và sử dụng subject mà không lo va chạm với các nhóm hay tổ chức khác. Các nhóm phát triển tự do chọn bất kỳ subject nào mà không ảnh hưởng đến phần còn lại của hệ thống, và mở account để export hoặc import chỉ những service và stream họ cần.

> 🇬🇧 *Accounts are easy, secure, and cost effective. There is one NATS deployment to manage, but organizations and development teams can self manage with more autonomy reducing time to value with faster, more agile development practices.*

Account dễ sử dụng, an toàn và tiết kiệm chi phí. Chỉ có một NATS deployment để quản lý, nhưng các tổ chức và nhóm phát triển có thể tự quản lý với nhiều quyền tự chủ hơn, giảm time-to-value với quy trình phát triển nhanh và linh hoạt hơn.

### Service và Streams

> 🇬🇧 *Services and streams are mechanisms to share messages between accounts.*

Service và stream là các cơ chế chia sẻ message giữa các account.

> 🇬🇧 *Think of a service as an RPC endpoint into an account. Behind that account there might be many microservices working in concert to handle requests, but from outside the account there is simply one subject exposed.*

Hãy coi service như một RPC endpoint vào một account. Phía sau account đó có thể có nhiều microservice phối hợp để xử lý request, nhưng từ bên ngoài account chỉ có một subject duy nhất được expose.

> 🇬🇧 ***Service** definitions share an endpoint:*
>
> *- Export a service to allow other accounts to import*
>
> *- Import a service to allow requests to be sent securely and seamlessly to another account*
>
> *Use cases include most applications - anything that accepts a request and returns a response.*

Định nghĩa **Service** chia sẻ một endpoint:

* Export một service để cho phép các account khác import
* Import một service để cho phép request được gửi an toàn và liền mạch đến account khác

Các trường hợp sử dụng bao gồm hầu hết ứng dụng — bất cứ thứ gì chấp nhận request và trả về response.

> 🇬🇧 ***Stream** definitions allow continuous data flow between accounts:*
>
> *- Export a stream to allow egress*
>
> *- Import a stream to allow ingress*
>
> *Use cases include Observability, Metrics, and Data analytics. Any application or endpoint reading a stream of data.*

Định nghĩa **Stream** cho phép luồng dữ liệu liên tục giữa các account:

* Export một stream để cho phép data đi ra ngoài
* Import một stream để cho phép data đi vào trong

Các trường hợp sử dụng bao gồm Observability, Metrics và Data analytics — bất kỳ ứng dụng hay endpoint nào đọc một stream dữ liệu.

> 🇬🇧 *Note that services and streams operate with **zero** client configuration or API changes. Services may even move between accounts, entirely transparent to end clients.*

Lưu ý rằng service và stream hoạt động mà **không cần** thay đổi cấu hình client hay API. Service thậm chí có thể di chuyển giữa các account, hoàn toàn trong suốt với end client.

### System Accounts

> 🇬🇧 *The system account publishes system messages under established subject patterns. These are internal NATS system messages that may be useful to operators.*

System account publish các system message theo các pattern subject đã định sẵn. Đây là các system message nội bộ của NATS có thể hữu ích cho operator.

> 🇬🇧 *Server initiated events and data include:*
>
> *- Client connection events*
>
> *- Account connection status*
>
> *- Authentication errors*
>
> *- Leaf node connection events*
>
> *- Server stats summary*

Các event và dữ liệu do server khởi tạo bao gồm:

* Sự kiện kết nối client
* Trạng thái kết nối account
* Lỗi xác thực
* Sự kiện kết nối leaf node
* Tóm tắt thống kê server

> 🇬🇧 *Tools and clients with proper privileges can request:*
>
> *- Service statistics*
>
> *- Server discovery and metrics*

Các tool và client có đặc quyền phù hợp có thể yêu cầu:

* Thống kê service
* Server discovery và metric

> 🇬🇧 *Account servers will also publish messages when an account changes.*

Account server cũng sẽ publish message khi một account thay đổi.

> 🇬🇧 *With this information and system metadata you can build useful monitoring and anomaly detection tools.*

Với thông tin và system metadata này, bạn có thể xây dựng các công cụ monitoring và phát hiện bất thường hữu ích.

## Triển khai toàn cầu

> 🇬🇧 *NATS 2.0 supports global deployments, allowing for global topologies that optimize for WANs while extend to the edge or devices.*

NATS 2.0 hỗ trợ deploy toàn cầu, cho phép các topology toàn cầu tối ưu cho WAN trong khi vẫn mở rộng đến edge hoặc thiết bị.

### Tự phục hồi

> 🇬🇧 *While self healing features have been part of NATS 1.X releases, we ensured they continue to work in global deployments. These include:*
>
> *- Client and server connections automatically reconnect*
>
> *- Auto-Discovery where servers exchange server topology changes with each other and with clients, in real time with zero configuration changes and zero downtime while being entirely transparent to clients. Clients can failover to servers they were not originally configured with.*
>
> *- NATS server clusters dynamically adjust to new or removed servers allowing for seamless rolling upgrades and scaling up or down.*

Mặc dù các tính năng tự phục hồi đã có trong các bản phát hành NATS 1.X, chúng tôi đảm bảo chúng tiếp tục hoạt động trong các deployment toàn cầu. Bao gồm:

* Kết nối client và server tự động kết nối lại
* Auto-Discovery, nơi các server trao đổi thay đổi topology với nhau và với client theo thời gian thực mà không cần thay đổi cấu hình, không có downtime, hoàn toàn trong suốt với client. Client có thể failover sang các server không có trong cấu hình ban đầu.
* Các cluster NATS server tự động điều chỉnh khi có server mới hoặc bị xóa, cho phép rolling upgrade liền mạch và mở rộng/thu hẹp quy mô.

### Superclusters

> 🇬🇧 *Conceptually, superclusters are clusters of NATS clusters. Create superclusters to deploy a truly global NATS network. Superclusters use a novel spline based technology with a unique approach to topology, keeping one hop semantics and optimizing WAN traffic through optimistic sends with interest graph pruning. Superclusters provide transparent, intelligent support for geo-distributed queue subscribers.*

Về mặt khái niệm, supercluster là cluster của các NATS cluster. Tạo supercluster để deploy một mạng NATS thực sự toàn cầu. Supercluster sử dụng công nghệ dựa trên spline mới lạ với cách tiếp cận topology độc đáo, duy trì ngữ nghĩa một hop và tối ưu lưu lượng WAN thông qua optimistic send kết hợp với interest graph pruning. Supercluster cung cấp hỗ trợ thông minh, trong suốt cho các queue subscriber (bên đăng ký nhận message) phân tán theo địa lý.

### Disaster Recovery

> 🇬🇧 *Superclusters inherently support disaster recovery. With geo-distributed queue subscribers, local clients are preferred, then an RTT is used to find the lowest latency NATS cluster containing a matching queue subscriber in the supercluster.*

Supercluster về bản chất đã hỗ trợ disaster recovery. Với các queue subscriber phân tán theo địa lý, client cục bộ được ưu tiên trước, sau đó RTT được dùng để tìm NATS cluster có độ trễ thấp nhất chứa queue subscriber phù hợp trong supercluster.

> 🇬🇧 *What does this mean?*

Điều này có nghĩa là gì?

> 🇬🇧 *Let's say you have a set of load balanced services in US East Coast (US-EAST), another set in the EU (EU-WEST), and a supercluster consisting of a NATS cluster in US-EAST connected to a NATS cluster in EU-WEST. Clients in the US would connect to a US-EAST, and services connected to that cluster would service those clients. Clients in Europe would automatically use services connected to EU-WEST. If the services in US-EAST disconnect, clients in US-EAST will begin using services in EU-WEST.*

Giả sử bạn có một tập hợp service cân bằng tải ở bờ Đông nước Mỹ (US-EAST), một tập khác ở EU (EU-WEST), và một supercluster gồm NATS cluster ở US-EAST kết nối với NATS cluster ở EU-WEST. Client ở Mỹ sẽ kết nối với US-EAST, và các service kết nối với cluster đó sẽ phục vụ các client này. Client ở châu Âu sẽ tự động sử dụng service kết nối với EU-WEST. Nếu service ở US-EAST ngắt kết nối, client ở US-EAST sẽ bắt đầu sử dụng service ở EU-WEST.

> 🇬🇧 *Once the Eastern US services have reconnected to US-EAST, those services will immediately begin servicing the Eastern US clients since they're local to the NATS cluster. This is automatic and entirely transparent to the client. There is no extra configuration in NATS servers.*

Khi service ở Đông Mỹ kết nối lại với US-EAST, các service đó sẽ ngay lập tức phục vụ lại các client Đông Mỹ vì chúng cục bộ với NATS cluster. Điều này hoàn toàn tự động và trong suốt với client, không cần cấu hình thêm trên NATS server.

> 🇬🇧 *This is **zero configuration disaster recovery**.*

Đây là **disaster recovery không cần cấu hình**.

### Leaf Nodes

> 🇬🇧 *Leaf nodes are NATS servers running in a special configuration, allowing hub and spoke topologies to extend superclusters.*

Leaf node là các NATS server chạy trong cấu hình đặc biệt, cho phép topology hub-and-spoke mở rộng supercluster.

> 🇬🇧 *Leaf nodes can also bridge separate security domains. e.g. IoT, mobile, web. They are ideal for edge computing, IoT hubs, or data centers that need to be connected to a global NATS deployment. Local applications that communicate using the loopback interface with physical VM or Container security can leverage leaf nodes as well.*

Leaf node cũng có thể kết nối các security domain riêng biệt, ví dụ: IoT, mobile, web. Chúng lý tưởng cho edge computing, IoT hub, hoặc data center cần kết nối với một NATS deployment toàn cầu. Các ứng dụng cục bộ giao tiếp qua loopback interface với bảo mật VM hoặc Container vật lý cũng có thể tận dụng leaf node.

> 🇬🇧 *Leaf nodes:*
>
> *- Transparently and securely bind to a remote NATS account*
>
> *- Securely bridge specific local data to a wider NATS deployment*
>
> *- Are 100% transparent to clients which remain simple, lightweight, and easy to develop*
>
> *- Allow for a local security scheme while using new NATS security features globally*
>
> *- Can create a DMZ between a local NATS deployment and external NATS cluster or supercluster.*

Leaf node:

* Liên kết trong suốt và an toàn với một NATS account từ xa
* Kết nối an toàn dữ liệu cục bộ cụ thể với một NATS deployment rộng hơn
* Hoàn toàn trong suốt với client, giữ cho client đơn giản, nhẹ và dễ phát triển
* Cho phép sử dụng security scheme cục bộ trong khi vẫn dùng tính năng bảo mật NATS mới ở cấp toàn cầu
* Có thể tạo DMZ giữa NATS deployment cục bộ và NATS cluster hoặc supercluster bên ngoài

## Bảo mật phân tán

### Operators, Accounts và Users

> 🇬🇧 *NATS 2.0 Security consists of defining Operators, Accounts, and Users within a NATS deployment.*
>
> *- An **Operator** provides the root of trust for the system, may represent a company or enterprise*
>
>   *- Creates **Accounts** for account administrators. An account represents an organization, business unit, or service offering with a secure context within the NATS deployment, for example an IT system monitoring group, a set of microservices, or a regional IoT deployment. Account creation would likely be managed by a central group.*
>
> *- **Accounts** define limits and may securely expose services and streams.*
>
>   *- Account managers create **Users** with permissions*
>
> *- **Users** have specific credentials and permissions.*

Bảo mật NATS 2.0 bao gồm việc định nghĩa Operator, Account và User trong một NATS deployment.

* Một **Operator** cung cấp root of trust cho hệ thống, có thể đại diện cho một công ty hoặc doanh nghiệp
  * Tạo **Account** cho quản trị viên account. Một account đại diện cho một tổ chức, đơn vị kinh doanh, hoặc dịch vụ với ngữ cảnh bảo mật trong NATS deployment, ví dụ nhóm giám sát hệ thống IT, một tập hợp microservice, hoặc một IoT deployment theo khu vực. Việc tạo account thường được quản lý bởi một nhóm trung tâm.
* **Account** định nghĩa giới hạn và có thể expose service và stream một cách an toàn.
  * Account manager tạo **User** kèm permission (quyền truy cập)
* **User** có credential (thông tin đăng nhập) và permission cụ thể.

### Chuỗi tin cậy

> 🇬🇧 *PKI (NKeys encoded Ed25519) and signed JWTs create a hierarchy of Operators, Accounts, and Users creating a scalable and flexible distributed security mechanism.*
>
> *- **Operators** are represented by a self signed JWT and is the only thing that is required to be configured in the server. This JWT is usually signed by a master key that is kept offline. The JWT will contain valid signing keys that can be revoked with the master updating this JWT.*
>
>   *- Operators will sign **Account** JWTs with various signing keys.*
>
>   *- **Accounts** sign **User** JWTs, again with various signing keys.*
>
> *- Clients or leaf nodes present **User** credentials and a signed nonce when connecting.*
>
>   *- The server uses resolvers to obtain JWTs and verify the client trust chain.*
>
> *This allows for rapid change of permissions, authentication and limits, to a secure multi-tenant NATS system.*

PKI (NKeys mã hóa Ed25519) và JWT đã ký tạo ra một phân cấp Operator, Account và User, hình thành cơ chế bảo mật phân tán có khả năng mở rộng và linh hoạt.

* **Operator** được đại diện bởi một JWT tự ký và là thứ duy nhất cần được cấu hình trên server. JWT này thường được ký bằng master key được giữ offline. JWT sẽ chứa các signing key hợp lệ có thể bị thu hồi khi master cập nhật JWT này.
  * Operator sẽ ký **Account** JWT bằng các signing key khác nhau.
  * **Account** ký **User** JWT, cũng với các signing key khác nhau.
* Client hoặc leaf node trình bày **User** credential và một nonce đã ký khi kết nối.
  * Server sử dụng resolver để lấy JWT và xác minh chuỗi tin cậy của client.

Điều này cho phép thay đổi nhanh permission, xác thực và giới hạn trong một hệ thống NATS multi-tenant bảo mật.

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **cluster**: cụm nhiều server chạy chung
- **credential**: thông tin đăng nhập
- **deploy**: triển khai
- **endpoint**: địa chỉ API cụ thể
- **metric**: số liệu đo lường
- **node**: một server trong cluster
- **permission**: quyền truy cập
- **queue subscriber**: bên đăng ký nhận message (trong nhóm queue)
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **token**: chuỗi xác thực