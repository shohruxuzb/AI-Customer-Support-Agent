# AI Customer Support Agent

This is a full-stack, production-ready AI Customer Support Chatbot built with **FastAPI** (Backend) and **Streamlit** (Frontend).
The agent supports RAG (Retrieval-Augmented Generation) so businesses can upload their own files (.pdf or .txt) and let the chatbot answer user queries based on those documents. It uses `sentence-transformers` for local embeddings and `FAISS` for quick vector storage and search.

## Features
- **Multi-LLM Support:** Choose between OpenAI and Groq APIs dynamically during your session.
- **Local RAG Pipeline:** Generates chunks and embeddings entirely locally using `all-MiniLM-L6-v2`, meaning you are not billed for embedding API calls.
- **Session-based Security:** API Keys are entered in the UI and are not hardcoded or saved anywhere in the repository. Provide it per session.
- **Modern UI:** Built using Streamlit, featuring file upload, chat history limits, usage limits (demo mode fallback), and chat UI.

## Tech Stack
- **Backend:** Python, FastAPI, PyPDF
- **Frontend:** Streamlit
- **Embeddings:** `sentence-transformers`
- **Vector Store:** `faiss-cpu`
- **LLM APIs:** `openai`, `groq`

## Setup & Run Instructions

### 1. Install Dependencies

Ensure you have Python installed. You can construct a virtual environment if you prefer. Then, install the requirements:

```bash
pip install -r requirements.txt
```

*(Note: The very first time you run the backend, `sentence-transformers` will download the `all-MiniLM-L6-v2` model weights locally ~80MB).*

### 2. Start the Backend

In a terminal, start the FastAPI server:
```bash
uvicorn backend.main:app --reload
```
The backend API will run on `http://127.0.0.1:8000`.

### 3. Start the Frontend

Open a new terminal window and run the Streamlit app:
```bash
streamlit run frontend/app.py
```
This will open your browser to `http://localhost:8501`.

## Usage
1. Open the UI.
2. In the Sidebar, select your preferred provider and input the API Key if available.
3. Upload a PDF or TXT using the Document Uploader in the sidebar and click **Process Document**.
4. Ask questions in the main chat interface about the loaded documents!
