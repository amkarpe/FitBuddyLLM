import json
from pathlib import Path
from pypdf import PdfReader
from src.config import PROCESSED_DOCS_PATH


RAW_ROOT = Path("data/raw")
ALLOWED_FOLDERS = ["nih_ods", "exercise_guidance", "who"]


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text.strip())

    return "\n".join(pages).strip()


def main():
    documents = []

    for folder_name in ALLOWED_FOLDERS:
        folder_path = RAW_ROOT / folder_name
        if not folder_path.exists():
            continue

        for pdf_file in folder_path.glob("*.pdf"):
            print(f"Parsing: {pdf_file}")
            text = extract_pdf_text(pdf_file)

            if not text:
                print(f"Skipped empty file: {pdf_file}")
                continue

            documents.append(
                {
                    "source": folder_name,
                    "title": pdf_file.stem,
                    "file_name": pdf_file.name,
                    "text": text,
                }
            )

    output_path = Path(PROCESSED_DOCS_PATH)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)

    print(f"Saved parsed documents to: {output_path}")
    print(f"Total documents: {len(documents)}")


if __name__ == "__main__":
    main()