import streamlit as st
from huggingface_hub import InferenceClient
import time

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# Simple client initialization
@st.cache_resource
def get_client():
    return InferenceClient(token=st.secrets["HF_TOKEN"])

client = get_client()

# Use a model that's known to work
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Simple prompt format
            conversation = ""
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    conversation += f"User: {msg['content']}\n"
                else:
                    conversation += f"Assistant: {msg['content']}\n"
            
            conversation += "Assistant:"
            
            # Generate response
            response = client.text_generation(
                prompt=conversation,
                model=MODEL_ID,
                max_new_tokens=500,
                temperature=0.7
            )
            
            # Display response
            clean_response = response.strip()
            display_text = ""
            for char in clean_response:
                display_text += char
                message_placeholder.markdown(display_text + "▌")
                time.sleep(0.01)
            
            message_placeholder.markdown(display_text)
            st.session_state.messages.append({"role": "assistant", "content": display_text})
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            message_placeholder.markdown(error_msg)
