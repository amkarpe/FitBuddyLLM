import json
from pathlib import Path
from src.config import PROCESSED_DOCS_PATH, CHUNKS_PATH


CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def main():
    input_path = Path(PROCESSED_DOCS_PATH)
    output_path = Path(CHUNKS_PATH)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc["text"])

        for idx, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "id": f"{doc['file_name']}_{idx}",
                    "text": chunk,
                    "metadata": {
                        "source": doc["source"],
                        "title": doc["title"],
                        "file_name": doc["file_name"],
                        "chunk_index": idx,
                    },
                }
            )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Saved chunks to: {output_path}")
    print(f"Total chunks: {len(all_chunks)}")


if __name__ == "__main__":
    main()