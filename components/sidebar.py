import streamlit as st
from database.supabase_client import logout_user

def render_sidebar():
    """Renders the navigation sidebar for authenticated users."""
    with st.sidebar:
        st.markdown('<h2>🏃‍♂️ FitTrack Pro</h2>', unsafe_allow_html=True)
        st.divider()
        
        user_info = st.session_state.get('user', {})
        if user_info:
            profile = user_info.get('profile') or {}
            name = profile.get('name', 'Lifter')
            st.markdown(f"**Hi, {name}!**")
        
        st.markdown("### Navigation")
        
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
        st.page_link("pages/2_Progress_Tracker.py", label="Progress Tracker", icon="📈")
        st.page_link("pages/3_BMI_Calculator.py", label="BMI Calculator", icon="⚖️")
        st.page_link("pages/4_Calorie_Calculator.py", label="Calorie Calculator", icon="🔥")
        st.page_link("pages/5_Workout_Planner.py", label="Workout Planner", icon="🏋️‍♀️")
        st.page_link("pages/6_Diet_Planner.py", label="Diet Planner", icon="🥗")
        st.page_link("pages/7_AI_Coach.py", label="AI Coach", icon="🤖")

        st.divider()
        
        if st.button("Log Out", use_container_width=True, type="secondary"):
            logout_user()
            st.rerun()
