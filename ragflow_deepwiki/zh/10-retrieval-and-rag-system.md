# 10 检索与 RAG 系统 (Retrieval and RAG System)

相关源文件：

- [agent/tools/retrieval.py](https://github.com/infiniflow/ragflow/blob/80a16e71/agent/tools/retrieval.py)
- [api/apps/chunk_app.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/apps/chunk_app.py)
- [api/apps/conversation_app.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/apps/conversation_app.py)
- [api/db/services/dialog_service.py](https://github.com/infiniflow/ragflow/blob/80a16e71/api/db/services/dialog_service.py)
- [rag/nlp/search.py](https://github.com/infiniflow/ragflow/blob/80a16e71/rag/nlp/search.py)
- [rag/svr/task_executor.py](https://github.com/infiniflow/ragflow/blob/80a16e71/rag/svr/task_executor.py)

检索与 RAG 系统是 RAGFlow 的核心，负责处理用户查询、从索引文档中检索相关知识切片、重排序结果，并生成带有引用的回答。该系统实现了结合向量相似度和 BM25 关键词匹配的混合搜索、复杂的重排序策略以及自动引用插入机制。

有关检索前的文档处理和索引，请参阅[文档处理流水线](/zh/6-document-processing-pipeline)。有关基于智能体的工作流，请参阅[智能体与工作流系统](/zh/9-agent-and-workflow-system)。

---

## 系统架构概览 (System Architecture Overview)

RAG 流水线执行以下阶段：
1.  **查询处理**：翻译查询、精炼多轮上下文、提取关键词。
2.  **混合搜索**：通过加权融合结合向量嵌入和 BM25 文本匹配。
3.  **重排序**：使用 Rerank 模型或混合相似度评分来优化切片优先级。
4.  **回答生成**：格式化上下文，调用 LLM 并配合系统提示词。
5.  **引用插入**：在生成的回答中嵌入参考文献。

---

## 核心流程与 API 入口 (Core Flow and Entry Points)

系统通过多个接口调用 RAG 能力：
- **OpenAI 兼容端点**：针对第三方工具集成。
- **原生 SDK / API**：针对自定义应用开发。
- **Web UI**：针对直接用户交互。

主要的执行逻辑封装在 `api/db/services/dialog_service.py` 的 `async_chat()` 方法中。

---

## 查询精炼与预处理 (Query Refinement)

在检索之前，系统会对用户查询进行多重转换：
- **多轮精炼 (Multi-turn Refinement)**：基于对话历史重写问题，使其语义完整。
- **跨语言支持 (Cross-language)**：将查询翻译为数据集支持的语言以扩大搜索范围。
- **关键词提取**：利用 LLM 提取查询中的核心术语以辅助全文检索。
- **元数据过滤**：基于预设条件（如作者、日期、标签）缩小搜索范围。

---

## 混合搜索架构 (Hybrid Search Architecture)

`rag/nlp/search.py` 中的 `Dealer` 类实现了混合搜索：
- **向量搜索**：将查询转换为嵌入向量，在 Elasticsearch 或 Infinity 中执行余弦相似度检索。
- **关键词搜索**：基于词法分析执行 BM25 关键词匹配。
- **加权融合**：通常采用 `weighted_sum` 策略（如 5% 关键词 + 95% 向量）。
- **回退策略**：若初始搜索无结果，会自动降低匹配阈值进行重试。

---

## 重排序与评分 (Reranking and Scoring)

检索到的切片会经过重排序以确保最相关的排在最前：
- **模型重排序**：调用专门的 Rerank 模型（如 Jina, Cohere, BGE）进行精细打分。
- **混合评分**：结合词法相似度、向量相似度、标签匹配度以及 PageRank 文档重要性进行综合评分。

---

## 回答生成与上下文控制 (Response Generation)

- **上下文构建**：将切片内容按顺序拼接，并严格遵守 LLM 的 Token 预算。
- **系统提示词**：注入格式化的知识块和引用规则说明。
- **流式响应**：利用 SSE 技术实时返回生成内容，并支持 `<think>` 思考块展示。

---

## 引用插入机制 (Citation Insertion)

RAGFlow 具备强大的引用处理能力：
- **自动插入**：如果模型未生成引用，系统会通过计算回答各句与切片的相似度，自动插入 `[ID:n]` 标记。
- **格式修复**：自动校正模型生成的各种非标准引用格式（如中文括号、缺失 ID 标识等）。
- **参考文献过滤**：在回答结束时，仅列出被实际引用到的文档信息。

---

## 高级检索特性 (Advanced Retrieval Features)

- **知识图谱集成**：在向量搜索的基础上并行检索关联的实体和关系子图。
- **父子切片检索**：检索到子切片时自动关联其所属的父切片，以提供更完整的背景。
- **TOC 增强**：针对带有目录结构的长文档，识别相关章节并扩展检索范围。
- **深度推理模式**：针对复杂问题启动多步规划、多重检索与反思迭代。

---

## 总结 (Summary)

检索与 RAG 系统通过多层次的精度优化和稳健的处理流水线，确保了回答的准确性和可追溯性：
- **混合搜索**：平衡了词法精确性与语义深度。
- **动态重排序**：通过先进模型确保最优质的上下文。
- **精准引用**：从底层算法级别解决了“幻觉”和来源不透明问题。
- **丰富的检索策略**：适配了从简单问答到复杂行业文档分析的多样化场景。
