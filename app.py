import streamlit as st
import requests
import json
import time
import random

# Page configuration
st.set_page_config(
    page_title="Free AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stChatMessage {
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .success-box {
        padding: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today? 🤖"}
    ]
if "api_working" not in st.session_state:
    st.session_state.api_working = True

# Title
st.markdown('<h1 class="main-header">🤖 Free AI Chatbot</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    model_choice = st.radio(
        "Choose AI Model:",
        ["HuggingFace API", "Smart Assistant", "Creative Writer"]
    )
    
    st.markdown("---")
    st.markdown("### 💡 Tips:")
    st.info("- HuggingFace API may take 20-30 seconds to load initially")
    st.info("- If API fails, it auto-switches to local smart responses")
    st.info("- No API key required for basic usage")
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat history cleared! How can I help you? 💫"}
        ]
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# AI Response Functions
def get_huggingface_response(user_input, retry_count=0):
    """Get response from Hugging Face Inference API with retry logic"""
    try:
        # Using a reliable model
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        payload = {
            "inputs": user_input,
            "parameters": {
                "max_length": 150,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9,
                "repetition_penalty": 1.1
            },
            "options": {
                "wait_for_model": True,
                "use_cache": True
            }
        }
        
        response = requests.post(API_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # Clean up the response
                if user_input in generated_text:
                    generated_text = generated_text.replace(user_input, '').strip()
                return generated_text if generated_text else "I understand! What else would you like to know?"
            return "Interesting! Tell me more about that."
            
        elif response.status_code == 503 and retry_count < 3:
            # Model is loading, wait and retry
            time.sleep(10)
            return get_huggingface_response(user_input, retry_count + 1)
            
        else:
            st.session_state.api_working = False
            return None
            
    except Exception as e:
        st.session_state.api_working = False
        return None

def get_smart_response(user_input):
    """Smart local responses for when API is unavailable"""
    user_input_lower = user_input.lower()
    
    # Greetings
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'hola']):
        return "Hello! 👋 I'm your AI assistant. How can I help you today?"
    
    # Questions about AI
    elif any(word in user_input_lower for word in ['what are you', 'who are you']):
        return "I'm an AI chatbot running on Streamlit! I can help answer questions, chat, and assist with various tasks. 🤖"
    
    # Help requests
    elif any(word in user_input_lower for word in ['help', 'support', 'problem']):
        return "I'm here to help! You can ask me questions, request information, or just chat with me. What do you need assistance with?"
    
    # Technical questions
    elif any(word in user_input_lower for word in ['python', 'code', 'programming']):
        return "I can help with programming concepts! Python is a great language for beginners and experts alike. 🐍"
    
    # Fun responses
    elif any(word in user_input_lower for word in ['joke', 'funny', 'laugh']):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
            "Why did the AI cross the road? To optimize the shortest path! 🚦",
            "What's a computer's favorite snack? Microchips! 🍟"
        ]
        return random.choice(jokes)
    
    # Weather
    elif any(word in user_input_lower for word in ['weather', 'temperature', 'rain']):
        return "I don't have real-time weather data, but I recommend checking a weather service for accurate forecasts! ☀️"
    
    # Default intelligent responses
    else:
        responses = [
            f"That's interesting! Regarding '{user_input}', could you tell me more about what you're looking for?",
            f"I understand you're asking about {user_input}. What specific aspect would you like me to focus on?",
            f"Thanks for sharing that! I'd be happy to discuss {user_input}. What would you like to know specifically?",
            f"That's a great topic! About {user_input}, is there something particular you'd like me to help with?",
            f"I see you're interested in {user_input}. Could you provide more details so I can assist you better?"
        ]
        return random.choice(responses)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = None
            
            # Try HuggingFace API first if it's working
            if st.session_state.api_working and model_choice == "HuggingFace API":
                response = get_huggingface_response(prompt)
            
            # If API failed or not chosen, use smart responses
            if response is None:
                if model_choice == "Creative Writer":
                    response = f"✨ As a creative writer, I find '{prompt}' quite inspiring! Let me craft something unique about this topic..."
                else:
                    response = get_smart_response(prompt)
            
            # Display response
            st.markdown(response)
            
            # Show status
            if not st.session_state.api_working and model_choice == "HuggingFace API":
                st.warning("🔧 Using smart responses while API loads. This is normal!")
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer with status
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.session_state.api_working:
        st.success("✅ System Status: All features working!")
    else:
        st.info("🔄 System Status: Using enhanced local responses")
    
    st.markdown("**Powered by Streamlit** 🤖 | ⭐ Star on GitHub if you like it!")

    # Add a refresh button
    if st.button("🔄 Check API Status"):
        st.session_state.api_working = True
        st.rerun()
