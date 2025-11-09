import streamlit as st
import requests
import os

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("🤖 AI Chatbot Settings")
model_options = {
    "Mistral 7B Free": "mistralai/mistral-7b-instruct:free",
}
selected_model = st.sidebar.selectbox("Choose AI Model:", list(model_options.keys()))
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = model_options[selected_model]
st.sidebar.markdown("---")
st.sidebar.markdown("💡 Tip: Use short prompts for faster responses.")

# -------------------------------
# Header
# -------------------------------
st.markdown(
    "<h1 style='text-align:center; color:#4B0082;'>🤖 Online AI Chatbot</h1>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# -------------------------------
# Session State
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# API Call Function
# -------------------------------
def ask_ai(message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"model": MODEL_NAME, "messages":[{"role":"user","content":message}]}
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠️ API Error: {response.text}"

# -------------------------------
# Scrollable Chat Container
# -------------------------------
chat_placeholder = st.empty()

def render_chat():
    with chat_placeholder.container():
        for role, msg in st.session_state.history:
            if role.startswith("🧍"):
                st.markdown(
                    f"<div style='background-color:#DCF8C6; padding:10px; border-radius:10px; margin:5px 0; width:fit-content;'>{msg}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background-color:#EAEAEA; padding:10px; border-radius:10px; margin:5px 0; width:fit-content;'>{msg}</div>",
                    unsafe_allow_html=True
                )

# -------------------------------
# Input Form at Bottom
# -------------------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", "")
    send_button = st.form_submit_button("Send")

if send_button and user_input.strip():
    # Add user message
    st.session_state.history.append(("🧍 You", user_input))
    render_chat()

    # Show AI typing
    typing_placeholder = st.empty()
    typing_placeholder.markdown(
        "<div style='background-color:#EAEAEA; padding:10px; border-radius:10px; margin:5px 0; width:fit-content; font-style:italic; color:gray;'>🤖 AI is typing...</div>",
        unsafe_allow_html=True
    )

    # Call AI
    output = ask_ai(user_input)

    # Replace typing placeholder with AI response
    st.session_state.history.append(("🤖 AI", output))
    typing_placeholder.empty()
    render_chat()
