import streamlit as st
from huggingface_hub import InferenceClient
import time

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot - Conversational")

# Use conversational interface instead
@st.cache_resource
def get_client():
    return InferenceClient(token=st.secrets["HF_TOKEN"])

client = get_client()

# Models that support conversational task
MODEL_OPTIONS = {
    "Mistral 7B": "mistralai/Mistral-7B-Instruct-v0.3",
    "Llama 3 8B": "meta-llama/Meta-Llama-3-8B-Instruct",
    "Zephyr 7B": "HuggingFaceH4/zephyr-7b-beta"
}

with st.sidebar:
    st.header("⚙️ Settings")
    selected_model = st.selectbox("Choose Model:", list(MODEL_OPTIONS.keys()))
    MODEL_ID = MODEL_OPTIONS[selected_model]
    
    max_tokens = st.slider("Response Length", 100, 1000, 500)
    temperature = st.slider("Creativity", 0.1, 1.0, 0.7)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Use chat completion (conversational)
            completion = client.chat_completion(
                model=MODEL_ID,
                messages=st.session_state.messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=False
            )
            
            response = completion.choices[0].message.content
            
            # Stream response
            display_text = ""
            words = response.split()
            for word in words:
                display_text += word + " "
                message_placeholder.markdown(display_text + "▌")
                time.sleep(0.03)
            
            message_placeholder.markdown(display_text)
            st.session_state.messages.append({"role": "assistant", "content": display_text.strip()})
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            message_placeholder.markdown(error_msg)

st.caption("Using Chat Completion API")
