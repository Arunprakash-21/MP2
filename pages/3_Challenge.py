import time

import streamlit as st
import pandas as pd

filename = "Mini Project 2 - Instructor Database.xlsx"
users = pd.read_excel(filename, sheet_name="Users")
question_data = pd.read_excel(filename, sheet_name="Questions")
challenge_data = pd.read_excel(filename, sheet_name="Challenges")
assoc_data = pd.read_excel(filename, sheet_name="Challenge-Users")
time_data = pd.read_excel(filename, sheet_name="Timerecord")

st.title("Challenge")

username = st.selectbox("Select which user you are:", users["username"])

if username is None:
    st.info("Create a user in the Users page first.")
    st.stop()

user_id = int(users.loc[users["username"] == username, "id"].iloc[0])
my_challenges = assoc_data[assoc_data["user_id"] == user_id]

st.header(f"Challenges for {username}")

if my_challenges.empty:
    st.info("No challenges have been sent to this user yet.")

for _, row in my_challenges.iterrows():
    assoc_id = int(row["id"])
    challenge_id = int(row["challenge_id"])
    question_id = int(challenge_data.loc[
        challenge_data["id"] == challenge_id, "question_id"].iloc[0])
    question = question_data.loc[question_data["id"] == question_id]
    expression = question["expression"].iloc[0]
    correct_answer = int(question["answer"].iloc[0])

    show_key = f"show_{assoc_id}"
    start_key = f"start_{assoc_id}"

    left, middle, right = st.columns([2, 1, 2])
    left.write(f"Challenge {challenge_id}")

    # Show/Hide toggle: the timer starts the moment the question is shown.
    label = "Hide" if st.session_state.get(show_key, False) else "Show"
    if middle.button(label, key=f"button_{assoc_id}"):
        if st.session_state.get(show_key, False):
            st.session_state[show_key] = False
        else:
            st.session_state[show_key] = True
            st.session_state[start_key] = time.time()
        st.rerun()

    # Display the recorded time on the row once the challenge is solved.
    records = time_data[time_data["challenge_user_id"] == assoc_id]
    if not records.empty:
        right.write(f"⏱️ {records['elapsed_time'].min():.2f} s")

    if st.session_state.get(show_key, False):
        st.subheader(f"Question: {expression}")
        with st.form(f"answer_{assoc_id}"):
            user_answer = st.number_input("Your answer:", step=1,
                                          key=f"answer_input_{assoc_id}")
            submit = st.form_submit_button("Submit Answer")

        if submit:
            if int(user_answer) == correct_answer:
                elapsed = time.time() - st.session_state[start_key]
                time_data.loc[len(time_data)] = [len(time_data),
                                                 assoc_id, elapsed]
                with pd.ExcelWriter(filename, mode='a',
                                    if_sheet_exists='replace') as f:
                    time_data.to_excel(f, sheet_name="Timerecord",
                                       index=False)
                st.session_state[show_key] = False
                st.rerun()
            else:
                st.error("Wrong answer. Try again!")
