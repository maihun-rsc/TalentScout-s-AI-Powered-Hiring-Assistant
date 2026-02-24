import streamlit as st
import os
from backend import HiringAssistantBackend
from dotenv import load_dotenv
from sentiment import analyze_sentiment

# Set up page configurations
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (UI Enhancement Bonus)
st.markdown("""
<style>
    .chat-bubble {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #2e6b8e;
        color: white;
        margin-left: auto;
    }
    .bot-bubble {
        background-color: #f1f0f0;
        color: black;
        margin-right: auto;
    }
    .title {
        text-align: center;
        color: #2e6b8e;
        font-family: 'Helvetica', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>TalentScout Hiring Assistant 💼</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Welcome! I'm TalentBot, here to understand your profile and skills.</p>", unsafe_allow_html=True)

# Sidebar for settings & Optional Enhancements
with st.sidebar:
    st.header("Settings & Options")
        
    st.markdown("---")
    st.write("**Bonus Features Enabled:**")
    st.checkbox("Multilingual Support ✅", value=True, disabled=True, help="Our model supports multiple languages. Just type in your language!")
    show_sentiment = st.checkbox("Show Sentiment Tracking", value=True, help="Track and display context and user tone.")
    
# Persona Selection Logic on Main Page
if "persona_selected" not in st.session_state:
    st.session_state.persona_selected = False
    st.session_state.selected_persona = "Lani"

if not st.session_state.persona_selected:
    st.markdown("<h3 style='text-align: center;'>Please select your Interviewer Persona to begin:</h3>", unsafe_allow_html=True)
    st.write("") # spacing
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Lani 👩🏻‍🦰\n\n(Balanced)", use_container_width=True):
            st.session_state.selected_persona = "Lani"
            st.session_state.persona_selected = True
            st.rerun()
    with col2:
        if st.button("Malik 🧔🏻‍♂️\n\n(Direct)", use_container_width=True):
            st.session_state.selected_persona = "Malik"
            st.session_state.persona_selected = True
            st.rerun()
    with col3:
        if st.button("Clara 👱🏻‍♀️\n\n(Chatty)", use_container_width=True):
            st.session_state.selected_persona = "Clara"
            st.session_state.persona_selected = True
            st.rerun()
            
    st.stop() # Wait for user input
    
# Initialize Backend
if "backend" not in st.session_state:
    # We initialize only once the persona is picked!
    st.session_state.backend = HiringAssistantBackend(persona=st.session_state.selected_persona)
    st.session_state.messages = [] 

if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    # Adding Initial Greeting (Dynamically customized per persona!)
    if st.session_state.selected_persona == "Malik":
        greeting = "I'm Malik, Hiring Manager at TalentScout. We're going to keep this highly efficient. Let's start with your Full Name."
    elif st.session_state.selected_persona == "Clara":
        greeting = "Hi there! 😊 I'm Clara, your hiring assistant today! I'm so excited to learn more about you. To get us started, could you share your Full Name with me?"
    else:
        greeting = "Hello. I am Lani, your hiring assistant for TalentScout. Let's begin the screening. Please provide your Full Name."
        
    st.session_state.messages = [{"role": "Assistant", "content": greeting}]
    # Sync with memory
    st.session_state.backend.chat_history.add_ai_message(greeting)

# Render Chat History
for msg in st.session_state.messages:
    if msg["role"] == "Assistant":
        st.chat_message("assistant").write(msg["content"])
    else:
        st.chat_message("user").write(msg["content"])

# User Input
if user_input := st.chat_input("Type your message here..."):
    # Calculate sentiment
    sent_info = None
    if show_sentiment:
        sent_info = analyze_sentiment(user_input)
        
    # Render user input
    st.session_state.messages.append({"role": "User", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
        if sent_info:
            st.markdown(f"<span style='font-size: 0.8em; color: {sent_info['color']};'>{sent_info['label']} (polarity: {sent_info['polarity']})</span>", unsafe_allow_html=True)
    
    # Show loading spinner while generating response
    with st.spinner("TalentBot is typing..."):
        # Process user message with LangChain
        response = st.session_state.backend.process_message(user_input)
        
    # Render bot response
    st.session_state.messages.append({"role": "Assistant", "content": response})
    st.chat_message("assistant").write(response)
