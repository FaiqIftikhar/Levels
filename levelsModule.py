"""
Module providing the main landing page of the app.
You can start the app by running `py -m streamlit run Levels.py`.
"""

import streamlit as st
from modules.navbar import navBar
from utils import calculateWageUnits, cleanData, changeWagedFactor
from backend.database import database

def setupMainPage():
    """This function calls the necassary streamlit elements to create the main landing page."""
    st.set_page_config(
        page_title="Levels",
        page_icon="💸",
        layout="wide"
    )

    navBar()

    st.title("💸 Levels for your salaries")

    st.sidebar.info("Select a page above.")

    st.markdown(
        """
        This is a small data app that shows salaries in hourly rate across 
        different countries of europe.\n
        👈 You can select one of the views from the sidebar\n
    """
    )

DATABASE = database()

setupMainPage()

st.markdown(
    """
<style>
div[data-testid="stMetricValue"] {
    font-size: 85px;
    background-color: #B2FBA5;
    text-align: center;
    border-radius: 25px;
    font-weight: 900;
}
strong {
    font-size: 22px;
    text-wrap: pretty;
    font-family: Copperplate
}
</style>
""",
    unsafe_allow_html=True,
)


# df = pd.read_csv("Salary_Data.csv")
df = DATABASE.getTableAsDataFrame()

a1, a2, a3 = st.columns(3)
a1.metric('**💯 Number of Levels:**', f"{len(df):,}")
a2.metric("**🚹 Developers that are male:**", f"{int(len(df[df['Gender'] == 'Male'])/len(df)*100)}%")
a3.metric("**👩🏽 Developers that are female:**", f"{int(len(df[df['Gender'] == 'Female']) / len(df)*100)}%")


b1, b2 = st.columns(2)
b1.metric('**🌍 Percentage of Developers from Germany:**', value=f"{int(len(df[df['Country'] == 'Germany']) / len(df)*100)}%")
b2.metric('**🚀 Most of the data is from:**', value=f"{df.City.mode()[0]}")

df = calculateWageUnits(df)

euroData = cleanData()
euroData = changeWagedFactor(euroData, "Hourly")

c1, c2 = st.columns(2)
b1.metric('**📈 Hourly wage in Germany according to Eurostat:**', value=f"€ {euroData[euroData['Country'] == 'Germany']['2024-S1'].iloc[0]}")
b2.metric('**💶 Hourly wage in Germany according to Levels:**', value=f"€ {round(df[df['Number of Hours'] == 20]['Wage_Hourly'].mean(), 2)}")


st.markdown("""Source of all data
        [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/earn_mw_cur__custom_12336095/default/bar?lang=en).""")
