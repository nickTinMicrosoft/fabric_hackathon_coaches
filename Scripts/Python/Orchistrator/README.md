# Orchestrator — Fabric Agents + RAG

This app coordinates multiple Fabric AI agents and Azure AI Search to answer complex, cross-domain operational questions using Azure OpenAI.

---

## How It Works

1. **Calls Fabric Agents** — Sends the user's question to Hospital, Train, and DevOps agents in parallel
2. **Queries Azure AI Search** — Retrieves relevant playbook/knowledge documents (RAG)
3. **Builds a prompt** — Combines agent responses and search results into a structured prompt
4. **Generates an answer** — Sends the prompt to Azure OpenAI for a final, actionable response

```
User Question → Fabric Agents (Hospital, Train, DevOps)
             → Azure AI Search (RAG)
             → Azure OpenAI → Final Answer
```

---

## Setup

1. Install dependencies:
   ```bash
   pip install openai azure-search-documents python-dotenv requests
   ```

2. Ensure the following are set in the `.env` file at the project root:
   ```
   # Azure OpenAI
   AZURE_OPENAI_API_KEY=<your-key>
   AZURE_OPENAI_ENDPOINT=<your-endpoint>
   AZURE_OPENAI_API_VERSION=2024-02-01
   AZURE_OPENAI_CHAT_MODEL=gpt-4o-mini

   # Azure AI Search
   AZURE_SEARCH_ENDPOINT=<your-search-endpoint>
   AZURE_SEARCH_KEY=<your-search-key>
   AZURE_SEARCH_INDEX_NAME=city-ops-index

   # Fabric Agent Endpoints (update when available)
   HOSPITAL_AGENT_ENDPOINT=<endpoint>
   HOSPITAL_AGENT_KEY=<key>
   TRAIN_AGENT_ENDPOINT=<endpoint>
   TRAIN_AGENT_KEY=<key>
   DEVOPS_AGENT_ENDPOINT=<endpoint>
   DEVOPS_AGENT_KEY=<key>
   ```

## Usage

```bash
python main.py
```

The demo asks: _"Region A has delays and rising hospital load. What should we do?"_ and prints agent signals followed by the AI-generated response.

---

## Architecture

| Component | Purpose |
|-----------|---------|
| Azure OpenAI | Final LLM reasoning and response generation |
| Azure AI Search | RAG — retrieves playbook and incident knowledge |
| Fabric Agents | Domain-specific real-time data (hospital, train, devops) |

---

[← Back to Python README](../README.md)
