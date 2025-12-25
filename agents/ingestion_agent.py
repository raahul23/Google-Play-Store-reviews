from google_play_scraper import reviews
import pandas as pd
from datetime import datetime
import os


class ReviewIngestionAgent:
    """
    Agent responsible for ingesting Google Play Store reviews
    and storing them as daily batches.
    """

    def __init__(self, app_id, output_dir="data/raw_reviews"):
        self.app_id = app_id
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_reviews_for_date(self, target_date: str):
        """
        Fetch reviews up to a target date.
        Due to Google Play limitations, this simulates daily batch ingestion.
        """
        target_date = datetime.strptime(target_date, "%Y-%m-%d").date()

        result, _ = reviews(
            self.app_id,
            lang="en",
            country="in",
            count=1000
        )

        collected_reviews = []
        for r in result:
            review_date = r["at"].date()

            if review_date <= target_date:
                collected_reviews.append({
                    "review_id": r.get("reviewId"),
                    "content": r.get("content"),
                    "rating": r.get("score"),
                    "date": review_date.isoformat()
                })

        return collected_reviews

    def save_latest_batch(self):
        """
        Save latest available reviews as a daily batch.
        """
        result, _ = reviews(
            self.app_id,
            lang="en",
            country="in",
            count=1000
        )

        if not result:
            print("No reviews fetched")
            return None

        processed = []
        for r in result:
            processed.append({
                "review_id": r.get("reviewId"),
                "content": r.get("content"),
                "rating": r.get("score"),
                "date": r["at"].date().isoformat()
            })

        df = pd.DataFrame(processed)

        batch_date = df["date"].max()
        file_path = os.path.join(self.output_dir, f"{batch_date}.csv")
        df.to_csv(file_path, index=False)

        print(f"Saved {len(df)} reviews for {batch_date}")
        return file_path
