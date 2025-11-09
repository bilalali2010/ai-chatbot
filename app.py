import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Online AI Chatbot")

API_KEY = os.getenv("HF_TOKEN")

HF_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"  # Free model

def ask_ai(prompt):
    url = "https://router.huggingface.co/hf-inference"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": HF_MODEL,
        "inputs": prompt
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        return data
    return f"⚠️ API Error: {response.text}"

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", placeholder="Ask something...")

if st.button("Send"):
    if user_input.strip():
        st.session_state.history.append(("🧍 You", user_input))
        reply = ask_ai(user_input)
        st.session_state.history.append(("🤖 AI", reply))

for role, message in st.session_state.history:
    st.markdown(f"**{role}:** {message}")
