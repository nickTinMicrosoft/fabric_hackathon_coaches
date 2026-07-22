---
layout: page
title: Goal 3 - Use AI to Discover Intelligence in Semi-Structured Data
---

# Use AI to Discover Intelligence in Semi-Structured Data (2 hours)

In this goal, point AI at your **semi-structured content** — free-text files such as course reviews, notes, or survey responses — to gather intelligence your project can use. You'll turn unstructured text into structured, analytics-ready signals in your Silver Lakehouse.

You can approach this however you want. The goal is to add intelligence to your dataset using any Azure AI or Fabric AI capability.

## What to Do

- Read your raw semi-structured files (for example, JSON/Parquet review text landed in Bronze).
- Use AI to **derive signals** from the text — sentiment, summaries, classifications, topic themes, or entities.
- Consider **privacy**: use an LLM to anonymize or de-identify free text before you persist it.
- Write the AI-derived signals back to a **Silver** table so downstream goals (modeling, reporting, Data Agents) can use them.

## Two AI Paths (both shown in the example notebooks)

- **Built-in Fabric AI functions** — `ai.analyze_sentiment`, `ai.summarize`, `ai.classify`, `ai.extract` run directly in a notebook with no API key.
- **Azure AI Foundry** — call a deployed chat model (for example, to anonymize/rewrite text) using an endpoint and key managed by a Fabric Variable Library.

> **Example notebooks:** See [`Notebooks/`](../Notebooks/) —
> `4 - Analyze CR with Built-in AI` (Fabric AI functions over review text) and
> `3 - Anonymize Course reviews with Foundry AI` (Azure AI Foundry de-identification).

## Hackathon Note

You can do this entirely in Fabric or call Azure AI services directly. Both are valid. Fabric is faster to start, while Azure AI gives more control.

## Reference Paths

### 1. Natural-Language Q&A Over Your Data (Data Agent / Chat with Data)

| Option | What to use | Learn link |
| --- | --- | --- |
| Fabric | Data Agent on Lakehouse/Warehouse | [How to create a Data Agent](https://learn.microsoft.com/fabric/data-science/how-to-create-data-agent) |
| Azure AI | RAG with embeddings and chat using Azure OpenAI Service | [Use your data with Azure OpenAI](https://learn.microsoft.com/azure/ai-services/openai/use-your-data) |

### 2. Summarize, Classify, Sentiment, and Entities (Text Enrichment)

| Option | What to use | Learn link |
| --- | --- | --- |
| Fabric | AI Functions in notebooks / Prompt Flow | [AI Functions overview](https://learn.microsoft.com/fabric/data-science/ai-functions/overview) |
| Azure AI | Azure AI Language (Text Analytics) | [Azure AI Language overview](https://learn.microsoft.com/azure/ai-services/language-service/overview) |

### 3. Embeddings and Similarity Search

| Option | What to use | Learn link |
| --- | --- | --- |
| Fabric | AI Functions and vector index in Lakehouse | [AI Functions overview](https://learn.microsoft.com/fabric/data-science/ai-functions/overview) |
| Azure AI | Embeddings with Azure OpenAI | [Generate embeddings](https://learn.microsoft.com/azure/ai-services/openai/how-to/embeddings) |

### 4. Build a Prediction Model (AutoML)

| Option | What to use | Learn link |
| --- | --- | --- |
| Fabric | AutoML experiment on Lakehouse tables | [AutoML overview in Fabric](https://learn.microsoft.com/fabric/data-science/automl-overview) |
| Azure AI | AutoML in Azure ML | [AutoML in Azure Machine Learning](https://learn.microsoft.com/azure/machine-learning/automl/overview) |

### 5. Detect Anomalies in Time-Series

| Option | What to use | Learn link |
| --- | --- | --- |
| Fabric | Notebook with Python/Spark anomaly logic | [How to use notebooks in Fabric](https://learn.microsoft.com/fabric/data-engineering/how-to-use-notebook) |
| Azure AI | Azure AI Anomaly Detector | [Anomaly Detector overview](https://learn.microsoft.com/azure/ai-services/anomaly-detector/overview) |

### 6. Enrich and Normalize Messy Text Fields with LLMs

| Option | What to use | Learn link |
| --- | --- | --- |
| Fabric | Prompt Flow / AI Functions | [AI Functions overview](https://learn.microsoft.com/fabric/data-science/ai-functions/overview) |
| Azure AI | Azure OpenAI chat/completions | [How to work with chat models](https://learn.microsoft.com/azure/ai-services/openai/how-to/chatgpt) |

### 7. Agentic Extension (Advanced / Bonus)

| Option | What to use | Learn link |
| --- | --- | --- |
| Fabric | Data Agent as your data tool | [Data Agent concepts](https://learn.microsoft.com/fabric/data-science/concept-data-agent) |
| Azure AI | Connect to Azure AI Foundry for orchestration | [Use Microsoft Fabric data agent in Azure AI Foundry](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric) |


---

**Navigation:** [&larr; Previous: Goal 2 &mdash; Silver Lakehouse](MS%20Azure%20Days%20Fabric%20Hackathon%20-%20Goal%202.md) &middot; [Next: Goal 4 &mdash; Gold Lakehouse &rarr;](MS%20Azure%20Days%20Fabric%20Hackathon%20-%20Goal%204.md)
