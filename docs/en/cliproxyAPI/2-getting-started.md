# Getting Started

Relevant source files

-   [.dockerignore](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/.dockerignore)
-   [.gitignore](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/.gitignore)
-   [README.md](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md)
-   [README\_CN.md](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README_CN.md)
-   [auths/.gitkeep](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/auths/.gitkeep)
-   [docker-build.ps1](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/docker-build.ps1)
-   [docker-build.sh](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/docker-build.sh)
-   [docker-compose.yml](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/docker-compose.yml)
-   [internal/api/handlers/management/auth\_files.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/api/handlers/management/auth_files.go)

This page guides you through installing and running your first CLI Proxy API server, authenticating with AI providers, and making your first API request. It covers the essential steps to get a working deployment with minimal configuration.

For detailed installation options and deployment scenarios, see [Installation and Deployment](/router-for-me/CLIProxyAPI/2.1-installation-and-deployment). For comprehensive configuration reference, see [Initial Configuration](/router-for-me/CLIProxyAPI/2.2-initial-configuration). For provider-specific authentication guides, see [Authentication Setup](/router-for-me/CLIProxyAPI/2.3-authentication-setup) and [Provider Integration](/router-for-me/CLIProxyAPI/6-provider-integration).

---

## Overview

CLI Proxy API is deployed as a single binary that:

1.  Loads configuration from `config.yaml`
2.  Authenticates with AI providers using OAuth or API keys
3.  Exposes OpenAI/Claude/Gemini-compatible HTTP endpoints
4.  Translates requests between API formats
5.  Routes requests to the appropriate AI provider

The server supports multiple storage backends for credentials and configuration, enabling deployment from single-server file-based systems to distributed database-backed configurations.

---

## Deployment Paths

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
**Sources:** [cmd/server/main.go50-482](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L50-L482) [internal/cmd/run.go19-56](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/run.go#L19-L56)

---

## Quick Start: File Storage Mode

This is the simplest deployment path for development and single-server deployments.

### Step 1: Obtain the Binary

Download the binary from the releases page or build from source:

```
go build -o cliproxy-api ./cmd/server
```
### Step 2: Create Configuration File

Create `config.yaml` in the working directory. A minimal configuration:

```
port: 8080log_level: infoauth_dir: ./auths
```
The server will create the `auths/` directory automatically on first run.

**Sources:** [cmd/server/main.go367-377](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L367-L377) [internal/config](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/config)/

### Step 3: Authenticate with a Provider

Use the built-in OAuth flows to authenticate with AI providers. Example for Google Gemini:

```
./cliproxy-api --login
```
This command:

1.  Opens a browser for Google OAuth
2.  Prompts for GCP project selection
3.  Completes Gemini CLI onboarding
4.  Saves tokens to `auths/gemini-{email}-{project}.json`

For other providers:

-   `--claude-login` for Anthropic Claude
-   `--codex-login` for OpenAI Codex
-   `--antigravity-login` for Antigravity
-   `--qwen-login` for Qwen
-   `--iflow-login` for iFlow

**Sources:** [cmd/server/main.go71-84](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L71-L84) [internal/cmd/login.go43-183](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/login.go#L43-L183)

### Step 4: Start the Server

```
./cliproxy-api
```
The server will:

1.  Load `config.yaml`
2.  Scan `auths/` directory for credentials
3.  Register executors for available providers
4.  Start the HTTP server on the configured port
5.  Begin watching for configuration changes

Expected output:

```
CLIProxyAPI Version: {version}, Commit: {commit}, BuiltAt: {date}
INFO[0000] CLIProxyAPI Version: {version}, Commit: {commit}, BuiltAt: {date}
INFO[0000] Server listening on :8080
```
**Sources:** [internal/cmd/run.go27-56](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/run.go#L27-L56) [cmd/server/main.go478-480](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L478-L480)

### Step 5: Make Your First Request

Use the OpenAI-compatible endpoint:

```
curl -X POST http://localhost:8080/v1/chat/completions \  -H "Content-Type: application/json" \  -d '{    "model": "gemini-2.0-flash-exp",    "messages": [      {"role": "user", "content": "Hello, world!"}    ]  }'
```
Or use the Gemini-compatible endpoint:

```
curl -X POST http://localhost:8080/v1beta/models/gemini-2.0-flash-exp:generateContent \  -H "Content-Type: application/json" \  -d '{    "contents": [      {"parts": [{"text": "Hello, world!"}]}    ]  }'
```
The server will automatically select an available credential for the requested model and translate the request to the appropriate provider format.

**Sources:** [internal/api](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/api)/

---

## Startup Flow and Service Initialization

> **[Mermaid sequence]**
> *(图表结构无法解析)*

**Sources:** [cmd/server/main.go50-482](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L50-L482) [internal/cmd/run.go27-56](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/run.go#L27-L56)

---

## Authentication and Credential Flow

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
**Sources:** [internal/cmd/login.go51-183](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/login.go#L51-L183) [sdk/auth](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/auth)/

---

## Storage Backend Configuration

The server detects the storage backend based on environment variables. Only one backend can be active at a time, with the following precedence:

| Priority | Backend | Environment Variable | Description |
| --- | --- | --- | --- |
| 1 | PostgreSQL | `PGSTORE_DSN` | Database connection string |
| 2 | Object Storage | `OBJECTSTORE_ENDPOINT` | S3/MinIO endpoint URL |
| 3 | Git | `GITSTORE_GIT_URL` | Git repository URL |
| 4 | File | *(none)* | Local file system (default) |

### File Storage (Default)

No configuration required. The server uses the current working directory or `auth_dir` from `config.yaml`.

```
./cliproxy-api
```
Config location: `./config.yaml`
Auth location: `./auths/*.json`

### PostgreSQL Storage

Set the database connection string:

```
export PGSTORE_DSN="postgres://user:password@localhost:5432/cliproxy?sslmode=disable"export PGSTORE_LOCAL_PATH="/var/lib/cliproxy"  # Optional: local spool directory./cliproxy-api
```
The server will:

1.  Create tables: `config_store`, `auth_store`
2.  Sync database ↔ local spool directory
3.  Use local files for file-based operations
4.  Persist changes back to database

Config location: `{PGSTORE_LOCAL_PATH}/pgstore/config/config.yaml`
Auth location: `{PGSTORE_LOCAL_PATH}/pgstore/auths/*.json`

**Sources:** [cmd/server/main.go166-255](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L166-L255) [internal/store/postgresstore.go49-100](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/store/postgresstore.go#L49-L100)

### Git Storage

Set the repository URL and credentials:

```
export GITSTORE_GIT_URL="https://github.com/user/cliproxy-config.git"export GITSTORE_GIT_USERNAME="git"export GITSTORE_GIT_TOKEN="ghp_xxxxxxxxxxxx"export GITSTORE_LOCAL_PATH="/var/lib/cliproxy"  # Optional./cliproxy-api
```
The server will:

1.  Clone the repository (or pull if exists)
2.  Use local clone for operations
3.  Commit and force-push changes
4.  Squash history to single commits

Config location: `{GITSTORE_LOCAL_PATH}/gitstore/config/config.yaml`
Auth location: `{GITSTORE_LOCAL_PATH}/gitstore/auths/*.json`

**Sources:** [cmd/server/main.go186-366](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L186-L366) [internal/store/gitstore.go88-209](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/store/gitstore.go#L88-L209)

### Object Storage (S3/MinIO)

Set the S3-compatible endpoint:

```
export OBJECTSTORE_ENDPOINT="https://s3.amazonaws.com"export OBJECTSTORE_ACCESS_KEY="AKIAIOSFODNN7EXAMPLE"export OBJECTSTORE_SECRET_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"export OBJECTSTORE_BUCKET="cliproxy-config"export OBJECTSTORE_LOCAL_PATH="/var/lib/cliproxy"  # Optional./cliproxy-api
```
The server will:

1.  Connect to S3/MinIO
2.  Sync bucket ↔ local mirror
3.  Use local files for operations
4.  Upload changes to bucket

Config location: `{OBJECTSTORE_LOCAL_PATH}/objectstore/config.yaml`
Auth location: `{OBJECTSTORE_LOCAL_PATH}/objectstore/auths/*.json`

**Sources:** [cmd/server/main.go199-323](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L199-L323) [internal/store/objectstore.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/store/objectstore.go)/

---

## Provider Authentication Examples

### Google Gemini (OAuth)

```
./cliproxy-api --login
```
Interactive flow:

1.  Browser opens for Google OAuth
2.  Select GCP project or type `ALL` for all projects
3.  Onboarding completes automatically
4.  Token saved to `auths/gemini-{email}-{project}.json`

Multiple projects can be activated by selecting `ALL` or providing a comma-separated list.

**Sources:** [internal/cmd/login.go51-183](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/login.go#L51-L183) [cmd/server/main.go453-455](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L453-L455)

### Anthropic Claude (OAuth)

```
./cliproxy-api --claude-login
```
Uses PKCE OAuth flow. Token saved to `auths/claude-{email}.json`.

**Sources:** [cmd/server/main.go463-464](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L463-L464)

### OpenAI Codex (OAuth)

```
./cliproxy-api --codex-login
```
Uses account hash for identification. Token saved to `auths/codex-{hash}.json`.

**Sources:** [cmd/server/main.go459-461](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L459-L461)

### Vertex AI (Service Account)

```
./cliproxy-api --vertex-import /path/to/service-account.json
```
Imports GCP service account key. Saved to `auths/vertex-{project_id}.json`.

**Sources:** [cmd/server/main.go450-452](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L450-L452)

### API Key Configuration

For providers supporting API keys, add them directly to `config.yaml`:

```
gemini_api_keys:  - "AIzaSy..."claude_api_keys:  - "sk-ant-..."codex_api_keys:  - "sk-..."
```
The server synthesizes these into `Auth` records automatically on startup.

**Sources:** [internal/config](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/config)/

---

## Hot Reload and Configuration Updates

The server watches for changes to configuration and authentication files and reloads automatically without restart:

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
Changes take effect immediately without dropping existing connections.

**Sources:** [sdk/cliproxy](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/cliproxy)/

---

## Request Processing Flow

> **[Mermaid sequence]**
> *(图表结构无法解析)*

**Sources:** [internal/api](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/api)/

---

## Verification Checklist

After completing the quick start, verify your deployment:

-   [ ]  Server starts without errors
-   [ ]  Configuration file is loaded (check logs for config path)
-   [ ]  At least one provider is authenticated (check logs for "registered X auths")
-   [ ]  HTTP server is listening (check logs for "listening on :port")
-   [ ]  Test request completes successfully
-   [ ]  File watcher is active (modify config, check for reload message)

Common issues:

-   **Port already in use**: Change `port` in `config.yaml`
-   **No auths found**: Run `--login` or equivalent for at least one provider
-   **Permission denied**: Ensure write access to `auth_dir` and config file location
-   **Storage backend errors**: Check environment variable syntax and connectivity

**Sources:** [internal/cmd/run.go27-56](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/cmd/run.go#L27-L56)

---

## Next Steps

Now that you have a working server:

1.  **Configure additional providers**: See [Authentication Setup](/router-for-me/CLIProxyAPI/2.3-authentication-setup) for provider-specific guides
2.  **Customize configuration**: See [Initial Configuration](/router-for-me/CLIProxyAPI/2.2-initial-configuration) for all available options
3.  **Set up model mapping**: See [Model Mapping and Exclusion](/router-for-me/CLIProxyAPI/8.2-model-mapping-and-exclusion) to create model aliases
4.  **Enable advanced features**: See [Advanced Features](/router-for-me/CLIProxyAPI/8-advanced-features) for thinking configuration, routing strategies, and monitoring
5.  **Deploy to production**: See [Cloud-Native Deployment](/router-for-me/CLIProxyAPI/10.2-cloud-native-deployment) for distributed deployments

For comprehensive API documentation, see [API Reference](/router-for-me/CLIProxyAPI/4-api-reference).

**Sources:** All sections above
