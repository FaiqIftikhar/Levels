"""
Module providing the main landing page of the app.
You can start the app by running `py -m streamlit run Levels.py`.
"""

import streamlit as st
from utils import *
from modules.navbar import Navbar

class levels:

    def __init__(self) -> None:
        pass    
    
    def setupMainPage(self):
        st.set_page_config(
            page_title="Levels",
            page_icon="💸",

        )

        Navbar()

        st.title("Levels for your salaries")

        st.sidebar.info("Select a page above.")

        st.markdown(
            """
            This is a small data app that shows salaries in hourly rate across 
            different countries of europe.\n
            **👈 You can select one of the views from the sidebar**\n

            Source of all data 
            [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/earn_mw_cur__custom_12336095/default/bar?lang=en).
        """
        )


LEVELS = levels().setupMainPage()