import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot - Direct API")

HF_TOKEN = st.secrets["HF_TOKEN"]

# Model configuration
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def query_model(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "do_sample": True,
            "return_full_text": False
        },
        "options": {
            "wait_for_model": True
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if prompt := st.chat_input("Ask me anything..."):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Generating response...")
        
        try:
            # Format prompt for Mistral
            conversation = ""
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    conversation += f"<|user|>{msg['content']}</s>"
                else:
                    conversation += f"<|assistant|>{msg['content']}</s>"
            
            conversation += "<|assistant|>"
            
            result = query_model(conversation)
            
            if isinstance(result, list) and len(result) > 0:
                response = result[0].get('generated_text', 'No response')
                
                # Clean response
                if response.startswith("<|assistant|>"):
                    response = response.replace("<|assistant|>", "").strip()
                response = response.split('</s>')[0].strip()
                
                # Stream display
                display_text = ""
                for word in response.split():
                    display_text += word + " "
                    message_placeholder.markdown(display_text + "▌")
                    time.sleep(0.03)
                
                message_placeholder.markdown(display_text)
                st.session_state.messages.append({"role": "assistant", "content": display_text.strip()})
            else:
                message_placeholder.markdown("Sorry, couldn't generate a response.")
                
        except Exception as e:
            message_placeholder.markdown(f"Error: {str(e)}")

st.caption("Using Direct Hugging Face API")
