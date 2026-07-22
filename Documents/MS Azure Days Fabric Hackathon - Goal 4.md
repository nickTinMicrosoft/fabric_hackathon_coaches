---
layout: page
title: Goal 4 - Build the Gold Lakehouse and Serve It
---

# Build the Gold Lakehouse and Serve It (2 hours)

Now that your data is in **Silver** and enriched with AI, build the **Gold Lakehouse** — the curated, business-ready layer — and serve it to consumers. In this goal you'll create **Materialized Lake Views**, a **Semantic Model**, and feed them into **Data Agents** and an **Ontology**.

## What to Do

- Create a **GoldLakehouse** and surface your Silver tables into it (OneLake shortcuts, zero-copy).
- Build **Materialized Lake Views (MLVs)** — pre-computed, physically stored Delta tables that Fabric refreshes in dependency order. Use a two-tier design: wide foundational marts, then thin business-question answers on top.
- Build a **Direct Lake Semantic Model** over the Gold marts so reports read live Lakehouse data with no import or refresh.
- Feed the model into a **Data Agent** for natural-language Q&A over your curated data.
- Connect entities and relationships into an **Ontology** to describe your business domain.

> **Example notebook:** See [`Notebooks/`](../Notebooks/) —
> `Gold - Business Marts (MLV)` builds four Tier-1 wide marts and six Tier-2 business-question
> answers as Materialized Lake Views, ready for a Direct Lake semantic model and Data Agents.

You can still finish by building a **Power BI report or dashboard** on top of the semantic model — the reference material below covers modeling, DAX, and reporting.

## Ideas and Suggestions

To help participants get creative, here are some simple and practical directions.

### Modeling Ideas

- Create relationships between fact and dimension tables.
- Build DAX measures (totals, averages, year-over-year growth, and so on).
- Add a semantic model to simplify the schema for reporting.
- Use Direct Lake so the dashboard reflects live Lakehouse data.

### Dashboard and Report Ideas

- Build a summary dashboard showing high-level KPIs.
- Create an AI-powered insights page using Smart Narratives.
- Use slicers to let users explore patterns by date, category, or region.
- Add visuals that highlight anomalies found by Azure AI.
- Build an Ask a Question Q&A visual so users can query the model in natural language.
- Create a Before vs After AI Enrichment comparison page.
- Build a drill-through page to dive deeper into any record or segment.

### Creative Optional Add-Ons

- Add bookmarks or buttons to create a guided storytelling experience.
- Use themes to brand your dashboard.
- Add a KPI card that uses conditional formatting (red/yellow/green).
- Build a mini Copilot-style insights page showing AI-generated summaries from enriched data.
- Add a tooltip page with deeper insights when hovering over visuals.

## Notes and References

### 1. Create the Data Model (Relationships, Facts, Dimensions)

| What to do | Learn link |
| --- | --- |
| Understand star schema (fact and dimension) | [Star schema guidance](https://learn.microsoft.com/power-bi/guidance/star-schema) |
| Create relationships in model view | [Create and manage relationships](https://learn.microsoft.com/power-bi/transform-model/desktop-create-and-manage-relationships) |
| Create a semantic model in Fabric | [Semantic models in Fabric](https://learn.microsoft.com/fabric/data-warehouse/semantic-models) |
| Use Direct Lake from Lakehouse | [Direct Lake overview](https://learn.microsoft.com/fabric/get-started/direct-lake-overview) |

### 2. Add Calculated Columns and DAX Measures

| What to do | Learn link |
| --- | --- |
| DAX basics (totals, averages, YoY, and so on) | [DAX basics quickstart](https://learn.microsoft.com/power-bi/transform-model/desktop-quickstart-learn-dax-basics) |
| Create measures | [Create measures in Power BI](https://learn.microsoft.com/power-bi/transform-model/desktop-measures) |
| Calculated columns vs measures | [Calculated columns in Power BI](https://learn.microsoft.com/power-bi/transform-model/desktop-calculated-columns) |

### 3. Build the Power BI Report or Dashboard

| Idea | Learn link |
| --- | --- |
| Create your first report | [Create reports in Power BI Desktop](https://learn.microsoft.com/power-bi/create-reports/desktop-create-reports) |
| Use slicers for exploration | [Slicers in Power BI](https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-slicers) |
| Smart Narratives (AI insights page) | [Smart narrative visual](https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-smart-narrative) |
| Q&A visual (ask questions in plain English) | [Q&A visual in Power BI](https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-q-and-a) |
| Drill-through pages | [Drill-through in reports](https://learn.microsoft.com/power-bi/create-reports/desktop-drillthrough) |
| Tooltip report pages | [Tooltips in Power BI reports](https://learn.microsoft.com/power-bi/create-reports/desktop-tooltips) |
| Bookmarks and buttons (storytelling) | [Bookmarks in Power BI](https://learn.microsoft.com/power-bi/create-reports/desktop-bookmarks) |

### 4. Suggested Storytelling Layout

| What to show | How |
| --- | --- |
| Anomalies detected | Line chart with anomaly flag |
| Sentiment and entities | Bar chart or word cloud from enriched columns |
| AI summaries | Smart narrative or text visual |
| Before vs After AI enrichment | Comparison page using the same visuals |

### 5. Direct Lake (Important for Hackathon Story)

Your report reads live from the Lakehouse. No import and no scheduled refresh.

- [Direct Lake overview](https://learn.microsoft.com/fabric/get-started/direct-lake-overview)

### 6. Optional Creative Polish

| Feature | Learn link |
| --- | --- |
| Themes and branding | [Report themes in Power BI](https://learn.microsoft.com/power-bi/create-reports/desktop-report-themes) |
| KPI cards with conditional formatting | [Card visual in Power BI](https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-card) |
| Dashboard tiles | [Create a dashboard in Power BI service](https://learn.microsoft.com/power-bi/create-reports/service-dashboard-create) |

## Expected Outcome

Participants should end with:

- A clean star schema model.
- Measures for key KPIs.
- A Direct Lake semantic model.
- A 3-5 page report showing AI insights.
- A Q&A or Smart Narrative page.
- Drill-through and tooltip pages for depth.



---

**Navigation:** [&larr; Previous: Goal 3 &mdash; AI Insights](MS%20Azure%20Days%20Fabric%20Hackathon%20-%20Goal%203.md) &middot; [Documents Home](README.md)
