import streamlit as st
import pandas as pd
import duckdb

st.write("Hello World!")
data = {"a": [1, 2, 3],
        "b": [4, 5, 6]}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(['Cat', 'Dog', 'Owl'])

with tab1:
    sql_query = st.text_area(label="Entrez votre requête SQL")
    result_query = duckdb.sql(sql_query).df()
    st.write(f"Vous avez entré la requête suivante : {sql_query}")
    st.dataframe(result_query)


with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=300)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=300)

