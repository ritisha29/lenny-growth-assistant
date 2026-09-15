from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHROMA_DIR = PROJECT_ROOT / "chroma_data"
COLLECTION_NAME = "lenny_podcast_transcripts"


class TranscriptRetriever:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIR)
        )

        self.collection = self.client.get_collection(
            name=COLLECTION_NAME
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: int = 20,
    ) -> list[dict]:

        query_embedding = self.embedding_model.encode(
            query
        ).tolist()

        query_kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": candidate_k,
        }

        # If a known guest is explicitly mentioned in the query,
        # restrict retrieval to that guest's transcript.
        guest_names = [
            "Jason Cohen",
            "Matt MacInnis",
            "Elena Verna",
            "Marc Andreessen",
            "Adam Mosseri",
        ]

        for guest in guest_names:
            if guest.lower() in query.lower():
                query_kwargs["where"] = {
                    "guest": guest
                }
                break

        results = self.collection.query(**query_kwargs)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        candidates = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            candidates.append(
                {
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        # Give a small boost to chunks containing words
        # from the query.
        query_words = {
            word.lower()
            for word in query.split()
            if len(word) > 3
        }

        for candidate in candidates:
            text_words = set(
                candidate["text"].lower().split()
            )

            lexical_matches = sum(
                1
                for word in query_words
                if word in text_words
            )

            candidate["lexical_matches"] = lexical_matches

        candidates.sort(
            key=lambda item: (
                item["distance"]
                - (item["lexical_matches"] * 0.01)
            )
        )

        return candidates[:top_k]