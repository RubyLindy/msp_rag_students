import os
import chromadb
from llm import embed

DATA_PATH = "data/NAS"
DB_PATH = "chroma_db"

def load_files():
    docs = []

    for f in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, f)

        with open(path, "r", encoding="utf-8") as file:
            docs.append({
                "filename": f,
                "content": file.read()
            })

    return docs


def chunk(text, size=800, overlap=150):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+size])
        i += size - overlap
    return chunks


def ingest():
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection("nas")

    docs = load_files()

    print(f"Loaded {len(docs)} documents")

    idx = 0
    docnum = 0

    for doc in docs:
        docnum += 1

        filename = doc["filename"]
        content = doc["content"]

        for c in chunk(content):
            emb = embed(c)

            collection.add(
                ids=[f"chunk-{idx}"],
                embeddings=[emb],
                documents=[c],
                metadatas=[{
                    "area": "NAS",
                    "source": filename
                }]
            )

            idx += 1

        print(f"Completed document: {docnum}")

    print(f"Ingested {idx} chunks")


if __name__ == "__main__":
    ingest()