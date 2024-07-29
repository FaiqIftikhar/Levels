import streamlit as st
from utils import *


st.title(f"{wage_factor} wages per country.")
select_countries = st.multiselect('Select Country', options=data['Country'])
if st.checkbox('Select all contries'):
    select_countries = data['Country']
# if st.checkbox('Show raw data'):

    # st.write(data)
st.line_chart(data[data['Country'].isin(select_countries)].set_index('Country').T, x_label='Years', y_label='Wages' )