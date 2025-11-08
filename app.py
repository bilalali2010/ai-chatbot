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
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
    ]

# Display messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def query_api(prompt):
    """Improved API query with better error handling"""
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
            "wait_for_model": True,
            "use_cache": False
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                if 'generated_text' in result[0]:
                    return result[0]['generated_text']
                else:
                    return str(result[0])
            elif isinstance(result, dict) and 'generated_text' in result:
                return result['generated_text']
            else:
                return "I received an unexpected response format."
        
        elif response.status_code == 503:
            return "🔄 The model is currently loading. Please wait 20-30 seconds and try again. This is normal for free Hugging Face models."
        
        elif response.status_code == 429:
            return "⏳ Rate limit exceeded. Please wait a minute and try again."
        
        else:
            return f"❌ API Error (Status {response.status_code}): {response.text}"
            
    except requests.exceptions.Timeout:
        return "⏰ Request timeout. The model is taking too long to respond. Please try again."
    except requests.exceptions.ConnectionError:
        return "🔌 Connection error. Please check your internet connection."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# User input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            # Create better prompt format for Mistral
            conversation = ""
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    conversation += f"<|user|>\n{msg['content']}</s>\n"
                elif msg["role"] == "assistant":
                    conversation += f"<|assistant|>\n{msg['content']}</s>\n"
            
            # Add the current prompt for assistant to respond
            conversation += "<|assistant|>\n"
            
            response = query_api(conversation)
            
            # Clean up the response
            if response.startswith("<|assistant|>"):
                response = response.replace("<|assistant|>", "").strip()
            
            # Remove any closing tags
            response = response.split('</s>')[0].strip()
            
            # If response is empty, provide a default
            if not response or len(response) < 2:
                response = "I'm here! How can I assist you today?"
            
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.caption("Built with Streamlit and Hugging Face 🤗 | Model: Mistral 7B")
