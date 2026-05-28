import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Step 1: Load parsed documents
with open("data/unstructured/parsed.jsonl", "r") as f:
    docs = [json.loads(line) for line in f]

# Step 2: Extract all texts to embed
texts = []
payloads = []

for doc in docs:
    if doc["type"] == "pdf":
        text = doc["text"]
    elif doc["type"] == "email":
        text = f"{doc['subject']}\n{doc['body']}"
    else:
        continue

    # Chunking logic (optional): skip for simplicity here
    texts.append(text)
    payloads.append({"source": doc["filename"], "text": text})

# Step 3: Create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(texts, show_progress_bar=True)

# Step 4: Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Create collection (or recreate)
collection_name = "docs"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
)

# Step 5: Upload documents as points
points = [
    PointStruct(id=i, vector=vec.tolist(), payload=payloads[i])
    for i, vec in enumerate(vectors)
]

client.upload_points(collection_name=collection_name, points=points)

print(f"✅ Uploaded {len(points)} embedded documents to Qdrant.")
