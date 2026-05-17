---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/nats-concepts/subject_mapping
title: Subject Mapping và Transforms
translated: true
translated_at: '2026-05-13T00:00:00Z'
---

# Subject Mapping và Transforms

> 🇬🇧 *Subject mapping and transforms is a powerful feature of the NATS server. Transformations (we will use mapping and transform interchangeably) apply to various situations when messages are generated and ingested, acting as translations and in some scenarios as filters.*

Subject mapping và transforms là một tính năng mạnh mẽ của NATS server. Transform (chúng ta sẽ dùng "mapping" và "transform" thay thế cho nhau) áp dụng trong nhiều tình huống khi message (gói dữ liệu được gửi đi) được tạo ra và nhận vào, đóng vai trò như các bản dịch và trong một số trường hợp như các bộ lọc.

> **⚠️ Cảnh báo:**
> Mapping và transforms là chủ đề nâng cao. Trước khi tiếp tục, hãy đảm bảo bạn hiểu các khái niệm NATS như cluster, account và stream.

> 🇬🇧 *Transforms can be defined (for details see below):*

**Có thể định nghĩa transform (chi tiết xem bên dưới):**
* Ở root của file config (áp dụng cho account $G mặc định). Áp dụng cho tất cả message khớp, đi vào account này qua kết nối client hoặc leaf node. Các subject không khớp sẽ không bị thay đổi.
* Ở cấp account riêng lẻ, theo quy tắc tương tự như trên.
* Trên các subject được import vào một account.
* Trong ngữ cảnh [JetStream](#subject-mapping-and-transforms-in-streams):
    * Trên message được import bởi stream (luồng message lưu trữ liên tục)
    * Trên message được republish bởi JetStream
    * Trên message được sao chép vào stream qua source hoặc mirror. Trong trường hợp này, transform đóng vai trò như bộ lọc.

> 🇬🇧 *Transforms may be used for:*

**Transform có thể dùng để:**
* Dịch giữa các namespace. Ví dụ: khi mapping giữa các account, hoặc khi cluster và leaf node triển khai ngữ nghĩa khác nhau cho cùng một subject (chuỗi định danh message).
* Loại bỏ (suppress) subject. Ví dụ: tạm thời để kiểm thử.
* Đảm bảo tương thích ngược sau khi thay đổi cấu trúc đặt tên subject.
* Gộp nhiều subject lại với nhau.
* [Phân tách và cô lập trên super-cluster hoặc leaf node](#cluster-scoped-mappings), bằng cách dùng transform khác nhau ở từng cluster và leaf node.
* Kiểm thử. Ví dụ: gộp tạm thời một subject thử nghiệm vào subject sản xuất, hoặc chuyển hướng subject sản xuất khỏi consumer sản xuất.
* [Phân vùng (partition) subject](#deterministic-subject-token-partitioning) và JetStream stream.
* [Lọc](#subject-mapping-and-transforms-in-streams) message được sao chép (sourced/mirrored) vào JetStream stream.
* [Chaos testing và sampling. Mapping có thể được gán trọng số (weighted)](#weighted-mappings). Cho phép một tỷ lệ phần trăm nhất định của message bị chuyển hướng, mô phỏng mất gói, lỗi, v.v.
* ...

> 🇬🇧 *Priority and sequence of operations*

**Thứ tự ưu tiên và trình tự xử lý**

> 🇬🇧 *Transforms are applied as soon as a message enters the scope in which the transform was defined (cluster, account, leaf node, stream) and independent of how they arrived (publish by client, passing through gateway, stream import, stream source/mirror). And before any routing or subscription interest is applied. The message will appear as if published from the transformed subject under all circumstances.*

Transform được áp dụng ngay khi message đi vào scope (phạm vi quyền) mà transform được định nghĩa (cluster, account, leaf node, stream), bất kể cách message đến (publish từ client, đi qua gateway, stream import, stream source/mirror). Và trước khi bất kỳ routing hay subscription interest nào được áp dụng. Message sẽ xuất hiện như thể được publish từ subject đã được transform trong mọi trường hợp.

> 🇬🇧 *Transforms are **not applied recursively** in the same scope. This is necessary to prevent trivial loops. In the example below only the first matching rule is applied.*

Transform **không được áp dụng đệ quy** trong cùng một scope. Điều này cần thiết để ngăn chặn các vòng lặp đơn giản. Trong ví dụ dưới đây, chỉ quy tắc khớp đầu tiên được áp dụng.

```shell
mappings: {
	transform.order target.order
	target.order transform.order
}
```

> 🇬🇧 *Transforms are **applied in sequence** as they pass through different scopes. For example:*

Transform **được áp dụng tuần tự** khi đi qua các scope khác nhau. Ví dụ:
1. Một subject được transform khi được publish
2. Được route đến leaf node và transform khi đến leaf node
3. Import vào stream và lưu trữ dưới tên đã được transform
4. Republish từ stream sang Core NATS dưới subject đích cuối cùng

On a central cluster:
```
server_name: "hub"
cluster: { name: "hub" }
mappings: {
	orders.* orders.central.{{wildcard(1)}}
}
```
OR
```
server_name: "hub"
cluster: { name: "hub" }
mappings: {
	orders.> orders.central.>}
}
```

On a leaf cluster    
```
server_name: "store1"
cluster: { name: "store1" }
mappings: {
	orders.central.* orders.local.{{wildcard(1)}}
}
```

A stream config on the leaf cluster   
```
{
  "name": "orders",
  "subjects": [ "orders.local.*"],
  "subject_transform":{"src":"orders.local.*","dest":"orders.{{wildcard(1)}}"},
  "retention": "limits",
  ...
  "republish": {
    "src": "orders.*",
    "dest": "orders.trace.{{wildcard(1)}}"
  },
```

> 🇬🇧 *When using **config file-based account management** (not using JWT security), you can define the core NATS account level subject transforms in server configuration files, and simply need to reload the configuration whenever you change a transform for the change to take effect.*

**Bảo mật**

Khi dùng **quản lý account dựa trên file config** (không dùng JWT security), bạn có thể định nghĩa subject transform ở cấp account Core NATS trong file config của server, và chỉ cần reload config khi thay đổi transform để áp dụng hiệu quả.

> 🇬🇧 *When using **operator JWT security** (distributed security) with the built-in resolver you define the transforms and the import/exports in the account JWT, so after modifying them, they will take effect as soon as you push the updated account JWT to the servers.*

Khi dùng **operator JWT security** (bảo mật phân tán) với resolver tích hợp sẵn, bạn định nghĩa transform và import/export trong account JWT. Sau khi sửa đổi, chúng sẽ có hiệu lực ngay khi bạn push account JWT đã cập nhật lên server.

**Kiểm thử và debug**

> **ℹ️ Thông tin:**
> Bạn có thể dễ dàng kiểm thử từng quy tắc subject transform bằng lệnh `nats server mapping` của CLI tool [`nats`](https://docs.nats.io/using-nats/nats-tools/nats\_cli). Xem ví dụ bên dưới.

> 🇬🇧 *From NATS server 2.11 (and NATS versions published thereafter) the handling of subjects, including mappings can be observed with `nats trace`*

Từ NATS server 2.11 (và các phiên bản NATS được phát hành sau đó), việc xử lý subject — bao gồm cả mapping — có thể được quan sát với `nats trace`.

> 🇬🇧 *In the example below a message is first disambiguated from `orders.device1.order1` -> `orders.hub.device1.order1`. Then imported into a stream and stored under its original name.*

Trong ví dụ dưới đây, message đầu tiên được phân tách (disambiguated) từ `orders.device1.order1` -> `orders.hub.device1.order1`. Sau đó được import vào stream và lưu trữ dưới tên gốc.

```shell
nats trace orders.device1.order1

Tracing message route to subject orders.device1.order1

Client "NATS CLI Version development" cid:16 cluster:"hub" server:"hub" version:"2.11.0-dev"
    Mapping subject:"orders.hub.device1.order1"
--J JetStream action:"stored" stream:"orders" subject:"orders.device1.order1"
--X No active interest

Legend: Client: --C Router: --> Gateway: ==> Leafnode: ~~> JetStream: --J Error: --X

Egress Count:

  JetStream: 1
````

## Simple mappings (Mapping đơn giản)

> 🇬🇧 *The example of `foo:bar` is straightforward. All messages the server receives on subject `foo` are remapped and can be received by clients subscribed to `bar`.*

Ví dụ với `foo:bar` rất đơn giản. Tất cả message mà server nhận trên subject `foo` sẽ được remap, và client đăng ký trên `bar` có thể nhận chúng.

```
nats server mapping foo bar foo
> bar
```

> 🇬🇧 *When no subject is provided the command will operate in interactive mode:*

Khi không cung cấp subject, lệnh sẽ hoạt động ở chế độ tương tác:

```
nats server mapping foo bar
> Enter subjects to test, empty subject terminates.
>
> ? Subject foo
> bar

> ? Subject test
> Error: no matching transforms available
```

> 🇬🇧 *Example server config. Note that the mappings below apply only to the default $G account.*

Ví dụ về config server. Lưu ý rằng các mapping bên dưới chỉ áp dụng cho account $G mặc định.

```
server_name: "hub"
cluster: { name: "hub" }
mappings: {
    orders.flush  orders.central.flush 
	orders.* orders.central.{{wildcard(1)}}
}
```

> 🇬🇧 *Mapping a full wildcard*

Mapping một full wildcard

```
server_name: "hub"
cluster: { name: "hub" }
mappings: {
    orders.>  orders.central.> 
}
```

> 🇬🇧 *With accounts. While this mapping applies to a specific account.*

Với account: trong khi mapping này áp dụng cho một account cụ thể.

```
server_name: "hub"
cluster: { name: "hub" }

accounts {
    accountA: { 
        mappings: {
            orders.flush  orders.central.flush 
        	orders.* orders.central.{{wildcard(1)}}
        }
    }
}
```

## Mapping full wildcard '>'

> 🇬🇧 *A full wildcard token can be used ONCE in source expression and must be present on the destination expression as well exactly once.*

Full wildcard token chỉ có thể dùng MỘT LẦN trong biểu thức source và phải xuất hiện đúng một lần trong biểu thức đích.

> 🇬🇧 *Example: Prefixing a subject:*

Ví dụ: Thêm prefix vào subject:

```
nats server mapping ">"  "baz.>" bar.a.b
> baz.bar.b.a
```

## Sắp xếp lại token của subject

> 🇬🇧 *Wildcard tokens may be referenced by position number in the destination mapping using (only for versions 2.8.0 and above of `nats-server`). Syntax: `{{wildcard(position)}}`. E.g. `{{wildcard(1)}}` references the first wildcard token, `{{wildcard(2)}}` references the second wildcard token, etc..*

Wildcard token có thể được tham chiếu theo số thứ tự vị trí trong destination mapping (chỉ áp dụng cho phiên bản 2.8.0 trở lên của `nats-server`). Cú pháp: `{{wildcard(position)}}`. Ví dụ: `{{wildcard(1)}}` tham chiếu đến wildcard token đầu tiên, `{{wildcard(2)}}` tham chiếu đến wildcard token thứ hai, v.v.

> 🇬🇧 *Example: with this transform `"bar.*.*" : "baz.{{wildcard(2)}}.{{wildcard(1)}}"`, messages that were originally published to `bar.a.b` are remapped in the server to `baz.b.a`. Messages arriving at the server on `bar.one.two` would be mapped to `baz.two.one`, and so forth. Try it for yourself using `nats server mapping`.*

Ví dụ: với transform `"bar.*.*" : "baz.{{wildcard(2)}}.{{wildcard(1)}}"`, message được publish lên `bar.a.b` sẽ được remap trong server thành `baz.b.a`. Message đến server trên `bar.one.two` sẽ được map thành `baz.two.one`, và cứ tiếp tục như vậy. Tự thử bằng cách dùng `nats server mapping`.

```
nats server mapping "bar.*.*"  "baz.{{wildcard(2)}}.{{wildcard(1)}}" bar.a.b
> baz.b.a
```

> **ℹ️ Thông tin:**
> Cú pháp mapping cũ đã bị deprecated dùng `$1`.`$2` thay cho `{{wildcard(1)}}.{{wildcard(2)}}` có thể thấy trong một số ví dụ khác.

## Bỏ token khỏi subject

> 🇬🇧 *You can drop tokens from the subject by not using all the wildcard tokens in the destination transform, with the exception of mappings defined as part of import/export between accounts in which case _all_ the wildcard tokens must be used in the transform destination.*

Bạn có thể bỏ token khỏi subject bằng cách không dùng hết tất cả wildcard token trong destination transform, ngoại trừ các mapping được định nghĩa trong import/export giữa các account — trong trường hợp đó _tất cả_ wildcard token đều phải được dùng trong transform đích.

```
nats server mapping "orders.*.*" "foo.{{wildcard(2)}}" orders.local.order1
> orders.order1
```

> **ℹ️ Thông tin:**
> Import/export mapping phải được map hai chiều không mơ hồ.

## Tách token

> 🇬🇧 *There are two ways you can split tokens:*

Có hai cách để tách token:

### Tách theo dấu phân cách

> 🇬🇧 *You can split a token on each occurrence of a separator string using the `split(separator)` transform function.*

Bạn có thể tách một token tại mỗi vị trí xuất hiện của chuỗi phân cách bằng hàm transform `split(separator)`.

Ví dụ:

* Tách theo '-': `nats server mapping "*" "{{split(1,-)}}" foo-bar` trả về `foo.bar`.
* Tách theo '--': `nats server mapping "*" "{{split(1,--)}}" foo--bar` trả về `foo.bar`.

### Tách tại vị trí offset

> 🇬🇧 *You can split a token in two at a specific location from the start or the end of the token using the `SplitFromLeft(wildcard index, offset)` and `SplitFromRight(wildcard index, offset)` transform functions (note that the upper camel case on all subject transform function names is optional you can also use all lowercase function names if you prefer).*

Bạn có thể tách token thành hai phần tại một vị trí cụ thể tính từ đầu hoặc cuối token, bằng cách dùng hàm transform `SplitFromLeft(wildcard index, offset)` và `SplitFromRight(wildcard index, offset)` (lưu ý rằng chữ hoa camelCase trong tất cả tên hàm transform là tùy chọn — bạn cũng có thể dùng tên hàm viết thường hoàn toàn).

Ví dụ:

* Tách token tại vị trí 4 từ trái: `nats server mapping "*" "{{splitfromleft(1,4)}}" 1234567` trả về `1234.567`.
* Tách token tại vị trí 4 từ phải: `nats server mapping "*" "{{splitfromright(1,4)}}" 1234567` trả về `123.4567`.

## Cắt lát (Slice) token

> 🇬🇧 *You can slice tokens into multiple parts at a specific interval from the start or the end of the token by using the `SliceFromLeft(wildcard index, number of characters)` and `SliceFromRight(wildcard index, number of characters)` mapping functions.*

Bạn có thể cắt token thành nhiều phần theo một khoảng cố định tính từ đầu hoặc cuối token, bằng cách dùng hàm mapping `SliceFromLeft(wildcard index, number of characters)` và `SliceFromRight(wildcard index, number of characters)`.

Ví dụ:

* Cắt mỗi 2 ký tự từ trái: `nats server mapping "*" "{{slicefromleft(1,2)}}" 1234567` trả về `12.34.56.7`.
* Cắt mỗi 2 ký tự từ phải: `nats server mapping "*" "{{slicefromright(1,2)}}" 1234567` trả về `1.23.45.67`.

## Phân vùng token subject theo cách tất định

> 🇬🇧 *Deterministic token partitioning allows you to use subject-based addressing to deterministically divide (partition) a flow of messages where one or more of the subject tokens is mapped into a partition key. Deterministically means, the same tokens are always mapped into the same key. The mapping will appear random and may not be `fair` for a small number of subjects.*

Tính năng phân vùng token tất định (deterministic token partitioning) cho phép dùng địa chỉ dựa trên subject để chia (partition) luồng message một cách tất định, trong đó một hoặc nhiều token của subject được map vào một partition key. Tất định có nghĩa là các token giống nhau luôn được map vào cùng một key. Việc mapping có thể có vẻ ngẫu nhiên và có thể không `fair` với số lượng nhỏ subject.

> 🇬🇧 *For example: new customer orders are published on `neworders.<customer id>`, you can partition those messages over 3 partition numbers (buckets), using the `partition(number of partitions, wildcard token positions...)` function which returns a partition number (between 0 and number of partitions-1) by using the following mapping `"neworders.*" : "neworders.{{wildcard(1)}}.{{partition(3,1)}}"`.*

Ví dụ: đơn hàng khách hàng mới được publish trên `neworders.<customer id>`, bạn có thể phân vùng các message đó thành 3 partition number (bucket), dùng hàm `partition(number of partitions, wildcard token positions...)` trả về một partition number (từ 0 đến số partition-1) bằng cách dùng mapping sau: `"neworders.*" : "neworders.{{wildcard(1)}}.{{partition(3,1)}}"`.

```
nats server mapping "neworders.*" "neworders.{{wildcard(1)}}.{{partition(3,1)}}" neworders.customerid1
> neworders.customerid1.0
```

> **ℹ️ Thông tin:**
> Có thể chỉ định nhiều vị trí token để tạo thành một loại _composite partition key_. Ví dụ, một subject có dạng `foo.*.*` có thể có partition transform là `foo.{{wildcard(1)}}.{{wildcard(2)}}.{{partition(5,1,2)}}` — kết quả sẽ là năm partition có dạng `foo.*.*.<n>`, nhưng dùng hash của cả hai wildcard token khi tính partition number.
>
> ```
> nats server mapping "foo.*.*" "foo.{{wildcard(1)}}.{{wildcard(2)}}.{{partition(5,1,2)}}" foo.us.customerid 
> > foo.us.customerid.0
> ```

This particular transform means that any message published on `neworders.<customer id>` will be mapped to `neworders.<customer id>.<a partition number 0, 1, or 2>`. i.e.:

| Published on          | Mapped to               |
| --------------------- | ----------------------- |
| neworders.customerid1 | neworders.customerid1.0 |
| neworders.customerid2 | neworders.customerid2.2 |
| neworders.customerid3 | neworders.customerid3.1 |
| neworders.customerid4 | neworders.customerid4.2 |
| neworders.customerid5 | neworders.customerid5.1 |
| neworders.customerid6 | neworders.customerid6.0 |

The transform is deterministic because (as long as the number of partitions is 3) 'customerid1' will always map to the same partition number. The mapping is hash-based, its distribution is random but tends towards 'perfectly balanced' distribution (i.e. the more keys you map the more the number of keys for each partition will tend to converge to the same number).

You can partition on more than one subject wildcard token at a time, e.g.: `{{partition(10,1,2)}}` distributes the union of token wildcards 1 and 2 over 10 partitions.

| Published on | Mapped to |
| ------------ | --------- |
| foo.1.a      | foo.1.a.1 |
| foo.1.b      | foo.1.b.0 |
| foo.2.b      | foo.2.b.9 |
| foo.2.a      | foo.2.a.2 |

What this deterministic partition transform enables is the distribution of the messages that are subscribed to using a single subscriber (on `neworders.*`) into three separate subscribers (respectively on `neworders.*.0`, `neworders.*.1` and `neworders.*.2`) that can operate in parallel.

```
nats server mapping "foo.*.*" "foo.{{wildcard(1)}}.{{wildcard(2)}}.{{partition(3,1,2)}}"
```

### When is deterministic partitioning uselful

The core NATS queue-groups and JetStream durable consumer mechanisms to distribute messages amongst a number of subscribers are partition-less and non-deterministic, meaning that there is no guarantee that two sequential messages published on the same subject are going to be distributed to the same subscriber. While in most use cases a completely dynamic, demand-driven distribution is what you need, it does come at the cost of guaranteed ordering because if two subsequent messages can be sent to two different subscribers which would then both process those messages at the same time at different speeds (or the message has to be re-transmitted, or the network is slow, etc.) and that could result in potential 'out of order' message delivery.

This means that if the application requires strictly ordered message processing, you need to limit distribution of messages to 'one at a time' (per consumer/queue-group, i.e. using the 'max acks pending' setting), which in turn hurts scalability because it means no matter how many workers you have subscribed, only one is doing any processing work at a time.

Being able to evenly split (i.e. partition) subjects in a deterministic manner (meaning that all the messages on a particular subject are always mapped to the same partition) allows you to distribute and scale the processing of messages in a subject stream while still maintaining strict ordering per subject. For example, inserting a partition number as a token in the message subject as part of the stream definition and then using subject filters to create a consumer per partition (or set of partitions).

Another scenario for deterministic partitioning is in the extreme message publication rate scenarios where you are reaching the limits of the throughput of incoming messages into a stream capturing messages using a wildcard subject. This limit can be ultimately reached at very high message rate due to the fact that a single nats-server process is acting as the RAFT leader (coordinator) for any given stream and can therefore become a limiting factor. In that case, distributing (i.e. partitioning) that stream into a number of smaller streams (each one with its own RAFT leader and therefore all these RAFT leaders are spread over all of the JetStream-enabled nats-servers in the cluster rather than a single one) in order to scale.

Yet another use case where deterministic partitioning can help is if you want to leverage local data caching of data (context or potentially heavy historical data for example) that the subscribing process need to access as part of the processing of the messages.

## Weighted mappings

Traffic can be split by percentage from one subject transform to multiple subject transforms.

### For A/B testing or canary releases

Here's an example for canary deployments, starting with version 1 of your service.

Applications would make requests of a service at `myservice.requests`. The responders doing the work of the server would subscribe to `myservice.requests.v1`. Your configuration would look like this:

```
  myservice.requests: [
    { destination: myservice.requests.v1, weight: 100% }
  ]
```

All requests to `myservice.requests` will go to version 1 of your service.

When version 2 comes along, you'll want to test it with a canary deployment. Version 2 would subscribe to `myservice.requests.v2`. Launch instances of your service.

Update the configuration file to redirect some portion of the requests made to `myservice.requests` to version 2 of your service.

For example the configuration below means 98% of the requests will be sent to version 1 and 2% to version 2.

```
    myservice.requests: [
        { destination: myservice.requests.v1, weight: 98% },
        { destination: myservice.requests.v2, weight: 2% }
    ]
```

Once you've determined Version 2 is stable you can switch 100% of the traffic over to it and you can then shut down the version 1 instance of your service.

### For traffic shaping in testing

Traffic shaping is also useful in testing. You might have a service that runs in QA that simulates failure scenarios which could receive 20% of the traffic to test the service requestor.

`myservice.requests.*: [{ destination: myservice.requests.{{wildcard(1)}}, weight: 80% }, { destination: myservice.requests.fail.{{wildcard(1)}}, weight: 20% }`

### For artificial loss

Alternatively, introduce loss into your system for chaos testing by mapping a percentage of traffic to the same subject. In this drastic example, 50% of the traffic published to `foo.loss.a` would be artificially dropped by the server.

`foo.loss.>: [ { destination: foo.loss.>, weight: 50% } ]`

You can both split and introduce loss for testing. Here, 90% of requests would go to your service, 8% would go to a service simulating failure conditions, and the unaccounted for 2% would simulate message loss.

`myservice.requests: [{ destination: myservice.requests.v3, weight: 90% }, { destination: myservice.requests.v3.fail, weight: 8% }]` the remaining 2% is "lost"

## Cluster scoped mappings

If you are running a super-cluster you can define transforms that apply only to messages being published from a specific cluster.

For example if you have 3 clusters named `east` `central` and `west` and you want to map messages published on `foo` in the `east` cluster to `foo.east`, those published in the `central` cluster to `foo.central` and so on for `west` you can do so by using the `cluster` keyword in the mapping source and destination.

```
mappings = {
        "foo":[
               {destination:"foo.west", weight: 100%, cluster: "west"},
               {destination:"foo.central", weight: 100%, cluster: "central"},
               {destination:"foo.east", weight: 100%, cluster: "east"}
        ]
}
```

This means that the application can be portable in terms of deployment and does not need to be configured with the name of the cluster it happens to be connected in order to compose the subject: it just publishes to `foo` and the server will map it to the appropriate subject based on the cluster it's running in.

## Subject mapping and transforms in streams

You can define subject mapping transforms as part of the stream configuration.

Transforms can be applied in multiple places in the stream configuration:

* You can apply a subject mapping transformation as part of a stream mirror
* You can apply a subject mapping transformation as part of a stream source
* You can apply an overall stream ingress subject mapping transformation that applies to all matching messages regardless of how they are ingested into the stream
* You can also apply a subject mapping transformation as part of the re-publishing of messages

Note that when used in Mirror, Sources or Republish, the subject transforms are filters with optional transformation, while when used in the Stream configuration it only transforms the subjects of the matching messages and does not act as a filter.

```
{
  "name": "orders",
  "subjects": [ "orders.local.*"],
  "subject_transform":{"src":"orders.local.*","dest":"orders.{{wildcard(1)}}"},
  "retention": "limits",
  ...
  "sources": [
    {
      "name": "other_orders",
      "subject_transforms": [
        {
          "src": "orders.online.*",
          "dest": "orders.{{wildcard(1)}}"
        }
      ]
    }
  ],
  "republish": {
    "src": "orders.*",
    "dest": "orders.trace.{{wildcard(1)}}"
  }
    
}
```
> **ℹ️ Thông tin:**
> Đối với các transform `sources` và `republish`, biểu thức `src` sẽ hoạt động như bộ lọc. Các subject không khớp sẽ bị bỏ qua.
>
> Đối với `subject_transform` ở cấp stream, các subject không khớp sẽ không bị thay đổi.

![](https://raw.githubusercontent.com/nats-io/nats.docs/master/assets/images/stream-transform.png)

## Thuật ngữ trong bài

- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **message**: gói dữ liệu được gửi đi
- **node**: một server trong cluster
- **partition**: phần dữ liệu được chia ra
- **publisher**: bên gửi message
- **scope**: phạm vi quyền
- **service**: dịch vụ
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **token**: chuỗi xác thực