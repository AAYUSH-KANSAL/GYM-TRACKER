import streamlit as st
import os
from groq import Groq
from components.sidebar import render_sidebar
from utils.style import apply_custom_styles

st.set_page_config(page_title="AI Coach | FitTrack", page_icon="🤖", layout="wide")
apply_custom_styles()

def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def show_ai_coach():
    if not st.session_state.get('user'):
        st.warning("Please log in to chat with the AI Coach.")
        st.stop()
        
    render_sidebar()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(88, 166, 255, 0.1) 0%, rgba(13, 17, 23, 0) 100%); 
                padding: 2rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.2); margin-bottom: 2rem;">
        <h1 style="color: #58a6ff; margin-bottom: 0;">AI Fitness Coach 🤖</h1>
        <p style="color: #8b949e; font-size: 1.1rem; margin-top: 0.5rem;">Chat with your personal AI trainer powered by Groq.</p>
    </div>
    """, unsafe_allow_html=True)
    
    client = get_groq_client()
    if not client:
        st.error("Groq API key is missing. Please check your .env file.")
        st.stop()
        
    user_data = st.session_state['user']
    user_profile = user_data.get('profile') or {}
    user_name = user_profile.get('name', 'Lifter')

    # Initialize chat history
    if "messages" not in st.session_state:
        system_prompt = f"You are a highly knowledgeable, motivating, and concise personal fitness trainer. Your client's name is {user_name}. Always be encouraging. Format your responses using markdown lists and bold text where appropriate for readability."
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        st.session_state.messages.append({"role": "assistant", "content": f"Hi {user_name}! I'm your AI Fitness Coach. What are we working on today? Need a workout split, diet advice, or form check tips?"})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask your coach anything..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("Coach is typing..."):
                try:
                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        temperature=0.7,
                        stream=True,
                    )
                    
                    for chunk in completion:
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")
                            
                    message_placeholder.markdown(full_response)
                except Exception as e:
                    st.error(f"Error communicating with AI: {e}")
                    full_response = "Sorry, I'm having trouble connecting right now."
                    message_placeholder.markdown(full_response)
                    
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    show_ai_coach()
