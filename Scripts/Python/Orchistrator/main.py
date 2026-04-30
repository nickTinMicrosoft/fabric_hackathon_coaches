# ================================
# ORCHESTRATOR: FABRIC AGENTS + RAG
# ================================

import os
import requests
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))

# ================================
# CONFIG
# ================================

# ---- Azure OpenAI ----
aoai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)
CHAT_MODEL = os.getenv("AZURE_OPENAI_CHAT_MODEL", "gpt-4o-mini")

# ---- Azure AI Search ----
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY")),
)

# ---- Fabric Agent Endpoints ----
AGENTS = {
    "hospital": {
        "endpoint": os.getenv("HOSPITAL_AGENT_ENDPOINT"),
        "api_key": os.getenv("HOSPITAL_AGENT_KEY"),
    },
    "train": {
        "endpoint": os.getenv("TRAIN_AGENT_ENDPOINT"),
        "api_key": os.getenv("TRAIN_AGENT_KEY"),
    },
    "devops": {
        "endpoint": os.getenv("DEVOPS_AGENT_ENDPOINT"),
        "api_key": os.getenv("DEVOPS_AGENT_KEY"),
    },
}

# ================================
# AGENT CALLER
# ================================

def call_fabric_agent(agent_name, question):
    agent = AGENTS[agent_name]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {agent['api_key']}"
    }

    payload = {
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(
            agent["endpoint"],
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()

        data = response.json()

        # Adjust based on actual Fabric response shape
        return data.get("response", str(data))

    except Exception as e:
        return f"{agent_name} agent error: {str(e)}"


# ================================
# PARALLEL AGENT EXECUTION
# ================================

def get_agent_data(question):
    return {
        "hospital": call_fabric_agent("hospital", question),
        "train": call_fabric_agent("train", question),
        "devops": call_fabric_agent("devops", question)
    }


# ================================
# AI SEARCH (RAG)
# ================================

def query_ai_search(query_text):
    results = search_client.search(
        search_text=query_text,
        top=3
    )

    docs = []
    for r in results:
        docs.append(r["content"])

    return "\n\n".join(docs)


# ================================
# BUILD PROMPT
# ================================

def build_prompt(question, agent_data, rag_context):

    return f"""
You are a real-time operations advisor.

USER QUESTION:
{question}

AGENT SIGNALS:

HOSPITAL:
{agent_data['hospital']}

TRAIN:
{agent_data['train']}

DEVOPS:
{agent_data['devops']}

PLAYBOOK / KNOWLEDGE:
{rag_context}

TASK:
1. Explain the current situation
2. Identify cross-domain risks
3. Recommend specific actions
4. Highlight system risks (latency, failures)

Keep response concise, structured, and actionable.
"""


# ================================
# LLM CALL
# ================================

def call_llm(prompt):
    response = aoai_client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert city operations AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# ================================
# MAIN ORCHESTRATOR
# ================================

def run_orchestrator(question):

    # 1. Call all Fabric agents
    agent_data = get_agent_data(question)

    # 2. Build smarter RAG query
    search_query = "hospital overload response train delay API latency incident playbook"

    # 3. Retrieve knowledge
    rag_context = query_ai_search(search_query)

    # 4. Build prompt
    prompt = build_prompt(question, agent_data, rag_context)

    # 5. Generate answer
    answer = call_llm(prompt)

    return {
        "agent_data": agent_data,
        "answer": answer
    }


# ================================
# RUN DEMO
# ================================

if __name__ == "__main__":

    question = "Region A has delays and rising hospital load. What should we do?"

    result = run_orchestrator(question)

    print("\n=== AGENT DATA ===")
    for k, v in result["agent_data"].items():
        print(f"\n{k.upper()}:\n{v}")

    print("\n=== FINAL ANSWER ===\n")
    print(result["answer"])