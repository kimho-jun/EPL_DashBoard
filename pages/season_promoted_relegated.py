
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('data/preprocess_data.csv')
    df2 = pd.read_csv('data/winner_list.csv')
        
    df['HSA'] = (df['HST'] / df['HS']) * 100
    df['HGSR'] = (df['FTHG'] / df['HST']) * 100
    
    df['ASA'] = (df['AST'] / df['AS']) * 100
    df['AGSR'] = (df['FTAG'] / df['AST']) * 100

        
    return df, df2

_, winner_team = load_data()

play_data = pd.read_csv("data/results.csv", encoding='cp949')
play_df = play_data[2824-380:10804].reset_index(drop=True) # 99-00 시즌 ~ 20-21 시즌 필터링
team_list_data = play_df.groupby('Season')['HomeTeam'].unique()
season_list = winner_team['Season']


team_2122 = np.array([
    'Man City', 'Liverpool', 'Chelsea', 'Tottenham', 'Arsenal', 
    'Man United', 'West Ham', 'Leicester', 'Brighton', 'Wolves', 
    'Newcastle', 'Crystal Palace', 'Brentford', 'Aston Villa', 'Southampton', 
    'Everton', 'Leeds', 'Burnley', 'Watford', 'Norwich'
])

team_list_data.loc['2021-22'] = team_2122 


promoted = []
relegated = []
for i in range(len(team_list_data)):
    if i != 21:
        promoted.append(np.setdiff1d(team_list_data.iloc[i+1], team_list_data.iloc[i]))
        relegated.append(np.setdiff1d(team_list_data.iloc[i+1], team_list_data.iloc[i+2]))
    elif i == 21:
        break

season_team_list = pd.DataFrame(
    {'Season' : season_list,
     'promoted': promoted,
     'relegated': relegated
    }
)

##############

with st.sidebar:
    season_list = winner_team['Season']
    st.sidebar.subheader("필터")
    selected_season = st.selectbox("시즌 선택", season_list)


st.subheader(f"[{selected_season}] Promoted & Relegated Team")
st.divider()

filtered_season = season_team_list[season_team_list['Season'] == selected_season]
promoted_team = filtered_season['promoted'].iloc[0]
relegated_team = filtered_season['relegated'].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⬆️Promoted")
    st.caption(f"Joined EPL from **Previous Season**")
    for team in promoted_team:
        st.markdown(
            f"""<div style='background-color:#2ecc71; color:white; padding:5px 15px; 
            border-radius:10px; margin-bottom:5px; text-align:center; font-weight:bold;'>
            {team}</div>""", 
            unsafe_allow_html=True
        )

with col2:
    st.markdown("### ⬇️ Relegated")
    st.caption(f"Heading to 2nd Division for **Next Season**")
    for team in relegated_team:
        st.markdown(
            f"""<div style='background-color:#e74c3c; color:white; padding:5px 15px; 
            border-radius:10px; margin-bottom:5px; text-align:center; font-weight:bold;'>
            {team}</div>""", 
            unsafe_allow_html=True
        )

yoyo_team = []
for team in promoted_team:
    if team in relegated_team:
        yoyo_team.append(team)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.subheader(f"Yo-Yo Detection")
st.caption('Immediate Return to 2nd Division(One-Season Stay)')
for team in yoyo_team:
        st.markdown(
            f"""<div style='background-color:#2980b9; color:white; padding:5px 15px; 
            border-radius:10px; margin-bottom:5px; text-align:center; font-weight:bold;'>
            🔁 {team}</div>""", 
            unsafe_allow_html=True
        )
