import streamlit as st


def Navbar():
    with st.sidebar:
        st.page_link('levelsModule.py', label='Levels', icon='🔥')
        st.page_link('pages/dashboardPage.py', label='Dashboard', icon='📊')
        st.page_link('pages/levelsEntryPage.py', label='Tell your level', icon='📈')
        st.page_link('pages/europeDataPage.py', label='Europe Data', icon='💶')
        st.markdown("""---""")