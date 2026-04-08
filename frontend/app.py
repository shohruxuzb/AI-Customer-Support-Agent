import streamlit as st
import requests
import json
import time

# Page Configuration
st.set_page_config(page_title="AI Customer Support Agent", page_icon="🤖", layout="wide")

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Sidebar for Setup & Document Upload
with st.sidebar:
    st.title("⚙️ Management")
    st.info("Upload documents to train the agent.")
    
    uploaded_file = st.file_uploader("Upload PDF or Text", type=["pdf", "txt"])
    if uploaded_file is not None:
        if st.button("🚀 Process & Index"):
            with st.spinner("Processing document..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    response = requests.post(f"{BACKEND_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success(f"Successfully processed: {uploaded_file.name}")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")

    st.divider()
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main Chat Interface
st.title("🤖 AI Customer Support Bot")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*(thinking...)*")
        
        try:
            # Prepare payload with history
            # Extract last 5 messages for memory
            payload = {
                "message": prompt,
                "history": st.session_state.messages[:-1]
            }
            
            response = requests.post(
                f"{BACKEND_URL}/chat", 
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                answer = response.json().get("response", "I'm sorry, I couldn't process that.")
                # Simulate typing effect
                full_response = ""
                for chunk in answer.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                message_placeholder.error(f"Error: {response.status_code}")
                
        except Exception as e:
            message_placeholder.error(f"Failed to connect to backend. Make sure it's running. Error: {str(e)}")
