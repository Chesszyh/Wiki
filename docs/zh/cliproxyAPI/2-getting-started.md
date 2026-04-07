# 入门指南

相关源文件

-   [.dockerignore](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/.dockerignore)
-   [.gitignore](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/.gitignore)
-   [README.md](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md)
-   [README\_CN.md](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README_CN.md)
-   [auths/.gitkeep](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/auths/.gitkeep)
-   [docker-build.ps1](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/docker-build.ps1)
-   [docker-build.sh](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/docker-build.sh)
-   [docker-compose.yml](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/docker-compose.yml)
-   [internal/api/handlers/management/auth\_files.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/api/handlers/management/auth_files.go)

本页面将引导您安装并运行您的第一个 CLI Proxy API 服务器、向 AI 供应商进行身份验证并发送您的第一个 API 请求。它涵盖了以最小配置获得可用部署的基本步骤。

有关详细的安装选项和部署方案，请参阅[安装与部署](/router-for-me/CLIProxyAPI/2.1-installation-and-deployment)。有关全面的配置参考，请参阅[初始配置](/router-for-me/CLIProxyAPI/2.2-initial-configuration)。有关特定供应商的身份验证指南，请参阅[身份验证设置](/router-for-me/CLIProxyAPI/2.3-authentication-setup)和[供应商集成](/router-for-me/CLIProxyAPI/6-provider-integration)。

---

## 概述

CLI Proxy API 以单个二进制文件形式部署，该文件负责：

1.  从 `config.yaml` 加载配置
2.  使用 OAuth 或 API 密钥向 AI 供应商进行身份验证
3.  暴露兼容 OpenAI/Claude/Gemini 的 HTTP 端点
4.  在 API 格式之间转换请求
5.  将请求路由到适当的 AI 供应商

服务器支持多种凭证和配置的存储后端，支持从基于本地文件的单服务器系统到基于数据库的分布式配置的部署。

---

## 部署路径

```mermaid
flowchart TD
    Start["CLI Proxy API Binary"]
    Choice["StorageBackend?"]
    FileMode["File Storage Mode"]
    PGMode["PostgresStore Mode"]
    GitMode["GitStore Mode"]
    ObjMode["ObjectStore Mode"]
    FileSetup["• Simple setup• Local config.yaml• auths/ directory"]
    PGSetup["• Set PGSTORE_DSN• Database tables• Local spool mirror"]
    GitSetup["• Set GITSTORE_GIT_URL• Git repository• Local clone"]
    ObjSetup["• Set OBJECTSTORE_ENDPOINT• S3-compatible storage• Local mirror"]
    AuthStep["Authenticate with Providers"]
    RunServer["Start Server"]
    Ready["Server Ready"]

    Start --> Choice
    Choice --> FileMode
    Choice --> PGMode
    Choice --> GitMode
    Choice --> ObjMode
    FileMode --> FileSetup
    PGMode --> PGSetup
    GitMode --> GitSetup
    ObjMode --> ObjSetup
    FileSetup --> AuthStep
    PGSetup --> AuthStep
    GitSetup --> AuthStep
    ObjSetup --> AuthStep
    AuthStep --> RunServer
    RunServer --> Ready
```
**来源：** [cmd/server/main.go50-482](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L50-L482) [internal/cmd/run.go19-56](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/run.go#L19-L56)

---

## 快速入门：文件存储模式

这是用于开发和单服务器部署的最简单部署路径。

### 步骤 1：获取二进制文件

从发布页面下载二进制文件或从源码构建：

```
go build -o cliproxy-api ./cmd/server
```
### 步骤 2：创建配置文件

在工作目录下创建 `config.yaml`。一个最小化配置示例：

```
port: 8080log_level: infoauth_dir: ./auths
```
服务器将在首次运行时自动创建 `auths/` 目录。

**来源：** [cmd/server/main.go367-377](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L367-L377) [internal/config](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/config)/

### 步骤 3：向供应商进行身份验证

使用内置的 OAuth 流程向 AI 供应商进行身份验证。以 Google Gemini 为例：

```
./cliproxy-api --login
```
此命令将：

1.  打开浏览器进行 Google OAuth 认证
2.  提示选择 GCP 项目
3.  完成 Gemini CLI 入职（onboarding）
4.  将令牌保存到 `auths/gemini-{email}-{project}.json`

对于其他供应商：

-   `--claude-login` 针对 Anthropic Claude
-   `--codex-login` 针对 OpenAI Codex
-   `--antigravity-login` 针对 Antigravity
-   `--qwen-login` 针对 Qwen
-   `--iflow-login` 针对 iFlow

**来源：** [cmd/server/main.go71-84](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L71-L84) [internal/cmd/login.go43-183](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/login.go#L43-L183)

### 步骤 4：启动服务器

```
./cliproxy-api
```
服务器将：

1.  加载 `config.yaml`
2.  扫描 `auths/` 目录以查找凭证
3.  为可用供应商注册执行器（Executors）
4.  在配置的端口上启动 HTTP 服务器
5.  开始监视配置更改

预期输出：

```
CLIProxyAPI Version: {version}, Commit: {commit}, BuiltAt: {date}
INFO[0000] CLIProxyAPI Version: {version}, Commit: {commit}, BuiltAt: {date}
INFO[0000] Server listening on :8080
```
**来源：** [internal/cmd/run.go27-56](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/run.go#L27-L56) [cmd/server/main.go478-480](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L478-L480)

### 步骤 5：发起您的第一个请求

使用兼容 OpenAI 的端点：

```
curl -X POST http://localhost:8080/v1/chat/completions \  -H "Content-Type: application/json" \  -d '{    "model": "gemini-2.0-flash-exp",    "messages": [      {"role": "user", "content": "Hello, world!"}    ]  }'
```
或者使用兼容 Gemini 的端点：

```
curl -X POST http://localhost:8080/v1beta/models/gemini-2.0-flash-exp:generateContent \  -H "Content-Type: application/json" \  -d '{    "contents": [      {"parts": [{"text": "Hello, world!"}]}    ]  }'
```
服务器将自动为请求的模型选择可用的凭证，并将请求翻译为相应的供应商格式。

**来源：** [internal/api](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/api)/

---

## 启动流程与服务初始化

> **[Mermaid sequence]**
> *(图表结构无法解析)*

**来源：** [cmd/server/main.go50-482](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L50-L482) [internal/cmd/run.go27-56](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/run.go#L27-L56)

---

## 身份验证与凭证流程

```mermaid
flowchart TD
    LoginCmd["Login Commands--login, --claude-login, etc."]
    OAuth["OAuth Flow"]
    Browser["Open Browser"]
    Callback["OAuth Callback"]
    TokenFile["Save Tokenauths/*.json"]
    Startup["Service.Run()"]
    ScanAuth["Scan auth_dir"]
    LoadTokens["Load *.json files"]
    Synthesize["Synthesize Auth Records"]
    RegisterAuth["Register with CoreManager"]
    Request["HTTP Request/v1/chat/completions"]
    SelectAuth["AuthSelectorRound-Robin/FillFirst"]
    Executor["Provider Executor"]
    APICall["API Call to Provider"]

    LoginCmd --> OAuth
    OAuth --> Browser
    Browser --> Callback
    Callback --> TokenFile
    Startup --> ScanAuth
    ScanAuth --> LoadTokens
    LoadTokens --> Synthesize
    Synthesize --> RegisterAuth
    Request --> SelectAuth
    SelectAuth --> Executor
    Executor --> APICall
    TokenFile --> ScanAuth
    RegisterAuth --> SelectAuth
```
**来源：** [internal/cmd/login.go51-183](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/login.go#L51-L183) [sdk/auth](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/auth)/

---

## 存储后端配置

服务器根据环境变量检测存储后端。一次只能有一个活动后端，优先级如下：

| 优先级 | 后端 | 环境变量 | 描述 |
| --- | --- | --- | --- |
| 1 | PostgreSQL | `PGSTORE_DSN` | 数据库连接字符串 |
| 2 | 对象存储 | `OBJECTSTORE_ENDPOINT` | S3/MinIO 端点 URL |
| 3 | Git | `GITSTORE_GIT_URL` | Git 仓库 URL |
| 4 | 文件 (File) | *(无)* | 本地文件系统（默认） |

### 文件存储（默认）

无需配置。服务器使用当前工作目录或 `config.yaml` 中的 `auth_dir`。

```
./cliproxy-api
```
配置位置：`./config.yaml`
认证位置：`./auths/*.json`

### PostgreSQL 存储

设置数据库连接字符串：

```
export PGSTORE_DSN="postgres://user:password@localhost:5432/cliproxy?sslmode=disable"export PGSTORE_LOCAL_PATH="/var/lib/cliproxy"  # 可选：本地脱机目录./cliproxy-api
```
服务器将：

1.  创建表：`config_store`、`auth_store`
2.  同步数据库 ↔ 本地脱机目录
3.  对基于文件的操作使用本地文件
4.  将更改持久化回数据库

配置位置：`{PGSTORE_LOCAL_PATH}/pgstore/config/config.yaml`
认证位置：`{PGSTORE_LOCAL_PATH}/pgstore/auths/*.json`

**来源：** [cmd/server/main.go166-255](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L166-L255) [internal/store/postgresstore.go49-100](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/store/postgresstore.go#L49-L100)

### Git 存储

设置仓库 URL 和凭证：

```
export GITSTORE_GIT_URL="https://github.com/user/cliproxy-config.git"export GITSTORE_GIT_USERNAME="git"export GITSTORE_GIT_TOKEN="ghp_xxxxxxxxxxxx"export GITSTORE_LOCAL_PATH="/var/lib/cliproxy"  # 可选./cliproxy-api
```
服务器将：

1.  克隆仓库（如果已存在则拉取最新内容）
2.  对操作使用本地克隆
3.  提交并强制推送更改
4.  将历史记录压缩为单个提交

配置位置：`{GITSTORE_LOCAL_PATH}/gitstore/config/config.yaml`
认证位置：`{GITSTORE_LOCAL_PATH}/gitstore/auths/*.json`

**来源：** [cmd/server/main.go186-366](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L186-L366) [internal/store/gitstore.go88-209](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/store/gitstore.go#L88-L209)

### 对象存储 (S3/MinIO)

设置兼容 S3 的端点：

```
export OBJECTSTORE_ENDPOINT="https://s3.amazonaws.com"export OBJECTSTORE_ACCESS_KEY="AKIAIOSFODNN7EXAMPLE"export OBJECTSTORE_SECRET_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"export OBJECTSTORE_BUCKET="cliproxy-config"export OBJECTSTORE_LOCAL_PATH="/var/lib/cliproxy"  # 可选./cliproxy-api
```
服务器将：

1.  连接到 S3/MinIO
2.  同步存储桶 ↔ 本地镜像
3.  对操作使用本地文件
4.  将更改上传到存储桶

配置位置：`{OBJECTSTORE_LOCAL_PATH}/objectstore/config.yaml`
认证位置：`{OBJECTSTORE_LOCAL_PATH}/objectstore/auths/*.json`

**来源：** [cmd/server/main.go199-323](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L199-L323) [internal/store/objectstore.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/store/objectstore.go)/

---

## 供应商身份验证示例

### Google Gemini (OAuth)

```
./cliproxy-api --login
```
交互式流程：

1.  浏览器打开进行 Google OAuth 认证
2.  选择 GCP 项目，或输入 `ALL` 以选择所有项目
3.  自动完成入职流程
4.  令牌保存到 `auths/gemini-{email}-{project}.json`

通过选择 `ALL` 或提供逗号分隔的列表，可以激活多个项目。

**来源：** [internal/cmd/login.go51-183](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/login.go#L51-L183) [cmd/server/main.go453-455](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L453-L455)

### Anthropic Claude (OAuth)

```
./cliproxy-api --claude-login
```
使用 PKCE OAuth 流程。令牌保存到 `auths/claude-{email}.json`。

**来源：** [cmd/server/main.go463-464](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L463-L464)

### OpenAI Codex (OAuth)

```
./cliproxy-api --codex-login
```
使用账户哈希进行识别。令牌保存到 `auths/codex-{hash}.json`。

**来源：** [cmd/server/main.go459-461](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L459-L461)

### Vertex AI (服务账户)

```
./cliproxy-api --vertex-import /path/to/service-account.json
```
导入 GCP 服务账户密钥。保存到 `auths/vertex-{project_id}.json`。

**来源：** [cmd/server/main.go450-452](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L450-L452)

### API 密钥配置

对于支持 API 密钥的供应商，直接将其添加到 `config.yaml` 中：

```
gemini_api_keys:  - "AIzaSy..."claude_api_keys:  - "sk-ant-..."codex_api_keys:  - "sk-..."
```
服务器在启动时会自动将这些合成（synthesize）为 `Auth` 记录。

**来源：** [internal/config](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/config)/

---

## 热重载与配置更新

服务器监视配置和身份验证文件的更改，并在不重启的情况下自动重新加载：

```mermaid
flowchart TD
    ConfigFile["config.yaml"]
    AuthFiles["auths/*.json"]
    Watcher["FileWatcher"]
    Debounce["Debounce Timer150ms config50ms auth"]
    ConfigReload["• Update logging• Update retry config• Rebind executors• Notify modules"]
    AuthReload["• Parse auth file• Register/update Auth• Register models"]

    ConfigFile --> Watcher
    AuthFiles --> Watcher
    Watcher --> Debounce
    Debounce --> ConfigReload
    Debounce --> AuthReload
```
更改会立即生效，且不会中断现有连接。

**来源：** [sdk/cliproxy](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/cliproxy)/

---

## 请求处理流程

> **[Mermaid sequence]**
> *(图表结构无法解析)*

**来源：** [internal/api](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/api)/

---

## 验证清单

完成快速入门后，验证您的部署：

-   [ ]  服务器启动且无错误
-   [ ]  配置文件已加载（检查日志中的配置路径）
-   [ ]  至少有一个供应商已通过身份验证（检查日志中的 "registered X auths"）
-   [ ]  HTTP 服务器正在监听（检查日志中的 "listening on :port"）
-   [ ]  测试请求成功完成
-   [ ]  文件观察器（File watcher）处于活动状态（修改配置，检查重新加载消息）

常见问题：

-   **端口已被占用**：更改 `config.yaml` 中的 `port`
-   **未找到认证（auths）**：为至少一个供应商运行 `--login` 或等效命令
-   **权限被拒绝**：确保对 `auth_dir` 和配置文件位置具有写入权限
-   **存储后端错误**：检查环境变量语法和连通性

**来源：** [internal/cmd/run.go27-56](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/run.go#L27-L56)

---

## 下一步

现在您已拥有一个正常运行的服务器：

1.  **配置其他供应商**：参阅[身份验证设置](/router-for-me/CLIProxyAPI/2.3-authentication-setup)了解特定供应商的指南
2.  **自定义配置**：参阅[初始配置](/router-for-me/CLIProxyAPI/2.2-initial-configuration)了解所有可用选项
3.  **设置模型映射**：参阅[模型映射与排除](/router-for-me/CLIProxyAPI/8.2-model-mapping-and-exclusion)以创建模型别名
4.  **启用高级功能**：参阅[高级功能](/router-for-me/CLIProxyAPI/8-advanced-features)了解思考配置、路由策略和监控
5.  **部署到生产环境**：参阅[云原生部署](/router-for-me/CLIProxyAPI/10.2-cloud-native-deployment)了解分布式部署

有关全面的 API 文档，请参阅[API 参考](/router-for-me/CLIProxyAPI/4-api-reference)。

**来源：** 以上所有部分
