"""
This is the utils file, it contains all the utilitarian functions, variables and constants.
"""

import warnings
import time
import streamlit as st
import pandas as pd

COLORS = [
    "#aa423a",
    "#f6b404",
    "#327a88",
    "#303e55",
    "#c7ab84",
    "#b1dbaa",
    "#feeea5",
    "#3e9a14",
    "#6e4e92",
    "#c98149",
    "#d1b844",
    "#8db6d8",
]


COUNTRIES = ['Germany', 'Austria', 'Luxembourg', 'France', 'Spain', 'Portugal', 'Netherlands']


@st.cache_data
def changeWagedFactor(df, wageFactor = 'Monthly'):
    """Function to change the wage factor in the dataset. Mainly used for Eurostat dataset."""
    factor = 1
    if wageFactor == 'Hourly':
        factor = 4*40

    for col in df.columns:
        if col == 'Country':
            df[col] = df[col]
        else:
            df[col] = (df[col] / factor).round(2)
    return df

def readExcelNoWarnings(fileName, sheetName = 'Sheet 1', header = 7):
    """This function is just there to suppress any warning while reading excel files."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return pd.read_excel(fileName, sheet_name=sheetName, header=header)

@st.cache_data
def cleanData():
    """This function cleans all the mess in the Eurostat data and returns it."""
    columnsData = readExcelNoWarnings("earn_mw_cur_spreadsheet.xlsx", sheetName='Sheet 1', header=7).columns
    columnsToDrop = [col for col in columnsData if 'Unnamed' in col]
    # cols_to_drop += [f"{i}-S{j}" for i in range(1999, 2014) for j in range(1,3)]
    return readExcelNoWarnings("earn_mw_cur_spreadsheet.xlsx",
                               sheetName='Sheet 1',
                               header=7
            ).drop(
                list(columnsToDrop), axis=1
            ).drop(
                [0, 38, 39, 40, 41, 42]
            ).reset_index(
                drop=True
            ).rename(
                columns={"TIME": "Country"}
            ).replace(':', 0)


def calculateWageUnits(df):
    """This function lets you calulate other wage units in the dataset, that the user never provided."""
    wageYearly, wageMonthly, wageHourly = [], [], []

    for _, rows in df.iterrows():
        if rows['Wage Unit'] == 'Yearly':
            wageYearly.append(rows['Salary'])
            wageMonthly.append(rows['Salary']/12)
            wageHourly.append(rows['Salary']/(52.143*rows['Number of Hours']))
        elif rows['Wage Unit'] == 'Monthly':
            wageYearly.append(rows['Salary']*12)
            wageMonthly.append(rows['Salary'])
            wageHourly.append(rows['Salary']/(4.345*(rows['Number of Hours'])))
        elif rows['Wage Unit'] == 'Hourly':
            wageYearly.append(rows['Salary']*(52.143*rows['Number of Hours']))
            wageMonthly.append(rows['Salary']*(4.345*rows['Number of Hours']))
            wageHourly.append(rows['Salary'])

    df['Wage_Monthly'], df['Wage_Yearly'], df['Wage_Hourly'] = wageMonthly, wageYearly, wageHourly
    df['OG_Salary'] = df['Salary']
    df['OG_Wage_Unit'] = df['Wage Unit']
    return df


def showEuroStatData(countrues):
    """This function is used in europeDataPage.py, to show the Eurostat data in a cool way."""
    wageFactor = 'Hourly'
    data = cleanData()
    data = changeWagedFactor(data, wageFactor)
    data = data[data['Country'].isin(countrues)].reset_index(drop=True).T
    newHeader = data.iloc[0]
    data = data[1:]
    data.columns = newHeader
    dictData = data.T.to_dict()

    sessions = list(dictData.keys())

    progressBar = st.sidebar.progress(0)
    statusText = st.sidebar.empty()
    lastRows = pd.DataFrame([dictData['2014-S1']], index=['2014-S1'])

    st.title(f"{wageFactor} Wages of European countries.")
    chart = st.line_chart(lastRows, x_label='Time Period', y_label=f'Wages ({wageFactor})')

    for i in range(1, len(sessions[1:])):
        new_rows = pd.DataFrame([dictData[sessions[i]]], index=[sessions[i]])
        statusText.text(f"Pulling Data: {int(100*i/(len(sessions)-2))}%")
        chart.add_rows(new_rows)
        progressBar.progress(int(100*i/(len(sessions)-2)))
        time.sleep(0.05)

    progressBar.empty()
    st.button("Re-run")

    st.markdown("""Data from [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/earn_mw_cur__custom_12336095/default/bar?lang=en)""")
