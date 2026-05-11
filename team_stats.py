
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    
    df = pd.read_csv('preprocess_data_2.csv')
    df2 = pd.read_csv('winner_list_2.csv')

    df['HSA'] = (df['HST'] / df['HS']) * 100    # 유효슈팅 / 전체 슈팅 -> 슛 정확도 
    df['HGSR'] = (df['FTHG'] / df['HST']) * 100  # 득점 / 유효 슈팅 -> 득점 성공률 
    
    df['ASA'] = (df['AST'] / df['AS']) * 100
    df['AGSR'] = (df['FTAG'] / df['AST']) * 100
    
    return df, df2

play_df, winner_team = load_data()


home_columns = {
'Season' : 'Match Season',
'HomeTeam' : 'Home Team', 'AwayTeam' : 'Away Team',
'FTHG' : 'Full Time Home Team Goals',
'HS' : 'Home Team Shots',
'HST' : 'Home Team Shots on Target', 
'HSA' : 'Home Team Shots Accuracy(%)',
'HGSR' : 'Home Team Goal Seccess Rate(%)',
'HC' : 'Home Team Corners',
'HF' : 'Home Team Fouls Committed',
'HY' : 'Home Team Yellow Cards',
'HR' : 'Home Team Red Cards'
    
}

away_columns = {
'Season' : 'Match Season',
'HomeTeam' : 'Home Team','AwayTeam' : 'Away Team',
'FTAG' :'Full Time Away Team Goals',
'AS' : 'Away Team Shots',
'AST' : 'Away Team Shots on Target',
'ASA' : 'Away Team Shots Accuracy(%)', 
'AGSR' : 'Away Team Goal Seccess Rate(%)',
'AC' : 'Away Team Corners',
'AF' : 'Away Team Fouls Committed',
'AY' : 'Away Team Yellow Cards',
'AR' : 'Away Team Red Cards',
}


st.title("EPL Winning Team Stats by Season")

st.divider()

with st.sidebar:
    st.header("필터")
    # st.sidebar.divider()
    season_list = winner_team['Season']
    st.sidebar.subheader("우승팀 조회")
    selected_season = st.selectbox("시즌 선택", season_list)

winner_name = winner_team[winner_team['Season'] == selected_season]['Winner'].iloc[0]


st.subheader(f"Season: {selected_season}")
st.subheader(f"Winner: 👑{winner_name}👑")

# 경기결과 그래프

game_result = pd.read_csv('game_result_2.csv')

season_data = game_result[game_result['Season'] == selected_season]
home_game = season_data[season_data['HomeTeam'] == winner_name]
away_game = season_data[season_data['AwayTeam'] == winner_name]


# st.header("Winner Game Results")

col1, col2 = st.columns(2)

with col1:
    st.info(f"{selected_season}, {winner_name}의 Home 성적")
    home_win = len(home_game[home_game['FTR']=='H']) 
    home_draw = len(home_game[home_game['FTR']=='D']) 
    home_lose = len(home_game[home_game['FTR']=='A']) 
    
    home_res = pd.DataFrame({
         'Results':['Win', 'Draw', 'Lose'],
         'Count': [home_win, home_draw, home_lose],
         'Color' : ['#007bff', '#6c757d', '#dc3545']
    })

 
    st.bar_chart(data = home_res, x='Results', y='Count', color='Color', horizontal=True, height=400) 
        

with col2:
    st.info(f"{selected_season}, {winner_name}의 Away 성적")
    away_win =  len(away_game[away_game['FTR']=='A'])
    away_draw = len(away_game[away_game['FTR']=='D'])
    away_lose = len(away_game[away_game['FTR']=='H'])
    
    away_res = pd.DataFrame({
         'Results':['Win', 'Draw', 'Lose'],
         'Count': [away_win, away_draw, away_lose],
         'Color' : ['#007bff', '#6c757d', '#dc3545']
    })
    
    st.bar_chart(data = away_res, x='Results', y='Count', color='Color', horizontal=True, height=400) 

#


st.subheader("Winner Score Metrics")

season_data = play_df[play_df['Season'] == selected_season]
home_game = season_data[season_data['HomeTeam'] == winner_name]
away_game = season_data[season_data['AwayTeam'] ==  winner_name]

# 'FTHG', 'FTAG'  
home_GF = home_game['FTHG'].sum()
home_GA = home_game['FTAG'].sum()

away_GF =  away_game['FTAG'].sum()
away_GA = away_game['FTHG'].sum()

total_GF = home_GF + away_GF 
total_GA = home_GA + away_GA

score_res = pd.DataFrame({
     'Results':['GF', 'GA'],
     'Count': [total_GF, total_GA],
     # 'Color' : ['#28a745', '#fd7e14', '#6f42c1']
     'Color' : ['#003366', '#8B0000']
})

st.bar_chart(data = score_res, x='Results', y='Count', color='Color',  horizontal=True, height=400)


####


st.divider()
select_season_data = play_df[play_df['Season'] == selected_season]

only_home = select_season_data[select_season_data['HomeTeam'] == winner_name]
only_away = select_season_data[select_season_data['AwayTeam'] == winner_name]



st.subheader("HomeTeam stats")
with st.sidebar:
    st.sidebar.divider()
    st.sidebar.subheader("HomeTeam stats")
    item_key = st.selectbox("조회할 스텟 선택 ", list(home_columns.keys())[3:],
                           format_func=lambda x: home_columns[x])

col3, col4 = st.columns(2)

with col3:
    st.info(f"Home ({winner_name})")
    mean_home = np.mean(only_home[item_key]) if not only_home.empty else 0
    st.metric(label = f"{home_columns[item_key]} (Avg)", value = f"{mean_home:.3f}")

with col4:
    st.info(f"Opposition Home (Away: {winner_name})")
    mean_oppo_home = np.mean(only_away[item_key]) if not only_away.empty else 0
    st.metric(label = f"{home_columns[item_key]} (Avg)", value = f"{mean_oppo_home:.3f}")


st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


st.subheader("AwayTeam stats")
with st.sidebar:
    st.sidebar.divider()
    st.sidebar.subheader("AwayTeam stats")
    item_key = st.selectbox("조회할 스텟 선택 ", list(away_columns.keys())[3:],
                           format_func=lambda x: away_columns[x])


col5, col6 = st.columns(2)


with col5:
    st.info(f"Away ({winner_name})")
    mean_away = np.mean(only_away[item_key]) if not only_away.empty else 0
    st.metric(label = f"{away_columns[item_key]} (Avg)", value = f"{mean_away:.3f}")

with col6:
    st.info(f"Opposition Away (Home: {winner_name})")
    mean_oppo_away = np.mean(only_home[item_key]) if not only_home.empty else 0
    st.metric(label = f"{away_columns[item_key]} (Avg)", value = f"{mean_oppo_away:.3f}")
