import streamlit as st
from huggingface_hub import InferenceClient
import time

# -------------------------
# STREAMLIT APP CONFIG
# -------------------------
st.set_page_config(
    page_title="My Hugging Face Chatbot", 
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Chatbot")
st.markdown("Chat with various AI models")

# -------------------------
# SIDEBAR CONFIGURATION
# -------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Models that work well with text generation
    MODEL_OPTIONS = {
        "Mistral 7B": "mistralai/Mistral-7B-Instruct-v0.3",
        "Zephyr 7B": "HuggingFaceH4/zephyr-7b-beta",
        "Llama 3 8B": "meta-llama/Meta-Llama-3-8B-Instruct",
    }
    
    selected_model = st.selectbox("Choose Model:", list(MODEL_OPTIONS.keys()))
    MODEL_ID = MODEL_OPTIONS[selected_model]
    
    max_tokens = st.slider("Max Tokens", 50, 1000, 512)
    temperature = st.slider("Temperature", 0.1, 1.0, 0.7)

# -------------------------
# TEXT GENERATION CLIENT
# -------------------------
@st.cache_resource
def get_client():
    try:
        HF_TOKEN = st.secrets["HF_TOKEN"]
        return InferenceClient(token=HF_TOKEN)
    except Exception as e:
        st.error(f"❌ Failed to initialize client: {e}")
        return None

client = get_client()

# -------------------------
# CHAT MEMORY
# -------------------------
if "messages" not in st.session_state:
    st.session_state["messages = []

# Display chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# TEXT GENERATION APPROACH
# -------------------------
def generate_response(messages, model_id, max_tokens=512, temperature=0.7):
    """Generate response using text generation"""
    # Format conversation for the model
    conversation = ""
    for msg in messages:
        if msg["role"] == "user":
            conversation += f"<|user|>\n{msg['content']}</s>\n"
        elif msg["role"] == "assistant":
            conversation += f"<|assistant|>\n{msg['content']}</s>\n"
    
    # Add the current prompt
    conversation += "<|assistant|>\n"
    
    # Generate response
    response = client.text_generation(
        prompt=conversation,
        model=model_id,
        max_new_tokens=max_tokens,
        temperature=temperature,
        stream=False
    )
    
    return response.strip()

user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ Thinking...")
        
        try:
            # Try text generation approach
            response = generate_response(
                st.session_state["messages"],
                MODEL_ID,
                max_tokens,
                temperature
            )
            
            message_placeholder.markdown(response)
            st.session_state["messages"].append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state["messages"].append({"role": "assistant", "content": error_msg})
