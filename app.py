import streamlit as st
import requests
import os

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(page_title="ChatGPT-Style AI Chat", page_icon="🤖", layout="wide")

# -------------------------
# Custom Dark Theme CSS
# -------------------------
st.markdown("""
    <style>
        /* Global dark theme */
        body, .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        .css-1d391kg { color: white; }

        /* Chat bubble container */
        .chat-bubble {
            padding: 14px 18px;
            border-radius: 12px;
            margin-bottom: 12px;
            max-width: 80%;
            line-height: 1.5;
            font-size: 16px;
            word-wrap: break-word;
        }

        /* User bubble */
        .user-bubble {
            background-color: #238636;
            color: white;
            margin-left: auto;
        }

        /* AI bubble */
        .ai-bubble {
            background-color: #21262d;
            border: 1px solid #30363d;
            color: #c9d1d9;
        }

        /* Input box */
        textarea {
            background-color: #0d1117 !important;
            color: #c9d1d9 !important;
            border-radius: 8px !important;
            border: 1px solid #30363d !important;
        }

        /* Send button */
        button[kind="primary"] {
            background-color: #238636 !important;
            color: white !important;
            border-radius: 6px !important;
        }
        button[kind="primary"]:hover {
            background-color: #2ea043 !important;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("🤖 AI Chat Settings")
st.sidebar.markdown("Model: **xAI: Grok 4.1 Fast**")
st.sidebar.markdown("---")

# -------------------------
# API setup
# -------------------------
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "x-ai/grok-4.1-fast:free"

if not API_KEY:
    st.sidebar.error("❌ OPENROUTER_API_KEY missing.")
    st.stop()

# -------------------------
# Session state
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": "You are a smart and factual assistant."}
    ]

chat_placeholder = st.empty()

# -------------------------
# API call
# -------------------------
def ask_ai():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"model": MODEL_NAME, "messages": st.session_state.history}

    try:
        r = requests.post(API_URL, headers=headers, json=data, timeout=180)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"⚠️ API Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"⚠️ Network error: {e}"

# -------------------------
# Chat render function
# -------------------------
def render_chat():
    with chat_placeholder.container():
        for msg in st.session_state.history:
            if msg["role"] == "system":
                continue

            if msg["role"] == "user":
                st.markdown(
                    f"<div class='chat-bubble user-bubble'>👤 <b>You:</b><br>{msg['content']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='chat-bubble ai-bubble'>🤖 <b>AI:</b><br>{msg['content']}</div>",
                    unsafe_allow_html=True
                )

# -------------------------
# Render chat
# -------------------------
render_chat()

# -------------------------
# Input form
# -------------------------
with st.form("chat_input", clear_on_submit=True):
    user_msg = st.text_area("Type your message here...", height=60)
    send_btn = st.form_submit_button("Send")

if send_btn and user_msg.strip():
    st.session_state.history.append({"role": "user", "content": user_msg.strip()})
    render_chat()

    with st.spinner("🤖 Thinking..."):
        reply = ask_ai()

    st.session_state.history.append({"role": "assistant", "content": reply})
    render_chat()
