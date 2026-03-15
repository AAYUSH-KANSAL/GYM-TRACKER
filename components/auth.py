import streamlit as st
from database.supabase_client import login_user, signup_user, get_user_profile

def authentication_flow():
    """Displays login/signup forms and handles authentication."""
    st.markdown("""
        <style>
        @keyframes fadeInSlide {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .animated-auth {
            animation: fadeInSlide 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="animated-auth">', unsafe_allow_html=True)
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("FitTrack Pro 🏋️‍♂️")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: #8b949e;'>Your ultimate companion for lifting, health, and progress tracking.</p>", unsafe_allow_html=True)
    
    st.divider()

    # Layout for centering the forms
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Log In", "Sign Up"])
        
        # --- LOGIN TAB ---
        with tab1:
            st.markdown("### Welcome Back")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Log In", use_container_width=True)
                
            if submit_login:
                if email and password:
                    with st.spinner("Logging in..."):
                        user, error = login_user(email, password)
                        if user:
                            # Attach custom metadata to session state if possible
                            profile = get_user_profile(user.id)
                            st.session_state['user'] = {
                                "id": user.id,
                                "email": user.email,
                                "profile": profile
                            }
                            st.success("Successfully logged in!")
                            st.rerun()
                        else:
                            st.error(f"Failed to log in: {error}")
                else:
                    st.warning("Please fill out both email and password fields.")
                    
        # --- SIGNUP TAB ---
        with tab2:
            st.markdown("### Create New Account")
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                new_email = st.text_input("Email")
                phone = st.text_input("Phone Number (Optional)", placeholder="+1234567890")
                new_password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit_signup = st.form_submit_button("Sign Up", use_container_width=True)
                
            if submit_signup:
                if not name or not new_email or not new_password or not confirm_password:
                    st.warning("Please fill out all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    with st.spinner("Creating account..."):
                        user, error = signup_user(new_email, new_password, name, phone)
                        if user:
                            # Re-fetch profile to ensure name/phone are synced
                            profile = get_user_profile(user.id)
                            st.session_state['user'] = {
                                "id": user.id,
                                "email": user.email,
                                "profile": profile or {"name": name, "phone": phone}
                            }
                            st.success("Account created successfully!")
                            st.rerun()
                        else:
                            st.error(f"Failed to create account: {error}")
                            
    # Footer disclaimer warning if supabase is not connected
    import os
    if not os.environ.get("SUPABASE_URL") or not os.environ.get("SUPABASE_KEY"):
        st.warning("⚠️ **Database not connected!** Application is running in offline mode. Please configure SUPABASE_URL and SUPABASE_KEY in `.env` to enable full functionality.")
        
    st.markdown('</div>', unsafe_allow_html=True)
