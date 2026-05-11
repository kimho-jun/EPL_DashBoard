
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 페이지 간 공통 데이터 공유 위한 캐싱
@st.cache_data
def load_data():
    df = pd.read_csv('data/preprocess_data.csv')
    df2 = pd.read_csv('data/winner_list.csv')
        
    df['HSA'] = (df['HST'] / df['HS']) * 100
    df['HGSR'] = (df['FTHG'] / df['HST']) * 100
    
    df['ASA'] = (df['AST'] / df['AS']) * 100
    df['AGSR'] = (df['FTAG'] / df['AST']) * 100

        
    return df, df2

play_df, winner_team = load_data()

with st.sidebar:
    season_list = winner_team['Season']
    st.sidebar.subheader("필터")
    selected_season = st.selectbox("시즌 선택", season_list)


referee_columns ={
    'TF' : 'Total Fouls Committed',
    'TY' : 'Total Yellow Cards',
    'TR' : 'Total Red Cards'
}
    

st.subheader(f"EPL, [{selected_season}] Referee Tendencies (AVG)")

referee_data=pd.read_csv('data/Referee_data.csv')
filtered_season = referee_data[referee_data['Season'] == selected_season]
grouping = filtered_season.groupby(['Season','Referee'], as_index=False).mean()



with st.sidebar:
    st.sidebar.divider()
    st.sidebar.subheader("Referee Stats")
    item_key = st.selectbox("판정 결과", list(referee_columns.keys()),
                           format_func=lambda x: referee_columns[x])


fig = px.bar(grouping, x=item_key, y='Referee', orientation='h')
fig.update_layout(height=1000)
fig.update_yaxes(dtick=1)
st.plotly_chart(fig)
