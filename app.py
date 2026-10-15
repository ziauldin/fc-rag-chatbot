import os
from flask import Flask, render_template, request, jsonify
from config import SECRET_KEY, DOCS_JSON_PATH
from modules.rag_pipeline import answer_query
from modules.vectorstore import initialize_vector_db

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# --- INITIALIZATION ---
# Ensure the vector store is initialized on application startup
# This will create the vector store if it doesn't exist and populate it 
# with the dummy data if it's empty.
print("Initializing Vector Database...")
initialize_vector_db()
print("Vector Database Initialization Complete.")

# --- ROUTES ---

@app.route('/')
def index():
    """Serves the main chat interface page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handles the POST request for the chatbot interaction."""
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400

    print(f"User Query: {user_message}")
    
    # Call the main RAG pipeline function
    try:
        chatbot_response = answer_query(user_message)
        print(f"Chatbot Response: {chatbot_response[:100]}...")
        return jsonify({"response": chatbot_response})
    except Exception as e:
        print(f"An error occurred during RAG pipeline execution: {e}")
        return jsonify({"response": "An internal error occurred. Please check the server logs."}), 500

# --- RUN THE APP ---
if __name__ == '__main__':
    # The host is set to '0.0.0.0' to make it accessible outside the container/sandbox
    app.run(debug=True, host='0.0.0.0', port=5000)

