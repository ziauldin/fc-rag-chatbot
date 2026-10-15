from modules.embeddings import generate_embedding
from modules.vectorstore import search_similar
from config import TOP_K_CHUNKS

def retrieve_chunks(query_text: str) -> list[str]:
    """
    Retrieves the most relevant chunks from the vector store for a given query.

    Args:
        query_text: The user's question.

    Returns:
        A list of strings, where each string is a retrieved document chunk.
    """
    print(f"Retrieving chunks for query: {query_text[:50]}...")
    
    # 1. Generate embedding for the query
    query_embedding = generate_embedding(query_text)
    
    if not query_embedding:
        print("Failed to generate query embedding.")
        return []

    # 2. Search the vector store for similar documents
    retrieved_data = search_similar(query_embedding, TOP_K_CHUNKS)
    
    # 3. Extract the text from the retrieved data
    chunks = [item['text'] for item in retrieved_data]
    
    print(f"Retrieved {len(chunks)} chunks.")
    return chunks

