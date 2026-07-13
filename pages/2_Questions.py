import streamlit as st
import pandas as pd

from library import EvaluateExpression

filename = "Mini Project 2 - Instructor Database.xlsx"
users = pd.read_excel(filename, sheet_name="Users")

st.title("Questions")

# Task 1: read the sheet with the name "Questions"
question_data = pd.read_excel(filename, sheet_name="Questions")

st.header("Questions List")
st.dataframe(question_data, hide_index=True)

st.header("Create New Question")
with st.form("new_question"):
    expression = st.text_input("Write a Math expression:")
    expression

    # Task 2: create an object instance of EvaluateExpression class
    # pass on the math expression to the object
    evaluator = EvaluateExpression(expression)

    # Task 3: call the evaluate() method of the EvaluateExpression object
    # and store it
    answer = evaluator.evaluate() if evaluator.expression else None

    selected_users = st.multiselect("Select Users to answer this challenge.",
                                    users["username"])
    submit = st.form_submit_button("Create Question")

if submit and (not expression.strip() or evaluator.expression == ""
              or answer is None):
    st.error("Please enter a valid math expression (digits, + - * / ( ) "
             "and spaces only, with balanced brackets).")
elif submit:
    # Task 4: read Challenges and Challenge-Users tables
    # from the Excel file to update
    challenge_data = pd.read_excel(filename, sheet_name="Challenges")
    assoc_data = pd.read_excel(filename, sheet_name="Challenge-Users")

    question_id = int(question_data["id"].max()) + 1 if not question_data.empty else 1
    challenge_id = int(challenge_data["id"].max()) + 1 if not challenge_data.empty else 1
    assoc_id = int(assoc_data["id"].max()) + 1 if not assoc_data.empty else 1

    question_data.loc[len(question_data)] = [question_id, expression, answer]
    challenge_data.loc[len(challenge_data)] = [challenge_id, question_id]

    for user in selected_users:
        user_id = int(users.loc[users["username"] == user, "id"].iloc[0])
        assoc_data.loc[len(assoc_data)] = [assoc_id, challenge_id, user_id]
        assoc_id += 1

    # Task 5: update the Excel file with the new data
    with pd.ExcelWriter(filename, mode='a', if_sheet_exists='replace') as f:
        question_data.to_excel(f, sheet_name="Questions", index=False)
        challenge_data.to_excel(f, sheet_name="Challenges", index=False)
        assoc_data.to_excel(f, sheet_name="Challenge-Users", index=False)

    st.rerun()
