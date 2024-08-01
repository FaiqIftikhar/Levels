"""A simple module to showcase the hand-drawn animation of europe wage data."""

import streamlit as st
from utils import showEuroStatData, COUNTRIES
from modules.navbar import navBar

st.set_page_config(page_title="Europe Data", page_icon="🇪🇺")

navBar()

st.title("💶 European National Data")

st.markdown("""
            This page shows stats of national wages of different countries within europe.
            """)


showEuroStatData(COUNTRIES)
