import streamlit as st
import pandas as pd

filename = "Mini Project 2 - Instructor Database.xlsx"
users = pd.read_excel(filename, sheet_name="Users")
question_data = pd.read_excel(filename, sheet_name="Questions")
challenge_data = pd.read_excel(filename, sheet_name="Challenges")
assoc_data = pd.read_excel(filename, sheet_name="Challenge-Users")
time_data = pd.read_excel(filename, sheet_name="Timerecord")

st.title("Hall of Fame")

if challenge_data.empty:
    st.info("No challenges have been created yet.")

# Each challenge is displayed as a new section showing the question,
# the correct answer, and the top three users with the shortest time.
for _, challenge in challenge_data.iterrows():
    challenge_id = int(challenge["id"])
    question_id = int(challenge["question_id"])
    question = question_data.loc[question_data["id"] == question_id]
    expression = question["expression"].iloc[0]
    answer = question["answer"].iloc[0]

    st.header(f"Challenge {challenge_id}")
    st.write(f"**Question:** `{expression}`")
    st.write(f"**Correct Answer:** {answer}")

    # Join Timerecord -> Challenge-Users -> Users to rank the answers.
    challenge_assocs = assoc_data[assoc_data["challenge_id"] == challenge_id]
    records = time_data[time_data["challenge_user_id"]
                        .isin(challenge_assocs["id"])]

    if records.empty:
        st.write("*No user has solved this challenge yet.*")
        continue

    # Keep each user's best time only, then rank the top three.
    best_times = {}
    for _, record in records.iterrows():
        assoc = challenge_assocs.loc[
            challenge_assocs["id"] == record["challenge_user_id"]]
        user_id = int(assoc["user_id"].iloc[0])
        elapsed = float(record["elapsed_time"])
        if user_id not in best_times or elapsed < best_times[user_id]:
            best_times[user_id] = elapsed

    ranked = sorted(best_times.items(), key=lambda pair: pair[1])[:3]
    rows = []
    for rank, (user_id, elapsed) in enumerate(ranked, start=1):
        username = users.loc[users["id"] == user_id, "username"].iloc[0]
        rows.append({"Rank": rank,
                     "Username": username,
                     "Time (s)": round(elapsed, 2)})

    st.subheader("Top Three Users")
    st.table(pd.DataFrame(rows).set_index("Rank"))
