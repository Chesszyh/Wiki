# Prebuilt Components

Relevant source files

-   [libs/langgraph/langgraph/graph/\_\_init\_\_.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/langgraph/langgraph/graph/__init__.py)
-   [libs/prebuilt/langgraph/prebuilt/\_\_init\_\_.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/__init__.py)
-   [libs/prebuilt/langgraph/prebuilt/chat\_agent\_executor.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py)
-   [libs/prebuilt/langgraph/prebuilt/tool\_node.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_node.py)
-   [libs/prebuilt/langgraph/prebuilt/tool\_validator.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_validator.py)
-   [libs/prebuilt/tests/test\_deprecation.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/tests/test_deprecation.py)
-   [libs/prebuilt/tests/test\_on\_tool\_call.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/tests/test_on_tool_call.py)
-   [libs/prebuilt/tests/test\_react\_agent.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/tests/test_react_agent.py)
-   [libs/prebuilt/tests/test\_tool\_node.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/tests/test_tool_node.py)
-   [libs/prebuilt/tests/test\_tool\_node\_interceptor\_unregistered.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/tests/test_tool_node_interceptor_unregistered.py)
-   [libs/prebuilt/tests/test\_tool\_node\_validation\_error\_filtering.py](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/tests/test_tool_node_validation_error_filtering.py)

Prebuilt components provide high-level abstractions for common LangGraph patterns, primarily focusing on tool-using agents and tool execution infrastructure. These components abstract away graph construction details while remaining fully customizable through parameters and hooks.

For low-level graph construction APIs, see [StateGraph API](/langchain-ai/langgraph/3.1-stategraph-api) and [Functional API (@task and @entrypoint)](/langchain-ai/langgraph/3.2-functional-api-(@task-and-@entrypoint)). For deployment of prebuilt agents, see [CLI and Deployment](/langchain-ai/langgraph/6-cli-and-deployment).

**Sources:** [libs/prebuilt/langgraph/prebuilt/\_\_init\_\_.py1-22](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/__init__.py#L1-L22)

## Overview

The prebuilt components module exports the following components from [libs/prebuilt/langgraph/prebuilt/\_\_init\_\_.py1-22](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/__init__.py#L1-L22):

| Component | Status | Purpose |
| --- | --- | --- |
| `ToolNode` | Active | Execute tool calls with parallel execution, error handling, and injection |
| `tools_condition` | Active | Conditional routing based on tool call presence |
| `InjectedState` | Active | Annotation for injecting graph state into tools |
| `InjectedStore` | Active | Annotation for injecting `BaseStore` into tools |
| `ToolRuntime` | Active | Bundle of runtime context for tools |
| `create_react_agent` | **Deprecated** | Build ReAct agents — use `langchain.agents.create_agent` instead |
| `ValidationNode` | **Deprecated** | Validate tool calls against schemas — use `create_agent` with custom error handling |

> **Migration note:** `create_react_agent` and several related types (`AgentState`, `AgentStatePydantic`, `AgentStateWithStructuredResponse`) were moved to the `langchain` package as of `LangGraphDeprecatedSinceV10`. See the [Deprecated Components](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/Deprecated Components) section for details.

Sources: [libs/prebuilt/langgraph/prebuilt/\_\_init\_\_.py1-22](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/__init__.py#L1-L22) [libs/prebuilt/langgraph/prebuilt/chat\_agent\_executor.py53-116](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py#L53-L116) [libs/prebuilt/langgraph/prebuilt/tool\_validator.py43-47](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_validator.py#L43-L47)

## Architecture: Prebuilt Components in Execution Pipeline

The following diagram bridges the gap between the high-level prebuilt abstractions and the underlying graph execution engine.

```mermaid
flowchart TD
    User["User Code"]
    CreateReactAgent["create_react_agent()"]
    ToolNode["ToolNode"]
    ToolsCondition["tools_condition()"]
    InjectedTypes["InjectedStateInjectedStoreToolRuntime"]
    StateGraph["StateGraph"]
    AddNode["add_node()"]
    AddEdge["add_edge()"]
    Compile["compile()"]
    Pregel["Pregel"]
    PregelLoop["_loop.py"]
    ToolRuntimeObj["ToolRuntime (dataclass)"]

    User --> CreateReactAgent
    User --> ToolNode
    User --> ToolsCondition
    User --> InjectedTypes
    CreateReactAgent --> StateGraph
    StateGraph --> AddNode
    StateGraph --> AddEdge
    AddNode --> ToolNode
    StateGraph --> Compile
    Compile --> Pregel
    ToolNode --> PregelLoop
    ToolsCondition --> PregelLoop
    InjectedTypes --> ToolRuntimeObj
```
**Sources:** [libs/prebuilt/langgraph/prebuilt/chat\_agent\_executor.py1-116](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py#L1-L116) [libs/prebuilt/langgraph/prebuilt/tool\_node.py1-1834](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_node.py#L1-L1834) [libs/prebuilt/langgraph/prebuilt/tool\_node.py1691-1710](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_node.py#L1691-L1710)

## create\_react\_agent Function

> **Deprecated since `LangGraphDeprecatedSinceV10`.** Use [`create_agent`](https://docs.langchain.com/oss/python/migrate/langgraph-v1) from `langchain.agents` instead. The function remains available for backwards compatibility but will be removed in a future version.

The `create_react_agent` function constructs a `CompiledStateGraph` that implements the ReAct (Reasoning and Acting) pattern. It creates a graph with an agent node that calls an LLM and a tools node that executes tool calls.

For details, see [ReAct Agent (create\_react\_agent)](/langchain-ai/langgraph/8.1-react-agent-(create_react_agent)).

### Graph Structure

The compiled graph differs based on the `version` parameter. In v1, a single `ToolNode` receives all tool calls. In v2 (default), each individual tool call is dispatched to a separate node instance using the `Send` API (`ToolCallWithContext`), enabling parallel execution and correct pause/resume semantics.

**`create_react_agent` v2 graph topology**

```mermaid
flowchart TD
    START["START"]
    pre_model_hook["pre_model_hook"]
    agent["agent(call_model)"]
    post_model_hook["post_model_hook"]
    tools["tools(ToolNode per Send)"]
    generate_structured_response["generate_structured_response"]
    END["END"]

    START --> agent
    agent --> tools
    tools --> agent
    agent --> END
```
Sources: [libs/prebuilt/langgraph/prebuilt/chat\_agent\_executor.py843-853](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py#L843-L853) [libs/prebuilt/langgraph/prebuilt/tool\_node.py282-303](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_node.py#L282-L303)

## ToolNode Class

`ToolNode` is a `RunnableCallable` that executes tool calls from language model outputs. It handles parallel execution, error handling, state injection, and control flow.

For details, see [ToolNode and Tool Execution](/langchain-ai/langgraph/8.2-toolnode-and-tool-execution).

### Tool Execution Pipeline

`ToolNode` processes inputs (either as graph state or direct tool call lists) through a parallelized execution loop.

```mermaid
flowchart TD
    Input["Input (dict/list)"]
    _parse_input["_parse_input()"]
    _run_one["_run_one()"]
    interceptor["wrap_tool_call()"]
    _execute_one["_execute_one_tool_call()"]
    _inject["_inject_tool_args()"]
    invoke["BaseTool.invoke()"]
    _combine["_combine_tool_outputs()"]
    Output["ToolMessage / Command"]

    Input --> _parse_input
    _parse --> input__run_one
    _run --> one_interceptor
    interceptor --> _execute_one
    _execute --> one__inject
    _inject --> invoke
    invoke --> _combine
    _combine --> Output
```
Sources: [libs/prebuilt/langgraph/prebuilt/tool\_node.py786-847](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_node.py#L786-L847) [libs/prebuilt/langgraph/prebuilt/tool\_node.py1029-1163](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_node.py#L1029-L1163)

## Dependency Injection System

`ToolNode` provides three injection annotations that allow tools to receive system-provided values without the LLM needing to supply them. These are identified at initialization time by `_get_all_injected_args()`.

| Annotation | Code Entity | Purpose |
| --- | --- | --- |
| `InjectedState` | `langgraph.prebuilt.InjectedState` | Inject specific fields or the entire graph state into a tool parameter |
| `InjectedStore` | `langgraph.prebuilt.InjectedStore` | Inject the `BaseStore` instance for cross-thread persistent storage |
| `ToolRuntime` | `langgraph.prebuilt.ToolRuntime` | Inject a bundle containing `state`, `config`, `store`, and `stream_writer` |

Sources: [libs/prebuilt/langgraph/prebuilt/tool\_node.py1495-1601](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_node.py#L1495-L1601) [libs/prebuilt/langgraph/prebuilt/tool\_node.py1604-1688](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_node.py#L1604-L1688) [libs/prebuilt/langgraph/prebuilt/tool\_node.py1691-1834](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_node.py#L1691-L1834)

## UI Integration

LangGraph provides specialized message types and functions for integrating graph state with user interfaces, allowing for transient UI updates that don't necessarily persist in the core message history.

For details, see [UI Integration](/langchain-ai/langgraph/8.3-ui-integration).

Sources: [libs/prebuilt/langgraph/prebuilt/tool\_node.py63-70](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_node.py#L63-L70)

## Deprecated Components

Several components in this module are deprecated as of `LangGraphDeprecatedSinceV10` and will be removed in a future major version.

### create\_react\_agent

Deprecated in favor of `create_agent` from `langchain.agents`. The underlying graph construction logic and `ToolNode` integration remain in this package for compatibility.

Sources: [libs/prebuilt/langgraph/prebuilt/chat\_agent\_executor.py274-278](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py#L274-L278)

### AgentState / AgentStatePydantic

The default state schemas used by `create_react_agent` define `messages` (with `add_messages` reducer) and `remaining_steps` fields. Both moved to `langchain.agents`.

Sources: [libs/prebuilt/langgraph/prebuilt/chat\_agent\_executor.py53-116](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py#L53-L116)

### ValidationNode

`ValidationNode` validated tool calls against Pydantic schemas without executing them. Deprecated in favor of using `create_agent` with custom tool error handling.

Sources: [libs/prebuilt/langgraph/prebuilt/tool\_validator.py43-114](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/langgraph/prebuilt/tool_validator.py#L43-L114)

## Testing Utilities

Test files demonstrate common patterns for using prebuilt components outside graph context, specifically requiring a mock `Runtime` to be provided in the `RunnableConfig`.

```
def _create_mock_runtime(store: BaseStore | None = None) -> Mock:    mock_runtime = Mock()    mock_runtime.store = store    mock_runtime.context = None    mock_runtime.stream_writer = lambda *args, **kwargs: None    return mock_runtime def _create_config_with_runtime(store: BaseStore | None = None) -> RunnableConfig:    return {"configurable": {"__pregel_runtime": _create_mock_runtime(store)}}
```
**Sources:** [libs/prebuilt/tests/test\_react\_agent.py67-87](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/tests/test_react_agent.py#L67-L87) [libs/prebuilt/tests/test\_tool\_node.py55-75](https://github.com/langchain-ai/langgraph/blob/1fd51e8f/libs/prebuilt/tests/test_tool_node.py#L55-L75)
