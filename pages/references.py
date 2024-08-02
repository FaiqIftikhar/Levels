"""This page provides all the references of the data used to build the app."""

import streamlit as st
from modules.navbar import navBar


st.set_page_config("Data references", page_icon="📖", layout="wide")

navBar()

st.title("📖 This page tells you the sources that were used in the app.")

st.subheader("The data used for Eurostat is pulled from [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/earn_mw_cur__custom_12336095/default/bar?lang=en).")

st.subheader("The dummy wage data for graphs is pulled from [levels.fyi](https://www.levels.fyi/?compare=Delivery%20Hero,Deutsche%20Bank,Bosch%20Global&track=Software%20Engineer).")

st.subheader("Some of the dummy data is also compared with [glassdoor](https://www.glassdoor.de/Job/index.htm).")

st.subheader("The logo of the app on the left is copied from [stackoverflow](https://survey.stackoverflow.co/2024/).")
