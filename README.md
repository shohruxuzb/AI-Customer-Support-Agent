# 🤖 AI Customer Support Chatbot (RAG-based)

An AI-powered customer support chatbot that answers user questions based on business documents (PDF/TXT).  
It uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware responses.

---

## 🌐 Live Demo

👉 https://ai-customer-support-agent-6umj.onrender.com  

⚠️ Note: The app may take 30–60 seconds to load initially due to free hosting.

---

## 🎥 Demo Video

👉 https://youtu.be/E7walQGG9f8

---

## 💼 Business Value

This solution helps businesses:

- Reduce customer support workload  
- Provide instant answers to FAQs  
- Enable 24/7 automated support  
- Improve response time and customer experience  

---

## ✨ Features

- 💬 Chat interface (AI assistant style)
- 📄 Upload PDF or TXT documents
- 🧠 Answers based on your data (RAG)
- 🔎 Fast semantic search using FAISS
- 🧾 Chat memory (context-aware responses)
- 🔑 Supports user-provided API keys (Groq / OpenAI)
- ⚡ Lightweight and fast

---

## 🧠 Example Use Case

1. Upload a company FAQ document  
2. Ask:
   > "What is your refund policy?"  
3. AI responds using information from the document  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **Vector DB:** FAISS  
- **Embeddings:** sentence-transformers (`all-MiniLM-L6-v2`)  
- **LLM:** Groq / OpenAI  

---

## ⚙️ How to Run Locally

bash
git clone https://github.com/shohruxuzb/AI-Customer-Support-Agent.git
cd AI-Customer-Support-Agent

pip install -r requirements.txt

# Run backend
uvicorn backend.main:app --reload

# Run frontend
streamlit run frontend/app.py
🚀 Deployment

You can deploy this project using:

Render
Railway
Example (Render):
Build command:
pip install -r requirements.txt
Start command:
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
🔐 API Key Usage

To use the chatbot:

Enter your Groq or OpenAI API key in the app
Keys are used only during the session and are not stored
📸 Screenshots

<img width="365" height="913" alt="Screenshot 2026-04-15 121335" src="https://github.com/user-attachments/assets/03d1559c-e95b-4f93-85fa-216d2f01d6ad" />
<img width="1911" height="909" alt="Screenshot 2026-04-15 121317" src="https://github.com/user-attachments/assets/f3b4d533-71fa-4355-96c4-04c3388fb39e" />


Chat interface
File upload
AI response
🧩 Use Cases
Customer support chatbot
FAQ automation
Internal knowledge assistant
Document Q&A system
📈 Future Improvements
Multi-language support
Admin dashboard
WhatsApp / Telegram integration
Database storage for conversations
👨‍💻 Author

Built by Shohruh

## 📞 Available for Freelance Work
I can build custom AI chatbots and automation tools for your business.
