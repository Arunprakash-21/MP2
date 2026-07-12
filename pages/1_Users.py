import streamlit as st
import pandas as pd

filename = "Mini Project 2 - Instructor Database.xlsx"
users = pd.read_excel(filename, sheet_name="Users")

# If the sheet was manually cleared and lost its columns, start fresh
# with the correct schema instead of crashing or showing NaN rows.
if not {"id", "username", "name"}.issubset(users.columns):
    users = pd.DataFrame(columns=["id", "username", "name"])

# Drop any row missing a username or name (leftover from a manual edit)
# so every remaining id is always backed by valid data.
valid_users = users.dropna(subset=["username", "name"]).reset_index(drop=True)
if len(valid_users) != len(users):
    users = valid_users
    with pd.ExcelWriter(filename, mode='a', if_sheet_exists='replace') as f:
        users.to_excel(f, sheet_name="Users", index=False)

st.title("Users")

st.header("Registered Users")
if users.empty:
    st.info("No registered users yet. Add one below!")
else:
    st.dataframe(users, hide_index=True)

st.header("Create New User")
with st.form("new_user", clear_on_submit=True):
    new_username = st.text_input("New Username:")
    new_name = st.text_input("Full Name:")
    submit = st.form_submit_button("Update User Table")

if submit:
    if new_username and new_name:
        new_id = int(users["id"].max()) + 1 if not users.empty else 1
        users.loc[len(users)] = [new_id, new_username, new_name]
        with pd.ExcelWriter(filename, mode='a', if_sheet_exists='replace') as f:
            users.to_excel(f, sheet_name="Users", index=False)

        st.rerun()
