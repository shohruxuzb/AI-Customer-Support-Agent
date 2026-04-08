# AI Customer Support Chatbot 🤖

A production-ready full-stack AI Customer Support Chatbot that uses RAG (Retrieval-Augmented Generation) to answer questions based on your specialized documents (PDF/Text).

## 🚀 Features
- **Document Ingestion**: Upload PDF or TXT files to automatically "train" your agent.
- **RAG Architecture**: Uses FAISS for lightning-fast similarity search and Groq (Llama 3.3) for intelligent responses.
- **Shared Context**: Singleton-based backend ensures uploaded data is immediately available for chat.
- **Streamlit Interface**: A clean, responsive UI with chat history and typing indicators.
- **Persistent Memory**: Remembers recent conversation history for more natural interactions.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **LLM**: Groq AI API (`llama-3.3-70b-versatile`)
- **Vector DB**: FAISS (Meta)
- **Embeddings**: `all-MiniLM-L6-v2` (Sentence Transformers)

## 📋 Prerequisites
- Python 3.9+
- Groq API Key (Get one at [console.groq.com](https://console.groq.com/))

## ⚙️ Installation & Setup

### 1. Clone & Environment
```bash
# Clone the repository (if applicable)
cd AI-Customer-Support-Agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory (or use the provided template):
```text
GROQ_API_KEY=your_gsk_xxx_key
MODEL_NAME=llama-3.3-70b-versatile
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 3. Running the App
The application consists of two parts running simultaneously.

#### **Start Backend**
```bash
uvicorn backend.main:app --reload
```

#### **Start Frontend**
```bash
streamlit run frontend/app.py
```

## 📂 Project Structure
```text
backend/
  main.py           # Application entry point
  routes/           # API endpoints (upload, chat)
  services/         # Core logic (FAISS, Groq, Singletons)
  utils/            # Document processing utilities
  vector_store/     # Persistent storage for indices
frontend/
  app.py            # Streamlit Chat UI
requirements.txt    # Python dependencies
.env                # Local configuration
.gitignore          # Git exclusion rules
```

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.
