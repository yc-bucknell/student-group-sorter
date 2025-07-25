import streamlit as st
import pandas as pd
import uuid

# Define survey questions and options
questions = {
    "What’s your favorite color?": ["Red", "Blue", "Green", "Not listed here"],
    "What’s your ideal weekend activity?": ["Watching movies/shows", "Going outside (hiking, sports)", "Gaming", "Not listed here"],
    "What’s your favorite drink?": ["Coffee", "Boba/Milk Tea", "Water", "Not listed here"],
    "Are you a morning person or a night owl?": ["Morning person", "Night owl", "Hard to say"],
    "Pick a superpower you’d like to have:": ["Flying", "Time travel", "Reading minds", "Not listed here"],
    "Pick a fictional world you’d live in:": ["Marvel Universe", "Pokémon", "Barbie Land 🌸", "Not listed here"],
}

# Fun group label rules based on answers
group_map = {
    "Boba/Milk Tea": "🧃 Boba Enthusiasts",
    "Time travel": "🦸 Time Travelers",
    "Gaming": "🎮 Gamers Guild",
    "Barbie Land 🌸": "💅 Barbie Squad",
    "Not listed here": "🌈 Mystery Mode"
}

def determine_group(answers):
    # Flatten answers and count which keyword appears most
    answer_values = list(answers.values())
    for keyword, group in group_map.items():
        if keyword in answer_values:
            return group
    return "🌈 Mystery Mode"

# Load existing responses
@st.cache_data
def load_data():
    try:
        return pd.read_csv("student_survey.csv")
    except:
        return pd.DataFrame(columns=["ID"] + list(questions.keys()) + ["Group"])

# Main app
st.title("🎲 Fun Student Group Sorter")

with st.form("survey_form"):
    st.write("Please answer the following fun questions:")
    responses = {}
    for q, options in questions.items():
        responses[q] = st.radio(q, options)

    submitted = st.form_submit_button("Submit")

    if submitted:
        group = determine_group(responses)
        student_id = str(uuid.uuid4())
        df = load_data()
        new_row = {"ID": student_id, **responses, "Group": group}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("student_survey.csv", index=False)
        st.success(f"✅ Thanks for submitting! You belong to: **{group}**")

# Optional: Display current stats (only if teacher is viewing)
with st.expander("📊 See current class group distribution"):
    df = load_data()
    if not df.empty:
        group_counts = df["Group"].value_counts()
        st.bar_chart(group_counts)
