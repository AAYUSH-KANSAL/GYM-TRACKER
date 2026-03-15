# FitTrack Pro 🏋️‍♂️

**FitTrack Pro** is a modern, premium Gym Progress Tracking Web App built with **Streamlit** and **Supabase**. It allows users to track their body measurements, calculate vital health metrics, plan workouts and diets, and chat with an AI Fitness Coach.

## ✨ Features

- **🔐 Secure Authentication**: Email-based signup and login powered by Supabase Auth with custom animated UI.
- **📊 Interactive Dashboard**: Visual overview of your latest body measurements and weight trends using premium Plotly area charts.
- **📈 Progress Tracker**: Log weight, chest, waist, biceps, and thigh measurements and see your history.
- **⚖️ BMI & Calorie Calculators**: Dynamically calculate your Body Mass Index and daily maintenance/loss/gain macros.
- **📅 Workout & Diet Planners**: Organize your weekly lifting splits and recurring meal schedules on a weekday basis.
- **🤖 AI Fitness Coach**: A conversational chat interface powered by **Groq (Llama 3)** to provide personalized training and nutrition advice.
- **💎 Premium UI/UX**: Custom dark-themed CSS with glassmorphism, smooth animations, and interactive navigation cards.

## 🚀 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend/Database**: [Supabase](https://supabase.com/)
- **AI Integration**: [Groq Cloud SDK](https://groq.com/)
- **Visualization**: [Plotly](https://plotly.com/)
- **Styling**: Vanilla CSS & HTML Injection

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/AAYUSH-KANSAL/GYM-TRACKER.git
cd GYM-TRACKER
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory and add your credentials:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
GROQ_API_KEY=your_groq_api_key
```

### 4. Database Setup
Execute the SQL script found in `database/schema.sql` within your Supabase SQL Editor to initialize the required tables (`profiles`, `progress`, `workouts`, `diets`).

### 5. Run the App
```bash
streamlit run app.py
```

## 📸 Screenshots
*(Add your screenshots here)*

---
Developed with ❤️ by [Aayush Kansal](https://github.com/AAYUSH-KANSAL)
