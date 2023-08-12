import streamlit as st
import json
import requests
import pandas as pd
import numpy as np

urlData = "https://api.airvisual.com/v2/city?city= &state= &country= &key=04fbbc5c-00d3-4e6e-8e8e-1073eadbb3e3"

st.set_page_config(
    page_title="Air Quality Index",
    layout="wide",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'About': '# Project #2, Developed by Camron Cisneros'
    }
)
st.title("Air Quality Index")
st.header("Camron Cisneros")

sidebar = st.sidebar.selectbox(
    "Select a Category",
    ["Country/State/City", "Nearest City", "Latitude/Longitude"]
)

if sidebar == "Country/State/City":
    urlCountry = "https://api.airvisual.com/v2/countries?key=04fbbc5c-00d3-4e6e-8e8e-1073eadbb3e3"
    country_response = requests.get(urlCountry).json()
    countryNames = []
    for dictionary in country_response["data"]:
        for key,value in dictionary.items():
            countryNames.append(value)
    country = st.selectbox("country",countryNames)
    if country:
        urlState = "https://api.airvisual.com/v2/states?country=" + country + "&key=04fbbc5c-00d3-4e6e-8e8e-1073eadbb3e3"
        state_response = requests.get(urlState).json()
        stateNames = []
        for dictionary in state_response["data"]:
            for key,value in dictionary.items():
                stateNames.append(value)
        state = st.selectbox("State", stateNames)
    if state:
        urlCity = "https://api.airvisual.com/v2/cities?state=" + state + "&country=" + country +"&key=04fbbc5c-00d3-4e6e-8e8e-1073eadbb3e3"
        city_response = requests.get(urlCity).json()
        cityNames = []
        if city_response["data"]["message"] == "Too Many Requests":
            city = st.error("Too Many Requests")
        elif city_response["status"] == "fail":
            city = st.error("There is no data for this Country's State")
        else:
            for dictionary in city_response["data"]:
                if len(dictionary) > 1:
                    for key,value in dictionary.items():
                        value = type(value) == str
                        cityNames.append(value)
                else:
                    cityNames = city_response["data"]["city"]
            city = st.selectbox("City", cityNames)

            urlData = "https://api.airvisual.com/v2/city?city="+city+"&state="+state+"&country="+country+"&key=04fbbc5c-00d3-4e6e-8e8e-1073eadbb3e3"
