import streamlit as st
from huggingface_hub import InferenceClient
import time

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot - Working Version")

# Initialize client with CORRECT provider
@st.cache_resource
def get_client():
    HF_TOKEN = st.secrets["HF_TOKEN"]
    return InferenceClient(
        provider="hf-inference",  # CORRECTED: Use 'hf-inference' instead of 'huggingface'
        token=HF_TOKEN
    )

client = get_client()

# Model options
MODEL_OPTIONS = {
    "Mistral 7B": "mistralai/Mistral-7B-Instruct-v0.3",
    "Llama 3.1 8B": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "Zephyr 7B": "HuggingFaceH4/zephyr-7b-beta",
    "Google Gemma 7B": "google/gemma-7b-it"
}

with st.sidebar:
    st.header("⚙️ Settings")
    selected_model = st.selectbox("Choose Model:", list(MODEL_OPTIONS.keys()))
    MODEL_ID = MODEL_OPTIONS[selected_model]
    
    st.divider()
    max_tokens = st.slider("Max Tokens", 100, 1000, 500)
    temperature = st.slider("Temperature", 0.1, 1.0, 0.7)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
    ]

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
        message_placeholder.markdown("🤔 Thinking...")
        
        try:
            # Format conversation for the model
            conversation = ""
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    conversation += f"<|user|>\n{msg['content']}</s>\n"
                elif msg["role"] == "assistant":
                    conversation += f"<|assistant|>\n{msg['content']}</s>\n"
            
            conversation += "<|assistant|>\n"
            
            # Generate response using text generation (more reliable)
            response = client.text_generation(
                prompt=conversation,
                model=MODEL_ID,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                stream=False
            )
            
            # Clean and stream the response
            clean_response = response.strip()
            if clean_response.startswith("<|assistant|>"):
                clean_response = clean_response.replace("<|assistant|>", "").strip()
            clean_response = clean_response.split('</s>')[0].strip()
            
            # Stream the response
            display_text = ""
            words = clean_response.split()
            for word in words:
                display_text += word + " "
                message_placeholder.markdown(display_text + "▌")
                time.sleep(0.03)
            
            message_placeholder.markdown(display_text)
            st.session_state.messages.append({"role": "assistant", "content": display_text.strip()})
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.error(f"Detailed error: {e}")

st.divider()
st.caption(f"Using {selected_model} | Hugging Face Inference API")
