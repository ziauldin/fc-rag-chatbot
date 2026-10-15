# 🤖 FC Training RAG Chatbot ("Shampy")

A retrieval-augmented support chatbot I built at Future Connect Training & Recruitment to answer learners' questions about the training programs, courses, and staff. Questions go through a local embedding model and a ChromaDB vector search over the company's knowledge base, and Gemini writes a friendly, plain-text answer from the retrieved context. If the knowledge base has nothing relevant, it falls back to general knowledge.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=flat-square&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Sentence_Transformers-FFD21E?style=flat-square&logo=huggingface&logoColor=black)

<!-- Add a screenshot: ![Chat UI](screenshots/chat.png) -->

## ✨ Features
- 💬 Web chat UI (Flask + vanilla JS) with a `/chat` JSON endpoint
- 🧠 Local embeddings with `all-MiniLM-L6-v2` (Sentence Transformers), so retrieval needs no API calls
- 🗂️ Persistent ChromaDB vector store, built automatically from JSON files on first start
- 🔎 Top-5 chunk retrieval with cosine similarity
- ✍️ Answers from `gemini-2.5-flash`, steered by a system prompt for tone, formatting, and staff-profile questions

## 🗂️ Knowledge base format
The company's documents are not included in this repo. Put your own JSON files in `data/` with these names: `fc_master_rag.json`, `fc_pdf_rag.json`, `fc_employees_rag.json`. Each file is a list of chunks:

```json
[
  { "text": "Chunk of text to index", "metadata": { "source": "brochure.pdf", "page": 1 } }
]
```

Any metadata keys work. Lists and nested objects are flattened to strings before indexing.

## 🚀 Run locally

```bash
git clone https://github.com/ziauldin/fc-rag-chatbot.git
cd fc-rag-chatbot
pip install -r requirements.txt
cp .env.example .env        # add your Gemini key: GOOGLE_API_KEY=...
python app.py
```

Open http://127.0.0.1:5000. On Windows you can run `run.bat` instead. The first start downloads the embedding model and builds the vector store in `data/vector_store/`.

## 🛠️ Tech stack
Python · Flask · Google Gemini API · ChromaDB · Sentence Transformers · HTML/CSS/JavaScript
