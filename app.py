# pylint: disable=missing-module-docstring
import os
import logging

import streamlit as st
import duckdb
import pandas as pd

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating folder data/")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    # We should use instead of exec: subprocess(['python','init_db.py']

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def check_users_solution(users_query: str) -> None:
    """
    Checks that user SQL query is correct by:
    1: checking the columns
    2: checking the values
    :param users_query: a string containing the query inserted by the user
    """
    result = con.execute(users_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
    except KeyError as err:
        st.write("Some columns are missing.")
    try:
        st.dataframe(result.compare(solution_df))
    except ValueError as err:
        n_lines_difference = result.shape[0] - solution_df.shape[0]
        if n_lines_difference != 0:
            st.write(
                f"Result has a {n_lines_difference} lines difference with the solution_df."
            )


def get_exercise(available_themes: list) -> pd.DataFrame:
    """
    Gets an exercise for the user whether the user selected a theme or not
    :param available_themes: the list of available themes
    :type available_themes: list of string
    :return: the exercise to show to the user
    :rtype: pandas DataFrame
    """
    if available_themes:
        st.write("You selected: ", theme)
        select_exercise_query = (
            f"SELECT * FROM memory_state WHERE theme = '{available_themes}'"
        )
    else:
        select_exercise_query = f"SELECT * FROM memory_state"
    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)

    return exercise


def display_tables(exercise: pd.DataFrame) -> None:
    """
    Displays to the user the tables needed to solve the SQL problem
    :param exercise: the exercise containing information on the tables
    :type exercise: pandas DataFrame
    """
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)
        # st.write("Expected:")
        # st.dataframe(solution_df)


with st.sidebar:
    available_themes_df = con.execute("SELECT theme FROM memory_state").df()
    theme = st.selectbox(
        "How would you like to review?",
        available_themes_df["theme"].unique(),
        # ("cross_joins", "Group By", "window_functions"),
        index=None,
        placeholder="Select a method..",
    )

    exercises_df = get_exercise(theme)

    exercise_name = exercises_df.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("Enter your code:")
query = st.text_area(label="Your SQL query here", key="user_input")


if query:
    check_users_solution(query)

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    display_tables(exercises_df)

with tab2:
    st.write(answer)
