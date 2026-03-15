import streamlit as st
import pandas as pd
import plotly.express as px
from components.sidebar import render_sidebar
from database.supabase_client import get_progress_data
from utils.style import apply_custom_styles

# Page configuration
st.set_page_config(page_title="Dashboard | FitTrack", page_icon="📊", layout="wide")
apply_custom_styles()

def show_dashboard():
    # Require authentication
    if not st.session_state.get('user'):
        st.warning("Please log in to view your dashboard.")
        st.stop()
        
    render_sidebar()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(88, 166, 255, 0.1) 0%, rgba(13, 17, 23, 0) 100%); 
                padding: 2rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.2); margin-bottom: 2rem;">
        <h1 style="color: #58a6ff; margin-bottom: 0;">Your Progress Dashboard 📊</h1>
        <p style="color: #8b949e; font-size: 1.1rem; margin-top: 0.5rem;">Overview of your recent physical changes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state['user']['id']
    data = get_progress_data(user_id)
    
    if not data:
        st.info("No progress data available. Head over to the Progress Tracker to add your first entry!")
        return
        
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Latest stats
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    cols = st.columns(4)
    with cols[0]:
        st.markdown('<div data-testid="metric-container">', unsafe_allow_html=True)
        st.metric("Current Weight", f"{latest.get('weight', 0)} kg", delta=f"{round(latest.get('weight', 0) - prev.get('weight', 0), 2)} kg" if len(df) > 1 else None, delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<div data-testid="metric-container">', unsafe_allow_html=True)
        st.metric("Chest", f"{latest.get('chest', '--')} cm")
        st.markdown('</div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('<div data-testid="metric-container">', unsafe_allow_html=True)
        st.metric("Waist", f"{latest.get('waist', '--')} cm")
        st.markdown('</div>', unsafe_allow_html=True)
    with cols[3]:
        st.markdown('<div data-testid="metric-container">', unsafe_allow_html=True)
        st.metric("Biceps", f"{latest.get('biceps', '--')} cm")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    
    # Weight Progress Chart
    st.subheader("Weight Trend")
    fig = px.area(df, x='date', y='weight', markers=True, 
                  template="plotly_dark", 
                  title="Weight Progress Over Time",
                  color_discrete_sequence=["#58a6ff"])
    
    fig.update_traces(fillcolor='rgba(88, 166, 255, 0.2)')
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    show_dashboard()
