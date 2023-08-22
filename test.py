import requests
import streamlit as st
import json
st.title("Currency Monitoring")
st.header("Find the latest crypto price updates")

url="https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"

crypto = st.selectbox("Choose a cryptocurrecy",
                      options=["Bitcoin","Ethereum","Litecoin"])
if crypto =="Bitcoin":
    url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"
    response = requests.get(url).json()
    #st.write(response)
    btc_price = response["USD"]
    st.write("The current price of bitcoin in US$ is {}".format(btc_price))
if crypto =="Ethereum":
    url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,JPY,EUR"
    response = requests.get(url).json()
    #st.write(response)
    btc_price = response["USD"]
    st.write("The current price of ethereum in US$ is {}".format(btc_price))
if crypto =="Litecoin":
    url = "https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD,JPY,EUR"
    response = requests.get(url).json()
    #st.write(response)
    btc_price = response["USD"]
    st.write("The current price of litecoin in US$ is {}".format(btc_price))

def currency_converter(cost,currency):
    file = open("api_keys.json")
    json_file = json.load(file)
    #t.write(type(file),type(json_file))
    api_key=json_file["currency_api"]
    url = "https://api.apilayer.com/currency_data/live?access_key="+api_key
    response = requests.get(url).json()
    st.write(response)


st.write(currency_converter(1000,"BTC"))

currency = st.radio("Choose a currency",
                    options=["BRL","EUR","BTC"])
value = st.number_input("Enter cost to be converted.")

if value and currency=="BRL":
    st.subheader("Brazilian Real")
    converted_cost = currency_converter(value,currency)
    st.write("R$ {:.2f} is equivalent to US$ {:.2f}",format(value,converted_cost))
if value and currency=="EUR":
    st.subheader("Euro")
    converted_cost = currency_converter(value,currency)
    st.write("€ {:.2f} is equivalent to US$ {:.2f}",format(value,converted_cost))
if value and currency=="BTC":
    st.subheader("Bitcoin")
    converted_cost = currency_converter(value,currency)
    st.write("{:.2f} bitcoin(s) is equivalent to US$ {:.2f}",format(value,converted_cost))
