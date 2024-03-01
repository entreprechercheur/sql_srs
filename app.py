# pylint: disable=missing-module-docstring
import os
import logging

import streamlit as st
import duckdb

if 'data' not in os.listdir():
    logging.error(os.listdir())
    logging.error('Creating folder data/')
    os.mkdir('data')

if 'exercises_sql_tables.duckdb' not in os.listdir('data'):
    exec(open('init_db.py').read())
    # We should use instead of exec: subprocess(['python','init_db.py']

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "How would you like to review?",
        ("cross_joins", "Group By", "window_functions"),
        index=None,
        placeholder="Select a method..",
    )

    try:
        st.write("You selected: ", theme)
        exercise = (
            con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
            .df()
            .sort_values("last_reviewed")
            .reset_index(drop=True)
        )
        st.write(exercise)

        exercise_name = exercise.loc[0, "exercise_name"]
        with open(f"answers/{exercise_name}.sql", "r") as f:
            answer = f.read()

        solution_df = con.execute(answer).df()
    except KeyError as e:
        pass

st.header("Enter your code:")
query = st.text_area(label="Your SQL query here", key="user_input")

if query:
    result = con.execute(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
    except KeyError as e:
        st.write("Some columns are missing.")

    try:
        st.dataframe(result.compare(solution_df))
    except ValueError as e:
        n_lines_difference = result.shape[0] - solution_df.shape[0]
        if n_lines_difference != 0:
            st.write(
                f"Result has a {n_lines_difference} lines difference with the solution_df."
            )

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    # To transform the string of list into a list of string
    try:
        exercise_tables = exercise.loc[0, "tables"]

        for table in exercise_tables:
            st.write(f"Table: {table}")
            df_table = con.execute(f"SELECT * FROM {table}").df()
            st.dataframe(df_table)
    #     st.write("Expected:")
    #     st.dataframe(solution_df)
    except KeyError as e:
        st.write("Welcome to the Spaced Repetition System for SQL")

with tab2:
    try:
        st.write(answer)
    except NameError as e:
        st.write("Please, select a SQL topic to practice, in the sidebar.")
