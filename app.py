import streamlit as st
import requests
import os
import html

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="ChatGPT-Style AI Chat", page_icon="🤖", layout="wide")

# -------------------------
# Styles (ChatGPT-like UI)
# -------------------------
st.markdown("""
<style>
.chat-wrapper {display:flex;gap:24px;align-items:flex-start;}
.left-col {width:260px;min-width:220px;}
.main-col {flex:1;display:flex;flex-direction:column;height:80vh;}
#chatbox {
    background:#fff;border-radius:12px;padding:18px;
    box-shadow:0 1px 3px rgba(0,0,0,0.06);
    overflow-y:auto;flex:1 1 auto;
    border:1px solid #e6e6e6;
}
.msg-row {display:flex;gap:12px;margin-bottom:12px;align-items:flex-end;}
.msg-row.user {justify-content:flex-end;}
.avatar {width:36px;height:36px;border-radius:50%;text-align:center;
    line-height:36px;font-size:18px;}
.avatar.user {background:#DCF8C6;}
.avatar.bot {background:#EAEAEA;}
.bubble {max-width:78%;padding:12px 14px;border-radius:12px;
    font-size:14px;line-height:1.4;white-space:pre-wrap;
    box-shadow:0 1px 1px rgba(0,0,0,0.03);}
.bubble.user {background:#DCF8C6;border-bottom-right-radius:6px;}
.bubble.bot {background:#EAEAEA;border-bottom-left-radius:6px;}
.input-area {margin-top:12px;display:flex;gap:8px;align-items:center;}
.input-box {flex:1;}
.send-btn {background:#4B0082;color:white;border:none;
    padding:8px 14px;border-radius:8px;}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("🤖 AI Chat Settings")
st.sidebar.markdown("Model: **Llama 3.1 (Free)**")
st.sidebar.markdown("---")
st.sidebar.markdown("Add your key in Streamlit Secrets:\n\n`OPENROUTER_API_KEY = sk-or-xxxxxx`")

# -------------------------
# API setup
# -------------------------
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ⭐ BEST free model (stable, fast, reliable)
MODEL_NAME = "meta-llama/llama-3.1-8b-instruct:free"

if not API_KEY:
    st.sidebar.error("❌ OPENROUTER_API_KEY missing in Streamlit Secrets.")
    st.stop()

# -------------------------
# Session history
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": "You are a helpful AI assistant."}
    ]

chat_box = st.empty()

# -------------------------
# Render chat nicely
# -------------------------
def render_chat():
    html_code = "<div id='chatbox'>"
    for msg in st.session_state.history:
        if msg["role"] == "system":
            continue
        role = msg["role"]
        role_class = "user" if role == "user" else "bot"
        avatar = "👤" if role == "user" else "🤖"
        content = html.escape(msg["content"])

        html_code += f"""
        <div class='msg-row {role_class}'>
            <div class='avatar {role_class}'>{avatar}</div>
            <div class='bubble {role_class}'>{content}</div>
        </div>
        """
    html_code += """
    </div>
    <script>
    var box = document.getElementById('chatbox');
    box.scrollTop = box.scrollHeight;
    </script>
    """
    chat_box.markdown(html_code, unsafe_allow_html=True)

render_chat()

# -------------------------
# API Call
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
        r = requests.post(API_URL, headers=headers, json=data, timeout=120)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ API Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"⚠️ Network error: {str(e)}"

# -------------------------
# Input box
# -------------------------
with st.form("chat_input", clear_on_submit=True):
    user_msg = st.text_area("You:", placeholder="Type your message...", height=60)
    send_btn = st.form_submit_button("Send")

if send_btn and user_msg.strip():
    # Add user message
    st.session_state.history.append({"role": "user", "content": user_msg.strip()})
    render_chat()

    with st.spinner("🤖 Thinking..."):
        reply = ask_ai()

    # Add bot reply
    st.session_state.history.append({"role": "assistant", "content": reply})
    render_chat()
