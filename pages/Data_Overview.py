import altair as alt
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="분석 도구",    # 브라우저 탭 제목
    page_icon= '',
    layout="wide"
)

st.title("데이터 개요")

df = pd.read_csv("sample_data.csv")

st.write("그래프를 선택하세요.")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    chart_type = st.selectbox("차트 종류 선택", ["산점도", "라인 차트", "막대 차트"], index=0)
    filter_by = st.selectbox("Filter by", df.columns, index=0)
with col2:
    x_axis = st.selectbox("x축 선택", df.columns, index=1)
    selected_categories = st.multiselect(
    "차트 필터",
    options=df[filter_by].unique(),
    default=df[filter_by].unique()  # 기본값: 모두 선택
    )
with col3:
    y_axis = st.selectbox("y축 선택", df.columns, index=2)
with col4:
    color_by = st.selectbox("Color by", df.columns, index=0)

filtered_df = df[df[filter_by].isin(selected_categories)]

if st.button("Run"):
    #그래프 생성
    chart = alt.Chart(filtered_df).encode(
        x=x_axis,
        y=y_axis,
        color=color_by,
        tooltip=[x_axis, y_axis]
    ).properties(
        width=600,
        height=400,
        title=f"{y_axis} vs {x_axis}"
    )

    if chart_type == "라인 차트":
        chart = chart.mark_line(point=True)
    elif chart_type == "막대 차트":
        chart = chart.mark_bar()
    elif chart_type == "산점도":
        chart = chart.mark_circle(size=60)
    else:
        chart = chart.mark_line(point=True)

    #그래프 출력
    st.altair_chart(chart, use_container_width=False)
