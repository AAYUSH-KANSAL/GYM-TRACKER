import streamlit as st
import pandas as pd
from components.sidebar import render_sidebar
from database.supabase_client import get_supabase
from utils.style import apply_custom_styles

st.set_page_config(page_title="Workout Planner | FitTrack", page_icon="🏋️‍♀️", layout="wide")
apply_custom_styles()

def fetch_workouts(user_id):
    supabase = get_supabase()
    if not supabase: return []
    try:
        response = supabase.table("workouts").select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception:
        return []

def add_workout(user_id, day, exercise, sets, reps):
    supabase = get_supabase()
    if not supabase: return False
    try:
        supabase.table("workouts").insert({
            "user_id": user_id, "day": day, "exercise": exercise, "sets": sets, "reps": reps
        }).execute()
        return True
    except Exception:
        return False

def delete_workout(workout_id):
    supabase = get_supabase()
    if not supabase: return False
    try:
        supabase.table("workouts").delete().eq("id", workout_id).execute()
        return True
    except Exception:
        return False

def show_workout_planner():
    if not st.session_state.get('user'):
        st.warning("Please log in to manage your workouts.")
        st.stop()
        
    render_sidebar()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(88, 166, 255, 0.1) 0%, rgba(13, 17, 23, 0) 100%); 
                padding: 2rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.2); margin-bottom: 2rem;">
        <h1 style="color: #58a6ff; margin-bottom: 0;">Workout Planner 🏋️‍♀️</h1>
        <p style="color: #8b949e; font-size: 1.1rem; margin-top: 0.5rem;">Plan and organize your weekly splits.</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state['user']['id']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Add Exercise")
        with st.form("add_workout_form", clear_on_submit=True):
            day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            exercise = st.text_input("Exercise Name (e.g., Barbell Bench Press)")
            sets = st.number_input("Sets", min_value=1, max_value=20, step=1, value=3)
            reps = st.number_input("Reps", min_value=1, max_value=100, step=1, value=10)
            
            submitted = st.form_submit_button("Add to Routine", use_container_width=True)
            if submitted:
                if exercise:
                    if add_workout(user_id, day, exercise, sets, reps):
                        st.success("Added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add exercise. Database connection issue.")
                else:
                    st.warning("Exercise name cannot be empty.")
                    
    with col2:
        st.markdown("### Your Weekly Routine")
        
        workouts = fetch_workouts(user_id)
        if workouts:
            df = pd.DataFrame(workouts)
            
            days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            df['day'] = pd.Categorical(df['day'], categories=days_order, ordered=True)
            df = df.sort_values(['day', 'id'])
            
            for day in days_order:
                day_data = df[df['day'] == day]
                if not day_data.empty:
                    st.markdown(f"#### {day}")
                    # Using columns to display grid
                    for _, row in day_data.iterrows():
                        cols = st.columns([4, 1, 1, 1])
                        cols[0].write(f"**{row['exercise']}**")
                        cols[1].write(f"{row['sets']} sets")
                        cols[2].write(f"{row['reps']} reps")
                        if cols[3].button("🗑️", key=f"del_{row['id']}", help="Delete"):
                            delete_workout(row['id'])
                            st.rerun()
                    st.divider()
        else:
            st.info("Your weekly routine is empty! Start adding exercises on the left.")

if __name__ == "__main__":
    show_workout_planner()
