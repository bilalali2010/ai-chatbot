import streamlit as st
import requests
import json
import time

# -------------------------
# STREAMLIT APP CONFIG
# -------------------------
st.set_page_config(
    page_title="AI Chatbot", 
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Chatbot")
st.markdown("Chat with AI models using Hugging Face Inference API")

# -------------------------
# SIDEBAR CONFIGURATION
# -------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    
    MODEL_OPTIONS = {
        "Mistral 7B Instruct": "mistralai/Mistral-7B-Instruct-v0.3",
        "Zephyr 7B Beta": "HuggingFaceH4/zephyr-7b-beta",
        "Microsoft Phi-3 Mini": "microsoft/Phi-3-mini-4k-instruct",
        "Llama 3 8B": "meta-llama/Meta-Llama-3-8B-Instruct"
    }
    
    selected_model = st.selectbox(
        "Choose Model:",
        list(MODEL_OPTIONS.keys()),
        index=0
    )
    MODEL_ID = MODEL_OPTIONS[selected_model]
    
    st.divider()
    st.subheader("API Parameters")
    max_tokens = st.slider("Max Tokens", 50, 1000, 512, 50)
    temperature = st.slider("Temperature", 0.1, 1.0, 0.7, 0.1)
    top_p = st.slider("Top-P", 0.1, 1.0, 0.9, 0.1)
    
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -------------------------
# HUGGING FACE API SETUP
# -------------------------
HF_TOKEN = st.secrets["HF_TOKEN"]
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# -------------------------
# CHAT MEMORY
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# IMPROVED API QUERY FUNCTION
# -------------------------
def query_huggingface(prompt, max_tokens=512, temperature=0.7, top_p=0.9):
    """Query Hugging Face Inference API with proper error handling"""
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "do_sample": True,
            "return_full_text": False
        },
        "options": {
            "wait_for_model": True,
            "use_cache": True
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # Handle different response formats
        if isinstance(result, list) and len(result) > 0:
            if 'generated_text' in result[0]:
                return result[0]['generated_text'].strip()
            else:
                # Try to extract text from any key
                return str(result[0]).strip()
        elif isinstance(result, dict):
            if 'generated_text' in result:
                return result['generated_text'].strip()
            else:
                return str(result).strip()
        else:
            return "Sorry, I couldn't generate a proper response."
            
    except requests.exceptions.RequestException as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

# -------------------------
# PROMPT FORMATTING FUNCTION
# -------------------------
def format_conversation(messages):
    """Format conversation for the model"""
    formatted_text = ""
    
    for msg in messages:
        if msg["role"] == "user":
            formatted_text += f"<|user|>\n{msg['content']}</s>\n"
        elif msg["role"] == "assistant":
            formatted_text += f"<|assistant|>\n{msg['content']}</s>\n"
    
    # Add the assistant prompt for the next response
    formatted_text += "<|assistant|>\n"
    return formatted_text

# -------------------------
# USER INPUT HANDLING
# -------------------------
user_input = st.chat_input("Type your message here...")

if user_input and user_input.strip():
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ Thinking...")
        
        try:
            # Format the entire conversation
            conversation_text = format_conversation(st.session_state.messages)
            
            # Get response from Hugging Face
            raw_response = query_huggingface(
                prompt=conversation_text,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            )
            
            # Clean up the response
            if raw_response.startswith("<|assistant|>"):
                response = raw_response.replace("<|assistant|>", "").strip()
            else:
                response = raw_response
            
            # Remove any trailing tags
            response = response.split('</s>')[0].strip()
            
            # Stream the response
            full_response = ""
            for char in response:
                full_response += char
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.01)
            
            message_placeholder.markdown(full_response)
            
            # Add to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"❌ Error generating response: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# -------------------------
# FOOTER
# -------------------------
st.divider()
st.caption("Built with Streamlit and Hugging Face 🤗")
