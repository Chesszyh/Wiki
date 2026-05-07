## 当前技术状态

* GitHub Actions: 编译（Build）和部署（Deploy）任务均显示 Success (Green)。
* GitHub Pages 设置: 显示 "Your site is live"，DNS 检查通过，已勾选 "Enforce
    HTTPS"。
* Cloudflare DNS: 
    * wiki 记录为 CNAME 指向 chesszyh.github.io。
    * 目前处于 "Proxied" (已代理/橙色云朵) 状态。

## 核心痛点

访问 https://wiki.chesszyh.xyz 报错 ERR_EMPTY_RESPONSE 或无法连接。

```bash
ubuntu@ip-172-31-45-166:~$ curl -v https://wiki.chesszyh.xyz
* Host wiki.chesszyh.xyz:443 was resolved.
* IPv6: 2606:4700:3030::6815:1fc4, 2606:4700:3030::ac43:b39e
* IPv4: (none)
*   Trying [2606:4700:3030::6815:1fc4]:443...
* Immediate connect fail for 2606:4700:3030::6815:1fc4: Network is unreachable
*   Trying [2606:4700:3030::ac43:b39e]:443...
* Immediate connect fail for 2606:4700:3030::ac43:b39e: Network is unreachable
* Failed to connect to wiki.chesszyh.xyz port 443 after 11 ms: Couldn't connect to server
* Closing connection
curl: (7) Failed to connect to wiki.chesszyh.xyz port 443 after 11 ms: Couldn't connect to server
```

```bash
ubuntu@ip-172-31-45-166:~$ curl -v https://blog.chesszyh.xyz
* Host blog.chesszyh.xyz:443 was resolved.
* IPv6: 2606:4700:3030::ac43:b39e, 2606:4700:3030::6815:1fc4
* IPv4: 104.21.31.196, 172.67.179.158
*   Trying 104.21.31.196:443...
* Connected to blog.chesszyh.xyz (104.21.31.196) port 443
* ALPN: curl offers h2,http/1.1
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
*  CAfile: /etc/ssl/certs/ca-certificates.crt
*  CApath: /etc/ssl/certs
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384 / X25519 / id-ecPublicKey
* ALPN: server accepted h2
* Server certificate:
*  subject: CN=chesszyh.xyz
*  start date: Mar 25 09:01:02 2026 GMT
*  expire date: Jun 23 09:01:01 2026 GMT
*  subjectAltName: host "blog.chesszyh.xyz" matched cert's "*.chesszyh.xyz"
*  issuer: C=US; O=Let's Encrypt; CN=E7
*  SSL certificate verify ok.
*   Certificate level 0: Public key type EC/prime256v1 (256/128 Bits/secBits), signed using ecdsa-with-SHA384
*   Certificate level 1: Public key type EC/secp384r1 (384/192 Bits/secBits), signed using sha256WithRSAEncryption
*   Certificate level 2: Public key type RSA (4096/152 Bits/secBits), signed using sha256WithRSAEncryption
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://blog.chesszyh.xyz/
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: blog.chesszyh.xyz]
* [HTTP/2] [1] [:path: /]
* [HTTP/2] [1] [user-agent: curl/8.5.0]
* [HTTP/2] [1] [accept: */*]
> GET / HTTP/2
> Host: blog.chesszyh.xyz
> User-Agent: curl/8.5.0
> Accept: */*
> 
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
* old SSL session ID is stale, removing
< HTTP/2 403
# ...
```

```bash
ubuntu@ip-172-31-45-166:~$ curl -4 -v https://wiki.chesszyh.xyz
* Could not resolve host: wiki.chesszyh.xyz
* Closing connection
curl: (6) Could not resolve host: wiki.chesszyh.xyz
```

`curl -v` 测试反馈：

1. 解析异常： wiki.chesszyh.xyz 目前仅解析出 IPv6地址（2606:4700...），在测试环境下显示 Network is unreachable。
2. 对比分析： 同一域名下的 blog.chesszyh.xyz github pages/cloudflare配置相同，但能正常解析出 IPv4 地址并建立 TLS 握手（虽然返回 403，但连接是通的）。403的原因可能是缓存问题，因为访问`https://chesszyh.github.io/`会跳转到我之前已经放弃的域名`https://blog.neurosama.uk/`

为什么在 GitHub Actions 部署成功、GitHub Pages 显示 Live 且 Cloudflare 已开启代理的情况下，新子域名 wiki 只解析出 IPv6 且报空响应，而同配置的 blog 子域名却有 IPv4 记录？

## 分析

1. Cloudflare 边缘证书 (Edge Certificate) 签发延迟
当你添加一个新子域名（如 wiki）并开启“橙色小云朵”代理时，Cloudflare 需要为这个新域名申请并部署 SSL 证书。
* 现象： 在证书还没下发到你访问的那个 CDN 节点前，HTTPS 握手会失败，表现为 ERR_EMPTY_RESPONSE 或 Connection Reset。
* 解决： 只需要等 5-15 分钟，证书在全球节点同步完成后，访问就通了。

2. GitHub Pages 内部路由更新
你在 GitHub 设置里填入 wiki.chesszyh.xyz 后，GitHub 的反向代理服务器需要更新它的全局路由表。
* 现象： 如果 GitHub 还没准备好接收这个域名的请求，它可能会直接拒绝连接（403）或者返回空数据。
* 验证： 你之前的 curl 看到 HTTP/2 403，很大概率就是 GitHub 还没把这个域名和你的 Wiki 仓库“对齐”。

3. DNS 负缓存 (Negative Caching)
在你配置好 DNS 之前，如果你尝试访问过这个网址，你的电脑、路由器或 ISP 可能会缓存“该域名不存在”的记录。
* 现象： 即使你后来配置好了，浏览器还是在尝试连接旧的 IP 或直接报错。
* 解决： 等待 TTL（生存时间）过期，或者刷新了本地 DNS 缓存后就会恢复正常。

---

为什么 blog 之前能通？
因为 blog 是你之前就配好的旧记录，SSL 证书和路由早已在全球生效。而 wiki 是全新的，必须经历上述的“初始化周期”。