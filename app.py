# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
import streamlit as st

CSV = """
beverage,price
orange juice,2.5
expresso,2
tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item,food_price
cookie,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df = duckdb.sql(ANSWER_STR).df()

with st.sidebar:
    option = st.selectbox(
        "How would you like to review?",
        ("Join", "Group By", "Windows Functions"),
        index=None,
        placeholder="Select a method..",
    )

    st.write("You selected: ", option)

st.header("Enter your code:")
query = st.text_area(label="Your SQL query here", key="user_input")

if query:
    result = duckdb.sql(query).df()
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
    st.write("Table: beverages")
    st.dataframe(beverages)
    st.write("Table: food_items")
    st.dataframe(food_items)
    st.write("Expected:")
    st.dataframe(solution_df)

with tab2:
    st.write(ANSWER_STR)
