import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Free AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b3137;
        color: white;
        margin-left: 20%;
    }
    .chat-message.assistant {
        background-color: #f0f2f6;
        margin-right: 20%;
    }
    .chat-input {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title
st.markdown('<h1 class="main-header">🤖 Free AI Chatbot</h1>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    model_choice = st.selectbox(
        "Choose AI Model:",
        ["DialoGPT-Medium", "HuggingFace API", "GPT-2"]
    )
    
    temperature = st.slider("Temperature:", 0.1, 1.0, 0.7)
    max_length = st.slider("Max Response Length:", 50, 500, 150)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Chat history display
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# AI Model Functions
def load_dialogpt_model():
    """Load DialoGPT model - runs locally"""
    if "dialogpt_model" not in st.session_state:
        with st.spinner("Loading AI model... This may take a minute."):
            tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
            model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
            st.session_state.dialogpt_model = (tokenizer, model)
    return st.session_state.dialogpt_model

def get_dialogpt_response(user_input, chat_history_ids=None):
    """Get response from DialoGPT model"""
    try:
        tokenizer, model = load_dialogpt_model()
        
        # Encode the user input
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        
        # Generate response
        bot_input_ids = new_input_ids if chat_history_ids is None else torch.cat([chat_history_ids, new_input_ids], dim=-1)
        
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=max_length + bot_input_ids.shape[-1],
            pad_token_id=tokenizer.eos_token_id,
            temperature=temperature,
            do_sample=True,
            top_p=0.9,
            no_repeat_ngram_size=3
        )
        
        # Decode response
        response = tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1]:][0], 
            skip_special_tokens=True
        )
        
        return response, chat_history_ids
        
    except Exception as e:
        return f"I encountered an error: {str(e)}", None

def get_huggingface_response(user_input):
    """Get response from Hugging Face Inference API"""
    try:
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": f"Bearer {st.secrets.get('HF_TOKEN', '')}"}
        
        payload = {
            "inputs": user_input,
            "parameters": {
                "max_length": max_length,
                "temperature": temperature,
                "do_sample": True
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            return "I'm having trouble connecting right now. Please try again."
            
    except Exception as e:
        return f"API Error: {str(e)}"

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if model_choice == "DialoGPT-Medium":
                response, _ = get_dialogpt_response(prompt)
            elif model_choice == "HuggingFace API":
                response = get_huggingface_response(prompt)
            else:
                response = "Please select a valid AI model."
            
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown(
    "Powered by Streamlit 🤖 | Models: DialoGPT • HuggingFace | "
    "**Completely Free AI Chatbot**"
)
