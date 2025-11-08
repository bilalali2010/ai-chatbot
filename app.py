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
st.markdown("Chat with various AI models powered by Hugging Face")

# -------------------------
# SIDEBAR CONFIGURATION
# -------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Use FREE and accessible models
    MODEL_OPTIONS = {
        "Mistral 7B Instruct": "mistralai/Mistral-7B-Instruct-v0.3",
        "Zephyr 7B Beta": "HuggingFaceH4/zephyr-7b-beta",
        "OpenHermes 2.5": "teknium/OpenHermes-2.5-Mistral-7B",
        "Microsoft Phi-3 Mini": "microsoft/Phi-3-mini-4k-instruct"
    }
    
    selected_model = st.selectbox(
        "Choose Model:",
        list(MODEL_OPTIONS.keys()),
        index=0
    )
    MODEL_ID = MODEL_OPTIONS[selected_model]
    
    st.divider()
    st.subheader("Model Parameters")
    max_tokens = st.slider("Max Tokens", 50, 1000, 512, 50)
    temperature = st.slider("Temperature", 0.1, 1.0, 0.7, 0.1)
    
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# -------------------------
# HUGGING FACE CLIENT - FIXED VERSION
# -------------------------
@st.cache_resource
def get_client():
    try:
        HF_TOKEN = st.secrets["HF_TOKEN"]
        # Initialize without specific model for chat completion
        return InferenceClient(token=HF_TOKEN)
    except Exception as e:
        st.error(f"❌ Failed to initialize client: {e}")
        return None

client = get_client()

# -------------------------
# CHAT MEMORY
# -------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # FIXED: Added missing quote and bracket

# Display previous messages
for msg in st.session_state["messages"]:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# -------------------------
# USER INPUT & RESPONSE
# -------------------------
user_input = st.chat_input("Type your message here...")

if user_input and user_input.strip():
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Get AI response
    if client is not None:
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            message_placeholder.markdown("⏳ Thinking...")
            
            try:
                # Prepare messages for the model
                messages = [{"role": m["role"], "content": m["content"]} 
                           for m in st.session_state["messages"]]
                
                # Generate response with explicit model parameter
                completion = client.chat_completion(
                    model=MODEL_ID,  # Explicitly specify model here
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=False
                )
                
                response = completion.choices[0].message["content"]
                
                # Stream the response for better UX
                full_response = ""
                message_placeholder.markdown("🔄 Generating response...")
                
                for chunk in response.split():
                    full_response += chunk + " "
                    time.sleep(0.02)
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                
                # Add AI response to history
                st.session_state["messages"].append({"role": "assistant", "content": full_response.strip()})
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(f"Detailed error: {e}")
                message_placeholder.markdown(error_msg)
                st.session_state["messages"].append({"role": "assistant", "content": error_msg})
