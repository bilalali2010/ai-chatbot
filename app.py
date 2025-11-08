import streamlit as st
import requests
import time

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# Configuration
HF_TOKEN = st.secrets["HF_TOKEN"]
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def query_api(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'No response generated')
        return "Please try again in a few seconds..."
    except Exception as e:
        return f"Error: {str(e)}"

# User input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Create simple prompt
            chat_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            full_prompt = f"{chat_history}\nassistant:"
            
            response = query_api(full_prompt)
            
            # Clean response
            if "assistant:" in response:
                response = response.split("assistant:")[-1].strip()
            
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

st.caption("Built with Streamlit and Hugging Face")
