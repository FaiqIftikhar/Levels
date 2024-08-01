"""
This page creates the form to enter wage data into the DB.
"""
import streamlit as st
import pandas as pd
from utils import COUNTRIES
import requests
import time
from modules.navbar import navBar

st.set_page_config(page_title="Check your level", page_icon="📈")

navBar()

st.title("📈 Enter your LEVEL!")

st.markdown("""
            This page lets you enter your wages, for a more rich experience. 
            """)



def check_data_validation(company, job_title, country, city, tag, number_of_hours, gender, salary, wage_unit, experience, level):
    """A simple function to do data validation of the form."""
    if company == '':
        st.toast("Please enter company name.", icon="⛔")
    elif job_title == '':
        st.toast("Please enter job title.", icon="⛔")
    elif country is None:
        st.toast("Please select country.", icon="⛔")
    else:
        st.toast("Saving data...", icon="⌛")
        df = pd.DataFrame([[country, city, company, job_title, tag, number_of_hours, 'Euro', gender, salary, wage_unit, experience, level]],
            columns=['Country', 'City', 'Company', 'Job Title', 'Tag', 'Number of Hours', 'Currency', 'Gender', 'Salary', 'Wage Unit', 'Years of Experience', 'Level']
            )
        original_df = pd.read_csv("Salary_Data.csv")
        original_df = pd.concat([original_df, df], axis=0).reset_index(drop=True)
        # print(original_df)
        original_df.to_csv("Salary_Data.csv", index=False)
        time.sleep(1)
        st.toast("Data saved.", icon="✅")
        time.sleep(1)
        st.balloons()

col1, col2 = st.columns(2)


with col1:
    country = ''
    
    country = st.selectbox("Enter Country", options=COUNTRIES, placeholder="Select one of the country...", index=None, key='Country')
    
    company = st.text_input("Enter your company name:")
    
    experience = st.selectbox("How many years of experience do you have?", options=['0-1 Years', '1-3 Years', '4-6 Years', '7+ Years'])

    level = ''

    match experience:
        case '0-1 Years':
            level = 'Fresh Graduate'
        case '1-3 Years':
            level = 'Junior'
        case '4-6 Years':
            level = 'Associate'
        case '7+ Years':
            level = 'Senior'

    salary = st.number_input("Please enter your salary: ", min_value=1, max_value=100000000)
    wage_unit = st.radio("Is the salary Hourly/Monthly/Yearly?", options=['Hourly', 'Monthly', 'Yearly'], horizontal=True)
    
with col2:
    if country != None:
        city = st.selectbox("Enter City", 
                            options=requests.post(
                                url = "https://countriesnow.space/api/v0.1/countries/cities",
                                json = {
                                    "country": country
                                }
                            ).json()['data']
        )
    elif country is None:
        city = st.selectbox("Enter City", options=[''],
                            disabled=True
        )
    job_title = st.text_input("Enter the job title you were working as:")
    tag = st.selectbox("Please select what area you are working in:", options=[
        'Full Stack', 'Frontend', 'Backend', 'Academia', 'Mobile Dev', 'Machine Learning', 'Data Science', 'DevOps', 'Artificial Intelligence', 'UI/UX', 'Security'
    ])
    number_of_hours = st.number_input("Please enter number of hours you work in a week:", min_value=1, max_value=40)

    gender = st.radio(
        "Please select a gender:", options=['Female', 'Male', 'Prefer not to say'], horizontal=True
    )


st.button(":green[Save data ➡️]",
            on_click=check_data_validation,
            args=(company, job_title, country, city, tag, number_of_hours, gender, salary, wage_unit, experience, level,),
            use_container_width=True
        )
