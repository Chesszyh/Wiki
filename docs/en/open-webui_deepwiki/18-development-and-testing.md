# Development and Testing

Relevant source files

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

This page documents the development environment setup, testing infrastructure, and build system for Open WebUI. It covers local development workflows, testing strategies, and continuous integration practices.

For production deployment configuration, see [Installation and Deployment](/open-webui/open-webui/3-installation-and-deployment). For detailed architecture of specific subsystems being developed, see [Architecture Overview](/open-webui/open-webui/2-architecture-overview).

## Development Environment

Open WebUI uses a dual-stack development approach with separate but coordinated frontend (Node.js/SvelteKit) and backend (Python/FastAPI) development servers.

### Development Stack Overview

```mermaid
flowchart TD
    Ollama["Ollama ServerPort 11434"]
    NPM["npm/Node.js>=18.13.0"]
    Vite["Vite Dev ServerPort 5173"]
    SvelteKit["SvelteKitHMR + SSR"]
    Uvicorn["uvicornPort 8080"]
    Python["Python3.11-3.12"]
    FastAPI["FastAPIopen_webui.main:app"]
    DB["SQLite/PostgreSQLDatabase"]
    Redis["RedisOptional"]

    NPM --> Vite
    Vite --> SvelteKit
    SvelteKit --> Uvicorn
    Python --> Uvicorn
    Uvicorn --> FastAPI
    FastAPI --> Ollama
    FastAPI --> DB
    FastAPI --> Redis
```
**Sources:** [package.json1-153](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L1-L153) [pyproject.toml1-210](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L1-L210) [backend/requirements.txt1-156](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L1-L156)

### Local Development Setup

Development requires both frontend and backend servers running simultaneously. The frontend development server proxies API requests to the backend server.

**Frontend Development Server:**

```
npm run dev          # Starts Vite on port 5173
npm run dev:5050     # Alternative port 5050
```
The `dev` script executes `npm run pyodide:fetch && vite dev --host`, which:

1.  Downloads Pyodide assets via `scripts/prepare-pyodide.js`
2.  Starts Vite dev server with hot module replacement (HMR)
3.  Enables network access via `--host` flag

**Backend Development Server:**

```
open-webui serve    # Starts uvicorn on port 8080
```
This command launches the FastAPI application defined in [backend/open\_webui/main.py](https://github.com/open-webui/open-webui/blob/a7271532/backend/open_webui/main.py) using uvicorn with automatic reload on code changes.

**Environment Variables:** Development requires minimal environment variables for local operation:

-   `WEBUI_SECRET_KEY`: Session encryption key (auto-generated if not set)
-   `OLLAMA_BASE_URL`: Connection to Ollama (defaults to `http://localhost:11434`)
-   `DATABASE_URL`: Database connection (defaults to SQLite in `./data` directory)

**Sources:** [package.json5-12](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L5-L12) [pyproject.toml164-165](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L164-L165)

### Development Scripts

The [package.json](https://github.com/open-webui/open-webui/blob/a7271532/package.json) defines comprehensive development scripts:

| Script | Purpose | Command |
| --- | --- | --- |
| `dev` | Start frontend dev server | `vite dev --host` |
| `build` | Production frontend build | `vite build` |
| `build:watch` | Watch mode for frontend | `vite build --watch` |
| `check` | Type checking | `svelte-check` |
| `lint` | Lint all code | Frontend + types + backend |
| `lint:frontend` | ESLint for frontend | `eslint . --fix` |
| `lint:backend` | Pylint for backend | `pylint backend/` |
| `format` | Format frontend code | `prettier --write` |
| `format:backend` | Format backend code | `black . --exclude venv` |
| `test:frontend` | Run frontend tests | `vitest --passWithNoTests` |
| `cy:open` | Open Cypress GUI | `cypress open` |

**Backend Development Commands:**

-   `black .`: Auto-format Python code to PEP 8 standards
-   `pylint backend/`: Static analysis for Python code quality
-   `pytest`: Run backend unit and integration tests

**Sources:** [package.json13-22](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L13-L22)

## Testing Infrastructure

Open WebUI implements a comprehensive testing strategy covering unit tests, integration tests, and end-to-end tests across both frontend and backend systems.

### Testing Architecture

```mermaid
flowchart TD
    Vitest["vitestUnit Tests"]
    Cypress["CypressE2E Tests"]
    TypeCheck["svelte-checkType Validation"]
    Pytest["pytestUnit + Integration"]
    MockAWS["motoS3 Mocking"]
    MockGCS["gcp-storage-emulatorGCS Mocking"]
    MockAzure["unittest.mockAzure Mocking"]
    PytestDocker["pytest-dockerContainer Tests"]
    ComposeStack["Docker Compose Stack"]
    OllamaTest["Ollama Test Server"]
    PostgresTest["PostgreSQL Test DB"]
    TmpPath["tmp_pathPytest Fixture"]
    Monkeypatch["monkeypatchEnvironment Mocking"]

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
**Sources:** [package.json34-51](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L34-L51) [backend/requirements.txt133-136](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L133-L136) [backend/open\_webui/test/apps/webui/storage/test\_provider.py1-350](https://github.com/open-webui/open-webui/blob/a7271532/backend/open_webui/test/apps/webui/storage/test_provider.py#L1-L350)

### Backend Testing Framework

The backend uses `pytest` as the primary testing framework with specialized fixtures and mocking libraries for external dependencies.

**Test Organization:**

```
backend/open_webui/test/
├── apps/
│   └── webui/
│       └── storage/
│           └── test_provider.py  # Storage provider tests
└── [other test modules]
```
**Storage Provider Testing Example:**

The [test\_provider.py](https://github.com/open-webui/open-webui/blob/a7271532/test_provider.py) demonstrates comprehensive testing patterns:

1.  **Fixture-based Setup:** The `mock_upload_dir` fixture uses `monkeypatch` and `tmp_path` to create isolated test directories:

```
def mock_upload_dir(monkeypatch, tmp_path):
    directory = tmp_path / "uploads"
    directory.mkdir()
    monkeypatch.setattr(provider, "UPLOAD_DIR", str(directory))
    return directory
```
2.  **Mock External Services:** Uses `moto` for AWS S3, `gcp-storage-emulator` for Google Cloud Storage, and `unittest.mock` for Azure:

```
@mock_aws
class TestS3StorageProvider:
    def __init__(self):
        self.s3_client = boto3.resource("s3", region_name="us-east-1")
```
3.  **Test Class Structure:** Organized by provider with shared test patterns:
    -   `test_upload_file`: Validates file upload to both local and cloud storage
    -   `test_get_file`: Verifies file retrieval and download
    -   `test_delete_file`: Confirms deletion from both storage layers
    -   `test_delete_all_files`: Tests bulk deletion operations

**Running Backend Tests:**

```
cd backend
PYTHONPATH=. pytest . -o log_cli=true -o log_cli_level=INFO
```
**Sources:** [backend/open\_webui/test/apps/webui/storage/test\_provider.py1-350](https://github.com/open-webui/open-webui/blob/a7271532/backend/open_webui/test/apps/webui/storage/test_provider.py#L1-L350) [backend/requirements.txt133-136](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L133-L136)

### Frontend Testing Framework

Frontend testing uses `vitest` for unit tests and `cypress` for end-to-end integration tests.

**Vitest Configuration:**

-   Runs via `npm run test:frontend`
-   Uses `--passWithNoTests` flag to allow builds without tests
-   Integrates with SvelteKit's component testing

**Cypress E2E Testing:**

```
npm run cy:open      # Opens interactive Cypress GUI
cypress run          # Runs tests headlessly (CI mode)
```
Cypress tests validate full user workflows against a running Docker Compose stack including Open WebUI, Ollama, and test services.

**Sources:** [package.json20-21](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L20-L21) [package.json34](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L34-L34)

### Integration Testing Pipeline

The disabled [.github/workflows/integration-test.disabled](https://github.com/open-webui/open-webui/blob/a7271532/.github/workflows/integration-test.disabled) shows the full integration testing approach:

```mermaid
flowchart TD
    Checkout["Checkout Repository"]
    BuildStack["Build Docker Composeopen-webui + ollama + test services"]
    WaitOllama["Wait for OllamaHealth Check"]
    PreloadModel["Preload Test Modelqwen:0.5b-chat-v1.5-q2_K"]
    CypressRun["Run Cypress TestsBrowser: Chrome"]
    UploadArtifacts["Upload Videos + Logs"]
    SQLiteTest["SQLite TestDefault Database"]
    PostgresTest["PostgreSQL TestService Container"]
    UvicornSQLite["Start BackendSQLite Mode"]
    HealthCheckSQLite["Health CheckGET /api/config"]
    UvicornPostgres["Start BackendPostgreSQL Mode"]
    HealthCheckPostgres["Health CheckGET /health/db"]
    ReconnectTest["Test DB Reconnectionpg_terminate_backend"]

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
**Key Testing Stages:**

1.  **Cypress E2E Tests (Lines 14-81):**

    -   Builds full stack: `docker-compose.yaml` + `docker-compose.api.yaml` + test services
    -   Waits for Ollama health endpoint (`http://localhost:11434`)
    -   Preloads lightweight model for faster tests (`qwen:0.5b-chat-v1.5-q2_K`)
    -   Runs Cypress against `http://localhost:3000`
    -   Uploads test videos and logs as artifacts
2.  **Migration Tests (Lines 105-256):**

    -   Tests SQLite database initialization and stability
    -   Tests PostgreSQL connection and automatic reconnection
    -   Validates database pool management under connection failures
    -   Uses `pg_terminate_backend` to simulate connection loss

**Environment Variables for Testing:**

```
WEBUI_SECRET_KEY=secret-key
GLOBAL_LOG_LEVEL=debug
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
DATABASE_POOL_SIZE=10
DATABASE_POOL_MAX_OVERFLOW=10
DATABASE_POOL_TIMEOUT=30
```
**Sources:** [.github/workflows/integration-test.disabled1-256](https://github.com/open-webui/open-webui/blob/a7271532/.github/workflows/integration-test.disabled#L1-L256) [docker-compose.playwright.yaml1-11](https://github.com/open-webui/open-webui/blob/a7271532/docker-compose.playwright.yaml#L1-L11)

### Playwright Testing

Playwright is used for web content loading with browser automation. The [docker-compose.playwright.yaml](https://github.com/open-webui/open-webui/blob/a7271532/docker-compose.playwright.yaml) defines a separate container for Playwright operations:

```
playwright:
  image: mcr.microsoft.com/playwright:v1.57.0-noble
  command: npx -y playwright@1.57.0 run-server --port 3000
```
**Critical Version Matching:** The Playwright container version (`v1.57.0`) **must match** the version in [backend/requirements.txt123](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L123-L123) and [pyproject.toml149](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L149-L149) Version mismatches cause test failures.

**Environment Configuration:**

```
WEB_LOADER_ENGINE=playwright
PLAYWRIGHT_WS_URL=ws://playwright:3000
```
**Sources:** [docker-compose.playwright.yaml1-11](https://github.com/open-webui/open-webui/blob/a7271532/docker-compose.playwright.yaml#L1-L11) [backend/requirements.txt123](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L123-L123)

## Build System

Open WebUI uses separate build systems for frontend (Vite) and backend (Hatchling) with integrated asset bundling.

### Build Pipeline Architecture

```mermaid
flowchart TD
    ViteConfig["vite.config.ts"]
    SvelteComponents["Svelte Componentssrc/**/*.svelte"]
    Assets["Static Assetsstatic/**"]
    ViteBuild["vite build"]
    FrontendBundle["build/**Static Files"]
    PyProject["pyproject.tomlhatchling config"]
    BackendSrc["backend/**/*.py"]
    HatchBuild["hatch build"]
    Wheel["dist/*.whlPython Package"]
    PyodideScript["scripts/prepare-pyodide.js"]
    PyodideAssets["Pyodide RuntimePython in Browser"]
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
**Sources:** [package.json8-12](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L8-L12) [pyproject.toml167-197](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L167-L197)

### Frontend Build System

**Vite Configuration:** The frontend build uses Vite with SvelteKit adapter:

-   Dev server: Fast HMR with hot module replacement
-   Build: Optimized production bundles with code splitting
-   Adapter: `@sveltejs/adapter-static` for static site generation or `@sveltejs/adapter-node` for Node.js deployment

**Build Scripts:**

```
npm run build           # Production build
npm run build:watch     # Watch mode for development
npm run preview         # Preview production build
```
**Static Asset Preparation:** The `pyodide:fetch` script ([package.json22](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L22-L22)) downloads Pyodide assets before builds:

```
node scripts/prepare-pyodide.js
```
This ensures Python runtime is available for in-browser code execution in [CodeBlock components](/open-webui/open-webui/5.4-code-block-execution).

**TypeScript Checking:**

```
npm run check              # One-time type check
npm run check:watch        # Continuous type checking
```
Uses `svelte-check` with TypeScript configuration to validate component types.

**Sources:** [package.json8-12](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L8-L12) [package.json22](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L22-L22) [package.json24-28](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L24-L28)

### Backend Build System

**Hatchling Configuration:**

The [pyproject.toml](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml) uses Hatchling as the build backend with custom configuration:

```
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
**Key Build Features:**

1.  **Source Mapping:** Backend code from `backend/` is packaged as `open_webui` module
2.  **Frontend Integration:** Compiled frontend assets from `build/` are included in the wheel at `open_webui/frontend`
3.  **Changelog Bundling:** [CHANGELOG.md](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md) is embedded for runtime version display
4.  **Version Extraction:** Version is read from [package.json](https://github.com/open-webui/open-webui/blob/a7271532/package.json) via pattern matching:

```
[tool.hatch.version]
path = "package.json"
pattern = '"version":\s*"(?P<version>[^"]+)"'
```
**Building the Package:**

```
# Using hatch
hatch build

# Generates: dist/open_webui-{version}-py3-none-any.whl
```
**Entry Point:** The package defines a console script entry point:

```
[project.scripts]
open-webui = "open_webui:app"
```
This allows running `open-webui serve` after installation.

**Sources:** [pyproject.toml167-197](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L167-L197)

### Dependency Management

**Frontend Dependencies:** Managed via `package.json` and `package-lock.json` with NPM:

-   Production dependencies: 89 packages (Svelte, Tiptap, marked, etc.)
-   Development dependencies: 32 packages (Vite, ESLint, Prettier, etc.)

**Backend Dependencies:** Managed via [requirements.txt](https://github.com/open-webui/open-webui/blob/a7271532/requirements.txt) and [pyproject.toml](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml):

-   Core dependencies: FastAPI, uvicorn, SQLAlchemy, etc.
-   AI/ML libraries: transformers, sentence-transformers, langchain
-   Database drivers: psycopg2-binary, pymongo, redis
-   Optional dependencies: Defined in `[project.optional-dependencies]`

**Optional Feature Dependencies:**

```
[project.optional-dependencies]
postgres = ["psycopg2-binary==2.9.11", "pgvector==0.4.2"]
all = [
    "pymongo", "pytest", "playwright==1.57.0",
    "qdrant-client", "pymilvus", "weaviate-client",
    "elasticsearch", "pinecone", "oracledb", ...
]
```
**Minimal Dependencies:** A minimal requirements file exists at [backend/requirements-min.txt](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements-min.txt) for lightweight deployments with only essential dependencies.

**Sources:** [package.json54-152](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L54-L152) [backend/requirements.txt1-156](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements.txt#L1-L156) [pyproject.toml8-162](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L8-L162) [backend/requirements-min.txt1-52](https://github.com/open-webui/open-webui/blob/a7271532/backend/requirements-min.txt#L1-L52)

## Version Management and Changelog

Open WebUI uses semantic versioning with a centralized version source and structured changelog.

### Version System Architecture

```mermaid
flowchart TD
    PackageJSON["package.jsonSingle Source of Truthversion: 0.6.43"]
    Hatchling["hatchlingPython Package Version"]
    ConstantsTS["src/lib/constants.tsWEBUI_VERSION"]
    MainPy["backend/open_webui/main.pyVERSION constant"]
    ChangelogMD["CHANGELOG.mdKeep a Changelog Format"]
    ChangelogAPI["GET /api/v1/changelogParsed Changelog"]
    ChangelogModal["ChangelogModal.svelteVersion Update UI"]
    ConfigAPI["GET /api/configReturns version"]
    LocalStorage["localStorage.versionClient-side Cache"]
    VersionCompare["Version ComparisonShow Modal if New"]

    PackageJSON --> Hatchling
    PackageJSON --> ConstantsTS
    ChangelogMD --> ChangelogAPI
    ChangelogAPI --> ChangelogModal
    ConfigAPI --> VersionCompare
    LocalStorage --> VersionCompare
    VersionCompare --> ChangelogModal
```
**Sources:** [package.json3](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L3-L3) [pyproject.toml179-180](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L179-L180) [CHANGELOG.md1-10](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md#L1-L10) [src/lib/components/ChangelogModal.svelte1-118](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/components/ChangelogModal.svelte#L1-L118)

### Changelog Format

The [CHANGELOG.md](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md) follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format with semantic versioning:

```
# Changelog

## [0.6.43] - 2025-12-22

### Added
- Feature descriptions with commit links
- Environment variable additions

### Fixed
- Bug fix descriptions with issue references

### Changed
- Breaking changes and modifications
- Dependency updates

### Removed
- Deprecated feature removals
```
**Changelog Structure:**

-   **Version Headers:** `## [version] - YYYY-MM-DD` format
-   **Categories:** Added, Fixed, Changed, Removed
-   **Entries:** Emoji prefix + description + links to commits/issues/PRs
-   **References:** GitHub commit hashes, issue numbers, PR numbers

**Category Semantics:**

-   **Added:** New features, capabilities, environment variables
-   **Fixed:** Bug fixes, error corrections, stability improvements
-   **Changed:** Breaking changes, behavior modifications, defaults
-   **Removed:** Deprecated features, cleanup

**Sources:** [CHANGELOG.md1-1170](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md#L1-L1170)

### Version Display UI

The [ChangelogModal.svelte](https://github.com/open-webui/open-webui/blob/a7271532/ChangelogModal.svelte) component displays version information and changelog to users:

**Modal Trigger Logic:**

1.  Fetch current version from `/api/config`
2.  Compare with `localStorage.version`
3.  Display modal if versions differ
4.  Update `localStorage.version` on dismiss

**Changelog Rendering:**

```
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
**Color Coding:**

-   **Added:** Blue background (`bg-blue-500/20`)
-   **Fixed:** Green background (`bg-green-500/20`)
-   **Changed:** Yellow background (`bg-yellow-500/20`)
-   **Removed:** Red background (`bg-red-500/20`)

**User Settings Persistence:** When user dismisses modal, version is saved to both localStorage and user settings:

```
localStorage.version = $config.version;
await settings.set({ ...$settings, ...{ version: $config.version } });
await updateUserSettings(localStorage.token, { ui: $settings });
```
**Sources:** [src/lib/components/ChangelogModal.svelte1-118](https://github.com/open-webui/open-webui/blob/a7271532/src/lib/components/ChangelogModal.svelte#L1-L118)

### Release Process

Based on the changelog structure and versioning system, the release process follows:

1.  **Update Version:** Modify `version` field in [package.json](https://github.com/open-webui/open-webui/blob/a7271532/package.json)
2.  **Update Changelog:** Add new version section in [CHANGELOG.md](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md) with date
3.  **Build Frontend:** `npm run build` generates static assets
4.  **Build Backend:** `hatch build` creates Python wheel with embedded frontend
5.  **Docker Build:** Multi-stage build creates production image
6.  **Tag Release:** Git tag matching version number
7.  **Deploy:** Docker image pushed to registry

**Semantic Versioning Rules:**

-   **Major (X.0.0):** Breaking changes, incompatible API changes
-   **Minor (0.X.0):** New features, backward-compatible additions
-   **Patch (0.0.X):** Bug fixes, backward-compatible patches

**Sources:** [CHANGELOG.md1-10](https://github.com/open-webui/open-webui/blob/a7271532/CHANGELOG.md#L1-L10) [package.json3](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L3-L3) [pyproject.toml179-180](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L179-L180)

## Code Quality Tools

Open WebUI enforces code quality through linting, formatting, and type checking tools.

### Frontend Code Quality

**ESLint Configuration:**

```
npm run lint:frontend    # Runs eslint with --fix
```
ESLint configuration includes:

-   `@typescript-eslint/eslint-plugin`: TypeScript-specific rules
-   `eslint-plugin-svelte`: Svelte component linting
-   `eslint-plugin-cypress`: Cypress test linting
-   `eslint-config-prettier`: Disables conflicting rules with Prettier

**Prettier Formatting:**

```
npm run format           # Formats all frontend files
```
Formats JavaScript, TypeScript, Svelte, CSS, Markdown, HTML, and JSON files with consistent style.

**TypeScript Checking:**

```
npm run check           # Type checks without emitting files
```
Uses `svelte-check` to validate TypeScript in Svelte components and TypeScript files.

**Sources:** [package.json13-18](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L13-L18) [package.json24-28](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L24-L28)

### Backend Code Quality

**Black Formatting:**

```
npm run format:backend   # Auto-formats Python code
black . --exclude venv
```
Black enforces consistent Python code style with zero configuration. Excludes virtual environment directories.

**Pylint Static Analysis:**

```
npm run lint:backend     # Runs pylint on backend
pylint backend/
```
Pylint performs static analysis checking for:

-   Code errors and bugs
-   Code smells and bad practices
-   PEP 8 compliance
-   Documentation completeness

**Codespell Configuration:** The [pyproject.toml199-204](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L199-L204) defines spell checking rules:

```
[tool.codespell]
skip = '.git*,*.svg,package-lock.json,i18n,*.lock,*.css'
check-hidden = true
ignore-words-list = 'ans'
```
**Sources:** [package.json16-18](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L16-L18) [pyproject.toml199-204](https://github.com/open-webui/open-webui/blob/a7271532/pyproject.toml#L199-L204)

## Development Workflow Best Practices

### Making Code Changes

1.  **Frontend Changes:**

    ```
    npm run dev              # Start dev server
    npm run check:watch      # Run type checking in background
    # Make changes, see live updates
    npm run lint:frontend    # Fix linting issues
    npm run format           # Format code
    ```

2.  **Backend Changes:**

    ```
    open-webui serve         # Start backend server
    # Make changes, server auto-reloads
    black .                  # Format Python code
    pylint backend/          # Check for issues
    pytest                   # Run tests
    ```

3.  **Full Stack Changes:**

    -   Start both frontend (`npm run dev`) and backend (`open-webui serve`)
    -   Frontend proxies API requests to backend
    -   Both servers support hot reloading

**Sources:** [package.json5-18](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L5-L18)

### Testing Before Commit

**Recommended Test Flow:**

```
# Frontend
npm run check            # Type checking
npm run lint            # Lint all (frontend + types + backend)
npm run format          # Format frontend
npm run test:frontend   # Run vitest

# Backend
npm run format:backend  # Format Python
npm run lint:backend    # Lint Python
cd backend && pytest    # Run Python tests
```
**Integration Testing:** For full integration tests with Docker:

```
# Build and test full stack
docker compose up --build

# Run Cypress tests (when enabled)
npm run cy:open
```
**Sources:** [package.json13-21](https://github.com/open-webui/open-webui/blob/a7271532/package.json#L13-L21) [.github/workflows/integration-test.disabled29-60](https://github.com/open-webui/open-webui/blob/a7271532/.github/workflows/integration-test.disabled#L29-L60)

### Database Migration Testing

When making database schema changes, test migrations with both SQLite and PostgreSQL:

```
# Test with SQLite (default)
WEBUI_SECRET_KEY=test open-webui serve

# Test with PostgreSQL
DATABASE_URL=postgresql://user:pass@localhost:5432/db open-webui serve
```
Verify:

-   Application starts successfully
-   Health check returns 200: `curl http://localhost:8080/health/db`
-   Database reconnection works after connection loss

**Sources:** [.github/workflows/integration-test.disabled156-229](https://github.com/open-webui/open-webui/blob/a7271532/.github/workflows/integration-test.disabled#L156-L229)
