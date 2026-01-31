# Deployment and Operations

Relevant source files

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
-   [api/app\_factory.py](https://github.com/langgenius/dify/blob/92dbc94f/api/app_factory.py)
-   [api/commands.py](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py)
-   [api/configs/feature/\_\_init\_\_.py](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py)
-   [api/configs/middleware/\_\_init\_\_.py](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/__init__.py)
-   [api/configs/packaging/\_\_init\_\_.py](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/packaging/__init__.py)
-   [api/controllers/console/datasets/datasets.py](https://github.com/langgenius/dify/blob/92dbc94f/api/controllers/console/datasets/datasets.py)
-   [api/core/rag/datasource/vdb/vector\_factory.py](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_factory.py)
-   [api/core/rag/datasource/vdb/vector\_type.py](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_type.py)
-   [api/extensions/ext\_storage.py](https://github.com/langgenius/dify/blob/92dbc94f/api/extensions/ext_storage.py)
-   [api/extensions/storage/storage\_type.py](https://github.com/langgenius/dify/blob/92dbc94f/api/extensions/storage/storage_type.py)
-   [api/migrations/README](https://github.com/langgenius/dify/blob/92dbc94f/api/migrations/README)
-   [api/pyproject.toml](https://github.com/langgenius/dify/blob/92dbc94f/api/pyproject.toml)
-   [api/tests/unit\_tests/configs/test\_dify\_config.py](https://github.com/langgenius/dify/blob/92dbc94f/api/tests/unit_tests/configs/test_dify_config.py)
-   [api/uv.lock](https://github.com/langgenius/dify/blob/92dbc94f/api/uv.lock)
-   [dev/pytest/pytest\_vdb.sh](https://github.com/langgenius/dify/blob/92dbc94f/dev/pytest/pytest_vdb.sh)
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

This document describes the deployment architecture, container orchestration, environment configuration, and operational considerations for running Dify in production or development environments. It covers Docker image builds, service dependencies, configuration management, and startup procedures.

For information about the overall system architecture and service topology, see [System Architecture Overview](/langgenius/dify/2-system-architecture-overview). For details on configuration models and Pydantic settings, see [Configuration System](/langgenius/dify/2.3-application-types-and-execution-modes).

## Docker Build Process and Multi-Architecture Images

Dify uses multi-stage Docker builds to create optimized production images for both the API backend and web frontend services. The build process is orchestrated through GitHub Actions CI/CD pipeline.

### API Service Multi-Stage Build

The API service uses a three-stage build defined in [api/Dockerfile1-122](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L1-L122):

**Stage 1: Base Image Setup** ([api/Dockerfile1-10](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L1-L10)):

-   Base: `python:3.12-slim-bookworm`
-   Installs `uv` package manager version 0.8.9
-   Sets working directory to `/app/api`

**Stage 2: Dependency Installation** ([api/Dockerfile12-26](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L12-L26)):

-   Installs system dependencies: `g++`, `libmpfr-dev`, `libmpc-dev` (for building `gmpy2`)
-   Copies `pyproject.toml` and `uv.lock`
-   Runs `uv sync --locked --no-dev` to install production dependencies
-   Creates virtual environment at `/app/api/.venv`

**Stage 3: Production Image** ([api/Dockerfile28-122](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L28-L122)):

-   Creates non-root user `dify` with UID 1001
-   Installs runtime dependencies:
    -   Node.js 22.x from NodeSource repository
    -   System libraries: `libgmp-dev`, `libmpfr-dev`, `libmpc-dev`
    -   Fonts: `fonts-noto-cjk` for PDF rendering
    -   `libmagic1` for MIME type detection
    -   `media-types` package for file extension mapping
-   Downloads NLTK data to `/usr/local/share/nltk_data`
-   Pre-caches Tiktoken encodings to `.tiktoken_cache`
-   Copies application code to `/app/api/`
-   Sets entrypoint to `/entrypoint.sh`

**Build Architecture Diagram:**

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
**Sources:** [api/Dockerfile1-122](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L1-L122)

Key build optimizations:

-   Multi-stage build reduces final image size by excluding build tools
-   `uv sync --locked` ensures reproducible builds
-   Pre-downloading NLTK and Tiktoken data avoids runtime downloads
-   Non-root user `dify:1001` for security
-   Build argument `COMMIT_SHA` for version tracking

**Sources:** [api/Dockerfile1-122](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L1-L122)

Key aspects of the API image:

| Aspect | Configuration | Location |
| --- | --- | --- |
| Base Image | `python:3.12-slim-bookworm` | [api/Dockerfile2](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L2-L2) |
| Package Manager | `uv` version 0.8.9 | [api/Dockerfile7-9](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L7-L9) |
| Dependencies | Defined in `pyproject.toml`, locked in `uv.lock` | [api/pyproject.toml1-230](https://github.com/langgenius/dify/blob/92dbc94f/api/pyproject.toml#L1-L230) [api/uv.lock1-105](https://github.com/langgenius/dify/blob/92dbc94f/api/uv.lock#L1-L105) |
| User | Non-root user `dify` with UID 1001 | [api/Dockerfile52-55](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L52-L55) |
| Entrypoint | `/entrypoint.sh` | [api/Dockerfile103](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L103-L103) |
| Working Directory | `/app/api` | [api/Dockerfile49](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L49-L49) |
| Exposed Port | 5001 | [api/Dockerfile39](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L39-L39) |

The build process uses `uv sync --locked --no-dev` to install production dependencies without dev packages, ensuring a minimal image size. NLTK data and Tiktoken caches are pre-downloaded during build to avoid runtime downloads.

**Sources:** [api/Dockerfile1-104](https://github.com/langgenius/dify/blob/92dbc94f/api/Dockerfile#L1-L104) [api/pyproject.toml1-230](https://github.com/langgenius/dify/blob/92dbc94f/api/pyproject.toml#L1-L230)

### Web Service Multi-Stage Build

The web service uses a four-stage build defined in [web/Dockerfile1-87](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L1-L87):

**Stage 1: Base Image Setup** ([web/Dockerfile1-16](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L1-L16)):

-   Base: `node:24-alpine`
-   Enables `corepack` for pnpm management
-   Installs `tzdata` for timezone support
-   Configures `PNPM_HOME` and adds to `PATH`

**Stage 2: Package Installation** ([web/Dockerfile19-29](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L19-L29)):

-   Copies `package.json` and `pnpm-lock.yaml`
-   Runs `corepack install` to use exact pnpm version from `package.json`
-   Executes `pnpm install --frozen-lockfile` for reproducible builds

**Stage 3: Build** ([web/Dockerfile32-38](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L32-L38)):

-   Copies all source code
-   Sets `NODE_OPTIONS="--max-old-space-size=4096"` for large builds
-   Runs `pnpm build:docker` which executes:
    -   `next build` with standalone output mode ([web/package.json28](https://github.com/langgenius/dify/blob/92dbc94f/web/package.json#L28-L28))
    -   `optimize-standalone.js` script to reduce output size ([web/scripts/optimize-standalone.js](https://github.com/langgenius/dify/blob/92dbc94f/web/scripts/optimize-standalone.js))

**Stage 4: Production** ([web/Dockerfile41-87](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L41-L87)):

-   Creates non-root user `dify:1001`
-   Installs PM2 globally: `pnpm add -g pm2`
-   Copies build artifacts:
    -   `.next/standalone/` - self-contained server
    -   `.next/static/` - static assets
    -   `public/` - public files
-   Sets entrypoint to `entrypoint.sh`

**Build Architecture Diagram:**

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
**Sources:** [web/Dockerfile1-87](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L1-L87) [web/package.json1-289](https://github.com/langgenius/dify/blob/92dbc94f/web/package.json#L1-L289)

**Next.js Standalone Output:**

The build uses Next.js standalone output mode configured in `next.config.js`:

```
output: 'standalone'
```
This creates a minimal production server bundle that includes only necessary dependencies, significantly reducing deployment size. The `optimize-standalone.js` script further removes unnecessary files.

**Sources:** [web/Dockerfile1-87](https://github.com/langgenius/dify/blob/92dbc94f/web/Dockerfile#L1-L87) [web/package.json28](https://github.com/langgenius/dify/blob/92dbc94f/web/package.json#L28-L28)

### Multi-Architecture Build Pipeline

The CI/CD pipeline builds images for both `amd64` and `arm64` architectures using GitHub Actions.

**Build Matrix** ([.github/workflows/build-push.yml](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/build-push.yml):

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
**Sources:** [.github/workflows/build-push.yml1-100](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/build-push.yml#L1-L100)

Build process uses:

-   `docker/setup-buildx-action` for BuildKit
-   `docker/setup-qemu-action` for cross-platform builds
-   Build argument `COMMIT_SHA` injected from Git SHA
-   Tagged with version from `pyproject.toml` and `package.json`

**Sources:** [.github/workflows/build-push.yml1-150](https://github.com/langgenius/dify/blob/92dbc94f/.github/workflows/build-push.yml#L1-L150)

## Service Orchestration with Docker Compose

Dify uses Docker Compose for orchestrating multiple services with dependency management, health checks, and profile-based conditional deployment.

### Service Topology and Dependencies

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
**Sources:** [docker/docker-compose-template.yaml1-320](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L1-L320) [docker/docker-compose.yaml1-850](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml#L1-L850)

### Service Configuration Details

**API Service** ([docker/docker-compose-template.yaml22-61](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L22-L61)):

-   Image: `langgenius/dify-api:1.11.1`
-   Environment: `MODE=api` to start Flask/Gunicorn server
-   Depends on: `init_permissions` (completed), database (healthy), Redis (started)
-   Volumes: `./volumes/app/storage:/app/api/storage` for file storage
-   Networks: `ssrf_proxy_network`, `default`

**Worker Service** ([docker/docker-compose-template.yaml64-100](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L64-L100)):

-   Image: `langgenius/dify-api:1.11.1` (same as API)
-   Environment: `MODE=worker` to start Celery workers
-   Queues: dataset, workflow, mail, ops\_trace, app\_deletion, plugin, etc.
-   Same dependencies and volumes as API service

**Worker Beat Service** ([docker/docker-compose-template.yaml103-131](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L103-L131)):

-   Image: `langgenius/dify-api:1.11.1` (same as API)
-   Environment: `MODE=beat` to start Celery beat scheduler
-   Manages periodic tasks like plugin upgrades, workflow scheduling

**Web Service** ([docker/docker-compose-template.yaml133-160](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L133-L160)):

-   Image: `langgenius/dify-web:1.11.1`
-   Environment variables for API URLs, marketplace, feature flags
-   No database dependencies (stateless frontend)

**Sources:** [docker/docker-compose-template.yaml1-320](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L1-L320)

### Docker Compose Profiles

Profiles enable conditional service deployment based on database and vector store choices:

| Profile | Services | Purpose |
| --- | --- | --- |
| `postgresql` | `db_postgres` | Use PostgreSQL as metadata database |
| `mysql` | `db_mysql` | Use MySQL as metadata database |
| `weaviate` | `weaviate` | Use Weaviate as vector database |
| `qdrant` | `qdrant` | Use Qdrant as vector database |
| `chroma` | `chroma` | Use Chroma as vector database |
| `pgvector` | `pgvector` | Use PGVector as vector database |
| `opensearch` | `opensearch` | Use OpenSearch as vector database |
| `oceanbase` | `oceanbase` | Use OceanBase as database |

Usage example:

```
docker compose --profile postgresql --profile weaviate up -d
```
**Sources:** [docker/docker-compose.middleware.yaml1-200](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.middleware.yaml#L1-L200) [api/README.md15-20](https://github.com/langgenius/dify/blob/92dbc94f/api/README.md#L15-L20)

### Health Checks

Services include health checks to ensure proper startup sequencing:

**PostgreSQL** ([docker/docker-compose-template.yaml183-197](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L183-L197)):

```
healthcheck:
  test: ["CMD", "pg_isready", "-h", "db_postgres", "-U", "postgres", "-d", "dify"]
  interval: 1s
  timeout: 3s
  retries: 60
```
**MySQL** ([docker/docker-compose-template.yaml216-227](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L216-L227)):

```
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-u", "root", "-p${DB_PASSWORD}"]
  interval: 1s
  timeout: 3s
  retries: 30
```
**Redis** ([docker/docker-compose-template.yaml240-245](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L240-L245)):

```
healthcheck:
  test: ["CMD-SHELL", "redis-cli -a ${REDIS_PASSWORD} ping | grep -q PONG"]
```
**Sandbox** ([docker/docker-compose-template.yaml267](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L267-L267)):

```
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8194/health"]
```
The `depends_on` configuration with `condition: service_healthy` ensures services wait for dependencies to be fully operational before starting.

**Sources:** [docker/docker-compose-template.yaml183-267](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L183-L267)

## Environment Configuration and Runtime Modes

Dify uses a hierarchical configuration system with environment variables validated through Pydantic settings models.

### Configuration Loading Flow

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
**Sources:** [docker/docker-compose.yaml1-850](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml#L1-L850) [docker/.env.example1-1000](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L1-L1000) [api/configs/app\_config.py1-50](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/app_config.py#L1-L50) [api/app\_factory.py18-25](https://github.com/langgenius/dify/blob/92dbc94f/api/app_factory.py#L18-L25)

### Runtime Mode Selection

The API service container runs in different modes based on the `MODE` environment variable:

**Mode Configuration Table:**

| Mode | Environment Variable | Process | Purpose |
| --- | --- | --- | --- |
| `api` | `MODE=api` | Gunicorn with Flask app | HTTP API server |
| `worker` | `MODE=worker` | Celery worker | Background task processing |
| `beat` | `MODE=beat` | Celery beat | Periodic task scheduling |
| `migration` | `MODE=migration` | Flask-Migrate | Database migrations only |

**Entrypoint Mode Selection** ([docker/entrypoint.sh1-100](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L1-L100)):

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
**Sources:** [docker/entrypoint.sh1-100](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L1-L100)

### Gunicorn Server Configuration (MODE=api)

**Key Environment Variables:**

| Variable | Default | Description |
| --- | --- | --- |
| `DIFY_BIND_ADDRESS` | `0.0.0.0` | Bind address for API server |
| `DIFY_PORT` | `5001` | HTTP port |
| `SERVER_WORKER_AMOUNT` | `1` | Number of Gunicorn workers |
| `SERVER_WORKER_CLASS` | `gevent` | Worker class (gevent/sync/solo) |
| `SERVER_WORKER_CONNECTIONS` | `10` | Max connections per worker |
| `GUNICORN_TIMEOUT` | `360` | Request timeout in seconds |

**Worker Class Selection:**

-   `gevent`: Async greenlet-based workers (default, recommended for I/O-bound)
-   `sync`: Synchronous workers (for CPU-bound tasks)
-   `solo`: Single-threaded worker (for debugging on Windows)

**Gunicorn Configuration File** ([api/gunicorn.conf.py](https://github.com/langgenius/dify/blob/92dbc94f/api/gunicorn.conf.py):

The configuration applies monkey patching for gevent when using the `gevent` worker class:

```
if worker_class == 'gevent':
    from gevent import monkey
    monkey.patch_all()
    # Patch psycopg2 for PostgreSQL async support
    from psycopg2.extensions import set_wait_callback
```
**Sources:** [docker/.env.example144-182](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L144-L182) [docker/entrypoint.sh60-70](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L60-L70) [api/gunicorn.conf.py1-50](https://github.com/langgenius/dify/blob/92dbc94f/api/gunicorn.conf.py#L1-L50)

### Celery Worker Configuration (MODE=worker)

**Queue Architecture:**

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
    WorkerProcess --> TriggerWorkflowQueue
    WorkerProcess --> TriggerRefreshQueue
    WorkerProcess --> RetentionQueue
```
**Sources:** [docker/entrypoint.sh20-58](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L20-L58)

**Autoscaling Configuration:**

When `CELERY_AUTO_SCALE=true`:

| Variable | Default | Description |
| --- | --- | --- |
| `CELERY_MAX_WORKERS` | `nproc` | Maximum workers (scales up to CPU cores) |
| `CELERY_MIN_WORKERS` | `1` | Minimum workers (baseline capacity) |

Command: `celery -A app.celery worker --autoscale=${MAX},${MIN}`

When `CELERY_AUTO_SCALE=false`:

| Variable | Default | Description |
| --- | --- | --- |
| `CELERY_WORKER_AMOUNT` | `1` | Fixed number of workers |
| `CELERY_WORKER_CLASS` | (empty) | Worker implementation (empty=gevent) |

Command: `celery -A app.celery worker -P ${CLASS} -c ${AMOUNT}`

**Sources:** [docker/.env.example184-212](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L184-L212) [docker/entrypoint.sh20-58](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L20-L58)

### Celery Beat Configuration (MODE=beat)

The beat scheduler manages periodic tasks defined in [api/schedule/schedule.py](https://github.com/langgenius/dify/blob/92dbc94f/api/schedule/schedule.py):

**Scheduled Tasks:**

-   `check_upgradable_plugin_task`: Checks for plugin updates every 15 minutes
-   `workflow_schedule_poller_task`: Polls scheduled workflows (configurable interval)
-   `clean_embedding_cache_task`: Cleans embedding cache (optional)
-   `clean_unused_datasets_task`: Removes unused datasets (optional)
-   `clean_messages_task`: Cleans old messages (optional)
-   `workflow_run_cleanup_task`: Cleans old workflow runs (optional)

**Configuration Variables:**

| Variable | Default | Description |
| --- | --- | --- |
| `ENABLE_CHECK_UPGRADABLE_PLUGIN_TASK` | `true` | Enable plugin update checks |
| `ENABLE_WORKFLOW_SCHEDULE_POLLER_TASK` | `true` | Enable workflow scheduling |
| `WORKFLOW_SCHEDULE_POLLER_INTERVAL` | `1` | Polling interval in minutes |
| `WORKFLOW_SCHEDULE_POLLER_BATCH_SIZE` | `100` | Workflows to poll per tick |
| `WORKFLOW_SCHEDULE_MAX_DISPATCH_PER_TICK` | `0` | Max dispatches per tick (0=unlimited) |

**Sources:** [docker/.env.example583-603](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L583-L603) [api/.env.example583-603](https://github.com/langgenius/dify/blob/92dbc94f/api/.env.example#L583-L603) [docker/entrypoint.sh67-70](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L67-L70)

### Environment Variable Categories

The configuration system divides environment variables into logical categories:

**1\. Service URLs and Endpoints** ([docker/.env.example8-59](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L8-L59)):

-   `CONSOLE_API_URL`: Backend URL for console API
-   `CONSOLE_WEB_URL`: Frontend URL for console web
-   `SERVICE_API_URL`: Service API URL shown to users
-   `APP_WEB_URL`: WebApp URL
-   `FILES_URL`: File access URL (signed, with expiration)
-   `INTERNAL_FILES_URL`: Internal file access for plugin daemon

**2\. Database Configuration** ([docker/.env.example232-326](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L232-L326)):

```
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
**3\. Redis Configuration** ([docker/.env.example330-384](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L330-L384)):

```
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
**4\. Storage Backend Selection** ([docker/.env.example406-514](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L406-L514)):

```
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
Supported storage types: `opendal`, `s3`, `aliyun-oss`, `azure-blob`, `baidu-obs`, `clickzetta-volume`, `google-storage`, `huawei-obs`, `oci-storage`, `tencent-cos`, `volcengine-tos`, `supabase`

**5\. Vector Database Selection** ([docker/.env.example520-522](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L520-L522)):

```
VECTOR_STORE=weaviate  # 30+ options supported
VECTOR_INDEX_NAME_PREFIX=Vector_index
```
Supported vector stores: `weaviate`, `oceanbase`, `qdrant`, `milvus`, `myscale`, `relyt`, `pgvector`, `pgvecto-rs`, `chroma`, `opensearch`, `oracle`, `tencent`, `elasticsearch`, `analyticdb`, `couchbase`, `vikingdb`, `opengauss`, `tablestore`, `vastbase`, `tidb`, `tidb_on_qdrant`, `baidu`, `lindorm`, `huawei_cloud`, `upstash`, `matrixone`, `clickzetta`, `alibabacloud_mysql`, `iris`

**Sources:** [docker/.env.example1-1000](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L1-L1000) [api/.env.example1-700](https://github.com/langgenius/dify/blob/92dbc94f/api/.env.example#L1-L700)

### Pydantic Configuration Models

Configuration is loaded into Pydantic models for validation and type safety.

**DifyConfig Composition** ([api/configs/app\_config.py10-43](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/app_config.py#L10-L43)):

```
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
**Key Configuration Classes:**

**SecurityConfig** ([api/configs/feature/\_\_init\_\_.py19-65](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L19-L65)):

-   `SECRET_KEY`: Session cookie signing key (generate with `openssl rand -base64 42`)
-   `RESET_PASSWORD_TOKEN_EXPIRY_MINUTES`: Password reset token TTL (default: 5)
-   `LOGIN_DISABLED`: Disable login checks (default: false)
-   `ADMIN_API_KEY_ENABLE`: Enable admin API key auth (default: false)

**CodeExecutionSandboxConfig** ([api/configs/feature/\_\_init\_\_.py86-174](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L86-L174)):

-   `CODE_EXECUTION_ENDPOINT`: Sandbox service URL (default: `http://sandbox:8194`)
-   `CODE_EXECUTION_API_KEY`: Sandbox API key (default: `dify-sandbox`)
-   `CODE_EXECUTION_CONNECT_TIMEOUT`: Connection timeout (default: 10.0s)
-   `CODE_EXECUTION_READ_TIMEOUT`: Read timeout (default: 60.0s)
-   `CODE_EXECUTION_POOL_MAX_CONNECTIONS`: Max connections (default: 100)
-   `CODE_MAX_STRING_LENGTH`: Max string length (default: 400000)
-   `CODE_MAX_NUMBER`: Max numeric value (default: 9223372036854775807)

**PluginConfig** ([api/configs/feature/\_\_init\_\_.py204-245](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L204-L245)):

-   `PLUGIN_DAEMON_URL`: Plugin daemon URL (default: `http://localhost:5002`)
-   `PLUGIN_DAEMON_KEY`: Plugin daemon authentication key
-   `PLUGIN_DAEMON_TIMEOUT`: Request timeout (default: 600.0s)
-   `INNER_API_KEY_FOR_PLUGIN`: Internal API key for plugin callbacks
-   `PLUGIN_MAX_PACKAGE_SIZE`: Max plugin package size in bytes (default: 15728640)

**Sources:** [api/configs/app\_config.py10-43](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/app_config.py#L10-L43) [api/configs/feature/\_\_init\_\_.py1-600](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L1-L600)

### Configuration Validation Examples

**Field Validation:**

```
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
**Computed Fields:**

Some configuration values are computed from other fields or environment:

```
@computed_field
@property
def SQLALCHEMY_DATABASE_URI_SCHEME(self) -> str:
    if self.DB_TYPE == "mysql":
        return "mysql+aiomysql"
    return "postgresql+psycopg2"
```
**Sources:** [api/configs/feature/\_\_init\_\_.py67-84](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L67-L84) [api/configs/middleware/\_\_init\_\_.py50-150](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/__init__.py#L50-L150)

### Configuration Validation

The Pydantic models provide automatic validation:

```
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
**Sources:** [api/configs/feature/\_\_init\_\_.py19-175](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/feature/__init__.py#L19-L175)

## Service Startup and Initialization

Services start through entrypoint scripts that handle migrations, mode selection, and process launching.

### API Service Entrypoint

The API service entrypoint script handles multiple startup modes:

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
**Sources:** [api/docker/entrypoint.sh1-100](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L1-L100)

### API Mode Configuration

**Gunicorn Server** ([api/docker/entrypoint.sh60-65](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L60-L65)):

```
if [[ "${MODE}" == "api" ]]; then
  exec gunicorn \
    --config gunicorn.conf.py \
    --bind "${DIFY_BIND_ADDRESS}:${DIFY_PORT}" \
    --workers "${SERVER_WORKER_AMOUNT}" \
    --worker-class "${SERVER_WORKER_CLASS}" \
    app:app
fi
```
Configuration parameters:

-   `SERVER_WORKER_AMOUNT`: Number of Gunicorn workers (default: 1)
-   `SERVER_WORKER_CLASS`: Worker type - `gevent` for async, `sync` for synchronous (default: gevent)
-   `SERVER_WORKER_CONNECTIONS`: Max connections per worker (default: 10)
-   `GUNICORN_TIMEOUT`: Request timeout in seconds (default: 360)

**Sources:** [api/docker/entrypoint.sh60-65](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L60-L65) [docker/.env.example153-182](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L153-L182)

### Worker Mode Configuration

**Celery Worker** ([api/docker/entrypoint.sh23-58](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L23-L58)):

The worker mode supports both fixed worker count and autoscaling:

```
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
Configuration parameters:

-   `CELERY_AUTO_SCALE`: Enable autoscaling (default: false)
-   `CELERY_MAX_WORKERS`: Max workers for autoscaling
-   `CELERY_MIN_WORKERS`: Min workers for autoscaling
-   `CELERY_WORKER_AMOUNT`: Fixed worker count (default: 1)
-   `CELERY_WORKER_CLASS`: Worker implementation - empty for gevent, `sync` or `solo` for alternatives

**Queue Routing:**

Different queues handle different task types:

-   `dataset`, `priority_dataset`: Document indexing and dataset operations
-   `workflow`, `priority_pipeline`, `pipeline`: Workflow execution
-   `mail`: Email notifications
-   `plugin`: Plugin operations
-   `app_deletion`: Application cleanup
-   `ops_trace`: Operational tracing
-   `conversation`: Conversation processing
-   `workflow_storage`: Workflow storage operations
-   `schedule_poller`, `schedule_executor`: Scheduled workflow execution
-   `triggered_workflow_dispatcher`: Trigger-based workflow dispatch
-   `trigger_refresh_executor`: Trigger refresh operations
-   `retention`: Data retention cleanup

**Sources:** [api/docker/entrypoint.sh20-58](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L20-L58) [docker/.env.example184-210](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L184-L210)

### Beat Mode Configuration

**Celery Beat Scheduler** ([api/docker/entrypoint.sh67-70](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L67-L70)):

```
if [[ "${MODE}" == "beat" ]]; then
  exec celery -A app.celery beat
fi
```
The beat scheduler manages periodic tasks like:

-   Plugin upgrade checks (every 15 minutes)
-   Workflow schedule polling
-   Dataset queue monitoring
-   Log cleanup
-   Embedding cache cleanup

**Sources:** [api/docker/entrypoint.sh67-70](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L67-L70) [api/.env.example566-582](https://github.com/langgenius/dify/blob/92dbc94f/api/.env.example#L566-L582)

### Database Migration Process

Migrations run automatically before service startup when `MIGRATION_ENABLED=true`:

```
if [[ "${MIGRATION_ENABLED}" == "true" ]]; then
  echo "Running migrations"
  flask upgrade-db

  # Pure migration mode exits after completion
  if [[ "${MODE}" == "migration" ]]; then
    echo "Migration completed, exiting normally"
    exit 0
  fi
fi
```
The migration system uses Alembic through Flask-Migrate:

-   Migration files: [api/migrations/versions/](https://github.com/langgenius/dify/blob/92dbc94f/api/migrations/versions/)
-   Upgrade command: `flask db upgrade`
-   Downgrade command: `flask db downgrade`

**Sources:** [api/docker/entrypoint.sh10-18](https://github.com/langgenius/dify/blob/92dbc94f/api/docker/entrypoint.sh#L10-L18) [api/README.md66-72](https://github.com/langgenius/dify/blob/92dbc94f/api/README.md#L66-L72)

### Web Service Entrypoint

The web service entrypoint script configures Next.js environment variables and starts PM2:

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
**Sources:** [web/docker/entrypoint.sh1-50](https://github.com/langgenius/dify/blob/92dbc94f/web/docker/entrypoint.sh#L1-L50) [web/package.json25](https://github.com/langgenius/dify/blob/92dbc94f/web/package.json#L25-L25)

PM2 configuration:

-   `PM2_INSTANCES`: Number of Node.js instances (default: 2)
-   Process manager handles restarts and load balancing
-   Logs to stdout/stderr for Docker container logs

**Sources:** [web/docker/entrypoint.sh1-50](https://github.com/langgenius/dify/blob/92dbc94f/web/docker/entrypoint.sh#L1-L50) [docker/docker-compose-template.yaml152](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L152-L152)

## Storage and Vector Database Configuration

### Storage Backend Selection

Dify supports multiple storage backends through a unified `STORAGE_TYPE` configuration:

**Storage Type Options:**

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
**Sources:** [docker/.env.example406-529](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L406-L529) [api/configs/middleware/\_\_init\_\_.py1-200](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/__init__.py#L1-L200)

### OpenDAL Storage Configuration

**OpenDAL** provides a unified interface to multiple storage systems. Configuration uses the pattern `OPENDAL_<SCHEME>_<CONFIG>`:

**File System (Default):**

```
STORAGE_TYPE=opendal
OPENDAL_SCHEME=fs
OPENDAL_FS_ROOT=storage
```
**S3-Compatible via OpenDAL:**

```
STORAGE_TYPE=opendal
OPENDAL_SCHEME=s3
OPENDAL_S3_BUCKET=my-bucket
OPENDAL_S3_ENDPOINT=https://s3.amazonaws.com
OPENDAL_S3_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
OPENDAL_S3_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
OPENDAL_S3_REGION=us-east-1
```
**Azure Blob via OpenDAL:**

```
STORAGE_TYPE=opendal
OPENDAL_SCHEME=azblob
OPENDAL_AZBLOB_CONTAINER=my-container
OPENDAL_AZBLOB_ACCOUNT_NAME=myaccount
OPENDAL_AZBLOB_ACCOUNT_KEY=mykey
```
**Sources:** [docker/.env.example407-420](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L407-L420) [api/configs/middleware/storage/opendal\_storage\_config.py1-50](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/storage/opendal_storage_config.py#L1-L50)

### Legacy Storage Backends

For backwards compatibility, direct storage backend types are supported:

**S3 Storage:**

```
STORAGE_TYPE=s3
S3_ENDPOINT=https://s3.amazonaws.com
S3_REGION=us-east-1
S3_BUCKET_NAME=difyai
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
S3_USE_AWS_MANAGED_IAM=false  # Use IAM role instead of keys
```
**Azure Blob Storage:**

```
STORAGE_TYPE=azure-blob
AZURE_BLOB_ACCOUNT_NAME=difyai
AZURE_BLOB_ACCOUNT_KEY=your-key
AZURE_BLOB_CONTAINER_NAME=difyai-container
AZURE_BLOB_ACCOUNT_URL=https://difyai.blob.core.windows.net
```
**Sources:** [docker/.env.example435-465](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L435-L465) [api/configs/middleware/storage/amazon\_s3\_storage\_config.py1-50](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/storage/amazon_s3_storage_config.py#L1-L50)

### Storage Implementation Mapping

**Storage Factory** ([api/extensions/ext\_storage.py1-150](https://github.com/langgenius/dify/blob/92dbc94f/api/extensions/ext_storage.py#L1-L150)):

```
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
**Storage Interface** ([api/extensions/storage/base\_storage.py](https://github.com/langgenius/dify/blob/92dbc94f/api/extensions/storage/base_storage.py)):

All storage implementations provide:

-   `save(filename: str, data: bytes) -> None`
-   `load(filename: str) -> bytes`
-   `load_once(filename: str) -> bytes` # Load and delete
-   `download(filename: str, target_filepath: str) -> None`
-   `exists(filename: str) -> bool`
-   `delete(filename: str) -> None`

**Sources:** [api/extensions/ext\_storage.py1-150](https://github.com/langgenius/dify/blob/92dbc94f/api/extensions/ext_storage.py#L1-L150)

### Vector Database Configuration

Dify supports 30+ vector database backends via the `VECTOR_STORE` environment variable:

**Vector Store Options:**

| Vector Store | Configuration Prefix | Default Port |
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
| `couchbase` | `COUCHBASE_` | \- |
| And 20+ more... |  |  |

**Sources:** [docker/.env.example520-700](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L520-L700) [api/configs/middleware/\_\_init\_\_.py200-400](https://github.com/langgenius/dify/blob/92dbc94f/api/configs/middleware/__init__.py#L200-L400)

### Weaviate Configuration Example

```
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

```
docker compose --profile postgresql --profile weaviate up -d
```
**Sources:** [docker/.env.example535-544](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L535-L544) [docker/docker-compose.yaml600-650](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml#L600-L650)

### Qdrant Configuration Example

```
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

```
docker compose --profile postgresql --profile qdrant up -d
```
**Sources:** [docker/.env.example558-568](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L558-L568) [docker/docker-compose.yaml650-700](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml#L650-L700)

### Vector Database Factory Pattern

**VDB Initialization** ([api/core/rag/datasource/vdb/vector\_factory.py1-150](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_factory.py#L1-L150)):

```
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
**Vector Interface** ([api/core/rag/datasource/vdb/vector\_base.py](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_base.py)):

All vector databases implement:

-   `create(texts: list, embeddings: list, metadatas: list) -> None`
-   `add_texts(texts: list, embeddings: list) -> None`
-   `delete_by_ids(ids: list) -> None`
-   `delete_by_document_id(document_id: str) -> None`
-   `search_by_vector(query_vector: list, top_k: int) -> list`
-   `search_by_full_text(query: str, top_k: int) -> list`

**Sources:** [api/core/rag/datasource/vdb/vector\_factory.py1-150](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_factory.py#L1-L150) [api/core/rag/datasource/vdb/vector\_type.py1-50](https://github.com/langgenius/dify/blob/92dbc94f/api/core/rag/datasource/vdb/vector_type.py#L1-L50)

### Database Migration for Vector Stores

The `vdb-migrate` command migrates data between vector databases:

```
docker exec -it dify-api-1 flask vdb-migrate --scope all
```
**Migration Process:**

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
**Sources:** [api/commands.py161-400](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py#L161-L400)

## Asynchronous Task Processing with Celery

Dify uses Celery for background task processing with Redis as the message broker and result backend.

### Celery Architecture

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
**Sources:** [docker/.env.example366-384](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L366-L384) [docker/entrypoint.sh20-58](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L20-L58)

### Broker and Backend Configuration

**Redis Configuration for Celery:**

```
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
**Broker URL Format:**

-   Standard: `redis://[[username]:password@]host:port/db`
-   Sentinel: `sentinel://:password@sentinel1:26379;sentinel://:password@sentinel2:26379/db`

**Sources:** [docker/.env.example366-384](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L366-L384)

### Task Queue Routing

Tasks are routed to specific queues based on their type:

**Queue Mapping:**

| Queue Name | Task Types | Priority |
| --- | --- | --- |
| `priority_dataset` | High-priority document indexing | High |
| `dataset` | Normal document indexing | Normal |
| `priority_pipeline` | High-priority workflow execution | High |
| `pipeline` | Normal workflow execution | Normal |
| `workflow` | General workflow tasks | Normal |
| `mail` | Email notifications | Low |
| `plugin` | Plugin installation, removal | Normal |
| `app_deletion` | Application cleanup | Low |
| `ops_trace` | Operational tracing | Low |
| `conversation` | Conversation processing | Normal |
| `workflow_storage` | Workflow storage operations | Normal |
| `schedule_poller` | Scheduled workflow polling | Normal |
| `schedule_executor` | Scheduled workflow execution | Normal |
| `triggered_workflow_dispatcher` | Trigger-based workflow dispatch | Normal |
| `trigger_refresh_executor` | Trigger refresh operations | Normal |
| `retention` | Data retention cleanup | Low |

**Task Registration Example** ([api/tasks/](https://github.com/langgenius/dify/blob/92dbc94f/api/tasks/):

```
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
**Sources:** [docker/entrypoint.sh20-58](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L20-L58) [api/tasks/](https://github.com/langgenius/dify/blob/92dbc94f/api/tasks/)

### Worker Autoscaling

**Fixed Worker Count:**

```
# Start 4 workers
CELERY_AUTO_SCALE=false
CELERY_WORKER_AMOUNT=4

# Command: celery -A app.celery worker -c 4 --queues ...
```
**Autoscaling Configuration:**

```
# Autoscale between 1 and 8 workers
CELERY_AUTO_SCALE=true
CELERY_MIN_WORKERS=1
CELERY_MAX_WORKERS=8

# Command: celery -A app.celery worker --autoscale=8,1 --queues ...
```
**Autoscaling Behavior:**

-   Celery monitors queue depth and worker load
-   Scales up when queues have waiting tasks
-   Scales down when workers are idle
-   Min workers maintained as baseline capacity
-   Max workers caps resource usage

**Sources:** [docker/.env.example184-212](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L184-L212) [docker/entrypoint.sh23-45](https://github.com/langgenius/dify/blob/92dbc94f/docker/entrypoint.sh#L23-L45)

### Periodic Task Scheduling (Celery Beat)

**Beat Scheduler Configuration:**

The beat scheduler runs as a separate process (`MODE=beat`) and manages periodic tasks.

**Task Schedule Definition** ([api/schedule/schedule.py](https://github.com/langgenius/dify/blob/92dbc94f/api/schedule/schedule.py)):

```
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
**Scheduled Task Types:**

1.  **Plugin Updates**: Check for plugin upgrades every 15 minutes
2.  **Workflow Scheduling**: Poll scheduled workflows (configurable interval)
3.  **Data Cleanup**: Clean old logs, messages, embeddings
4.  **Monitoring**: Dataset queue monitoring, alerts

**Configuration Variables:**

```
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
**Sources:** [api/.env.example583-603](https://github.com/langgenius/dify/blob/92dbc94f/api/.env.example#L583-L603) [docker/.env.example583-603](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L583-L603)

### Task Result Storage

**Result Backend Configuration:**

```
CELERY_BACKEND=redis
# Results stored in same Redis instance as broker
# Expires after task completion or timeout
```
**Task Result Access:**

```
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
**Sources:** [docker/.env.example366-384](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L366-L384)

### Celery Monitoring

**Flower (Optional):**

Flower provides a web-based monitoring interface for Celery:

```
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
**Built-in Monitoring:**

```
# Inspect active tasks
celery -A app.celery inspect active

# Inspect registered tasks
celery -A app.celery inspect registered

# Check worker stats
celery -A app.celery inspect stats
```
**Sources:** [docker/.env.example366-384](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L366-L384)

### Volume Mounts and Data Persistence

**Critical Volumes:**

| Volume | Mount Point | Purpose |
| --- | --- | --- |
| `./volumes/db/data` | `/var/lib/postgresql/data` | PostgreSQL data directory |
| `./volumes/mysql/data` | `/var/lib/mysql` | MySQL data directory |
| `./volumes/redis/data` | `/data` | Redis persistence |
| `./volumes/app/storage` | `/app/api/storage` | Uploaded files, temp files, plugin storage |
| `./volumes/sandbox/dependencies` | `/dependencies` | Python dependencies for sandbox |
| `./volumes/sandbox/conf` | `/conf` | Sandbox configuration |

**Permission Initialization:**

The `init_permissions` service ensures correct ownership before other services start:

```
init_permissions:
  image: busybox:latest
  command: |
    chown -R 1001:1001 /app/api/storage
  volumes:
    - ./volumes/app/storage:/app/api/storage
  restart: "no"
```
**Sources:** [docker/docker-compose-template.yaml4-20](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L4-L20) [docker/docker-compose-template.yaml56-58](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L56-L58)

### Security Considerations

**SSRF Protection:**

The SSRF proxy service prevents server-side request forgery attacks:

```
ssrf_proxy:
  image: ubuntu/squid:latest
  environment:
    SQUID_CONFIG: |
      http_access deny all
      http_access allow localhost
```
Sandbox and worker services route outbound HTTP requests through this proxy.

**Secret Management:**

Critical secrets to configure:

-   `SECRET_KEY`: Session cookie signing (generate with `openssl rand -base64 42`)
-   `DB_PASSWORD`: Database password
-   `REDIS_PASSWORD`: Redis password
-   `SANDBOX_API_KEY`: Sandbox service API key
-   `PLUGIN_DAEMON_KEY`: Plugin daemon authentication

**Sources:** [docker/.env.example96-99](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L96-L99) [docker/docker-compose-template.yaml259-260](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L259-L260)

### Monitoring and Health

**Health Check Endpoints:**

| Service | Health Check | Description |
| --- | --- | --- |
| API | `http://localhost:5001/health` | Flask application health |
| Web | `http://localhost:3000/` | Next.js server response |
| Sandbox | `http://localhost:8194/health` | Sandbox service health |
| PostgreSQL | `pg_isready` command | Database readiness |
| Redis | `redis-cli ping` command | Cache availability |

**Metrics and Tracing:**

OpenTelemetry support ([docker/.env.example621-638](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L621-L638)):

```
ENABLE_OTEL=false
OTLP_BASE_ENDPOINT=http://localhost:4318
OTEL_EXPORTER_TYPE=otlp
OTEL_SAMPLING_RATE=0.1
```
When enabled, the system exports traces to OTLP endpoints for observability.

**Sources:** [docker/.env.example621-638](https://github.com/langgenius/dify/blob/92dbc94f/docker/.env.example#L621-L638) [docker/docker-compose-template.yaml267](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose-template.yaml#L267-L267)

### Deployment Patterns

**Development Deployment:**

1.  Clone repository
2.  Copy `.env.example` to `.env` in `docker/` directory
3.  Generate `SECRET_KEY`
4.  Start with profiles:

```
cd docker
docker compose --profile postgresql --profile weaviate up -d
```
**Sources:** [api/README.md11-21](https://github.com/langgenius/dify/blob/92dbc94f/api/README.md#L11-L21)

**Production Deployment:**

1.  Use production-grade database and Redis (managed services recommended)
2.  Configure S3-compatible storage instead of local filesystem
3.  Set up reverse proxy (Nginx) with SSL termination
4.  Enable monitoring and logging aggregation
5.  Configure backup strategies for volumes
6.  Set resource limits in docker-compose or Kubernetes

**Kubernetes Deployment:**

For production Kubernetes deployment:

-   Use StatefulSets for databases
-   Use Deployments with HPA for API/worker services
-   Configure PersistentVolumeClaims for storage
-   Use ConfigMaps for configuration
-   Use Secrets for sensitive data
-   Set up Ingress for external access

**Sources:** [docker/docker-compose.yaml1-850](https://github.com/langgenius/dify/blob/92dbc94f/docker/docker-compose.yaml#L1-L850)

### Command-Line Management

The API service provides Flask commands for administrative tasks:

**Reset Password** ([api/commands.py53-88](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py#L53-L88)):

```
docker exec -it dify-api-1 flask reset-password \
  --email user@example.com \
  --new-password newpassword \
  --password-confirm newpassword
```
**Vector Database Migration** ([api/commands.py161-167](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py#L161-L167)):

```
docker exec -it dify-api-1 flask vdb-migrate --scope all
```
**Reset Encryption Keys** ([api/commands.py120-158](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py#L120-L158)):

```
docker exec -it dify-api-1 flask reset-encrypt-key-pair
```
These commands require the API container to be running.

**Sources:** [api/commands.py53-167](https://github.com/langgenius/dify/blob/92dbc94f/api/commands.py#L53-L167) [api/README.md1-117](https://github.com/langgenius/dify/blob/92dbc94f/api/README.md#L1-L117)
