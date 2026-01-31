# 结果后端 (Result Backends)

相关源文件

-   [celery/app/builtins.py](https://github.com/celery/celery/blob/4d068b56/celery/app/builtins.py)
-   [celery/backends/base.py](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py)
-   [celery/backends/redis.py](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py)
-   [celery/result.py](https://github.com/celery/celery/blob/4d068b56/celery/result.py)
-   [docs/userguide/configuration.rst](https://github.com/celery/celery/blob/4d068b56/docs/userguide/configuration.rst)
-   [t/unit/backends/test\_base.py](https://github.com/celery/celery/blob/4d068b56/t/unit/backends/test_base.py)
-   [t/unit/backends/test\_redis.py](https://github.com/celery/celery/blob/4d068b56/t/unit/backends/test_redis.py)
-   [t/unit/tasks/test\_chord.py](https://github.com/celery/celery/blob/4d068b56/t/unit/tasks/test_chord.py)
-   [t/unit/tasks/test\_result.py](https://github.com/celery/celery/blob/4d068b56/t/unit/tasks/test_result.py)

## 目的与范围

Celery 中的结果后端 (Result backends) 为任务执行结果和状态提供了持久化存储与检索机制。当任务完成（成功或失败）时，工作者会将结果存储在配置好的后端中。客户端随后可以查询该后端以检查任务状态，并使用任务 ID 检索结果。

本文件涵盖：

-   后端架构与接口层级
-   后端的选择与配置
-   可用的后端实现
-   结果序列化与检索模式
-   Chord 协调机制
-   错误处理与重试策略

有关任务定义与调用的信息，请参阅[任务 (Tasks)](/celery/celery/3-tasks)。有关工作者执行详情，请参阅[工作者 (Workers)](/celery/celery/5-workers)。有关周期性任务调度的信息，请参阅[周期性任务 (Beat)](/celery/celery/7-periodic-tasks-(beat))。

## 后端架构概览 (Backend Architecture Overview)

**图表：结果后端类层级**

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
来源：[celery/backends/base.py108-907](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L108-L907) [celery/backends/redis.py190-196](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L190-L196)

后端系统使用三层抽象：

1.  **Backend** —— 定义生命周期方法的核心接口
2.  **BaseBackend** —— 带有 `SyncBackendMixin` 的同步实现
3.  **专门的基类** —— 针对键值存储的 `KeyValueStoreBackend`，以及针对特定模式的其他类

### 核心后端接口

位于 [celery/backends/base.py108-823](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L108-L823) 的 `Backend` 类定义了所有后端必须实现的基础接口：

| 方法 | 目的 |
| --- | --- |
| `store_result()` | 存储带有状态的任务结果 |
| `get_task_meta()` | 按 ID 检索任务元数据 |
| `mark_as_done()` | 将任务标记为成功完成 |
| `mark_as_failure()` | 将任务标记为因异常失败 |
| `mark_as_retry()` | 将任务标记为正在重试 |
| `mark_as_started()` | 标记任务执行已开始 |
| `forget()` | 从后端移除结果 |
| `on_chord_part_return()` | 处理 chord header 任务完成 |
| `apply_chord()` | 当 header 完成时应用 chord 回调 |

在 [celery/backends/base.py109-136](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L109-L136) 定义的关键属性：

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
来源：[celery/backends/base.py108-823](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L108-L823)

### 后端初始化 (Backend Initialization)

在 [celery/backends/base.py138-166](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L138-L166) 的后端初始化处理：

-   来自 `result_serializer` 的序列化器配置
-   带有 `result_cache_max` 限制的 LRU 缓存设置（如果禁用则使用 `_nulldict`）
-   通过 `prepare_expires()` 进行结果过期设置
-   来自 `result_accept_content` 或 `accept_content` 的内容类型接受设置
-   重试配置：`result_backend_always_retry`, `result_backend_max_retries`, 指数退避参数

**图表：后端初始化流**

```mermaid
flowchart TD
    Init["Backend.init"]
    Serializer["设置序列化器result_serializer 配置"]
    Cache["设置 LRU 缓存_cache = LRUCache 或 _nulldict"]
    Expires["准备过期设置prepare_expires"]
    Accept["设置接受内容result_accept_content"]
    Retry["设置重试策略always_retry, max_retries"]
    Registry["serializer_registry._encoders"]
    NullDict["如果 max_cached_results == -1:_nulldict"]
    LRU["否则:LRUCache(limit=cmax)"]
    Precedence["优先级:1. accept 参数2. result_accept_content3. accept_content"]
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
来源：[celery/backends/base.py138-166](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L138-L166)

## 后端选择与注册

`celery.app.backends` 模块（位于 [celery/app/backends.py1-70](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L1-L70)）通过别名和动态加载提供后端选择。

### 后端别名 (Backend Aliases)

位于 [celery/app/backends.py15-38](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L15-L38) 的 `BACKEND_ALIASES` 字典将短名称映射到后端类：

| 别名 | 后端类 | 存储类型 |
| --- | --- | --- |
| `rpc` | `celery.backends.rpc.RPCBackend` | AMQP 消息 |
| `redis` / `rediss` | `celery.backends.redis.RedisBackend` | Redis |
| `sentinel` | `celery.backends.redis.SentinelBackend` | Redis Sentinel |
| `database` / `db` | `celery.backends.database.DatabaseBackend` | SQL 数据库 |
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
| `file` | `celery.backends.filesystem.FilesystemBackend` | 本地文件系统 |
| `consul` | `celery.backends.consul.ConsulBackend` | Consul KV |
| `riak` | `celery.backends.riak.RiakBackend` | Riak KV |
| `arangodb` | `celery.backends.arangodb.ArangoDbBackend` | ArangoDB |
| `cosmosdbsql` | `celery.backends.cosmosdbsql.CosmosDBSQLBackend` | Azure Cosmos DB |
| `disabled` | `celery.backends.base.DisabledBackend` | 无存储 |

来源：[celery/app/backends.py15-38](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L15-L38)

### 后端选择函数

**`by_name(backend, loader)`** 位于 [celery/app/backends.py41-56](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L41-L56)：

-   使用 `BACKEND_ALIASES` 将后端别名解析为类
-   通过 `loader.override_backends` 支持自定义后端
-   从 `celery.result_backends` 命名空间加载扩展
-   使用 `symbol_by_name()` 进行动态导入

**`by_url(backend, loader)`** 位于 [celery/app/backends.py59-69](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L59-L69)：

-   解析后端 URL 协议 (scheme)
-   处理诸如 `cache+pylibmc://` 之类的复合协议
-   返回 `(backend_class, url)` 元组

来源：[celery/app/backends.py41-69](https://github.com/celery/celery/blob/4d068b56/celery/app/backends.py#L41-L69)

## 结果存储与序列化

### 存储结果 (Storing Results)

**图表：结果存储流**

```mermaid
flowchart TD
    StoreResult["store_resultcelery.backends.base:612-644"]
    EncodeResult["encode_resultcelery.backends.base:550-553"]
    PrepareException["prepare_exceptioncelery.backends.base:424-432"]
    PrepareValue["prepare_valuecelery.backends.base:505-509"]
    CheckState["状态是否在 EXCEPTION_STATES 中？"]
    Pickleable["序列化器是否在 EXCEPTION_ABLE_CODECS 中？"]
    GetPickleable["get_pickleable_exception"]
    SerializeDict["序列化为字典：exc_type, exc_message, exc_module"]
    Retry["带有指数退避的重试循环"]
    InternalStore["_store_result后端特定的实现"]
    CheckException["exception_safe_to_retry?"]
    Backoff["get_exponential_backoff_interval休眠并重试"]
    Raise["抛出异常"]
    MaxRetries["重试次数 <max_retries?"]
    BackendStoreError["抛出 BackendStoreError"]

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
来源：[celery/backends/base.py550-644](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L550-L644)

位于 [celery/backends/base.py612-644](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L612-L644) 的 `store_result()` 方法：

1.  使用 `encode_result()` 对结果进行编码，该方法：
    -   对于异常状态：调用 `prepare_exception()` 来序列化异常
    -   对于成功状态：调用 `prepare_value()` 来准备结果值
2.  当启用 `result_backend_always_retry` 时实现重试逻辑
3.  通过 `get_exponential_backoff_interval()` 使用指数退避
4.  委派给后端特定的 `_store_result()` 方法

### 结果元数据结构

位于 [celery/backends/base.py558-607](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L558-L607) 的 `_get_result_meta()` 方法构造元数据：

```
meta = {
    'status': state,
    'result': result,
    'traceback': traceback,
    'children': self.current_task_children(request),
    'date_done': date_done,  # ISO 格式或 None
}
```
当配置 `result_extended=True` 时，包含 [celery/backends/base.py581-605](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L581-L605) 处的额外字段：

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
来源：[celery/backends/base.py558-607](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L558-L607)

### 检索结果 (Retrieving Results)

**图表：结果检索流**

```mermaid
flowchart TD
    GetTaskMeta["get_task_metacelery.backends.base:692-729"]
    Cache["检查 _cache"]
    GetInternal["_get_task_meta_for后端特定的实现"]
    Retry["带有退避的重试"]
    CheckCache["缓存已启用且在 _cache 中？"]
    ReturnCached["返回缓存的元数据"]
    Success["是否成功？"]
    CacheSuccess["如果状态为 SUCCESS 则进行缓存"]
    CheckRetry["exception_safe_to_retry?"]
    RaiseError["抛出异常"]
    CheckMax["重试次数 <max_retries?"]
    BackendGetMetaError["抛出 BackendGetMetaError"]
    ReturnMeta["返回元数据"]

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
来源：[celery/backends/base.py692-729](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L692-L729)

位于 [celery/backends/base.py692-729](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L692-L729) 的 `get_task_meta()` 方法：

1.  首先检查 LRU 缓存以查找已缓存的结果
2.  调用后端特定的 `_get_task_meta_for()`
3.  如果启用，则使用指数退避实现重试逻辑
4.  在 `_cache` 字典中缓存 SUCCESS 状态的结果
5.  返回包含 status, result, traceback, children 的元数据字典

### LRU 缓存

后端在 [celery/backends/base.py148](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L148-L148) 使用 LRU 缓存来避免重复的后端查询：

-   由 `result_cache_max` 配置控制（默认值取决于后端）
-   设置为 `-1` 以禁用缓存（使用 `_nulldict`）
-   仅缓存 SUCCESS 状态的结果，见 [celery/backends/base.py727-728](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L727-L728)
-   在 `forget()` 时清除缓存，见 [celery/backends/base.py646-648](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L646-L648)

来源：[celery/backends/base.py148](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L148-L148) [celery/backends/base.py646-648](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L646-L648) [celery/backends/base.py727-728](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L727-L728)

## 客户端结果对象

### AsyncResult

位于 [celery/result.py69-548](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L69-L548) 的 `AsyncResult` 类提供了查询任务状态的主要接口：

| 属性/方法 | 描述 |
| --- | --- |
| `id` | 任务 UUID |
| `backend` | 结果后端实例 |
| `parent` | 链中的父结果 |
| `state` / `status` | 当前任务状态 (PENDING, STARTED, SUCCESS 等) |
| `result` / `info` | 任务返回值或异常 |
| `traceback` | 失败时的异常回溯 |
| `children` | 子任务结果列表 |
| `get(timeout, propagate)` | 等待并返回结果 |
| `ready()` | 检查任务是否已完成 |
| `successful()` | 检查任务是否成功完成 |
| `failed()` | 检查任务是否失败 |
| `forget()` | 从后端移除结果 |
| `revoke()` | 撤销任务执行 |

来源：[celery/result.py69-548](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L69-L548)

**图表：AsyncResult 状态查询**

```mermaid
flowchart TD
    AsyncResult["AsyncResultcelery.result.AsyncResult"]
    GetState["state 属性477-506 行"]
    GetResult["result 属性460-469 行"]
    GetTraceback["traceback 属性472-474 行"]
    GetTaskMeta["_get_task_meta442-445 行"]
    MaybeCache["_maybe_set_cache433-440 行"]
    Backend["backend.get_task_meta444 行"]
    Cache["_cache是否已填充？"]
    ReadyState["状态是否在 READY_STATES 中？"]
    SetCache["_set_cache存储在 _cache 中"]
    ReturnMeta["返回元数据"]

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
来源：[celery/result.py433-506](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L433-L506)

### 阻塞式结果检索 (Blocking Result Retrieval)

位于 [celery/result.py190-262](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L190-L262) 的 `get()` 方法实现了阻塞式结果检索：

```
def get(self, timeout=None, propagate=True, interval=0.5,
        no_ack=True, follow_parents=True, callback=None,
        on_message=None, on_interval=None,
        disable_sync_subtasks=True):
```
在 [celery/result.py235-261](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L235-L261) 的关键行为：

1.  检查 `ignored` 标志 —— 如果被忽略则立即返回
2.  强制执行 `disable_sync_subtasks` 以防止死锁（抛出 `RuntimeError`）
3.  如果 `follow_parents=True`，则追踪父链，重新抛出父任务异常
4.  如果可用，则返回缓存的结果
5.  委派给 `backend.wait_for_pending()`，该方法：
    -   对于同步后端：每隔一定间隔轮询 `get_task_meta()`
    -   对于异步后端：使用原生的发布/订阅机制

来源：[celery/result.py190-262](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L190-L262)

### ResultSet 与 GroupResult

**ResultSet** 位于 [celery/result.py551-887](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L551-L887) —— 多个结果的集合：

```
results = ResultSet([result1, result2, result3])
all_ready = results.ready()
all_values = results.get()  # 或 results.join()
```
**GroupResult** 位于 [celery/result.py890-1058](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L890-L1058) —— 具有持久化存储的 ResultSet：

```
group_result = GroupResult(id='group-id', results=[...])
group_result.save()  # 持久化到后端
restored = GroupResult.restore('group-id')  # 从后端恢复
```
关键方法：

-   `join()` / `get()` —— 等待所有结果
-   `join_native()` —— 后端优化的批量检索
-   `ready()` —— 检查是否所有任务都已完成
-   `successful()` / `failed()` —— 汇总状态检查
-   `save()` / `restore()` —— 持久化操作

来源：[celery/result.py551-1058](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L551-L1058)

### EagerResult

位于 [celery/result.py1061-1109](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L1061-L1109) 的 `EagerResult` 为即时执行 (`task_always_eager=True`) 提供立即结果：

-   无后端交互 —— 结果存储在内存中
-   支持与 `AsyncResult` 相同的接口
-   用于同步测试
-   `ready()` 始终返回 `True`

来源：[celery/result.py1061-1109](https://github.com/celery/celery/blob/4d068b56/celery/result.py#L1061-L1109)

## Redis 后端实现

位于 [celery/backends/redis.py190-662](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L190-L662) 的 Redis 后端展示了一个具有高级特性的典型实现。

### Redis 后端架构

**图表：Redis 后端组件**

```mermaid
flowchart TD
    RedisBackend["RedisBackendcelery.backends.redis:190-662"]
    KeyValueStoreBackend["BaseKeyValueStoreBackendcelery.backends.base:910-1063"]
    AsyncBackendMixin["AsyncBackendMixincelery.backends.asynchronous"]
    Client["redis.StrictRedis 客户端实例"]
    ResultConsumer["ResultConsumercelery.backends.redis:83-188"]
    PubSub["redis.PubSub订阅任务键"]
    ChordSupport["Chord 支持基于 INCR 的协调"]
    JKey["jkey: 结果的有序集合"]
    TKey["tkey: 总数计数器"]
    SKey["skey: Chord 大小"]
    Commands["Redis 命令"]
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
来源：[celery/backends/redis.py190-662](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L190-L662) [celery/backends/redis.py83-188](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L83-L188)

### 键值存储模式

位于 [celery/backends/base.py910-1063](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L910-L1063) 的 `KeyValueStoreBackend` 提供了 KV 抽象：

```
# 键前缀
task_keyprefix = 'celery-task-meta-'
group_keyprefix = 'celery-taskset-meta-'
chord_keyprefix = 'chord-unlock-'
```
后端实现提供了：

-   `get(key)` —— 检索单个值
-   `mget(keys)` —— 检索多个键
-   `set(key, value)` —— 存储值并带有可选过期时间
-   `delete(key)` —— 移除键
-   `incr(key)` —— 原子递增 (可选)

来源：[celery/backends/base.py910-1063](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L910-L1063)

### 用于异步结果的 Redis 发布/订阅

位于 [celery/backends/redis.py83-188](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L83-L188) 的 `ResultConsumer` 实现了非轮询式的结果检索：

**图表：Redis ResultConsumer 流**

```mermaid
flowchart TD
    Start["开始146-150 行"]
    Subscribe["订阅任务键"]
    DrainEvents["drain_events161-168 行"]
    GetMessage["pubsub.get_message"]
    OnStateChange["on_state_change142-144 行"]
    CreatePubSub["创建 pubsub 实例"]
    CheckMessage["是否 message 且 type=='message'？"]
    Decode["解码结果"]
    Sleep["休眠超时"]
    CheckReady["状态是否在 READY_STATES 中？"]
    Cancel["cancel_for 退订"]
    Continue["继续监听"]

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
来源：[celery/backends/redis.py83-188](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L83-L188)

关键特性：

-   订阅 `celery-task-meta-{task_id}` 键
-   当任务完成时，通过 PUBLISH 接收结果
-   当任务达到 READY 状态时自动退订
-   通过 [celery/backends/redis.py127-136](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L127-L136) 处的重连逻辑处理连接错误

### Redis 连接配置

后端支持广泛的 Redis 连接配置 [celery/backends/redis.py213-328](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L213-L328)：

| 参数 | 配置键 | 描述 |
| --- | --- | --- |
| `host` | `redis_host` | Redis 服务器主机名 |
| `port` | `redis_port` | Redis 服务器端口 |
| `db` | `redis_db` | Redis 数据库编号 |
| `password` | `redis_password` | 认证密码 |
| `username` | `redis_username` | 用户名 (Redis 6.0+) |
| `max_connections` | `redis_max_connections` | 连接池大小 |

URL 格式：`redis://[:password]@host:port/db` 或使用 `rediss://` 进行 SSL 连接

来源：[celery/backends/redis.py213-328](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L213-L328)

## Chord 协调

Chord 要求后端在执行回调之前协调 header 任务的完成情况。后端通过 chord 协议来实现这一点。

### Chord 协议接口

后端在 [celery/backends/base.py775-813](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L775-L813) 实现以下接口：

| 方法 | 目的 |
| --- | --- |
| `on_chord_part_return(request, state, result)` | 每个 header 任务完成时调用 |
| `apply_chord(header_result_args, body)` | 初始化 chord 执行 |
| `set_chord_size(group_id, chord_size)` | 存储预期的 header 大小 |
| `add_to_chord(chord_id, result)` | 向 chord header 添加任务 |
| `ensure_chords_allowed()` | 验证后端是否支持 chord |

对于不具备原生支持的后端，在 [celery/backends/base.py784-805](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L784-L805) 的回退方案使用了：

-   在 [celery/app/builtins.py37-98](https://github.com/celery/celery/blob/4d068b56/celery/app/builtins.py#L37-L98) 定义的 `celery.chord_unlock` 任务
-   使用 `GroupResult.ready()` 轮询 header 完成情况
-   当所有 header 任务完成时应用回调

来源：[celery/backends/base.py775-813](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L775-L813) [celery/app/builtins.py37-98](https://github.com/celery/celery/blob/4d068b56/celery/app/builtins.py#L37-L98)

### Redis Chord 实现

**图表：Redis Chord 协调**

```mermaid
flowchart TD
    OnChordPart["on_chord_part_returnredis.py:507-569"]
    EncodeResult["对带有状态的结果进行编码"]
    Pipeline["Redis 流水线 (Pipeline)"]
    ZADD["ZADD jkey分数 = group_index"]
    ZCOUNT["ZCOUNT jkey"]
    GET_T["GET tkey总差异"]
    GET_S["GET skeyChord 大小"]
    Expire["如果已配置，则为键设置 EXPIRE"]
    Calculate["readycount == total?"]
    RestoreGroup["GroupResult.restore543 行"]
    Wait["等待更多部分"]
    CheckComplex["结果中是否有任何 GroupResult？"]
    UnlockDirectly["直接解锁 chord有序结果"]
    EndNormal["正常完成"]
    ApplyBody["使用累积的结果应用 chord body"]

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
来源：[celery/backends/redis.py507-569](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L507-L569)

[celery/backends/redis.py507-569](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L507-L569) 处的 Redis 实现：

1.  使用 `ZADD` 将每个结果存储在有序集合中，并以 `group_index` 作为分数
2.  使用 `ZCOUNT` 统计已完成的任务
3.  与存储在 `skey` 中的 chord 大小进行比较
4.  当全部完成时，通过 `ZRANGE` 检索有序结果
5.  使用累积的结果应用回调

[celery/backends/redis.py499-501](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L499-L501) 处的 `_chord_zset` 标志控制是否使用：

-   **有序集合 (ZADD/ZRANGE)** —— 保留顺序，默认值为 `True`
-   **列表 (RPUSH/LRANGE)** —— 追加顺序，遗留支持

来源：[celery/backends/redis.py499-569](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L499-L569)

### Chord 错误处理

当一个 chord header 任务失败时，[celery/backends/base.py309-335](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L309-L335) 处的 `chord_error_from_stack()` 会处理清理工作：

**图表：Chord 错误处理**

```mermaid
flowchart TD
    ChordError["chord_error_from_stackbase.py:309-335"]
    CheckGroup["回调是否为 group？"]
    HandleGroup["_handle_group_chord_errorbase.py:337-403"]
    HandleSingle["处理单个回调"]
    FreezeGroup["冻结组以获得任务 ID"]
    RevokeAll["撤销所有组任务"]
    IterateTasks["针对组中的每个任务："]
    CreateFakeRequest["创建伪造的请求上下文"]
    CallErrbacks["调用错误回调"]
    MarkFailed["使用原始异常 mark_as_failure"]
    MarkGroup["将组本身标记为失败"]
    CreateFakeReq2["创建伪造请求"]
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
来源：[celery/backends/base.py309-403](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L309-L403)

[celery/backends/base.py337-403](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L337-L403) 处针对组回调的特殊处理：

1.  撤销组主体中所有挂起的任务
2.  为每个任务创建伪造的请求上下文
3.  使用原始异常调用错误回调
4.  将每个任务标记为失败
5.  防止组主体任务无限期挂起

## 错误处理与弹性 (Error Handling and Resilience)

### 重试逻辑 (Retry Logic)

后端在 [celery/backends/base.py612-644](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L612-L644) (针对 `store_result()`) 和 [celery/backends/base.py692-729](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L692-L729) (针对 `get_task_meta()`) 实现了针对瞬态故障的可配置重试逻辑：

**配置选项：**

| 设置项 | 默认值 | 描述 |
| --- | --- | --- |
| `result_backend_always_retry` | `False` | 启用针对可恢复错误的自动重试 |
| `result_backend_max_retries` | `inf` | 最大重试尝试次数 |
| `result_backend_base_sleep_between_retries_ms` | `10` | 初始退避延迟 |
| `result_backend_max_sleep_between_retries_ms` | `10000` | 最大退避延迟 |

来源：[celery/backends/base.py157-161](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L157-L161)

**指数退避 (Exponential Backoff)：**

使用 [celery/backends/base.py635-637](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L635-L637) 处的 `get_exponential_backoff_interval()`：

```
sleep_amount = get_exponential_backoff_interval(
    self.base_sleep_between_retries_ms,
    retries,
    self.max_sleep_between_retries_ms,
    True
) / 1000
```
该公式提供了带有抖动 (jitter) 和上限的指数级增长。

### 异常安全性 (Exception Safety)

每个后端都实现了 [celery/backends/base.py682-690](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L682-L690) 处的 `exception_safe_to_retry()`：

```
def exception_safe_to_retry(self, exc):
    """检查异常是否可以安全地进行重试。

    默认情况下，没有任何异常是安全可重试的。
    后端必须使用正确的谓词进行重写。
    """
    return False
```
[celery/backends/redis.py401-404](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L401-L404) 处的 Redis 后端实现：

```
def exception_safe_to_retry(self, exc):
    if isinstance(exc, self.connection_errors):
        return True
    return False
```
来源：[celery/backends/base.py682-690](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L682-L690) [celery/backends/redis.py401-404](https://github.com/celery/celery/blob/4d068b56/celery/backends/redis.py#L401-L404)

### 异常序列化

[celery/backends/base.py424-432](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L424-L432) 处的 `prepare_exception()` 方法处理异常序列化：

**对于 pickle 序列化器：**

-   使用 `get_pickleable_exception()` 创建异常的 pickle 拷贝
-   通过创建合成等效物来处理不可 pickle 的异常

**对于 JSON/其他序列化器：**

-   在 [celery/backends/base.py429-432](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L429-L432) 处序列化为字典：

```
{
    'exc_type': 'ExceptionClass',
    'exc_message': exception_args,
    'exc_module': 'module.name'
}
```
[celery/backends/base.py434-503](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L434-L503) 处的 `exception_to_python()` 方法在反序列化时带有安全检查：

-   验证异常类确实是 `BaseException` 的子类
-   防止通过恶意存储的结果执行任意代码
-   如果原始异常类不可用，则创建合成异常类

来源：[celery/backends/base.py424-503](https://github.com/celery/celery/blob/4d068b56/celery/backends/base.py#L424-L503)

## 数据库后端 (Database Backend)

位于 `celery/backends/database.py` 的数据库后端使用 SQLAlchemy 或 Django ORM 进行关系型存储：

**表结构：**

-   `celery_taskmeta` —— 任务结果
-   `celery_tasksetmeta` —— 组结果

**配置：**

-   `result_backend = 'db+sqlite:///results.db'`
-   `result_backend = 'db+postgresql://user:pass@host/db'`
-   `database_engine_options` —— SQLAlchemy 引擎选项
-   `database_short_lived_sessions` —— 会话生命周期管理
-   `database_table_names` —— 自定义表名

**自动清理：**

-   不支持 `autoexpire`
-   需要 `celery.backend_cleanup` 周期性任务
-   定义在 [celery/app/builtins.py13-23](https://github.com/celery/celery/blob/4d068b56/celery/app/builtins.py#L13-L23)

来源：[celery/app/builtins.py13-23](https://github.com/celery/celery/blob/4d068b56/celery/app/builtins.py#L13-L23)

## RPC 后端

位于 `celery/backends/rpc.py` 的 RPC 后端使用 AMQP 的 reply-to 模式：

**关键特性：**

-   无持久化存储 —— 结果通过消息代理传递
-   为每个客户端进程创建带有自动删除功能的排他性响应队列
-   通过异步消息消费支持原生 join
-   如果消费者断开连接后仍需要结果，则不适用

**消息流：**

1.  客户端创建排他性响应队列
2.  任务在消息属性中包含 `reply_to` 和 `correlation_id`
3.  工作者将结果发布到响应队列
4.  客户端从响应队列中消费匹配 `correlation_id` 的结果

**局限性：**

-   如果客户端断开连接，结果将丢失
-   无结果持久化
-   无法查询历史结果

来源：架构图展示 RPC 为 20 多个后端之一

## 测试矩阵

[tox.ini1-137](https://github.com/celery/celery/blob/4d068b56/tox.ini#L1-L137) 处的集成测试矩阵跨 Python 版本验证了各后端：

**[tox.ini6](https://github.com/celery/celery/blob/4d068b56/tox.ini#L6-L6) 处的后端测试组合：**

-   `rabbitmq_redis` —— RabbitMQ 代理 + Redis 后端
-   `rabbitmq` —— RabbitMQ + RPC 后端
-   `redis` —— Redis 代理 + Redis 后端
-   `dynamodb` —— Redis 代理 + DynamoDB 后端
-   `azureblockblob` —— Redis 代理 + Azure Blob 后端
-   `cache` —— Redis 代理 + Memcached 后端
-   `cassandra` —— Redis 代理 + Cassandra 后端
-   `elasticsearch` —— Redis 代理 + Elasticsearch 后端

**测试执行：**

-   7 个 Python 版本：3.9, 3.10, 3.11, 3.12, 3.13, 3.14, PyPy3
-   9 种后端配置
-   总计：63 种测试环境组合

来源：[tox.ini1-137](https://github.com/celery/celery/blob/4d068b56/tox.ini#L1-L137)
