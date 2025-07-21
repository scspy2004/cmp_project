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

df = pd.read_csv('data/result.csv')

max_count = int(df.groupby("slot").size().max())
result_dfs = []
for i in range(max_count):
    result_dfs.append(df.groupby("slot").nth(i).reset_index())


# def highlight_fail(cell):
#     if isinstance(cell, str) and "fail" in cell.lower():
#         return "background-color: rgb(255, 191, 191)"
#     return ""


def style_cell(cell):
    if isinstance(cell, str) and "fail" in cell.lower():
        return "background-color: rgb(255, 191, 191); font-weight: bold"
    elif isinstance(cell, str) and "pass" in cell.lower():
        return "background-color: rgb(191, 191, 255)"
    else:
        return ""



def highlight_fail(cell):
    if isinstance(cell, str) and "fail" in cell.lower():
        return "color: rgb(0, 0, 255); background-color: rgb(255, 191, 191)"
    return ""


# styled_df = result_dfs[0].style.applymap(highlight_fail)

# st.dataframe(styled_df, height=1000)

# style_css = """
# <style>
# table { border-collapse: collapse; }
# th:nth-child(1), td:nth-child(1) { width: 25px; }
# th:nth-child(2), td:nth-child(2) { width: 100px; }
# th:nth-child(3), td:nth-child(3) { width: 50px; }
# th, td { border: 1px solid #ddd; padding: 4px; text-align: center; }
# </style>
# """

exclude_columns = ['date']

cols = st.columns(max_count)
for i in range(max_count):
    filtered_df = result_dfs[i].drop(columns=exclude_columns)
    filtered_df['result'] = filtered_df['result'].str.replace('pass', 'pass<br>pass')
    styled_df = filtered_df.style.applymap(style_cell)
    # .set_properties(**{'text-align': 'center'})

    with cols[i]:
        st.dataframe(styled_df, use_container_width=True, height=800)
        print(styled_df)
        # styled_df['result'] = styled_df['result'].str.replace('pass', 'pass<br>pass')
        styled_df_html = styled_df.to_html(escape=False)

        st.markdown(styled_df_html, unsafe_allow_html=True)






