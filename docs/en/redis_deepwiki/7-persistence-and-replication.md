# Persistence and Replication

Relevant source files

-   [redis.conf](https://github.com/redis/redis/blob/8ad54215/redis.conf)
-   [src/aof.c](https://github.com/redis/redis/blob/8ad54215/src/aof.c)
-   [src/config.c](https://github.com/redis/redis/blob/8ad54215/src/config.c)
-   [src/db.c](https://github.com/redis/redis/blob/8ad54215/src/db.c)
-   [src/debug.c](https://github.com/redis/redis/blob/8ad54215/src/debug.c)
-   [src/module.c](https://github.com/redis/redis/blob/8ad54215/src/module.c)
-   [src/networking.c](https://github.com/redis/redis/blob/8ad54215/src/networking.c)
-   [src/object.c](https://github.com/redis/redis/blob/8ad54215/src/object.c)
-   [src/rdb.c](https://github.com/redis/redis/blob/8ad54215/src/rdb.c)
-   [src/replication.c](https://github.com/redis/redis/blob/8ad54215/src/replication.c)
-   [src/server.c](https://github.com/redis/redis/blob/8ad54215/src/server.c)
-   [src/server.h](https://github.com/redis/redis/blob/8ad54215/src/server.h)
-   [tests/unit/introspection.tcl](https://github.com/redis/redis/blob/8ad54215/tests/unit/introspection.tcl)

This document covers Redis's data persistence mechanisms and master-replica replication system. Persistence ensures data durability through RDB snapshots and AOF transaction logs, while replication enables data synchronization across multiple Redis instances for high availability and read scaling.

For information about clustering and distributed Redis deployments, see [Redis Cluster](/redis/redis/6.1-redis-cluster). For high availability monitoring and failover management, see [Redis Sentinel](/redis/redis/6.2-redis-sentinel).

## Overview

Redis provides two complementary persistence mechanisms and a comprehensive replication system:

**Persistence Systems:**

-   **RDB (Redis Database)**: Point-in-time binary snapshots stored in `.rdb` files
-   **AOF (Append Only File)**: Transaction log recording all write operations in `.aof` files

**Replication System:**

-   Master-replica architecture with asynchronous replication
-   Full synchronization (FULLRESYNC) and partial synchronization (PSYNC)
-   Replication backlog for efficient partial resynchronization
-   RDB channel replication for improved performance during full sync

```mermaid
flowchart TD
    RDB["RDB Snapshotsrdb.c"]
    AOF["AOF Transaction Logaof.c"]
    MANIFEST["AOF ManifestaofManifest"]
    SERVER["redisServerserver.c"]
    DB["redisDbDatabase State"]
    MASTER["Master Instance"]
    REPLICA["Replica Instance"]
    BACKLOG["Replication BacklogreplBacklog"]
    RDBCHAN["RDB Channelrdb channel replication"]

    SERVER --> RDB
    SERVER --> AOF
    SERVER --> BACKLOG
    DB --> RDB
    DB --> AOF
    MASTER --> REPLICA
    BACKLOG --> REPLICA
    RDBCHAN --> REPLICA
    AOF --> MANIFEST
```
Sources: [src/server.h80-81](https://github.com/redis/redis/blob/8ad54215/src/server.h#L80-L81) [src/replication.c16-28](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L16-L28) [src/rdb.c1-50](https://github.com/redis/redis/blob/8ad54215/src/rdb.c#L1-L50) [src/aof.c1-50](https://github.com/redis/redis/blob/8ad54215/src/aof.c#L1-L50)

## RDB Persistence

RDB creates point-in-time binary snapshots of the entire Redis dataset. The system supports both manual snapshots via `BGSAVE` and automatic snapshots based on configurable save points.

### RDB Data Structures and Process

```mermaid
flowchart TD
    LOAD["rdbLoad()rdb.c:2100"]
    PARSE["rdbLoadType()Parse Objects"]
    RESTORE["Restore to redisDb"]
    BGSAVE["rdbSave()rdb.c:1089"]
    FORK["Fork Child Process"]
    WRITE["rdbSaveRio()Write RDB Data"]
    RENAME["Atomic Rename"]
    SAVETYPE["rdbSaveType()rdb.c:101"]
    SAVELEN["rdbSaveLen()rdb.c:157"]
    SAVEOBJ["rdbSaveObject()Object Serialization"]

    BGSAVE --> FORK
    FORK --> WRITE
    WRITE --> SAVETYPE
    WRITE --> SAVELEN
    WRITE --> SAVEOBJ
    WRITE --> RENAME
    LOAD --> PARSE
    PARSE --> RESTORE
```
The RDB format uses type-length-value encoding with compression support:

| Component | Function | Description |
| --- | --- | --- |
| Type Byte | `rdbSaveType()` | Object type identifier |
| Length Encoding | `rdbSaveLen()` | Variable-length integer encoding |
| Object Data | `rdbSaveObject()` | Type-specific serialization |
| Checksum | `rdbSaveRaw()` | CRC64 checksum for integrity |

Sources: [src/rdb.c95-103](https://github.com/redis/redis/blob/8ad54215/src/rdb.c#L95-L103) [src/rdb.c157-188](https://github.com/redis/redis/blob/8ad54215/src/rdb.c#L157-L188) [src/rdb.c1089-1150](https://github.com/redis/redis/blob/8ad54215/src/rdb.c#L1089-L1150)

### RDB Configuration

Key configuration options in `redis.conf`:

```
save 900 1      # Save if at least 1 key changed in 900 seconds
save 300 10     # Save if at least 10 keys changed in 300 seconds
save 60 10000   # Save if at least 10000 keys changed in 60 seconds

dbfilename dump.rdb
rdbcompression yes
rdbchecksum yes
```
The save points are managed by the `saveparam` structure and processed in `serverCron()`.

Sources: [redis.conf394-415](https://github.com/redis/redis/blob/8ad54215/redis.conf#L394-L415) [src/server.h1527-1531](https://github.com/redis/redis/blob/8ad54215/src/server.h#L1527-L1531) [src/config.c344-349](https://github.com/redis/redis/blob/8ad54215/src/config.c#L344-L349)

## AOF Persistence

AOF (Append Only File) logs all write operations in a human-readable format, providing better durability guarantees than RDB at the cost of larger file sizes.

### AOF Architecture

```mermaid
flowchart TD
    CMD["Write Command"]
    PROP["propagateNow()Propagate to AOF"]
    BUF["AOF Bufferserver.aof_buf"]
    FSYNC["AOF Fsyncaof_background_fsync()"]
    REWRITE["rewriteAppendOnlyFile()aof.c:1729"]
    TEMP["Temporary AOF File"]
    INCR["Incremental AOFINCR type files"]
    MANIFEST["AOF ManifestaofManifest structure"]
    BASE["BASE File.base.rdb or .base.aof"]
    INCREMENTAL["INCR Files.incr.aof"]
    HISTORY["HISTORY FilesPrevious versions"]

    REWRITE --> TEMP
    TEMP --> INCR
    INCR --> MANIFEST
    MANIFEST --> BASE
    MANIFEST --> INCREMENTAL
    MANIFEST --> HISTORY
    CMD --> PROP
    PROP --> BUF
    BUF --> FSYNC
```
### AOF Manifest System

The AOF manifest tracks multiple AOF files and their relationships:

| Field | Purpose | Values |
| --- | --- | --- |
| `file_type` | File classification | `'b'` (base), `'i'` (incremental), `'h'` (history) |
| `file_seq` | Sequence number | Monotonically increasing |
| `start_offset` | Starting replication offset | Used for PSYNC |
| `end_offset` | Ending replication offset | Used for PSYNC |

Sources: [src/aof.c72-86](https://github.com/redis/redis/blob/8ad54215/src/aof.c#L72-L86) [src/aof.c153-171](https://github.com/redis/redis/blob/8ad54215/src/aof.c#L153-L171) [src/aof.c210-228](https://github.com/redis/redis/blob/8ad54215/src/aof.c#L210-L228)

### AOF Fsync Policies

```mermaid
flowchart TD
    NO["appendfsync noNo fsync - OS handles"]
    EVERYSEC["appendfsync everysecFsync every second"]
    ALWAYS["appendfsync alwaysFsync after each write"]
    BIO["Bio Threadaof_background_fsync()"]
    MAIN["Main ThreadDirect fsync()"]

    NO --> BIO
    EVERYSEC --> BIO
    ALWAYS --> MAIN
```
Sources: [src/aof.c615-618](https://github.com/redis/redis/blob/8ad54215/src/aof.c#L615-L618) [src/config.c80-85](https://github.com/redis/redis/blob/8ad54215/src/config.c#L80-L85) [src/bio.h50-60](https://github.com/redis/redis/blob/8ad54215/src/bio.h#L50-L60)

## Replication Architecture

Redis replication follows a master-replica model with asynchronous data synchronization. The system supports both full and partial synchronization to optimize network usage and minimize downtime.

### Core Replication Data Structures

```mermaid
flowchart TD
    REPLID["server.replidReplication ID"]
    REPLOFF["server.master_repl_offsetCurrent offset"]
    BACKLOG["server.repl_backlogCircular buffer"]
    SLAVES["server.slavesConnected replicas"]
    MASTERHOST["server.masterhostMaster address"]
    REPLSTATE["server.repl_stateConnection state"]
    REPLOFFSET["server.repl_ack_offAcknowledged offset"]
    CACHED["server.cached_masterCached connection"]
    BLOCKS["server.repl_buffer_blocksList of replBufBlock"]
    INDEX["blocks_indexRax tree for fast lookup"]
    HISTLEN["histlenTotal history length"]

    REPLOFF --> BACKLOG
    BACKLOG --> BLOCKS
    BLOCKS --> INDEX
    SLAVES --> REPLSTATE
```
The `replBacklog` structure manages the replication buffer:

| Field | Type | Purpose |
| --- | --- | --- |
| `ref_repl_buf_node` | `listNode*` | Reference to first buffer block |
| `histlen` | `long long` | Total bytes in backlog |
| `offset` | `long long` | Starting offset of backlog |
| `blocks_index` | `rax*` | Index for fast offset lookup |

Sources: [src/server.h1715-1724](https://github.com/redis/redis/blob/8ad54215/src/server.h#L1715-L1724) [src/replication.c163-174](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L163-L174) [src/replication.c213-223](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L213-L223)

## Master-Replica Synchronization

### PSYNC Protocol State Machine

> **[Mermaid stateDiagram]**
> *(图表结构无法解析)*

### Synchronization Types

**Full Synchronization (FULLRESYNC):**

-   Triggered when replica connects for the first time or when partial resync is not possible
-   Master creates RDB snapshot and sends entire dataset
-   Can use disk-based or diskless replication

**Partial Synchronization (PSYNC):**

-   Uses replication ID and offset to resume from a specific point
-   Relies on replication backlog to replay missed commands
-   Much faster than full synchronization

> **[Mermaid sequence]**
> *(图表结构无法解析)*

Sources: [src/replication.c498-514](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L498-L514) [src/replication.c1089-1150](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L1089-L1150) [src/server.h498-514](https://github.com/redis/redis/blob/8ad54215/src/server.h#L498-L514)

### RDB Channel Replication

For improved performance during full synchronization, Redis supports RDB channel replication where the replica opens two connections:

1.  **Main channel**: Receives replication stream (buffered during RDB loading)
2.  **RDB channel**: Receives RDB data for loading

```mermaid
flowchart TD
    MAIN_CONN["Main ConnectionReplication stream"]
    RDB_CONN["RDB ConnectionRDB data transfer"]
    BGSAVE["BGSAVE Process"]
    MAIN_BUF["Main Channel BufferAccumulate commands"]
    RDB_LOAD["RDB LoadingrdbLoadRio()"]
    APPLY["Apply Buffered Commands"]

    BGSAVE --> RDB_CONN
    RDB --> CONN_RDB_LOAD
    MAIN --> CONN_MAIN_BUF
    RDB --> LOAD_APPLY
    MAIN --> BUF_APPLY
```
This approach allows the replica to receive the RDB snapshot while simultaneously buffering new writes from the master, reducing synchronization time and master memory usage.

Sources: [src/replication.c26](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L26-L26) [src/replication.c73-81](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L73-L81) [src/replication.c556-560](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L556-L560)

## Replication Buffer Management

### Buffer Block Structure

The replication system uses a linked list of `replBufBlock` structures to efficiently manage the replication stream:

```mermaid
flowchart TD
    B1["replBufBlock 1repl_offset: 1000size: 16KBrefcount: 3"]
    B2["replBufBlock 2repl_offset: 17384size: 16KBrefcount: 2"]
    B3["replBufBlock 3repl_offset: 33768size: 8KBrefcount: 1"]
    IDX["offset -> block mappingFast PSYNC lookup"]
    R1["Replica 1offset: 1000"]
    R2["Replica 2offset: 17384"]
    R3["Replica 3offset: 33768"]

    B1 --> B2
    B2 --> B3
    R1 --> B1
    R2 --> B2
    R3 --> B3
    IDX --> B1
    IDX --> B2
```
The reference counting system ensures blocks are freed only when no replicas need them, while the rax tree index enables fast offset lookups for PSYNC operations.

Sources: [src/replication.c213-223](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L213-L223) [src/replication.c318-371](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L318-L371) [src/server.h1715-1724](https://github.com/redis/redis/blob/8ad54215/src/server.h#L1715-L1724)

## Configuration and Management

### Key Configuration Parameters

| Parameter | Default | Purpose |
| --- | --- | --- |
| `repl-backlog-size` | 1MB | Size of replication backlog |
| `repl-backlog-ttl` | 3600 | Seconds to keep backlog after last replica |
| `repl-diskless-sync` | no | Use diskless replication |
| `repl-diskless-load` | disabled | Load RDB directly from socket |
| `min-replicas-to-write` | 0 | Minimum replicas for writes |
| `min-replicas-max-lag` | 10 | Maximum replica lag in seconds |

### Monitoring and Diagnostics

Redis provides several commands for monitoring persistence and replication:

-   `INFO replication` - Replication status and metrics
-   `INFO persistence` - RDB and AOF statistics
-   `LASTSAVE` - Timestamp of last successful RDB save
-   `BGREWRITEAOF` - Trigger AOF rewrite
-   `BGSAVE` - Trigger RDB snapshot

The server tracks various metrics including replication lag, backlog statistics, and persistence operation counts accessible through the `INFO` command.

Sources: [redis.conf394-500](https://github.com/redis/redis/blob/8ad54215/redis.conf#L394-L500) [src/server.h1527-1600](https://github.com/redis/redis/blob/8ad54215/src/server.h#L1527-L1600) [src/replication.c3500-3600](https://github.com/redis/redis/blob/8ad54215/src/replication.c#L3500-L3600)
