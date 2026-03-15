import streamlit as st
from components.sidebar import render_sidebar
from utils.calculations import calculate_bmi
from utils.style import apply_custom_styles

st.set_page_config(page_title="BMI Calculator | FitTrack", page_icon="⚖️", layout="wide")
apply_custom_styles()

def show_bmi_calculator():
    if not st.session_state.get('user'):
        st.warning("Please log in to use the calculators.")
        st.stop()
        
    render_sidebar()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(88, 166, 255, 0.1) 0%, rgba(13, 17, 23, 0) 100%); 
                padding: 2rem; border-radius: 12px; border: 1px solid rgba(88, 166, 255, 0.2); margin-bottom: 2rem;">
        <h1 style="color: #58a6ff; margin-bottom: 0;">BMI Calculator ⚖️</h1>
        <p style="color: #8b949e; font-size: 1.1rem; margin-top: 0.5rem;">Calculate your Body Mass Index (BMI) to understand your weight category.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Enter your details")
        st.markdown('<div data-testid="metric-container">', unsafe_allow_html=True)
        weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, value=70.0)
        height = st.number_input("Height (cm)", min_value=0.0, step=0.1, value=170.0)
        st.markdown('</div>', unsafe_allow_html=True)
        
        calc_btn = st.button("Calculate BMI", type="primary")
        
    with col2:
        if calc_btn:
            if weight > 0 and height > 0:
                bmi, category = calculate_bmi(weight, height)
                
                # Determine color based on category
                color = "#58a6ff" # Blue (Normal)
                if category == "Underweight":
                    color = "#f1e05a" # Yellow
                elif category == "Overweight":
                    color = "#d29922" # Orange
                elif category == "Obese":
                    color = "#f85149" # Red
                    
                st.markdown(f"""
                <div style="background: rgba(33, 38, 45, 0.7); border: 1px solid #30363d; border-radius: 12px; padding: 2rem; text-align: center;">
                    <h3 style="color: #8b949e;">Your BMI is</h3>
                    <h1 style="color: {color}; font-size: 4rem; margin: 0;">{bmi}</h1>
                    <h2 style="color: {color};">{category}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                ### BMI Categories
                - **Underweight**: < 18.5
                - **Normal weight**: 18.5 - 24.9
                - **Overweight**: 25 - 29.9
                - **Obese**: ≥ 30
                """)
            else:
                st.error("Please enter valid weight and height.")

if __name__ == "__main__":
    show_bmi_calculator()
