"""
A simple module/method to create the navbor links and connect them to the relevant Python file.
"""
import streamlit as st


def navBar():
    """This function creates the navbar links."""
    with st.sidebar:
        st.image("./resources/hero.png", width=250)
        st.markdown("""---""")
        st.page_link('levelsModule.py', label='Levels', icon='💸')
        st.page_link('pages/dashboardPage.py', label='Dashboard', icon='📊')
        st.page_link('pages/levelsEntryPage.py', label='Tell your level', icon='📈')
        st.page_link('pages/europeDataPage.py', label='Europe Data', icon='💶')
        st.page_link('pages/references.py', label='Data References', icon='📖')
        st.markdown("""---""")
