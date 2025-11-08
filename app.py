import streamlit as st
import requests
import time

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot - Direct API")

# Hugging Face API configuration
HF_TOKEN = st.secrets["HF_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def query_huggingface(prompt):
    """Direct API call to Hugging Face"""
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# User input
if prompt := st.chat_input("What would you like to know?"):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Format prompt for the model
                conversation = "\n".join([
                    f"<|user|>{msg['content']}</s>" if msg['role'] == 'user' 
                    else f"<|assistant|>{msg['content']}</s>" 
                    for msg in st.session_state.messages
                ]) + "<|assistant|>"
                
                response = query_huggingface(conversation)
                
                if isinstance(response, list) and len(response) > 0:
                    answer = response[0]['generated_text']
                else:
                    answer = "Sorry, I couldn't generate a response."
                
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
