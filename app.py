import streamlit as st
import requests
import os

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="ChatGPT-Style AI Chat",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("🤖 AI Chat Settings")
st.sidebar.markdown("Model: **xAI: Grok 4.1**")
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

# Placeholder for chat messages
chat_placeholder = st.empty()


# -------------------------
# API call function
# -------------------------
def ask_ai():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": st.session_state.history
    }

    try:
        r = requests.post(API_URL, headers=headers, json=data, timeout=180)

        if r.status_code == 200:
            reply = r.json()["choices"][0]["message"]["content"].strip()
            return reply or "⚠️ Sorry, I could not generate a response."
        else:
            return f"⚠️ API Error {r.status_code}: {r.text}"

    except Exception as e:
        return f"⚠️ Network error: {e}"


# -------------------------
# Display chat
# -------------------------
def render_chat():
    with chat_placeholder.container():
        for msg in st.session_state.history:
            if msg["role"] == "system":
                continue
            if msg["role"] == "user":
                st.markdown(f"👤 **You:** {msg['content']}")
            elif msg["role"] == "assistant":
                st.markdown(f"🤖 **AI:** {msg['content']}")


# -------------------------
# Render chat first
# -------------------------
render_chat()

# -------------------------
# Input form at the bottom
# -------------------------
with st.form("chat_input", clear_on_submit=True):
    user_msg = st.text_area("Type your message here...", height=60)
    send_btn = st.form_submit_button("Send")

    if send_btn and user_msg.strip():
        # Add user message
        st.session_state.history.append(
            {"role": "user", "content": user_msg.strip()}
        )

        render_chat()

        # Get AI response
        with st.spinner("🤖 Thinking..."):
            reply = ask_ai()

        st.session_state.history.append(
            {"role": "assistant", "content": reply}
        )

        render_chat()
