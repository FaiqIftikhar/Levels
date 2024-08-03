"""
This page creates the form to enter wage data into the DB.
"""
import random
import time

import requests
import streamlit as st
from backend.database import Database
from modules.navbar import navBar
from utils import COUNTRIES

st.set_page_config(page_title="Check your level", page_icon="📈")

navBar()

st.title("📈 Enter your LEVEL!")

st.markdown(
    """
    This page lets you enter your wages, for a more rich experience.
    """
)

DATABASE = Database()


def checkDataValidation(dataRow):
    """A simple function to do data validation of the form."""
    if dataRow[2] == "":  # For company name.
        st.toast("Please enter company name.", icon="⛔")
    elif dataRow[3] == "":  # For job title.
        st.toast("Please enter job title.", icon="⛔")
    elif dataRow[0] is None:  # For country.
        st.toast("Please select country.", icon="⛔")
    elif dataRow[1] == "":
        st.toast("Please select city.", icon="⛔")
    else:
        st.toast("Saving data...", icon="⌛")
        result = DATABASE.addRowToTable(dataRow)
        time.sleep(1)
        st.toast(f"Data saved. {result}", icon="✅")
        time.sleep(1)
        st.balloons()


col1, col2 = st.columns(2)


with col1:

    country = st.selectbox(
        "Enter Country",
        options=COUNTRIES,
        placeholder="Select one of the country...",
        index=None,
        key="Country",
    )

    company = st.text_input("Enter your company name:")

    experience = st.selectbox(
        "How many years of experience do you have?",
        options=["0-1 Years", "1-3 Years", "4-6 Years", "7+ Years"],
    )

    match experience:
        case "0-1 Years":
            LEVEL = "Fresh Graduate"
        case "1-3 Years":
            LEVEL = "Junior"
        case "4-6 Years":
            LEVEL = "Associate"
        case "7+ Years":
            LEVEL = "Senior"

    salary = st.number_input(
        "Please enter your salary: ", min_value=1, max_value=100000000
    )
    wageUnit = st.radio(
        "Is the salary Hourly/Monthly/Yearly?",
        options=["Hourly", "Monthly", "Yearly"],
        horizontal=True,
    )

with col2:
    CITY = ""
    if country is not None:
        CITY = st.selectbox(
            "Enter City",
            options=requests.post(
                url="https://countriesnow.space/api/v0.1/countries/cities",
                json={"country": country},
                timeout=10,
            ).json()["data"],
        )
    elif country is None:
        CITY = st.selectbox("Enter City", options=[""], disabled=True)
    jobTitle = st.text_input("Enter the job title you were working as:")

    tag = st.selectbox(
        "Please select what area you are working in:",
        options=[
            "Full Stack",
            "Frontend",
            "Backend",
            "Academia",
            "Mobile Dev",
            "Machine Learning",
            "Data Science",
            "DevOps",
            "Artificial Intelligence",
            "UI/UX",
            "Security",
        ],
    )

    numberOfHours = st.number_input(
        "Please enter number of hours you work in a week:", min_value=1, max_value=40
    )

    gender = st.radio(
        "Please select a gender:",
        options=["Female", "Male", "Prefer not to say"],
        horizontal=True,
    )

    yearsLowerBound = int(experience[0])
    yearsUpperBound = 12 if int(experience[0]) == 7 else int(experience[2])

    YEARS = round(random.uniform(yearsLowerBound, yearsUpperBound), 2)

st.button(
    ":green[Save data ➡️]",
    on_click=checkDataValidation,
    args=(
        [
            country,
            CITY,
            company,
            jobTitle,
            tag,
            numberOfHours,
            "Euro",
            gender,
            salary,
            wageUnit,
            experience,
            LEVEL,
            YEARS,
        ],
    ),
    use_container_width=True,
)
