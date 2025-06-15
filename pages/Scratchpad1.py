import streamlit as st
import pandas as pd
import plotly.express as px

# 샘플 데이터
df = pd.DataFrame({
    "카테고리": ["A", "A", "B", "B", "C", "C", "C"],
    "서브카테고리": ["A1", "A2", "B1", "B2", "C1", "C2", "C3"],
    "값": [10, 20, 5, 15, 25, 10, 5]
})

st.title("트리맵 + 필터 예제")

# 사용자가 필터링할 카테고리 선택 (멀티셀렉트)
selected_cats = st.multiselect("카테고리 선택", options=df["카테고리"].unique(), default=df["카테고리"].unique())

# 필터 적용
filtered_df = df[df["카테고리"].isin(selected_cats)]

# 트리맵 그리기
fig = px.treemap(
    filtered_df,
    path=["카테고리", "서브카테고리"],
    values="값",
    color="값",
    color_continuous_scale='Viridis'
)

st.plotly_chart(fig, use_container_width=True)