import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Online AI Chatbot")

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "mistralai/mistral-7b-instruct:free"  # ✅ Free online model

st.markdown("Chat using **Mistral-7B Free Model** 🌍")

if "history" not in st.session_state:
    st.session_state.history = []

def ask_ai(message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠️ API Error: {response.text}"

user_input = st.text_input("You:", "")

if st.button("Send"):
    output = ask_ai(user_input)
    st.session_state.history.append(("🧍 You", user_input))
    st.session_state.history.append(("🤖 AI", output))

for role, msg in st.session_state.history:
    st.write(f"**{role}:** {msg}")
