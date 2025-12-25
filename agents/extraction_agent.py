import pandas as pd
import os


class TopicExtractionAgent:
    """
    Agent responsible for extracting raw topics from reviews.

    NOTE:
    - LLM calls are intentionally DISABLED to avoid quota issues.
    - Deterministic fallback logic is used to ensure pipeline continuity.
    """

    def __init__(self, prompt_path="prompts/topic_extraction.txt"):
        # prompt_path kept for design completeness (agentic architecture)
        self.prompt_path = prompt_path

    def extract_topics(self, review_text: str):
        """
        Deterministic topic extraction (fallback-only mode).
        """
        return self.fallback_extract(review_text)

    def fallback_extract(self, review_text: str):
        """
        Heuristic extraction using keyword-based high-recall rules.
        """
        keyword_topic_map = {
            "delivery": "Delivery issue",
            "late": "Delivery delayed",
            "delay": "Delivery delayed",
            "cold": "Food cold",
            "stale": "Food stale",
            "rude": "Delivery partner rude",
            "crash": "App crash",
            "bug": "App bug",
            "payment": "Payment issue",
            "refund": "Refund issue",
            "support": "Customer support issue",
            "customer care": "Customer support issue",
            "instamart": "Instamart issue",
            "price": "Pricing issue",
            "expensive": "Pricing issue",
            "map": "Maps not working properly",
            "location": "Maps not working properly",
            "bolt": "10 minute delivery request",
            "fast delivery": "10 minute delivery request"
        }

        text = review_text.lower()
        topics = set()

        for keyword, topic in keyword_topic_map.items():
            if keyword in text:
                topics.add(topic)

        return list(topics)

    def process_daily_file(self, input_csv, output_csv):
        """
        Process a daily batch of reviews and extract topics.
        """
        df = pd.read_csv(input_csv)

        all_records = []

        for _, row in df.iterrows():
            topics = self.extract_topics(str(row["content"]))

            for topic in topics:
                all_records.append({
                    "review_id": row["review_id"],
                    "topic": topic,
                    "date": row["date"]
                })

        out_df = pd.DataFrame(all_records)
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        out_df.to_csv(output_csv, index=False)

        print(f"Extracted topics saved to {output_csv}")
