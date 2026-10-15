from sentence_transformers import SentenceTransformer

# Load a free, high-quality embedding model
# This will download once and run locally afterward.
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str) -> list[float]:
    """
    Generates a local embedding using a free SentenceTransformer model.
    No API calls, no quotas, no billing.
    """
    if not text:
        return []

    # Encode returns a NumPy array → convert to list for ChromaDB
    embedding = model.encode(text).tolist()
    return embedding
