import streamlit as st
from huggingface_hub import InferenceClient
import time

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot - Working Version")

# Initialize client with new endpoint
@st.cache_resource
def get_client():
    HF_TOKEN = st.secrets["HF_TOKEN"]
    return InferenceClient(
        provider="huggingface",
        token=HF_TOKEN
    )

client = get_client()

# Model options
MODEL_OPTIONS = {
    "Mistral 7B": "mistralai/Mistral-7B-Instruct-v0.3",
    "Llama 3.1 8B": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "Zephyr 7B": "HuggingFaceH4/zephyr-7b-beta"
}

with st.sidebar:
    selected_model = st.selectbox("Model:", list(MODEL_OPTIONS.keys()))
    MODEL_ID = MODEL_OPTIONS[selected_model]
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ Thinking...")
        
        try:
            # Use text generation as fallback
            conversation = ""
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    conversation += f"User: {msg['content']}\n\n"
                else:
                    conversation += f"Assistant: {msg['content']}\n\n"
            
            conversation += "Assistant: "
            
            # Generate response
            response = client.text_generation(
                prompt=conversation,
                model=MODEL_ID,
                max_new_tokens=500,
                temperature=0.7,
                stream=False
            )
            
            # Stream response
            full_response = response.strip()
            display_text = ""
            for word in full_response.split():
                display_text += word + " "
                message_placeholder.markdown(display_text + "▌")
                time.sleep(0.05)
            
            message_placeholder.markdown(display_text)
            st.session_state.messages.append({"role": "assistant", "content": display_text.strip()})
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

st.caption("Using updated Hugging Face API")
