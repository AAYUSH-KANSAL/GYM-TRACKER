import streamlit as st
from dotenv import load_dotenv

# Set up page layout and configuration FIRST, before any other Streamlit commands
st.set_page_config(
    page_title="Gym Progress Tracker",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# We will load styles and auth here later
from utils.style import apply_custom_styles
from components.auth import authentication_flow
from components.sidebar import render_sidebar

def main():
    apply_custom_styles()
    
    # Check if user is authenticated
    if 'user' not in st.session_state:
        st.session_state['user'] = None

    if st.session_state['user'] is None:
        # Hide sidebar completely if not logged in
        st.markdown("""
            <style>
                [data-testid="collapsedControl"] {display: none;}
                [data-testid="stSidebar"] {display: none;}
            </style>
        """, unsafe_allow_html=True)
        # User not logged in, show auth flow
        authentication_flow()
    else:
        # User logged in, render main layout
        render_sidebar()
        
        user_data = st.session_state['user']
        user_profile = user_data.get('profile') or {}
        username = user_profile.get('name', user_data.get('email', 'Lifter'))
        
        # Hero Section
        st.markdown(f"""
        <div class="hero-section">
            <h1 style="font-size: 4rem; margin-bottom: 1rem; background: -webkit-linear-gradient(45deg, #3fb950, #58a6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;">
                FitTrack Pro
            </h1>
            <h2 style="color: #f0f6fc; font-weight: 300; margin-bottom: 2rem;">Welcome back, {username}! 💪</h2>
            <p style="font-size: 1.25rem; color: #8b949e; max-width: 700px; margin: 0 auto; line-height: 1.6;">
                The only bad workout is the one that didn't happen. Tracking your progress is the first step toward your best self. 
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Daily Motivation
        quotes = [
            "Your only limit is you.",
            "Action is the foundational key to all success.",
            "What hurts today makes you stronger tomorrow.",
            "Motivation is what gets you started. Habit is what keeps you going.",
            "Success starts with self-discipline.",
            "Don't stop when you're tired. Stop when you're done.",
            "Fitness is not about being better than someone else. It's about being better than you were yesterday."
        ]
        import datetime
        daily_quote = quotes[datetime.datetime.now().day % len(quotes)]
        
        st.markdown(f"""
        <div class="quote-box">
            "{daily_quote}"
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="action-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3 style="margin-top:0; color: #58a6ff;">Analytics</h3>
                <p style="color: #8b949e; font-size: 0.95rem; min-height: 60px;">Deep dive into your progress charts and physical transformations.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Go to Dashboard", key="btn_dash", use_container_width=True):
                st.switch_page("pages/1_Dashboard.py")
                
        with col2:
            st.markdown("""
            <div class="action-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🏋️‍♂️</div>
                <h3 style="margin-top:0; color: #3fb950;">Workouts</h3>
                <p style="color: #8b949e; font-size: 0.95rem; min-height: 60px;">Manage your weekly splits and stay consistent with your routine.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Manage Workouts", key="btn_work", use_container_width=True):
                st.switch_page("pages/5_Workout_Planner.py")
                
        with col3:
            st.markdown("""
            <div class="action-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <h3 style="margin-top:0; color: #f1e05a;">AI Coach</h3>
                <p style="color: #8b949e; font-size: 0.95rem; min-height: 60px;">Ask your AI Coach for diet advice or customized lifting tips.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Chat with Coach", key="btn_coach", use_container_width=True):
                st.switch_page("pages/7_AI_Coach.py")
        
        st.divider()
        st.markdown("""
        <p style="text-align: center; color: #484f58; font-size: 0.8rem;">
            FITTRACK PRO v1.1 | Powered by Groq & Supabase
        </p>
        """, unsafe_allow_html=True)
        
if __name__ == "__main__":
    main()
