import streamlit as st
import requests

st.set_page_config(page_title="AI Chatbot", page_icon="💬")
st.title("🤖 Ollama Cloud Chatbot")

API_KEY = "YOUR_OLLAMA_API_KEY"  # Replace this with your real key

def ask_ollama(prompt):
    url = "https://api.ollama.com/v1/generate"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"model": "llama3", "prompt": prompt}

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"⚠️ Error: {response.text}"
    except Exception as e:
        return f"❌ Connection error: {e}"

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("💬 You:", placeholder="Type your question...")

if st.button("Send"):
    if user_input.strip():
        st.session_state.history.append(("🧍 You", user_input))
        reply = ask_ollama(user_input)
        st.session_state.history.append(("🤖 AI", reply))

for role, message in st.session_state.history:
    st.markdown(f"**{role}:** {message}")
