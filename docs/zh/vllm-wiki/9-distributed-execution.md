# 分布式执行

相关源文件

-   [docs/design/moe\_kernel\_features.md](https://github.com/vllm-project/vllm/blob/7cc302dd/docs/design/moe_kernel_features.md?plain=1)
-   [tests/entrypoints/test\_api\_server\_process\_manager.py](https://github.com/vllm-project/vllm/blob/7cc302dd/tests/entrypoints/test_api_server_process_manager.py)
-   [tests/kernels/moe/modular\_kernel\_tools/mk\_objects.py](https://github.com/vllm-project/vllm/blob/7cc302dd/tests/kernels/moe/modular_kernel_tools/mk_objects.py)
-   [tests/v1/engine/test\_engine\_core.py](https://github.com/vllm-project/vllm/blob/7cc302dd/tests/v1/engine/test_engine_core.py)
-   [tests/v1/engine/test\_engine\_core\_client.py](https://github.com/vllm-project/vllm/blob/7cc302dd/tests/v1/engine/test_engine_core_client.py)
-   [vllm/config/parallel.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py)
-   [vllm/distributed/device\_communicators/all2all.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/device_communicators/all2all.py)
-   [vllm/distributed/device\_communicators/base\_device\_communicator.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/device_communicators/base_device_communicator.py)
-   [vllm/distributed/device\_communicators/cuda\_communicator.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/device_communicators/cuda_communicator.py)
-   [vllm/distributed/device\_communicators/pynccl.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/device_communicators/pynccl.py)
-   [vllm/distributed/elastic\_ep/elastic\_execute.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/elastic_ep/elastic_execute.py)
-   [vllm/distributed/elastic\_ep/elastic\_state.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/elastic_ep/elastic_state.py)
-   [vllm/distributed/parallel\_state.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/parallel_state.py)
-   [vllm/distributed/utils.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/utils.py)
-   [vllm/engine/async\_llm\_engine.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/engine/async_llm_engine.py)
-   [vllm/engine/llm\_engine.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/engine/llm_engine.py)
-   [vllm/engine/protocol.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/engine/protocol.py)
-   [vllm/entrypoints/cli/serve.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/entrypoints/cli/serve.py)
-   [vllm/entrypoints/launcher.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/entrypoints/launcher.py)
-   [vllm/entrypoints/llm.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/entrypoints/llm.py)
-   [vllm/model\_executor/layers/fused\_moe/all2all\_utils.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/model_executor/layers/fused_moe/all2all_utils.py)
-   [vllm/model\_executor/layers/fused\_moe/fused\_marlin\_moe.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/model_executor/layers/fused_moe/fused_marlin_moe.py)
-   [vllm/v1/engine/async\_llm.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/async_llm.py)
-   [vllm/v1/engine/coordinator.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/coordinator.py)
-   [vllm/v1/engine/core.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core.py)
-   [vllm/v1/engine/core\_client.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core_client.py)
-   [vllm/v1/engine/llm\_engine.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/llm_engine.py)
-   [vllm/v1/engine/utils.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/utils.py)
-   [vllm/v1/utils.py](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/utils.py)

本文档介绍了 vLLM 的分布式执行能力，涵盖并行策略（张量、流水线、数据、专家、上下文）、通信基础设施以及多进程引擎管理。关于模型加载和权重分发，请参见 [构建系统与部署](/vllm-project/vllm/11-build-system-and-deployment)。关于注意力相关的分布式特性，如解耦式服务，请参见 [注意力后端](/vllm-project/vllm/8-attention-backends)。

---

## 并行策略概览

vLLM 支持五种主要并行策略，可组合使用以在多 GPU 和多节点上扩展推理。这些策略通过 `ParallelConfig` 对象进行配置。

| 策略 | 缩写 | 目的 | 配置 | 典型使用场景 |
| --- | --- | --- | --- | --- |
| **张量并行** | TP | 在 GPU 之间分片模型权重 | `tensor_parallel_size` | 模型大到单个 GPU 无法容纳 |
| **流水线并行** | PP | 在 GPU 之间分发层 | `pipeline_parallel_size` | 非常深的模型，降低每个 GPU 的内存占用 |
| **数据并行** | DP | 在多个实例之间复制模型 | `data_parallel_size` | 使用独立批次提升吞吐量 |
| **专家并行** | EP | 分发 MoE 专家 | `tensor_parallel_size` × `data_parallel_size` | 混合专家（MoE）模型 |
| **上下文并行** | CP | 拆分长序列 | `prefill_context_parallel_size`, `decode_context_parallel_size` | 长上下文窗口 |

总 world size 通常为 `TP × PP × DP`。专家并行度则按 TP 和 DP 大小的乘积计算，用于专家分片 [vllm/config/parallel.py101-107](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L101-L107)

详情请参见 [并行策略](/vllm-project/vllm/9.1-parallelism-strategies)。

**来源：** [vllm/config/parallel.py99-172](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L99-L172) [vllm/v1/engine/core.py137-142](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core.py#L137-L142)

---

## 配置与初始化

### ParallelConfig 结构

`ParallelConfig` 类封装了所有分布式执行设置。它管理 worker 数量、rank 分配以及数据并行和模型并行的后端选择。

标题：ParallelConfig 属性

**来源：** [vllm/config/parallel.py99-172](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L99-L172)

---

## 分布式通信基础设施

vLLM 使用特定于平台的通信后端（NCCL 用于 NVIDIA/AMD，XCCL 用于 Intel，Gloo 用于 CPU）来执行诸如 `all_reduce`、`all_gather` 和 `reduce_scatter` 之类的集合操作。

### 通信后端选择

系统通过 `init_distributed_environment` 初始化分布式环境，并为每个并行维度（TP、PP、DP）创建专用进程组 [vllm/distributed/parallel_state.py8-24](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/parallel_state.py#L8-L24)

标题：分布式组管理

详情请参见 [通信基础设施](/vllm-project/vllm/9.2-communication-infrastructure)。

**来源：** [vllm/distributed/parallel_state.py126-170](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/parallel_state.py#L126-L170) [vllm/v1/engine/llm_engine.py82-89](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/llm_engine.py#L82-L89)

---

## 多进程引擎管理

在 vLLM V1 中，engine 可以以解耦的多进程模式运行，其中 `EngineCore` 位于与前端 `AsyncLLM` 或 `LLM` 客户端分离的后台进程中。

### 引擎与客户端交互

`EngineCoreClient` 管理 `EngineCore` 进程的生命周期。它使用 ZMQ 进行进程间通信（IPC），发送 `EngineCoreRequest` 对象并接收 `EngineCoreOutputs` [vllm/v1/engine/core_client.py35-44](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core_client.py#L35-L44)

标题：解耦式引擎架构

### 数据并行负载均衡

当 `data_parallel_size > 1` 时，vLLM 可以使用内部或外部负载均衡。`DPLBAsyncMPClient` 在多个 DP 引擎 rank 之间实现内部负载均衡，支持轮询或粘性路由（用于延迟交互模型）[vllm/v1/engine/core_client.py124-130](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core_client.py#L124-L130)

详情请参见 [多进程引擎管理](/vllm-project/vllm/9.3-multi-process-engine-management)。

**来源：** [vllm/v1/engine/core_client.py69-130](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core_client.py#L69-L130) [vllm/v1/engine/utils.py82-110](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/utils.py#L82-L110) [vllm/v1/engine/llm_engine.py111-118](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/llm_engine.py#L111-L118)

---

## KV 缓存传输与解耦式服务

vLLM 通过在不同引擎实例之间传输 KV 缓存块来支持解耦式服务（prefill-decode 分离）。

### KVConnector 与握手

`EngineCore` 初始化 KV 缓存，并且如果存在 `KVConnector`，则会从所有 worker 收集握手元数据，以便进行网络传输 [vllm/v1/engine/core.py163-180](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core.py#L163-L180)。这使得“prefill” rank 可以将已计算的 KV 块发送给“decode” rank。

详情请参见 [KV 缓存传输与解耦式服务](/vllm-project/vllm/9.4-kv-cache-transfer-and-disaggregated-serving)。

**来源：** [vllm/v1/engine/core.py163-180](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core.py#L163-L180) [vllm/v1/kv\_cache\_interface.py1](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/kv_cache_interface.py#L1-L1)

---

## 专家并行（EP）

对于混合专家（MoE）模型，vLLM 支持专家并行，它会在 DP 和 TP rank 之间对专家进行分片。

### EP 负载均衡（EPLB）

`EPLBConfig` 决定如何重新排列专家以平衡计算负载。策略包括 `linear` 和 `round_robin` 放置方式 [vllm/config/parallel.py53-94](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L53-L94)。MoE 层在专家路由期间使用 `deepep` 或 `flashinfer` 等专用后端进行 `all2all` 通信 [vllm/config/parallel.py38-50](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L38-L50)

**来源：** [vllm/config/parallel.py153-172](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L153-L172) [vllm/v1/engine/core.py137-142](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core.py#L137-L142)
