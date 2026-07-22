# Coach Notebooks (Answer Keys)

These are the **full solution notebooks** for coaches — the completed answers behind the attendee
guides. Do **not** hand these to attendees; use them to guide and unblock participants.

The attendee-facing copies live in the
[`fabric_hackathon_attendee`](https://github.com/nickTinMicrosoft/fabric_hackathon_attendee) repo
under `Notebooks/`. All notebooks resolve workspace items by name at runtime (no tenant GUIDs).

## Silver — Transform (Goal 2)

| Notebook | What it does |
| --- | --- |
| `1 - Normalize SIS to Silver Lakehouse.ipynb` | Reads the Bronze SIS mirror (Azure SQL → OneLake), conforms 11 tables to `snake_case`, enforces primary keys, and writes managed Delta dims/facts to `SilverLakehouse` (`dbo`). |
| `2 - Transform Grad Exams to Silver Lakehouse.ipynb` | **Answer key.** Full PySpark solution: reads the Bronze Graduate Exams mirror (Cosmos), normalizes `undergradContext`, explodes `relevantCourses[]`, and writes `dbo.grad_exam_result` and `dbo.grad_exam_relevant_course`. |
| `2 - Transform Grad Exams to Silver Lakehouse (COPILOT BUILD).ipynb` | **Attendee version.** The Copilot-guided discovery notebook attendees actually use — step-by-step prompts (+ ✅ Verify checks) and empty code cells, so they build the answer above themselves with Copilot. |

## AI — Discover Insights (Goal 3)

| Notebook | What it does |
| --- | --- |
| `3 - Anonymize Course reviews with Foundry AI.ipynb` | Calls an Azure AI Foundry chat model to anonymize/rewrite free-text course reviews (removing identifiers) and writes a de-identified Silver table. Endpoint/key from a Fabric Variable Library. |
| `4 - Analyze CR with Built-in AI.ipynb` | Uses Fabric's built-in AI functions (`ai.analyze_sentiment`, `ai.summarize`, `ai.classify`, `ai.extract`) over raw review text to derive sentiment, recommendation, and topic themes into `course_review_signal_ai`. |

## Gold — Model & Serve (Goal 4)

| Notebook | What it does |
| --- | --- |
| `Gold - Business Marts (MLV).ipynb` | Builds the Gold layer as **Materialized Lake Views** in `GoldLakehouse`: four Tier-1 wide marts and six Tier-2 business-question answers, ready for a Direct Lake semantic model and Data Agents. |
