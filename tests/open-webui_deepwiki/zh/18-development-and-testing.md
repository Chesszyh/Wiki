# 开发与测试 (Development and Testing)

相关源文件

-   [.github/workflows/integration-test.disabled](https://github.com/open-webui/open-webui/blob/a7271532/.github/workflows/integration-test.disabled)
-   [CHANGELOG.md](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md)
-   [backend/open\_webui/storage/provider.py](https://github.com/open-webui/open-webui/blob/a7271532/backend/open_webui/storage/provider.py)
-   [backend/open\_webui/test/apps/webui/storage/test\_provider.py](https://github.com/open-webui/open-webui/blob/a7271532/backend/open_webui/test/apps/webui/storage/test_provider.py)
-   [backend/requirements-min.txt](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements-min.txt)
-   [backend/requirements.txt](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt)
-   [docker-compose.playwright.yaml](https://github.com/open-webui/open-webui/blob/a7271532/docker-compose.playwright.yaml)
-   [package-lock.json](https://github.com/open-webui/open-webui/blob/a7271532/package-lock.json)
-   [package.json](https://github.com/open-webui/open-webui/blob/a7271532/package.json)
-   [pyproject.toml](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml)
-   [src/app.css](https://github.com/open-webui/open-webui/blob/a7271532/src/app.css)
-   [src/lib/components/ChangelogModal.svelte](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/components/ChangelogModal.svelte)
-   [src/lib/components/common/RichTextInput.svelte](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/components/common/RichTextInput.svelte)
-   [src/lib/components/icons/XMark.svelte](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/components/icons/XMark.svelte)
-   [uv.lock](https://github.com/open-webui/open-webui/blob/a7271532/uv.lock)

本页面记录了 Open WebUI 的开发环境设置、测试基础设施和构建系统。它涵盖了本地开发工作流程、测试策略以及持续集成实践。

有关生产环境部署配置的信息，请参阅 [安装与部署](/open-webui/open-webui/3-installation-and-deployment)。有关正在开发的特定子系统的详细架构，请参阅 [架构概览](/open-webui/open-webui/2-architecture-overview)。

## 开发环境

Open WebUI 使用双栈开发方法，分别运行前端 (Node.js/SvelteKit) 和后端 (Python/FastAPI) 开发服务器，两者相互协调。

### 开发栈概览

```mermaid
flowchart TD
    Ollama["Ollama 服务器 端口 11434"]
    NPM["npm/Node.js >= 18.13.0"]
    Vite["Vite 开发服务器 端口 5173"]
    SvelteKit["SvelteKit HMR + SSR"]
    Uvicorn["uvicorn 端口 8080"]
    Python["Python 3.11-3.12"]
    FastAPI["FastAPI open_webui.main:app"]
    DB["SQLite/PostgreSQL 数据库"]
    Redis["Redis (可选)"]

    NPM --> Vite
    Vite --> SvelteKit
    SvelteKit --> Uvicorn
    Python --> Uvicorn
    Uvicorn --> FastAPI
    FastAPI --> Ollama
    FastAPI --> DB
    FastAPI --> Redis
```
**来源：** [package.json1-153](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L1-L153) [pyproject.toml1-210](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L1-L210) [backend/requirements.txt1-156](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L1-L156)

### 本地开发设置

开发需要前端和后端服务器同时运行。前端开发服务器会将 API 请求代理到后端服务器。

**前端开发服务器：**

```bash
npm run dev          # 在端口 5173 启动 Vite
npm run dev:5050     # 备选端口 5050
```
`dev` 脚本执行 `npm run pyodide:fetch && vite dev --host`，其流程如下：

1.  通过 `scripts/prepare-pyodide.js` 下载 Pyodide 资源。
2.  启动带有热模块替换 (HMR) 功能的 Vite 开发服务器。
3.  通过 `--host` 标志启用网络访问。

**后端开发服务器：**

```bash
open-webui serve    # 在端口 8080 启动 uvicorn
```
该命令使用 uvicorn 启动 [backend/open\_webui/main.py](https://github.com/open-webui/open-webui/blob/a7271532/backend/open_webui/main.py) 中定义的 FastAPI 应用程序，并在代码更改时自动重载。

**环境变量：** 本地运行开发环境需要最少量的环境变量：

-   `WEBUI_SECRET_KEY`：会话加密密钥（如果未设置则自动生成）。
-   `OLLAMA_BASE_URL`：连接到 Ollama 的地址（默认为 `http://localhost:11434`）。
-   `DATABASE_URL`：数据库连接字符串（默认为 `./data` 目录下的 SQLite）。

**来源：** [package.json5-12](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L5-L12) [pyproject.toml164-165](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L164-L165)

### 开发脚本

[package.json](https://github.com/open-webui/open-webui/blob/a7271532/package.json) 定义了全面的开发脚本：

| 脚本 | 用途 | 命令 |
| --- | --- | --- |
| `dev` | 启动前端开发服务器 | `vite dev --host` |
| `build` | 生产环境前端构建 | `vite build` |
| `build:watch` | 前端监听模式 | `vite build --watch` |
| `check` | 类型检查 | `svelte-check` |
| `lint` | 代码检查 | 前端 + 类型 + 后端 |
| `lint:frontend` | 前端 ESLint 检查 | `eslint . --fix` |
| `lint:backend` | 后端 Pylint 检查 | `pylint backend/` |
| `format` | 前端代码格式化 | `prettier --write` |
| `format:backend` | 后端代码格式化 | `black . --exclude venv` |
| `test:frontend` | 运行前端测试 | `vitest --passWithNoTests` |
| `cy:open` | 打开 Cypress GUI | `cypress open` |

**后端开发命令：**

-   `black .`: 按照 PEP 8 标准自动格式化 Python 代码。
-   `pylint backend/`: 对 Python 代码质量进行静态分析。
-   `pytest`: 运行后端单元测试和集成测试。

**来源：** [package.json13-22](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L13-L22)

## 测试基础设施

Open WebUI 实施了全面的测试策略，涵盖了前端和后端系统的单元测试、集成测试和端到端测试。

### 测试架构

```mermaid
flowchart TD
    Vitest["vitest 单元测试"]
    Cypress["Cypress E2E 测试"]
    TypeCheck["svelte-check 类型验证"]
    Pytest["pytest 单元 + 集成测试"]
    MockAWS["moto S3 模拟"]
    MockGCS["gcp-storage-emulator GCS 模拟"]
    MockAzure["unittest.mock Azure 模拟"]
    PytestDocker["pytest-docker 容器测试"]
    ComposeStack["Docker Compose 栈"]
    OllamaTest["Ollama 测试服务器"]
    PostgresTest["PostgreSQL 测试数据库"]
    TmpPath["tmp_path pytest 固件"]
    Monkeypatch["monkeypatch 环境模拟"]

    Pytest --> MockAWS
    Pytest --> MockGCS
    Pytest --> MockAzure
    Pytest --> PytestDocker
    Pytest --> TmpPath
    Pytest --> Monkeypatch
    Cypress --> ComposeStack
    ComposeStack --> OllamaTest
    ComposeStack --> PostgresTest
```
**来源：** [package.json34-51](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L34-L51) [backend/requirements.txt133-136](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L133-L136) [backend/open\_webui/test/apps/webui/storage/test\_provider.py1-350](https://github.com/open-webui/open-webui/blob/a7271532/backend/open_webui/test/apps/webui/storage/test_provider.py#L1-L350)

### 后端测试框架

后端使用 `pytest` 作为主要的测试框架，并为外部依赖项配备了专门的固件 (fixtures) 和模拟 (mocking) 库。

**测试组织结构：**

```text
backend/open_webui/test/
├── apps/
│   └── webui/
│       └── storage/
│           └── test_provider.py  # 存储提供商测试
└── [其它测试模块]
```
**存储提供商测试示例：**

[test\_provider.py](https://github.com/open-webui/open-webui/blob/a7271532/test_provider.py) 展示了全面的测试模式：

1.  **基于固件的设置：** `mock_upload_dir` 固件使用 `monkeypatch` 和 `tmp_path` 来创建隔离的测试目录：

```python
def mock_upload_dir(monkeypatch, tmp_path):
    directory = tmp_path / "uploads"
    directory.mkdir()
    monkeypatch.setattr(provider, "UPLOAD_DIR", str(directory))
    return directory
```
2.  **模拟外部服务：** 对 AWS S3 使用 `moto`，对 Google Cloud Storage 使用 `gcp-storage-emulator`，对 Azure 使用 `unittest.mock`：

```python
@mock_aws
class TestS3StorageProvider:
    def __init__(self):
        self.s3_client = boto3.resource("s3", region_name="us-east-1")
```
3.  **测试类结构：** 按提供商组织，具有通用的测试模式：
    -   `test_upload_file`: 验证向本地和云存储的文件上传。
    -   `test_get_file`: 验证文件的检索和下载。
    -   `test_delete_file`: 确认从两个存储层级中删除文件。
    -   `test_delete_all_files`: 测试批量删除操作。

**运行后端测试：**

```bash
cd backend
PYTHONPATH=. pytest . -o log_cli=true -o log_cli_level=INFO
```
**来源：** [backend/open\_webui/test/apps/webui/storage/test\_provider.py1-350](https://github.com/open-webui/open-webui/blob/a7271532/backend/open_webui/test/apps/webui/storage/test_provider.py#L1-L350) [backend/requirements.txt133-136](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L133-L136)

### 前端测试框架

前端测试使用 `vitest` 进行单元测试，并使用 `cypress` 进行端到端集成测试。

**Vitest 配置：**

-   通过 `npm run test:frontend` 运行。
-   使用 `--passWithNoTests` 标志以允许在没有测试的情况下进行构建。
-   与 SvelteKit 的组件测试集成。

**Cypress E2E 测试：**

```bash
npm run cy:open      # 打开交互式的 Cypress GUI
cypress run          # 以无头模式运行测试 (CI 模式)
```
Cypress 测试根据运行中的 Docker Compose 栈（包含 Open WebUI、Ollama 和测试服务）验证完整的用户工作流程。

**来源：** [package.json20-21](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L20-L21) [package.json34](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L34-L34)

### 集成测试流水线

被禁用的 [.github/workflows/integration-test.disabled](https://github.com/open-webui/open-webui/blob/a7271532/.github/workflows/integration-test.disabled) 展示了完整的集成测试方法：

```mermaid
flowchart TD
    Checkout["检出代码库"]
    BuildStack["构建 Docker Compose 栈 open-webui + ollama + 测试服务"]
    WaitOllama["等待 Ollama 健康检查"]
    PreloadModel["预加载测试模型 qwen:0.5b-chat-v1.5-q2_K"]
    CypressRun["运行 Cypress 测试 浏览器: Chrome"]
    UploadArtifacts["上传视频 + 日志"]
    SQLiteTest["SQLite 测试 默认数据库"]
    PostgresTest["PostgreSQL 测试 服务容器"]
    UvicornSQLite["启动后端 SQLite 模式"]
    HealthCheckSQLite["健康检查 GET /api/config"]
    UvicornPostgres["启动后端 PostgreSQL 模式"]
    HealthCheckPostgres["健康检查 GET /health/db"]
    ReconnectTest["测试数据库重连 pg_terminate_backend"]

    Checkout --> BuildStack
    BuildStack --> WaitOllama
    WaitOllama --> PreloadModel
    PreloadModel --> CypressRun
    CypressRun --> UploadArtifacts
    Checkout --> SQLiteTest
    SQLiteTest --> UvicornSQLite
    UvicornSQLite --> HealthCheckSQLite
    HealthCheckSQLite --> PostgresTest
    PostgresTest --> UvicornPostgres
    UvicornPostgres --> HealthCheckPostgres
    HealthCheckPostgres --> ReconnectTest
```
**关键测试阶段：**

1.  **Cypress E2E 测试 (Lines 14-81)：**
    -   构建完整的技术栈：`docker-compose.yaml` + `docker-compose.api.yaml` + 测试服务。
    -   等待 Ollama 健康检查端点 (`http://localhost:11434`)。
    -   预加载轻量级模型以加速测试 (`qwen:0.5b-chat-v1.5-q2_K`)。
    -   针对 `http://localhost:3000` 运行 Cypress。
    -   将测试视频和日志作为构件 (artifacts) 上传。
2.  **迁移测试 (Lines 105-256)：**
    -   测试 SQLite 数据库初始化和稳定性。
    -   测试 PostgreSQL 连接和自动重连。
    -   验证连接失败情况下的数据库连接池管理。
    -   使用 `pg_terminate_backend` 模拟连接断开。

**用于测试的环境变量：**

```text
WEBUI_SECRET_KEY=secret-key
GLOBAL_LOG_LEVEL=debug
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
DATABASE_POOL_SIZE=10
DATABASE_POOL_MAX_OVERFLOW=10
DATABASE_POOL_TIMEOUT=30
```
**来源：** [.github/workflows/integration-test.disabled1-256](https://github.com/open-webui/open-webui/blob/a7271532/.github/workflows/integration-test.disabled#L1-L256) [docker-compose.playwright.yaml1-11](https://github.com/open-webui/open-webui/blob/a7271532/docker-compose.playwright.yaml#L1-L11)

### Playwright 测试

Playwright 用于通过浏览器自动化加载网页内容。[docker-compose.playwright.yaml](https://github.com/open-webui/open-webui/blob/a7271532/docker-compose.playwright.yaml) 为 Playwright 操作定义了一个独立的容器：

```yaml
playwright:
  image: mcr.microsoft.com/playwright:v1.57.0-noble
  command: npx -y playwright@1.57.0 run-server --port 3000
```
**关键的版本匹配：** Playwright 容器版本 (`v1.57.0`) **必须匹配** [backend/requirements.txt123](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L123-L123) 和 [pyproject.toml149](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L149-L149) 中的版本。版本不匹配会导致测试失败。

**环境配置：**

```text
WEB_LOADER_ENGINE=playwright
PLAYWRIGHT_WS_URL=ws://playwright:3000
```
**来源：** [docker-compose.playwright.yaml1-11](https://github.com/open-webui/open-webui/blob/a7271532/docker-compose.playwright.yaml#L1-L11) [backend/requirements.txt123](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L123-L123)

## 构建系统

Open WebUI 分别为前端 (Vite) 和后端 (Hatchling) 使用独立的构建系统，并集成了资产打包功能。

### 构建流水线架构

```mermaid
flowchart TD
    ViteConfig["vite.config.ts"]
    SvelteComponents["Svelte 组件 src/**/*.svelte"]
    Assets["静态资源 static/**"]
    ViteBuild["vite build"]
    FrontendBundle["build/** 静态文件"]
    PyProject["pyproject.toml hatchling 配置"]
    BackendSrc["backend/**/*.py"]
    HatchBuild["hatch build"]
    Wheel["dist/*.whl Python 包"]
    PyodideScript["scripts/prepare-pyodide.js"]
    PyodideAssets["Pyodide 运行时 (浏览器中的 Python)"]
    Dockerfile["Dockerfile"]
    DockerImage["ghcr.io/open-webui/open-webui"]

    ViteConfig --> ViteBuild
    SvelteComponents --> ViteBuild
    Assets --> ViteBuild
    ViteBuild --> FrontendBundle
    PyProject --> HatchBuild
    BackendSrc --> HatchBuild
    HatchBuild --> Wheel
    PyodideScript --> ViteBuild
    FrontendBundle --> PyProject
    Wheel --> Dockerfile
    Dockerfile --> DockerImage
```
**来源：** [package.json8-12](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L8-L12) [pyproject.toml167-197](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L167-L197)

### 前端构建系统

**Vite 配置：** 前端构建使用带有 SvelteKit 适配器的 Vite：

-   开发服务器：快速的 HMR 功能。
-   构建：优化的生产环境包，具有代码分割功能。
-   适配器：`@sveltejs/adapter-static` 用于生成静态站点，或 `@sveltejs/adapter-node` 用于 Node.js 部署。

**构建脚本：**

```bash
npm run build           # 生产环境构建
npm run build:watch     # 开发监听模式
npm run preview         # 预览生产环境构建
```
**静态资产准备：** `pyodide:fetch` 脚本 ([package.json22](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L22-L22)) 在构建之前下载 Pyodide 资产：

```bash
node scripts/prepare-pyodide.js
```
这确保了 Python 运行时可用于 [CodeBlock 组件](/open-webui/open-webui/5.4-code-block-execution) 中的浏览器内代码执行。

**TypeScript 检查：**

```bash
npm run check              # 一次性类型检查
npm run check:watch        # 持续类型检查
```
使用带有 TypeScript 配置的 `svelte-check` 来验证组件类型。

**来源：** [package.json8-12](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L8-L12) [package.json22](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L22-L22) [package.json24-28](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L24-L28)

### 后端构建系统

**Hatchling 配置：**

[pyproject.toml](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml) 使用 Hatchling 作为构建后端，并具有自定义配置：

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
sources = ["backend"]
exclude = [".dockerignore", ".gitignore", ...]
force-include = {
    "CHANGELOG.md" = "open_webui/CHANGELOG.md",
    build = "open_webui/frontend"
}
```
**关键构建特性：**

1.  **源码映射：** 来自 `backend/` 的后端代码被打包为 `open_webui` 模块。
2.  **前端集成：** 来自 `build/` 的已编译前端资产被包含在 wheel 包的 `open_webui/frontend` 位置。
3.  **更新日志绑定：** [CHANGELOG.md](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md) 被嵌入以供运行时版本显示。
4.  **版本提取：** 通过模式匹配从 [package.json](https://github.com/open-webui/open-webui/blob/a7271532/package.json) 中读取版本：

```toml
[tool.hatch.version]
path = "package.json"
pattern = '"version":\s*"(?P<version>[^"]+)"'
```
**构建软件包：**

```bash
# 使用 hatch
hatch build

# 生成: dist/open_webui-{version}-py3-none-any.whl
```
**入口点：** 软件包定义了一个控制台脚本入口点：

```toml
[project.scripts]
open-webui = "open_webui:app"
```
这允许在安装后运行 `open-webui serve`。

**来源：** [pyproject.toml167-197](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L167-L197)

### 依赖管理

**前端依赖项：** 通过 `package.json` 和 `package-lock.json` 使用 NPM 管理：

-   生产环境依赖项：89 个包 (Svelte, Tiptap, marked 等)。
-   开发环境依赖项：32 个包 (Vite, ESLint, Prettier 等)。

**后端依赖项：** 通过 [requirements.txt](https://github.com/open-webui/open-webui/blob/a7271532/requirements.txt) 和 [pyproject.toml](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml) 管理：

-   核心依赖项：FastAPI, uvicorn, SQLAlchemy 等。
-   AI/ML 库：transformers, sentence-transformers, langchain。
-   数据库驱动：psycopg2-binary, pymongo, redis。
-   可选依赖项：定义在 `[project.optional-dependencies]` 中。

**针对特定特性的可选依赖项：**

```toml
[project.optional-dependencies]
postgres = ["psycopg2-binary==2.9.11", "pgvector==0.4.2"]
all = [
    "pymongo", "pytest", "playwright==1.57.0",
    "qdrant-client", "pymilvus", "weaviate-client",
    "elasticsearch", "pinecone", "oracledb", ...
]
```
**最小化依赖：** 在 [backend/requirements-min.txt](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements-min.txt) 处存在一个最小 requirements 文件，用于仅包含基本依赖项的轻量级部署。

**来源：** [package.json54-152](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L54-L152) [backend/requirements.txt1-156](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L1-L156) [pyproject.toml8-162](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L8-L162) [backend/requirements-min.txt1-52](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements-min.txt#L1-L52)

## 版本管理与更新日志

Open WebUI 使用语义化版本控制，具有集中的版本源和结构化的更新日志。

### 版本系统架构

```mermaid
flowchart TD
    PackageJSON["package.json 唯一可信源 版本: 0.6.43"]
    Hatchling["hatchling Python 软件包版本"]
    ConstantsTS["src/lib/constants.ts WEBUI_VERSION"]
    MainPy["backend/open_webui/main.py VERSION 常量"]
    ChangelogMD["CHANGELOG.md Keep a Changelog 格式"]
    ChangelogAPI["GET /api/v1/changelog 已解析的更新日志"]
    ChangelogModal["ChangelogModal.svelte 版本更新 UI"]
    ConfigAPI["GET /api/config 返回版本"]
    LocalStorage["localStorage.version 客户端缓存"]
    VersionCompare["版本对比 如果是新版本则显示模态框"]

    PackageJSON --> Hatchling
    PackageJSON --> ConstantsTS
    ChangelogMD --> ChangelogAPI
    ChangelogAPI --> ChangelogModal
    ConfigAPI --> VersionCompare
    LocalStorage --> VersionCompare
    VersionCompare --> ChangelogModal
```
**来源：** [package.json3](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L3-L3) [pyproject.toml179-180](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L179-L180) [CHANGELOG.md1-10](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md#L1-L10) [src/lib/components/ChangelogModal.svelte1-118](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/components/ChangelogModal.svelte#L1-L118)

### 更新日志格式

[CHANGELOG.md](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md) 遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 格式及语义化版本控制：

```markdown
# Changelog

## [0.6.43] - 2025-12-22

### Added
- 带有提交链接的特性描述
- 新增的环境变量

### Fixed
- 带有议题引用 (issue references) 的错误修复描述

### Changed
- 破坏性变更和修改
- 依赖项更新

### Removed
- 已弃用特性的移除
```
**更新日志结构：**

-   **版本标题：** `## [版本号] - YYYY-MM-DD` 格式。
-   **类别：** Added, Fixed, Changed, Removed。
-   **条目：** 表情符号前缀 + 描述 + 提交/议题/PR 的链接。
-   **引用：** GitHub 提交哈希、议题编号、PR 编号。

**类别语义：**

-   **Added：** 新特性、功能、环境变量。
-   **Fixed：** 错误修复、更正、稳定性改进。
-   **Changed：** 破坏性变更、行为修改、默认值。
-   **Removed：** 已弃用特性的清理。

**来源：** [CHANGELOG.md1-1170](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md#L1-L1170)

### 版本显示 UI

[ChangelogModal.svelte](https://github.com/open-webui/open-webui/blob/a7271532/ChangelogModal.svelte) 组件向用户显示版本信息和更新日志：

**模态框触发逻辑：**

1.  从 `/api/config` 获取当前版本。
2.  与 `localStorage.version` 进行比较。
3.  如果版本不同则显示模态框。
4.  关闭模态框时更新 `localStorage.version`。

**更新日志渲染：**

```html
{#each Object.keys(changelog) as version}
  <div class="font-semibold text-xl">
    v{version} - {changelog[version].date}
  </div>

  {#each Object.keys(changelog[version]).filter(section => section !== 'date') as section}
    <div class="{section === 'added' ? 'bg-blue-500/20' :
                 section === 'fixed' ? 'bg-green-500/20' :
                 section === 'changed' ? 'bg-yellow-500/20' :
                 section === 'removed' ? 'bg-red-500/20' : ''}">
      {section}
    </div>

    {@html DOMPurify.sanitize(entry?.raw)}
  {/each}
{/each}
```
**颜色编码：**

-   **Added：** 蓝色背景 (`bg-blue-500/20`)。
-   **Fixed：** 绿色背景 (`bg-green-500/20`)。
-   **Changed：** 黄色背景 (`bg-yellow-500/20`)。
-   **Removed：** 红色背景 (`bg-red-500/20`)。

**用户设置持久化：** 当用户关闭模态框时，版本会保存到 localStorage 和用户设置中：

```javascript
localStorage.version = $config.version;
await settings.set({ ...$settings, ...{ version: $config.version } });
await updateUserSettings(localStorage.token, { ui: $settings });
```
**来源：** [src/lib/components/ChangelogModal.svelte1-118](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/components/ChangelogModal.svelte#L1-L118)

### 发布流程

基于更新日志结构和版本控制系统，发布流程如下：

1.  **更新版本：** 修改 [package.json](https://github.com/open-webui/open-webui/blob/a7271532/package.json) 中的 `version` 字段。
2.  **更新日志：** 在 [CHANGELOG.md](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md) 中添加带有日期的新版本章节。
3.  **构建前端：** `npm run build` 生成静态资产。
4.  **构建后端：** `hatch build` 创建嵌入了前端资产的 Python wheel 包。
5.  **Docker 构建：** 多阶段构建创建生产环境镜像。
6.  **标记发布：** 创建与版本号一致的 Git 标签。
7.  **部署：** 将 Docker 镜像推送到镜像仓库。

**语义化版本控制规则：**

-   **主版本号 (X.0.0)：** 破坏性变更，不兼容的 API 更改。
-   **次版本号 (0.X.0)：** 新特性，向后兼容的增加。
-   **修订号 (0.0.X)：** 错误修复，向后兼容的补丁。

**来源：** [CHANGELOG.md1-10](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md#L1-L10) [package.json3](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L3-L3) [pyproject.toml179-180](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L179-L180)

## 代码质量工具

Open WebUI 通过检查、格式化和类型检查工具强制执行代码质量。

### 前端代码质量

**ESLint 配置：**

```bash
npm run lint:frontend    # 运行带有 --fix 的 eslint
```
ESLint 配置包含：

-   `@typescript-eslint/eslint-plugin`: TypeScript 特定规则。
-   `eslint-plugin-svelte`: Svelte 组件检查。
-   `eslint-plugin-cypress`: Cypress 测试检查。
-   `eslint-config-prettier`: 禁用与 Prettier 冲突的规则。

**Prettier 格式化：**

```bash
npm run format           # 格式化所有前端文件
```
以统一的风格格式化 JavaScript, TypeScript, Svelte, CSS, Markdown, HTML, 和 JSON 文件。

**TypeScript 检查：**

```bash
npm run check           # 进行类型检查而不产生文件
```
使用 `svelte-check` 验证 Svelte 组件和 TypeScript 文件中的 TypeScript 代码。

**来源：** [package.json13-18](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L13-L18) [package.json24-28](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L24-L28)

### 后端代码质量

**Black 格式化：**

```bash
npm run format:backend   # 自动格式化 Python 代码
black . --exclude venv
```
Black 以零配置强制执行一致的 Python 代码风格。排除了虚拟环境目录。

**Pylint 静态分析：**

```bash
npm run lint:backend     # 在后端运行 pylint
pylint backend/
```
Pylint 执行静态分析，检查：

-   代码错误和 bug。
-   代码异味 (Code smells) 和不良实践。
-   PEP 8 合规性。
-   文档完整性。

**Codespell 配置：** [pyproject.toml199-204](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L199-L204) 定义了拼写检查规则：

```toml
[tool.codespell]
skip = '.git*,*.svg,package-lock.json,i18n,*.lock,*.css'
check-hidden = true
ignore-words-list = 'ans'
```
**来源：** [package.json16-18](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L16-L18) [pyproject.toml199-204](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L199-L204)

## 开发工作流程最佳实践

### 进行代码更改

1.  **前端更改：**

    ```bash
    npm run dev              # 启动开发服务器
    npm run check:watch      # 在后台运行类型检查
    # 进行更改，查看实时更新
    npm run lint:frontend    # 修复检查出的问题
    npm run format           # 格式化代码
    ```

2.  **后端更改：**

    ```bash
    open-webui serve         # 启动后端服务器
    # 进行更改，服务器自动重载
    black .                  # 格式化 Python 代码
    pylint backend/          # 检查问题
    pytest                   # 运行测试
    ```

3.  **全栈更改：**

    -   同时启动前端 (`npm run dev`) 和后端 (`open-webui serve`)。
    -   前端将 API 请求代理到后端。
    -   两个服务器都支持热重载。

**来源：** [package.json5-18](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L5-L18)

### 提交前的测试

**推荐的测试流程：**

```bash
# 前端
npm run check            # 类型检查
npm run lint             # 检查所有代码 (前端 + 类型 + 后端)
npm run format           # 格式化前端
npm run test:frontend    # 运行 vitest

# 后端
npm run format:backend   # 格式化 Python
npm run lint:backend     # 检查 Python
cd backend && pytest     # 运行 Python 测试
```
**集成测试：** 对于使用 Docker 的完整集成测试：

```bash
# 构建并测试全栈
docker compose up --build

# 运行 Cypress 测试 (启用时)
npm run cy:open
```
**来源：** [package.json13-21](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L13-L21) [.github/workflows/integration-test.disabled29-60](https://github.com/open-webui/open-webui/blob/a7271532/.github/workflows/integration-test.disabled#L29-L60)

### 数据库迁移测试

进行数据库架构更改时，请同时使用 SQLite 和 PostgreSQL 测试迁移：

```bash
# 使用 SQLite 测试 (默认)
WEBUI_SECRET_KEY=test open-webui serve

# 使用 PostgreSQL 测试
DATABASE_URL=postgresql://user:pass@localhost:5432/db open-webui serve
```
验证：

-   应用程序成功启动。
-   健康检查返回 200: `curl http://localhost:8080/health/db`。
-   连接丢失后数据库能够自动重连。

**来源：** [.github/workflows/integration-test.disabled156-229](https://github.com/open-webui/open-webui/blob/a7271532/.github/workflows/integration-test.disabled#L156-L229)