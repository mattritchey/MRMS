# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 09:56:29 2022

@author: mritchey
"""
#streamlit run "C:\Users\mritchey\.spyder-py3\Python Scripts\streamlit projects\mrms\mrms_streamlit.py"
import pandas as pd
import streamlit as st
import webbrowser
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

@st.cache
def geocode(address):
    try:
        address2 = address.replace(' ', '+').replace(',', '%2C')
        df = pd.read_json(
            f'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={address2}&benchmark=2020&format=json')
        results = df.iloc[:1, 0][0][0]['coordinates']
        lat, lon = results['y'], results['x']
    except:
        geolocator = Nominatim(user_agent="GTA Lookup")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        location = geolocator.geocode(address)
        lat, lon = location.latitude, location.longitude
    return pd.DataFrame({'Lat': lat, 'Lon': lon}, index=[0])

#Set Columns
st.set_page_config(layout="wide")
col1, col2 = st.columns((2))

#Input Data
with st.form(key='Form1'):
    with st.sidebar:
        address = st.sidebar.text_input(
            "Address", "123 Main Street, Cincinnati, OH 43215")
        date = st.sidebar.date_input(
            "Date",  pd.Timestamp(2022, 7, 6)).strftime('%Y%m%d')
        var = st.sidebar.selectbox(
            'Product:', ('Hail', 'Flooding', 'Rain: Radar', 'Rain: Multi Sensor', 'Tornado'))
        submitted1 = st.form_submit_button(label='Go to MRMS Site')

year, month, day = date[:4], date[4:6], date[6:]

#Select Variable
if var == 'Hail':
    var_input = 'hails&product=MESHMAX1440M'
elif var == 'Flooding':
    var_input = 'flash&product=FL_ARI24H'
elif var == 'Rain: Radar':
    var_input = 'q3rads&product=Q3EVAP24H'
elif var == 'Rain: Multi Sensor':
    var_input = 'q3mss&product=P1_Q3MS24H'
elif var == 'Tornado':
    var_input = 'azsh&product=RT1440M'

#Geocode
result = geocode(address)
lat, lon = result.values[0]

#Map
m = folium.Map(location=[lat, lon],  zoom_start=12, height=500)
folium.Marker(
    location=[lat, lon],
    popup=address).add_to(m)

with col1:
    st.title('MRMS')
    st_folium(m, height=500)

#Submit Url to New Tab
url = f'https://mrms.nssl.noaa.gov/qvs/product_viewer/index.php?web_exec_mode=run&menu=menu_config.txt&year={year}&month={month}&day={day}&hour=23&minute=30&time_mode=static&zoom=9&clon={lon}&clat={lat}&base=0&overlays=1&mping_mode=0&product_type={var_input}&qpe_pal_option=0&opacity=.75&looping_active=off&num_frames=6&frame_step=200&seconds_step=600'
if submitted1 == True:
    webbrowser.open_new_tab(url)

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)
