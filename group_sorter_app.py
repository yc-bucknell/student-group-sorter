
import streamlit as st
import pandas as pd
import os

# CSV path for appending new responses
CSV_FILE = "student_survey.csv"

# Load existing survey data
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["Name", "Q1", "Q2", "Q3", "Q4"])

st.title("🎓 Student Personality Group Sorter")

# Survey questions
st.subheader("📝 Quick Survey")

name = st.text_input("Enter your name:")

q1 = st.radio("1. How do you prefer to recharge after a long day?",
              ["🧘 Calm", "🎉 Energetic", "🚀 Adventurous", "Not listed here"],
              index=None)

q2 = st.radio("2. Which best describes your thinking style?",
              ["📈 Analytical", "🎨 Creative", "🧠 Strategic", "Not listed here"],
              index=None)

q3 = st.radio("3. What time of day are you most productive?",
              ["🌅 Morning", "🌙 Night", "☀️ Afternoon", "Not listed here"],
              index=None)

q4 = st.radio("4. Do you prefer working in groups or alone?",
              ["👥 Group", "👤 Individual", "🤷 Hard to say"],
              index=None)

if st.button("Submit"):
    if not name or not q1 or not q2 or not q3 or not q4:
        st.warning("Please answer all questions before submitting.")
    else:
        # Append new row to the CSV
        new_row = pd.DataFrame([[name, q1, q2, q3, q4]], columns=["Name", "Q1", "Q2", "Q3", "Q4"])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        
        st.success("Thanks for your submission!")
        
        if all(ans == "Not listed here" for ans in [q1, q2, q3]):
            st.info("🤔 Hmm... we can't quite guess your type!")
        else:
            # Group logic
            group_traits = {
                "🧘 Calm": "Type A", "📈 Analytical": "Type A", "🌅 Morning": "Type A", "👥 Group": "Type A",
                "🎉 Energetic": "Type B", "🎨 Creative": "Type B", "🌙 Night": "Type B", "👤 Individual": "Type B",
                "🚀 Adventurous": "Type C", "🧠 Strategic": "Type C", "☀️ Afternoon": "Type C"
            }
            
            answers = [q1, q2, q3, q4]
            traits = [group_traits.get(ans) for ans in answers if ans in group_traits]
            group = max(set(traits), key=traits.count)
            
            st.balloons()
            st.markdown(f"🎯 Based on your answers, you belong to **{group}** personality group!")
