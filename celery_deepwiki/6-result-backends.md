# Result Backends

Relevant source files

-   [celery/app/builtins.py](https://github.com/celery/celery/blob/4d068b56/celery/app/builtins.py)
-   [celery/backends/base.py](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py)
-   [celery/backends/redis.py](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py)
-   [celery/result.py](https://github.com/celery/celery/blob/4d068b56/celery/result.py)
-   [docs/userguide/configuration.rst](https://github.com/celery/celery/blob/4d068b56/docs/userguide/configuration.rst)
-   [t/unit/backends/test\_base.py](https://github.com/celery/celery/blob/4d068b56/t/unit/backends/test_base.py)
-   [t/unit/backends/test\_redis.py](https://github.com/celery/celery/blob/4d068b56/t/unit/backends/test_redis.py)
-   [t/unit/tasks/test\_chord.py](https://github.com/celery/celery/blob/4d068b56/t/unit/tasks/test_chord.py)
-   [t/unit/tasks/test\_result.py](https://github.com/celery/celery/blob/4d068b56/t/unit/tasks/test_result.py)

## Purpose and Scope

Result backends in Celery provide persistent storage and retrieval mechanisms for task execution results and state. When a task completes (successfully or with failure), the worker stores the result in the configured backend. Clients can then query the backend to check task status and retrieve results using the task ID.

This document covers:

-   The backend architecture and interface hierarchy
-   Backend selection and configuration
-   Available backend implementations
-   Result serialization and retrieval patterns
-   Chord coordination mechanisms
-   Error handling and retry strategies

For information about task definition and invocation, see [Tasks](/celery/celery/3-tasks). For worker execution details, see [Workers](/celery/celery/5-workers). For periodic task scheduling, see [Periodic Tasks (Beat)](/celery/celery/7-periodic-tasks-(beat)).

## Backend Architecture Overview

**Diagram: Result Backend Class Hierarchy**

```mermaid
flowchart TD
    Backend["Backendcelery.backends.base.Backend"]
    SyncBackendMixin["SyncBackendMixincelery.backends.base"]
    AsyncBackendMixin["AsyncBackendMixincelery.backends.asynchronous"]
    BaseBackend["BaseBackendcelery.backends.base"]
    KeyValueStoreBackend["BaseKeyValueStoreBackendcelery.backends.base"]
    RedisBackend["RedisBackendcelery.backends.redis"]
    CacheBackend["CacheBackendcelery.backends.cache"]
    DatabaseBackend["DatabaseBackendcelery.backends.database"]
    RPCBackend["RPCBackendcelery.backends.rpc"]
    SentinelBackend["SentinelBackendcelery.backends.redis"]

    Backend --> BaseBackend
    SyncBackendMixin --> BaseBackend
    BaseBackend --> KeyValueStoreBackend
    KeyValueStoreBackend --> RedisBackend
    KeyValueStoreBackend --> CacheBackend
    BaseBackend --> DatabaseBackend
    BaseBackend --> RPCBackend
    AsyncBackendMixin --> RedisBackend
    AsyncBackendMixin --> RPCBackend
    RedisBackend --> SentinelBackend
```
Sources: [celery/backends/base.py108-907](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L108-L907) [celery/backends/redis.py190-196](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L190-L196)

The backend system uses a three-layer abstraction:

1.  **Backend** - Core interface defining lifecycle methods
2.  **BaseBackend** - Synchronous implementation with `SyncBackendMixin`
3.  **Specialized base classes** - `KeyValueStoreBackend` for KV stores, others for specific patterns

### Core Backend Interface

The `Backend` class at [celery/backends/base.py108-823](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L108-L823) defines the fundamental interface all backends must implement:

| Method | Purpose |
| --- | --- |
| `store_result()` | Store task result with state |
| `get_task_meta()` | Retrieve task metadata by ID |
| `mark_as_done()` | Mark task as successfully completed |
| `mark_as_failure()` | Mark task as failed with exception |
| `mark_as_retry()` | Mark task as being retried |
| `mark_as_started()` | Mark task execution has started |
| `forget()` | Remove result from backend |
| `on_chord_part_return()` | Handle chord header task completion |
| `apply_chord()` | Apply chord callback when header completes |

Key attributes defined at [celery/backends/base.py109-136](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L109-L136):

```
READY_STATES = states.READY_STATES
UNREADY_STATES = states.UNREADY_STATES
EXCEPTION_STATES = states.EXCEPTION_STATES

supports_native_join = False
supports_autoexpire = False
persistent = True

retry_policy = {
    'max_retries': 20,
    'interval_start': 0,
    'interval_step': 1,
    'interval_max': 1,
}
```
Sources: [celery/backends/base.py108-823](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L108-L823)

### Backend Initialization

Backend initialization at [celery/backends/base.py138-166](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L138-L166) handles:

-   Serializer configuration from `result_serializer`
-   LRU cache setup with `result_cache_max` limit (or `_nulldict` if disabled)
-   Result expiration with `prepare_expires()`
-   Content type acceptance from `result_accept_content` or `accept_content`
-   Retry configuration: `result_backend_always_retry`, `result_backend_max_retries`, exponential backoff parameters

**Diagram: Backend Initialization Flow**

```mermaid
flowchart TD
    Init["Backend.init"]
    Serializer["Setup Serializerresult_serializer config"]
    Cache["Setup LRU Cache_cache = LRUCache or _nulldict"]
    Expires["Prepare Expirationprepare_expires"]
    Accept["Setup Accept Contentresult_accept_content"]
    Retry["Setup Retry Policyalways_retry, max_retries"]
    Registry["serializer_registry._encoders"]
    NullDict["if max_cached_results == -1:_nulldict"]
    LRU["else:LRUCache(limit=cmax)"]
    Precedence["Precedence:1. accept param2. result_accept_content3. accept_content"]
    BackoffConfig["base_sleep_between_retries_msmax_sleep_between_retries_ms"]

    Init --> Serializer
    Init --> Cache
    Init --> Expires
    Init --> Accept
    Init --> Retry
    Serializer --> Registry
    Cache --> NullDict
    Cache --> LRU
    Accept --> Precedence
    Retry --> BackoffConfig
```
Sources: [celery/backends/base.py138-166](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L138-L166)

## Backend Selection and Registration

The `celery.app.backends` module at [celery/app/backends.py1-70](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L1-L70) provides backend selection through aliases and dynamic loading.

### Backend Aliases

The `BACKEND_ALIASES` dictionary at [celery/app/backends.py15-38](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L15-L38) maps short names to backend classes:

| Alias | Backend Class | Storage Type |
| --- | --- | --- |
| `rpc` | `celery.backends.rpc.RPCBackend` | AMQP messages |
| `redis` / `rediss` | `celery.backends.redis.RedisBackend` | Redis |
| `sentinel` | `celery.backends.redis.SentinelBackend` | Redis Sentinel |
| `database` / `db` | `celery.backends.database.DatabaseBackend` | SQL database |
| `mongodb` | `celery.backends.mongodb.MongoBackend` | MongoDB |
| `cache` | `celery.backends.cache.CacheBackend` | Memcached |
| `cassandra` | `celery.backends.cassandra.CassandraBackend` | Cassandra |
| `elasticsearch` | `celery.backends.elasticsearch.ElasticsearchBackend` | Elasticsearch |
| `couchbase` | `celery.backends.couchbase.CouchbaseBackend` | Couchbase |
| `couchdb` | `celery.backends.couchdb.CouchBackend` | CouchDB |
| `dynamodb` | `celery.backends.dynamodb.DynamoDBBackend` | DynamoDB |
| `s3` | `celery.backends.s3.S3Backend` | Amazon S3 |
| `gs` | `celery.backends.gcs.GCSBackend` | Google Cloud Storage |
| `azureblockblob` | `celery.backends.azureblockblob.AzureBlockBlobBackend` | Azure Blob |
| `file` | `celery.backends.filesystem.FilesystemBackend` | Local filesystem |
| `consul` | `celery.backends.consul.ConsulBackend` | Consul KV |
| `riak` | `celery.backends.riak.RiakBackend` | Riak KV |
| `arangodb` | `celery.backends.arangodb.ArangoDbBackend` | ArangoDB |
| `cosmosdbsql` | `celery.backends.cosmosdbsql.CosmosDBSQLBackend` | Azure Cosmos DB |
| `disabled` | `celery.backends.base.DisabledBackend` | No storage |

Sources: [celery/app/backends.py15-38](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L15-L38)

### Backend Selection Functions

**`by_name(backend, loader)`** at [celery/app/backends.py41-56](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L41-L56):

-   Resolves backend alias to class using `BACKEND_ALIASES`
-   Supports custom backends via `loader.override_backends`
-   Loads extensions from `celery.result_backends` namespace
-   Uses `symbol_by_name()` for dynamic import

**`by_url(backend, loader)`** at [celery/app/backends.py59-69](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L59-L69):

-   Parses backend URL scheme
-   Handles compound schemes like `cache+pylibmc://`
-   Returns tuple of `(backend_class, url)`

Sources: [celery/app/backends.py41-69](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L41-L69)

## Result Storage and Serialization

### Storing Results

**Diagram: Result Storage Flow**

```mermaid
flowchart TD
    StoreResult["store_resultcelery.backends.base:612-644"]
    EncodeResult["encode_resultcelery.backends.base:550-553"]
    PrepareException["prepare_exceptioncelery.backends.base:424-432"]
    PrepareValue["prepare_valuecelery.backends.base:505-509"]
    CheckState["state inEXCEPTION_STATES?"]
    Pickleable["serializer inEXCEPTION_ABLE_CODECS?"]
    GetPickleable["get_pickleable_exception"]
    SerializeDict["Serialize as dict:exc_type, exc_message, exc_module"]
    Retry["Retry Loopwith exponential backoff"]
    InternalStore["_store_resultBackend-specific implementation"]
    CheckException["exception_safe_to_retry?"]
    Backoff["get_exponential_backoff_intervalSleep and retry"]
    Raise["Raise exception"]
    MaxRetries["retries <max_retries?"]
    BackendStoreError["Raise BackendStoreError"]

    StoreResult --> EncodeResult
    EncodeResult --> CheckState
    CheckState --> PrepareException
    CheckState --> PrepareValue
    PrepareException --> Pickleable
    Pickleable --> GetPickleable
    Pickleable --> SerializeDict
    StoreResult --> Retry
    Retry --> InternalStore
    Retry --> CheckException
    CheckException --> Backoff
    CheckException --> Raise
    Backoff --> MaxRetries
    MaxRetries --> Retry
    MaxRetries --> BackendStoreError
```
Sources: [celery/backends/base.py550-644](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L550-L644)

The `store_result()` method at [celery/backends/base.py612-644](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L612-L644):

1.  Encodes the result using `encode_result()` which:
    -   For exception states: calls `prepare_exception()` to serialize exceptions
    -   For success states: calls `prepare_value()` to prepare the value
2.  Implements retry logic when `result_backend_always_retry` is enabled
3.  Uses exponential backoff via `get_exponential_backoff_interval()`
4.  Delegates to backend-specific `_store_result()` method

### Result Metadata Structure

The `_get_result_meta()` method at [celery/backends/base.py558-607](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L558-L607) constructs metadata:

```
meta = {
    'status': state,
    'result': result,
    'traceback': traceback,
    'children': self.current_task_children(request),
    'date_done': date_done,  # ISO format or None
}
```
With `result_extended=True` configuration, additional fields at [celery/backends/base.py581-605](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L581-L605):

```
request_meta = {
    'name': request.task,
    'args': request.args,
    'kwargs': request.kwargs,
    'worker': request.hostname,
    'retries': request.retries,
    'queue': request.delivery_info.get('routing_key'),
}
```
Sources: [celery/backends/base.py558-607](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L558-L607)

### Retrieving Results

**Diagram: Result Retrieval Flow**

```mermaid
flowchart TD
    GetTaskMeta["get_task_metacelery.backends.base:692-729"]
    Cache["Check _cache"]
    GetInternal["_get_task_meta_forBackend-specific"]
    Retry["Retry with backoff"]
    CheckCache["cache enabledand in _cache?"]
    ReturnCached["Return cached meta"]
    Success["Success?"]
    CacheSuccess["Cache if SUCCESS state"]
    CheckRetry["exception_safe_to_retry?"]
    RaiseError["Raise exception"]
    CheckMax["retries <max_retries?"]
    BackendGetMetaError["Raise BackendGetMetaError"]
    ReturnMeta["Return meta"]

    GetTaskMeta --> CheckCache
    CheckCache --> ReturnCached
    CheckCache --> GetInternal
    GetInternal --> Success
    Success --> CacheSuccess
    Success --> CheckRetry
    CheckRetry --> Retry
    CheckRetry --> RaiseError
    Retry --> CheckMax
    CheckMax --> GetInternal
    CheckMax --> BackendGetMetaError
    CacheSuccess --> ReturnMeta
```
Sources: [celery/backends/base.py692-729](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L692-L729)

The `get_task_meta()` method at [celery/backends/base.py692-729](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L692-L729):

1.  Checks LRU cache first for cached results
2.  Calls backend-specific `_get_task_meta_for()`
3.  Implements retry logic with exponential backoff if enabled
4.  Caches SUCCESS state results in `_cache` dictionary
5.  Returns metadata dictionary with status, result, traceback, children

### LRU Cache

The backend uses an LRU cache at [celery/backends/base.py148](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L148-L148) to avoid repeated backend queries:

-   Controlled by `result_cache_max` configuration (default: depends on backend)
-   Set to `-1` to disable caching (uses `_nulldict`)
-   Only SUCCESS state results are cached at [celery/backends/base.py727-728](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L727-L728)
-   Cache cleared on `forget()` at [celery/backends/base.py646-648](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L646-L648)

Sources: [celery/backends/base.py148](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L148-L148) [celery/backends/base.py646-648](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L646-L648) [celery/backends/base.py727-728](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L727-L728)

## Client-Side Result Objects

### AsyncResult

The `AsyncResult` class at [celery/result.py69-548](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L69-L548) provides the primary interface for querying task state:

| Property/Method | Description |
| --- | --- |
| `id` | Task UUID |
| `backend` | Result backend instance |
| `parent` | Parent result in chain |
| `state` / `status` | Current task state (PENDING, STARTED, SUCCESS, etc.) |
| `result` / `info` | Task return value or exception |
| `traceback` | Exception traceback if failed |
| `children` | List of child task results |
| `get(timeout, propagate)` | Wait for and return result |
| `ready()` | Check if task has completed |
| `successful()` | Check if task completed successfully |
| `failed()` | Check if task failed |
| `forget()` | Remove result from backend |
| `revoke()` | Revoke task execution |

Sources: [celery/result.py69-548](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L69-L548)

**Diagram: AsyncResult State Query**

```mermaid
flowchart TD
    AsyncResult["AsyncResultcelery.result.AsyncResult"]
    GetState["state propertyline 477-506"]
    GetResult["result propertyline 460-469"]
    GetTraceback["traceback propertyline 472-474"]
    GetTaskMeta["_get_task_metaline 442-445"]
    MaybeCache["_maybe_set_cacheline 433-440"]
    Backend["backend.get_task_metaline 444"]
    Cache["_cachepopulated?"]
    ReadyState["state inREADY_STATES?"]
    SetCache["_set_cacheStore in _cache"]
    ReturnMeta["Return meta"]

    AsyncResult --> GetState
    AsyncResult --> GetResult
    AsyncResult --> GetTraceback
    GetState --> GetTaskMeta
    GetResult --> GetTaskMeta
    GetTraceback --> GetTaskMeta
    GetTaskMeta --> MaybeCache
    MaybeCache --> Backend
    Backend --> Cache
    Cache --> ReadyState
    ReadyState --> SetCache
    ReadyState --> ReturnMeta
```
Sources: [celery/result.py433-506](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L433-L506)

### Blocking Result Retrieval

The `get()` method at [celery/result.py190-262](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L190-L262) implements blocking result retrieval:

```
def get(self, timeout=None, propagate=True, interval=0.5,
        no_ack=True, follow_parents=True, callback=None,
        on_message=None, on_interval=None,
        disable_sync_subtasks=True):
```
Key behaviors at [celery/result.py235-261](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L235-L261):

1.  Checks `ignored` flag - returns immediately if ignored
2.  Enforces `disable_sync_subtasks` to prevent deadlocks (raises `RuntimeError`)
3.  Follows parent chain if `follow_parents=True`, re-raising parent exceptions
4.  Returns cached result if available
5.  Delegates to `backend.wait_for_pending()` which:
    -   For sync backends: polls `get_task_meta()` at intervals
    -   For async backends: uses native pub/sub mechanisms

Sources: [celery/result.py190-262](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L190-L262)

### ResultSet and GroupResult

**ResultSet** at [celery/result.py551-887](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L551-L887) - Collection of multiple results:

```
results = ResultSet([result1, result2, result3])
all_ready = results.ready()
all_values = results.get()  # or results.join()
```
**GroupResult** at [celery/result.py890-1058](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L890-L1058) - ResultSet with persistent storage:

```
group_result = GroupResult(id='group-id', results=[...])
group_result.save()  # Persist to backend
restored = GroupResult.restore('group-id')  # Restore from backend
```
Key methods:

-   `join()` / `get()` - Wait for all results
-   `join_native()` - Backend-optimized batch retrieval
-   `ready()` - Check if all tasks complete
-   `successful()` / `failed()` - Aggregate status checks
-   `save()` / `restore()` - Persistence operations

Sources: [celery/result.py551-1058](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L551-L1058)

### EagerResult

`EagerResult` at [celery/result.py1061-1109](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L1061-L1109) provides immediate results for eager execution (`task_always_eager=True`):

-   No backend interaction - result stored in memory
-   Supports same interface as `AsyncResult`
-   Used for synchronous testing
-   `ready()` always returns `True`

Sources: [celery/result.py1061-1109](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L1061-L1109)

## Redis Backend Implementation

The Redis backend at [celery/backends/redis.py190-662](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L190-L662) demonstrates a typical implementation with advanced features.

### Redis Backend Architecture

**Diagram: Redis Backend Components**

```mermaid
flowchart TD
    RedisBackend["RedisBackendcelery.backends.redis:190-662"]
    KeyValueStoreBackend["BaseKeyValueStoreBackendcelery.backends.base:910-1063"]
    AsyncBackendMixin["AsyncBackendMixincelery.backends.asynchronous"]
    Client["redis.StrictRedisClient instance"]
    ResultConsumer["ResultConsumercelery.backends.redis:83-188"]
    PubSub["redis.PubSubSubscribe to task keys"]
    ChordSupport["Chord SupportINCR-based coordination"]
    JKey["jkey: Sorted set of results"]
    TKey["tkey: Total counter"]
    SKey["skey: Chord size"]
    Commands["Redis Commands"]
    GET["GET/MGET"]
    SET["SET/SETEX"]
    DEL["DEL"]
    INCR["INCR"]
    ZADD["ZADD/ZRANGE"]
    PUBLISH["PUBLISH"]

    RedisBackend --> KeyValueStoreBackend
    RedisBackend --> AsyncBackendMixin
    RedisBackend --> Client
    RedisBackend --> ResultConsumer
    ResultConsumer --> PubSub
    RedisBackend --> ChordSupport
    ChordSupport --> JKey
    ChordSupport --> TKey
    ChordSupport --> SKey
    RedisBackend --> Commands
    Commands --> GET
    Commands --> SET
    Commands --> DEL
    Commands --> INCR
    Commands --> ZADD
    Commands --> PUBLISH
```
Sources: [celery/backends/redis.py190-662](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L190-L662) [celery/backends/redis.py83-188](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L83-L188)

### Key-Value Store Pattern

`KeyValueStoreBackend` at [celery/backends/base.py910-1063](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L910-L1063) provides the KV abstraction:

```
# Key prefixes
task_keyprefix = 'celery-task-meta-'
group_keyprefix = 'celery-taskset-meta-'
chord_keyprefix = 'chord-unlock-'
```
Backend implementations provide:

-   `get(key)` - Retrieve single value
-   `mget(keys)` - Retrieve multiple values
-   `set(key, value)` - Store value with optional expiration
-   `delete(key)` - Remove key
-   `incr(key)` - Atomic increment (optional)

Sources: [celery/backends/base.py910-1063](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L910-L1063)

### Redis Pub/Sub for Async Results

The `ResultConsumer` at [celery/backends/redis.py83-188](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L83-L188) enables non-polling result retrieval:

**Diagram: Redis ResultConsumer Flow**

```mermaid
flowchart TD
    Start["startline 146-150"]
    Subscribe["Subscribe to task key"]
    DrainEvents["drain_eventsline 161-168"]
    GetMessage["pubsub.get_message"]
    OnStateChange["on_state_changeline 142-144"]
    CreatePubSub["Create pubsub instance"]
    CheckMessage["message andtype=='message'?"]
    Decode["Decode result"]
    Sleep["Sleep timeout"]
    CheckReady["status inREADY_STATES?"]
    Cancel["cancel_forUnsubscribe"]
    Continue["Continue listening"]

    Start --> CreatePubSub
    CreatePubSub --> Subscribe
    DrainEvents --> GetMessage
    GetMessage --> CheckMessage
    CheckMessage --> Decode
    CheckMessage --> Sleep
    Decode --> OnStateChange
    OnStateChange --> CheckReady
    CheckReady --> Cancel
    CheckReady --> Continue
```
Sources: [celery/backends/redis.py83-188](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L83-L188)

Key features:

-   Subscribes to `celery-task-meta-{task_id}` keys
-   Receives results via PUBLISH when task completes
-   Automatically unsubscribes when task reaches READY state
-   Handles connection errors with reconnection logic at [celery/backends/redis.py127-136](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L127-L136)

### Redis Connection Configuration

Redis backend initialization at [celery/backends/redis.py213-328](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L213-L328) supports:

| Configuration | Description |
| --- | --- |
| `redis_host` / `redis_port` / `redis_db` | Connection parameters |
| `redis_password` | Authentication password |
| `redis_username` | Username (Redis 6+) |
| `redis_socket_timeout` | Socket timeout |
| `redis_socket_connect_timeout` | Connection timeout |
| `redis_retry_on_timeout` | Retry on timeout errors |
| `redis_max_connections` | Connection pool size |
| `redis_backend_use_ssl` | SSL/TLS configuration |
| `redis_backend_credential_provider` | Dynamic credential provider |
| `redis_backend_health_check_interval` | Health check interval |

URL format: `redis://[:password]@host:port/db` or `rediss://` for SSL

Sources: [celery/backends/redis.py213-328](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L213-L328)

## Chord Coordination

Chords require backends to coordinate header task completion before executing the callback. Backends implement this through the chord protocol.

### Chord Protocol Interface

At [celery/backends/base.py775-813](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L775-L813) backends implement:

| Method | Purpose |
| --- | --- |
| `on_chord_part_return(request, state, result)` | Called when each header task completes |
| `apply_chord(header_result_args, body)` | Initialize chord execution |
| `set_chord_size(group_id, chord_size)` | Store expected header size |
| `add_to_chord(chord_id, result)` | Add task to chord header |
| `ensure_chords_allowed()` | Verify backend supports chords |

For backends without native support, the fallback at [celery/backends/base.py784-805](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L784-L805) uses:

-   `celery.chord_unlock` task defined at [celery/app/builtins.py37-98](https://github.com/celery/celery/blob/4d068b56/celery/app/builtins.py#L37-L98)
-   Polls header completion using `GroupResult.ready()`
-   Applies callback when all header tasks complete

Sources: [celery/backends/base.py775-813](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L775-L813) [celery/app/builtins.py37-98](https://github.com/celery/celery/blob/4d068b56/celery/app/builtins.py#L37-L98)

### Redis Chord Implementation

**Diagram: Redis Chord Coordination**

```mermaid
flowchart TD
    OnChordPart["on_chord_part_returnredis.py:507-569"]
    EncodeResult["Encode result with state"]
    Pipeline["Redis Pipeline"]
    ZADD["ZADD jkeyScore = group_index"]
    ZCOUNT["ZCOUNT jkey"]
    GET_T["GET tkeyTotal diff"]
    GET_S["GET skeyChord size"]
    Expire["EXPIRE keys if configured"]
    Calculate["readycount == total?"]
    RestoreGroup["GroupResult.restoreline 543"]
    Wait["Wait for more parts"]
    CheckComplex["Any GroupResultin results?"]
    UnlockDirectly["Unlock chord directlyOrdered results"]
    EndNormal["Normal completion"]
    ApplyBody["Apply chord bodywith results"]

    OnChordPart --> EncodeResult
    EncodeResult --> Pipeline
    Pipeline --> ZADD
    Pipeline --> ZCOUNT
    Pipeline --> GET_T
    Pipeline --> GET_S
    Pipeline --> Expire
    GET --> T_Calculate
    GET --> S_Calculate
    Calculate --> RestoreGroup
    Calculate --> Wait
    RestoreGroup --> CheckComplex
    CheckComplex --> UnlockDirectly
    CheckComplex --> EndNormal
    UnlockDirectly --> ApplyBody
```
Sources: [celery/backends/redis.py507-569](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L507-L569)

The Redis implementation at [celery/backends/redis.py507-569](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L507-L569):

1.  Stores each result in sorted set using `ZADD` with `group_index` as score
2.  Counts completed tasks with `ZCOUNT`
3.  Compares against chord size stored in `skey`
4.  When all complete, retrieves ordered results via `ZRANGE`
5.  Applies callback with accumulated results

The `_chord_zset` flag at [celery/backends/redis.py499-501](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L499-L501) controls whether to use:

-   **Sorted set (ZADD/ZRANGE)** - Preserves order, default `True`
-   **List (RPUSH/LRANGE)** - Append order, legacy support

Sources: [celery/backends/redis.py499-569](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L499-L569)

### Chord Error Handling

When a chord header task fails, `chord_error_from_stack()` at [celery/backends/base.py309-335](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L309-L335) handles cleanup:

**Diagram: Chord Error Handling**

```mermaid
flowchart TD
    ChordError["chord_error_from_stackbase.py:309-335"]
    CheckGroup["callback isgroup?"]
    HandleGroup["_handle_group_chord_errorbase.py:337-403"]
    HandleSingle["Handle single callback"]
    FreezeGroup["Freeze group to get task IDs"]
    RevokeAll["Revoke all group tasks"]
    IterateTasks["For each task in group:"]
    CreateFakeRequest["Create fake request context"]
    CallErrbacks["Call error callbacks"]
    MarkFailed["mark_as_failurewith original exception"]
    MarkGroup["Mark group itself as failed"]
    CreateFakeReq2["Create fake request"]
    CallErrbacks2["_call_task_errbacks"]
    FailFromStack["fail_from_current_stack"]

    ChordError --> CheckGroup
    CheckGroup --> HandleGroup
    CheckGroup --> HandleSingle
    HandleGroup --> FreezeGroup
    FreezeGroup --> RevokeAll
    RevokeAll --> IterateTasks
    IterateTasks --> CreateFakeRequest
    CreateFakeRequest --> CallErrbacks
    CallErrbacks --> MarkFailed
    MarkFailed --> MarkGroup
    HandleSingle --> CreateFakeReq2
    CreateFakeReq2 --> CallErrbacks2
    CallErrbacks2 --> FailFromStack
```
Sources: [celery/backends/base.py309-403](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L309-L403)

Special handling for group callbacks at [celery/backends/base.py337-403](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L337-L403):

1.  Revokes all pending tasks in the group body
2.  Creates fake request contexts for each task
3.  Calls error callbacks with the original exception
4.  Marks each task as failed
5.  Prevents group body tasks from hanging indefinitely

## Error Handling and Resilience

### Retry Logic

The backend implements configurable retry logic for transient failures at [celery/backends/base.py612-644](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L612-L644) for `store_result()` and [celery/backends/base.py692-729](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L692-L729) for `get_task_meta()`:

**Configuration options:**

| Setting | Default | Description |
| --- | --- | --- |
| `result_backend_always_retry` | `False` | Enable retry on recoverable errors |
| `result_backend_max_retries` | `inf` | Maximum retry attempts |
| `result_backend_base_sleep_between_retries_ms` | `10` | Initial backoff delay |
| `result_backend_max_sleep_between_retries_ms` | `10000` | Maximum backoff delay |

Sources: [celery/backends/base.py157-161](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L157-L161)

**Exponential Backoff:**

Uses `get_exponential_backoff_interval()` at [celery/backends/base.py635-637](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L635-L637):

```
sleep_amount = get_exponential_backoff_interval(
    self.base_sleep_between_retries_ms,
    retries,
    self.max_sleep_between_retries_ms,
    True
) / 1000
```
Formula provides exponential growth with jitter and capping.

### Exception Safety

Each backend implements `exception_safe_to_retry()` at [celery/backends/base.py682-690](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L682-L690):

```
def exception_safe_to_retry(self, exc):
    """Check if an exception is safe to retry.

    By default no exception is safe to retry.
    Backends must override with correct predicates.
    """
    return False
```
Redis backend implementation at [celery/backends/redis.py401-404](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L401-L404):

```
def exception_safe_to_retry(self, exc):
    if isinstance(exc, self.connection_errors):
        return True
    return False
```
Sources: [celery/backends/base.py682-690](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L682-L690) [celery/backends/redis.py401-404](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L401-L404)

### Exception Serialization

The `prepare_exception()` method at [celery/backends/base.py424-432](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L424-L432) handles exception serialization:

**For pickle serializer:**

-   Uses `get_pickleable_exception()` to create pickleable exception copy
-   Handles unpickleable exceptions by creating synthetic equivalents

**For JSON/other serializers:**

-   Serializes to dictionary at [celery/backends/base.py429-432](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L429-L432):

```
{
    'exc_type': 'ExceptionClass',
    'exc_message': exception_args,
    'exc_module': 'module.name'
}
```
The `exception_to_python()` method at [celery/backends/base.py434-503](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L434-L503) deserializes with security checks:

-   Validates exception class is actually a `BaseException` subclass
-   Prevents arbitrary code execution via malicious stored results
-   Creates synthetic exception classes if original unavailable

Sources: [celery/backends/base.py424-503](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L424-L503)

## Database Backend

The database backend at [celery/backends/database.py](https://github.com/celery/celery/blob/4d068b56/celery/backends/database.py) uses SQLAlchemy or Django ORM for relational storage:

**Table structure:**

-   `celery_taskmeta` - Task results
-   `celery_tasksetmeta` - Group results

**Configuration:**

-   `result_backend = 'db+sqlite:///results.db'`
-   `result_backend = 'db+postgresql://user:pass@host/db'`
-   `database_engine_options` - SQLAlchemy engine options
-   `database_short_lived_sessions` - Session lifecycle management
-   `database_table_names` - Custom table names

**Automatic cleanup:**

-   Does not support `autoexpire`
-   Requires `celery.backend_cleanup` periodic task
-   Defined at [celery/app/builtins.py13-23](https://github.com/celery/celery/blob/4d068b56/celery/app/builtins.py#L13-L23)

Sources: [celery/app/builtins.py13-23](https://github.com/celery/celery/blob/4d068b56/celery/app/builtins.py#L13-L23)

## RPC Backend

The RPC backend at [celery/backends/rpc.py](https://github.com/celery/celery/blob/4d068b56/celery/backends/rpc.py) uses AMQP's reply-to pattern:

**Key characteristics:**

-   No persistent storage - results via message broker
-   Creates per-client reply queue with auto-delete
-   Supports native join via async message consumption
-   Not suitable if results needed after consumer disconnects

**Message flow:**

1.  Client creates exclusive reply queue
2.  Task includes `reply_to` and `correlation_id` in message properties
3.  Worker publishes result to reply queue
4.  Client consumes from reply queue matching correlation\_id

**Limitations:**

-   Results lost if client disconnects
-   No result persistence
-   Cannot query historical results

Sources: Architecture diagrams show RPC as one of 20+ backends

## Testing Matrix

The integration test matrix at [tox.ini1-137](https://github.com/celery/celery/blob/4d068b56/tox.ini#L1-L137) validates backends across Python versions:

**Backend test combinations at [tox.ini6](https://github.com/celery/celery/blob/4d068b56/tox.ini#L6-L6):**

-   `rabbitmq_redis` - RabbitMQ broker + Redis backend
-   `rabbitmq` - RabbitMQ + RPC backend
-   `redis` - Redis broker + Redis backend
-   `dynamodb` - Redis broker + DynamoDB backend
-   `azureblockblob` - Redis broker + Azure Blob backend
-   `cache` - Redis broker + Memcached backend
-   `cassandra` - Redis broker + Cassandra backend
-   `elasticsearch` - Redis broker + Elasticsearch backend

**Test execution:**

-   7 Python versions: 3.9, 3.10, 3.11, 3.12, 3.13, 3.14, PyPy3
-   9 backend configurations
-   Total: 63 test environment combinations

Sources: [tox.ini1-137](https://github.com/celery/celery/blob/4d068b56/tox.ini#L1-L137)
