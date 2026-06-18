from typing import List, Dict
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from src.config import CHROMA_DIR, COLLECTION_NAME


embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )
    return collection


def retrieve_context(query: str, top_k: int = 4) -> List[Dict]:
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    docs = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    ids = results.get("ids", [[]])[0]

    for doc_id, text, metadata in zip(ids, documents, metadatas):
        docs.append(
            {
                "id": doc_id,
                "text": text,
                "source": metadata.get("source", "Unknown"),
                "title": metadata.get("title", "Unknown"),
                "file_name": metadata.get("file_name", "Unknown"),
                "chunk_index": metadata.get("chunk_index", -1),
            }
        )

    return docs


def format_context(docs: List[Dict]) -> str:
    if not docs:
        return "No relevant context found."

    formatted = []
    for i, doc in enumerate(docs, start=1):
        formatted.append(
            f"[Source {i}: {doc['title']} | file: {doc['file_name']}]\n{doc['text']}"
        )
    return "\n\n".join(formatted)