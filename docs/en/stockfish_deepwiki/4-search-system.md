# Search System

Relevant source files

-   [src/search.cpp](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp)
-   [src/thread.h](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/thread.h)

## Purpose and Scope

The Search System is the most critical component of Stockfish (importance 3593), responsible for exploring the game tree to find the best chess move. This page provides a comprehensive overview of the search architecture, its key components, and how they interact.

For detailed information about specific aspects:

-   **Algorithm details** (iterative deepening, alpha-beta, pruning, extensions): See [Search Algorithm and Iterative Deepening](/official-stockfish/Stockfish/4.1-search-algorithm-and-iterative-deepening)
-   **Thread management and parallelization**: See [Thread Management and Parallel Search](/official-stockfish/Stockfish/4.2-thread-management-and-parallel-search)
-   **Move ordering heuristics**: See [Move Ordering and Move Picker](/official-stockfish/Stockfish/4.3-move-ordering-and-move-picker)
-   **Position evaluation**: See [Evaluation System](/official-stockfish/Stockfish/5-evaluation-system)
-   **Move generation**: See [Move Generation](/official-stockfish/Stockfish/3.3-move-generation)

## System Architecture

The search system consists of several interconnected components that work together to explore the chess position tree efficiently.

```mermaid
flowchart TD
    ThreadPool["ThreadPool(thread.h:115-177)"]
    SearchManager["SearchManager(search.h)"]
    LimitsType["LimitsTypeSearch constraints"]
    MainWorker["Main WorkerSearch::Worker"]
    Helper1["Helper Worker 1Search::Worker"]
    HelperN["Helper Worker NSearch::Worker"]
    StartSearching["start_searching():183-254"]
    IterDeep["iterative_deepening():259-544"]
    SearchRoot["search<Root>():614-1487"]
    SearchPV["search<PV>():614-1487"]
    SearchNonPV["search<NonPV>():614-1487"]
    QSearch["qsearch():1496-1734"]
    Stack["Stack[MAX_PLY+10]Per-ply state"]
    RootMoves["RootMovesCandidate moves"]
    Position["PositionBoard state"]
    MainHistory["mainHistoryMove history"]
    CaptureHistory["captureHistory"]
    ContHistory["continuationHistory"]
    TT["TranspositionTablePosition cache"]

    ThreadPool --> SearchManager
    ThreadPool --> MainWorker
    ThreadPool --> Helper1
    ThreadPool --> HelperN
    MainWorker --> StartSearching
    Helper1 --> StartSearching
    HelperN --> StartSearching
    StartSearching --> IterDeep
    IterDeep --> SearchRoot
    SearchRoot --> SearchPV
    SearchRoot --> SearchNonPV
    SearchPV --> SearchNonPV
    SearchPV --> QSearch
    SearchNonPV --> QSearch
    IterDeep --> Stack
    IterDeep --> RootMoves
    SearchRoot --> Position
    SearchPV --> Position
    SearchRoot --> MainHistory
    SearchRoot --> CaptureHistory
    SearchRoot --> ContHistory
    SearchRoot --> TT
```
**Sources:** [src/search.cpp1-2212](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L1-L2212) [src/thread.h74-109](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/thread.h#L74-L109) [src/thread.h115-177](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/thread.h#L115-L177)

## Key Data Structures

### Search::Worker

The `Search::Worker` class is the core search engine that executes the search algorithm. Each thread has its own `Worker` instance with thread-local state.

| Member | Type | Purpose |
| --- | --- | --- |
| `rootPos` | `Position` | Root position being searched |
| `rootMoves` | `RootMoves` | Candidate moves at root with scores |
| `rootDepth` | `Depth` | Current depth being searched |
| `completedDepth` | `Depth` | Last fully completed depth |
| `selDepth` | `int` | Maximum selective depth reached |
| `mainHistory` | `ButterflyHistory` | Main history table (color, move) |
| `captureHistory` | `CapturePieceToHistory` | History for capture moves |
| `continuationHistory` | `ContinuationHistory` | History based on move sequences |
| `lowPlyHistory` | `LowPlyHistory` | History for low ply positions |
| `accumulatorStack` | `AccumulatorStack` | NNUE incremental updates |
| `nodes` | `atomic<uint64_t>` | Node count for this worker |
| `tbHits` | `atomic<uint64_t>` | Tablebase probe count |

**Key Methods:**

| Method | Line | Purpose |
| --- | --- | --- |
| `start_searching()` | [183-254](https://github.com/official-stockfish/Stockfish/blob/c27c1747/183-254) | Entry point for search |
| `iterative_deepening()` | [259-544](https://github.com/official-stockfish/Stockfish/blob/c27c1747/259-544) | Main iterative deepening loop |
| `search<NodeType>()` | [614-1487](https://github.com/official-stockfish/Stockfish/blob/c27c1747/614-1487) | Recursive alpha-beta search |
| `qsearch<NodeType>()` | [1496-1734](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1496-1734) | Quiescence search |
| `do_move()` | [547-568](https://github.com/official-stockfish/Stockfish/blob/c27c1747/547-568) | Make move and update state |
| `undo_move()` | [577-580](https://github.com/official-stockfish/Stockfish/blob/c27c1747/577-580) | Unmake move |
| `evaluate()` | [1755-1758](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1755-1758) | Evaluate position using NNUE |

**Sources:** [src/search.cpp156-175](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L156-L175) [src/search.cpp183-254](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L183-L254) [src/search.cpp259-544](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L259-L544)

### Stack Structure

The `Stack` structure maintains per-ply search state. An array of `Stack` objects forms the search stack, with each element representing one ply in the search tree.

```mermaid
flowchart TD
    Sentinel["ss-7 to ss-1(sentinel entries)"]
    Current["ss (current ply)"]
    Future["ss+1 to ss+MAX_PLY"]
    PV["pv*Principal variation"]
    ContHist["continuationHistory*Move sequence history"]
    ContCorrHist["continuationCorrectionHistory*Eval correction history"]
    CurrentMove["currentMoveMove at this ply"]
    ExcludedMove["excludedMoveFor singular extension"]
    StaticEval["staticEvalStatic evaluation"]
    StatScore["statScoreHistory score"]
    MoveCount["moveCountMoves searched"]
    Ply["plyDistance from root"]
    CutoffCnt["cutoffCntBeta cutoffs"]
    InCheck["inCheckPosition in check"]
    TtPv["ttPvPart of PV in TT"]
    TtHit["ttHitTT hit at this node"]
    Reduction["reductionLMR reduction applied"]

    Sentinel --> Current
    Current --> Future
    Current --> PV
    Current --> ContHist
    Current --> CurrentMove
    Current --> StaticEval
```
The stack is initialized with sentinel entries at negative indices to allow safe access from continuation history lookups. At each search node, the stack pointer `ss` is passed down, with child nodes using `ss+1`.

**Stack Usage Pattern:**

-   `ss`: Current search node
-   `(ss-1)->currentMove`: Parent's move that led here
-   `(ss-2)->staticEval`: Grandparent's static evaluation
-   `(ss+1)->pv`: Child's principal variation

**Sources:** [src/search.cpp278-292](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L278-L292) [src/search.cpp547-568](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L547-L568) [src/search.cpp570-575](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L570-L575)

### RootMove Structure

`RootMove` tracks information about candidate moves at the root position during iterative deepening.

| Field | Type | Purpose |
| --- | --- | --- |
| `pv` | `std::vector<Move>` | Principal variation starting with this move |
| `score` | `Value` | Current search score |
| `uciScore` | `Value` | Score reported to UCI |
| `previousScore` | `Value` | Score from previous iteration |
| `averageScore` | `Value` | Running average of scores |
| `meanSquaredScore` | `Value` | Mean squared score for aspiration window |
| `effort` | `uint64_t` | Nodes spent searching this move |
| `selDepth` | `int` | Selective depth reached |
| `tbRank` | `int` | Tablebase rank (for TB root positions) |
| `tbScore` | `Value` | Tablebase score |
| `scoreLowerbound` | `bool` | Score is lower bound (fail high) |
| `scoreUpperbound` | `bool` | Score is upper bound (fail low) |

The `RootMoves` vector is sorted after each search iteration, with the best move moved to the front.

**Sources:** [src/search.cpp331-333](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L331-L333) [src/search.cpp383](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L383-L383) [src/search.cpp1305-1354](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L1305-L1354)

### SearchManager

`SearchManager` coordinates the search process, manages time, and handles output.

| Responsibility | Implementation |
| --- | --- |
| Time management | `TimeManager tm` member |
| PV output | `pv()` method [2114-2183](https://github.com/official-stockfish/Stockfish/blob/c27c1747/2114-2183) |
| Time checking | `check_time()` [1944-1974](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1944-1974) |
| Search updates | `UpdateContext` callbacks |
| Best move tracking | `bestPreviousScore`, `bestPreviousAverageScore` |
| Pondering control | `ponder`, `stopOnPonderhit` flags |

**Sources:** [src/search.cpp1944-1974](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L1944-L1974) [src/search.cpp2114-2183](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L2114-L2183)

## Search Control Flow

The following diagram shows the complete control flow from search initiation to completion, with actual function calls and their locations in the code.

```mermaid
flowchart TD
    UCIGo["UCI 'go' command"]
    StartThinking["ThreadPool::start_thinking()(thread.cpp)"]
    SetPosition["Setup positionand limits"]
    MainStart["Main thread:Worker::start_searching():183-254"]
    HelperStart["Helper threads:Worker::start_searching():188-192"]
    TMInit["TimeManager::init():194-195"]
    TTNewSearch["tt.new_search():196"]
    StartHelpers["threads.start_searching():206"]
    IterDeep["iterative_deepening():259-544"]
    DepthLoop["rootDepth < MAX_PLY!threads.stop:322-323"]
    MultiPVLoop["For each PV linepvIdx < multiPV:341"]
    AspWindow["Aspiration windowalpha/beta setup:354-358"]
    SearchRoot["search<Root>(pos, ss,alpha, beta, depth):375"]
    FailWindow["Fail high/low?:400-416"]
    ReSearch["Widen windowre-search:402-418"]
    SortRoot["std::stable_sortrootMoves:383"]
    CheckStop["threads.stop?:388"]
    OutputPV["SearchManager::pv()Output UCI info:434"]
    DepthComplete["completedDepth = rootDepth:441"]
    CheckTime["check_time()Stop if time up:485-528"]
    BestThread["threads.get_best_thread():237"]
    OutputBest["Output bestmoveand ponder:253"]

    UCIGo --> StartThinking
    StartThinking --> SetPosition
    SetPosition --> MainStart
    SetPosition --> HelperStart
    MainStart --> TMInit
    TMInit --> TTNewSearch
    TTNewSearch --> StartHelpers
    StartHelpers --> IterDeep
    HelperStart --> IterDeep
    IterDeep --> DepthLoop
    DepthLoop --> MultiPVLoop
    DepthLoop --> BestThread
    MultiPVLoop --> AspWindow
    AspWindow --> SearchRoot
    SearchRoot --> SortRoot
    SortRoot --> CheckStop
    CheckStop --> BestThread
    CheckStop --> FailWindow
    FailWindow --> ReSearch
    FailWindow --> OutputPV
    ReSearch --> SearchRoot
    OutputPV --> MultiPVLoop
    MultiPVLoop --> DepthComplete
    DepthComplete --> CheckTime
    CheckTime --> DepthLoop
    BestThread --> OutputBest
```
**Sources:** [src/search.cpp183-254](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L183-L254) [src/search.cpp259-544](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L259-L544)

## Recursive Search Structure

The core search algorithm uses template specialization to handle three node types: `Root`, `PV` (Principal Variation), and `NonPV`.

```mermaid
flowchart TD
    SearchFunc["search<NodeType>(pos, ss, alpha, beta, depth, cutNode):614-1487"]
    RootInst["NodeType = RootFirst ply only"]
    PVInst["NodeType = PVPrincipal variation"]
    NonPVInst["NodeType = NonPVZero-window search"]
    Step1["Step 1: Initialize node:657-671"]
    Step2["Step 2: Check draw/stop:675-678"]
    Step3["Step 3: Mate distance:680-689"]
    Step4["Step 4: TT lookup:701-710"]
    Step5["Step 5: TB probe:802-854"]
    Step6["Step 6: Static eval:712-742"]
    Step7["Step 7: Razoring:870-874"]
    Step8["Step 8: Futility:876-890"]
    Step9["Step 9: Null move:892-925"]
    Step10["Step 10: IIR:929-933"]
    Step11["Step 11: ProbCut:935-981"]
    Step12["Step 12: Small ProbCut:985-989"]
    Step13["Step 13: Moves loop:1003-1398"]
    Step14["Step 14: Pruning:1049-1117"]
    Step15["Step 15: Extensions:1119-1181"]
    Step16["Step 16: Make move:1183-1188"]
    Step17["Step 17: LMR:1231-1262"]
    Step18["Step 18: Full depth:1264-1274"]
    Step19["Step 19: Undo:1293-1294"]
    Step20["Step 20: Update best:1298-1387"]
    Step21["Step 21: Mate check:1400-1412"]
    RecurseNonPV["Recursive call:search<NonPV>(ss+1):902, 966, 1137, 1242, 1257, 1272"]
    RecursePV["Recursive call:search<PV>(ss+1):1290"]
    QSearchCall["Terminal call:qsearch(ss+1):624, 874, 962"]

    SearchFunc --> RootInst
    SearchFunc --> PVInst
    SearchFunc --> NonPVInst
    Step1 --> Step2
    Step2 --> Step3
    Step3 --> Step4
    Step4 --> Step5
    Step5 --> Step6
    Step6 --> Step7
    Step7 --> Step8
    Step8 --> Step9
    Step9 --> Step10
    Step10 --> Step11
    Step11 --> Step12
    Step12 --> Step13
    Step13 --> Step14
    Step14 --> Step15
    Step15 --> Step16
    Step16 --> Step17
    Step17 --> Step18
    Step18 --> Step19
    Step19 --> Step20
    Step20 --> Step13
    Step13 --> Step21
    Step17 --> RecurseNonPV
    Step18 --> RecurseNonPV
    RecursePV --> SearchFunc
    RecurseNonPV --> SearchFunc
    Step7 --> QSearchCall
```
**Key Search Characteristics:**

-   **Template-based dispatch**: Three node types with `constexpr bool` flags determine behavior at compile time [618-620](https://github.com/official-stockfish/Stockfish/blob/c27c1747/618-620)
-   **Fail-soft alpha-beta**: Returns values outside `[alpha, beta]` window
-   **Zero-window search**: Non-PV nodes use `alpha = beta - 1` for faster searches [638](https://github.com/official-stockfish/Stockfish/blob/c27c1747/638)
-   **Depth-first with iterative deepening**: Explores to depth D before increasing to D+1

**Sources:** [src/search.cpp614-1487](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L614-L1487)

## Quiescence Search

When depth reaches zero, regular search transitions to quiescence search (`qsearch`) to resolve tactical sequences and avoid the horizon effect.

**Quiescence Characteristics:**

| Aspect | Description |
| --- | --- |
| **Entry condition** | `depth <= 0` in main search [623-624](https://github.com/official-stockfish/Stockfish/blob/c27c1747/623-624) |
| **Moves searched** | Only captures and checks (in check positions: all evasions) [1614-1616](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1614-1616) |
| **Stand pat** | Can return static eval without searching [1590-1600](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1590-1600) |
| **Depth** | Uses special `DEPTH_QS` constant for TT entries |
| **Pruning** | Futility pruning based on material gain [1636-1658](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1636-1658) |
| **SEE filtering** | Prunes captures with bad Static Exchange Evaluation [1654-1667](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1654-1667) |

**Sources:** [src/search.cpp1496-1734](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L1496-L1734)

## Integration with Other Systems

The search system integrates tightly with other Stockfish components:

```mermaid
flowchart TD
    Search["Search::Worker"]
    Position["PositionBoard state"]
    MoveGen["MoveGenLegal moves"]
    MovePicker["MovePickerMove ordering"]
    NNUE["NNUE::NetworkNeural network"]
    AccStack["AccumulatorStackIncremental updates"]
    Evaluate["Eval::evaluate()"]
    MainHist["mainHistory"]
    CaptHist["captureHistory"]
    ContHist["continuationHistory"]
    LowPlyHist["lowPlyHistory"]
    CorrHist["correctionHistory"]
    SharedHist["SharedHistories"]
    TT["TranspositionTablePosition cache"]
    Syzygy["Syzygy TablebasesEndgame DB"]

    Search --> Position
    Search --> MovePicker
    MovePicker --> MoveGen
    MoveGen --> Position
    Search --> Evaluate
    Evaluate --> NNUE
    Evaluate --> AccStack
    AccStack --> Position
    Search --> MainHist
    Search --> CaptHist
    Search --> ContHist
    Search --> LowPlyHist
    Search --> CorrHist
    Search --> SharedHist
    Search --> TT
    Search --> Syzygy
    Position --> TT
```
**Integration Points:**

| System | Usage in Search | Location |
| --- | --- | --- |
| Position | Board state, move execution, legal move validation | Throughout search |
| MovePicker | Iterates moves in optimal order | [996-997](https://github.com/official-stockfish/Stockfish/blob/c27c1747/996-997) [1615-1616](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1615-1616) |
| MoveGen | Generates pseudo-legal moves | Via MovePicker |
| NNUE | Position evaluation at leaf nodes | [1755-1758](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1755-1758) |
| AccumulatorStack | Incremental NNUE updates during move execution | [557-558](https://github.com/official-stockfish/Stockfish/blob/c27c1747/557-558) |
| TranspositionTable | Position cache for cutoffs and move ordering | [704](https://github.com/official-stockfish/Stockfish/blob/c27c1747/704) [838-840](https://github.com/official-stockfish/Stockfish/blob/c27c1747/838-840) [974-975](https://github.com/official-stockfish/Stockfish/blob/c27c1747/974-975) |
| History tables | Move ordering and pruning decisions | [996-997](https://github.com/official-stockfish/Stockfish/blob/c27c1747/996-997) [1084-1092](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1084-1092) [1220-1225](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1220-1225) |
| Syzygy | Endgame tablebase probes | [802-854](https://github.com/official-stockfish/Stockfish/blob/c27c1747/802-854) |
| TimeManager | Time control and search stopping | [194-195](https://github.com/official-stockfish/Stockfish/blob/c27c1747/194-195) [485-528](https://github.com/official-stockfish/Stockfish/blob/c27c1747/485-528) |

**Sources:** [src/search.cpp547-568](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L547-L568) [src/search.cpp704](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L704-L704) [src/search.cpp996-997](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L996-L997) [src/search.cpp1755-1758](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L1755-L1758)

## Thread Coordination

The search is parallelized using a shared-nothing architecture where each thread maintains its own `Search::Worker` with thread-local state.

**Thread Roles:**

| Thread Type | Responsibilities |
| --- | --- |
| Main thread | Time management, PV output, best thread selection, result reporting |
| Helper threads | Independent searches at the same root position with different random variations |

**Shared State:**

-   `TranspositionTable`: Lock-free shared hash table
-   `SharedHistories`: NUMA-replicated shared history tables
-   `threads.stop`: Atomic flag to stop all threads
-   `threads.increaseDepth`: Flag to control depth increments

**Thread Coordination Flow:**

1.  Main thread initializes time manager and transposition table [194-196](https://github.com/official-stockfish/Stockfish/blob/c27c1747/194-196)
2.  Main thread starts helper threads [206](https://github.com/official-stockfish/Stockfish/blob/c27c1747/206)
3.  All threads run `iterative_deepening()` independently [188-191](https://github.com/official-stockfish/Stockfish/blob/c27c1747/188-191) [207](https://github.com/official-stockfish/Stockfish/blob/c27c1747/207)
4.  Main thread monitors time and sets stop flag [485-528](https://github.com/official-stockfish/Stockfish/blob/c27c1747/485-528)
5.  All threads check stop flag periodically [322](https://github.com/official-stockfish/Stockfish/blob/c27c1747/322) [388](https://github.com/official-stockfish/Stockfish/blob/c27c1747/388) [676](https://github.com/official-stockfish/Stockfish/blob/c27c1747/676)
6.  Main thread waits for all threads to finish [223](https://github.com/official-stockfish/Stockfish/blob/c27c1747/223)
7.  Best thread is selected based on completed depth and score [237](https://github.com/official-stockfish/Stockfish/blob/c27c1747/237)

**Sources:** [src/search.cpp183-254](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L183-L254) [src/search.cpp322-323](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L322-L323) [src/thread.h115-177](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/thread.h#L115-L177)

## Search Heuristics Summary

The search employs numerous heuristics to improve efficiency. These are documented in detail in [Search Algorithm and Iterative Deepening](/official-stockfish/Stockfish/4.1-search-algorithm-and-iterative-deepening), but are summarized here for reference:

| Heuristic | Purpose | Location |
| --- | --- | --- |
| Aspiration windows | Narrow alpha-beta window around expected score | [354-421](https://github.com/official-stockfish/Stockfish/blob/c27c1747/354-421) |
| Transposition table | Cache position evaluations | [701-799](https://github.com/official-stockfish/Stockfish/blob/c27c1747/701-799) |
| Null move pruning | Skip move to prove position is good | [892-925](https://github.com/official-stockfish/Stockfish/blob/c27c1747/892-925) |
| Internal iterative reduction | Reduce depth when no TT move | [929-933](https://github.com/official-stockfish/Stockfish/blob/c27c1747/929-933) |
| ProbCut | Prune if reduced search gives high value | [935-981](https://github.com/official-stockfish/Stockfish/blob/c27c1747/935-981) |
| Razoring | Return qsearch if eval very low | [870-874](https://github.com/official-stockfish/Stockfish/blob/c27c1747/870-874) |
| Futility pruning | Prune moves unlikely to raise alpha | [876-890](https://github.com/official-stockfish/Stockfish/blob/c27c1747/876-890) [1100-1109](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1100-1109) |
| Late move reductions (LMR) | Search later moves at reduced depth | [1231-1262](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1231-1262) |
| Singular extensions | Extend moves that appear uniquely best | [1129-1181](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1129-1181) |
| SEE pruning | Prune moves with bad material exchange | [1075-1080](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1075-1080) [1114](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1114) |
| History-based pruning | Prune moves with poor historical performance | [1089-1090](https://github.com/official-stockfish/Stockfish/blob/c27c1747/1089-1090) |

**Sources:** [src/search.cpp354-421](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L354-L421) [src/search.cpp870-1181](https://github.com/official-stockfish/Stockfish/blob/c27c1747/src/search.cpp#L870-L1181)
