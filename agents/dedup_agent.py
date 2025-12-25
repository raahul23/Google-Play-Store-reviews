import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os


class TopicDeduplicationAgent:
    """
    Agent responsible for semantic deduplication and normalization of topics.
    """

    def __init__(self, similarity_threshold=0.8):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.similarity_threshold = similarity_threshold

    def deduplicate_topics(self, topics):
        """
        Groups semantically similar topics and returns a mapping:
        raw_topic -> canonical_topic
        """
        embeddings = self.model.encode(topics)
        similarity_matrix = cosine_similarity(embeddings)

        canonical_topics = {}
        visited = set()

        for i, topic in enumerate(topics):
            if topic in visited:
                continue

            canonical_topics[topic] = topic
            visited.add(topic)

            for j in range(i + 1, len(topics)):
                if similarity_matrix[i][j] >= self.similarity_threshold:
                    canonical_topics[topics[j]] = topic
                    visited.add(topics[j])

        return canonical_topics

    def process_extracted_topics(self, input_csv, output_csv):
        """
        Reads extracted topics and outputs normalized topics.
        """
        df = pd.read_csv(input_csv)

        unique_topics = df["topic"].unique().tolist()
        topic_map = self.deduplicate_topics(unique_topics)

        df["canonical_topic"] = df["topic"].map(topic_map)

        os.makedirs(os.path.dirname(output_csv), exist_ok=True)
        df.to_csv(output_csv, index=False)

        print(f"Deduplicated topics saved to {output_csv}")
