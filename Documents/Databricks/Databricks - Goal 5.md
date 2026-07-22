---
layout: page
title: Databricks Goal 5
---

🤖 GOAL 5 — Add AI Agent Layer (Natural Language Data Access)
Now we make it intelligent.

🎯 What Users Are Doing
Users ask natural language questions like:
    “Show top 5 states by customers.”
The agent converts this into SQL and runs it.

❓ Why This Matters
    • No SQL knowledge required
    • Self-service analytics
    • Executive-friendly interface
    • Modern AI experience

Architecture
User → AI Agent → Generate SQL → Run in Databricks → Return Result

Example Agent (Simple PySpark + OpenAI Style)

question = "Top 5 states by customers"

prompt = f"""
You are a SQL assistant.
Generate a Databricks SQL query for this question:

Question: {question}

Table: hackathon.gold.customers_by_state
"""

# response = openai_client.chat.completions.create(...)
# sql_query = response.choices[0].message.content

sql_query = """
SELECT State, total_customers
FROM hackathon.gold.customers_by_state
ORDER BY total_customers DESC
LIMIT 5
"""

result = spark.sql(sql_query)
display(result)

Official References

Databricks AI Functions (LLM in SQL)
https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai-functions
Databricks Model Serving
https://learn.microsoft.com/en-us/azure/databricks/machine-learning/model-serving/
Vector Search (for RAG Agents)
https://learn.microsoft.com/en-us/azure/databricks/generative-ai/vector-search
Lakehouse AI Overview
https://learn.microsoft.com/en-us/azure/databricks/lakehouse-ai/


---

**Navigation:** [&larr; Previous: Goal 4 &mdash; Build Curated Tables (Silver & Gold)](Databricks%20-%20Goal%204.md) &middot; [Next: Goal 6 &mdash; Mirror to Microsoft Fabric &rarr;](Databricks%20-%20Goal%206.md)
