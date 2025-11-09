import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Online AI Chatbot")

API_KEY = os.getenv("HF_TOKEN")

HF_MODEL = "meta-llama/Llama-3.2-1B-Instruct"  # ✅ Works with HF router

def ask_ai(prompt):
    url = "https://router.huggingface.co/hf-inference"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": HF_MODEL,
        "input": prompt  # ✅ New router uses "input" instead of "inputs"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"]
            else:
                return json.dumps(data, indent=2)
        except Exception:
            return response.text

    return f"⚠️ API Error {response.status_code}: {response.text}"

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", placeholder="Ask anything...")

if st.button("Send"):
    if user_input.strip():
        st.session_state.history.append(("🧍 You", user_input))
        reply = ask_ai(user_input)
        st.session_state.history.append(("🤖 AI", reply))

for role, msg in st.session_state.history:
    st.markdown(f"**{role}:** {msg}")
