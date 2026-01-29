# 7 数据源集成 (Data Source Integration)

相关源文件：

- [api/apps/connector_app.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/apps/connector_app.py)
- [api/db/services/connector_service.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/db/services/connector_service.py)
- [api/utils/common.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/utils/common.py)
- [common/constants.py](https://github.com/infiniflow/ragflow/blob/80a16e71/common/constants.py)
- [common/data_source/__init__.py](https://github.com/infiniflow/ragflow/blob/80a16e71/common/data_source/__init__.py)
- [common/data_source/config.py](https://github.com/infiniflow/ragflow/blob/80a16e71/common/data_source/config.py)
- [docker/docker-compose-base.yml](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/docker-compose-base.yml)
- [docker/infinity_conf.toml](https://github.com/infiniflow/ragflow/blob/80a16e71/docker/infinity_conf.toml)
- [helm/values.yaml](https://github.com/infiniflow/ragflow/blob/80a16e71/helm/values.yaml)
- [pyproject.toml](https://github.com/infiniflow/ragflow/blob/80a16e71/pyproject.toml)
- [rag/svr/sync_data_source.py](https://github.com/infiniflow/ragflow/blob/80a16e71/rag/svr/sync_data_source.py)
- [sdk/python/pyproject.toml](https://github.com/infiniflow/ragflow/blob/80a16e71/sdk/python/pyproject.toml)
- [sdk/python/uv.lock](https://github.com/infiniflow/ragflow/blob/80a16e71/sdk/python/uv.lock)
- [uv.lock](https://github.com/infiniflow/ragflow/blob/80a16e71/uv.lock)
- [web/src/pages/user-setting/data-source/constant/index.tsx](https://github.com/infiniflow/ragflow/blob/80a16e71/web/src/pages/user-setting/data-source/constant/index.tsx)

本文档描述了 RAGFlow 的数据源连接器（Connector）系统，该系统支持将 21 个以上外部平台的文档自动同步到 RAGFlow 知识库中。有关同步后的文档处理流程，请参阅 [文档处理流水线 (Document Processing Pipeline)](/zh/6-document-processing-pipeline)。有关管理连接器的 API 端点，请参阅 [数据集与知识库 API (Dataset and Knowledge Base APIs)](/zh/8-backend-api-system/8.3-dataset-and-knowledge-base-apis)。

## 概述 (Overview)

数据源集成系统提供了一个插件化架构，用于定期从外部服务获取文档并导入到 RAGFlow 知识库。每个连接器都实现了标准化的接口（`LoadConnector`、`PollConnector`），用于全量和增量同步，并内置了凭据管理和错误恢复机制。

**支持的数据源**（`FileSource` 枚举中列出的 21 个活跃连接器）：

- **对象存储 (Blob Storage)**: S3, R2, Oracle Storage (OCI), Google Cloud Storage
- **协同工具 (Collaboration)**: Confluence, Notion, Discord
- **电子邮件 (Email)**: Gmail, IMAP
- **云端文件 (Cloud Files)**: Google Drive, Dropbox, Box, WebDAV
- **项目管理 (Project Management)**: Jira, GitHub, GitLab, Bitbucket, Asana, Airtable
- **支持与教育 (Support/Education)**: Zendesk, Moodle

**核心组件：**

- **`SyncBase`**：处理生命周期、超时和错误日志的任务包装类。
- **连接器类**：针对特定源的实现（如 `S3`、`Notion`、`Gmail`）。
- **`LoadConnector` / `PollConnector`**：用于全量和增量同步的抽象接口。
- **`Document` 模型**：统一的文档表示。
- **`sync_logs` 表**：进度追踪和错误存储。

**入口点**：`sync_data_source.py` 服务作为一个独立的异步进程运行，从 Redis 队列 `SVR_QUEUE_NAME` 中消费任务。

## 架构 (Architecture)

### 连接器类层次结构

系统采用三层架构：
1.  **`SyncBase` (任务包装层)**：管理任务生命周期，强制执行超时，限制并发，并记录异常信息。
2.  **连接器实现层**：继承自 `SyncBase` 并重写 `_generate(task)` 方法，实例化底层的连接器实现。
3.  **抽象接口层**：定义了 `load_from_state()`（全量同步）和 `poll_source()`（增量轮询）的标准接口。

## 同步生命周期 (Synchronization Lifecycle)

### 任务执行流程

1.  **任务初始化**：从队列获取任务，启动日志记录，并受信号量控制的并发限制。
2.  **文档检索**：调用连接器生成器，连接器根据状态决定是执行全量同步还是基于时间范围的增量同步。
3.  **批处理**：将检索到的文档转换为字典格式，插入 `document` 表，上传到 MinIO，并排队等待解析任务。
4.  **进度更新**：实时更新已同步文档数量和错误信息。
5.  **完成与调度**：标记任务完成，并根据配置调度下一次同步任务。

### 凭据管理与 OAuth 刷新 (Credential Management and OAuth Refresh)

基于 OAuth 的连接器（如 Gmail、Google Drive、Box、Dropbox）会自动检测过期的访问令牌（Access Token），利用刷新令牌（Refresh Token）获取新令牌，并将更新后的凭据持久化到数据库中。

## 支持的数据源分类 (Supported Data Sources)

### 对象存储连接器 (Blob Storage Connectors)
包括 **S3**、**R2**、**Oracle Storage** 和 **Google Cloud Storage**。它们利用 `opendal` 库提供统一的访问接口，支持前缀过滤、基于时间戳的轮询和流式下载。

### 协同平台连接器 (Collaboration Platform Connectors)
- **Confluence**：支持索引空间（Space）、页面（Page）或全部内容。
- **Notion**：递归遍历页面层级。
- **Discord**：从指定服务器和频道获取消息。

### 电子邮件连接器 (Email Connectors)
- **Gmail**：使用 OAuth2 和全域代理权限。
- **IMAP**：支持多文件夹和基于 `SINCE` 准则的增量轮询。

### 项目管理连接器 (Project Management Connectors)
- **Jira**：支持 JQL 查询、标签过滤及附件处理。
- **GitHub/GitLab/Bitbucket**：同步代码文件、Issue 和 Pull/Merge Request。
- **Asana**：获取任务、评论和附件。

## 配置与部署 (Configuration and Deployment)

### 前端配置
Web UI 为每个数据源定义了配置模式，包括凭据字段、终结点和范围参数。部分连接器使用了专门的 React 组件来处理 OAuth 流程。

### 并发控制
系统通过 `MAX_CONCURRENT_TASKS` 环境变量限制同时运行的同步任务数量（默认为 5），以防止资源耗尽。

### 错误处理
系统定义了多种异常类型（如凭据缺失、令牌过期、权限不足等）。同步过程中，批量的失败不会导致整个同步任务中断，系统会记录失败详情并继续处理后续批次。
