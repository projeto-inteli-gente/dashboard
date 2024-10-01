import streamlit as st
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space

# Define pages
page_sociodemagraphy = st.Page("pages/sociodemography.py",          title="Características sociodemografia")
page_economy         = st.Page("pages/dimensions/economic.py",      title="Economia")
page_sociocultural   = st.Page("pages/dimensions/sociocultural.py", title="Sociocultural")
page_environment     = st.Page("pages/dimensions/environment.py",   title="Meio ambiente")
page_institutional   = st.Page("pages/dimensions/institutional.py", title="Capacidades institucionais")

pg = st.navigation([page_sociodemagraphy, 
                    page_economy, 
                    page_sociocultural, 
                    page_environment, 
                    page_institutional], 
                    position="hidden")
st.set_page_config(page_title="Dashboard IARA", layout="wide")

# Sidebar
with st.sidebar:
    options_list = ["opções"]

    region = st.selectbox('Região', options_list)
    state = st.selectbox('Estado', options_list)
    mesoregion = st.selectbox('Mesoregião', options_list)
    city = st.selectbox('Município', options_list)

    add_vertical_space(5)
    st.image("images/iara_logo.png", use_column_width=True)

with st.container(height=450):
    pg.run()

# Link pages at the bottom of the screen
with st.container():
    col1, col2, col3, col4, col5 = st.columns(spec=[19, 10, 11, 11, 14], gap="medium")
    with col1:
        st.page_link(page_sociodemagraphy)
    with col2:
        st.page_link(page_economy)
    with col3:
        st.page_link(page_sociocultural)
    with col4:
        st.page_link(page_environment)
    with col5:
        st.page_link(page_institutional)
