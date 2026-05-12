# EPL_DashBoard
Streamlit을 활용한 EPL(English Premier League) 데이터 시각화 및 통계

대시보드 링크: https://epldashboard-cu44cpdqwbfnbocwszqrdj.streamlit.app/

- 00-01시즌부터 20-21시즌까지의 EPL의 데이터를 활용(출처: kaggle)
- ``team_stats``에선 우승팀과 우승팀의 세부 스텟(득점, 실점, 유효슈팅 정확도, 유효슈팅 득점 확률, 파울 횟수 등)을 확인할 수 있고,
- 심판의 경기 진행 성향도 결과에 중요하기 때문에``Referee Tendencies``에선 시즌 별 심판 성향(경기의 평균 파울, 옐로 카드, 레드 카드 부여 횟수)를 파악할 수 있도록 barplot으로 시각화 
- ``promoted_relegated_team`` 페이지를 통해 이전 시즌에서 승격한 팀, 다음 시즌 2부리그 강등 팀을 나열하였고, 승격한 뒤 바로 강등당한 팀은 Yo-Yo Detection을 통해 확인할 수 있도록 구성