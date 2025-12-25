from agents.ingestion_agent import ReviewIngestionAgent
from agents.extraction_agent import TopicExtractionAgent
from agents.dedup_agent import TopicDeduplicationAgent
from agents.trend_agent import TrendAggregationAgent

if __name__ == "__main__":
    ingestor = ReviewIngestionAgent("in.swiggy.android")
    raw_file = ingestor.save_latest_batch()

    extractor = TopicExtractionAgent()
    extractor.process_daily_file(
        raw_file,
        "data/processed/extracted_topics.csv"
    )

    dedup = TopicDeduplicationAgent(similarity_threshold=0.8)
    dedup.process_extracted_topics(
        "data/processed/extracted_topics.csv",
        "data/processed/normalized_topics.csv"
    )

    trend = TrendAggregationAgent(window_days=30)
    trend.generate_trend_report(
        "data/processed/normalized_topics.csv",
        "output/trend_report.csv"
    )
