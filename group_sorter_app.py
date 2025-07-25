import streamlit as st
import pandas as pd
import os

CSV_FILE = "student_survey.csv"

# Load existing data or create new
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["Name", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Group"])

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
    not_listed_cols = ["Q1", "Q2", "Q3", "Q5", "Q6"]
    if all(row[col] == "Not listed here" for col in not_listed_cols) and row["Q4"] == "Hard to say":
        return "🌈 Mystery Mode"
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
        new_entry = {
            "Name": name.strip(),
            "Q1": Q1,
            "Q2": Q2,
            "Q3": Q3,
            "Q4": Q4,
            "Q5": Q5,
            "Q6": Q6
        }
        # Assign group to the new entry
        new_entry["Group"] = assign_group(new_entry)
        
        # Append to dataframe and save
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        
        # Show user summary
        st.markdown(generate_summary(new_entry))

# Display current group distribution chart
if not df.empty and "Group" in df.columns:
    st.subheader("📊 Current Group Distribution")
    group_counts = df["Group"].value_counts()
    st.bar_chart(group_counts)

    # Download button for the updated CSV with groups
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Group Roster CSV",
        data=csv,
        file_name="student_group_roster.csv",
        mime="text/csv"
    )
