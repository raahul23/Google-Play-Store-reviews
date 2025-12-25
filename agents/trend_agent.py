import pandas as pd
from datetime import datetime, timedelta
import os


class TrendAggregationAgent:
    """
    Agent responsible for generating T-30 to T trend tables
    from normalized topic data.
    """

    def __init__(self, window_days=30):
        self.window_days = window_days

    def generate_trend_report(self, input_csv, output_csv):
        df = pd.read_csv(input_csv)

        df["date"] = pd.to_datetime(df["date"])

        end_date = df["date"].max()
        start_date = end_date - timedelta(days=self.window_days)

        date_range = pd.date_range(start=start_date, end=end_date)

        filtered_df = df[df["date"].between(start_date, end_date)]

        pivot = (
            filtered_df
            .groupby(["canonical_topic", "date"])
            .size()
            .reset_index(name="count")
            .pivot(index="canonical_topic", columns="date", values="count")
            .fillna(0)
        )

        pivot = pivot.reindex(columns=date_range, fill_value=0)

        pivot.columns = [d.strftime("%Y-%m-%d") for d in pivot.columns]

        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        pivot.to_csv(output_csv)

        print(f"Trend report saved to {output_csv}")
