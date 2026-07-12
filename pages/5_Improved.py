# Improved version of the Questions page (Exercise 3).
#
# User Experience improvements over pages/2_Questions.py:
# - Live validation of the math expression with a clear error message
#   instead of a raw Streamlit exception on invalid input.
# - A preview of the computed answer before the question is created,
#   so the creator can catch typos in the expression.
# - Required-field feedback: warns when no expression is entered or no
#   recipient is selected, instead of silently writing bad rows.
# - Success confirmation showing exactly who received the challenge.
# - Questions list is searchable and shown with friendly column names.
#
# Code Quality improvements:
# - All Excel access goes through two helper functions (load_sheet /
#   save_sheets) instead of repeated read/write boilerplate.
# - Constants for the filename and sheet names — no magic strings.
# - Small single-purpose functions with docstrings instead of one long
#   script, which makes the page unit-testable.
# - No duplicated evaluation logic: validation and answer preview reuse
#   the same safe_evaluate() helper.
#
# See DESIGN.md for the metrics, Pugh chart and full design process.

import streamlit as st
import pandas as pd

from library import EvaluateExpression

FILENAME = "Mini Project 2 - Instructor Database.xlsx"
SHEET_USERS = "Users"
SHEET_QUESTIONS = "Questions"
SHEET_CHALLENGES = "Challenges"
SHEET_ASSOC = "Challenge-Users"


def load_sheet(sheet_name):
    # Read one worksheet of the app database into a DataFrame.
    return pd.read_excel(FILENAME, sheet_name=sheet_name)


def save_sheets(sheets):
    # Write {sheet_name: DataFrame} back to the Excel database.
    with pd.ExcelWriter(FILENAME, mode="a", if_sheet_exists="replace") as f:
        for sheet_name, data in sheets.items():
            data.to_excel(f, sheet_name=sheet_name, index=False)


def safe_evaluate(expression):
    # Evaluate an infix expression.
    # Returns (answer, error_message). Exactly one of the two is None.
    if not expression.strip():
        return None, "Please enter a math expression."
    evaluator = EvaluateExpression(expression)
    if evaluator.expression == "":
        return None, ("The expression contains invalid characters. Only "
                      "digits, . + - * / ( ) and spaces are allowed.")
    try:
        answer = evaluator.evaluate()
    except (ZeroDivisionError, TypeError, IndexError):
        return None, ("The expression could not be evaluated. "
                      "Check for division by zero or unbalanced brackets.")
    # Negative numbers and decimals now evaluate; an unbalanced expression
    # (e.g. "(1 + 2") returns None instead of a value.
    if answer is None:
        return None, "The expression is incomplete or has unbalanced brackets."
    return answer, None


def create_question(expression, answer, selected_users, users):
    # Append the new question, challenge and recipient rows, then save.
    question_data = load_sheet(SHEET_QUESTIONS)
    challenge_data = load_sheet(SHEET_CHALLENGES)
    assoc_data = load_sheet(SHEET_ASSOC)

    question_id = int(question_data["id"].max()) + 1 if not question_data.empty else 1
    challenge_id = int(challenge_data["id"].max()) + 1 if not challenge_data.empty else 1
    question_data.loc[len(question_data)] = [question_id, expression, answer]
    challenge_data.loc[len(challenge_data)] = [challenge_id, question_id]

    for user in selected_users:
        user_id = int(users.loc[users["username"] == user, "id"].iloc[0])
        assoc_id = int(assoc_data["id"].max()) + 1 if not assoc_data.empty else 1
        assoc_data.loc[len(assoc_data)] = [assoc_id, challenge_id, user_id]

    save_sheets({SHEET_QUESTIONS: question_data,
                 SHEET_CHALLENGES: challenge_data,
                 SHEET_ASSOC: assoc_data})


def show_questions_list(question_data):
    # Display the existing questions with search and friendly headers.
    st.header("Questions List")
    search = st.text_input("🔍 Search questions:",
                           placeholder="e.g. (1 + 2) * 3")
    display = question_data.rename(columns={"id": "ID",
                                            "expression": "Expression",
                                            "answer": "Answer"})
    if search:
        display = display[display["Expression"].astype(str)
                          .str.contains(search, regex=False)]
    if display.empty:
        st.info("No questions found. Create one below!")
    else:
        st.dataframe(display.set_index("ID"), use_container_width=True)


def show_create_form(users):
    # Display the creation form with validation and answer preview.
    st.header("Create New Question")
    expression = st.text_input("Write a Math expression:",
                               placeholder="e.g. (1 + 2) * 3")

    answer, error = safe_evaluate(expression)
    if expression:
        if error:
            st.error(error)
        else:
            st.success(f"Preview — `{expression}` evaluates to **{answer}**")

    selected_users = st.multiselect(
        "Select Users to answer this challenge.", users["username"])

    if st.button("Create Question", type="primary"):
        if error:
            st.error("Fix the expression before creating the question.")
        elif not selected_users:
            st.warning("Select at least one user to send the challenge to.")
        else:
            create_question(expression, answer, selected_users, users)
            st.success(f"Challenge sent to: {', '.join(selected_users)} 🎉")
            st.rerun()


st.title("Questions (Improved)")
users = load_sheet(SHEET_USERS)
show_questions_list(load_sheet(SHEET_QUESTIONS))
show_create_form(users)
