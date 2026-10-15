import os
import json
import chromadb
from chromadb.utils import embedding_functions
from modules.embeddings import generate_embedding
from config import VECTOR_DB_DIR

# ----------------------------------------
# CUSTOM EMBEDDING FUNCTION
# ----------------------------------------
class GeminiEmbeddingFunction(embedding_functions.EmbeddingFunction):
    """Wrapper to use Gemini embeddings inside ChromaDB."""
    def __call__(self, texts):
        vectors = []
        for t in texts:
            emb = generate_embedding(t)
            if emb:
                vectors.append(emb)
            else:
                print(f"[WARNING] Failed to embed text: {t[:40]}...")
                vectors.append([0.0] * 768)  # Safe fallback
        return vectors


# ----------------------------------------
# CHROMA CLIENT
# ----------------------------------------
gemini_ef = GeminiEmbeddingFunction()
client = chromadb.PersistentClient(path=VECTOR_DB_DIR)

COLLECTION_NAME = "fc_training_collection"


# ----------------------------------------
# GET OR CREATE COLLECTION
# ----------------------------------------
def get_or_create_collection():
    try:
        col = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=gemini_ef
        )
        print(f"[INFO] Loaded existing ChromaDB collection: {COLLECTION_NAME}")
        return col

    except Exception:
        print(f"[INFO] Collection not found. Creating new one: {COLLECTION_NAME}")
        col = client.create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
            embedding_function=gemini_ef
        )
        return col


# ----------------------------------------
# LOAD MULTIPLE JSON DATASETS
# ----------------------------------------
def load_all_rag_files():
    data_dir = "data"

    json_files = [
        "fc_employees_rag.json",
        "fc_master_rag.json",
        "fc_pdf_rag.json"
    ]

    all_docs = []

    for file in json_files:
        path = os.path.join(data_dir, file)

        if not os.path.exists(path):
            print(f"[WARNING] File not found: {path}")
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                docs = json.load(f)
                print(f"[INFO] Loaded {len(docs)} docs from {file}")
                all_docs.extend(docs)
        except Exception as e:
            print(f"[ERROR] Could not read {file}: {e}")

    print(f"[INFO] Total documents loaded: {len(all_docs)}")
    return all_docs



# ----------------------------------------
# INITIALIZE VECTOR DATABASE
# ----------------------------------------
def initialize_vector_db():
    collection = get_or_create_collection()

    # Skip rebuild if DB already populated
    if collection.count() > 0:
        print(f"[INFO] Vector DB already initialized with {collection.count()} embeddings.")
        return

    documents = load_all_rag_files()

    if not documents:
        print("[ERROR] No documents found. Cannot build vector DB.")
        return

    print(f"[INFO] Building vector DB with {len(documents)} documents...")

    texts = []
    metadatas = []
    ids = []

    for i, doc in enumerate(documents):

        # ----------------------------------------
        # TEXT
        # ----------------------------------------
        text = doc.get("text", "").strip()
        if not text:
            continue
        texts.append(text)

        # ----------------------------------------
        # METADATA CLEANING (MAIN FIX)
        # ----------------------------------------
        meta = doc.get("metadata", {})

        if not isinstance(meta, dict):
            meta = {}

        clean_meta = {}
        for key, val in meta.items():

            # FIX: Convert list → comma-separated string
            if isinstance(val, list):
                clean_meta[key] = ", ".join([str(v) for v in val])

            # FIX: Convert nested dict → JSON string
            elif isinstance(val, dict):
                clean_meta[key] = json.dumps(val)

            # Valid types → keep
            else:
                clean_meta[key] = val

        # Add guaranteed metadata
        clean_meta["source"] = doc.get("source", "fc_rag_data")
        clean_meta["index"] = i

        metadatas.append(clean_meta)

        # ----------------------------------------
        # UNIQUE ID
        # ----------------------------------------
        ids.append(f"doc_{i}")


    # ----------------------------------------
    # INSERT INTO CHROMA
    # ----------------------------------------
    try:
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        print("[SUCCESS] Vector DB initialization complete.")

    except Exception as e:
        print(f"[ERROR] Failed to add documents: {e}")


# ----------------------------------------
# SEARCH MODULE
# ----------------------------------------
def search_similar(query_embedding, top_k):
    collection = get_or_create_collection()

    if not query_embedding:
        print("[ERROR] Empty query embedding.")
        return []

    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas"]
        )

        output = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            output.append({
                "text": doc,
                "metadata": meta
            })

        return output

    except Exception as e:
        print(f"[ERROR] Similarity search failed: {e}")
        return []

