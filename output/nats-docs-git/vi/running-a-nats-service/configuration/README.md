---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/running-a-nats-service/configuration
title: Cấu hình
translated: true
translated_at: '2026-05-13T00:00:00+00:00'
---

# Cấu hình

> 🇬🇧 *While the NATS server has many flags that allow for simple testing of features from command line. The standard way of configuring the NATS server product is through a configuration file. We use a simple configuration format that combines the best of traditional formats and newer styles such as JSON and YAML.*

NATS server có nhiều flag cho phép kiểm tra tính năng nhanh từ command line, nhưng cách chuẩn để cấu hình là dùng file config (cấu hình). Định dạng config kết hợp ưu điểm của các format truyền thống với các style hiện đại như JSON và YAML.

```shell
nats-server -config my-server.conf
```

> 🇬🇧 *The NATS configuration supports the following syntax:*

NATS config hỗ trợ cú pháp sau:

- Lines can be commented with `#` and `//`
- Values can be assigned to properties with delimiters:
  - Equals sign: `foo = 2`
  - Colon: `foo: 2`
  - Whitespace: `foo 2`
- Arrays are enclosed in brackets: `["a", "b", "c"]`
- Maps are enclosed in braces: `{foo: 2}`
- Maps can be assigned with no delimiter `accounts { SYS {...}, cloud-user {...} }`  
- Semicolons can be optionally used as terminators `host: 127.0.0.1; port: 4222;`

> 🇬🇧 *The NATS configuration file is parsed with UTF-8 encoding.*

File config của NATS được phân tích cú pháp theo encoding UTF-8.

> **ℹ️ Info:**
> We strongly recommend using only ASCII for names and values, limiting the use of Unicode, no ASCII text to comments.

> **ℹ️ Info:**
> Khuyến nghị chỉ dùng ASCII cho tên và giá trị, hạn chế dùng Unicode; phần comment không bị giới hạn ASCII.

#### Lưu ý

> 🇬🇧 *The NATS configuration in the file can also be rendered as a JSON object (with comments!), but to combine it with variables the variables still have to be unquoted.*

Config NATS trong file cũng có thể biểu diễn dưới dạng JSON object (có hỗ trợ comment!), nhưng khi kết hợp với biến, các biến đó vẫn phải để không có dấu nháy.

> **ℹ️ Info:**
> JSON config files should be limited machine generated configuration files

> **ℹ️ Info:**
> File config dạng JSON chỉ nên dùng cho các file được tạo tự động bởi máy.

## Chuỗi và Số

> 🇬🇧 *The configuration parser is very forgiving, as you have seen:*

Bộ phân tích cú pháp config rất linh hoạt:

- values can be a primitive, or a list, or a map
- strings and numbers typically do the right thing
- numbers support units such as, 1K for 1000, 1KB for 1024

> 🇬🇧 *String values that start with a digit _can_ create issues. To force such values as strings, quote them.*

Các giá trị chuỗi bắt đầu bằng chữ số _có thể_ gây ra vấn đề. Để buộc chúng được xử lý là chuỗi, hãy đặt trong dấu nháy.

_BAD Config_:

```text
listen: 127.0.0.1:4222
authorization: {
    # Bad - Number parsing error
    token: 3secret
}
```

Fixed Config:

```text
listen: 127.0.0.1:4222
authorization: {
    # Good
    token: "3secret"
}
```

## Biến

> 🇬🇧 *Server configurations can specify variables. Variables allow you to reference a value from one or more sections in the configuration.*

Config server có thể khai báo biến. Biến cho phép tham chiếu một giá trị từ một hoặc nhiều phần trong config.

**Variables syntax:**

* Are block-scoped
* Are referenced with a `$` prefix. Variables in quotes blocks are ignored. For example, a usage like `foo = "$VAR1"` will result in `foo` being the literal string `"$VAR1"`.
* Variables MUST be used to be recognized as such. The config parser will distinguish `unknown field` from variable by finding a reference to the variable. 
* Variable reference which are not defined will be resolved from environment variables.

**Variable resolution sequence:** 
* Look for variable in same scope
* Look for variable in parent scopes
* Look for variable in enviroment variables
* If not found stop server startup with the error below

`nats-server: variable reference for 'PORT' on line 5 can not be found`

> **⚠️ Warning:**
> If the environment variable value begins with a number you may have trouble resolving it depending on the server version you are running.

> **⚠️ Warning:**
> Nếu giá trị biến môi trường bắt đầu bằng chữ số, bạn có thể gặp sự cố khi phân giải tùy thuộc vào phiên bản server đang chạy.

```text
# Define a variable in the config
TOKEN: "secret"

# Reference the variable
authorization {
    token: $TOKEN
}
```

```text
# Define a variable in the config
# But TOKEN is never used resulting in a config parsing error
TOKEN: "secret"

# Reference the variable
authorization {
    token: "another secret"
}
```
```shell
unknown field "TOKEN"
```

> 🇬🇧 *A similar configuration, but this time, the variable is resolved from the environment:*

Cấu hình tương tự, nhưng lần này biến được phân giải từ môi trường:

```shell
export TOKEN="hello"
nats-server -c /config/file
```

```text
# TOKEN is defined in the environment
authorization {
    token: $TOKEN
}
```

## Include Directive

> 🇬🇧 *The `include` directive allows you to split a server configuration into several files. This is useful for separating configuration into chunks that you can easily reuse between different servers.*

Directive `include` cho phép chia config server thành nhiều file. Điều này hữu ích khi cần tách config thành các phần có thể tái sử dụng giữa các server khác nhau.

> 🇬🇧 *Includes _must_ use relative paths, and are relative to the main configuration \(the one specified via the `-c` option\):*

Include _phải_ dùng đường dẫn tương đối, tính từ file config chính (file được chỉ định qua option `-c`):

server.conf:

```text
listen: 127.0.0.1:4222
include ./auth.conf
```

> Note that `include` is not followed by `=` or `:`, as it is a _directive_.

> Lưu ý rằng `include` không có `=` hay `:` theo sau vì nó là một _directive_.

auth.conf:

```text
authorization: {
    token: "f0oBar"
}
```

```text
> nats-server -c server.conf
```

## Reload Cấu hình

> 🇬🇧 *The config file is being read by the server on startup and is not re-scanned for changes and not locked.*

File config được server đọc khi khởi động và không tự động theo dõi thay đổi, cũng không bị khóa.

> 🇬🇧 *A server can reload most configuration changes without requiring a server restart or clients to disconnect by sending the nats-server a [signal](../nats_admin/signals.md):*

Server có thể reload hầu hết các thay đổi config mà không cần khởi động lại hay ngắt kết nối client bằng cách gửi [signal](../nats_admin/signals.md) tới nats-server:

```shell
nats-server --signal reload
```

> 🇬🇧 *As of NATS v2.10.0, a reload signal can be sent on a NATS service using a system account user, where `<server-id>` is the unique ID of the server be targeted.*

Từ NATS v2.10.0, có thể gửi signal reload trên một NATS service thông qua tài khoản hệ thống, trong đó `<server-id>` là ID duy nhất của server đích.

```shell
nats --user sys --password sys request '$SYS.REQ.SERVER.<server-id>.RELOAD' ""
```

## Các Thuộc tính Cấu hình

> 🇬🇧 *Config files have the following structure (in no specific order). All blocks and properties are optional (except host and port).*

File config có cấu trúc sau (không theo thứ tự cụ thể). Tất cả các block và thuộc tính đều là tùy chọn (ngoại trừ host và port).

> 🇬🇧 *Please see sections below for links to detailed explanations of each configuration block*

Xem các phần bên dưới để biết giải thích chi tiết về từng block config.

```text
#General settings
host: 0.0.0.0
port: 4222

# Various server level options
# ...

# The following sections are maps with a set of (nested) properties

jetstream {
    # JetStream storage location, limits and encryption
	store_dir: nats
}

tls { 
    # Configuration map for tls parameters used for client connections, 
    # routes and https monitoring connections.
}

gateway {
    # Configuration map for gateway. Gateways are used to connected clusters.
}

leafnodes {
    # Configuration map for leafnodes. LeafNodes are lightweight clusters.
}

mqtt {
    # Configuration map for mqtt. Allow clients to connect via mqtt protocol.
} 

websocket {
    # Configuration map for websocket. Allow clients to connect via websockets.
} 

accounts {
    # List of accounts and user within accounts
    # User may have an authorization and authentication section
}

authorization { 
    # User may have an authorization and authentication section
    # This section is only useful when no accounts are defined
}

mappings {
    # Subject mappings for default account
    # When accounts are defined this section must be in the account map
}

resolver {
    # Pointer to external Authentication/Authorization resolver
    # There are multiple possible resolver type explained in their own chapters of this docuemntaion
    # memory, nats-base, url ... more may be added in the future
    # This parameter can be a value `MEMORY` for simple configuration
    # or a map of properties for connecting to the resolver
}

resolver_tls {
    # TLS configuration for an URL based resolver
}

resolver_preload {
    # List of JWT tokens to be loaded at server start.
}

```

### Kết nối

| Property                                                                                           | Description                                                                                                                                                                           | Default / Example                                  |
| :------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------- |
| `host`                                                                                             | Host for client connections.                                                                                                                                                          | `0.0.0.0`                                 |
| `port`                                                                                             | Port for client connections.                                                                                                                                                          | `4222`                                    |
| `listen`                                                                                           | Listen specification `<host>:<port>` for client connections. Either use this or the options `host` and/or `port`.                                                                     | `0.0.0.0:4222`  &nbsp; Inherits from `host` and `port`                    |
| `client_advertise`                                                                                 | Alternative client listen specification `<host>:<port>` or just `<host>` to advertise to clients and other server. Advertising is only active in [cluster](./clustering/cluster_config.md) setups with NAT. Explicitly setting the URL is useful when the server is situated behind a load balancer and/or TLS server authentication requires the correct DNS name to be presented. To completely disable `client_advertise` please set `no_advertise: true` in the [cluster configuration](./clustering) section.   | A list of all interfaces the the server is bound to. `E.g. 127.0.0.1:4222,192.168.0.13:4222` |
| [`tls`](./securing_nats/tls.md)                                | Configuration map for [tls](./securing_nats/tls.md) parameters used for client connections, routes and https monitoring connections.                                                                                                                             |                  `tls {}` &nbsp;No tls active by default. Plain text TCP/IP.                         |
| [`gateway`](./gateways/gateway.md#gateway-configuration-block) | Configuration map for [gateway](./gateways). Gateways are used to connected clusters into superclusters.                                                                                                     |    `gateway {}` &nbsp; None by default.                                       |
| [`leafnodes`](./leafnodes/leafnode_conf.md)                    | Configuration map for [leafnodes](./leafnodes). LeafNodes are lightweight clusters.                                                                                                  |                `leafnodes {}` &nbsp; None by default.                             |
| [`mqtt`](./mqtt/mqtt_config.md)                                | Configuration map for [mqtt](./mqtt). Allow clients to connect via mqtt protocol.                                                                                                            |       `mqtt {}` &nbsp; Not active by default.                                       |
| [`websocket`](./websocket/websocket_conf.md)                   | Configuration map for [websocket](./websocket).                                                                                                   |    `websocket {}` &nbsp; Not active by default.                                          |

### Clustering

| Property                                                                        | Description                                                                        | Default |
| :------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------- | :------ |
| [`cluster`](./clustering/cluster_config.md) | Configuration map for [cluster](./clustering). Nats Servers can form a cluster for load balancing and redundancy. |       `cluster {}` &nbsp; Not active by default.           |

### Subject Mappings

> 🇬🇧 *Note that each accounts forms its own subject namespace. Therefore the `mappings` section can appear on the server level (applying to the default account) or on the account level.*

Lưu ý rằng mỗi account tạo thành một namespace subject (chuỗi định danh message) riêng. Do đó, phần `mappings` có thể xuất hiện ở cấp server (áp dụng cho account mặc định) hoặc ở cấp account.

```text
host: 0.0.0.0
port:4222

mappings: {
	foo: bar
}

accounts: {
    accountA: { 
	mappings: {
	    orders.acme.*: orders.$1
	}
        users: [
            {user: admin, password: admin},
            {user: user, password: user}
           ]
    },
}
```

| Property                                                                        | Description                                                                        | Default |
| :------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------- | :------ |
| [`mappings`](./configuring_subject_mapping.md) | Configuration map for [mapping subject](./configuring_subject_mapping.md). Allows for subjects aliasing and patterns based translation. Can be used to great effect in supercluster and leafnode configuration and when sourcing streams.  |       `mappings {}` &nbsp; (none set)            |

### Timeout Kết nối

| Property         | Description                                                                                                                                                                                                                                                                                                                | Default |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------ |
| `ping_interval`  | Duration at which pings are sent to clients, leaf nodes and routes. In the presence of client traffic, such as messages or client side pings, the server will not send pings. Therefore it is recommended to keep this value bigger than what [clients use](../../using-nats/developing-with-nats/connecting/pingpong.md). | `"2m"`  |
| `ping_max`       | After how many unanswered pings the server will allow before closing the connection.                                                                                                                                                                                                                                       | `2`     |
| `write_deadline` | Maximum number of seconds the server will block when writing. Once this threshold is exceeded the connection will be closed. See [_slow consumer_](../../using-nats/developing-with-nats/events/slow.md) on how to deal with this on the client.                                                                                | `"10s"` |

### Giới hạn

| Property            | Description                                                                                                                                                                                                                                                                                                                                                                                                   | Default        |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------- |
| `max_connections`   | Maximum number of active client connections.                                                                                                                                                                                                                                                                                                                                                                  | `64K`          |
| `max_control_line`  | Maximum length of a protocol line \(including combined length of subject and queue group\). Increasing this value may require [client changes](../../using-nats/developing-with-nats/connecting/misc.md#set-the-maximum-control-line-size) to be used. Applies to all traffic.                                                                                                                                     | `4KB`          |
| `max_payload`       | Maximum number of bytes in a message payload. Reducing this size may force you to implement [chunking](../../using-nats/developing-with-nats/connecting/misc.md#get-the-maximum-payload-size) in your clients. Applies to client and leafnode payloads. It is not recommended to use values over 8MB but `max_payload` can be set up to 64MB. The max payload must be equal to or smaller than the `max_pending` value. | `1MB`          |
| `max_pending`       | Maximum number of bytes buffered for a connection. Applies to client connections. Note that applications can also set 'PendingLimits' (number of messages and total size) for their subscriptions.                                                                                                                                                                                                             | `64MB`         |
| `max_subscriptions` | Maximum numbers of subscriptions per client and leafnode accounts connection.                                                                                                                                                                                                                                                                                                                                 | `0`, unlimited |

### Cài đặt JetStream ở Server

> 🇬🇧 *You can enable JetStream in the server's configuration by simply adding a `jetstream {}` map. By default, the JetStream subsystem will store data in the /tmp directory, but you can specify the directory to use via the `store_dir`, as well as the limits for JetStream storage (a value of 0 means no limit).*

Có thể bật JetStream bằng cách thêm map `jetstream {}` vào config server. Mặc định, JetStream lưu dữ liệu trong thư mục /tmp; có thể chỉ định thư mục khác qua `store_dir` và đặt giới hạn lưu trữ (giá trị 0 nghĩa là không giới hạn).

> 🇬🇧 *Normally JetStream will be run in clustered mode and will replicate data, so the best place to store JetStream data would be locally on a fast SSD. One should specifically avoid NAS or NFS storage for JetStream.*

Thông thường JetStream chạy trong cluster (cụm nhiều server chạy chung) và tự sao chép dữ liệu, vì vậy nên lưu dữ liệu JetStream ở ổ SSD nhanh trên máy local. Cần tránh dùng NAS hoặc NFS cho JetStream.

> **⚠️ Warning:**
> Note that each JetStream enabled server MUST use its own individual storage directory.  JetStream replicates data between cluster nodes (up to 5 replicas), achieving redundancy and availability through this.
>
> JetStream does not implement standby and fault tolerance through a shared file system. If a standby server shares a storage directory with an active server, you must make sure only one is active at any time. Access conflicts are not detected. We do not recommend such a setup.

> **⚠️ Warning:**
> Mỗi server bật JetStream PHẢI dùng thư mục lưu trữ riêng. JetStream sao chép dữ liệu giữa các node trong cluster (tối đa 5 replica), qua đó đạt được tính dự phòng và khả dụng.
>
> JetStream không hỗ trợ standby hay fault tolerance qua file system dùng chung. Nếu một server standby chia sẻ thư mục lưu trữ với server đang hoạt động, phải đảm bảo chỉ một server hoạt động tại một thời điểm. Xung đột truy cập không được phát hiện. Chúng tôi không khuyến nghị thiết lập này.

> 🇬🇧 *Here's an example minimal file that will store data in a local "nats" directory with some limits.*

Đây là ví dụ file config tối giản lưu dữ liệu vào thư mục "nats" local với một số giới hạn.

`$ nats-server -c js.conf`

```text
jetstream {
  store_dir: nats

  # 1GB
  max_memory_store: 1073741824

  # 10GB
  max_file_store: 10737418240
}
```

**Global JetStream options (server level)**

| Property                  | Description                                                                                                                                                                               | Default                 | Version |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------- | :------ |
| `enable`                     |  Enable/disable JetStream without removing this section.  | `true`  | 2.2.0  |
| `store_dir`               | Directory to use for JetStream storage.                                                                                                                                                   | `/tmp/nats/jetstream`   | 2.2.0   |
| `max_memory_store`        | Maximum size of the 'memory' storage                                                                                                                                                      | 75% of available memory | 2.2.0   |
| `domain`        | Isolates the JetStream cluster to the local cluster. Recommended use with leaf nodes.                                                                                                                                                      | (not set) | 2.2.3   |
| `extension_hint`        | `no_extend` or  `will_extend` - Used in a leaf cluster that may or may not want to extend the domain of the hub it connects to. This option ONLY applies if a `SYSTEM` account is shared (connected) between leaf and hub AND the following conditions are met: <br> * IF the leaf node is standalone (not a cluster) AND supposed to extend (by using the same domain name) the domain of the hub, `will_extend` is required to hint this. If not set, the standalone leaf node will not know it's supposed to be part of a JetStream cluster. <BR> * IF the leaf is a full cluster and is NOT supposed to extend the domain of the hub (because domain names are different) `no_extend` is recommended. This will stop the leaf cluster from waiting for the hub RAFT group to become visible. If not set in the leaf, JetStream will NOT become ready on first startup until the hub can be connected. <BR> Note that this only matters during initial start of the leaf cluster.    | (not set) | 2.2.3   |
| `max_file_store`          | Maximum size of the 'file' storage. For units use `m mb g gb t tb`                                                                                                                                                         |  `1TB`  | 2.2.0   |
| `cipher`                  | Set to enable storage-level [encryption at rest](../nats_admin/jetstream_admin/encryption_at_rest.md). Choose either `chacha`/`chachapoly` or `aes`.                          | (not set)               | 2.3.0   |
| `key`                     | The encryption key to use when encryption is enabled. A key length of at least 32 bytes is recommended. Note, this key is HMAC-256 hashed on startup which reduces the byte length to 64. | (not set)               | 2.3.0   |
| `prev_encryption_key`                     |    The previous encryption key. Used when changing storage encryption keys. | (not set)   | 2.10.0   |
| `max_outstanding_catchup` | Max in-flight bytes for stream catch-up                                                                                                                                                   | 64MB                    | 2.9.0   |
| `max_buffered_msgs`                     |    Maximum number of messages JetStream will buffer in memory when falling behind with RAFT or I/O. Used to protect against OOM when there are write bursts to a queue. | 10.000  | 2.11.0   |
| `max_buffered_size`                     |    Maximum number of bytes JetStream will buffer in memory when falling behind with RAFT or I/O. Used to protect against OOM when there are write bursts to a queue. | 128MB  | 2.11.0   |
| `request_queue_limit`                     |    Limits the number of API commands JetStream will buffer in memory. When the limit is reached, clients will get error responses rather than a timeout. Lower the value if you want to detect clients flooding JetStream. | 10.000  | 2.11.0   |
| `sync_interval`           | Examples: `10s` `1m` `always`  -   Change the default fsync/sync interval for page cache in the filestore. By default JetStream relies on stream replication in the cluster to guarantee data is available after an OS crash. If you run JetStream without replication or with a replication of just 2 you may want to shorten the fsync/sync interval. - You can force an fsync after each messsage with `always`, this will slow down the throughput to a few hundred msg/s. See also the documentaton about the interaction between the stream replication factor and syncing data to disk [here](../../nats-concepts/jetstream/README.md#persistent-and-consistent-distributed-storage). | 2m                      | 2.10.0  |
| `strict`                     |    Return errors for invalid JetStream API requests. Some older client APIs may not expect this. Set to `false` for maximum backward compatibility.  | `true`  | 2.11.0   |
| `unique_tag`                     |    JetStream peers will be placed in servers with tags unique relative to the `unique_tag`  prefix. E.g. nodes in a cluster (or supercluster) are tagged `az:1`,`az:1`,`az:2`,`az:2`,`az:3`,`az:3`,`az:3` . Setting `unique_tag=az` will result in a new replica 3 stream to be placed in all three availability zones.  | (not set))  | 2.8.0  |
| `tpm`                     |  Trusted Platform Module   [TPM base encryption](#jetstream-tpm-encryption) | `tpm {}` (not set)  | 2.11.0   |
| `limits`                     |   [JetStream server limits](#jetstream-server-limits) | `limits{}`  (not set) | 2.8.0   |

### Cài đặt JetStream theo Account

> 🇬🇧 *A JetStream section may also appear in accounts. JetStream is disabled by default. The minimal configuration will enable JetStream.*

Phần JetStream cũng có thể xuất hiện trong cấu hình account. JetStream mặc định bị tắt; config tối giản sau đây sẽ bật JetStream.

```text
accounts {
  A {}
    jetstream {
    }
  } 

```

| Property                  | Description                                                                                                                                                                               | Default                 | Version |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------- | :------ |
| `max_memory`                     |  Maximum memory for in-memory streams. Sum of all accounts must be smaller than the server limit.  | no limit or server limit  | 2.2.0  |
| `max_file`                     |  Maximum memory for disk streams. Sum of all accounts must be smaller than the server limit. | no limit or server limit | 2.2.0  |
| `max_streams`                     |  Maximum number of streams.  | no limit  | 2.2.0  |
| `max_consumers`                     |  Maximum number of consumers per stream(!).  | no limit  | 2.2.0  |
| `max_ack_pending`                     |   Max acks pending in explicit ack mode. Stream stops delivery when the limits have been reached. Can override the server limit. | no limit or server limit  | 2.8.0  |
| `max_bytes_required`                     |  When `true` all streams require a max_bytes limit set. | `false`  | 2.7.0  |
| `store_max_stream_bytes`                     | Maximum size limit to which a disk stream can be set. Usually combined with `max_bytes_required`  | no limit  | 2.8.0  |
| `memory_max_stream_bytes`                     |  Maximum size limit to which a memory stream can be set. Usually combined with `max_bytes_required`  | no limit  | 2.8.0  |
| `cluster_traffic`                     |  `system` or `owner` Configures the account in which stream replication and RAFT traffic is sent. By default (and in all versions prior to 2.11.0) all cluster traffic was handled in the system account. When set to `owner`, such RAFT and replication traffic will be in the account where the stream was created. | `system`  | 2.11.0  |

### JetStream TPM Encryption

````
jetstream {
  store_dir: nats
  max_file_store: 10G
  tpm {
          keys_file: "keys"
          encryption_password: "pwd"
  }
}
````
| Property                  | Description                                                                                                                                                                               | Default                 | Version |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------- | :------ |
| `keys_file`                     |  Specifies the file where encryption keys are stored. This option is required, otherwise TPM will not be active. If the file does NOT EXIST, a new key will be dynamically created and stored in the `pcr`  | required | 2.11.0  |
| `encryption_password`                     | Password used for decrypting data the keys file. OR, the password used to seal the dynamically created key in the TPM store. | required  | 2.11.0  |
| `srk_password`                     |  The Storage Root Key (SRK) password is used to access the TPM's storage root key. The srk password is optional in TPM 2.0. | not set  | 2.11.0  |
| `pcr`                     |  Platform Configuration Registers (PCRs). 0-16 are reserved. Pick a value from 17 to 23. |  22  | 2.11.0  | 
| `cipher`                     |   `chacha`/`chachapoly` or `aes`.                    | `chachapoly` | 2.11.0  |  

### JetStream Server Limits

````
jetstream {
  store_dir: nats
  max_file_store: 10G
  limits {
      max_ack_pending: 10000
      duplicate_window: 600s
  }
}
````
| Property                  | Description                                                                                                                                                                               | Default                 | Version |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------- | :------ |
| `max_ack_pending`                     |  Default max acks pending in explicit ack mode. Stream stops delivery when the limits have been reached.   | no limit | 2.8.0  |
| `max_ha_assets`                     |  Maximum number of RAFT assets (stream and consumers) which can be placed on this node. Will not affect stream/consumers with replicas=1  | no limit  | 2.8.0  |
| `max_request_batch`                     |  Maximum fetch size for pull consumers. Use with caution. May break existing clients violating this limit.| no limit  | 2.8.0  |
| `duplicate_window`                     |  Maximum(!) de-duplication window of streams. Stream creation will fail if the value specified is larger than this. | no limit (but default for new streams is 120s) | 2.8.0  |  

### Xác thực và Phân quyền

#### Xác thực và Phân quyền Tập trung

> 🇬🇧 *A default NATS server will have no authentication or authorization enabled. This is useful for development and simple embedded use cases only. The default account is `$G`.*

Mặc định NATS server không bật xác thực hay phân quyền. Điều này chỉ phù hợp cho môi trường phát triển và các trường hợp nhúng đơn giản. Account mặc định là `$G`.

> 🇬🇧 *Once at least one user is configured in the authorization or accounts sections, the default $G account and no-authentication user are disabled. You can restore no authentication access by setting the `no_auth_user`.*

Khi có ít nhất một user được cấu hình trong phần authorization hoặc accounts, account $G mặc định và user không xác thực sẽ bị tắt. Có thể khôi phục truy cập không xác thực bằng cách đặt `no_auth_user`.

| Property                                                                                       | Description                                                                                                                                                                                                                                                                                                                                                                                                     | Default                                                                                 |
| :--------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| [`authorization`](./securing_nats/auth_intro)              | Configuration map for client [authentication/authorization](./securing_nats/auth_intro). List of user and their auth setting. This section is used when only the default account ($G) is active.                                                                                                                                                                                                        | `authorization {}` &nbsp;(not set)                                                      |
| [`accounts`](./securing_nats/accounts.md)                  | Configuration map for multi tenancy via [accounts](./securing_nats/accounts.md). A list of accounts each with its own users and their auth settings. Each account forms its own subject and stream namespace, with no data shared unless explicit `import` and `export` is configured.                                                                                                                            | `accounts {}` &nbsp;(not set)                                                           |
| [`no_auth_user`](./securing_nats/accounts.md#no-auth-user) | [Username](./securing_nats/auth_intro/username_password.md) present in the [authorization block](./securing_nats/auth_intro) or an [`account`](./securing_nats/accounts.md). A client connecting without any form of authentication will be associated with this user, its permissions and account. | (not set) - will deny unauthorized access by default if any other users are configured. |

#### Xác thực và Phân quyền Phi tập trung

> 🇬🇧 *The Configuration options here refer to [JWT](./securing_nats/jwt) based authentication and authorization.*

Các tùy chọn cấu hình ở đây liên quan đến xác thực và phân quyền dựa trên [JWT](./securing_nats/jwt).

| Property                                                                                           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| :------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`operator`](./securing_nats/jwt/README.md)                    | The Json Web Token of the [auth operator.](./securing_nats)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| [`resolver`](./securing_nats/jwt/README.md)                    | The built-in NATS [`resolver`](./securing_nats/jwt/resolver.md#nats-based-resolver), [`MEMORY`](./securing_nats/jwt/resolver.md#memory) for static or [`URL(<url>)`](./securing_nats/jwt/resolver.md#url-resolver) to use an external account server. \(When the operator JWT contains an account URL, it will be used as default. In this case `resolver` is only needed to overwrite the default.\) |
| [`resolver_tls`](./securing_nats/jwt/resolver.md#url-resolver) | [`tls` configuration map](./securing_nats/tls.md) for tls connections to the resolver. \(This is for an outgoing connection and therefore does not use `timeout`, `verify` and `map_and_verify`\)                                                                                                                                                                                                                                                                             |
| [`resolver_preload`](./securing_nats/jwt/resolver.md#memory)   | [Map](./securing_nats/jwt/resolver.md#memory) to preload account public keys and their corresponding JWT. Keys consist of `<account public nkey>`, value is the `<corresponding jwt>`.                                                                                                                                                                                                                                                                                        |

### Cấu hình Runtime

| Property                 | Description                                                                                                                                                                                                                                                      | Default                |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------- |
| `disable_sublist_cache`  | If `true` disable subscription caches for all accounts. This saves resources in situations where different subjects are used all the time.                                                                                                                                    | `false`, cache enabled |
| `lame_duck_duration`     | In lame duck mode the server rejects new clients and **slowly** closes client connections. After this duration is over, the server shuts down. This value cannot be set lower than 30 seconds. Start lame duck mode with: [`nats-server --signal ldm`](../nats_admin/signals.md). | `"2m"`                 |
| `lame_duck_grace_period` | This is the duration the server waits, after entering lame duck mode, before starting to close client connections                                                                                                                                                                | `"10s"`                |
| `no_fast_producer_stall` | if `true`, the server will no longer stall the producer when attempting to deliver a message to a slow consumer but instead skip this consumer(by dropping the message for this consumer) and move to the next. | `false` the server will stall the fast producer |

### Cấu hình Cluster, Giám sát và Tracing

| Property                                                                                           | Description                                                                                                                                                                                                              | Default                   | Version |
|:---------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------|:--------|
| `server_name`                                                                                      | The server's name, shows up in logging. Defaults to the server's id. When JetStream is used, within a domain, all server names need to be unique.                                                                        | Generated Server ID       |         |
| `server_tags`                                                                                      | A set of tags describing properties of the server. This will be exposed through `/varz` and can be used for system resource requests, such as placement of streams. It is recommended to use `key:value` style notation. | `[]`                      |         |
| `server_metadata`                                                                                  | A map containing string keys and values describing metadata of the server. This will be exposed through `/varz` and can be used for system resource requests.                                                            | `{}`                      | 2.12.0  |
| `trace`                                                                                            | If `true` enable protocol trace log messages. Excludes the system account.                                                                                                                                               | `false`, disabled         |         |
| `trace_verbose`                                                                                    | If `true` enable protocol trace log messages. Includes the system account.                                                                                                                                               | `false`, disabled         |         |
| `debug`                                                                                            | If `true` enable debug log messages                                                                                                                                                                                      | `false`, disabled         |         |
| `logtime`                                                                                          | If set to `false`, log without timestamps                                                                                                                                                                                | `true`, include timestamp |         |
| `log_file`                                                                                         | Log file name, relative to...                                                                                                                                                                                            | No log file               |         |
| [`log_size_limit`](./logging.md#using-the-configuration-file)  | Size in bytes after the log file rolls over to a new one                                                                                                                                                                 | `0`, unlimited            |         |
| [`logfile_max_num`](./logging.md#using-the-configuration-file) | Set the number of rotated logs to retain.                                                                                                                                                                                | `0`, unlimited            |         |
| `max_traced_msg_len`                                                                               | Set a limit to the trace of the payload of a message.                                                                                                                                                                    | `0`, unlimited            |         |
| `syslog`                                                                                           | Log to syslog.                                                                                                                                                                                                           | `false`, disabled         |         |
| `remote_syslog`                                                                                    | [Syslog server](./logging.md#syslog) address.                                                                                                                                        | (not set)                 |         |
| [`http_port`](./monitoring.md)                                 | http port for server monitoring.                                                                                                                                                                                         | (inactive)                |         |  
| [`http`](./monitoring.md)                                      | Listen specification `<host>:<port>`for server monitoring.                                                                                                                                                               | (inactive)                |         |
| [`https_port`](./monitoring.md)                                | https port for server monitoring. This is influenced by the tls property.                                                                                                                                                | (inactive)                |         |
| [`http_base_path`](./monitoring.md)                            | base path for monitoring endpoints.                                                                                                                                                                                      | `/`                       |         |
| [`https`](./monitoring.md)                                     | Listen specification `<host>:<port>`for TLS server monitoring.  Requires the `tls` section to be present.                                                                                                                | (inactive)                |         |
| `system_account`                                                                                   | Name of the system account. Users of this account can subscribe to system events. See [System Accounts](./sys_accounts/README.md#system-account) for more details.                   | `$SYS`                    |         |
| `pid_file`                                                                                         | File containing PID, relative to ... This can serve as input to [nats-server --signal](../nats_admin/signals.md)                                                                                    | (non set)                 |         |
| `port_file_dir`                                                                                    | Directory to write a file containing the servers' open ports to, relative to ...                                                                                                                                         | (not set)                 |         |
| `connect_error_reports`                                                                            | Number of attempts at which a repeated failed route, gateway or leaf node connection is reported. Connect attempts are made once every second.                                                                           | `3600`, approx every hour |         |
| `reconnect_error_reports`                                                                          | Number of failed attempts to reconnect a route, gateway or leaf node connection. Default is to report every attempt.                                                                                                     | `1`, every failed attempt |         |

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **cache**: bộ nhớ đệm
- **cluster**: cụm nhiều server chạy chung
- **config**: cấu hình
- **consumer**: bên xử lý dữ liệu từ stream
- **node**: một server trong cluster
- **payload**: nội dung chính của message
- **permission**: quyền truy cập
- **queue group**: nhóm subscribers chia sẻ tải
- **replica**: bản sao dữ liệu
- **stream**: luồng message lưu trữ liên tục
- **subject**: chuỗi định danh message (giống topic)
- **timeout**: thời gian chờ tối đa
- **token**: chuỗi xác thực