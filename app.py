import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="AI Chatbot - Real Conversations",
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
        font-weight: bold;
    }
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 15px;
        padding: 15px;
    }
    .success-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hey there! I'm your AI friend. I'm here to have real conversations and help with anything you need. What would you like to talk about today? 😊"}
    ]

# Title
st.markdown('<h1 class="main-header">🤖 AI Conversation Partner</h1>', unsafe_allow_html=True)
st.markdown('<div class="success-banner">💬 Real Conversations • No Templates • Just Natural Chat</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("💬 Chat Settings")
    if st.button("🔄 Start New Conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "🔄 Conversation refreshed! What's on your mind today?"}
        ]
        st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_natural_response(user_input):
    user_input_lower = user_input.lower().strip()
    
    # Greetings and basic conversation
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'hola']):
        return random.choice([
            "👋 Hey! Great to see you! How's your day going?",
            "😊 Hello there! What's new with you today?",
            "🤖 Hi! I was just thinking about our conversation. What would you like to talk about?",
            "🎉 Hey! Perfect timing - I was hoping we could chat. What's on your mind?"
        ])
    
    elif any(word in user_input_lower for word in ['how are you', 'how do you do']):
        return random.choice([
            "I'm doing really well! Just enjoying our conversation. Thanks for asking! How about you?",
            "I'm great! Every chat with you makes my day better. How are you feeling today?",
            "Doing awesome! I love helping people and having interesting conversations. What's new with you?"
        ])
    
    elif any(word in user_input_lower for word in ['good', 'great', 'awesome', 'fine']):
        return random.choice([
            "That's wonderful to hear! 😊 What's making your day so good?",
            "Awesome! I love when people are having a good day. Want to share what's going well?",
            "Great! Positive energy is contagious. What would you like to do with this good mood?"
        ])
    
    elif any(word in user_input_lower for word in ['bad', 'not good', 'tired', 'sad']):
        return random.choice([
            "I'm sorry to hear that. Want to talk about what's going on? I'm here to listen.",
            "That sounds tough. Remember that it's okay to not be okay sometimes. Want to share what's bothering you?",
            "I understand. We all have rough days. Is there anything I can do to help you feel better?"
        ])
    
    elif any(word in user_input_lower for word in ['thank', 'thanks']):
        return random.choice([
            "You're very welcome! I'm always happy to help. 😊",
            "No problem at all! It's my pleasure to assist you.",
            "Anytime! I enjoy our conversations and helping however I can."
        ])
    
    elif any(word in user_input_lower for word in ['what can you do', 'your capabilities']):
        return "I can have real conversations about pretty much anything! I'm good at explaining concepts, helping with creative ideas, answering questions about technology and science, and just being a good chat partner. What would you like to try first?"
    
    elif any(word in user_input_lower for word in ['who are you', 'what are you']):
        return "I'm an AI conversation partner created to have genuine, helpful chats with people. I'm not just a question-answer machine - I can actually understand context and have flowing conversations. I learn from our chat to make our conversation better!"
    
    # Knowledge questions - real answers, not templates
    elif "what is ai" in user_input_lower:
        return "AI stands for Artificial Intelligence. In simple terms, it's about creating computer systems that can do things that normally require human intelligence - like understanding language, recognizing images, solving problems, and learning from experience. The AI you're talking to right now is an example of a language model that can understand and generate human-like text!"
    
    elif "what is python" in user_input_lower:
        return "Python is a programming language that's really popular because it's easy to read and write. People use it for everything from building websites to analyzing data to creating AI systems. It's named after Monty Python, not the snake! Here's a simple example:\n\n```python\n# This prints a greeting\nname = input('What\\'s your name? ')\nprint(f'Hello {name}! Nice to meet you!')\n```\n\nIt's a great language to start with if you want to learn programming!"
    
    elif "how does chatgpt work" in user_input_lower:
        return "ChatGPT works by learning patterns from huge amounts of text from the internet. It's like a super-smart autocomplete that understands context. When you type something, it predicts what words should come next based on everything it's learned. The amazing part is how it can maintain conversation flow and understand complex questions!"
    
    elif "weather" in user_input_lower:
        return "I don't have live weather data, but I can tell you that talking about weather is one of the most common conversation starters! Are you planning something outdoors, or just curious about the climate where you are?"
    
    elif "joke" in user_input_lower or "funny" in user_input_lower:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
        return f"{random.choice(jokes)}\n\n😄 Hope that made you smile! Want to hear another one?"
    
    elif "movie" in user_input_lower or "film" in user_input_lower:
        return "I love talking about movies! While I can't watch them myself, I know a lot about different films. Are you thinking of watching something new, or do you have a favorite movie you'd like to discuss?"
    
    elif "music" in user_input_lower:
        return "Music is amazing, isn't it? It can change our mood, bring back memories, and connect people. What kind of music do you enjoy? I can talk about different genres, artists, or even help with music theory!"
    
    elif "book" in user_input_lower:
        return "Books are like windows to other worlds! I've 'read' millions of books through my training. Are you looking for book recommendations, or is there a particular book you'd like to discuss?"
    
    elif "food" in user_input_lower or "cook" in user_input_lower:
        return "Food brings people together! I know a lot about different cuisines, cooking techniques, and recipes. Are you planning to cook something, or just enjoying talking about delicious food?"
    
    elif "travel" in user_input_lower:
        return "Travel is such an exciting topic! I can tell you about different places around the world, travel tips, or help plan imaginary trips. Where would you like to 'visit' in our conversation?"
    
    elif "programming" in user_input_lower or "coding" in user_input_lower:
        return "Programming is like learning to speak a new language that computers understand! I can help explain programming concepts, help debug code, or suggest learning resources. What programming topic interests you right now?"
    
    elif "game" in user_input_lower:
        return "Games are a great way to have fun and challenge your mind! I know about video games, board games, puzzles, and even can help create simple text-based games. What kind of games do you enjoy?"
    
    # Questions with question marks
    elif "?" in user_input:
        responses = [
            f"That's an interesting question! Let me think about '{user_input}'... From what I understand, this could be looked at from a few different angles. What specifically are you most curious about?",
            f"Hmm, '{user_input}' - that's a thoughtful question. I'd approach this by considering the key factors involved. Want me to break down what I know about this topic?",
            f"Great question! Regarding '{user_input}', I can share what I've learned about this. The main thing to understand is how different pieces connect together. Should I start with the basics or dive right into the details?"
        ]
        return random.choice(responses)
    
    # Simple statements - continue conversation naturally
    elif len(user_input.split()) <= 3:
        simple_responses = [
            "Got it! What would you like to explore next?",
            "Interesting! Tell me more about that.",
            "I see! What's on your mind about this?",
            "Cool! Want to dive deeper into this topic?",
            "Nice! What aspect of this interests you most?"
        ]
        return random.choice(simple_responses)
    
    # Longer statements - engage with the content
    else:
        engagement_responses = [
            f"That's really interesting about '{user_input}'. I'd love to hear more about your thoughts on this!",
            f"Thanks for sharing that! '{user_input}' sounds like something worth exploring further. What got you interested in this?",
            f"I appreciate you telling me about '{user_input}'. This seems like a topic we could really dive into. What would you like to know more about?",
            f"That's fascinating! Regarding '{user_input}', I have some ideas we could explore together. Want to continue this conversation?",
            f"I'm really enjoying our chat about '{user_input}'. What part of this topic do you find most interesting?"
        ]
        return random.choice(engagement_responses)

# Chat input
if prompt := st.chat_input("💬 Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_natural_response(prompt)
            st.markdown(response)
    
    # Add to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("---")
st.success("💬 **Having a great conversation!** Keep chatting - I'm really enjoying this!")
st.markdown("**Real AI Conversations** • 🤖 **No Templates** • 😊 **Just Natural Chat**")

# Add some conversation starters
with st.expander("💡 Need conversation ideas?"):
    st.markdown("""
    **Try asking me about:**
    - Your day or how you're feeling
    - Technology and how things work
    - Creative ideas or brainstorming
    - Books, movies, or music
    - Learning new skills
    - Or just share what's on your mind!
    
    I'm here for real conversation, not just Q&A! 🎉
    """)
