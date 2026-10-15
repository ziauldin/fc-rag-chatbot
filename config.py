import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API KEY ---
# Set GOOGLE_API_KEY in a .env file (see .env.example).
# Used by the Gemini model that writes the answers (embeddings run locally).
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set. Copy .env.example to .env and add your Gemini API key.")

# --- VECTOR DATABASE CONFIGURATION ---
# Directory where the persistent ChromaDB vector store will be saved.
VECTOR_DB_DIR = "data/vector_store"

# --- DATA CONFIGURATION ---
# Path to the JSON file containing the training documents (chunks).
DOCS_JSON_PATH = "data/fc_master_rag.json"

# --- RAG CONFIGURATION ---
# The number of top-k chunks to retrieve from the vector store.
TOP_K_CHUNKS = 5

# --- MODEL CONFIGURATION ---
# Embedding model name
EMBEDDING_MODEL = "models/embedding-001"
# LLM model name for generation
GENERATION_MODEL = "gemini-pro"

# --- FLASK CONFIGURATION ---
# Secret key for Flask sessions (can be anything for this simple app)
SECRET_KEY = os.urandom(24)


