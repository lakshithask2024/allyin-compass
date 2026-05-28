from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from config import QDRANT_HOST, QDRANT_PORT

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
COLLECTION = "docs"

def query_vector(query: str, k: int = 3):
    try:
        embedding = model.encode(query)
        if not client.collection_exists(COLLECTION):
            return [{
                "id": -1,
                "score": 0.0,
                "text": "⚠️ Vector DB not initialized."
            }]

        hits = client.search(
            collection_name=COLLECTION,
            query_vector=embedding,
            limit=k
        )

        return [{
            "id": h.id,
            "score": h.score,
            "text": h.payload.get("text", "[no text]")
        } for h in hits]

    except Exception as e:
        return [{
            "id": -1,
            "score": 0.0,
            "text": f"⚠️ Qdrant error: {str(e)}"
        }]
