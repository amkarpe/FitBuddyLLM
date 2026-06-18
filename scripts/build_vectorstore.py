import json
from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from src.config import CHUNKS_PATH, CHROMA_DIR, COLLECTION_NAME


def main():
    input_path = Path(CHUNKS_PATH)

    with open(input_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    client = chromadb.PersistentClient(path=CHROMA_DIR)

    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )

    ids = [chunk["id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        collection.add(
            ids=ids[i:i + batch_size],
            documents=documents[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size],
        )
        print(f"Inserted {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")

    print(f"Vectorstore built successfully at: {CHROMA_DIR}")


if __name__ == "__main__":
    main()