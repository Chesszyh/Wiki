# Distributed Execution

Relevant source files

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

This document describes vLLM's distributed execution capabilities, covering parallelism strategies (Tensor, Pipeline, Data, Expert, Context), communication infrastructure, and multi-process engine management. For model loading and weight distribution, see [Build System and Deployment](/vllm-project/vllm/11-build-system-and-deployment). For attention-specific distributed features like disaggregated serving, see [Attention Backends](/vllm-project/vllm/8-attention-backends).

---

## Parallelism Strategies Overview

vLLM supports five primary parallelism strategies that can be combined to scale inference across multiple GPUs and nodes. These are configured via the `ParallelConfig` object.

| Strategy | Abbreviation | Purpose | Configuration | Typical Use Case |
| --- | --- | --- | --- | --- |
| **Tensor Parallelism** | TP | Shard model weights across GPUs | `tensor_parallel_size` | Models too large for single GPU |
| **Pipeline Parallelism** | PP | Distribute layers across GPUs | `pipeline_parallel_size` | Very deep models, reduce memory per GPU |
| **Data Parallelism** | DP | Replicate model across instances | `data_parallel_size` | Increase throughput with independent batches |
| **Expert Parallelism** | EP | Distribute MoE experts | `tensor_parallel_size` × `data_parallel_size` | Mixture-of-Experts models |
| **Context Parallelism** | CP | Split long sequences | `prefill_context_parallel_size`, `decode_context_parallel_size` | Long context windows |

The total world size is generally `TP × PP × DP`. Expert parallelism degree is calculated as the product of TP and DP sizes for expert sharding [vllm/config/parallel.py101-107](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L101-L107)

For details, see [Parallelism Strategies](/vllm-project/vllm/9.1-parallelism-strategies).

**Sources:** [vllm/config/parallel.py99-172](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L99-L172) [vllm/v1/engine/core.py137-142](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core.py#L137-L142)

---

## Configuration and Initialization

### ParallelConfig Structure

The `ParallelConfig` class encapsulates all distributed execution settings. It manages worker counts, rank assignments, and backend selection for data and model parallelism.

Title: ParallelConfig Attributes

**Sources:** [vllm/config/parallel.py99-172](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L99-L172)

---

## Distributed Communication Infrastructure

vLLM utilizes platform-specific communication backends (NCCL for NVIDIA/AMD, XCCL for Intel, Gloo for CPU) to perform collective operations like `all_reduce`, `all_gather`, and `reduce_scatter`.

### Communication Backend Selection

The system initializes the distributed environment through `init_distributed_environment` and creates specialized process groups for each parallelism dimension (TP, PP, DP) [vllm/distributed/parallel\_state.py8-24](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/parallel_state.py#L8-L24)

Title: Distributed Group Management

For details, see [Communication Infrastructure](/vllm-project/vllm/9.2-communication-infrastructure).

**Sources:** [vllm/distributed/parallel\_state.py126-170](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/distributed/parallel_state.py#L126-L170) [vllm/v1/engine/llm\_engine.py82-89](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/llm_engine.py#L82-L89)

---

## Multi-Process Engine Management

In vLLM V1, the engine can run in a decoupled multi-process mode where the `EngineCore` resides in a separate background process from the front-end `AsyncLLM` or `LLM` client.

### Engine and Client Interaction

The `EngineCoreClient` manages the lifecycle of `EngineCore` processes. It uses ZMQ for inter-process communication (IPC) to send `EngineCoreRequest` objects and receive `EngineCoreOutputs` [vllm/v1/engine/core\_client.py35-44](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core_client.py#L35-L44)

Title: Decoupled Engine Architecture

### Data Parallel Load Balancing

When `data_parallel_size > 1`, vLLM can use internal or external load balancing. `DPLBAsyncMPClient` implements an internal round-robin or sticky routing (for late interaction models) load balancer across multiple DP engine ranks [vllm/v1/engine/core\_client.py124-130](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core_client.py#L124-L130)

For details, see [Multi-Process Engine Management](/vllm-project/vllm/9.3-multi-process-engine-management).

**Sources:** [vllm/v1/engine/core\_client.py69-130](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core_client.py#L69-L130) [vllm/v1/engine/utils.py82-110](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/utils.py#L82-L110) [vllm/v1/engine/llm\_engine.py111-118](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/llm_engine.py#L111-L118)

---

## KV Cache Transfer and Disaggregated Serving

vLLM supports disaggregated serving (prefill-decode separation) by transferring KV cache blocks between different engine instances.

### KVConnector and Handshake

The `EngineCore` initializes KV caches and, if a `KVConnector` is present, collects handshake metadata from all workers to facilitate network transfers [vllm/v1/engine/core.py163-180](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core.py#L163-L180) This allows a "prefill" rank to send computed KV blocks to a "decode" rank.

For details, see [KV Cache Transfer and Disaggregated Serving](/vllm-project/vllm/9.4-kv-cache-transfer-and-disaggregated-serving).

**Sources:** [vllm/v1/engine/core.py163-180](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core.py#L163-L180) [vllm/v1/kv\_cache\_interface.py1](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/kv_cache_interface.py#L1-L1)

---

## Expert Parallelism (EP)

For Mixture-of-Experts (MoE) models, vLLM supports Expert Parallelism, which shards experts across DP and TP ranks.

### EP Load Balancing (EPLB)

The `EPLBConfig` governs how experts are rearranged to balance computational load. Strategies include `linear` and `round_robin` placement [vllm/config/parallel.py53-94](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L53-L94) MoE layers use specialized backends like `deepep` or `flashinfer` for `all2all` communication during expert routing [vllm/config/parallel.py38-50](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L38-L50)

**Sources:** [vllm/config/parallel.py153-172](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/config/parallel.py#L153-L172) [vllm/v1/engine/core.py137-142](https://github.com/vllm-project/vllm/blob/7cc302dd/vllm/v1/engine/core.py#L137-L142)
