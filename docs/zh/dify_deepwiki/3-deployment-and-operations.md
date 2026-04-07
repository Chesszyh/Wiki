# 部署和运维

相关源文件

-   [.github/workflows/api-tests.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/api-tests.yml)
-   [.github/workflows/autofix.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/autofix.yml)
-   [.github/workflows/build-push.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/build-push.yml)
-   [.github/workflows/db-migration-test.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/db-migration-test.yml)
-   [.github/workflows/deploy-agent-dev.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/deploy-agent-dev.yml)
-   [.github/workflows/deploy-dev.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/deploy-dev.yml)
-   [.github/workflows/deploy-hitl.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/deploy-hitl.yml)
-   [.github/workflows/docker-build.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/docker-build.yml)
-   [.github/workflows/main-ci.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/main-ci.yml)
-   [.github/workflows/stale.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/stale.yml)
-   [.github/workflows/style.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/style.yml)
-   [.github/workflows/tool-test-sdks.yaml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/tool-test-sdks.yaml)
-   [.github/workflows/translate-i18n-claude.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/translate-i18n-claude.yml)
-   [.github/workflows/trigger-i18n-sync.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/trigger-i18n-sync.yml)
-   [.github/workflows/vdb-tests.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/vdb-tests.yml)
-   [.github/workflows/web-tests.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/web-tests.yml)
-   [api/.env.example](https://github.com/langgenius/dify/blob/92dbc94f/api/.env.example)
-   [api/Dockerfile](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile)
-   [api/app.py](https://github.com/langgenius/dify/blob/92dbc94f/api/app.py)
-   [api/app_factory.py](https://github.com/langgenius/dify/blob/92dbc94f/api/app_factory.py)
-   [api/commands.py](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py)
-   [api/configs/feature/__init__.py](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py)
-   [api/configs/middleware/__init__.py](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/__init__.py)
-   [api/configs/packaging/__init__.py](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/packaging/__init__.py)
-   [api/controllers/console/datasets/datasets.py](https://github.com/langgenius/dify/blob/92dbc94f/api/controllers/console/datasets/datasets.py)
-   [api/core/rag/datasource/vdb/vector_factory.py](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_factory.py)
-   [api/core/rag/datasource/vdb/vector_type.py](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_type.py)
-   [api/extensions/ext_storage.py](https://github.com/langgenius/dify/blob/92dbc94f/api/extensions/ext_storage.py)
-   [api/extensions/storage/storage_type.py](https://github.com/langgenius/dify/blob/92dbc94f/api/extensions/storage/storage_type.py)
-   [api/migrations/README](https://github.com/langgenius/dify/blob/92dbc94f/api/migrations/README)
-   [api/pyproject.toml](https://github.com/langgenius/dify/blob/92dbc94f/api/pyproject.toml)
-   [api/tests/unit_tests/configs/test_dify_config.py](https://github.com/langgenius/dify/blob/92dbc94f/api/tests/unit_tests/configs/test_dify_config.py)
-   [api/uv.lock](https://github.com/langgenius/dify/blob/92dbc94f/api/uv.lock)
-   [dev/pytest/pytest_vdb.sh](https://github.com/langgenius/dify/blob/92dbc94f/dev/pytest/pytest_vdb.sh)
-   [docker/.env.example](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example)
-   [docker/docker-compose-template.yaml](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml)
-   [docker/docker-compose.middleware.yaml](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.middleware.yaml)
-   [docker/docker-compose.yaml](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml)
-   [docker/middleware.env.example](https://github.com/langgenius/dify/blob/92dbc94f/docker/middleware.env.example)
-   [web/.nvmrc](https://github.com/langgenius/dify/blob/92dbc94f/web/.nvmrc)
-   [web/Dockerfile](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile)
-   [web/README.md](https://github.com/langgenius/dify/blob/92dbc94f/web/README.md)
-   [web/i18n-config/README.md](https://github.com/langgenius/dify/blob/92dbc94f/web/i18n-config/README.md)
-   [web/package.json](https://github.com/langgenius/dify/blob/92dbc94f/web/package.json)

本文档描述了在生产或开发环境中运行 Dify 的部署架构、容器编排、环境配置以及运维注意事项。涵盖了 Docker 镜像构建、服务依赖、配置管理和启动程序。

有关整体系统架构和服务拓扑的信息，请参阅[系统架构概览](/langgenius/dify/2-system-architecture-overview)。有关配置模型和 Pydantic 设置的详细信息，请参阅[配置系统](/langgenius/dify/2.3-application-types-and-execution-modes)。

## Docker 构建流程和多架构镜像

Dify 使用多阶段 Docker 构建来为 API 后端和 Web 前端服务创建优化的生产镜像。构建过程通过 GitHub Actions CI/CD 管道进行编排。

### API 服务多阶段构建

API 服务使用 [api/Dockerfile1-122](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L1-L122) 中定义的三个阶段构建：

**阶段 1: 基础镜像设置** ([api/Dockerfile1-10](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L1-L10)):

-   基础镜像: `python:3.12-slim-bookworm`
-   安装 `uv` 包管理器版本 0.8.9
-   设置工作目录为 `/app/api`

**阶段 2: 依赖安装** ([api/Dockerfile12-26](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L12-L26)):

-   安装系统依赖: `g++`, `libmpfr-dev`, `libmpc-dev` (用于构建 `gmpy2`)
-   复制 `pyproject.toml` 和 `uv.lock`
-   运行 `uv sync --locked --no-dev` 安装生产依赖
-   在 `/app/api/.venv` 创建虚拟环境

**阶段 3: 生产镜像** ([api/Dockerfile28-122](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L28-L122)):

-   创建非 root 用户 `dify`, UID 为 1001
-   安装运行时依赖:
    -   来自 NodeSource 仓库的 Node.js 22.x
    -   系统库: `libgmp-dev`, `libmpfr-dev`, `libmpc-dev`
    -   字体: `fonts-noto-cjk` 用于 PDF 渲染
    -   `libmagic1` 用于 MIME 类型检测
    -   `media-types` 包用于文件扩展名映射
-   下载 NLTK 数据到 `/usr/local/share/nltk_data`
-   预缓存 Tiktoken 编码到 `.tiktoken_cache`
-   复制应用程序代码到 `/app/api/`
-   设置入口点为 `/entrypoint.sh`

**构建架构图：**

```mermaid
flowchart TD
    Base["FROM python:3.12-slim-bookworm AS baseWORKDIR /app/api"]
    UVInstall["RUN pip install uv==0.8.9"]
    Packages["FROM base AS packages"]
    SysDeps["RUN apt-get install g++ libmpfr-dev libmpc-dev"]
    CopyLock["COPY pyproject.toml uv.lock ./"]
    UVSync["RUN uv sync --locked --no-dev"]
    VEnv["Creates .venv/ with dependencies"]
    Production["FROM base AS production"]
    CreateUser["RUN groupadd/useradd dify:1001"]
    InstallRuntime["RUN apt-get install nodejs libgmp-devfonts-noto-cjk libmagic1 media-types"]
    CopyVEnv["COPY --from=packages .venv/ .venv/"]
    DownloadNLTK["RUN python -c 'import nltk; nltk.download()'"]
    CacheTiktoken["RUN python -c 'import tiktoken'"]
    CopyCode["COPY --chown=dify:dify . /app/api/"]
    SetEntrypoint["ENTRYPOINT /entrypoint.sh"]

    Base --> UVInstall
    UVInstall --> Packages
    Packages --> SysDeps
    SysDeps --> CopyLock
    CopyLock --> UVSync
    UVSync --> VEnv
    VEnv --> Production
    Production --> CreateUser
    CreateUser --> InstallRuntime
    InstallRuntime --> CopyVEnv
    CopyVEnv --> DownloadNLTK
    DownloadNLTK --> CacheTiktoken
    CacheTiktoken --> CopyCode
    CopyCode --> SetEntrypoint
```
**来源：** [api/Dockerfile1-122](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L1-L122)

关键构建优化：

-   多阶段构建通过排除构建工具减少最终镜像大小
-   `uv sync --locked` 确保可重现的构建
-   预下载 NLTK 和 Tiktoken 数据避免运行时下载
-   非 root 用户 `dify:1001` 提高安全性
-   构建参数 `COMMIT_SHA` 用于版本跟踪

**来源：** [api/Dockerfile1-122](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L1-L122)

API 镜像的关键方面：

| 方面 | 配置 | 位置 |
| --- | --- | --- |
| 基础镜像 | `python:3.12-slim-bookworm` | [api/Dockerfile2](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L2-L2) |
| 包管理器 | `uv` 版本 0.8.9 | [api/Dockerfile7-9](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L7-L9) |
| 依赖项 | 定义在 `pyproject.toml`, 锁定在 `uv.lock` | [api/pyproject.toml1-230](https://github.com/langgenius/dify/blob/92dbc94f/api/pyproject.toml#L1-L230) [api/uv.lock1-105](https://github.com/langgenius/dify/blob/92dbc94f/api/uv.lock#L1-L105) |
| 用户 | 非 root 用户 `dify`, UID 1001 | [api/Dockerfile52-55](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L52-L55) |
| 入口点 | `/entrypoint.sh` | [api/Dockerfile103](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L103-L103) |
| 工作目录 | `/app/api` | [api/Dockerfile49](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L49-L49) |
| 暴露端口 | 5001 | [api/Dockerfile39](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L39-L39) |

构建过程使用 `uv sync --locked --no-dev` 安装生产依赖项而不包含开发包，确保最小的镜像大小。NLTK 数据和 Tiktoken 缓存在构建期间预下载，以避免运行时下载。

**来源：** [api/Dockerfile1-104](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L1-L104) [api/pyproject.toml1-230](https://github.com/langgenius/dify/blob/92dbc94f/api/pyproject.toml#L1-L230)

### Web 服务多阶段构建

Web 服务使用 [web/Dockerfile1-87](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L1-L87) 中定义的四阶段构建：

**阶段 1: 基础镜像设置** ([web/Dockerfile1-16](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L1-L16)):

-   基础镜像: `node:24-alpine`
-   启用 `corepack` 用于 pnpm 管理
-   安装 `tzdata` 用于时区支持
-   配置 `PNPM_HOME` 并添加到 `PATH`

**阶段 2: 包安装** ([web/Dockerfile19-29](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L19-L29)):

-   复制 `package.json` 和 `pnpm-lock.yaml`
-   运行 `corepack install` 使用 `package.json` 中确切的 pnpm 版本
-   执行 `pnpm install --frozen-lockfile` 进行可重现构建

**阶段 3: 构建** ([web/Dockerfile32-38](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L32-L38)):

-   复制所有源代码
-   设置 `NODE_OPTIONS="--max-old-space-size=4096"` 用于大型构建
-   运行 `pnpm build:docker`，执行：
    -   `next build` 使用 standalone 输出模式 ([web/package.json28](https://github.com/langgenius/dify/blob/92dbc94f/web/package.json#L28-L28))
    -   `optimize-standalone.js` 脚本减少输出大小 ([web/scripts/optimize-standalone.js](https://github.com/langgenius/dify/blob/92dbc94f/web/scripts/optimize-standalone.js))

**阶段 4: 生产** ([web/Dockerfile41-87](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L41-L87)):

-   创建非 root 用户 `dify:1001`
-   全局安装 PM2: `pnpm add -g pm2`
-   复制构建产物:
    -   `.next/standalone/` - 自包含服务器
    -   `.next/static/` - 静态资源
    -   `public/` - 公共文件
-   设置入口点为 `entrypoint.sh`

**构建架构图：**

```mermaid
flowchart TD
    Base["FROM node:24-alpine AS baseRUN corepack enable"]
    SetPNPM["ENV PNPM_HOME=/pnpmENV PATH=$PNPM_HOME:$PATH"]
    Packages["FROM base AS packagesWORKDIR /app/web"]
    CopyPackageJSON["COPY package.json pnpm-lock.yaml"]
    CorepackInstall["RUN corepack install"]
    PNPMInstall["RUN pnpm install --frozen-lockfile"]
    Builder["FROM base AS builderWORKDIR /app/web"]
    CopyFromPackages["COPY --from=packages /app/web/"]
    CopySource["COPY . ."]
    SetNodeOpts["ENV NODE_OPTIONS=--max-old-space-size=4096"]
    PNPMBuild["RUN pnpm build:docker"]
    Production["FROM base AS production"]
    SetEnvVars["ENV NODE_ENV=productionENV EDITION=SELF_HOSTEDENV PM2_INSTANCES=2"]
    CreateDifyUser["RUN adduser -S -u 1001 dify"]
    InstallPM2["RUN pnpm add -g pm2"]
    CopyStandalone["COPY --from=builder --chown=dify:dify.next/standalone/"]
    CopyStatic["COPY --from=builder --chown=dify:dify.next/static/ .next/static/"]
    CopyPublic["COPY --from=builder --chown=dify:difypublic/ public/"]
    CopyEntrypoint["COPY --chown=dify:dify entrypoint.sh"]

    Base --> SetPNPM
    SetPNPM --> Packages
    Packages --> CopyPackageJSON
    CopyPackageJSON --> CorepackInstall
    CorepackInstall --> PNPMInstall
    PNPMInstall --> Builder
    Builder --> CopyFromPackages
    CopyFromPackages --> CopySource
    CopySource --> SetNodeOpts
    SetNodeOpts --> PNPMBuild
    PNPMBuild --> Production
    Production --> SetEnvVars
    SetEnvVars --> CreateDifyUser
    CreateDifyUser --> InstallPM2
    InstallPM2 --> CopyStandalone
    CopyStandalone --> CopyStatic
    CopyStatic --> CopyPublic
    CopyPublic --> CopyEntrypoint
```
**来源：** [web/Dockerfile1-87](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L1-L87) [web/package.json1-289](https://github.com/langgenius/dify/blob/92dbc94f/web/package.json#L1-L289)

**Next.js Standalone 输出：**

构建使用 `next.config.js` 中配置的 Next.js standalone 输出模式：

```javascript
output: 'standalone'
```
这创建了一个仅包含必要依赖项的最小生产服务器包，显著减少了部署大小。`optimize-standalone.js` 脚本进一步删除了不必要的文件。

**来源：** [web/Dockerfile1-87](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L1-L87) [web/package.json28](https://github.com/langgenius/dify/blob/92dbc94f/web/package.json#L28-L28)

### 多架构构建管道

CI/CD 管道使用 GitHub Actions 为 `amd64` 和 `arm64` 架构构建镜像。

**构建矩阵** ([.github/workflows/build-push.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/build-push.yml):

```mermaid
flowchart TD
    Trigger["Push to main/deploy/or tag"]
    BuildAPI["Build API Imageplatforms: linux/amd64,linux/arm64buildx with QEMU"]
    BuildWeb["Build Web Imageplatforms: linux/amd64,linux/arm64buildx with QEMU"]
    PushRegistry["Push to DockerHublanggenius/dify-api:taglanggenius/dify-web:tag"]

    Trigger --> BuildAPI
    Trigger --> BuildWeb
    BuildAPI --> PushRegistry
    BuildWeb --> PushRegistry
```
**来源：** [.github/workflows/build-push.yml1-100](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/build-push.yml#L1-L100)

构建过程使用：

-   `docker/setup-buildx-action` 用于 BuildKit
-   `docker/setup-qemu-action` 用于跨平台构建
-   从 Git SHA 注入的构建参数 `COMMIT_SHA`
-   使用 `pyproject.toml` 和 `package.json` 中的版本打标签

**来源：** [.github/workflows/build-push.yml1-150](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/build-push.yml#L1-L150)

## 使用 Docker Compose 进行服务编排

Dify 使用 Docker Compose 编排多个服务，具有依赖管理、健康检查和基于 Profile 的条件部署功能。

### 服务拓扑与依赖

```mermaid
flowchart TD
    InitPerms["init_permissionsbusybox:latestFixes volume permissions"]
    DBPostgres["db_postgrespostgres:15-alpineProfile: postgresqlPort: 5432Health: pg_isready"]
    DBMySQL["db_mysqlmysql:8.0Profile: mysqlPort: 3306Health: mysqladmin ping"]
    Redis["redisredis:6-alpinePort: 6379Health: redis-cli ping"]
    API["apilanggenius/dify-api:1.11.1MODE=apiPort: 5001"]
    Worker["workerlanggenius/dify-api:1.11.1MODE=workerCelery all queues"]
    WorkerBeat["worker_beatlanggenius/dify-api:1.11.1MODE=beatCelery scheduler"]
    Web["weblanggenius/dify-web:1.11.1Port: 3000"]
    Sandbox["sandboxlanggenius/dify-sandbox:0.2.12Port: 8194Code execution"]
    PluginDaemon["plugin_daemonlanggenius/dify-plugin-daemon:0.5.1-localPort: 5002Go service"]
    SSRFProxy["ssrf_proxyubuntu/squid:latestPort: 3128Security proxy"]
    Nginx["nginxnginx:latestReverse proxy"]

    InitPerms --> API
    InitPerms --> Worker
    InitPerms --> WorkerBeat
    DBPostgres --> API
    DBPostgres --> Worker
    DBPostgres --> WorkerBeat
    DBMySQL --> API
    DBMySQL --> Worker
    Redis --> API
    Redis --> Worker
    Redis --> WorkerBeat
    API --> PluginDaemon
    Worker --> Sandbox
    Nginx --> API
    Nginx --> Web
    Sandbox --> SSRFProxy
```
**来源：** [docker/docker-compose-template.yaml1-320](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L1-L320) [docker/docker-compose.yaml1-850](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml#L1-L850)

### 服务配置详情

**API 服务** ([docker/docker-compose-template.yaml22-61](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L22-L61)):

-   镜像: `langgenius/dify-api:1.11.1`
-   环境: `MODE=api` 启动 Flask/Gunicorn 服务器
-   依赖于: `init_permissions` (完成), 数据库 (健康), Redis (启动)
-   卷: `./volumes/app/storage:/app/api/storage` 用于文件存储
-   网络: `ssrf_proxy_network`, `default`

**Worker 服务** ([docker/docker-compose-template.yaml64-100](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L64-L100)):

-   镜像: `langgenius/dify-api:1.11.1` (与 API 相同)
-   环境: `MODE=worker` 启动 Celery workers
-   队列: dataset, workflow, mail, ops_trace, app_deletion, plugin, 等
-   与 API 服务相同的依赖和卷

**Worker Beat 服务** ([docker/docker-compose-template.yaml103-131](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L103-L131)):

-   镜像: `langgenius/dify-api:1.11.1` (与 API 相同)
-   环境: `MODE=beat` 启动 Celery beat 调度器
-   管理周期性任务，如插件升级、工作流调度

**Web 服务** ([docker/docker-compose-template.yaml133-160](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L133-L160)):

-   镜像: `langgenius/dify-web:1.11.1`
-   用于 API URL、市场、功能标志的环境变量
-   无数据库依赖（无状态前端）

**来源：** [docker/docker-compose-template.yaml1-320](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L1-L320)

### Docker Compose Profiles

Profiles 允许基于数据库和向量存储的选择进行条件服务部署：

| Profile | 服务 | 用途 |
| --- | --- | --- |
| `postgresql` | `db_postgres` | 使用 PostgreSQL 作为元数据数据库 |
| `mysql` | `db_mysql` | 使用 MySQL 作为元数据数据库 |
| `weaviate` | `weaviate` | 使用 Weaviate 作为向量数据库 |
| `qdrant` | `qdrant` | 使用 Qdrant 作为向量数据库 |
| `chroma` | `chroma` | 使用 Chroma 作为向量数据库 |
| `pgvector` | `pgvector` | 使用 PGVector 作为向量数据库 |
| `opensearch` | `opensearch` | 使用 OpenSearch 作为向量数据库 |
| `oceanbase` | `oceanbase` | 使用 OceanBase 作为数据库 |

使用示例：

```bash
docker compose --profile postgresql --profile weaviate up -d
```
**来源：** [docker/docker-compose.middleware.yaml1-200](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.middleware.yaml#L1-L200) [api/README.md15-20](https://github.com/langgenius/dify/blob/92dbc94f/api/README.md#L15-L20)

### 健康检查

服务包含健康检查以确保正确的启动顺序：

**PostgreSQL** ([docker/docker-compose-template.yaml183-197](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L183-L197)):

```yaml
healthcheck:
  test: ["CMD", "pg_isready", "-h", "db_postgres", "-U", "postgres", "-d", "dify"]
  interval: 1s
  timeout: 3s
  retries: 60
```
**MySQL** ([docker/docker-compose-template.yaml216-227](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L216-L227)):

```yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-u", "root", "-p${DB_PASSWORD}"]
  interval: 1s
  timeout: 3s
  retries: 30
```
**Redis** ([docker/docker-compose-template.yaml240-245](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L240-L245)):

```yaml
healthcheck:
  test: ["CMD-SHELL", "redis-cli -a ${REDIS_PASSWORD} ping | grep -q PONG"]
```
**Sandbox** ([docker/docker-compose-template.yaml267](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L267-L267)):

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8194/health"]
```
带有 `condition: service_healthy` 的 `depends_on` 配置确保服务在启动前等待依赖项完全运行。

**来源：** [docker/docker-compose-template.yaml183-267](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L183-L267)

## 环境配置和运行时模式

Dify 使用分层配置系统，并通过 Pydantic 设置模型验证环境变量。

### 配置加载流程

```mermaid
flowchart TD
    EnvExample["docker/.env.exampleTemplate with 650+ variables"]
    UserEnv["docker/.envUser configuration"]
    OSEnv["OS Environment VariablesOverride .env values"]
    SharedEnvAnchor["x-shared-env anchordocker-compose.yaml:7Common API/worker config"]
    APIService["api serviceMODE=api"]
    WorkerService["worker serviceMODE=worker"]
    BeatService["worker_beat serviceMODE=beat"]
    DifyConfig["DifyConfig classapi/configs/app_config.pyPydantic BaseSettings"]
    FeatureConfig["SecurityConfigAppExecutionConfigCodeExecutionSandboxConfigPluginConfigetc."]
    MiddlewareConfig["StorageConfigVectorStoreConfigDatabaseConfigRedisConfigCeleryConfig"]
    FlaskConfig["app.config.from_mapping()app_factory.py:24"]
    RuntimeAccess["Runtime: dify_config.SECRET_KEYdify_config.DB_HOSTetc."]

    EnvExample --> UserEnv
    UserEnv --> SharedEnvAnchor
    OSEnv --> SharedEnvAnchor
    SharedEnvAnchor --> APIService
    SharedEnvAnchor --> WorkerService
    SharedEnvAnchor --> BeatService
    APIService --> DifyConfig
    WorkerService --> DifyConfig
    BeatService --> DifyConfig
    DifyConfig --> FeatureConfig
    DifyConfig --> MiddlewareConfig
    FeatureConfig --> FlaskConfig
    MiddlewareConfig --> FlaskConfig
    DifyConfig --> RuntimeAccess
```
**来源：** [docker/docker-compose.yaml1-850](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml#L1-L850) [docker/.env.example1-1000](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L1-L1000) [api/configs/app_config.py1-50](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/app_config.py#L1-L50) [api/app_factory.py18-25](https://github.com/langgenius/dify/blob/92dbc94f/api/app_factory.py#L18-L25)

### 运行时模式选择

API 服务容器根据 `MODE` 环境变量在不同模式下运行：

**模式配置表：**

| 模式 | 环境变量 | 进程 | 用途 |
| --- | --- | --- | --- |
| `api` | `MODE=api` | Gunicorn with Flask app | HTTP API 服务器 |
| `worker` | `MODE=worker` | Celery worker | 后台任务处理 |
| `beat` | `MODE=beat` | Celery beat | 周期性任务调度 |
| `migration` | `MODE=migration` | Flask-Migrate | 仅数据库迁移 |

**入口点模式选择** ([docker/entrypoint.sh1-100](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L1-L100)):

```mermaid
flowchart TD
    Entrypoint["#!/bin/bash /entrypoint.sh"]
    CheckMigration["MIGRATION_ENABLED== 'true'?"]
    RunMigration["flask upgrade-dbAlembic migrations"]
    CheckMode["MODE value?"]
    ModeAPI["MODE=apiexec gunicorn--config gunicorn.conf.py--bind 0.0.0.0:5001--workers $SERVER_WORKER_AMOUNT--worker-class $SERVER_WORKER_CLASSapp:app"]
    ModeWorker["MODE=worker"]
    CheckAutoscale["CELERY_AUTO_SCALE== 'true'?"]
    WorkerFixed["exec celery -A app.celery worker-P $CELERY_WORKER_CLASS-c $CELERY_WORKER_AMOUNT--queues dataset,workflow,..."]
    WorkerAutoscale["exec celery -A app.celery worker--autoscale=$MAX,$MIN--queues dataset,workflow,..."]
    ModeBeat["MODE=beatexec celery -A app.celery beat"]
    ModeMigration["MODE=migrationexit 0"]

    Entrypoint --> CheckMigration
    CheckMigration --> RunMigration
    CheckMigration --> CheckMode
    RunMigration --> CheckMode
    CheckMode --> ModeAPI
    CheckMode --> ModeWorker
    CheckMode --> ModeBeat
    CheckMode --> ModeMigration
    ModeWorker --> CheckAutoscale
    CheckAutoscale --> WorkerAutoscale
    CheckAutoscale --> WorkerFixed
```
**来源：** [docker/entrypoint.sh1-100](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L1-L100)

### Gunicorn 服务器配置 (MODE=api)

**关键环境变量：**

| 变量 | 默认值 | 描述 |
| --- | --- | --- |
| `DIFY_BIND_ADDRESS` | `0.0.0.0` | API 服务器绑定地址 |
| `DIFY_PORT` | `5001` | HTTP 端口 |
| `SERVER_WORKER_AMOUNT` | `1` | Gunicorn worker 数量 |
| `SERVER_WORKER_CLASS` | `gevent` | Worker 类 (gevent/sync/solo) |
| `SERVER_WORKER_CONNECTIONS` | `10` | 每个 worker 的最大连接数 |
| `GUNICORN_TIMEOUT` | `360` | 请求超时时间（秒） |

**Worker 类选择：**

-   `gevent`: 基于 greenlet 的异步 worker（默认，推荐用于 I/O 密集型）
-   `sync`: 同步 worker（用于 CPU 密集型任务）
-   `solo`: 单线程 worker（用于 Windows 调试）

**Gunicorn 配置文件** ([api/gunicorn.conf.py](https://github.com/langgenius/dify/blob/92dbc94f/api/gunicorn.conf.py)):

当使用 `gevent` worker 类时，配置会应用 monkey patching：

```python
if worker_class == 'gevent':
    from gevent import monkey
    monkey.patch_all()
    # Patch psycopg2 for PostgreSQL async support
    from psycopg2.extensions import set_wait_callback
```
**来源：** [docker/.env.example144-182](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L144-L182) [docker/entrypoint.sh60-70](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L60-L70) [api/gunicorn.conf.py1-50](https://github.com/langgenius/dify/blob/92dbc94f/api/gunicorn.conf.py#L1-L50)

### Celery Worker 配置 (MODE=worker)

**队列架构：**

```mermaid
flowchart TD
    RedisBroker["Redis BrokerDB 1CELERY_BROKER_URL"]
    WorkerProcess["Celery Worker Processcelery -A app.celery worker"]
    DatasetQueue["dataset queueDocument indexing"]
    PriorityDatasetQueue["priority_dataset queueHigh-priority indexing"]
    WorkflowQueue["workflow queueWorkflow execution"]
    PipelineQueue["pipeline queuePipeline tasks"]
    PriorityPipelineQueue["priority_pipeline queueHigh-priority pipeline"]
    MailQueue["mail queueEmail notifications"]
    PluginQueue["plugin queuePlugin operations"]
    AppDeletionQueue["app_deletion queueApplication cleanup"]
    OpsTraceQueue["ops_trace queueOperational tracing"]
    ConversationQueue["conversation queueConversation processing"]
    WorkflowStorageQueue["workflow_storage queueWorkflow storage operations"]
    SchedulePollerQueue["schedule_poller queueScheduled workflow polling"]
    ScheduleExecutorQueue["schedule_executor queueScheduled workflow execution"]
    TriggerWorkflowQueue["triggered_workflow_dispatcher queueTrigger-based dispatch"]
    TriggerRefreshQueue["trigger_refresh_executor queueTrigger refresh"]
    RetentionQueue["retention queueData retention cleanup"]

    RedisBroker --> WorkerProcess
    WorkerProcess --> DatasetQueue
    WorkerProcess --> PriorityDatasetQueue
    WorkerProcess --> WorkflowQueue
    WorkerProcess --> PipelineQueue
    WorkerProcess --> PriorityPipelineQueue
    WorkerProcess --> MailQueue
    WorkerProcess --> PluginQueue
    WorkerProcess --> AppDeletionQueue
    WorkerProcess --> OpsTraceQueue
    WorkerProcess --> ConversationQueue
    WorkerProcess --> WorkflowStorageQueue
    WorkerProcess --> SchedulePollerQueue
    WorkerProcess --> ScheduleExecutorQueue
    WorkerProcess --> TriggerDispatchQueue
    WorkerProcess --> TriggerRefreshQueue
    WorkerProcess --> RetentionQueue
```
**来源：** [docker/entrypoint.sh20-58](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L20-L58)

**自动缩放配置：**

当 `CELERY_AUTO_SCALE=true`:

| 变量 | 默认值 | 描述 |
| --- | --- | --- |
| `CELERY_MAX_WORKERS` | `nproc` | 最大 workers（扩展至 CPU 核心数） |
| `CELERY_MIN_WORKERS` | `1` | 最小 workers（基准容量） |

命令: `celery -A app.celery worker --autoscale=${MAX},${MIN}`

当 `CELERY_AUTO_SCALE=false`:

| 变量 | 默认值 | 描述 |
| --- | --- | --- |
| `CELERY_WORKER_AMOUNT` | `1` | 固定 workers 数量 |
| `CELERY_WORKER_CLASS` | (空) | Worker 实现（空=gevent） |

命令: `celery -A app.celery worker -P ${CLASS} -c ${AMOUNT}`

**来源：** [docker/.env.example184-212](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L184-L212) [docker/entrypoint.sh20-58](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L20-L58)

### Celery Beat 配置 (MODE=beat)

**Celery Beat 调度器** ([docker/entrypoint.sh67-70](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L67-L70)):

Beat 调度器管理在 [api/schedule/schedule.py](https://github.com/langgenius/dify/blob/92dbc94f/api/schedule/schedule.py) 中定义的周期性任务：

**计划任务：**

-   `check_upgradable_plugin_task`: 每 15 分钟检查一次插件更新
-   `workflow_schedule_poller_task`: 轮询计划的工作流（间隔可配置）
-   `clean_embedding_cache_task`: 清理嵌入缓存（可选）
-   `clean_unused_datasets_task`: 删除未使用的数据库（可选）
-   `clean_messages_task`: 清理旧消息（可选）
-   `workflow_run_cleanup_task`: 清理旧工作流运行（可选）

**配置变量：**

| 变量 | 默认值 | 描述 |
| --- | --- | --- |
| `ENABLE_CHECK_UPGRADABLE_PLUGIN_TASK` | `true` | 启用插件更新检查 |
| `ENABLE_WORKFLOW_SCHEDULE_POLLER_TASK` | `true` | 启用工作流调度 |
| `WORKFLOW_SCHEDULE_POLLER_INTERVAL` | `1` | 轮询间隔（分钟） |
| `WORKFLOW_SCHEDULE_POLLER_BATCH_SIZE` | `100` | 每次轮询的工作流数量 |
| `WORKFLOW_SCHEDULE_MAX_DISPATCH_PER_TICK` | `0` | 每次最大调度数（0=无限制） |

**来源：** [docker/.env.example583-603](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L583-L603) [api/.env.example583-603](https://github.com/langgenius/dify/blob/92dbc94f/api/.env.example#L583-L603) [docker/entrypoint.sh67-70](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L67-L70)

### 环境变量分类

配置系统将环境变量分为逻辑类别：

**1. 服务 URL 和端点** ([docker/.env.example8-59](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L8-L59)):

-   `CONSOLE_API_URL`: 控制台 API 的后端 URL
-   `CONSOLE_WEB_URL`: 控制台 Web 的前端 URL
-   `SERVICE_API_URL`: 向用户显示的服务 API URL
-   `APP_WEB_URL`: WebApp URL
-   `FILES_URL`: 文件访问 URL（签名，有过期时间）
-   `INTERNAL_FILES_URL`: 插件守护进程的内部文件访问

**2. 数据库配置** ([docker/.env.example232-326](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L232-L326)):

```yaml
DB_TYPE=postgresql  # or mysql
DB_USERNAME=postgres
DB_PASSWORD=difyai123456
DB_HOST=db_postgres
DB_PORT=5432
DB_DATABASE=dify

# Connection pooling
SQLALCHEMY_POOL_SIZE=30
SQLALCHEMY_MAX_OVERFLOW=10
SQLALCHEMY_POOL_RECYCLE=3600
SQLALCHEMY_POOL_TIMEOUT=30
```
**3. Redis 配置** ([docker/.env.example330-384](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L330-L384)):

```yaml
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=difyai123456
REDIS_DB=0

# Sentinel mode (optional)
REDIS_USE_SENTINEL=false
REDIS_SENTINELS=
REDIS_SENTINEL_SERVICE_NAME=

# Cluster mode (optional)
REDIS_USE_CLUSTERS=false
REDIS_CLUSTERS=
```
**4. 存储后端选择** ([docker/.env.example406-514](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L406-L514)):

```yaml
STORAGE_TYPE=opendal  # or s3, azure-blob, aliyun-oss, etc.

# OpenDAL configuration
OPENDAL_SCHEME=fs
OPENDAL_FS_ROOT=storage

# S3 configuration
S3_ENDPOINT=
S3_BUCKET_NAME=difyai
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_USE_AWS_MANAGED_IAM=false
```
支持的存储类型: `opendal`, `s3`, `aliyun-oss`, `azure-blob`, `baidu-obs`, `clickzetta-volume`, `google-storage`, `huawei-obs`, `oci-storage`, `tencent-cos`, `volcengine-tos`, `supabase`

**5. 向量数据库选择** ([docker/.env.example520-522](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L520-L522)):

```yaml
VECTOR_STORE=weaviate  # 30+ options supported
VECTOR_INDEX_NAME_PREFIX=Vector_index
```
支持的向量存储: `weaviate`, `oceanbase`, `qdrant`, `milvus`, `myscale`, `relyt`, `pgvector`, `pgvecto-rs`, `chroma`, `opensearch`, `oracle`, `tencent`, `elasticsearch`, `analyticdb`, `couchbase`, `vikingdb`, `opengauss`, `tablestore`, `vastbase`, `tidb`, `tidb_on_qdrant`, `baidu`, `lindorm`, `huawei_cloud`, `upstash`, `matrixone`, `clickzetta`, `alibabacloud_mysql`, `iris`

**来源：** [docker/.env.example1-1000](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L1-L1000) [api/.env.example1-700](https://github.com/langgenius/dify/blob/92dbc94f/api/.env.example#L1-L700)

### Pydantic 配置模型

配置被加载到 Pydantic 模型中以进行验证和类型安全检查。

**DifyConfig 组合** ([api/configs/app_config.py10-43](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/app_config.py#L10-L43)):

```python
class DifyConfig(
    # Packaging information
    PackagingInfo,

    # Feature configurations
    SecurityConfig,
    AppExecutionConfig,
    CodeExecutionSandboxConfig,
    TriggerConfig,
    AsyncWorkflowConfig,
    PluginConfig,
    MarketplaceConfig,
    EndpointConfig,
    FileAccessConfig,
    HttpConfig,
    InnerAPIConfig,
    ModelLoadBalanceConfig,
    BillingConfig,
    ToolConfig,
    MailConfig,
    WorkflowConfig,
    DatasetConfig,

    # Middleware configurations
    StorageConfig,
    VectorStoreConfig,
    KeywordStoreConfig,
    DatabaseConfig,
    RedisConfig,
    CeleryConfig,
    CORSConfig,
    WorkflowNodeExecutionConfig,
    IndexingConfig,

    # Deployment configurations
    DeploymentConfig,
    ServerConfig,

    # Logging configuration
    LoggingConfig,

    BaseSettings,
):
    pass
```
**关键配置类：**

**SecurityConfig** ([api/configs/feature/__init__.py19-65](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L19-L65)):

-   `SECRET_KEY`: 会话 cookie 签名密钥（使用 `openssl rand -base64 42` 生成）
-   `RESET_PASSWORD_TOKEN_EXPIRY_MINUTES`: 密码重置令牌 TTL（默认：5）
-   `LOGIN_DISABLED`: 禁用登录检查（默认：false）
-   `ADMIN_API_KEY_ENABLE`: 启用管理员 API 密钥认证（默认：false）

**CodeExecutionSandboxConfig** ([api/configs/feature/__init__.py86-174](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L86-L174)):

-   `CODE_EXECUTION_ENDPOINT`: 沙箱服务 URL（默认：`http://sandbox:8194`）
-   `CODE_EXECUTION_API_KEY`: 沙箱 API 密钥（默认：`dify-sandbox`）
-   `CODE_EXECUTION_CONNECT_TIMEOUT`: 连接超时（默认：10.0s）
-   `CODE_EXECUTION_READ_TIMEOUT`: 读取超时（默认：60.0s）
-   `CODE_EXECUTION_POOL_MAX_CONNECTIONS`: 最大连接数（默认：100）
-   `CODE_MAX_STRING_LENGTH`: 最大字符串长度（默认：400000）
-   `CODE_MAX_NUMBER`: 最大数值（默认：9223372036854775807）

**PluginConfig** ([api/configs/feature/__init__.py204-245](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L204-L245)):

-   `PLUGIN_DAEMON_URL`: 插件守护进程 URL（默认：`http://localhost:5002`）
-   `PLUGIN_DAEMON_KEY`: 插件守护进程认证密钥
-   `PLUGIN_DAEMON_TIMEOUT`: 请求超时（默认：600.0s）
-   `INNER_API_KEY_FOR_PLUGIN`: 插件回调的内部 API 密钥
-   `PLUGIN_MAX_PACKAGE_SIZE`: 最大插件包大小（字节）（默认：15728640）

**来源：** [api/configs/app_config.py10-43](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/app_config.py#L10-L43) [api/configs/feature/__init__.py1-600](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L1-L600)

### 配置验证示例

**字段验证：**

```python
# PositiveInt ensures value > 0
APP_MAX_EXECUTION_TIME: PositiveInt = Field(
    description="Maximum allowed execution time for application in seconds",
    default=1200,
)

# HttpUrl validates URL format
CODE_EXECUTION_ENDPOINT: HttpUrl = Field(
    description="URL endpoint for code execution service",
    default=HttpUrl("http://sandbox:8194"),
)

# NonNegativeInt ensures value >= 0
APP_DEFAULT_ACTIVE_REQUESTS: NonNegativeInt = Field(
    description="Default concurrent active requests (0 for unlimited)",
    default=0,
)
```
**计算字段：**

某些配置值是根据其他字段或环境计算得出的：

```python
@computed_field
@property
def SQLALCHEMY_DATABASE_URI_SCHEME(self) -> str:
    if self.DB_TYPE == "mysql":
        return "mysql+aiomysql"
    return "postgresql+psycopg2"
```
**来源：** [api/configs/feature/__init__.py67-84](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L67-L84) [api/configs/middleware/__init__.py50-150](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/__init__.py#L50-L150)

### 配置验证

Pydantic 模型提供自动验证：

```python
# SecurityConfig
SECRET_KEY: str = Field(
    description="Secret key for secure session cookie signing",
    default="",
)

# CodeExecutionSandboxConfig
CODE_EXECUTION_ENDPOINT: HttpUrl = Field(
    description="URL endpoint for code execution service",
    default=HttpUrl("http://sandbox:8194"),
)

# DatabaseConfig
SQLALCHEMY_POOL_SIZE: PositiveInt = Field(
    description="Size of database connection pool",
    default=30,
)
```
**来源：** [api/configs/feature/__init__.py19-175](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L19-L175)

## 服务启动和初始化

服务通过处理迁移、模式选择和进程启动的入口点脚本启动。

### API 服务入口点

API 服务入口点脚本处理多种启动模式：

```mermaid
flowchart TD
    Start["/entrypoint.sh"]
    CheckMigration["MIGRATION_ENABLED==true?"]
    RunMigration["flask upgrade-dbDatabase migrations"]
    CheckMode["MODEvariable"]
    ModeAPI["MODE=apiStart GunicornFlask server"]
    ModeWorker["MODE=workerStart Celeryworker processes"]
    ModeBeat["MODE=beatStart Celerybeat scheduler"]
    ModeMigration["MODE=migrationExit aftermigration"]
    APIProcess["gunicorn--config gunicorn.conf.py--worker-class gevent--workers ${SERVER_WORKER_AMOUNT}"]
    WorkerConfig["Configure Celeryautoscale or fixed workers"]
    WorkerQueues["Queues: dataset,workflow, mail, plugin,app_deletion, etc."]
    WorkerProcess["celery -A app.celery worker-P ${CELERY_WORKER_CLASS}--queues ${QUEUES}"]
    BeatProcess["celery -A app.celery beatPeriodic task scheduler"]

    Start --> CheckMigration
    CheckMigration --> RunMigration
    CheckMigration --> CheckMode
    RunMigration --> CheckMode
    CheckMode --> ModeAPI
    CheckMode --> ModeWorker
    CheckMode --> ModeBeat
    CheckMode --> ModeMigration
    ModeAPI --> APIProcess
    ModeWorker --> WorkerConfig
    WorkerConfig --> WorkerQueues
    WorkerQueues --> WorkerProcess
    ModeBeat --> BeatProcess
```
**来源：** [api/docker/entrypoint.sh1-100](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L1-L100)

### API 模式配置

**Gunicorn 服务器** ([api/docker/entrypoint.sh60-65](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L60-L65)):

```bash
if [[ "${MODE}" == "api" ]]; then
  exec gunicorn \
    --config gunicorn.conf.py \
    --bind "${DIFY_BIND_ADDRESS}:${DIFY_PORT}" \
    --workers "${SERVER_WORKER_AMOUNT}" \
    --worker-class "${SERVER_WORKER_CLASS}" \
    app:app
fi
```
配置参数：

-   `SERVER_WORKER_AMOUNT`: Gunicorn worker 数量（默认：1）
-   `SERVER_WORKER_CLASS`: Worker 类型 - `gevent` 用于异步，`sync` 用于同步（默认：gevent）
-   `SERVER_WORKER_CONNECTIONS`: 每个 worker 的最大连接数（默认：10）
-   `GUNICORN_TIMEOUT`: 请求超时时间（秒）（默认：360）

**来源：** [api/docker/entrypoint.sh60-65](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L60-L65) [docker/.env.example153-182](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L153-L182)

### Worker 模式配置

**Celery Worker** ([api/docker/entrypoint.sh23-58](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L23-L58)):

Worker 模式支持固定 worker 数量和自动缩放：

```bash
if [[ "${MODE}" == "worker" ]]; then
  if [ "${CELERY_AUTO_SCALE,,}" = "true" ]; then
    AVAILABLE_CORES=$(nproc)
    MAX_WORKERS=${CELERY_MAX_WORKERS:-$AVAILABLE_CORES}
    MIN_WORKERS=${CELERY_MIN_WORKERS:-1}
    exec celery -A app.celery worker \
      --autoscale=${MAX_WORKERS},${MIN_WORKERS} \
      --queues dataset,priority_dataset,workflow,mail,plugin,...
  else
    CELERY_WORKER_AMOUNT=${CELERY_WORKER_AMOUNT:-1}
    exec celery -A app.celery worker \
      -P ${CELERY_WORKER_CLASS} \
      -c ${CELERY_WORKER_AMOUNT} \
      --queues dataset,priority_dataset,workflow,mail,plugin,...
  fi
fi
```
配置参数：

-   `CELERY_AUTO_SCALE`: 启用自动缩放（默认：false）
-   `CELERY_MAX_WORKERS`: 自动缩放的最大 workers
-   `CELERY_MIN_WORKERS`: 自动缩放的最小 workers
-   `CELERY_WORKER_AMOUNT`: 固定 worker 数量（默认：1）
-   `CELERY_WORKER_CLASS`: Worker 实现 - 空为 gevent，`sync` 或 `solo` 为替代方案

**队列路由：**

不同的队列处理不同类型的任务：

-   `dataset`, `priority_dataset`: 文档索引和数据集操作
-   `workflow`, `priority_pipeline`, `pipeline`: 工作流执行
-   `mail`: 邮件通知
-   `plugin`: 插件操作
-   `app_deletion`: 应用程序清理
-   `ops_trace`: 运维跟踪
-   `conversation`: 对话处理
-   `workflow_storage`: 工作流存储操作
-   `schedule_poller`, `schedule_executor`: 计划的工作流执行
-   `triggered_workflow_dispatcher`: 基于触发器的工作流调度
-   `trigger_refresh_executor`: 触发器刷新操作
-   `retention`: 数据保留清理

**来源：** [api/docker/entrypoint.sh20-58](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L20-L58) [docker/.env.example184-210](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L184-L210)

### Beat 模式配置

**Celery Beat 调度器** ([api/docker/entrypoint.sh67-70](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L67-L70)):

```bash
if [[ "${MODE}" == "beat" ]]; then
  exec celery -A app.celery beat
fi
```
Beat 调度器管理周期性任务，如：

-   插件升级检查（每 15 分钟）
-   工作流调度轮询
-   数据集队列监控
-   日志清理
-   嵌入缓存清理

**来源：** [api/docker/entrypoint.sh67-70](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L67-L70) [api/.env.example566-582](https://github.com/langgenius/dify/blob/92dbc94f/api/.env.example#L566-L582)

### 数据库迁移流程

当 `MIGRATION_ENABLED=true` 时，迁移在服务启动前自动运行：

```bash
if [[ "${MIGRATION_ENABLED}" == "true" ]]; then
  echo "Running migrations"
  flask upgrade-db

  # 纯迁移模式在完成后退出
  if [[ "${MODE}" == "migration" ]]; then
    echo "Migration completed, exiting normally"
    exit 0
  fi
fi
```
迁移系统通过 Flask-Migrate 使用 Alembic：

-   迁移文件: [api/migrations/versions/](https://github.com/langgenius/dify/blob/92dbc94f/api/migrations/versions/)
-   升级命令: `flask db upgrade`
-   降级命令: `flask db downgrade`

**来源：** [api/docker/entrypoint.sh10-18](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L10-L18) [api/README.md66-72](https://github.com/langgenius/dify/blob/92dbc94f/api/README.md#L66-L72)

### Web 服务入口点

Web 服务入口点脚本配置 Next.js 环境变量并启动 PM2：

```mermaid
flowchart TD
    WebStart["/bin/sh entrypoint.sh"]
    SetEnv["Set Next.js env varsNEXT_PUBLIC_DEPLOY_ENVNEXT_PUBLIC_EDITIONNEXT_PUBLIC_API_PREFIX"]
    CopyFiles["scripts/copy-and-start.mjsCopy server.js to root"]
    PM2Start["pm2-runtime startecosystem.config.js"]
    PM2Instances["PM2_INSTANCES processesdefault: 2"]
    NextServer["Next.js ServerPort 3000"]

    WebStart --> SetEnv
    SetEnv --> CopyFiles
    CopyFiles --> PM2Start
    PM2Start --> PM2Instances
    PM2Instances --> NextServer
```
**来源：** [web/docker/entrypoint.sh1-50](https://github.com/langgenius/dify/blob/92dbc94f/web/docker/entrypoint.sh#L1-L50) [web/package.json25](https://github.com/langgenius/dify/blob/92dbc94f/web/package.json#L25-L25)

PM2 配置：

-   `PM2_INSTANCES`: Node.js 实例数量（默认：2）
-   进程管理器处理重启和负载均衡
-   日志输出到 stdout/stderr 供 Docker 容器日志使用

**来源：** [web/docker/entrypoint.sh1-50](https://github.com/langgenius/dify/blob/92dbc94f/web/docker/entrypoint.sh#L1-L50) [docker/docker-compose-template.yaml152](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L152-L152)

## 存储和向量数据库配置

### 存储后端选择

Dify 通过统一的 `STORAGE_TYPE` 配置支持多种存储后端：

**存储类型选项：**

```mermaid
flowchart TD
    StorageType["STORAGE_TYPE environment variable"]
    OpenDAL["opendalApache OpenDALUnified storage interface"]
    S3["s3Amazon S3 / S3-compatible"]
    Azure["azure-blobAzure Blob Storage"]
    Aliyun["aliyun-ossAlibaba Cloud OSS"]
    Google["google-storageGoogle Cloud Storage"]
    Tencent["tencent-cosTencent Cloud COS"]
    Huawei["huawei-obsHuawei Cloud OBS"]
    Baidu["baidu-obsBaidu Cloud BOS"]
    Volcengine["volcengine-tosVolcengine TOS"]
    OCI["oci-storageOracle Cloud Storage"]
    Supabase["supabaseSupabase Storage"]
    ClickZetta["clickzetta-volumeClickZetta Volume Storage"]

    StorageType --> OpenDAL
    StorageType --> S3
    StorageType --> Azure
    StorageType --> Aliyun
    StorageType --> Google
    StorageType --> Tencent
    StorageType --> Huawei
    StorageType --> Baidu
    StorageType --> Volcengine
    StorageType --> OCI
    StorageType --> Supabase
    StorageType --> ClickZetta
```
**来源：** [docker/.env.example406-529](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L406-L529) [api/configs/middleware/__init__.py1-200](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/__init__.py#L1-L200)

### OpenDAL 存储配置

**OpenDAL** 提供了一个统一的接口来访问多种存储系统。配置使用 `OPENDAL_<SCHEME>_<CONFIG>` 模式：

**文件系统（默认）：**

```yaml
STORAGE_TYPE=opendal
OPENDAL_SCHEME=fs
OPENDAL_FS_ROOT=storage
```
**通过 OpenDAL 的兼容 S3：**

```yaml
STORAGE_TYPE=opendal
OPENDAL_SCHEME=s3
OPENDAL_S3_BUCKET=my-bucket
OPENDAL_S3_ENDPOINT=https://s3.amazonaws.com
OPENDAL_S3_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
OPENDAL_S3_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
OPENDAL_S3_REGION=us-east-1
```
**通过 OpenDAL 的 Azure Blob：**

```yaml
STORAGE_TYPE=opendal
OPENDAL_SCHEME=azblob
OPENDAL_AZBLOB_CONTAINER=my-container
OPENDAL_AZBLOB_ACCOUNT_NAME=myaccount
OPENDAL_AZBLOB_ACCOUNT_KEY=mykey
```
**来源：** [docker/.env.example407-420](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L407-L420) [api/configs/middleware/storage/opendal_storage_config.py1-50](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/storage/opendal_storage_config.py#L1-L50)

### 遗留存储后端

为了向后兼容，支持直接存储后端类型：

**S3 存储：**

```yaml
STORAGE_TYPE=s3
S3_ENDPOINT=https://s3.amazonaws.com
S3_REGION=us-east-1
S3_BUCKET_NAME=difyai
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
S3_USE_AWS_MANAGED_IAM=false  # Use IAM role instead of keys
```
**Azure Blob 存储：**

```yaml
STORAGE_TYPE=azure-blob
AZURE_BLOB_ACCOUNT_NAME=difyai
AZURE_BLOB_ACCOUNT_KEY=your-key
AZURE_BLOB_CONTAINER_NAME=difyai-container
AZURE_BLOB_ACCOUNT_URL=https://difyai.blob.core.windows.net
```
**来源：** [docker/.env.example435-465](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L435-L465) [api/configs/middleware/storage/amazon_s3_storage_config.py1-50](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/storage/amazon_s3_storage_config.py#L1-L50)

### 存储实现映射

**存储工厂** ([api/extensions/ext_storage.py1-150](https://github.com/langgenius/dify/blob/92dbc94f/api/extensions/ext_storage.py#L1-L150)):

```python
def init_app(self, app: Flask):
    storage_type = dify_config.STORAGE_TYPE

    if storage_type == 'opendal':
        self.storage_runner = OpenDALStorage(app=app)
    elif storage_type == 's3':
        self.storage_runner = S3Storage(app=app)
    elif storage_type == 'azure-blob':
        self.storage_runner = AzureBlobStorage(app=app)
    # ... more storage types
```
**存储接口** ([api/extensions/storage/base_storage.py](https://github.com/langgenius/dify/blob/92dbc94f/api/extensions/storage/base_storage.py)):

所有存储实现提供：

-   `save(filename: str, data: bytes) -> None`
-   `load(filename: str) -> bytes`
-   `load_once(filename: str) -> bytes` # 加载并删除
-   `download(filename: str, target_filepath: str) -> None`
-   `exists(filename: str) -> bool`
-   `delete(filename: str) -> None`

**来源：** [api/extensions/ext_storage.py1-150](https://github.com/langgenius/dify/blob/92dbc94f/api/extensions/ext_storage.py#L1-L150)

### 向量数据库配置

Dify 通过 `VECTOR_STORE` 环境变量支持 30+ 种向量数据库后端：

**向量存储选项：**

| 向量存储 | 配置前缀 | 默认端口 |
| --- | --- | --- |
| `weaviate` | `WEAVIATE_` | 8080 |
| `qdrant` | `QDRANT_` | 6333 |
| `milvus` | `MILVUS_` | 19530 |
| `pgvector` | `PGVECTOR_` | 5432 |
| `chroma` | `CHROMA_` | 8000 |
| `opensearch` | `OPENSEARCH_` | 9200 |
| `elasticsearch` | `ELASTICSEARCH_` | 9200 |
| `oceanbase` | `OCEANBASE_VECTOR_` | 2881 |
| `redis` | `REDIS_` | 6379 |
| `analyticdb` | `ANALYTICDB_` | 5432 |
| `couchbase` | `COUCHBASE_` | - |
| 还有 20+ 更多... |  |  |

**来源：** [docker/.env.example520-700](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L520-L700) [api/configs/middleware/__init__.py200-400](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/__init__.py#L200-L400)

### Weaviate 配置示例

```yaml
VECTOR_STORE=weaviate
VECTOR_INDEX_NAME_PREFIX=Vector_index

# Connection
WEAVIATE_ENDPOINT=http://weaviate:8080
WEAVIATE_API_KEY=WVF5YThaHlkYwhGUSmCRgsX3tD5ngdN8pkih
WEAVIATE_GRPC_ENDPOINT=grpc://weaviate:50051

# Tokenization (word/trigram/lowercase/whitespace)
WEAVIATE_TOKENIZATION=word
```
**Docker Compose Profile:**

```bash
docker compose --profile postgresql --profile weaviate up -d
```
**来源：** [docker/.env.example535-544](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L535-L544) [docker/docker-compose.yaml600-650](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml#L600-L650)

### Qdrant 配置示例

```yaml
VECTOR_STORE=qdrant
VECTOR_INDEX_NAME_PREFIX=Vector_index

# Connection
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=difyai123456
QDRANT_CLIENT_TIMEOUT=20

# gRPC (optional, faster than HTTP)
QDRANT_GRPC_ENABLED=false
QDRANT_GRPC_PORT=6334

# Replication for high availability
QDRANT_REPLICATION_FACTOR=1
```
**Docker Compose Profile:**

```bash
docker compose --profile postgresql --profile qdrant up -d
```
**来源：** [docker/.env.example558-568](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L558-L568) [docker/docker-compose.yaml650-700](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml#L650-L700)

### 向量数据库工厂模式

**VDB 初始化** ([api/core/rag/datasource/vdb/vector_factory.py1-150](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_factory.py#L1-L150)):

```python
class Vector:
    def __init__(self, dataset: Dataset, attributes: list | None = None):
        self._dataset = dataset
        self._embeddings = self._get_embeddings()

        vector_type = dify_config.VECTOR_STORE

        if vector_type == VectorType.WEAVIATE:
            from core.rag.datasource.vdb.weaviate.weaviate_vector import WeaviateVector
            self._vector_processor = WeaviateVector(...)
        elif vector_type == VectorType.QDRANT:
            from core.rag.datasource.vdb.qdrant.qdrant_vector import QdrantVector
            self._vector_processor = QdrantVector(...)
        # ... more vector types
```
**向量接口** ([api/core/rag/datasource/vdb/vector_base.py](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_base.py)):

所有向量数据库实现：

-   `create(texts: list, embeddings: list, metadatas: list) -> None`
-   `add_texts(texts: list, embeddings: list) -> None`
-   `delete_by_ids(ids: list) -> None`
-   `delete_by_document_id(document_id: str) -> None`
-   `search_by_vector(query_vector: list, top_k: int) -> list`
-   `search_by_full_text(query: str, top_k: int) -> list`

**来源：** [api/core/rag/datasource/vdb/vector_factory.py1-150](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_factory.py#L1-L150) [api/core/rag/datasource/vdb/vector_type.py1-50](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_type.py#L1-L50)

### 向量存储的数据库迁移

`vdb-migrate` 命令在向量数据库之间迁移数据：

```bash
docker exec -it dify-api-1 flask vdb-migrate --scope all
```
**迁移流程：**

```mermaid
flowchart TD
    Command["flask vdb-migrate --scope all"]
    CheckScope["scope?"]
    KnowledgeScope["scope=knowledgeMigrate datasets"]
    AnnotationScope["scope=annotationMigrate app annotations"]
    AllScope["scope=allMigrate both"]
    GetDatasets["Query Dataset.query.all()"]
    GetAppAnnotations["Query AppAnnotationSetting.query.all()"]
    OldVDB["Old Vector StoreRead from current VECTOR_STORE"]
    NewVDB["New Vector StoreWrite to target VDB"]
    RetrieveVectors["Retrieve document vectors"]
    ReindexVectors["Reindex in new VDB"]
    UpdateDataset["Update dataset.index_struct"]

    Command --> CheckScope
    CheckScope --> KnowledgeScope
    CheckScope --> AnnotationScope
    CheckScope --> AllScope
    KnowledgeScope --> GetDatasets
    AnnotationScope --> GetAppAnnotations
    AllScope --> GetDatasets
    AllScope --> GetAppAnnotations
    GetDatasets --> OldVDB
    GetAppAnnotations --> OldVDB
    OldVDB --> RetrieveVectors
    RetrieveVectors --> NewVDB
    NewVDB --> ReindexVectors
    ReindexVectors --> UpdateDataset
```
**来源：** [api/commands.py161-400](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py#L161-L400)

## 使用 Celery 进行异步任务处理

Dify 使用 Celery 进行后台任务处理，并使用 Redis 作为消息代理和结果后端。

### Celery 架构

```mermaid
flowchart TD
    APIService["API Serviceapp.celery.send_task()"]
    WorkerBeat["Worker BeatPeriodic tasks"]
    Triggers["TriggersWebhooks, schedules"]
    RedisBroker["Redis DB 1CELERY_BROKER_URLredis://:password@redis:6379/1"]
    DatasetQ["datasetDocument indexing"]
    PriorityDatasetQ["priority_datasetHigh-priority indexing"]
    WorkflowQ["workflowWorkflow execution"]
    PipelineQ["pipelinePipeline tasks"]
    MailQ["mailEmail notifications"]
    PluginQ["pluginPlugin operations"]
    AppDeletionQ["app_deletionCleanup tasks"]
    OpsTraceQ["ops_traceTracing"]
    ConversationQ["conversationChat processing"]
    WorkflowStorageQ["workflow_storageStorage ops"]
    SchedulePollerQ["schedule_pollerSchedule polling"]
    ScheduleExecutorQ["schedule_executorSchedule execution"]
    TriggerDispatchQ["triggered_workflow_dispatcherTrigger dispatch"]
    TriggerRefreshQ["trigger_refresh_executorTrigger refresh"]
    RetentionQ["retentionData cleanup"]
    Worker1["Celery Worker 1Processes all queues"]
    Worker2["Celery Worker 2Autoscale if enabled"]
    WorkerN["Celery Worker N..."]
    RedisBackend["Redis DB 1CELERY_BACKEND=redisTask results"]

    APIService --> RedisBroker
    WorkerBeat --> RedisBroker
    Triggers --> RedisBroker
    RedisBroker --> DatasetQ
    RedisBroker --> PriorityDatasetQ
    RedisBroker --> WorkflowQ
    RedisBroker --> PipelineQ
    RedisBroker --> MailQ
    RedisBroker --> PluginQ
    RedisBroker --> AppDeletionQ
    RedisBroker --> OpsTraceQ
    RedisBroker --> ConversationQ
    RedisBroker --> WorkflowStorageQ
    RedisBroker --> SchedulePollerQ
    RedisBroker --> ScheduleExecutorQ
    RedisBroker --> TriggerDispatchQ
    RedisBroker --> TriggerRefreshQ
    RedisBroker --> RetentionQ
    DatasetQ --> Worker1
    PriorityDatasetQ --> Worker1
    WorkflowQ --> Worker1
    PipelineQ --> Worker2
    MailQ --> Worker2
    PluginQ --> WorkerN
    AppDeletionQ --> WorkerN
    Worker1 --> RedisBackend
    Worker2 --> RedisBackend
    WorkerN --> RedisBackend
```
**来源：** [docker/.env.example366-384](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L366-L384) [docker/entrypoint.sh20-58](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L20-L58)

### Broker 和后端配置

**Celery 的 Redis 配置：**

```yaml
# Redis connection for Celery
CELERY_BROKER_URL=redis://:difyai123456@redis:6379/1
CELERY_BACKEND=redis
BROKER_USE_SSL=false

# Redis Sentinel support (optional)
CELERY_USE_SENTINEL=false
CELERY_SENTINEL_MASTER_NAME=mymaster
CELERY_SENTINEL_PASSWORD=sentinel-password
CELERY_SENTINEL_SOCKET_TIMEOUT=0.1
```
**Broker URL 格式：**

-   标准: `redis://[[username]:password@]host:port/db`
-   Sentinel: `sentinel://:password@sentinel1:26379;sentinel://:password@sentinel2:26379/db`

**来源：** [docker/.env.example366-384](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L366-L384)

### 任务队列路由

任务根据其类型路由到特定队列：

**队列映射：**

| 队列名称 | 任务类型 | 优先级 |
| --- | --- | --- |
| `priority_dataset` | 高优先级文档索引 | High |
| `dataset` | 普通文档索引 | Normal |
| `priority_pipeline` | 高优先级工作流执行 | High |
| `pipeline` | 普通工作流执行 | Normal |
| `workflow` | 通用工作流任务 | Normal |
| `mail` | 邮件通知 | Low |
| `plugin` | 插件安装、移除 | Normal |
| `app_deletion` | 应用程序清理 | Low |
| `ops_trace` | 运维跟踪 | Low |
| `conversation` | 对话处理 | Normal |
| `workflow_storage` | 工作流存储操作 | Normal |
| `schedule_poller` | 计划工作流轮询 | Normal |
| `schedule_executor` | 计划工作流执行 | Normal |
| `triggered_workflow_dispatcher` | 基于触发器的工作流调度 | Normal |
| `trigger_refresh_executor` | 触发器刷新操作 | Normal |
| `retention` | 数据保留清理 | Low |

**任务注册示例** ([api/tasks/](https://github.com/langgenius/dify/blob/92dbc94f/api/tasks/):

```python
from celery import shared_task

@shared_task(queue='dataset', bind=True, max_retries=3)
def document_indexing_task(self, dataset_id: str, document_ids: list):
    """
    Index documents in background
    Runs in 'dataset' queue
    """
    pass

@shared_task(queue='mail', bind=True)
def send_email_task(self, to: str, subject: str, body: str):
    """
    Send email notification
    Runs in 'mail' queue
    """
    pass
```
**来源：** [docker/entrypoint.sh20-58](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L20-L58) [api/tasks/](https://github.com/langgenius/dify/blob/92dbc94f/api/tasks/)

### Worker 自动缩放

**固定 Worker 数量：**

```yaml
# Start 4 workers
CELERY_AUTO_SCALE=false
CELERY_WORKER_AMOUNT=4

# Command: celery -A app.celery worker -c 4 --queues ...
```
**自动缩放配置：**

```yaml
# Autoscale between 1 and 8 workers
CELERY_AUTO_SCALE=true
CELERY_MIN_WORKERS=1
CELERY_MAX_WORKERS=8

# Command: celery -A app.celery worker --autoscale=8,1 --queues ...
```
**自动缩放行为：**

-   Celery 监控队列深度和 worker 负载
-   当队列有等待任务时扩展
-   当 worker 空闲时缩减
-   维持最小 workers 作为基准容量
-   最大 workers 限制资源使用

**来源：** [docker/.env.example184-212](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L184-L212) [docker/entrypoint.sh23-45](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L23-L45)

### 周期性任务调度 (Celery Beat)

**Beat 调度器配置：**

Beat 调度器作为单独的进程运行 (`MODE=beat`) 并管理周期性任务。

**任务计划定义** ([api/schedule/schedule.py](https://github.com/langgenius/dify/blob/92dbc94f/api/schedule/schedule.py)):

```python
# Example schedule configuration
CELERYBEAT_SCHEDULE = {
    'check-upgradable-plugins': {
        'task': 'tasks.check_upgradable_plugin_task',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'workflow-schedule-poller': {
        'task': 'tasks.workflow_schedule_poller_task',
        'schedule': timedelta(minutes=WORKFLOW_SCHEDULE_POLLER_INTERVAL),
    },
    'clean-embedding-cache': {
        'task': 'tasks.clean_embedding_cache_task',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
        'enabled': ENABLE_CLEAN_EMBEDDING_CACHE_TASK,
    },
}
```
**计划任务类型：**

1.  **插件更新**：每 15 分钟检查一次插件升级
2.  **工作流调度**：轮询计划的工作流（间隔可配置）
3.  **数据清理**：清理旧日志、消息、嵌入
4.  **监控**：数据集队列监控、警报

**配置变量：**

```yaml
ENABLE_CHECK_UPGRADABLE_PLUGIN_TASK=true
ENABLE_WORKFLOW_SCHEDULE_POLLER_TASK=true
WORKFLOW_SCHEDULE_POLLER_INTERVAL=1  # minutes
WORKFLOW_SCHEDULE_POLLER_BATCH_SIZE=100
WORKFLOW_SCHEDULE_MAX_DISPATCH_PER_TICK=0  # 0=unlimited

ENABLE_CLEAN_EMBEDDING_CACHE_TASK=false
ENABLE_CLEAN_UNUSED_DATASETS_TASK=false
ENABLE_CLEAN_MESSAGES=false
ENABLE_WORKFLOW_RUN_CLEANUP_TASK=false
```
**来源：** [api/.env.example583-603](https://github.com/langgenius/dify/blob/92dbc94f/api/.env.example#L583-L603) [docker/.env.example583-603](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L583-L603)

### 任务结果存储

**结果后端配置：**

```yaml
CELERY_BACKEND=redis
# Results stored in same Redis instance as broker
# Expires after task completion or timeout
```
**任务结果访问：**

```python
from celery.result import AsyncResult

# Send task
result = document_indexing_task.delay(dataset_id, document_ids)

# Check status
if result.ready():
    # Task completed
    output = result.get()
else:
    # Task still running
    state = result.state  # PENDING, STARTED, SUCCESS, FAILURE
```
**来源：** [docker/.env.example366-384](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L366-L384)

### Celery 监控

**Flower (可选):**

Flower 提供了一个基于 Web 的 Celery 监控界面：

```yaml
# Not included in default docker-compose
# Can be added as additional service
flower:
  image: mher/flower
  command: celery --broker=redis://:difyai123456@redis:6379/1 flower
  ports:
    - "5555:5555"
  depends_on:
    - redis
```
**内置监控：**

```bash
# Inspect active tasks
celery -A app.celery inspect active

# Inspect registered tasks
celery -A app.celery inspect registered

# Check worker stats
celery -A app.celery inspect stats
```
**来源：** [docker/.env.example366-384](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L366-L384)

### 卷挂载和数据持久化

**关键卷：**

| 卷 | 挂载点 | 用途 |
| --- | --- | --- |
| `./volumes/db/data` | `/var/lib/postgresql/data` | PostgreSQL 数据目录 |
| `./volumes/mysql/data` | `/var/lib/mysql` | MySQL 数据目录 |
| `./volumes/redis/data` | `/data` | Redis 持久化 |
| `./volumes/app/storage` | `/app/api/storage` | 上传文件、临时文件、插件存储 |
| `./volumes/sandbox/dependencies` | `/dependencies` | 沙箱的 Python 依赖 |
| `./volumes/sandbox/conf` | `/conf` | 沙箱配置 |

**权限初始化：**

`init_permissions` 服务在其他服务启动前确保正确的所有权：

```yaml
init_permissions:
  image: busybox:latest
  command: |
    chown -R 1001:1001 /app/api/storage
  volumes:
    - ./volumes/app/storage:/app/api/storage
  restart: "no"
```
**来源：** [docker/docker-compose-template.yaml4-20](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L4-L20) [docker/docker-compose-template.yaml56-58](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L56-L58)

### 安全注意事项

**SSRF 保护：**

SSRF 代理服务防止服务器端请求伪造攻击：

```yaml
ssrf_proxy:
  image: ubuntu/squid:latest
  environment:
    SQUID_CONFIG: |
      http_access deny all
      http_access allow localhost
```
沙箱和 worker 服务通过此代理路由出站 HTTP 请求。

**密钥管理：**

需要配置的关键密钥：

-   `SECRET_KEY`: 会话 cookie 签名（使用 `openssl rand -base64 42` 生成）
-   `DB_PASSWORD`: 数据库密码
-   `REDIS_PASSWORD`: Redis 密码
-   `SANDBOX_API_KEY`: 沙箱服务 API 密钥
-   `PLUGIN_DAEMON_KEY`: 插件守护进程认证

**来源：** [docker/.env.example96-99](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L96-L99) [docker/docker-compose-template.yaml259-260](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L259-L260)

### 监控和健康

**健康检查端点：**

| 服务 | 健康检查 | 描述 |
| --- | --- | --- |
| API | `http://localhost:5001/health` | Flask 应用程序健康 |
| Web | `http://localhost:3000/` | Next.js 服务器响应 |
| Sandbox | `http://localhost:8194/health` | 沙箱服务健康 |
| PostgreSQL | `pg_isready` 命令 | 数据库就绪 |
| Redis | `redis-cli ping` 命令 | 缓存可用性 |

**指标和跟踪：**

OpenTelemetry 支持 ([docker/.env.example621-638](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L621-L638)):

```yaml
ENABLE_OTEL=false
OTLP_BASE_ENDPOINT=http://localhost:4318
OTEL_EXPORTER_TYPE=otlp
OTEL_SAMPLING_RATE=0.1
```
启用后，系统将跟踪导出到 OTLP 端点以进行可观测性分析。

**来源：** [docker/.env.example621-638](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L621-L638) [docker/docker-compose-template.yaml267](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L267-L267)

### 部署模式

**开发部署：**

1.  克隆仓库
2.  在 `docker/` 目录中将 `.env.example` 复制到 `.env`
3.  生成 `SECRET_KEY`
4.  使用 Profiles 启动：

```bash
cd docker
docker compose --profile postgresql --profile weaviate up -d
```
**来源：** [api/README.md11-21](https://github.com/langgenius/dify/blob/92dbc94f/api/README.md#L11-L21)

**生产部署：**

1.  使用生产级数据库和 Redis（推荐托管服务）
2.  配置兼容 S3 的存储而不是本地文件系统
3.  设置具有 SSL 终止的反向代理 (Nginx)
4.  启用监控和日志聚合
5.  配置卷的备份策略
6.  在 docker-compose 或 Kubernetes 中设置资源限制

**Kubernetes 部署：**

对于生产 Kubernetes 部署：

-   使用 StatefulSets 作为数据库
-   使用具有 HPA 的 Deployments 作为 API/worker 服务
-   配置 PersistentVolumeClaims 用于存储
-   使用 ConfigMaps 进行配置
-   使用 Secrets 存储敏感数据
-   设置 Ingress 进行外部访问

**来源：** [docker/docker-compose.yaml1-850](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml#L1-L850)

### 命令行管理

API 服务提供用于管理任务的 Flask 命令：

**重置密码** ([api/commands.py53-88](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py#L53-L88)):

```bash
docker exec -it dify-api-1 flask reset-password \
  --email user@example.com \
  --new-password newpassword \
  --password-confirm newpassword
```
**向量数据库迁移** ([api/commands.py161-167](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py#L161-L167)):

```bash
docker exec -it dify-api-1 flask vdb-migrate --scope all
```
**重置加密密钥** ([api/commands.py120-158](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py#L120-L158)):

```bash
docker exec -it dify-api-1 flask reset-encrypt-key-pair
```
这些命令需要 API 容器正在运行。

**来源：** [api/commands.py53-167](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py#L53-L167) [api/README.md1-117](https://github.com/langgenius/dify/blob/92dbc94f/api/README.md#L1-L117)
