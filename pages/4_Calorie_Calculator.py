import streamlit as st
from components.sidebar import render_sidebar
from utils.calculations import calculate_maintenance_calories
from utils.style import apply_custom_styles

st.set_page_config(page_title="Calorie Calculator | FitTrack", page_icon="🔥", layout="wide")
apply_custom_styles()

def show_calorie_calculator():
    if not st.session_state.get('user'):
        st.warning("Please log in to use the calculators.")
        st.stop()
        
    render_sidebar()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(88, 166, 255, 0.1) 0%, rgba(13, 17, 23, 0) 100%); 
                padding: 2rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.2); margin-bottom: 2rem;">
        <h1 style="color: #58a6ff; margin-bottom: 0;">Calorie Calculator 🔥</h1>
        <p style="color: #8b949e; font-size: 1.1rem; margin-top: 0.5rem;">Find out how many calories you need to maintain, lose, or gain weight.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("### Your details")
        with st.form("calorie_form"):
            age = st.number_input("Age (years)", min_value=10, max_value=120, step=1, value=25)
            gender = st.selectbox("Gender", ["Male", "Female"])
            weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, value=70.0)
            height = st.number_input("Height (cm)", min_value=0.0, step=0.1, value=170.0)
            activity_level = st.selectbox(
                "Activity Level", 
                ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"]
            )
            
            calc_btn = st.form_submit_button("Calculate Calories", use_container_width=True)
            
    with col2:
        if calc_btn:
            maint, loss, gain = calculate_maintenance_calories(age, gender, height, weight, activity_level)
            
            st.markdown("### Your Results")
            
            # Maintenance
            st.markdown(f"""
            <div data-testid="metric-container" style="border-left: 4px solid #8b949e; margin-bottom: 1rem;">
                <h4 style="margin:0; color:#c9d1d9;">Maintenance</h4>
                <p style="margin:0; font-size: 0.9rem; color:#8b949e;">Maintain your current weight</p>
                <h2 style="margin:0; color:#8b949e;">{maint} kcal / day</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Fat Loss
            st.markdown(f"""
            <div data-testid="metric-container" style="border-left: 4px solid #2ea043; margin-bottom: 1rem;">
                <h4 style="margin:0; color:#c9d1d9;">Fat Loss</h4>
                <p style="margin:0; font-size: 0.9rem; color:#8b949e;">Aggressive weight loss (-500 kcal)</p>
                <h2 style="margin:0; color:#2ea043;">{loss} kcal / day</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Muscle Gain
            st.markdown(f"""
            <div data-testid="metric-container" style="border-left: 4px solid #58a6ff; margin-bottom: 1rem;">
                <h4 style="margin:0; color:#c9d1d9;">Muscle Gain (Bulking)</h4>
                <p style="margin:0; font-size: 0.9rem; color:#8b949e;">Moderate weight gain (+300 kcal)</p>
                <h2 style="margin:0; color:#58a6ff;">{gain} kcal / day</h2>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_calorie_calculator()
