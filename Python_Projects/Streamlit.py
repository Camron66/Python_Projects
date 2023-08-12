import json
import time

import requests
import pandas as pd
import numpy as np
import streamlit as st

url = "https://api-nba-v1.p.rapidapi.com/players/statistics"
url_2 = "https://api-nba-v1.p.rapidapi.com/teams/statistics"
url_3 = "https://api-nba-v1.p.rapidapi.com/standings"
url_4 = "https://api-nba-v1.p.rapidapi.com/teams"

headers = {
    'x-rapidapi-key': 'b45e353113mshe1d8e3bdfa132c1p116028jsne02a0529a562',
    'x-rapidapi-host': 'api-nba-v1.p.rapidapi.com'
}

st.set_page_config(
    page_title="NBA Statistics",
    layout="wide",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'About': '# Project #2, Developed by Camron Cisneros'
    }
)

st.title("NBA Statistics")
st.header("Camron Cisneros")

add_selectbox = st.sidebar.selectbox(
    "Select a Category",
    ["Homepage", "Compare", "Divisions", "Standings","Soccer Stadium Map"]
)
if add_selectbox == "Compare":
    st.subheader("Input two teams below and compare the blocks, steals, assists, points, and rebound totals")
    team = st.text_input("Input team 1 here", "Lakers")
    team1_response = requests.get(url_4, headers=headers, params={"search": team}).json()
    team1_r = team1_response["response"]

    team2 = st.text_input("Input team 2 here", "Heat")
    team2_response = requests.get(url_4, headers=headers, params={"search": team2}).json()
    team2_r = team2_response["response"]

    team1_id = team1_r[0]["id"]
    team1_statistics_response = requests.get(url_2, headers=headers, params={"id": team1_id, "season": "2022"}).json()
    team1_statistics_r = team1_statistics_response["response"]

    team2_id = team2_r[0]["id"]
    team2_statistics_response = requests.get(url_2, headers=headers, params={"id": team2_id, "season": "2022"}).json()
    team2_statistics_r = team2_statistics_response["response"]

    table1 = pd.DataFrame(
        [team1_statistics_r[0], team2_statistics_r[0]],
        index=[team1_r[0]["name"], team2_r[0]["name"]],
        columns=["blocks", "steals", "assists", "points", "totReb"]
    )
    if st.button("Generate Table"):
        st.dataframe(table1)
    if st.checkbox("Generate Charts"):
        st.area_chart(table1)
        st.line_chart(table1)

elif add_selectbox == "Divisions":
    genre = st.radio(
        "Which Division Would you like to observe?",
        ("Atlantic", "Pacific", "Northwest", "Central", "Southwest", "Southeast")
    )
    if genre == "Atlantic":
        atlantic_team = requests.get(url_4, headers=headers, params={"division": "Atlantic"}).json()
        atlantic_teams = atlantic_team["response"]
        atlantic_table = pd.DataFrame(
            atlantic_teams,
            index=[1, 2, 3, 4, 5],
            columns=["name"]
        )
        st.dataframe(atlantic_table)
        st.success("You have selected the Atlantic Division")
    if genre == "Pacific":
        pacific_team = requests.get(url_4, headers=headers, params={"division": "Pacific"}).json()
        pacific_teams = pacific_team["response"]
        pacific_table = pd.DataFrame(
            pacific_teams,
            index=[1, 2, 3, 4, 5],
            columns=["name"]
        )
        st.dataframe(pacific_table)
        st.success("You have selected the Pacific Division")
    if genre == "Central":
        central_team = requests.get(url_4, headers=headers, params={"division": "Central"}).json()
        central_teams = central_team["response"]
        central_table = pd.DataFrame(
            central_teams,
            index=[1, 2, 3, 4, 5],
            columns=["name"]
        )
        st.dataframe(central_table)
        st.success("You have selected the Central Division")
    if genre == "Northwest":
        northwest_team = requests.get(url_4, headers=headers, params={"division": "Pacific"}).json()
        northwest_teams = northwest_team["response"]
        northwest_table = pd.DataFrame(
            northwest_teams,
            index=[1, 2, 3, 4, 5],
            columns=["name"]
        )
        st.dataframe(northwest_table)
        st.success("You have selected the Northwest Division")
    if genre == "Southwest":
        southwest_team = requests.get(url_4, headers=headers, params={"division": "Southwest"}).json()
        southwest_teams = southwest_team["response"]
        southwest_table = pd.DataFrame(
            southwest_teams,
            index=[1, 2, 3, 4, 5],
            columns=["name"]
        )
        st.dataframe(southwest_table)
        st.success("You have selected the Southwest Division")
    if genre == "Southeast":
        southeast_team = requests.get(url_4, headers=headers, params={"division": "Southeast"}).json()
        southeast_teams = southeast_team["response"]
        southeast_table = pd.DataFrame(
            southeast_teams,
            index=[1, 2, 3, 4, 5],
            columns=["name"]
        )
        st.dataframe(southeast_table)
        st.success("You have selected the Southeast Division")

elif add_selectbox == "Standings":
    standings_r = requests.get(url_3, headers=headers, params={"league": "standard", "season": 2022}).json()
    standings_response = standings_r["response"]
    teams = st.multiselect(
        'What are your favorite teams',
        [
            standings_response[0]["team"]["name"], standings_response[1]["team"]["name"],
            standings_response[2]["team"]["name"], standings_response[3]["team"]["name"],
            standings_response[4]["team"]["name"], standings_response[5]["team"]["name"],
            standings_response[6]["team"]["name"], standings_response[7]["team"]["name"],
            standings_response[8]["team"]["name"], standings_response[9]["team"]["name"],
            standings_response[10]["team"]["name"], standings_response[11]["team"]["name"],
            standings_response[12]["team"]["name"], standings_response[13]["team"]["name"],
            standings_response[14]["team"]["name"], standings_response[15]["team"]["name"],
            standings_response[16]["team"]["name"], standings_response[17]["team"]["name"],
            standings_response[18]["team"]["name"], standings_response[19]["team"]["name"],
            standings_response[20]["team"]["name"], standings_response[21]["team"]["name"],
            standings_response[22]["team"]["name"], standings_response[23]["team"]["name"],
            standings_response[24]["team"]["name"], standings_response[25]["team"]["name"],
            standings_response[26]["team"]["name"], standings_response[27]["team"]["name"],
            standings_response[28]["team"]["name"], standings_response[29]["team"]["name"]],
        [
            standings_response[0]["team"]["name"], standings_response[2]["team"]["name"],
            standings_response[3]["team"]["name"]],
    )
    stat1 = st.select_slider(
        "Which Statistic do you want to select?",
        options=("Winning Statistics", "Losing Statistics", "Extra Statistics")
    )

    def search(team):
        search_response = requests.get(url_4, headers=headers, params={"search": team}).json()
        team_id = search_response["response"][0]["id"]
        team_standings = requests.get(url_3, headers=headers,
                                  params={"league": "standard", "season": 2022, "team": team_id}).json()
        return team_standings["response"]
    search_button = st.button("Search for Statistics")

    all_teams = []
    for i in teams:
        time.sleep(.001)
        all_teams.append(search(i))
    if stat1 == "Winning Statistics":
        if search_button:
            winning_table = pd.DataFrame(
                [all_teams[0][0]["win"],
                 all_teams[1][0]["win"],
                 all_teams[2][0]["win"]],
                index=[all_teams[0][0]["team"]["name"],
                       all_teams[1][0]["team"]["name"],
                       all_teams[2][0]["team"]["name"]],
                columns=["total","percentage","lastTen"]
            )
            st.dataframe(winning_table)
            st.bar_chart(winning_table)
            st.info("The", all_teams[0][0]["team"]["name"], "have the most wins, with", all_teams[0][0]["win"]["total"], "total wins")

    elif stat1 == "Losing Statistics":
        if search_button:
            losing_table = pd.DataFrame(
                [all_teams[0][0]["loss"],
                 all_teams[1][0]["loss"],
                 all_teams[2][0]["loss"]],
                index=[all_teams[0][0]["team"]["name"],
                       all_teams[1][0]["team"]["name"],
                       all_teams[2][0]["team"]["name"]],
                columns=["total", "percentage", "lastTen"]
            )
            st.dataframe(losing_table)
            st.bar_chart(losing_table)
            st.info("The", all_teams[2][0]["team"]["name"], "have the most losses, with", all_teams[0][0]["loss"]["total"], "total losses")

    elif stat1 == "Extra Statistics":
        if search_button:
            extra_table = pd.DataFrame(
                [all_teams[0][0],
                 all_teams[1][0],
                 all_teams[2][0]],
                index=[all_teams[0][0]["team"]["name"],
                       all_teams[1][0]["team"]["name"],
                       all_teams[2][0]["team"]["name"]],
                columns=["gamesBehind", "streak", "winStreak","tieBreakerPoints"]
            )
            st.dataframe(extra_table)
            st.bar_chart(extra_table)

elif add_selectbox == "Soccer Stadium Map":
    soccer_stadiums = pd.read_csv("csv/SoccerStadiumCoordinates.csv")
    st.dataframe(soccer_stadiums)
    st.caption("Soccer Stadium table")
    st.map(soccer_stadiums)
    st.caption("Soccer Stadium map")

else:
    st.write("This is a NBA statistics website, browse the sidebar to view the abilities")
    st.info("If there is an KeyError: 'response' then the there were too many api calls")
