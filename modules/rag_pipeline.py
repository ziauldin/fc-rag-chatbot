from modules.retriever import retrieve_chunks
from modules.generator import generate_answer
from modules.vectorstore import initialize_vector_db

# Initialize DB once
initialize_vector_db()

def answer_query(user_query: str) -> str:
    try:
        print(f"User Query: {user_query}")

        # 1. Retrieve chunks → list of dicts
        context_chunks = retrieve_chunks(user_query)
        print(f"Retrieved {len(context_chunks)} chunks.")

        if not context_chunks:
            return "I couldn't find any relevant information."

        # 2. Join chunks into ONE STRING of context
        context_text = "\n\n".join(context_chunks)

        # 3. Generate final answer
        response = generate_answer(context_text, user_query)
        return response

    except Exception as e:
        print("RAG Pipeline ERROR:", e)
        return "There was an internal error while processing your request."
