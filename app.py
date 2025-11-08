import streamlit as st
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
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
    ]

# Title
st.markdown('<h1 class="main-header">🤖 Free AI Chatbot</h1>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    model_choice = st.selectbox(
        "Choose AI Model:",
        ["HuggingFace API", "Local Model (Basic)"]
    )
    
    temperature = st.slider("Temperature:", 0.1, 1.0, 0.7)
    max_length = st.slider("Max Response Length:", 50, 500, 150)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat history cleared! How can I help you?"}
        ]
        st.rerun()

    st.info("💡 For best results, use HuggingFace API with a free token")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# AI Response Functions
def get_huggingface_response(user_input):
    """Get response from Hugging Face Inference API"""
    try:
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        # You can get a free token from huggingface.co
        headers = {"Authorization": f"Bearer {st.secrets.get('HF_TOKEN', '')}"}
        
        payload = {
            "inputs": user_input,
            "parameters": {
                "max_length": max_length,
                "temperature": temperature,
                "do_sample": True,
                "top_p": 0.9
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'Sorry, I could not generate a response.')
            else:
                return "Sorry, I didn't understand that. Could you rephrase?"
        else:
            return f"⚠️ API temporarily unavailable. Status: {response.status_code}"

    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_local_response(user_input):
    """Simple local response when API is not available"""
    responses = [
        "I'm a basic AI assistant. For full features, please configure the HuggingFace API.",
        "Hello! I can help with general questions. What would you like to know?",
        "I'm here to assist you. Feel free to ask me anything!",
        "That's an interesting question. For more detailed responses, try the HuggingFace API option."
    ]
    import random
    return random.choice(responses)

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
            if model_choice == "HuggingFace API":
                response = get_huggingface_response(prompt)
            else:
                response = get_local_response(prompt)
            
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.markdown(
    "**Powered by Streamlit & HuggingFace** 🤖 | "
    "⭐ Star this repo on GitHub if you like it!"
)
