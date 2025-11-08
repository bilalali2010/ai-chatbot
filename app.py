import streamlit as st
from huggingface_hub import InferenceClient

# -------------------------
# STREAMLIT APP CONFIG
# -------------------------
st.set_page_config(page_title="My Hugging Face Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")
st.write("Ask me anything and I'll reply using my Hugging Face model.")

# -------------------------
# HUGGING FACE CLIENT
# -------------------------
HF_TOKEN = st.secrets["HF_TOKEN"]  # Add HF_TOKEN in Streamlit Secrets
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"  # You can replace with your own

client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

# -------------------------
# CHAT MEMORY
# -------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------------
# USER INPUT
# -------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Get AI response
    try:
        completion = client.chat_completion(
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]],
            max_tokens=200
        )
        response = completion.choices[0].message["content"]
    except Exception as e:
        response = f"❌ Error: {e}"

    # Add AI response to history
    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
