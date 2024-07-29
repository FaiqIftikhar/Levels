import streamlit as st


st.subheader('Raw data')
st.write(data[data['Country'].isin(select_countries)])