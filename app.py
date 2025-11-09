import streamlit as st
import requests
import json

# -----------------------------
# ⚙️ PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Ollama AI Chatbot", page_icon="🦙", layout="centered")

# -----------------------------
# 🎨 CUSTOM CSS
# -----------------------------
st.markdown("""
    <style>
    body {background-color: #F8F9FA;}
    .chat-bubble-user {
        background-color: #DCF8C6; padding:10px; border-radius:10px;
        margin-bottom:10px; max-width:80%; margin-left:auto;
    }
    .chat-bubble-bot {
        background-color: #E9ECEF; padding:10px; border-radius:10px;
        margin-bottom:10px; max-width:80%; margin-right:auto;
    }
    .chat-container {max-height: 500px; overflow-y: auto;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# 🔑 API CONFIG
# -----------------------------
API_KEY = st.secrets["OLLAMA_API_KEY"]
API_URL = "https://api.ollama.cloud/v1/chat/completions"

# -----------------------------
# 🧠 MODEL SETTINGS
# -----------------------------
MODEL_NAME = "llama3:8b"
  # Change to mistral / phi3 / gemma / codellama / etc.

# -----------------------------
# 💾 SESSION MEMORY
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# 🏷️ HEADER
# -----------------------------
st.markdown("<h1 style='text-align:center;'>🦙 Ollama AI Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Powered by Ollama API & Streamlit Cloud</p>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# 💬 INPUT AREA
# -----------------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Your message:", placeholder="Type something here ...")
    send = st.form_submit_button("Send")

# -----------------------------
# 🤖 CHAT LOGIC
# -----------------------------
if send and user_input:
    with st.spinner("Thinking..."):
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": user_input}]
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = f"⚠️ Error: {response.text}"

    st.session_state.history.append({"user": user_input, "bot": reply})

# -----------------------------
# 💬 DISPLAY CHAT
# -----------------------------
st.markdown("### Conversation")
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for chat in reversed(st.session_state.history):
    st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {chat['user']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-bubble-bot'><b>Bot:</b> {chat['bot']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# 🗑️ CLEAR CHAT
# -----------------------------
if st.button("🗑️ Clear Chat"):
    st.session_state.history = []
    st.rerun()

# -----------------------------
# ⚙️ FOOTER
# -----------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:gray;'>Made with ❤️ using Streamlit & Ollama API | Model: Llama 3</p>",
    unsafe_allow_html=True
)
