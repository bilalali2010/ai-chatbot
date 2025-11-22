import streamlit as st
import requests
import os

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Z.ai Style Chatbot", page_icon="🤖", layout="wide")

# -------------------------
# Custom CSS (Light Theme)
# -------------------------
st.markdown("""
<style>

    /* Background */
    body, .stApp {
        background-color: #f5f7fa !important;
        font-family: "Segoe UI", sans-serif;
    }

    /* Center Layout */
    .center-container {
        display: flex;
        justify-content: center;
        text-align: center;
        padding-top: 60px;
    }

    /* Main Title */
    .main-title {
        font-size: 48px;
        font-weight: 700;
        color: #333;
        margin-bottom: 25px;
    }

    /* Chat box */
    .chat-box {
        background: white;
        padding: 20px 25px;
        width: 700px;
        border-radius: 14px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        margin: auto;
        border: 1px solid #eee;
    }

    /* Tool Buttons */
    .tool-row {
        margin-top: 20px;
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
    }

    .tool-btn {
        background: white;
        padding: 10px 18px;
        border-radius: 10px;
        border: 1px solid #ddd;
        cursor: pointer;
        font-size: 14px;
        transition: 0.2s;
        box-shadow: 0px 1px 4px rgba(0,0,0,0.06);
    }

    .tool-btn:hover {
        background: #eef1f5;
    }

    /* Chat Bubbles */
    .msg {
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 10px;
        max-width: 80%;
    }

    .user-msg {
        background: #dbeafe;
        margin-left: auto;
    }

    .bot-msg {
        background: #fff;
        border: 1px solid #eee;
        margin-right: auto;
    }

    /* Input box styling */
    textarea {
        border-radius: 12px !important;
        border: 1px solid #ddd !important;
        background: white !important;
    }

    /* Send button */
    button[kind="primary"] {
        background: #2563eb !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }

</style>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.markdown("### 🤖 Model: Grok 4.1 Fast")
st.sidebar.markdown("---")

# -------------------------
# API Info
# -------------------------
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "x-ai/grok-4.1-fast:free"

if not API_KEY:
    st.sidebar.error("❌ Missing OPENROUTER_API_KEY in secrets.")
    st.stop()

# -------------------------
# Session State
# -------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []


# -------------------------
# API Call
# -------------------------
def ask_ai():
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"model": MODEL, "messages": [{"role": "system", "content": "You are a helpful assistant."}] + st.session_state.chat}

    try:
        r = requests.post(API_URL, headers=headers, json=data)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return f"⚠️ API Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"⚠️ Network error: {e}"


# -------------------------
# MAIN UI
# -------------------------
st.markdown("<div class='center-container'><h1 class='main-title'>Hi, I'm Z.ai</h1></div>", unsafe_allow_html=True)

# Chat Box
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

# Input Form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("How can I help you today?")
    send = st.form_submit_button("Send")

if send and user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})
    bot_reply = ask_ai()
    st.session_state.chat.append({"role": "assistant", "content": bot_reply})

# Render messages
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(f"<div class='msg user-msg'>🙋‍♂️ {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='msg bot-msg'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Tool Buttons (bottom like screenshot)
st.markdown("""
<div class='tool-row'>
    <div class='tool-btn'>🌐 Web Search</div>
    <div class='tool-btn'>💡 Deep Think</div>
</div>

<div class='tool-row'>
    <div class='tool-btn'>📊 AI Slides</div>
    <div class='tool-btn'>🧩 Full-Stack</div>
    <div class='tool-btn'>🎨 Magic Design</div>
    <div class='tool-btn'>🔍 Deep Research</div>
    <div class='tool-btn'>💻 Write Code</div>
</div>
""", unsafe_allow_html=True)
