import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Free AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Hugging Face configuration
@st.cache_data
def get_huggingface_models():
    return {
        "Microsoft DialoGPT": "microsoft/DialoGPT-large",
        "Google FLAN-T5": "google/flan-t5-xxl",
        "Facebook Blenderbot": "facebook/blenderbot-400M-distill",
        "GPT-2": "gpt2"
    }

def query_huggingface(prompt: str, model: str, conversation_history: list = None):
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    
    # For models that need API token (free account)
    headers = {
        "Authorization": f"Bearer {st.secrets.get('HF_API_KEY', '')}",
        "Content-Type": "application/json"
    }
    
    # Format prompt based on model type
    if "dialo" in model.lower():
        # For conversational models
        inputs = prompt
    else:
        # For text generation models
        inputs = f"Conversation:\n{''.join([f'User: {msg["content"]}\nAI: ' if msg['role'] == 'user' else f'{msg["content"]}\n' for msg in conversation_history[-4:]])}User: {prompt}\nAI:"
    
    payload = {
        "inputs": inputs,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.7,
            "do_sample": True
        },
        "options": {
            "wait_for_model": True
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=45)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'No response generated')
            else:
                return str(result)
        else:
            return f"Model is loading... Please try again in 30 seconds. (Status: {response.status_code})"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar configuration
with st.sidebar:
    st.title("🤖 Chatbot Settings")
    
    models = get_huggingface_models()
    selected_model = st.selectbox(
        "Choose Model",
        list(models.keys())
    )
    
    st.markdown("---")
    st.markdown("**Note:** Some models may take 20-30 seconds to load initially")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title("💬 Free AI Chatbot")
st.markdown("Powered by Hugging Face • 100% Free")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            model_id = models[selected_model]
            response = query_huggingface(
                prompt, 
                model_id,
                st.session_state.messages
            )
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
