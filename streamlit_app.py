import json
import requests
import pandas as pd
import numpy as np
import streamlit as st
from datetime import date, time
import time as tm
import pydeck as pdk
import plotly.express as px
st.set_page_config(
    page_title="HCI - Streamlit",
    layout="wide",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a Bug': 'https://www.gregoryreis.com',
        'About': '# Project #2, Developed by Camron Cisneros'
    }
)

st.title("Project #2")
st.header("HCI - Prof Gregory Murad Reis, PhD")

add_selectbox = st.sidebar.selectbox(
    "Select a Project",
    ["Homepage","Geological periods","US capitals", "BBC Campus","Crypto","NASA"]
)
if add_selectbox == "Geological periods":
    col1, col2, col3, = st.columns(3)
    with col1:
        geological_periods = pd.DataFrame(
            {
                "Geological Period":["Quaternary","Neogene","Paleogene","Cretaceous","Jurassic","Triassic"],
                "Millions of Years":[2.588,23.03,66,145.5,201.3,252.17]
            }
        )
        st.dataframe(geological_periods)
        st.caption("Geological Periods in millions of years ago")
    with col2:
        st.image("media/sedona_usa.jpeg")
        st.caption("Sedona, Arizona, USA, by Edmundo Mendez Jr. 2020")
    with col3:
        st.video("media/volcano.mp4")
        st.video("A video Captured by Martin Sanchez")

elif add_selectbox == "US capitals":
    col1,col2 = st.columns(2)
    with col1:
        usa_capitals = pd.read_csv("csv/capitals_usa.csv")
        st.dataframe(usa_capitals)
        st.caption("Table of the 50 USA States and Capitals")
    with col2:
        st.map(usa_capitals)
        st.caption("Map of the USA Capitals")

elif add_selectbox == "BBC Campus":
    st.subheader("1 - Map - Water Quality Parameters")
    uploaded_file = st.file_uploader("Choose a CSV file (if none i provided, a default data set will be shown")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv("csv/biscayne_bay_dataset_dec_2021.csv")

    zoom_lat = df["latitude"].mean()
    zoom_long = df["longitude"].mean()

    st.pydeck_chart(pdk.Deck(
    # map_style https://docs.mapbox.com/api/maps/styles/
    map_style='mapbox://styles/mapbox/satellite-streets-v11',
    initial_view_state=pdk.ViewState(
        latitude=zoom_lat,
        longitude=zoom_long,
        zoom=18,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[longitude, latitude]',
            get_color='[26, 255, 0, 160]',
            get_radius=0.25,
            pickable=True,
        ),
    ],
    tooltip={
        "html": "Lat: {latitude} <br/> Long:{longitude} <br/> ODO(mg/L):{ODO (mg/L)} <br/>"
                "Temp(C): {Temperature (C)} <br/> pH: {pH} <br/> TWC(m): {Total Water Column (m)} <br/>",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
))
    with st.expander("See definitions for the water quality parameters"):
        st.write("- Total Water Column (m): measure of depth from the surface to the bottom of the ocean \n"
                 "- Temperature (C): Physical Property that expresses the average thermal energy there is"
                 "\n- pH: measure of how acidic or basic the water is, ranging from 0 to 14, with 7 being nuetral. < 7 indicates acidity, wheareas > 7 indicates basic"
                 "\n- ODO (mg/L): concentration of molecular oxygen dissolved")

    st.subheader("2 - Plots - Water Quality Parameters")
    col1,col2 = st.columns(2)

    with col1:
        water_parameter = st.radio(
            "Select water parameter",
            ["ODO (mg/L)", "Temperature (C)", "pH", "Total Water Column (m)"]
        )
    with col2:
        color = st.color_picker("Pick a color", "#00f900")
        st.write("The chosen color is", color)

    if water_parameter:
        fig = px.line(
            df,
            x=df.index,
            y=water_parameter,
            title=water_parameter
        )
        fig.update_traces(line_color=color)
        st.plotly_chart(fig)

    st.subheader("3 - 3D Plot for the Total Water Column")
    fig2 = px.scatter_3d(df,
                        x="longitude",
                        y="latitude",
                        z="Total Water Column (m)",
                        color="Total Water Column (m)")
    fig2.update_scenes(zaxis_autorange="reversed")
    fig2.update_scenes(xaxis_autorange="reversed")
    fig2.update_scenes(yaxis_autorange="reversed")
    st.plotly_chart(fig2)

    st.subheader("4 - Table - Water Quality Parameters")
    parameters=st.multiselect(
        "Select One or More Parameters",
        ["ODO (mg/L)", "Temperature (C)", "pH", "Total Water Column (m)"]
    )
    st.dataframe(df[["latitude","longitude"]+parameters])

    st.subheader("5 - Descriptive Statistics - Water Quality Parameters")
    st.dataframe(df.describe())

elif  add_selectbox == "Crypto":
    st.title("Currency Monitoring")
    st.header("Find the latest crypto price updates")

    url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"

    crypto = st.selectbox("Choose a cryptocurrecy",
                          options=["Bitcoin", "Ethereum", "Litecoin"])
    if crypto == "Bitcoin":
        url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"
        response = requests.get(url).json()
        # st.write(response)
        btc_price = response["USD"]
        st.write("The current price of bitcoin in US$ is {}".format(btc_price))
    if crypto == "Ethereum":
        url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,JPY,EUR"
        response = requests.get(url).json()
        # st.write(response)
        btc_price = response["USD"]
        st.write("The current price of ethereum in US$ is {}".format(btc_price))
    if crypto == "Litecoin":
        url = "https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD,JPY,EUR"
        response = requests.get(url).json()
        # st.write(response)
        btc_price = response["USD"]
        st.write("The current price of litecoin in US$ is {}".format(btc_price))


    def currency_converter(cost, currency):
        file = open("api_keys.json")
        json_file = json.load(file)
        # t.write(type(file),type(json_file))
        api_key = json_file["currency_api"]
        url = "http://api.currencylayer.com/live?access_key=" + api_key
        response = requests.get(url).json()
        desiredCurrency = "USD"+currency
        value2 = response[desiredCurrency]
        converted_cost = cost/value2
        return converted_cost


    st.write(currency_converter(1000, "BTC"))

    currency = st.radio("Choose a currency",
                        options=["BRL", "EUR", "BTC"])
    value = st.number_input("Enter cost to be converted.")

    if value and currency == "BRL":
        st.subheader("Brazilian Real")
        converted_cost = currency_converter(value, currency)
        st.write("R$ {:.2f} is equivalent to US$ {:.2f}", format(value, converted_cost))
    if value and currency == "EUR":
        st.subheader("Euro")
        converted_cost = currency_converter(value, currency)
        st.write("€ {:.2f} is equivalent to US$ {:.2f}", format(value, converted_cost))
    if value and currency == "BTC":
        st.subheader("Bitcoin")
        converted_cost = currency_converter(value, currency)
        st.write("{:.2f} bitcoin(s) is equivalent to US$ {:.2f}", format(value, converted_cost))

elif add_selectbox == "NASA":
    nasa_api = open("nasa_api.json")
    nasa_api = json.load(nasa_api)  # dictionary
    api_key = nasa_api["nasa_api"]  # string

    apod_url = "https://api.nasa.gov/planetary/apod?api_key=" + api_key

    response = requests.get(apod_url).json()

    st.subheader("Astronomy Picture of the Day: " + response["title"])
    st.text("Today is " + response["date"])

    st.image(response["url"],
             caption="Image credit: " + response["copyright"],
             width=360)

    explanation = st.checkbox("Click here for an explanation")
    if explanation:
        st.write(response["explanation"])

    st.subheader("Mars Rover Photos")

    mars_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=100&api_key=" + api_key
    response2 = requests.get(mars_url).json()

    # st.write(response2) # temporarily

    cameraChoice = st.selectbox("Please select a camera:",
                                options=["",
                                         "Front Hazard Avoidance Camera",
                                         "Rear Hazard Avoidance Camera",
                                         "Mast Camera",
                                         "Chemistry and Camera Complex",
                                         "Navigation Camera"])

    if cameraChoice:
        for i in response2["photos"]:
            if i["camera"]["full_name"] == cameraChoice:
                st.image(i["img_src"], width=360)

else:
    st.subheader("PID : 6187231"
                 "Date : 11/2/2022")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    major = st.selectbox('What is your major',
                         ["", "Computer Science", "Information Technology", "Cybersecurity", "Data Science"])
    campus = st.radio('Which campus are you at?',
                      ["MMC", "BBC", "EC"])
    date_started = st.text_input("Start date at FIU")
    today = date.today().year

    if first_name and last_name and major and campus and date_started:
        st.write("Hi,", first_name, "! You have been at FIU", campus, "for", str(today - date_started.year),
                 "years studying",
                 major, ".")

    st.subheader("Streamlit Features")

    basic_plots = st.checkbox("Basic Plots")
    if basic_plots:
        chart_data = pd.DataFrame(
            np.random.rand(20, 4),
            columns=["A", "B", "C","D"])
        st.line_chart(chart_data)

    sliders = st.checkbox("Sliders")
    if sliders:
        st.info("Integer slider for age")
        age = st.slider("How old are you?",0,130,21)
        st.write("I'm,",str(age),"years old.")

        st.info("Time Slider for appointment")
        appointment = st.slider(
            "Schedule your appointment:",
            value = (time(11,30),time(12,45))

        )
        st.write("You're scheduled for:",
                 appointment[0].strftime("%H:%M"),
                 "to", appointment[1].strftime("%H:%M"))

        st.info("Float Slider for range")
        values = st.slider("Select a range of values",
                           0.0,100.0,(25.0,75.0))
        st.write("Values:",str(values))
    audio = st.checkbox("Audio")
    if audio:
        st.write("Waves and Birds")
        st.audio("https://bigsoundbank.com/UPLOAD/mp3/0267.mp3", format="media/mp3", start_time=0)

    boxes = st.checkbox("Boxes")
    if boxes:
        st.success("This is a success box")
        st.warning("This is a warning box")
        st.error("This is an error box")
        st.info("This is an info box")

    balloons = st.checkbox("Surprise")
    if balloons:
        st.balloons()

    progress_bar = st.checkbox("Progress Bar")
    if progress_bar:
        latest_iteration = st.empty()
        bar = st.progress(0)
        for i in range(100):
            latest_iteration.text(f'Iteration {i+1}')
            bar.progress(i+1)
            tm.sleep(0.01)

