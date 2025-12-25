# 📊 Google Play Store Review Trend Analysis (Agentic AI)

![Agentic AI Pipeline](https://raw.githubusercontent.com/github/explore/main/topics/artificial-intelligence/artificial-intelligence.png)

---

## 🔍 Problem Statement
Product teams rely on user reviews to identify **recurring issues, feature requests, and emerging feedback trends**.  
However, app-store reviews arrive **daily, unstructured, noisy, and semantically inconsistent**.

This project implements an **Agentic AI pipeline** that:
- Consumes **daily Google Play Store reviews**
- Extracts issues, requests, and feedback with **high recall**
- **Deduplicates semantically similar topics**
- Produces a **T-30 → T trend analysis table**

This solution strictly follows the **Pulsegen assignment requirements**.

---

## 🧠 Agentic Architecture

![Multi Agent Workflow](https://raw.githubusercontent.com/github/explore/main/topics/data-science/data-science.png)

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

yaml
Copy code

Each stage is implemented as an **independent agent**, ensuring modularity, explainability, and scalability.

---

## 🤖 Agent Overview

### 1️⃣ Review Ingestion Agent
- Fetches Google Play Store reviews
- Treats each day’s reviews as a **batch**
- Handles API limitations gracefully
- Output:
data/raw_reviews/YYYY-MM-DD.csv

yaml
Copy code

---

### 2️⃣ Topic Extraction Agent
- Extracts **issues, requests, and feedback**
- Designed for **high recall**
- Uses a deterministic fallback extractor to ensure reliability
- Output:
data/processed/extracted_topics.csv

yaml
Copy code

**Design choice:** Over-extraction first → cleanup later

---

### 3️⃣ Topic Deduplication & Normalization Agent ⭐
- Uses **sentence embeddings** (`all-MiniLM-L6-v2`)
- Computes **cosine similarity**
- Merges semantically equivalent topics

Example:
"delivery guy was rude"
"delivery partner behaved badly"
"delivery person impolite"
→ Delivery partner rude

makefile
Copy code

Output:
data/processed/normalized_topics.csv

yaml
Copy code

---

### 4️⃣ Trend Aggregation Agent
- Computes rolling **T-30 → T** window
- Rows → Topics
- Columns → Dates
- Values → Daily frequency
- Missing days filled with `0`

Final output:
output/trend_report.csv

yaml
Copy code

---

## 📅 Date Logic
- **T** = latest available review date
- **Window** = T-30 → T
- Continuous calendar dates guaranteed
- Zero-filled gaps preserve temporal consistency

This exactly matches the assignment specification.

---

## 📁 Project Structure

Google-Play-Store-reviews/
│
├── agents/
│ ├── ingestion_agent.py
│ ├── extraction_agent.py
│ ├── dedup_agent.py
│ ├── trend_agent.py
│ └── init.py
│
├── data/
│ ├── raw_reviews/
│ └── processed/
│
├── output/
│ └── trend_report.csv
│
├── prompts/
│ └── topic_extraction.txt
│
├── main.py
├── requirements.txt
└── README.md

yaml
Copy code

---

## ▶️ How to Run

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
2️⃣ Run the pipeline
bash
Copy code
python main.py
3️⃣ View output
Open:

bash
Copy code
output/trend_report.csv
📊 Sample Output

Topic	2025-11-25	...	2025-12-24
Delivery delayed	3	...	21
Food cold	1	...	11
App crash	0	...	7

⚙️ Assumptions & Limitations
Google Play does not guarantee historical backfill

Daily batch ingestion simulates real-world streaming constraints

LLM usage is optional; deterministic fallback ensures reproducibility

Trends improve as daily batches accumulate

✅ Assignment Compliance
Agentic AI approach ✔

Topic deduplication ✔

Trend analysis ✔

Correct output format ✔

Daily batch processing ✔

👤 Author
Raahul U
Pulsegen – Agentic AI Assignment
