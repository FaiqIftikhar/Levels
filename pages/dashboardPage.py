"""
This file creates the dashboard page. Generates relevant graphs to show data.
"""

import streamlit as st
import altair as alt
import pandas as pd
from utils import calculateWageUnits, COLORS
from backend.database import database
from modules.navbar import navBar


st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

navBar()

st.title("📊 Dashboard")

st.markdown("""
            **This page can tell you an interesting story ⛩️.**\n
            👈 Choose filters from the sidebar.
            """)

DATABASE = database()

view = st.sidebar.radio("Select how you want to see data: ", options=['Scatter', 'Bar'], index=0, horizontal=True)

class DataFiltering():
    """This class creates a filtering object on top of a dataframe. Then lets you filter the df based on filters defined in the Frontend."""
    def __init__(self, dataFrame) -> None:
        """init function for the class."""
        self.filteredData = dataFrame

    def setCountry(self, country):
        """Sets the Country pivot on the whole data."""
        self.filteredData = self.filteredData[self.filteredData['Country'] == country]

    def setWageUnit(self, wageUnit):
        """Sets the wage unit pivot on the whole data."""
        if wageUnit == 'Yearly':
            self.filteredData['Salary'] = self.filteredData['Wage_Yearly']
            self.filteredData['Wage Unit'] = 'Yearly'
        elif wageUnit == 'Monthly':
            self.filteredData['Salary'] = self.filteredData['Wage_Monthly']
            self.filteredData['Wage Unit'] = 'Monthly'
        elif wageUnit == 'Hourly':
            self.filteredData['Salary'] = self.filteredData['Wage_Hourly']
            self.filteredData['Wage Unit'] = 'Hourly'

    def setHours(self, hours):
        """Sets the wage hours (Part time/Full time) on the whole data."""
        upperBound, lowerBound = 0, 0
        if hours == 'All':
            upperBound, lowerBound = 60, 0
        elif hours == 'Full Time':
            upperBound, lowerBound = 40, 20
        elif hours == 'Part Time':
            upperBound, lowerBound = 20, 0

        self.filteredData = self.filteredData[
            (self.filteredData['Number of Hours'] <= upperBound) & (self.filteredData['Number of Hours'] > lowerBound)
            ]


# df = pd.read_csv("Salary_Data.csv")
df = DATABASE.getTableAsDataFrame()

df = calculateWageUnits(df)


DATAFILTER = DataFiltering(df)

countrySelection = st.sidebar.selectbox('You can select the country here:', options=list(df['Country'].unique()) + ['Bolivia', 'Denmark'], index= 0, key='countrySelection')
DATAFILTER.setCountry(countrySelection)

wageUnitSelection = st.sidebar.selectbox('You can select wage unit here:', options=['Yearly', 'Monthly', 'Hourly'], index=0, key = 'wageUnitSelection')
DATAFILTER.setWageUnit(wageUnitSelection)

workHoursSelection = st.sidebar.selectbox('You can select working hours here:', options=['Full Time', 'Part Time'], index=0, key = 'workHoursSelection')
DATAFILTER.setHours(workHoursSelection)

pivotSelection = st.sidebar.selectbox('You can select here the key column:', options=['City', 'Gender', 'Job Title', 'Tag'], key = 'pivotSelection')


# st.dataframe(DATAFILTER.df)

DOMAIN = DATAFILTER.filteredData[pivotSelection].unique()




salarySelect = alt.selection_point(fields=[pivotSelection])
salaryPie = (
    (
        alt.Chart(DATAFILTER.filteredData,
                  title=alt.Title(
                    'Chart to show scale of data.',
                    color="#8db6d8",
                    fontSize=30,
                    fontWeight=900))
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(
                "Salary",
                type="quantitative",
                aggregate="count",
                title="Number of Input data points",
            ),

            color=alt.Color(
                field=pivotSelection,
                type="nominal",
                scale=alt.Scale(domain=DOMAIN, range=COLORS),
                title=pivotSelection,
            ),
            opacity=alt.condition(salarySelect, alt.value(1), alt.value(0.25)),
        )
    )
    .add_params(salarySelect)
    .properties(width=325)
)

salarySummary = (
    (
        alt.Chart(DATAFILTER.filteredData)
        .mark_bar(cornerRadiusEnd=20)
        .encode(
            xOffset=f"{pivotSelection}:N",
            x=alt.X(
                "Level",
                type="nominal",
                sort=['Fresh Graduate', 'Junior', 'Associate', 'Senior']
            ),
            y=alt.Y(
                field="Salary",
                type="quantitative",
                aggregate="mean",
                title="Average Salary"
            ),
            tooltip=["Level", "Salary", pivotSelection],
            color=alt.Color(
                pivotSelection,
                type="nominal",
                scale=alt.Scale(domain=DOMAIN, range=COLORS),
                legend=alt.Legend(
                    direction="vertical",
                    orient='right',
                    titleColor="#8db6d8",
                    titleFontSize=30,
                    titleFontWeight=900,
                    titleLimit=200,
                    titleLineHeight=10,
                    rowPadding=10,
                    symbolType="circle",
                    tickCount=4,
                ),
            ),
        )
    )
    .transform_filter(salarySelect)
    .properties(width=650)
)

# st.write([i+1 for i in range(0,len(DATAFILTER.filteredData[pivotSelection]))])

salaryScatter = (
    (
        alt.Chart(DATAFILTER.filteredData)
        .mark_circle(size=20)
        .encode(
            # xOffset=f"{pivotSelection}:N",
            x=alt.X(
                "Years",
                type="quantitative",
                # sort=['Fresh Graduate', 'Junior', 'Associate', 'Senior']
            ),
            y=alt.Y(
                field="Salary",
                type="quantitative",
                aggregate="mean",
                title="Average Salary",
                sort="-y"
            ),
            size=alt.Size(pivotSelection, legend=None, scale=alt.Scale(range=[100, 500])),
            tooltip=["Years", "Salary", pivotSelection],
            color=alt.Color(
                pivotSelection,
                type="nominal",
                scale=alt.Scale(domain=DOMAIN, range=COLORS),
                legend=alt.Legend(
                    direction="vertical",
                    orient='right',
                    titleColor="#8db6d8",
                    titleFontSize=30,
                    titleFontWeight=900,
                    titleLimit=200,
                    titleLineHeight=10,
                    rowPadding=10,
                    symbolType="circle",
                    tickCount=4,
                ),
            )
        )
    )
    .transform_filter(salarySelect)
    .properties(width=650)
)

TOPROW = None
if view == 'Scatter':
    TOPROW = salaryPie | salaryScatter
elif view == 'Bar':
    TOPROW = salaryPie | salarySummary

st.altair_chart(TOPROW)
