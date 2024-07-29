import streamlit as st
import utils
import time
import pandas as pd

st.set_page_config(page_title="Europe Data", page_icon="🇪🇺")

st.title("💶 European National Data")

st.markdown("""
            This page shows stats of national wages of different countries within europe.
            """)

Countries = utils.COUNTRIES
wage_factor = 'Hourly'
data = utils.clean_data()
data = utils.change_waged_factor(data, wage_factor)
data = data[data['Country'].isin(Countries)].reset_index(drop=True).T
new_header = data.iloc[0]
data = data[1:]
data.columns = new_header
_dict_data = data.T.to_dict()

sessions = list(_dict_data.keys())

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = pd.DataFrame([_dict_data['2014-S1']], index=['2014-S1'])

st.title(f"{wage_factor} Wages of European countries.")
chart = st.line_chart(last_rows, x_label='Time Period', y_label=f'Wages ({wage_factor})')
print(last_rows)
for i in range(1, len(sessions[1:])):
    new_rows = pd.DataFrame([_dict_data[sessions[i]]], index=[sessions[i]])
    print(new_rows)
    status_text.text("Pulling Data: %i%%" % int(100*i/(len(sessions)-2)))
    chart.add_rows(new_rows)
    progress_bar.progress(int(100*i/(len(sessions)-2)))
    # last_rows = new_rows
    # print(last_rows)
    time.sleep(0.05)

progress_bar.empty()
st.button("Re-run")

st.markdown("""Data from [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/earn_mw_cur__custom_12336095/default/bar?lang=en)""")

# data = clean_data()


# wage_factor = st.selectbox('Select wage unit', options=['Hourly', 'Monthly'], index=1)

# data = change_waged_factor(data, wage_factor)
# select_countries = st.multiselect('Select Country', options=data['Country'])
# st.subheader('Raw data')
# st.write(data[data['Country'].isin(select_countries)])