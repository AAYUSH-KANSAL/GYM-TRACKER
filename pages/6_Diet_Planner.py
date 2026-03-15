import streamlit as st
import datetime
import pandas as pd
from components.sidebar import render_sidebar
from database.supabase_client import get_supabase
from utils.style import apply_custom_styles

st.set_page_config(page_title="Diet Planner | FitTrack", page_icon="🥗", layout="wide")
apply_custom_styles()

def fetch_diets(user_id, day):
    supabase = get_supabase()
    if not supabase: return []
    try:
        response = supabase.table("diets").select("*").eq("user_id", user_id).eq("day", day).execute()
        return response.data
    except Exception:
        return []

def add_diet_entry(user_id, day, meal_type, food_items):
    supabase = get_supabase()
    if not supabase: return False
    try:
        supabase.table("diets").insert({
            "user_id": user_id, 
            "day": day, 
            "meal_type": meal_type, 
            "food_items": food_items
        }).execute()
        return True
    except Exception as e:
        print(e)
        return False

def delete_diet_entry(entry_id):
    supabase = get_supabase()
    if not supabase: return False
    try:
        supabase.table("diets").delete().eq("id", entry_id).execute()
        return True
    except Exception:
        return False

def show_diet_planner():
    if not st.session_state.get('user'):
        st.warning("Please log in to manage your diet.")
        st.stop()
        
    render_sidebar()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(46, 160, 67, 0.1) 0%, rgba(13, 17, 23, 0) 100%); 
                padding: 2rem; border-radius: 12px; border: 1px solid rgba(46, 160, 67, 0.2); margin-bottom: 2rem;">
        <h1 style="color: #3fb950; margin-bottom: 0;">Diet Planner 🥗</h1>
        <p style="color: #8b949e; font-size: 1.1rem; margin-top: 0.5rem;">Track your weekly meals to stay on top of your nutrition.</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state['user']['id']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Log Meal")
        with st.form("add_diet_form", clear_on_submit=True):
            day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            meal_type = st.selectbox("Meal Category", ["Breakfast", "Lunch", "Dinner", "Snacks"])
            food_items = st.text_area("What did you eat?", placeholder="e.g., 2 Eggs, 1 Avocado Toast, Black Coffee")
            
            submitted = st.form_submit_button("Add Meal", use_container_width=True)
            if submitted:
                if food_items:
                    if add_diet_entry(user_id, day, meal_type, food_items):
                        st.success("Meal logged successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to log meal. Database connection issue.")
                else:
                    st.warning("Please enter your food items.")
                    
    with col2:
        st.markdown("### Your Weekly Log")
        selected_day = st.selectbox("View log for:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], key="view_day")
        
        meals = fetch_diets(user_id, selected_day)
        if meals:
            df = pd.DataFrame(meals)
            
            meal_order = ["Breakfast", "Lunch", "Dinner", "Snacks"]
            df['meal_type'] = pd.Categorical(df['meal_type'], categories=meal_order, ordered=True)
            df = df.sort_values(['meal_type', 'id'])
            
            for m_type in meal_order:
                type_data = df[df['meal_type'] == m_type]
                if not type_data.empty:
                    st.markdown(f"#### {m_type}")
                    for _, row in type_data.iterrows():
                        cols = st.columns([5, 1])
                        cols[0].markdown(f"• {row['food_items']}")
                        if cols[1].button("🗑️", key=f"del_diet_{row['id']}", help="Delete"):
                            delete_diet_entry(row['id'])
                            st.rerun()
                    st.divider()
        else:
            st.info(f"No meals logged for {selected_day}.")

if __name__ == "__main__":
    show_diet_planner()
