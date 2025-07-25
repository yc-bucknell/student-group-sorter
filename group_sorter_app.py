import streamlit as st
import pandas as pd
import os

# File path for storing survey data
CSV_FILE = "student_survey.csv"

# Load existing data or create new
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["Name", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6"])

st.title("🎲 Fun Grouping App with Emojis and Personality Types!")

# Input student's name
name = st.text_input("Enter your full name:")

# Survey questions matching your Moodle setup
Q1 = st.radio("1. What’s your favorite color?", ["Red", "Blue", "Green", "Not listed here"])
Q2 = st.radio("2. What’s your ideal weekend activity?", [
    "Watching movies/shows", "Going outside (hiking, sports)", "Gaming", "Not listed here"
])
Q3 = st.radio("3. What’s your favorite drink?", ["Coffee", "Boba/Milk Tea", "Water", "Not listed here"])
Q4 = st.radio("4. Are you a morning person or a night owl?", ["Morning person", "Night owl", "Hard to say"])
Q5 = st.radio("5. Pick a superpower you’d like to have:", ["Flying", "Time travel", "Reading minds", "Not listed here"])
Q6 = st.radio("6. Pick a fictional world you’d live in:", [
    "Marvel Universe", "Pokémon", "Barbie Land 🌸", "Not listed here"
])

def assign_group(row):
    # If all "Not listed here" (except Q4), assign Mystery Mode
    not_listed_cols = ["Q1", "Q2", "Q3", "Q5", "Q6"]
    if all(row[col] == "Not listed here" for col in not_listed_cols) and row["Q4"] == "Hard to say":
        return "🌈 Mystery Mode"
    
    # Priority groups based on dominant traits
    if row["Q3"] == "Boba/Milk Tea":
        return "🧃 Boba Enthusiasts"
    if row["Q5"] == "Time travel":
        return "🦸 Time Travelers"
    if row["Q2"] == "Gaming":
        return "🎮 Gamers Guild"
    if row["Q6"] == "Barbie Land 🌸":
        return "💅 Barbie Squad"
    return "🌟 Free Spirits"

def generate_summary(row):
    group = assign_group(row)
    summary = f"""
    ## Hello, {row['Name']}! 🎉
    You belong to the group: **{group}**
    
    Here’s what you picked:
    - Favorite color: {row['Q1']}
    - Weekend activity: {row['Q2']}
    - Favorite drink: {row['Q3']}
    - Morning or night person: {row['Q4']}
    - Desired superpower: {row['Q5']}
    - Fictional world: {row['Q6']}
    """
    return summary

if st.button("Submit"):
    if not name.strip():
        st.error("Please enter your name.")
    else:
        # Add new entry to dataframe
        new_entry = {
            "Name": name.strip(),
            "Q1": Q1,
            "Q2": Q2,
            "Q3": Q3,
            "Q4": Q4,
            "Q5": Q5,
            "Q6": Q6
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        
        # Show summary and group
        st.markdown(generate_summary(new_entry))
