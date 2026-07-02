# Exercise 3 — Design Documentation: `5_Improved.py`

## 1. Page Chosen

An improved version of **`pages/2_Questions.py`** (the Questions page). The old page
still works — questions can be created from either page and every other page keeps
functioning regardless of which version was used.

## 2. Design Process

1. **Research** — reviewed UI/UX heuristics (Nielsen's 10 usability heuristics,
   in particular *error prevention*, *visibility of system status* and
   *help users recognize and recover from errors*) and code quality literature
   (Clean Code naming/function-size guidance, DRY, cyclomatic complexity).
2. **Brainstormed pain points** in the current app:
   - Questions page crashes with a raw exception on invalid input (e.g. `1/0`, letters).
   - No feedback after creating a question — did it work? Who got it?
   - You can create a question with no recipients, producing an orphan challenge.
   - Repeated Excel read/write boilerplate on every page; magic strings everywhere.
   - Questions list becomes hard to scan once it grows (no search).
3. **Listed candidate improvements** with an estimated cost for each.
4. **Selected the page with a Pugh chart** (below).
5. **Implemented and measured** against the success metrics (below).

## 3. Pugh Chart (baseline: keep app as is)

| Criteria (weight)              | Users | **Questions** | Challenge | Hall of Fame |
|--------------------------------|:-----:|:-------------:|:---------:|:------------:|
| UX pain severity (3)           |   0   |      +2       |    +1     |      +1      |
| Code quality gain (2)          |  +1   |      +2       |    +1     |      +1      |
| Implementation cost (2)        |  +1   |       0       |    −1     |      0       |
| Risk of breaking other pages (1)|  0   |       0       |    −1     |      0       |
| **Weighted total**             | **4** |    **10**     |   **2**   |    **5**     |

The Questions page scores highest: it has the worst failure mode (uncaught
exceptions from user input) and the most duplicated code, at moderate cost.

## 4. Success Criteria / Metrics

### User Experience
- **Error prevention**: 0 uncaught exceptions from user input (old page: crashes on
  invalid characters, unbalanced brackets and division by zero).
- **Visibility of system status**: user sees the computed answer *before* submitting,
  and a confirmation naming the recipients *after* — 100% of actions get feedback.
- **Task success**: impossible to create a challenge with no recipients or an
  invalid expression (old page silently wrote `None` answers).
- **Findability**: locating a question among N questions is O(1) via search
  instead of scrolling the whole table.

### Code Quality
- **DRY / duplication**: Excel I/O reduced from 5 copies of read/write boilerplate
  to 2 helper functions (`load_sheet`, `save_sheets`).
- **Function size**: longest function ≤ ~25 lines; the old page was one ~60-line script.
- **Cyclomatic complexity**: every function ≤ 5 branches.
- **Magic strings**: 0 — filename and sheet names are module constants.
- **Documentation**: 100% of functions have docstrings.
- **Testability**: `safe_evaluate()` and `create_question()` are pure-ish functions
  that can be unit-tested without Streamlit.

## 5. Constraints Respected

- The app works end-to-end using either `2_Questions.py` or `5_Improved.py`.
- No user-defined function was replaced by a third-party library — `Stack` and
  `EvaluateExpression` from `library.py` are still used for all evaluation.
- Only alternative Streamlit/Pandas API calls were used for refactoring
  (`st.dataframe`, `st.button(type="primary")`, `DataFrame.rename`).
