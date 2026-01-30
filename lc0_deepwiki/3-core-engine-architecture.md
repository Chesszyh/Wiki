# Core Engine Architecture

Relevant source files

-   [src/chess/callbacks.h](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/chess/callbacks.h)
-   [src/chess/uciloop.cc](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/chess/uciloop.cc)
-   [src/chess/uciloop.h](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/chess/uciloop.h)
-   [src/engine.cc](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc)
-   [src/engine.h](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.h)
-   [src/engine\_loop.cc](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine_loop.cc)
-   [src/engine\_loop.h](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine_loop.h)
-   [src/main.cc](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/main.cc)
-   [src/selfplay/loop.cc](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/selfplay/loop.cc)

This page describes the core engine architecture of Lc0, including the main entry points, engine controller, UCI protocol handling, and the coordination between different subsystems. The focus is on the high-level architectural components and their interactions.

For details about the neural network system, see [Neural Network System](/LeelaChessZero/lc0/6-neural-network-system). For search algorithm implementation, see [Search Algorithm](/LeelaChessZero/lc0/5-search-algorithm). For UCI protocol specifics, see [UCI Protocol Implementation](/LeelaChessZero/lc0/3.1-uci-protocol-implementation).

## System Overview

The Lc0 engine follows a modular architecture where the core engine serves as a coordinator between the UCI protocol layer, search algorithms, neural network backends, and chess game logic. The architecture supports multiple execution modes including standard UCI engine operation, self-play tournaments, and various utility tools.

## Main Entry Point and Engine Selection

The application starts in `main()` where it initializes core systems and determines which execution mode to use. The primary engine selection logic resides in `ChooseAndRunEngine()`.

### Engine Selection Flow

```mermaid
flowchart TD
    main["main()"]
    init["Initialize Systems"]
    mode["Check Execution Mode"]
    selfplay["selfplay mode"]
    benchmark["benchmark modes"]
    tools["conversion tools"]
    engine["ChooseAndRunEngine()"]
    explicit["Check Explicit Search Name"]
    default["Check DEFAULT_SEARCH"]
    binary["Check Binary Name"]
    classic["Default to 'classic'"]
    run1["RunEngine(factory)"]
    run2["RunEngine(factory)"]
    run3["RunEngine(factory)"]
    run4["RunEngine(factory)"]

    main --> init
    init --> mode
    mode --> selfplay
    mode --> benchmark
    mode --> tools
    mode --> engine
    engine --> explicit
    explicit --> default
    default --> binary
    binary --> classic
    explicit --> run1
    default --> run2
    binary --> run3
    classic --> run4
```
**Sources:** [src/main.cc44-75](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/main.cc#L44-L75) [src/main.cc78-140](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/main.cc#L78-L140)

## Core Engine Architecture Components

The engine architecture consists of several key layers that work together to provide UCI-compliant chess engine functionality.

### Architecture Overview

```mermaid
flowchart TD
    main["main()"]
    RunEngine["RunEngine()"]
    UciLoop["UciLoop"]
    StringUciResponder["StringUciResponder"]
    StdoutUciResponder["StdoutUciResponder"]
    Engine["Engine"]
    EngineControllerBase["EngineControllerBase"]
    UciPonderForwarder["UciPonderForwarder"]
    SearchBase["SearchBase"]
    CachingBackend["CachingBackend"]
    SyzygyTablebase["SyzygyTablebase"]
    OptionsDict["OptionsDict"]
    GameState["GameState"]
    Position["Position"]
    ChessBoard["ChessBoard"]

    main --> RunEngine
    RunEngine --> UciLoop
    RunEngine --> Engine
    UciLoop --> StringUciResponder
    StringUciResponder --> StdoutUciResponder
    UciLoop --> EngineControllerBase
    Engine --> EngineControllerBase
    Engine --> UciPonderForwarder
    Engine --> SearchBase
    Engine --> CachingBackend
    Engine --> SyzygyTablebase
    Engine --> OptionsDict
    Engine --> GameState
    GameState --> Position
    Position --> ChessBoard
```
**Sources:** [src/engine\_loop.cc47-82](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine_loop.cc#L47-L82) [src/engine.cc147-155](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc#L147-L155) [src/chess/uciloop.cc166-172](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/chess/uciloop.cc#L166-L172)

## Engine Class Design

The `Engine` class implements `EngineControllerBase` and serves as the primary coordinator for all engine operations. It manages the lifecycle of searches, backend configurations, and game state.

### Engine Component Relationships

```mermaid
flowchart TD
    Engine["Engine"]
    uci_forwarder_["uci_forwarder_UciPonderForwarder"]
    options_["options_OptionsDict"]
    search_["search_SearchBase"]
    backend_["backend_CachingBackend"]
    syzygy_tb_["syzygy_tb_SyzygyTablebase"]
    last_position_["last_position_GameState"]
    last_go_params_["last_go_params_GoParams"]
    SearchFactory["SearchFactory"]
    BackendManager["BackendManager"]
    UciResponder["UciResponder"]

    Engine --> uci_forwarder_
    Engine --> options_
    Engine --> search_
    Engine --> backend_
    Engine --> syzygy_tb_
    Engine --> last_position_
    Engine --> last_go_params_
    SearchFactory --> search_
    BackendManager --> backend_
    UciResponder --> uci_forwarder_
```
**Sources:** [src/engine.h40-87](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.h#L40-L87) [src/engine.cc147-155](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc#L147-L155)

## UCI Protocol Integration

The UCI protocol handling is implemented through a layered approach where `UciLoop` processes commands and delegates engine operations to `EngineControllerBase` implementations.

### UCI Command Flow

```mermaid
flowchart TD
    stdin["stdin input"]
    ParseCommand["ParseCommand()"]
    DispatchCommand["DispatchCommand()"]
    uci["uci"]
    isready["isready"]
    position["position"]
    go["go"]
    stop["stop"]
    setoption["setoption"]
    EnsureReady["EnsureReady()"]
    SetPosition["SetPosition()"]
    Go["Go()"]
    Stop["Stop()"]
    OptionsParser["OptionsParser"]
    SendId["SendId()"]
    OutputBestMove["OutputBestMove()"]
    OutputThinkingInfo["OutputThinkingInfo()"]
    stdout["stdout output"]

    stdin --> ParseCommand
    ParseCommand --> DispatchCommand
    DispatchCommand --> uci
    DispatchCommand --> isready
    DispatchCommand --> position
    DispatchCommand --> go
    DispatchCommand --> stop
    DispatchCommand --> setoption
    uci --> SendId
    isready --> EnsureReady
    position --> SetPosition
    go --> Go
    stop --> Stop
    setoption --> OptionsParser
    SendId --> stdout
    OutputBestMove --> stdout
    OutputThinkingInfo --> stdout
```
**Sources:** [src/chess/uciloop.cc174-250](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/chess/uciloop.cc#L174-L250) [src/chess/uciloop.cc80-131](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/chess/uciloop.cc#L80-L131)

## Engine Lifecycle and State Management

The engine manages several types of state and coordinates their updates across different operations.

### Engine State Management

| State Component | Type | Purpose | Update Triggers |
| --- | --- | --- | --- |
| `ponder_enabled_` | `bool` | Pondering support flag | `SetPosition()` |
| `strict_uci_timing_` | `bool` | UCI timing mode | `SetPosition()` |
| `last_position_` | `GameState` | Current game position | `SetPosition()`, `NewGame()` |
| `last_go_params_` | `GoParams` | Last search parameters | `Go()` |
| `backend_name_` | `string` | Active backend name | `UpdateBackendConfig()` |
| `previous_tb_paths_` | `string` | Tablebase paths | `EnsureSyzygyTablebasesLoaded()` |

**Sources:** [src/engine.h76-86](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.h#L76-L86) [src/engine.cc217-225](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc#L217-L225)

## Backend and Search Integration

The engine coordinates between the search algorithm and neural network backend through well-defined interfaces.

### Integration Flow

```mermaid
flowchart TD
    SetPosition["SetPosition()"]
    Go["Go()"]
    UpdateBackendConfig["UpdateBackendConfig()"]
    BackendManager["BackendManager"]
    CreateMemCache["CreateMemCache()"]
    backend_["backend_CachingBackend"]
    search_["search_SearchBase"]
    SetBackend["SetBackend()"]
    StartSearch["StartSearch()"]
    SetSyzygyTablebase["SetSyzygyTablebase()"]
    MakeGameState["MakeGameState()"]
    InitializeSearchPosition["InitializeSearchPosition()"]
    GameState["GameState"]

    UpdateBackendConfig --> BackendManager
    BackendManager --> CreateMemCache
    CreateMemCache --> backend_
    backend --> _SetBackend
    SetBackend --> search_
    SetPosition --> MakeGameState
    MakeGameState --> GameState
    Go --> InitializeSearchPosition
    InitializeSearchPosition --> search_
    search --> _StartSearch
    search --> _SetSyzygyTablebase
```
**Sources:** [src/engine.cc164-177](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc#L164-L177) [src/engine.cc215-225](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc#L215-L225) [src/engine.cc233-242](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc#L233-L242)

## Pondering Support

The engine includes sophisticated pondering support through the `UciPonderForwarder` class, which transforms search output for ponder mode.

### Ponder Implementation

```mermaid
flowchart TD
    PonderHit["PonderHit()"]
    EnsureSearchStopped["EnsureSearchStopped()"]
    StartClock["StartClock()"]
    RestorePosition["InitializeSearchPosition(for_ponder=false)"]
    ContinueSearch["StartSearch()"]
    Go["Go(ponder=true)"]
    InitializeSearchPosition["InitializeSearchPosition(for_ponder=true)"]
    TrimPosition["Remove Last Move"]
    StartSearch["StartSearch()"]
    UciPonderForwarder["UciPonderForwarder"]
    TransformThinkingInfo["Transform Scores/Depth"]
    FilterPV["Filter PV for Ponder Move"]

    Go --> InitializeSearchPosition
    InitializeSearchPosition --> TrimPosition
    TrimPosition --> StartSearch
    StartSearch --> UciPonderForwarder
    UciPonderForwarder --> TransformThinkingInfo
    UciPonderForwarder --> FilterPV
    PonderHit --> EnsureSearchStopped
    EnsureSearchStopped --> StartClock
    StartClock --> RestorePosition
    RestorePosition --> ContinueSearch
```
**Sources:** [src/engine.cc91-145](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc#L91-L145) [src/engine.cc249-257](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc#L249-L257) [src/engine.cc200-213](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc#L200-L213)

## Configuration and Options Management

The engine uses a sophisticated options system that integrates configuration from multiple sources including command line, UCI options, and configuration files.

### Options Integration

```mermaid
flowchart TD
    CommandLine["Command Line"]
    ConfigFile["Config File"]
    UCIOptions["UCI setoption"]
    OptionsParser["OptionsParser"]
    OptionsDict["OptionsDict"]
    kSyzygyTablebaseId["kSyzygyTablebaseId"]
    kStrictUciTiming["kStrictUciTiming"]
    kPonderId["kPonderId"]
    kPreload["kPreload"]
    SharedBackendParams["SharedBackendParams"]
    kBackendId["kBackendId"]
    kNNCacheSizeId["kNNCacheSizeId"]

    CommandLine --> OptionsParser
    ConfigFile --> OptionsParser
    UCIOptions --> OptionsParser
    OptionsParser --> OptionsDict
    OptionsDict --> kSyzygyTablebaseId
    OptionsDict --> kStrictUciTiming
    OptionsDict --> kPonderId
    OptionsDict --> kPreload
    OptionsDict --> SharedBackendParams
    SharedBackendParams --> kBackendId
    SharedBackendParams --> kNNCacheSizeId
```
**Sources:** [src/engine.cc41-72](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine.cc#L41-L72) [src/engine\_loop.cc51-63](https://github.com/LeelaChessZero/lc0/blob/b4e98c19/src/engine_loop.cc#L51-L63)
