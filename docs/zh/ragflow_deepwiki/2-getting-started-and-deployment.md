# 入门与部署

相关源文件

-   [.github/workflows/release.yml](https://github.com/infiniflow/ragflow/blob/80a16e71/.github/workflows/release.yml)
-   [.github/workflows/tests.yml](https://github.com/infiniflow/ragflow/blob/80a16e71/.github/workflows/tests.yml)
-   [Dockerfile](https://github.com/infiniflow/ragflow/blob/80a16e71/Dockerfile)
-   [Dockerfile.deps](https://github.com/infiniflow/ragflow/blob/80a16e71/Dockerfile.deps)
-   [README.md](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md)
-   [README\_id.md](https://github.com/infiniflow/ragflow/blob/80a16e71/README_id.md)
-   [README\_ja.md](https://github.com/infiniflow/ragflow/blob/80a16e71/README_ja.md)
-   [README\_ko.md](https://github.com/infiniflow/ragflow/blob/80a16e71/README_ko.md)
-   [README\_pt\_br.md](https://github.com/infiniflow/ragflow/blob/80a16e71/README_pt_br.md)
-   [README\_tzh.md](https://github.com/infiniflow/ragflow/blob/80a16e71/README_tzh.md)
-   [README\_zh.md](https://github.com/infiniflow/ragflow/blob/80a16e71/README_zh.md)
-   [api/db/runtime\_config.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/db/runtime_config.py)
-   [docker/.env](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env)
-   [docker/README.md](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/README.md)
-   [docs/configurations.md](https://github.com/infiniflow/ragflow/blob/80a16e71/docs/configurations.md)
-   [docs/guides/manage\_files.md](https://github.com/infiniflow/ragflow/blob/80a16e71/docs/guides/manage_files.md)
-   [docs/guides/upgrade\_ragflow.mdx](https://github.com/infiniflow/ragflow/blob/80a16e71/docs/guides/upgrade_ragflow.mdx)
-   [docs/quickstart.mdx](https://github.com/infiniflow/ragflow/blob/80a16e71/docs/quickstart.mdx)
-   [download\_deps.py](https://github.com/infiniflow/ragflow/blob/80a16e71/download_deps.py)

本页引导您完成 RAGFlow 的部署，从先决条件直到运行第一个实例。RAGFlow 作为一个由 Docker Compose 编排的容器化应用栈进行部署，其主容器同时运行 Flask API 服务器 ([api/ragflow\_server.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/ragflow_server.py)) 和异步任务执行器 ([rag/svr/task\_executor.py](https://github.com/infiniflow/ragflow/blob/80a16e71/rag/svr/task_executor.py))。

有关特定部署主题的详细信息：

-   Docker Compose 服务定义与编排：参见第 2.1 页
-   环境变量与运行时配置：参见第 2.2 页
-   文档存储后端选择 (Elasticsearch/Infinity/OpenSearch)：参见第 2.3 页
-   Docker 构建过程与 CI/CD 流水线：参见第 2.4 页

有关整体系统架构，请参见第 3 页。

## 先决条件

在部署 RAGFlow 之前，请确保您的系统符合以下要求：

| 资源 | 最低要求 | 备注 |
| --- | --- | --- |
| **CPU** | 4 核 (x86\_64) | 提供 ARM64 支持，但需要手动构建 |
| **内存 (RAM)** | 16 GB | Elasticsearch 需要约 8GB，参见 [docker/.env64](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L64-L64) 中的 `MEM_LIMIT` |
| **磁盘** | 50 GB 空闲空间 | 包括 Docker 镜像、卷和文档存储 |
| **Docker** | ≥ 24.0.0 | 检查命令：`docker --version` |
| **Docker Compose** | ≥ v2.26.1 | 检查命令：`docker compose version` |
| **gVisor** (可选) | 最新版本 | 仅在启用沙箱/代码执行功能时需要 |

**平台特定说明：**

-   **ARM64 平台**：官方 Docker 镜像仅支持 x86\_64。ARM64 用户必须按照 [Dockerfile1-207](https://github.com/infiniflow/ragflow/blob/80a16e71/Dockerfile#L1-L207) 的说明构建自定义镜像（参见第 2.4 页）。
-   **Windows**：需要带有 WSL2 后端的 Docker Desktop。
-   **macOS**：需要 Docker Desktop。Apple Silicon 用户需要自定义 ARM64 构建。

**Elasticsearch 的系统优化：**

Elasticsearch 要求 Docker 宿主机上的 `vm.max_map_count ≥ 262144`。该内核参数限制了一个进程可以分配的内存映射区域数量。

```bash
# 检查当前值
sysctl vm.max_map_count

# 临时设置（重启后失效）
sudo sysctl -w vm.max_map_count=262144

# 在 /etc/sysctl.conf 中永久持久化
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

如果此值不足，Elasticsearch 将无法启动，并出现类似 `Can't connect to ES cluster` 或 `max virtual memory areas vm.max_map_count [65530] is too low` 的错误。

数据源：[README.md136-152](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md#L136-L152) [docs/quickstart.mdx28-90](https://github.com/infiniflow/ragflow/blob/80a16e71/docs/quickstart.mdx#L28-L90) [docker/.env64](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L64-L64)

## 快速入门：使用 Docker Compose 部署

**快速入门部署流程**

> **[Mermaid sequence]**
> *(图表结构无法解析)*

数据源：[README.md180-235](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md#L180-235) [docs/quickstart.mdx186-234](https://github.com/infiniflow/ragflow/blob/80a16e71/docs/quickstart.mdx#L186-L234)

### 分步部署指南

1.  **克隆仓库：**

    ```bash
    git clone https://github.com/infiniflow/ragflow.git
    cd ragflow/docker
    ```

2.  **切换到稳定版本（推荐）：**

    ```bash
    git checkout v0.23.1
    ```

    这确保了 [docker/entrypoint.sh](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/entrypoint.sh) 脚本与 Docker 镜像版本匹配。

3.  **启动服务：**

    ```bash
    docker compose -f docker-compose.yml up -d
    ```

    该命令会：

    -   从 [docker/.env1-258](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L1-L258) 读取配置
    -   拉取 Docker 镜像：`infiniflow/ragflow:v0.23.1`（约 2GB 压缩大小）、`elasticsearch:8.11.3`、`mysql:8.0`、`redis`、`minio`、`nginx`
    -   创建 Docker 网络和卷
    -   按依赖顺序启动容器
4.  **验证启动状态：**

    ```bash
    docker logs -f docker-ragflow-cpu-1
    ```

    等待确认初始化成功的输出：

    ```
         ____   ___    ______ ______ __
        / __ \ /   |  / ____// ____// /____  _      __
       / /_/ // /| | / / __ / /_   / // __ \| | /| / /
      / _, _// ___ |/ /_/ // __/  / // /_/ /| |/ |/ /
     /_/ |_|/_/  |_|\____//_/    /_/ \____/ |__/|__/

     * Running on all addresses (0.0.0.0)
    ```

    **警告：** 在看到此消息之前登录可能会导致 `network abnormal` 错误，因为初始化尚未完成。

5.  **访问 Web 界面：**

    打开浏览器并导航至：

    ```
    http://YOUR_SERVER_IP
    ```

    在默认设置下，使用 80 端口，因此 URL 中不需要端口号（参见 [docker/.env133](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L133-L133) 中的 `SVR_WEB_HTTP_PORT`）。

6.  **配置 LLM 提供商：**

    登录后，点击您的个人头像 → **模型提供商 (Model Providers)** 来配置 LLM 服务的 API 密钥。至少需要：

    -   一个聊天模型（例如 OpenAI GPT-4, Anthropic Claude）
    -   一个嵌入模型（例如 OpenAI text-embedding-ada-002, BAAI/bge-m3）

    然后点击 **系统模型设置 (System Model Settings)** 来选择用于聊天、嵌入和其他任务的默认模型。

数据源：[README.md180-250](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md#L180-L250) [docs/quickstart.mdx186-267](https://github.com/infiniflow/ragflow/blob/80a16e71/docs/quickstart.mdx#L186-L267)

## 部署选项

### 标准 Docker 部署

默认部署使用预构建的 Docker 镜像，采用基于 CPU 的文档处理：

```bash
cd ragflow/docker
docker compose -f docker-compose.yml up -d
```

启动的关键容器包括：

-   `docker-ragflow-cpu-1`：主应用（nginx + Flask API + 任务执行器）
-   `docker-es01-1`：用于文档存储的 Elasticsearch 8.11.3
-   `docker-mysql-1`：用于元数据（用户、数据集、对话）的 MySQL 8.0
-   `docker-redis-1`：用于缓存和任务队列的 Redis
-   `docker-minio-1`：用于对象存储（上传的文件）的 MinIO

数据源：[README.md193-206](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md#L193-L206) [docker/docker-compose.yml1-100](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/docker-compose.yml#L1-L100)

### GPU 加速部署

如需使用 GPU 实现更快的文档处理：

```bash
cd ragflow/docker
# 在 .env 第一行插入 DEVICE=gpu
sed -i '1i DEVICE=gpu' .env
docker compose -f docker-compose.yml up -d
```

这会改变：

-   容器名称：使用 `docker-ragflow-gpu-1` 而非 `docker-ragflow-cpu-1`
-   DeepDoc 推理通过 CUDA 在 GPU 上运行
-   要求宿主机安装 NVIDIA Docker 运行时

[docker/.env25](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L25-L25) 中的 `DEVICE` 变量控制激活哪个 Docker Compose Profile，从而在 DeepDoc 处理流水线的 CPU 和 GPU 变体之间切换。

数据源：[README.md200-206](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md#L200-L206) [docker/.env21-27](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L21-L27)

### 从源码进行开发部署

对于开发工作流，可以在宿主机运行 RAGFlow 源码，并在 Docker 中运行后端服务：

```bash
# 仅启动后端服务（不启动 RAGFlow 容器）
docker compose -f docker/docker-compose-base.yml up -d

# 将容器主机名映射到 localhost
echo "127.0.0.1 es01 mysql minio redis" | sudo tee -a /etc/hosts

# 安装 Python 依赖
uv sync --python 3.12
uv run download_deps.py

# 启动后端服务
source .venv/bin/activate
export PYTHONPATH=$(pwd)
bash docker/launch_backend_service.sh

# 启动前端开发服务器（在另一个终端中）
cd web
npm install
npm run dev  # 访问 http://localhost:8000
```

此设置：

-   直接在宿主机上运行 [api/ragflow\_server.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/ragflow_server.py) 和 [rag/svr/task\_executor.py](https://github.com/infiniflow/ragflow/blob/80a16e71/rag/svr/task_executor.py)。
-   使用 [docker/docker-compose-base.yml1-249](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/docker-compose-base.yml#L1-L249) 仅启动 MySQL, Elasticsearch, Redis 和 MinIO。
-   为后端 (Python) 和前端 (React/UmiJS) 启用热重载。
-   适用于调试和快速迭代。

数据源：[README.md315-377](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md#L315-L377) [docker/docker-compose-base.yml1-249](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/docker-compose-base.yml#L1-L249)

## 初始配置

部署后，RAGFlow 仅需极少配置即可开始处理文档：

### 配置文件

| 文件 | 目的 | 是否需要修改 |
| --- | --- | --- |
| [docker/.env](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env) | Docker Compose 环境变量（端口、密码、镜像标签） | 可选：更改默认密码、端口 |
| [docker/service\_conf.yaml.template](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/service_conf.yaml.template) | 后端服务配置（数据库、LLM 工厂） | 必须：添加 LLM API 密钥 |
| [docker/docker-compose.yml](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/docker-compose.yml) | 服务定义与容器编排 | 可选：调整资源限制 |

`.env` 文件包含 `MYSQL_PASSWORD`, `DOC_ENGINE`, `RAGFLOW_IMAGE` 等变量，Docker Compose 使用这些变量配置容器。在容器启动时，[docker/entrypoint.sh](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/entrypoint.sh) 使用 `envsubst` 处理 `service_conf.yaml.template`，将 `${VARIABLE}` 占位符替换为环境中的实际值。

数据源：[docker/.env1-258](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L1-L258) [docker/service\_conf.yaml.template1-200](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/service_conf.yaml.template#L1-L200) [README.md252-266](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md#L252-L266)

### 关键配置步骤

1.  **更改默认密码（生产部署）：**

    编辑 [docker/.env](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env) 并更新：

    ```env
    MYSQL_PASSWORD=your_secure_password
    ELASTIC_PASSWORD=your_secure_password
    MINIO_PASSWORD=your_secure_password
    REDIS_PASSWORD=your_secure_password
    ```

    **警告：** [docker/.env1-6](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L1-L6) 中的默认密码是不安全的，绝不应在生产环境中使用。

2.  **配置 LLM API 密钥：**

    编辑 [docker/service\_conf.yaml.template](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/service_conf.yaml.template) 的 `user_default_llm` 部分，添加您的 LLM 提供商 API 密钥。至少配置：

    -   一个聊天模型提供商（例如 OpenAI, Anthropic, 通义千问）
    -   一个嵌入模型提供商

    或者，在登录后通过 Web UI 配置（设置 → 模型提供商）。

3.  **应用配置更改：**

    ```bash
    docker compose -f docker/docker-compose.yml up -d
    ```

    这会使用更新后的配置重新创建容器。

数据源：[docker/.env1-6](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L1-L6) [docker/service\_conf.yaml.template](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/service_conf.yaml.template) [README.md244-249](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md#L244-L249)

## 常见部署场景

### 切换文档存储后端

默认情况下，RAGFlow 使用 Elasticsearch 存储文档。如需切换到 Infinity（优化的向量数据库）：

```bash
# 停止服务并移除卷（警告：这会删除所有已索引的文档）
docker compose -f docker/docker-compose.yml down -v

# 编辑 docker/.env
sed -i 's/DOC_ENGINE=elasticsearch/DOC_ENGINE=infinity/' docker/.env

# 使用新后端重启
docker compose -f docker/docker-compose.yml up -d
```

`DOC_ENGINE` 变量 ([docker/.env19](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L19-L19)) 控制 [docker/docker-compose.yml](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/docker-compose.yml) 中激活哪个 Profile，从而启动 `es01`, `infinity` 或 `opensearch01` 服务。

有关后端详细对比和配置选项，请参见第 2.3 页。

数据源：[docker/.env13-19](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L13-L19) [README.md273-291](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md#L273-L291)

### 启用可选服务

**TEI 嵌入服务**（本地嵌入生成）：

```env
# 编辑 docker/.env，取消注释以下其中一项：
COMPOSE_PROFILES=${COMPOSE_PROFILES},tei-cpu    # CPU 模式
# 或用于 GPU 加速：
# COMPOSE_PROFILES=${COMPOSE_PROFILES},tei-gpu
```

TEI 服务 ([docker/docker-compose.yml](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/docker-compose.yml)) 提供本地嵌入模型推理，消除了对外部 LLM API 进行向量化的依赖。

**沙箱代码执行器 (Sandbox Code Executor)**（用于 Agent 的 Python/JS 代码执行）：

```bash
# 首先安装 gVisor
# 然后编辑 docker/.env，取消注释：
SANDBOX_ENABLED=1
COMPOSE_PROFILES=${COMPOSE_PROFILES},sandbox
```

要求宿主机有 gVisor 运行时并预先拉取了基础镜像 ([docker/.env219-231](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L219-L231))。

数据源：[docker/.env150-231](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/.env#L150-L231) [README.md150](https://github.com/infiniflow/ragflow/blob/80a16e71/README.md#L150-L150)

## 后续步骤

RAGFlow 部署完成后：

1.  通过 Web UI **创建您的第一个数据集**并上传文档。
2.  根据您的文档类型 **配置切片模板**。
3.  **设置聊天助手**来查询您的文档。

对于生产级部署：

-   查看第 2.2 页中详细的配置选项。
-   在第 2.3 页中选择合适的文档存储后端。
-   实施监控和备份策略。

对于开发工作流：

-   按照第 2.4 页构建自定义 Docker 镜像。
-   配置 CI/CD 流水线以进行自动化测试。
