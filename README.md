📊 Google Play Store Review Trend Analysis (Agentic AI)

🔍 Problem Statement

Product teams rely on user reviews to identify recurring issues, feature requests, and emerging feedback trends.
However, raw app-store reviews arrive daily, unstructured, noisy, and semantically inconsistent.

This project builds an Agentic AI pipeline that:

Consumes daily Google Play Store reviews (batch-wise)

Extracts high-recall topics (issues, requests, feedback)

Deduplicates semantically similar topics

Produces a T-30 → T trend analysis table for decision-making

This implementation strictly follows the Pulsegen Assignment requirements.

🧠 High-Level Architecture
Google Play Reviews (Daily Batch)
          ↓
 Review Ingestion Agent
          ↓
 Topic Extraction Agent
          ↓
 Topic Deduplication & Normalization Agent
          ↓
 Trend Aggregation Agent
          ↓
 30-Day Topic Trend Report (CSV)


Each stage is implemented as an independent agent, ensuring modularity, explainability, and scalability.

🤖 Agent Descriptions
1️⃣ Review Ingestion Agent

Fetches Google Play Store reviews

Treats each day’s reviews as a batch

Handles real-world API limitations gracefully

Outputs: data/raw_reviews/YYYY-MM-DD.csv

2️⃣ Topic Extraction Agent

Extracts issues, requests, and feedback

Designed for high recall

Uses a deterministic fallback extractor to ensure uninterrupted execution when LLM quota is unavailable

Outputs: data/processed/extracted_topics.csv

Design Choice:
Over-extraction first → cleanup later (best practice for trend analysis)

3️⃣ Topic Deduplication & Normalization Agent ⭐

Uses sentence embeddings (all-MiniLM-L6-v2)

Computes cosine similarity

Consolidates semantically equivalent topics

Example:

"delivery guy was rude"
"delivery partner behaved badly"
"delivery person impolite"
→ Delivery partner rude


Outputs: data/processed/normalized_topics.csv

4️⃣ Trend Aggregation Agent

Computes rolling T-30 → T window

Rows → Canonical topics

Columns → Calendar dates

Values → Topic frequency per day

Missing days filled with 0

Final Output:

output/trend_report.csv

📅 Date Logic (Important)

T = latest available review date

Window = T-30 → T

Continuous calendar dates ensured

Zero-filled gaps maintain temporal consistency

This exactly matches the assignment specification.

📁 Project Structure
Google-Play-Store-reviews/
│
├── agents/
│   ├── ingestion_agent.py
│   ├── extraction_agent.py
│   ├── dedup_agent.py
│   ├── trend_agent.py
│   └── __init__.py
│
├── data/
│   ├── raw_reviews/
│   └── processed/
│
├── output/
│   └── trend_report.csv
│
├── prompts/
│   └── topic_extraction.txt
│
├── main.py
├── requirements.txt
└── README.md

▶️ How to Run
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run the full pipeline
python main.py

3️⃣ View output

Open:

output/trend_report.csv

📊 Sample Output (Trend Table)
Topic	2025-11-25	...	2025-12-24
Delivery delayed	3	...	21
Food cold	1	...	11
App crash	0	...	7
⚙️ Assumptions & Limitations

Google Play API does not guarantee historical backfill

Daily batch ingestion simulates real-world streaming constraints

LLM usage is optional; deterministic fallback ensures reproducibility

Trends become richer as more daily batches accumulate

✅ Why This Approach

✔ True Agentic AI design

✔ High recall with semantic normalization

✔ No LDA / TopicBERT

✔ Production-ready, fault-tolerant pipeline

✔ Directly usable by product teams

🎯 Assignment Compliance

Agentic AI ✔

Topic deduplication ✔

Trend analysis ✔

Correct output format ✔

Daily batch assumption ✔

👤 Author

Raahul U
Google Play Store Review Trend Analysis – Pulsegen Assignment
