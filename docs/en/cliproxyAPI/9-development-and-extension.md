# Development and Extension

Relevant source files

-   [docs/sdk-access.md](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/docs/sdk-access.md)
-   [docs/sdk-access\_CN.md](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/docs/sdk-access_CN.md)
-   [internal/access/config\_access/provider.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/access/config_access/provider.go)
-   [internal/access/reconcile.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/internal/access/reconcile.go)
-   [sdk/access/errors.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/access/errors.go)
-   [sdk/access/manager.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/access/manager.go)
-   [sdk/access/registry.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/access/registry.go)
-   [sdk/cliproxy/builder.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/cliproxy/builder.go)
-   [sdk/config/config.go](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/config/config.go)

This document provides technical guidance for developers extending CLIProxyAPI functionality. It covers the SDK architecture, extension points, and development patterns for creating custom executors, storage backends, and translations.

For operational deployment configurations, see [Deployment Scenarios](/router-for-me/CLIProxyAPI/10-deployment-scenarios). For configuration file structure and options, see [Configuration Guide](/router-for-me/CLIProxyAPI/5-configuration-guide). For authentication implementation details, see [Authentication Flows](/router-for-me/CLIProxyAPI/7-authentication-flows).

---

## Extension Architecture Overview

CLIProxyAPI is designed with multiple extension points that allow developers to add new providers, storage backends, access control mechanisms, and protocol translations without modifying core code.

### Extension Points Map

*SDK types and their relationships to CLIProxyAPI extension points. Node labels use package-qualified names from the codebase.*

```mermaid
flowchart TD
    Builder["Builder(sdk/cliproxy/builder.go)"]
    Hooks["Hooks struct(OnBeforeStart / OnAfterStart)"]
    ProviderExecutor["ProviderExecutor Interface"]
    CustomExec["Custom Executor"]
    Store["Store Interface(sdk/auth)"]
    FileStore["FileTokenStore"]
    PostgresStore["PostgresStore"]
    GitStore["GitTokenStore"]
    ObjectStore["ObjectTokenStore"]
    CustomStore["Custom Store"]
    Translator["Translator Interface(internal/translator)"]
    CustomTrans["Custom Translator"]
    AccessProvider["Provider Interface(sdk/access/registry.go)"]
    RegisterProviderFn["RegisterProvider(typ, provider)(sdk/access)"]
    ConfigAccess["config-api-key provider(internal/access/config_access)"]
    CustomAccess["Custom Provider"]
    CoreAuthMgr["coreauth.Manager(sdk/cliproxy/auth)"]
    APIServer["API Server(internal/api)"]
    ModelRegistry["Model Registry"]

    Builder --> Hooks
    Builder --> APIServer
    Builder --> CoreAuthMgr
    Builder --> ModelRegistry
    CustomExec --> ProviderExecutor
    APIServer --> ProviderExecutor
    CustomStore --> Store
    FileStore --> Store
    PostgresStore --> Store
    GitStore --> Store
    ObjectStore --> Store
    CoreAuthMgr --> Store
    CustomTrans --> Translator
    APIServer --> Translator
    CustomAccess --> AccessProvider
    ConfigAccess --> AccessProvider
    RegisterProviderFn --> AccessProvider
    APIServer --> AccessProvider
```
Sources: [sdk/cliproxy/builder.go1-242](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/cliproxy/builder.go#L1-L242) [sdk/access/registry.go1-83](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/sdk/access/registry.go#L1-L83)

---

## SDK Package Structure

The CLIProxyAPI SDK is organized into reusable packages under `sdk/` that enable embedding the proxy service in applications.

### Core SDK Packages

| Package | Purpose | Key Types |
| --- | --- | --- |
| `sdk/cliproxy` | Service builder and lifecycle management | `Builder`, `ServiceOptions` |
| `sdk/cliproxy/auth` | Credential and authentication management | `Manager`, `AuthRecord`, `Selector` |
| `sdk/executor` | Provider executor interface and registry | `ProviderExecutor`, `ExecutionOptions` |
| `sdk/auth` | Storage abstraction for credentials | `Store`, `FileTokenStore` |
| `sdk/model` | Model registry and availability tracking | `Registry`, `ModelRegistration` |
| `sdk/access` | Request authentication interface | `AccessProvider` |

### Builder Pattern Usage

The `Builder` pattern in `sdk/cliproxy` is the primary entry point for embedding CLIProxyAPI:

> **[Mermaid sequence]**
> *(图表结构无法解析)*

**Sources:** [cmd/server/main.go446-481](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L446-L481) [README.md57](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md#L57-L57) [README.md79-85](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md#L79-L85)

---

## Creating Custom Executors

Custom executors implement the `ProviderExecutor` interface to add support for new AI service providers.

### ProviderExecutor Interface

The executor interface defines methods for request handling and streaming:

```mermaid
flowchart TD
    Interface["ProviderExecutor"]
    Execute["Execute(ctx, auth, request, opts)Non-streaming execution"]
    ExecuteStream["ExecuteStream(ctx, auth, request, opts)Streaming execution"]
    GetProviderName["GetProviderName()Returns provider identifier"]
    SupportedModels["GetSupportedModels()Returns model list"]
    AuthHandling["Auth InjectionAPI keys, OAuth tokens, etc."]
    RequestPrep["Request PreparationFormat conversion"]
    HTTPClient["HTTP ClientProxy-aware"]
    ErrorHandling["Error HandlingRetry logic, cooldowns"]
    ResponseParse["Response ParsingJSON/SSE parsing"]
    UsageReport["Usage ReportingToken tracking"]
    Factory["ExecutorFactory Function"]
    Register["RegisterExecutorFactory(name, factory)"]
    Registry["Global Executor Registry"]

    Interface --> Execute
    Interface --> ExecuteStream
    Interface --> GetProviderName
    Interface --> SupportedModels
    Execute --> AuthHandling
    Execute --> RequestPrep
    Execute --> HTTPClient
    Execute --> ErrorHandling
    Execute --> ResponseParse
    Execute --> UsageReport
    ExecuteStream --> AuthHandling
    ExecuteStream --> RequestPrep
    ExecuteStream --> HTTPClient
    ExecuteStream --> ErrorHandling
    ExecuteStream --> ResponseParse
    ExecuteStream --> UsageReport
    Factory --> Interface
    Register --> Factory
    Registry --> Register
```
### Executor Implementation Pattern

Custom executors typically follow this structure:

1.  **Define executor struct** with provider-specific configuration
2.  **Implement interface methods** for execution and metadata
3.  **Create factory function** that returns executor instances
4.  **Register factory** with the executor registry

The executor must handle:

-   **Authentication injection**: API keys, OAuth tokens, or service accounts into requests
-   **Request preparation**: Construct provider-specific HTTP requests
-   **Error handling**: Parse provider errors, apply retry logic, trigger cooldowns
-   **Response parsing**: Extract completion, usage, and metadata
-   **Model registration**: Report supported models to the registry

**Reference implementations:**

-   Gemini executor for API key and OAuth patterns
-   Claude executor for tool handling and thinking blocks
-   OpenAI-compatible executor for generic provider support

**Sources:** [README.md85](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md#L85-L85) Diagram 1 (Executors section)

---

## Custom Storage Backends

Storage backends implement the `Store` interface to persist authentication credentials and configuration.

### Store Interface

```mermaid
flowchart TD
    Store["Store Interface(sdk/auth)"]
    Save["Save(auth)Persist credential"]
    Load["Load(provider, id)Retrieve credential"]
    List["List(provider)List all credentials"]
    Delete["Delete(provider, id)Remove credential"]
    AuthDir["AuthDir()Storage root path"]
    Watch["Watch(callback)Change notifications"]
    FileStore["FileTokenStoreLocal JSON files"]
    PostgresStore["PostgresStoreDatabase + cache"]
    GitStore["GitTokenStoreGit repo + clone"]
    ObjectStore["ObjectTokenStoreS3-compatible + cache"]
    Caching["Local CachingReduce remote calls"]
    Sync["SynchronizationPull/push on demand"]
    Bootstrap["BootstrapInitialize from template"]
    Versioning["Version ControlAudit trail"]

    Store --> Save
    Store --> Load
    Store --> List
    Store --> Delete
    Store --> AuthDir
    Store --> Watch
    FileStore --> Store
    PostgresStore --> Store
    GitStore --> Store
    ObjectStore --> Store
    PostgresStore --> Caching
    GitStore --> Sync
    GitStore --> Versioning
    ObjectStore --> Caching
    PostgresStore --> Bootstrap
    ObjectStore --> Bootstrap
```
### Storage Backend Selection

The storage backend is configured via environment variables and registered globally:

| Backend | Environment Variables | Use Case |
| --- | --- | --- |
| **FileTokenStore** | (default) | Single instance, local development |
| **PostgresStore** | `PGSTORE_DSN`, `PGSTORE_SCHEMA`, `PGSTORE_LOCAL_PATH` | Multi-instance, shared state |
| **GitTokenStore** | `GITSTORE_GIT_URL`, `GITSTORE_GIT_USERNAME`, `GITSTORE_GIT_TOKEN`, `GITSTORE_LOCAL_PATH` | Version control, audit trail |
| **ObjectTokenStore** | `OBJECTSTORE_ENDPOINT`, `OBJECTSTORE_ACCESS_KEY`, `OBJECTSTORE_SECRET_KEY`, `OBJECTSTORE_BUCKET`, `OBJECTSTORE_LOCAL_PATH` | Containerized, cloud deployment |

### Registration Flow

Storage backends are registered once during initialization and used by all components:

1.  **Environment detection**: [cmd/server/main.go166-214](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L166-L214) checks environment variables
2.  **Store instantiation**: [cmd/server/main.go226-322](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L226-L322) creates store based on config
3.  **Global registration**: [cmd/server/main.go435-443](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L435-L443) via `RegisterTokenStore()`
4.  **Component usage**: Auth Manager and other components access via registered store

**Sources:** [cmd/server/main.go166-443](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L166-L443) Diagram 3 (Token Storage Backends section)

---

## Translation System Architecture

The translation system converts requests and responses between different AI provider formats (OpenAI, Claude, Gemini, etc.).

### Translator Interface and Registry

```mermaid
flowchart TD
    Registry["Global Translator Registry(internal/translator)"]
    RegisterTranslator["RegisterTranslator(name, instance)"]
    GetTranslator["GetTranslator(name)"]
    Translator["Translator Interface"]
    TranslateRequest["TranslateRequest(source, target, payload)"]
    TranslateResponse["TranslateResponse(source, target, payload)"]
    TranslateStream["TranslateStreamChunk(source, target, chunk)"]
    SupportedFormats["GetSupportedFormatsReturns format list"]
    OpenAITrans["OpenAITranslatorOpenAI format handling"]
    ClaudeTrans["ClaudeTranslatorAnthropic Messages API"]
    GeminiTrans["GeminiTranslatorGoogle GenerativeAI"]
    AntigravityTrans["AntigravityTranslatorAntigravity format"]
    MessageMap["Message MappingRole conversion"]
    ToolConvert["Tool ConversionFunction/tool format"]
    ContentBlock["Content Block MappingText/image/thinking"]
    StreamSSE["Stream FormatSSE parsing/generation"]

    Registry --> RegisterTranslator
    Registry --> GetTranslator
    RegisterTranslator --> Translator
    GetTranslator --> Translator
    Translator --> TranslateRequest
    Translator --> TranslateResponse
    Translator --> TranslateStream
    Translator --> SupportedFormats
    OpenAITrans --> Translator
    ClaudeTrans --> Translator
    GeminiTrans --> Translator
    AntigravityTrans --> Translator
    TranslateRequest --> MessageMap
    TranslateRequest --> ToolConvert
    TranslateRequest --> ContentBlock
    TranslateStream --> StreamSSE
```
### Bidirectional Translation Chains

The system supports multi-hop translations for protocol bridging:

```mermaid
flowchart TD
    Client["ClientOpenAI format"]
    OpenAITrans["OpenAI Translator"]
    ClaudeTrans["Claude Translator"]
    GeminiTrans["Gemini Translator"]
    AntigravityTrans["Antigravity Translator"]
    Provider["Provider API"]

    Client --> OpenAITrans
    OpenAITrans --> ClaudeTrans
    ClaudeTrans --> AntigravityTrans
    AntigravityTrans --> Provider
    Provider --> AntigravityTrans
    AntigravityTrans --> ClaudeTrans
    ClaudeTrans --> OpenAITrans
    OpenAITrans --> Client
```
### Translation Considerations

Custom translators must handle:

1.  **Message role mapping**: Convert between `user`/`assistant`/`system` and provider-specific roles
2.  **Content blocks**: Map text, images, tool calls, and thinking blocks
3.  **Tool definitions**: Convert function calling schemas between formats
4.  **Streaming chunks**: Parse and generate SSE (Server-Sent Events) format
5.  **Usage statistics**: Extract and normalize token counts
6.  **Error handling**: Translate provider error codes to standard format

**Sources:** [README.md82](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md#L82-L82) Diagram 6 (Translation Stage section)

---

## Access Control Extension

Access providers implement the `AccessProvider` interface to customize request authentication.

### AccessProvider Interface

```mermaid
flowchart TD
    Provider["AccessProvider"]
    Name["Name()Provider identifier"]
    Validate["Validate(request)Authenticate request"]
    Priority["Priority()Evaluation order"]
    ConfigProvider["ConfigAccessProviderconfig.yaml API keys"]
    BearerProvider["BearerTokenProviderAuthorization header"]
    CustomProvider["Custom ProviderYour implementation"]
    ExtractCreds["Extract CredentialsFrom headers/query"]
    CheckAuth["Check AuthorizationValidate against backend"]
    Return["Return ValidationResultAllowed/denied + metadata"]
    Register["Register()In access package"]
    GlobalRegistry["Global Provider Registry"]
    AccessManager["Access ManagerCoordinates providers"]

    Provider --> Name
    Provider --> Validate
    Provider --> Priority
    ConfigProvider --> Provider
    BearerProvider --> Provider
    CustomProvider --> Provider
    Validate --> ExtractCreds
    ExtractCreds --> CheckAuth
    CheckAuth --> Return
    Register --> GlobalRegistry
    GlobalRegistry --> AccessManager
    AccessManager --> Provider
```
### Custom Access Provider Pattern

To add custom authentication:

1.  **Implement interface**: Create struct with `Name()`, `Validate()`, `Priority()` methods
2.  **Extract credentials**: Parse authentication data from HTTP request
3.  **Validate**: Check credentials against your authentication backend
4.  **Return result**: Provide `ValidationResult` with allow/deny decision
5.  **Register**: Call package-level `Register()` function in `init()`

Higher priority providers are evaluated first. First successful validation wins.

**Sources:** [cmd/server/main.go446](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L446-L446) [README.md83](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md#L83-L83) Diagram 1 (Access Manager section)

---

## Development Workflow

### Building Extensions

```mermaid
flowchart TD
    Clone["Clone Repositorygit clone"]
    Branch["Create Feature Branchgit checkout -b"]
    Implement["Implement ExtensionExecutor/Store/Translator"]
    Register["Register Componentinit() or explicit call"]
    Test["Run Testsgo test ./..."]
    Example["Create Exampleexamples/ directory"]
    UnitTest["Unit TestsIndividual component"]
    IntegTest["Integration TestsFull request flow"]
    ManualTest["Manual TestingReal API calls"]
    CodeDocs["Code DocumentationGodoc comments"]
    Example2["Example CodeUsage patterns"]
    README["Update READMEFeature announcement"]

    Clone --> Branch
    Branch --> Implement
    Implement --> Register
    Register --> Test
    Test --> Example
    Test --> UnitTest
    Test --> IntegTest
    Test --> ManualTest
    Example --> CodeDocs
    Example --> Example2
    Example2 --> README
```
### Debug Mode Configuration

Enable detailed logging for development:

```
# config.yamldebug: truelog_level: "debug"log_api_requests: truelog_api_responses: truelog_request_body: truelog_response_body: true
```
This configuration logs:

-   All HTTP requests with headers and bodies
-   All HTTP responses with headers and bodies
-   Auth selection decisions
-   Model registry state changes
-   Translation operations

### Example: Custom Provider

The `examples/custom-provider` directory demonstrates implementing a custom executor:

**Structure:**

-   Custom executor implementation
-   Factory function and registration
-   Example configuration
-   Integration test

**Key patterns demonstrated:**

-   Implementing `ProviderExecutor` interface methods
-   Handling authentication injection
-   Parsing provider responses
-   Registering with executor registry
-   Model registration and availability

**Sources:** [README.md85](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md#L85-L85) [README.md87-95](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md#L87-L95)

---

## SDK Embedding Example

### Minimal Embedding Pattern

> **[Mermaid sequence]**
> *(图表结构无法解析)*

### Programmatic Configuration

Instead of `config.yaml`, configurations can be provided programmatically:

| Configuration Aspect | SDK Method | Example |
| --- | --- | --- |
| Server port | `cfg.Port = 8080` | Set before `Build()` |
| Auth directory | `cfg.AuthDir = "/path/to/auths"` | Set before `Build()` |
| Storage backend | `RegisterTokenStore(store)` | Before `Build()` |
| Access providers | `access.Register()` | In `init()` or before `Build()` |
| Custom executors | `executor.RegisterExecutorFactory()` | In `init()` or before `Build()` |
| Log level | `cfg.LogLevel = "debug"` | Set before `Build()` |

**Sources:** [cmd/server/main.go428-481](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/cmd/server/main.go#L428-L481) [README.md79-85](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md#L79-L85)

---

## Testing and Debugging

### Testing Strategy

```mermaid
flowchart TD
    Unit["Unit TestsComponent isolation"]
    Integration["Integration TestsMulti-component flows"]
    E2E["End-to-End TestsFull request cycles"]
    Executor["Executor TestsRequest/response handling"]
    Translator["Translator TestsFormat conversions"]
    Store["Store TestsPersistence operations"]
    AuthMgr["Auth Manager TestsSelection/cooldown logic"]
    MockServer["Mock HTTP ServersSimulate providers"]
    TestAuth["Test CredentialsMock auth records"]
    AssertLib["Testify LibraryAssertions"]

    Unit --> Executor
    Unit --> Translator
    Unit --> Store
    Integration --> AuthMgr
    E2E --> MockServer
    Executor --> TestAuth
    Translator --> AssertLib
    Store --> TestAuth
    AuthMgr --> MockServer
```
### Debugging Techniques

| Issue Type | Debug Approach | Configuration |
| --- | --- | --- |
| Request routing | Enable `log_api_requests: true` | Logs incoming request details |
| Response format | Enable `log_api_responses: true` | Logs outgoing response details |
| Auth selection | Enable `log_level: "debug"` | Logs selector decisions |
| Translation errors | Enable `log_request_body: true` | Logs payload transformations |
| Provider errors | Check executor error handling | Review retry logic and cooldowns |
| Model availability | Query `/v1/models` endpoint | Check registry state |
| Config hot-reload | Watch file watcher logs | Verify debounce and hash checks |

### Common Extension Issues

**Executor not invoked:**

-   Verify factory registration via `RegisterExecutorFactory()`
-   Check provider name matches configuration
-   Ensure models are registered with model registry

**Storage not persisting:**

-   Verify `Save()` implementation writes to backend
-   Check `AuthDir()` returns correct path
-   Ensure file permissions for write access

**Translation not applied:**

-   Verify translator registration via `RegisterTranslator()`
-   Check format names match expected values
-   Ensure bidirectional support for request and response

**Access denied:**

-   Verify access provider registration
-   Check `Priority()` evaluation order
-   Ensure `Validate()` returns proper result

**Sources:** [README.md85](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md#L85-L85) Diagram 5 (Model Registry section)

---

## Key Interfaces Summary

| Interface | Package | Purpose | Registration Method |
| --- | --- | --- | --- |
| `ProviderExecutor` | `sdk/executor` | Execute provider requests | `RegisterExecutorFactory(name, factory)` |
| `Store` | `sdk/auth` | Persist credentials | `RegisterTokenStore(store)` |
| `Translator` | `internal/translator` | Convert request/response formats | `RegisterTranslator(name, instance)` |
| `AccessProvider` | `internal/access` | Authenticate requests | `Register()` in package init |
| `Selector` | `sdk/cliproxy/auth` | Choose auth for request | Set in config: `round_robin` or `fill_first` |

**Sources:** [README.md79-85](https://github.com/router-for-me/CLIProxyAPI/blob/c66cb0af/README.md#L79-L85) All architecture diagrams
