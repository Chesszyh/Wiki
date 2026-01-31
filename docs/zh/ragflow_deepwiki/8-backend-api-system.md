# 8 后端 API 系统 (Backend API System)

相关源文件：

- [admin/server/admin_server.py](https://github.com/infiniflow/ragflow/blob/80a16e71/admin/server/admin_server.py)
- [api/apps/sdk/chat.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/apps/sdk/chat.py)
- [api/apps/sdk/dataset.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/apps/sdk/dataset.py)
- [api/apps/sdk/doc.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/apps/sdk/doc.py)
- [api/apps/sdk/session.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/apps/sdk/session.py)
- [api/ragflow_server.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/ragflow_server.py)
- [api/utils/api_utils.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/utils/api_utils.py)
- [sdk/python/ragflow_sdk/ragflow.py](https://github.com/infiniflow/ragflow/blob/80a16e71/sdk/python/ragflow_sdk/ragflow.py)

后端 API 系统提供了与 RAGFlow 所有功能交互的全面 RESTful 接口。该系统支持通过标准 HTTP 端点和 OpenAI 兼容接口，以编程方式访问数据集管理、文档处理、聊天助手、智能体（Agent）工作流以及检索操作。

**范围**：本页面涵盖整体架构、身份验证机制、API 设计模式及 OpenAI 兼容层。有关详细的端点文档，请参阅：
- 数据集与知识库操作：[数据集与知识库 API](/zh/8-backend-api-system/8.3-dataset-and-knowledge-base-apis)
- 文件上传与切片管理：[文档与文件管理 API](/zh/8-backend-api-system/8.4-document-and-file-management-apis)
- 聊天补全与对话：[聊天与对话 API](/zh/8-backend-api-system/8.5-chat-and-conversation-apis)
- 智能体工作流 API：[画布 API 与管理](/zh/9-agent-and-workflow-system/9.7-canvas-api-and-management)

## 系统架构 (System Architecture)

后端 API 系统基于 Quart（异步 Flask）构建，提供同步和异步端点。所有 API 功能均暴露在 `/api/v1` 命名空间下，具有一致的身份验证方式和响应格式。

## 应用初始化与配置 (Application Initialization and Configuration)

API 应用在 `api/apps/__init__.py` 中初始化为一个 Quart 实例，支持 CORS 并进行了自定义配置。应用使用了较长的超时时间（600 秒），以适应 CPU 上运行的本地模型较慢的响应速度。支持高达 1GB 的请求/响应体，以满足大文件上传需求。

## 身份验证与授权 (Authentication and Authorization)

RAGFlow 实现了双重身份验证系统，支持基于会话（Session）和基于令牌（Token）的认证。
-   **`@login_required` 装饰器**：用于 Web UI，通过 JWT 令牌或 Redis 会话强制执行已验证的会话。
-   **`@token_required` 装饰器**：用于 SDK 或外部 API 调用，验证 `APIToken` 表中的 Bearer 令牌，并注入 `tenant_id` 参数。

同一端点可以通过 Web 会话或 API 令牌进行访问，增强了集成的灵活性。

## OpenAI 兼容 API 层 (OpenAI-Compatible API Layer)

RAGFlow 提供了兼容 OpenAI 的端点，遵循与 OpenAI Chat Completions API 相同的请求/响应格式。
-   **端点**：`/api/v1/chats_openai/{chat_id}/chat/completions`。
-   **特性**：支持消息历史处理、元数据过滤（通过 `extra_body`）、引用（Citations）显示以及精确的 Token 用量追踪。

## Python SDK 架构 (Python SDK Architecture)

Python SDK (`ragflow-sdk`) 提供了面向对象的接口，将复杂的 HTTP 请求抽象为 Python 类（如 `DataSet`、`Document`、`Chat`、`Session`）。开发者可以使用熟悉的 Python 语法创建数据集、上传文档、启动聊天会话。

## 请求校验与错误处理 (Request Validation and Error Handling)

所有 API 端点均实现了一致的请求校验和标准化的 JSON 响应格式。
-   **成功响应**：返回 `code: 0` 及相应的数据。
-   **错误响应**：返回对应的错误码（如 `101` 参数错误, `104` 权限不足）及错误消息。

## 流式响应实现 (Streaming Response Implementation)

系统使用服务器发送事件 (SSE) 来实现聊天补全和智能体执行结果的实时流式传输。流式响应支持“思考过程 (Thinking)”与“内容 (Content)”的分离显示，并在最后一个数据块中包含引用信息和统计数据。

## 元数据过滤系统 (Metadata Filtering System)

RAGFlow 支持在检索和聊天 API 中使用复杂的基于元数据的文档过滤。用户可以通过逻辑运算符（AND/OR）和比较运算符（is, contains, gte 等）精确控制搜索范围。
