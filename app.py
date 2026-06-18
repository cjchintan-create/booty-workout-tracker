import streamlit as st
import datetime
import requests

# App Configuration
st.set_page_config(page_title="Booty Committee Tracker", page_icon="🍑", layout="centered")

st.markdown("""
    <style>
    .main .block-container {
        max-width: 500px;
        padding-top: 2rem;
    }
    h1 {
        text-align: center;
        color: #D35400;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        width: 100%;
        background-color: #E67E22;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #D35400;
        color: white;
    }
    .exercise-box {
        background-color: #FFF5EE;
        padding: 12px;
        border-radius: 8px;
        border-left: 6px solid #E67E22;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .exercise-title {
        color: #D35400;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 2px;
    }
    .exercise-subtitle {
        color: #7F8C8D;
        font-size: 13px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍑 Teeny Tiny Big Booty Tracker")
st.subheader("The Ultimate Hourglass Routine")

# --- ROUTINE DATA DIRECTLY FROM PDF ---
ROUTINES = {
    "Day 1: Glutes & Hamstrings": [
        {"name": "Hip Thrusts", "sets": 4, "reps": "8-12 reps", "note": "Squeeze glutes at top for 2s. Keep chin tucked."},
        {"name": "Abductions", "sets": 3, "reps": "15-20 reps", "note": "Controlled negative. Focus on outer glute."},
        {"name": "Step Ups", "sets": 3, "reps": "10-12 reps (per side)", "note": "Drive through front heel on stable box."}
    ],
    "Day 2: Back & Rear Delts (Top Hourglass)": [
        {"name": "Lat Pull Down", "sets": 4, "reps": "10-12 reps", "note": "Pull with elbows down. Avoid excessive lean back."},
        {"name": "Face Pulls", "sets": 3, "reps": "15 reps", "note": "Pull towards ears/forehead. Focus on rear delts."},
        {"name": "Single Arm Row", "sets": 3, "reps": "10-12 reps (per side)", "note": "Keep torso parallel to floor/supported."}
    ],
    "Day 3: Glutes & Quads": [
        {"name": "Hip Thrusts (Heavy/Kas)", "sets": 4, "reps": "10 reps", "note": "Heavy loading day or Kas Glute Bridge variation."},
        {"name": "Bulgarian Split Squats", "sets": 3, "reps": "8-12 reps (per side)", "note": "Slight forward lean for glutes, deep knee flexion for quads."},
        {"name": "Cable Kickbacks", "sets": 3, "reps": "12-15 reps", "note": "Kick back and slightly outward at a 45-degree angle."}
    ],
    "Day 4: Glutes & Arms": [
        {"name": "Hyperextensions", "sets": 3, "reps": "12-15 reps", "note": "Round upper back intentionally to isolate glutes."},
        {"name": "Tricep Work (Pushdowns/Extensions)", "sets": 3, "reps": "12-15 reps", "note": "Choose cable pushdowns or overhead extensions."},
        {"name": "Bicep Work (Curls)", "sets": 3, "reps": "12-15 reps", "note": "Choose dumbbell curls or cable hammer curls."}
    ]
}

# --- SYNC TO GOOGLE SHEET ---
def save_to_google_sheets(data_list):
    try:
        # Live Google Apps Script Deployment URL for her sheet
        WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxF60a2oppl0zYXcKtzKp9wKp2htJyD_XrwQ9grjXjo3EByn1NglQWTu77CZISx4t7iOw/exec"
        
        response = requests.post(WEB_APP_URL, json=data_list)
        if response.status_code == 200 and response.json().get("status") == "success":
            return True
        else:
            st.error(f"Sheet Web App Error: {response.text}")
            return False
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return False

# --- APP INTERFACE ---
date_input = st.date_input("Training Date", datetime.date.today())
routine_input = st.selectbox("Choose Workout Day", list(ROUTINES.keys()))

st.markdown("---")

current_session_accumulator = []
active_exercises = ROUTINES[routine_input]

for ex in active_exercises:
    st.markdown(f"""
        <div class='exercise-box'>
            <div class='exercise-title'>{ex['name']}</div>
            <div class='exercise-subtitle'>Plan: {ex['sets']} Sets x {ex['reps']}</div>
            <div style='color: #7F8C8D; font-size: 12px; font-style: italic;'>Tip: {ex['note']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    for set_num in range(1, ex['sets'] + 1):
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input(f"Weight - Set {set_num}", min_value=0.0, max_value=500.0, step=2.5, key=f"{ex['name']}_w_{set_num}")
        with col2:
            reps = st.number_input(f"Reps - Set {set_num}", min_value=0, max_value=100, step=1, key=f"{ex['name']}_r_{set_num}")
        
        current_session_accumulator.append({
            "Date": str(date_input),
            "Workout Day": routine_input,
            "Exercise Name": ex['name'],
            "Set Number": set_num,
            "Weight Logged": weight,
            "Reps Executed": reps
        })

if st.button("Save Training Session Logs to Cloud"):
    if save_to_google_sheets(current_session_accumulator):
        st.success("Workout successfully synced to your Google Sheet!")
        st.balloons()
