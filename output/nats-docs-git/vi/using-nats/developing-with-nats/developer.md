---
crawled_at: '2026-05-10T14:19:53.695272+00:00'
source_url: https://docs.nats.io/using-nats/developing-with-nats/developer
title: Cách Phát Triển với NATS Client API
translated: true
translated_at: '2026-05-17T00:00:00Z'
---

# Cách Phát Triển với NATS Client API

> 🇬🇧 *Developing with NATS involves a blend of distributed application techniques, common NATS features, and library-specific syntax. Besides this guide, most libraries provide auto-generated API documentation, along with language and platform-specific examples, guides, and other resources.*

Phát triển với NATS kết hợp các kỹ thuật distributed application, các tính năng phổ biến của NATS và cú pháp riêng của từng library (thư viện). Ngoài tài liệu này, hầu hết các library còn cung cấp API (giao diện lập trình) documentation được tạo tự động, kèm theo các ví dụ, hướng dẫn và tài nguyên theo ngôn ngữ và nền tảng cụ thể.

| Language | Links                                                                                                               | Supported by Synadia                                                           |
| :--- |:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| :------|
| Golang | [nats.go](https://github.com/nats-io/nats.go), [godoc](http://godoc.org/github.com/nats-io/nats.go)                                                       |  Yes                     |
| Java | [nats.java](https://github.com/nats-io/nats.java), [javadoc](https://javadoc.io/doc/io.nats/jnats), [nats.java examples](https://github.com/nats-io/nats.java/tree/main/src/examples/java/io/nats/examples), [java-nats-examples repo](https://github.com/nats-io/java-nats-examples) |  Yes   | 
| .NET | [nats.net](https://github.com/nats-io/nats.net), [docs](http://nats-io.github.io/nats.net/), [package](https://www.nuget.org/packages/NATS.Net)       |  Yes              |
| Rust | [nats.rs](https://github.com/nats-io/nats.rs), [rust doc](https://docs.rs/async-nats/latest/async_nats/)               |  Yes                                                                                   |
| JavaScript | [nats.js](https://github.com/nats-io/nats.js), [jsdoc](https://nats-io.github.io/nats.js/) |  Yes  |
| Python | [nats.py](https://github.com/nats-io/nats.py), [doc](https://nats-io.github.io/nats.py/)                       |  Yes                                                                  |
| C | [nats.c](https://github.com/nats-io/nats.c), [doc](http://nats-io.github.io/nats.c)                      |  Yes                                                                        |
| Ruby | [nats-pure.rb](https://github.com/nats-io/nats-pure.rb), [yard](https://www.rubydoc.info/gems/nats)                                                                            |
| Elixir | [nats.ex](https://github.com/nats-io/nats.ex), [hex doc](https://hex.pm/packages/gnat)                                                                                         |
| Zig | [nats.zig](https://github.com/nats-io/nats.zig)                                                                                                                                |
| Swift | [nats.swift](https://github.com/nats-io/nats.swift) |

> 🇬🇧 *Not all libraries have their own documentation, depending on the language community, but be sure to check out the client libraries' README for more information.*

Không phải library nào cũng có tài liệu riêng — điều này tùy thuộc vào cộng đồng của từng ngôn ngữ. Hãy kiểm tra README của các client library để biết thêm thông tin.

> 🇬🇧 *There are many other NATS client libraries and examples contributed and maintained by the community and available on GitHub, such as:*

Ngoài ra còn nhiều NATS client library và ví dụ khác do cộng đồng đóng góp và duy trì, có thể tìm thấy trên GitHub:

* [Kotlin Multiplatform client](https://github.com/n-hass/nats.kt), and Java client in [Kotlin examples](https://github.com/nats-io/kotlin-nats-examples)
* [Dart](https://github.com/dgofman/nats_client), [Dart](https://github.com/chartchuo/dart-nats) and [Dart](https://github.com/c16a/nats-dart)
* [Tcl](https://github.com/Kazmirchuk/nats-tcl)
* [Crystal](https://github.com/jgaskins/nats)
* [PHP](https://github.com/basis-company/nats.php) and [PHP](https://github.com/repejota/phpnats)
* [Pascal](https://github.com/biot2/nats.pas/blob/main/nats.core.pas)
* and many [more](https://github.com/search?o=desc&p=1&q=nats+client&s=updated&type=Repositories)...

## Thuật ngữ trong bài

- **API**: giao diện lập trình
- **library**: thư viện