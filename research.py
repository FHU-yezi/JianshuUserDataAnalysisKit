import streamlit as st
import pandas as pd
from db_config import db, UserData
import plotly.express as px
import sqlite3

st.title("简书用户大数据分析平台")

pages = ["数据概览", "图表分析"]
page = st.sidebar.selectbox("页面", pages)

@st.cache()
def load_data_to_dataframe():
    con = sqlite3.connect("UserData.db")
    df = pd.read_sql("SELECT * FROM userdata", con)
    return df
df = load_data_to_dataframe()
TOTAL_DATA_COUNT = len(UserData)

if page == "数据概览":
    st.header("数据概览")
    st.write("数据总量：", TOTAL_DATA_COUNT)
    st.write("有效数据量：", len(UserData.select(UserData).where(UserData.FTN_count != None)))
elif page == "图表分析":
    graph_type = st.sidebar.selectbox("图表类型", ["折线图", "散点图"])
    samples_count = int(st.sidebar.number_input("样本量", min_value=10, max_value=TOTAL_DATA_COUNT, value=TOTAL_DATA_COUNT))
    df = df.sample(n=samples_count)
    if graph_type == "折线图":
        x = st.sidebar.selectbox("X 轴", list(df.columns))
        y = st.sidebar.selectbox("Y 轴", list(df.columns))
        button = st.sidebar.button("生成图表")
        if button:
            graph = px.line(x=df[x], y=df[y], title=f"{x} 与 {y} 的折线图")
            st.write(graph)
    elif graph_type == "散点图":
        x = st.sidebar.selectbox("X 轴", list(df.columns))
        y = st.sidebar.selectbox("Y 轴", list(df.columns))
        button = st.sidebar.button("生成图表")
        if button:
            graph = px.scatter(x=df[x], y=df[y], title=f"{x} 与 {y} 的散点图")
            st.write(graph)
    