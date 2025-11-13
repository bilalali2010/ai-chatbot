import streamlit as st
import requests
import os
import html

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="ChatGPT-Style AI Chat", page_icon="🤖", layout="wide")

# -------------------------
# Styles (ChatGPT-like)
# -------------------------
st.markdown("""
<style>
.chat-wrapper {display:flex;gap:24px;align-items:flex-start;}
.left-col {width:260px;min-width:220px;}
.main-col {flex:1;display:flex;flex-direction:column;height:80vh;}
#chatbox {background:#fff;border-radius:12px;padding:18px;
box-shadow:0 1px 3px rgba(0,0,0,0.06);overflow-y:auto;flex:1 1 auto;
border:1px solid #e6e6e6;}
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
st.sidebar.markdown("Model: **Gemma 7B Free (OpenRouter)**")
st.sidebar.markdown("---")
st.sidebar.markdown("Add your key in Streamlit Secrets:\n\n`OPENROUTER_API_KEY = sk-or-xxxxxx`")

# -------------------------
# API setup
# -------------------------
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "google/gemma-7b-it:free"

if not API_KEY:
    st.sidebar.error("❌ OPENROUTER_API_KEY missing in Streamlit Secrets.")
    st.stop()

# -------------------------
# Initialize / sanitize session state
# -------------------------
if "history" not in st.session_state or not isinstance(st.session_state.history, list):
    st.session_state.history = []

# Convert old string entries to dicts
new_history = []
for item in st.session_state.history:
    if isinstance(item, dict) and "role" in item and "content" in item:
        new_history.append(item)
    else:
        # treat plain strings as user messages
        new_history.append({"role": "user", "content": str(item)})
st.session_state.history = new_history

# Ensure a system prompt exists at top
if not st.session_state.history or st.session_state.history[0].get("role") != "system":
    st.session_state.history.insert(0, {
        "role": "system",
        "content": "You are a smart and factual assistant."
    })

# -------------------------
# API call
# -------------------------
def ask_ai():
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"model": MODEL_NAME, "messages": st.session_state.history}
    try:
        r = requests.post(API_URL, headers=headers, json=data, timeout=120)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"⚠️ API Error {r.status_code}: {r.text}"
    except Exception as e:
        return f"⚠️ Network error: {str(e)}"

# -------------------------
# Display chat
# -------------------------
chat_box = st.empty()

def render_chat():
    html_code = "<div id='chatbox'>"
    for msg in st.session_state.history:
        if not isinstance(msg, dict):
            continue
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "system":
            continue
        role_class = "user" if role == "user" else "bot"
        avatar = "👤" if role == "user" else "🤖"
        html_code += f"<div class='msg-row {role_class}'><div class='avatar {role_class}'>{avatar}</div><div class='bubble {role_class}'>{html.escape(content)}</div></div>"
    html_code += "</div><script>document.getElementById('chatbox').scrollTop=document.getElementById('chatbox').scrollHeight;</script>"
    chat_box.markdown(html_code, unsafe_allow_html=True)

render_chat()

# -------------------------
# Input section
# -------------------------
with st.form("chat_input", clear_on_submit=True):
    user_msg = st.text_area("You:", placeholder="Type your message...", height=60)
    send_btn = st.form_submit_button("Send")

if send_btn and user_msg.strip():
    st.session_state.history.append({"role": "user", "content": user_msg.strip()})
    render_chat()
    with st.spinner("🤖 Thinking..."):
        reply = ask_ai()
    st.session_state.history.append({"role": "assistant", "content": reply})
    render_chat()
