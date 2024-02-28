# pylint: disable=missing-module-docstring

import streamlit as st
import duckdb

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# solution_df = duckdb.sql(ANSWER_STR).df()

with st.sidebar:
    theme = st.selectbox(
        "How would you like to review?",
        ("cross_joins", "Group By", "Windows Functions"),
        index=None,
        placeholder="Select a method..",
    )

    st.write("You selected: ", theme)
    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("Enter your code:")
query = st.text_area(label="Your SQL query here", key="user_input")

# if query:
#     result = duckdb.sql(query).df()
#     st.dataframe(result)

#     try:
#         result = result[solution_df.columns]
#     except KeyError as e:
#         st.write("Some columns are missing.")

#     try:
#         st.dataframe(result.compare(solution_df))
#     except ValueError as e:
#         n_lines_difference = result.shape[0] - solution_df.shape[0]
#         if n_lines_difference != 0:
#             st.write(
#                 f"Result has a {n_lines_difference} lines difference with the solution_df."
#             )

# tab1, tab2 = st.tabs(["Tables", "Solution"])

# with tab1:
#     st.write("Table: beverages")
#     st.dataframe(beverages)
#     st.write("Table: food_items")
#     st.dataframe(food_items)
#     st.write("Expected:")
#     st.dataframe(solution_df)

# with tab2:
#     st.write(ANSWER_STR)
