import streamlit as st
import requests
import time

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot with Google Gemma")

HF_TOKEN = st.secrets["HF_TOKEN"]
# Try Google Gemma which might be more available
MODEL_ID = "google/gemma-7b-it"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.chat_message("user").write(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Generating response...")
        
        try:
            # Simple prompt for Gemma
            chat_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            full_prompt = f"{chat_history}\nuser: {prompt}\nassistant:"
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 400,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    answer = result[0].get('generated_text', '').strip()
                    
                    # Extract assistant response
                    if "assistant:" in answer:
                        answer = answer.split("assistant:")[-1].strip()
                    
                    if answer:
                        # Stream display
                        display_text = ""
                        for word in answer.split():
                            display_text += word + " "
                            message_placeholder.markdown(display_text + "▌")
                            time.sleep(0.03)
                        
                        message_placeholder.markdown(display_text)
                        st.session_state.messages.extend([
                            {"role": "user", "content": prompt},
                            {"role": "assistant", "content": display_text.strip()}
                        ])
                    else:
                        message_placeholder.markdown("🔄 Model is loading. Please wait 30 seconds and try again.")
                else:
                    message_placeholder.markdown("❌ No response from model. The model might be loading.")
            else:
                message_placeholder.markdown(f"❌ API Error {response.status_code}. Please try again.")
                
        except Exception as e:
            message_placeholder.markdown(f"❌ Error: {str(e)}")

st.caption("Using Google Gemma 7B")
