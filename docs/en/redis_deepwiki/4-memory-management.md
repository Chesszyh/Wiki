# Memory Management

Relevant source files

-   [deps/jemalloc/include/jemalloc/internal/jemalloc\_internal\_externs.h](https://github.com/redis/redis/blob/8ad54215/deps/jemalloc/include/jemalloc/internal/jemalloc_internal_externs.h)
-   [deps/jemalloc/include/jemalloc/internal/jemalloc\_internal\_inlines\_c.h](https://github.com/redis/redis/blob/8ad54215/deps/jemalloc/include/jemalloc/internal/jemalloc_internal_inlines_c.h)
-   [deps/jemalloc/include/jemalloc/jemalloc\_macros.h.in](https://github.com/redis/redis/blob/8ad54215/deps/jemalloc/include/jemalloc/jemalloc_macros.h.in)
-   [deps/jemalloc/src/jemalloc.c](https://github.com/redis/redis/blob/8ad54215/deps/jemalloc/src/jemalloc.c)
-   [deps/jemalloc/src/jemalloc\_cpp.cpp](https://github.com/redis/redis/blob/8ad54215/deps/jemalloc/src/jemalloc_cpp.cpp)
-   [src/Makefile](https://github.com/redis/redis/blob/8ad54215/src/Makefile)
-   [src/config.h](https://github.com/redis/redis/blob/8ad54215/src/config.h)
-   [src/evict.c](https://github.com/redis/redis/blob/8ad54215/src/evict.c)
-   [src/expire.c](https://github.com/redis/redis/blob/8ad54215/src/expire.c)
-   [src/zmalloc.c](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c)
-   [src/zmalloc.h](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.h)
-   [tests/unit/expire.tcl](https://github.com/redis/redis/blob/8ad54215/tests/unit/expire.tcl)
-   [tests/unit/maxmemory.tcl](https://github.com/redis/redis/blob/8ad54215/tests/unit/maxmemory.tcl)

Redis memory management encompasses allocation tracking, eviction policies, key expiration, and memory optimization strategies. This system ensures Redis operates efficiently within memory constraints while providing predictable performance characteristics.

For information about data structure memory optimization, see [Memory-Efficient Data Structures](/redis/redis/3.4-memory-efficient-data-structures). For eviction and expiration policy details, see [Eviction and Expiration Policies](/redis/redis/4.1-eviction-and-expiration-policies). For memory allocator build configuration, see [Memory Allocators and Build System](/redis/redis/4.2-memory-allocators-and-build-system).

## Memory Allocation Architecture

Redis implements a multi-layered memory management architecture built on top of pluggable allocators with comprehensive tracking and control mechanisms.

```mermaid
flowchart TD
    ZMALLOC["zmalloc.cMemory Tracking Abstraction"]
    USAGE_TRACKING["used_memory arrayPer-thread Usage Tracking"]
    OOM_HANDLER["zmalloc_oom_handlerOut-of-Memory Handler"]
    JEMALLOC["jemallocProduction Default"]
    TCMALLOC["tcmallocAlternative Allocator"]
    LIBC["libc mallocFallback/Debug"]
    SERVER["server.cGlobal Memory Limits"]
    EVICT["evict.cMemory Pressure Handler"]
    EXPIRE["expire.cKey Expiration"]
    OBJECTS["Redis ObjectsString, Hash, List, etc."]
    MAXMEM["maxmemory settingMemory Limit"]
    EVICTION["Eviction PoliciesLRU/LFU/TTL/Random"]
    DEFRAG["defrag.cActive Defragmentation"]

    ZMALLOC --> JEMALLOC
    ZMALLOC --> TCMALLOC
    ZMALLOC --> LIBC
    SERVER --> ZMALLOC
    EVICT --> ZMALLOC
    EXPIRE --> ZMALLOC
    OBJECTS --> ZMALLOC
    SERVER --> MAXMEM
    EVICT --> EVICTION
    SERVER --> DEFRAG
    ZMALLOC --> USAGE_TRACKING
    ZMALLOC --> OOM_HANDLER
```
Sources: [src/zmalloc.c1-1030](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c#L1-L1030) [src/zmalloc.h1-164](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.h#L1-L164) [src/Makefile79-106](https://github.com/redis/redis/blob/8ad54215/src/Makefile#L79-L106)

## Memory Tracking and Statistics

The `zmalloc` layer provides comprehensive memory usage tracking with thread-safe per-thread counters and detailed allocator statistics.

### Thread-Safe Usage Tracking

Redis tracks memory usage across multiple threads using cache-line aligned per-thread counters to avoid contention:

```mermaid
flowchart TD
    THREAD1["Thread 1used_memory[0]"]
    THREAD2["Thread 2used_memory[1]"]
    THREADN["Thread Nused_memory[n]"]
    TOTAL["zmalloc_used_memory()Sum All Threads"]
    ZMALLOC["zmalloc()"]
    ZCALLOC["zcalloc()"]
    ZREALLOC["zrealloc()"]
    ZFREE["zfree()"]

    ZMALLOC --> THREAD1
    ZCALLOC --> THREAD2
    ZREALLOC --> THREADN
    ZFREE --> THREADN
    THREAD1 --> TOTAL
    THREAD2 --> TOTAL
    THREADN --> TOTAL
```
Sources: [src/zmalloc.c85-109](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c#L85-L109) [src/zmalloc.c503-516](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c#L503-L516)

### Allocator-Specific Statistics

When using jemalloc, Redis exposes detailed memory statistics including fragmentation metrics:

| Function | Purpose | Key Metrics |
| --- | --- | --- |
| `zmalloc_get_allocator_info()` | Global allocator stats | allocated, active, resident, fragmentation |
| `zmalloc_get_allocator_info_by_arena()` | Per-arena stats | arena-specific allocation patterns |
| `zmalloc_get_frag_smallbins()` | Fragmentation analysis | small bin fragmentation bytes |
| `zmalloc_get_rss()` | OS memory usage | resident set size from OS |

Sources: [src/zmalloc.c799-845](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c#L799-L845) [src/zmalloc.c852-891](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c#L852-L891)

## Eviction System Architecture

The eviction system maintains memory usage within configured limits through multiple eviction policies and sampling strategies.

```mermaid
flowchart TD
    GETMAX["getMaxmemoryState()Check Memory Usage"]
    THRESHOLD["maxmemory SettingConfigured Limit"]
    OVERHEAD["freeMemoryGetNotCountedMemory()Exclude Replication Buffers"]
    POOL["EvictionPoolLRU16-entry Sample Pool"]
    POPULATE["evictionPoolPopulate()Sample Keys from DB"]
    SCORE["Policy-based ScoringLRU/LFU/TTL"]
    LRU["LRU PolicyestimateObjectIdleTime()"]
    LFU["LFU PolicyLFUDecrAndReturn()"]
    TTL["TTL PolicyKey Expiration Time"]
    RANDOM["Random PolicyNo Scoring"]
    PERFORM["performEvictions()Main Eviction Loop"]
    TIMELIMIT["evictionTimeLimitUs()Time-bounded Execution"]
    DELETE["deleteKey()Remove Selected Keys"]

    PERFORM --> POOL
    POOL --> POPULATE
    POPULATE --> SCORE
    SCORE --> LRU
    SCORE --> LFU
    SCORE --> TTL
    PERFORM --> TIMELIMIT
    PERFORM --> DELETE
    GETMAX --> THRESHOLD
    GETMAX --> OVERHEAD
```
Sources: [src/evict.c104-116](https://github.com/redis/redis/blob/8ad54215/src/evict.c#L104-L116) [src/evict.c126-215](https://github.com/redis/redis/blob/8ad54215/src/evict.c#L126-L215) [src/evict.c510-700](https://github.com/redis/redis/blob/8ad54215/src/evict.c#L510-L700)

### Eviction Pool Strategy

Redis uses a sampling-based eviction pool to approximate optimal eviction policies efficiently:

-   **Pool Size**: 16 entries (`EVPOOL_SIZE`)
-   **Sampling**: Keys sampled from random dictionary slots
-   **Scoring**: Policy-specific scoring (idle time for LRU, inverted frequency for LFU)
-   **Selection**: Highest scoring key selected for eviction

Sources: [src/evict.c34-42](https://github.com/redis/redis/blob/8ad54215/src/evict.c#L34-L42) [src/evict.c163-214](https://github.com/redis/redis/blob/8ad54215/src/evict.c#L163-L214)

## Key Expiration Management

Redis implements both passive and active expiration strategies to ensure expired keys are removed efficiently.

```mermaid
flowchart TD
    ACCESS["Key Access"]
    CHECK_TTL["Check TTL on Access"]
    LAZY_DELETE["Delete if Expired"]
    CYCLE["activeExpireCycle()Periodic Cleanup"]
    FAST["ACTIVE_EXPIRE_CYCLE_FAST1000μs limit"]
    SLOW["ACTIVE_EXPIRE_CYCLE_SLOW25% CPU limit"]
    SAMPLE["Sample Keysconfig_keys_per_loop"]
    EXPIRE_CHECK["activeExpireCycleTryExpire()Check Each Key"]
    STATS["Update avg_ttl Stats"]
    HFE["activeExpireHashFieldCycle()Hash Field TTL"]
    EBUCKETS["ebIsEmpty()Expiration Bucket Check"]
    FIELD_DELETE["hashTypeDbActiveExpire()Remove Expired Fields"]

    CYCLE --> FAST
    CYCLE --> SLOW
    SLOW --> SAMPLE
    SAMPLE --> EXPIRE_CHECK
    EXPIRE --> CHECK_STATS
    CYCLE --> HFE
    HFE --> EBUCKETS
    HFE --> FIELD_DELETE
    ACCESS --> CHECK_TTL
    CHECK --> TTL_LAZY_DELETE
```
Sources: [src/expire.c187-408](https://github.com/redis/redis/blob/8ad54215/src/expire.c#L187-L408) [src/expire.c38-51](https://github.com/redis/redis/blob/8ad54215/src/expire.c#L38-L51) [src/expire.c144-185](https://github.com/redis/redis/blob/8ad54215/src/expire.c#L144-L185)

### Active Expiration Parameters

| Parameter | Fast Cycle | Slow Cycle | Purpose |
| --- | --- | --- | --- |
| Time Limit | 1000μs | 25% CPU | Prevent blocking |
| Keys per Loop | 20 + effort | 20 + effort | Sampling size |
| Acceptable Stale | 10% - effort | 10% - effort | Continue threshold |
| Database Coverage | All DBs | CRON\_DBS\_PER\_CALL | Coverage strategy |

Sources: [src/expire.c93-98](https://github.com/redis/redis/blob/8ad54215/src/expire.c#L93-L98) [src/expire.c191-200](https://github.com/redis/redis/blob/8ad54215/src/expire.c#L191-L200)

## Memory Allocator Integration

Redis supports multiple memory allocators configured at build time, with jemalloc as the production default.

### Allocator Selection Logic

```mermaid
flowchart TD
    BUILD["Build Configuration"]
    LINUX["Linux Platform?"]
    JEMALLOC_DEFAULT["Default: jemalloc"]
    LIBC_DEFAULT["Default: libc"]
    OVERRIDE_JE["USE_JEMALLOC=yes"]
    OVERRIDE_TC["USE_TCMALLOC=yes"]
    OVERRIDE_LIBC["USE_JEMALLOC=no"]
    SANITIZER["SANITIZER=address/memory"]
    JE_FUNCS["je_malloc()je_free()je_realloc()"]
    TC_FUNCS["tc_malloc()tc_free()tc_realloc()"]
    LIBC_FUNCS["malloc()free()realloc()"]

    BUILD --> LINUX
    LINUX --> JEMALLOC_DEFAULT
    LINUX --> LIBC_DEFAULT
    JEMALLOC --> DEFAULT_OVERRIDE_TC
    JEMALLOC --> DEFAULT_OVERRIDE_LIBC
    LIBC --> DEFAULT_OVERRIDE_JE
    SANITIZER --> LIBC_FUNCS
    OVERRIDE --> JE_JE_FUNCS
    OVERRIDE --> TC_TC_FUNCS
    OVERRIDE --> LIBC_LIBC_FUNCS
```
Sources: [src/Makefile79-106](https://github.com/redis/redis/blob/8ad54215/src/Makefile#L79-L106) [src/zmalloc.c56-80](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c#L56-L80)

### jemalloc Redis Integration

Redis uses a customized jemalloc with Redis-specific features:

-   **Fragmentation Hints**: `JEMALLOC_FRAG_HINT` enables defragmentation support
-   **Usable Size**: `JEMALLOC_ALLOC_WITH_USIZE` provides allocation size feedback
-   **Background Threads**: `set_jemalloc_bg_thread()` controls async purging
-   **Arena Management**: Per-arena statistics and control

Sources: [deps/jemalloc/include/jemalloc/jemalloc\_macros.h.in152-156](https://github.com/redis/redis/blob/8ad54215/deps/jemalloc/include/jemalloc/jemalloc_macros.h.in#L152-L156) [src/zmalloc.c894-912](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c#L894-L912)

## Memory Optimization Strategies

### Active Defragmentation

When enabled with supported allocators, Redis performs active defragmentation to reduce memory fragmentation:

```mermaid
flowchart TD
    SCAN["Scan Memory Objects"]
    ALLOC_NEW["zmalloc_no_tcache()Allocate New Memory"]
    COPY["Copy Object Data"]
    FREE_OLD["zfree_no_tcache()Free Fragmented Memory"]
    THRESHOLD["Fragmentation Threshold"]
    TIME_LIMIT["CPU Time Limits"]
    RATE_LIMIT["Defragmentation Rate"]

    THRESHOLD --> SCAN
    SCAN --> ALLOC_NEW
    ALLOC --> NEW_COPY
    COPY --> FREE_OLD
    TIME --> LIMIT_SCAN
    RATE --> LIMIT_SCAN
```
Sources: [src/zmalloc.c242-256](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c#L242-L256)

### Memory Usage Exclusions

Redis excludes certain memory usage from eviction calculations to prevent feedback loops:

-   **Replication Buffers**: Exclude output buffers beyond backlog size
-   **AOF Buffers**: Exclude append-only file write buffers
-   **Client Buffers**: Configurable client memory limits

Sources: [src/evict.c308-343](https://github.com/redis/redis/blob/8ad54215/src/evict.c#L308-L343) [src/evict.c369-420](https://github.com/redis/redis/blob/8ad54215/src/evict.c#L369-L420)

### RSS and Memory Reporting

Redis provides multiple memory usage metrics for monitoring and debugging:

| Metric | Function | Purpose |
| --- | --- | --- |
| Used Memory | `zmalloc_used_memory()` | Total allocated by Redis |
| RSS | `zmalloc_get_rss()` | OS resident set size |
| Private Dirty | `zmalloc_get_private_dirty()` | Process-private dirty pages |
| Peak Memory | Server stats | Historical maximum usage |

Sources: [src/zmalloc.c607-728](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c#L607-L728) [src/zmalloc.c1024-1060](https://github.com/redis/redis/blob/8ad54215/src/zmalloc.c#L1024-L1060)
