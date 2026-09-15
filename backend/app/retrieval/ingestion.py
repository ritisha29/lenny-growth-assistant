from pathlib import Path
import json

import chromadb
import frontmatter
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[3]

TRANSCRIPTS_DIR = PROJECT_ROOT / "data" / "transcripts"
SOURCE_INDEX = PROJECT_ROOT / "temp-lenny-data" / "index.json"
CHROMA_DIR = PROJECT_ROOT / "chroma_data"

COLLECTION_NAME = "lenny_podcast_transcripts"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def load_source_index() -> dict[str, dict]:
    """
    Load podcast metadata from the dataset's index.json.

    Returns:
        A mapping from transcript filename to metadata.
    """

    with SOURCE_INDEX.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    podcast_index = {}

    for podcast in data.get("podcasts", []):
        filename = podcast.get("filename", "")

        if filename:
            podcast_index[
                Path(filename).name
            ] = podcast

    return podcast_index


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """
    Split transcript text into overlapping word-based chunks.
    """

    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunks.append(
            " ".join(words[start:end])
        )

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def load_transcripts() -> list[dict]:
    """
    Load podcast transcripts and attach reliable source metadata.
    """

    source_index = load_source_index()

    documents = []

    for file_path in sorted(
        TRANSCRIPTS_DIR.glob("*.md")
    ):
        post = frontmatter.load(file_path)

        indexed_metadata = source_index.get(
            file_path.name,
            {},
        )

        metadata = {
    "episode_title": indexed_metadata.get("title", post.get("title", file_path.stem)),
    "guest": indexed_metadata.get("guest", post.get("guest", "")),
    "date": indexed_metadata.get("date", post.get("date", "")),
    "source_url": indexed_metadata.get(
        "post_url",
        indexed_metadata.get("youtube_url", post.get("post_url", ""))
    ),
    "description": indexed_metadata.get("description", post.get("description", "")),
    "filename": file_path.name,
}

        chunks = chunk_text(post.content)

        for index, chunk in enumerate(chunks):
            documents.append(
                {
                    "id": f"{file_path.stem}-{index}",
                    "text": chunk,
                    "metadata": {
                        **metadata,
                        "chunk_index": index,
                    },
                }
            )

    return documents


def build_vector_store():
    """
    Rebuild the ChromaDB collection from podcast transcripts.
    """

    print("Loading embedding model...")

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print("Loading transcripts...")

    documents = load_transcripts()

    print(
        f"Loaded {len(documents)} transcript chunks."
    )

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    # Make ingestion repeatable.
    existing = collection.get()

    if existing["ids"]:
        collection.delete(
            ids=existing["ids"]
        )

    print("Creating embeddings...")

    texts = [
        document["text"]
        for document in documents
    ]

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True,
    ).tolist()

    collection.add(
        ids=[
            document["id"]
            for document in documents
        ],
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            document["metadata"]
            for document in documents
        ],
    )

    print(
        f"Successfully indexed {len(documents)} chunks."
    )


if __name__ == "__main__":
    build_vector_store()