import os
import json
import chromadb
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

# Constants
VECTOR_DIR = "vector_db"
COLLECTION_NAME = "sensitive_examples"
DATA_FILE = "data/examples.json"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup Chroma client
chroma_client = PersistentClient(path=VECTOR_DIR)
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

def load_examples():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def index_examples():
    examples = load_examples()

    print(f"📚 Indexing {len(examples)} examples...")
    embeddings = model.encode(examples).tolist()
    ids = [f"ex_{i}" for i in range(len(examples))]

    collection.add(
        documents=examples,
        embeddings=embeddings,
        ids=ids
    )

    print(f"✅ Indexed and saved to {VECTOR_DIR}")

def search_similar(text, top_k=5):
    embedding = model.encode([text])[0].tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return results

def add_example_to_vector_db(text: str):
    """Add a new sentence to Chroma DB (auto-learn)."""
    embedding = model.encode([text]).tolist()
    import datetime
    uid = f"ex_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')}"
    collection.add(
        documents=[text],
        embeddings=embedding,
        ids=[uid]
    )
    print(f"🆕 Added new example to vector DB: {text}")

if __name__ == "__main__":
    index_examples()
