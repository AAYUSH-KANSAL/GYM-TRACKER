import os
from supabase import create_client, Client
import streamlit as st

@st.cache_resource
def init_connection() -> Client:
    """Initialize connection to Supabase."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

def get_supabase():
    """Returns the cached Supabase client."""
    client = init_connection()
    if not client:
        return None
    return client

def login_user(email, password):
    """Authenticate a user."""
    supabase = get_supabase()
    if not supabase: return None, "Supabase environment variables not set"
    
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            return response.user, None
        return None, "Login failed"
    except Exception as e:
        return None, str(e)

def signup_user(email, password, name, phone=None):
    """Register a new user and add to profiles table."""
    supabase = get_supabase()
    if not supabase: return None, "Supabase environment variables not set"
    
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        
        # After successful sign up, insert profile
        if response.user:
            try:
                # Use upsert to create or update profile
                supabase.table("profiles").upsert({
                    "id": response.user.id,
                    "user_id": response.user.id,
                    "name": name,
                    "email": email,
                    "phone": phone
                }).execute()
            except Exception as e:
                # Log error but don't fail signup if profile creation has issues (e.g. trigger already did it)
                print(f"Profile creation error: {e}")
                
            return response.user, None
        return None, "Sign up failed"
    except Exception as e:
        return None, str(e)

def logout_user():
    """Sign out the current user."""
    supabase = get_supabase()
    if supabase:
        supabase.auth.sign_out()
    st.session_state['user'] = None

def get_user_profile(user_id):
    """Fetch user profile."""
    supabase = get_supabase()
    if not supabase: return None
    try:
        response = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except:
        return None

def save_progress_entry(user_id, date, weight, chest=None, waist=None, biceps=None, thigh=None):
    """Save body measurements."""
    supabase = get_supabase()
    if not supabase: return False
    try:
        data = {
            "user_id": user_id,
            "date": str(date),
            "weight": weight,
            "chest": chest,
            "waist": waist,
            "biceps": biceps,
            "thigh": thigh
        }
        supabase.table("progress").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error saving progress: {e}")
        return False

def get_progress_data(user_id):
    """Fetch progress measurements."""
    supabase = get_supabase()
    if not supabase: return []
    try:
        response = supabase.table("progress").select("*").eq("user_id", user_id).order("date").execute()
        return response.data
    except:
        return []
