import streamlit as st
import pandas as pd


def by_time(pair):
    # Sort key: the elapsed time is the second item of a (user_id, time) pair.
    return pair[1]


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

   
    best_times = {}
    for _, record in records.iterrows(): \
        # A time record stores a "challenge_user_id" link, not the user id,
        # so look that link up in Challenge-Users to find the real user.
        assoc = challenge_assocs.loc[
            challenge_assocs["id"] == record["challenge_user_id"]]
        user_id = int(assoc["user_id"].iloc[0])  # .iloc[0] grabs the first result 
        elapsed = float(record["elapsed_time"])
        # Store this time if it's the user's first, or faster than their best.
        if user_id not in best_times or elapsed < best_times[user_id]:
            best_times[user_id] = elapsed

    # Sort users fastest-first, then keep only the top three.
    ranked_pairs = sorted(best_times.items(), key=by_time)  # (user_id, time) sorted by time
    ranked = ranked_pairs[:3]  # first 3 = podium

    # Turn the ranking into display rows, numbering them 1, 2, 3.
    rows = []
    for rank, (user_id, elapsed) in enumerate(ranked, start=1):
        username = users.loc[users["id"] == user_id, "username"].iloc[0]  # id -> name
        rows.append({
            "Rank": rank,
            "Username": username,
            "Time (s)": round(elapsed, 2)
        })

    st.subheader("Top Three Users")
    st.table(pd.DataFrame(rows).set_index("Rank"))
