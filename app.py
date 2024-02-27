import streamlit as st
import pandas as pd
import duckdb
import io

csv = '''
beverage,price
orange juice,2.5
expresso,2
tea,3
'''
beverages = pd.read_csv(io.StringIO(csv))


csv2 = '''
food_item,food_price
cookie,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = '''
SELECT * FROM beverages
CROSS JOIN food_items
'''

solution = duckdb.sql(answer).df()


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

tab1, tab2 = st.tabs(['Tables', 'Solution'])

with tab1:
    st.write("Table: beverages")
    st.dataframe(beverages)
    st.write("Table: food_items")
    st.dataframe(food_items)
    st.write("Expected:")
    st.dataframe(solution)

with tab2:
    st.write(answer)
