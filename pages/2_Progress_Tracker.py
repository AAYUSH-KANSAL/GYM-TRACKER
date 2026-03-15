import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
from components.sidebar import render_sidebar
from database.supabase_client import save_progress_entry, get_progress_data
from utils.style import apply_custom_styles

st.set_page_config(page_title="Progress Tracker | FitTrack", page_icon="📈", layout="wide")
apply_custom_styles()

def show_progress_tracker():
    if not st.session_state.get('user'):
        st.warning("Please log in to track your progress.")
        st.stop()
        
    render_sidebar()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(46, 160, 67, 0.1) 0%, rgba(13, 17, 23, 0) 100%); 
                padding: 2rem; border-radius: 12px; border: 1px solid rgba(46, 160, 67, 0.2); margin-bottom: 2rem;">
        <h1 style="color: #3fb950; margin-bottom: 0;">Progress Tracker 📈</h1>
        <p style="color: #8b949e; font-size: 1.1rem; margin-top: 0.5rem;">Log your latest measurements and visualize your journey.</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state['user']['id']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Entry")
        with st.form("progress_form"):
            entry_date = st.date_input("Date", datetime.date.today())
            weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, format="%.1f")
            chest = st.number_input("Chest (cm)", min_value=0.0, step=0.5, format="%.1f")
            waist = st.number_input("Waist (cm)", min_value=0.0, step=0.5, format="%.1f")
            biceps = st.number_input("Biceps (cm)", min_value=0.0, step=0.5, format="%.1f")
            thigh = st.number_input("Thigh (cm)", min_value=0.0, step=0.5, format="%.1f")
            
            submit = st.form_submit_button("Save Progress", use_container_width=True)
            
            if submit:
                if weight > 0:
                    success = save_progress_entry(
                        user_id=user_id,
                        date=entry_date,
                        weight=weight,
                        chest=chest if chest > 0 else None,
                        waist=waist if waist > 0 else None,
                        biceps=biceps if biceps > 0 else None,
                        thigh=thigh if thigh > 0 else None
                    )
                    if success:
                        st.success("Progress saved successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to save progress. Please try again.")
                else:
                    st.warning("Weight is required.")
                    
    with col2:
        st.subheader("History")
        data = get_progress_data(user_id)
        if data:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date']).dt.date
            df = df.sort_values('date', ascending=False)
            
            # Show dataframe
            st.dataframe(
                df[['date', 'weight', 'chest', 'waist', 'biceps', 'thigh']].style.format(na_rep="--"),
                use_container_width=True,
                hide_index=True
            )
            
            st.divider()
            st.subheader("Visual Trends")
            
            metric_to_plot = st.selectbox("Select metric to visualize", ['weight', 'chest', 'waist', 'biceps', 'thigh'])
            
            df_plot = df.dropna(subset=[metric_to_plot]).sort_values('date')
            if not df_plot.empty:
                fig = px.area(df_plot, x='date', y=metric_to_plot, markers=True, 
                              template="plotly_dark",
                              color_discrete_sequence=["#2ea043"])
                fig.update_traces(fillcolor='rgba(46, 160, 67, 0.2)')
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=10, b=0))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"Not enough data to plot {metric_to_plot}.")

        else:
            st.info("No entries yet. Add your first measurement!")

if __name__ == "__main__":
    show_progress_tracker()
