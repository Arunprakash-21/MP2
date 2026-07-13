# Mini Project 2: Math Quiz App

A multi-page Streamlit web app where users create math questions in **infix
notation**, send them as challenges to other users, race to answer them, and
compete on a Hall of Fame leaderboard. A local Excel file acts as the database.

## Project Structure

```
Home.py                                  # Home page
library.py                               # Stack + EvaluateExpression (from scratch)
test_library.py                          # pytest tests for library.py
Mini Project 2 - Instructor Database.xlsx # Excel "database" (5 sheets)
pages/
  1_Users.py                             # Register users (Exercise 1)
  2_Questions.py                         # Create + send questions (Exercise 2)
  3_Challenge.py                         # Attempt challenges with a timer
  4_Hall_of_Fame.py                      # Top-3 ranking per challenge
  5_Improved.py                          # Improved Questions page (Exercise 3)
Pipfile                                  # pipenv environment (Python 3.12)
```

The Excel database has five sheets: `Users`, `Questions`, `Challenges`,
`Challenge-Users` and `Timerecord`.

## Setup

Using pipenv (as in the course handout):

```bash
python -m pip install --user pipenv
python -m pipenv install
python -m pipenv shell
```

Or using the bundled virtual environment:

```bash
python3 -m venv .venv
.venv/bin/pip install streamlit pandas openpyxl pytest
source .venv/bin/activate
```

## Running the App

```bash
streamlit run Home.py
```

Then open http://localhost:8501.

1. **Users** — add a few users.
2. **Questions** — enter an infix expression (e.g. `(1 + 2) * 3`) and select
   the users to challenge.
3. **Challenge** — pick who you are, **Show** a challenge and answer it; the
   elapsed time from Show to a correct Submit is recorded on the row.
4. **Hall of Fame** — every challenge with its question, correct answer and
   the top three fastest users.
5. **Questions (Improved)** — Exercise 3 version of the Questions page
   

## Running the Tests

```bash
pytest
```

The tests cover the `Stack` class (push/pop/peek/is_empty) and the
`EvaluateExpression` class (expression validation, `insert_space`, and
`evaluate` with operator precedence and brackets) in `library.py`.
