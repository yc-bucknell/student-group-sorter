import streamlit as st
import pandas as pd
import os

st.title("🎲 Fun Group Sorter Game!")

# Load or create CSV
file_path = "student_survey.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=["Name", "Color", "Weekend", "Drink", "PersonType", "Superpower", "World"])

# Get student name
name = st.text_input("Enter your name")

# Ask fun survey questions
color = st.radio("1. What’s your favorite color?", ["Red", "Blue", "Green", "Not listed here"])
weekend = st.radio("2. What’s your ideal weekend activity?", ["Watching movies/shows", "Going outside (hiking, sports)", "Gaming", "Not listed here"])
drink = st.radio("3. What’s your favorite drink?", ["Coffee", "Boba/Milk Tea", "Water", "Not listed here"])
person_type = st.radio("4. Are you a morning person or a night owl?", ["Morning person", "Night owl", "Hard to say"])
superpower = st.radio("5. Pick a superpower you’d like to have:", ["Flying", "Time travel", "Reading minds", "Not listed here"])
world = st.radio("6. Pick a fictional world you’d live in:", ["Marvel Universe", "Pokémon", "Barbie Land 🌸", "Not listed here"])

if st.button("Submit"):
    if name.strip() == "":
        st.error("Please enter your name.")
    else:
        new_row = {
            "Name": name.strip(),
            "Color": color,
            "Weekend": weekend,
            "Drink": drink,
            "PersonType": person_type,
            "Superpower": superpower,
            "World": world
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_path, index=False)

        if all(choice == "Not listed here" for choice in [color, weekend, drink, superpower, world]) and person_type == "Hard to say":
            st.warning("Hmm... 🤔 I can't quite guess your type! You're truly unique!")
        else:
            group_id = f"{color[:1]}{weekend[:1]}{drink[:1]}{person_type[:1]}{superpower[:1]}{world[:1]}"
            st.success(f"🎉 Thanks {name}! You’ve been grouped into: **Group {group_id.upper()}**")

        st.info("You can close the window now or refresh to start over.")
