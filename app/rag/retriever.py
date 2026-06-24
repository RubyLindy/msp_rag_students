import chromadb
from app.rag.llm import embed

DB_PATH = "chroma_db"

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("nas")


def retrieve(query, k=5):
    q_emb = embed(query)

    print("Count of documents in the collection:", collection.count())

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k
    )

    return {
    "documents": results["documents"][0],
    "metadatas": results["metadatas"][0],
    "distances": results["distances"][0]
    }

## Add distance as a return value to the retrieve function





