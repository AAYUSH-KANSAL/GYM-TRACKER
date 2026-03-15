import streamlit as st

def apply_custom_styles():
    """Applies premium CSS styles for a modern Gym Tracker Web App."""
    st.markdown("""
        <style>
        /* Main background and font */
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Inter', -apple-system, sans-serif;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        
        /* Hide default Streamlit sidebar navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* Hide Streamlit branding components while keeping the header area (needed for mobile menu) */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Ensure the header is transparent so it doesn't clash, but keep it for the hamburger menu */
        header[data-testid="stHeader"] {
            background-color: rgba(0,0,0,0);
            border-bottom: none;
        }
        
        /* Hide the 'Deploy' button and other clutter in the header */
        .stDeployButton {
            display: none;
        }

        /* Premium Buttons */
        .stButton>button {
            background-color: #2ea043;
            color: #ffffff;
            border-radius: 6px;
            border: 1px solid rgba(240, 246, 252, 0.1);
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #3fb950;
            border-color: rgba(240, 246, 252, 0.1);
            color: #ffffff;
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4);
        }
        
        /* Metric Cards / Glassmorphism */
        div[data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 800;
            color: #58a6ff;
        }
        div[data-testid="metric-container"] {
            background: rgba(33, 38, 45, 0.7);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        /* Inputs and Text Areas */
        div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
            background-color: #0d1117 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
            color: #c9d1d9 !important;
        }
        div[data-baseweb="input"] > div:focus-within {
            border-color: #58a6ff !important;
            box-shadow: 0 0 0 1px #58a6ff !important;
        }

        /* Headers */
        h1, h2, h3 {
            color: #f0f6fc;
            font-weight: 700;
        }
        
        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #30363d;
        }

        /* Home Page Specials */
        .hero-section {
            background: linear-gradient(135deg, rgba(46, 160, 67, 0.15) 0%, rgba(88, 166, 255, 0.1) 100%);
            border-radius: 20px;
            padding: 4rem 2rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
            overflow: hidden;
        }
        .hero-section::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(46, 160, 67, 0.1) 0%, transparent 70%);
            animation: rotate 10s linear infinite;
        }
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        .action-card {
            background: rgba(22, 27, 34, 0.6);
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            height: 100%;
        }
        .action-card:hover {
            transform: translateY(-10px);
            background: rgba(33, 38, 45, 0.8);
            border-color: #58a6ff;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }
        .quote-box {
            font-style: italic;
            color: #8b949e;
            border-left: 3px solid #3fb950;
            padding-left: 1.5rem;
            margin: 2rem 0;
            font-size: 1.2rem;
        }
        </style>
    """, unsafe_allow_html=True)
