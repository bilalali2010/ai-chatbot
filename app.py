import streamlit as st
import requests
import os
import time

# ---------------------------- #
# 🧩 Basic Page Configuration
# ---------------------------- #
st.set_page_config(page_title="AI Chatbot | OpenRouter", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        .chat-message {
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 8px;
            line-height: 1.5;
            font-size: 16px;
        }
        .user {
            background-color: #DCF8C6;
            text-align: right;
        }
        .bot {
            background-color: #F1F0F0;
            text-align: left;
        }
        .chat-container {
            max-height: 75vh;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 12px;
            background-color: #fff;
        }
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: white;
            padding: 16px;
            box-shadow: 0 -3px 10px rgba(0, 0, 0, 0.1);
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 1px solid #ccc;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Professional AI Chatbot")
st.caption("Powered by OpenRouter — using **LLaMA 3 (Free)** 🌍")

# ---------------------------- #
# 🔑 API Configuration
# ---------------------------- #
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "meta-llama/llama-3-8b-instruct:free"

# ---------------------------- #
# 💬 Chat History
# ---------------------------- #
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------- #
# 🚀 AI Function
# ---------------------------- #
def ask_ai(message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": message}]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠️ API Error {response.status_code}: {response.text}"

# ---------------------------- #
# 🧠 Chat Display
# ---------------------------- #
chat_placeholder = st.container()

with chat_placeholder:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for role, msg in st.session_state.history:
        if role == "user":
            st.markdown(f'<div class="chat-message user"><b>🧍 You:</b> {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot"><b>🤖 AI:</b> {msg}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------- #
# 💬 Input at Bottom
# ---------------------------- #
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_input = st.text_input("Type your message...", "", key="user_input", label_visibility="collapsed")
col1, col2 = st.columns([0.85, 0.15])
with col2:
    send = st.button("Send 🚀")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------- #
# ⚡ Processing Logic
# ---------------------------- #
if send and user_input.strip() != "":
    with st.spinner("🤖 Thinking..."):
        time.sleep(0.8)  # Just for smooth UX
        ai_reply = ask_ai(user_input)

    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("bot", ai_reply))
    st.rerun()
