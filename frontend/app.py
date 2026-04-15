import streamlit as st
import requests

import os

# FastAPI Backend URL - allows Render override via Environment Variables
API_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000/api")

# Page configuration
st.set_page_config(page_title="AI Customer Support", page_icon="💬", layout="wide")

# Custom CSS for an enhanced look and feel
st.markdown("""
<style>
/* Center main content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
/* Chat buble margins */
.stChatMessage {
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I am your AI Customer Support assistant. Upload your documents in the sidebar, provide your API key, and ask me anything."
    })
    
# Demo usage counter if no API key is provided
if "demo_usage_count" not in st.session_state:
    st.session_state.demo_usage_count = 0

# Sidebar setup
with st.sidebar:
    st.title("⚙️ Configuration")
    
    st.subheader("Model Settings")
    provider = st.selectbox("LLM Provider", ["OpenAI", "Groq"])
    api_key = st.text_input("API Key", type="password", help="Enter your provider's API key. It is not saved permanently.")
    
    st.markdown("---")
    
    st.subheader("📄 Knowledge Base")
    uploaded_file = st.file_uploader("Upload Document (PDF/TXT)", type=["pdf", "txt"])
    
    if st.button("Process Document", use_container_width=True):
        if uploaded_file is not None:
            with st.spinner("Processing ..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    response = requests.post(f"{API_URL}/documents/upload", files=files)
                    if response.status_code == 200:
                        st.success(f"Processed: {uploaded_file.name}")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error("Failed to connect to the backend server. Is FastAPI running?")
        else:
            st.warning("Please choose a file to upload.")

    st.markdown("---")
    
    if st.button("🗑️ Reset Chat Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.demo_usage_count = 0
        st.rerun()
        
    st.markdown("---")
    st.caption("Backend must be running on http://127.0.0.1:8000")

# Main Interface
st.title("💬 Chat Interface")

# Render previous chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input handling
if prompt := st.chat_input("Ask a question about the uploaded documents..."):
    
    # Check Demo Usage
    if not api_key:
        if st.session_state.demo_usage_count >= 5:
            st.error("Demo limit of 5 messages reached. Please provide an API key in the sidebar to continue.")
            st.stop()
            
    # Add user message to state and UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare chat context (last 5 interactions properly paired to avoid exceeding context)
    # We slice -11 to -1 to get up to 10 messages (5 pairs), but the user asked for max 5.
    recent_history = st.session_state.messages[-5:-1]

    with st.chat_message("assistant"):
        with st.spinner("Starting AI system / generating answer... please wait (this can take 30-60 seconds on the free tier on the very first run!)"):
            payload = {
                "query": prompt,
                "history": recent_history,
                "provider": provider.lower(),
                "api_key": api_key if api_key else ""
            }
            
            try:
                res = requests.post(f"{API_URL}/chat", json=payload)
                if res.status_code == 200:
                    answer = res.json().get("answer", "No response retrieved.")
                    if not api_key:
                        st.session_state.demo_usage_count += 1
                else:
                    detail = res.json().get("detail", "Server Error")
                    answer = f"**Error from Backend:** {detail}"
            except Exception as e:
                answer = "**Connection Error:** Could not connect to the backend server. Please ensure FastAPI is running."

            st.markdown(answer)
    
    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})
