import altair as alt
import streamlit as st
import pandas as pd
import plotly.express as px
import os


eqp_options = ["C001", "C002", "C003"]
lot_options = ["AAA001.1", "AAA002.1", "AAA003.1"]

cols = st.columns(2)
with cols[0]:
    eqp_id = st.selectbox("EQP ID: ", eqp_options)
with cols[1]:
    lot_id = st.selectbox("Lot ID: ", lot_options)

st.markdown("---")

print(os.listdir('data'))
df = pd.read_csv('data/result.csv')

max_count = int(df.groupby("slot").size().max())
result_dfs = []
for i in range(max_count):
    result_dfs.append(df.groupby("slot").nth(i).reset_index())

style_css = """
<style>
table {
  border-collapse: collapse;
}
th:nth-child(1), td:nth-child(1) { width: 25px; }
th:nth-child(2), td:nth-child(2) { width: 100px; }
th:nth-child(3), td:nth-child(3) { width: 50px; }
th, td {
  border: 1px solid #ddd;
  padding: 4px;
  text-align: center;
}
</style>
"""

exclude_columns = ['date']

cols = st.columns(max_count)
for i in range(max_count):
    html_table = result_dfs[i].drop(columns=exclude_columns).to_html(index=False)
    with cols[i]:
        st.markdown(style_css + html_table, unsafe_allow_html=True)



