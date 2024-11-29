import streamlit as st
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space

# Definir as páginas
page_sociodemagraphy = st.Page("scripts/sociodemography.py",          title="Características sociodemografia")
page_economy         = st.Page("scripts/dimensions/economic.py",      title="Economia")
page_sociocultural   = st.Page("scripts/dimensions/sociocultural.py", title="Sociocultural")
page_environment     = st.Page("scripts/dimensions/environment.py",   title="Meio ambiente")
page_institutional   = st.Page("scripts/dimensions/institutional.py", title="Capacidades institucionais")
# st.session_state['page_sociodemagraphy'] = page_sociodemagraphy
pg = st.navigation([page_sociodemagraphy, 
                    page_economy, 
                    page_sociocultural, 
                    page_environment, 
                    page_institutional], 
                    position="hidden")
st.set_page_config(page_title="Dashboard IARA", layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

# Sidebar, onde é feita a selecao do escopo para os graficos de todas as paginas
with st.sidebar:
    regions_list = pd.read_csv("data/regions.csv", header=None)
    selected_region = st.selectbox(label='Região', options=regions_list, placeholder="Escolha uma região", index=None)
    st.session_state['Região'] = selected_region

    if(selected_region=="Sudeste"):
        states_list = pd.read_csv("data/states_sudeste.csv", header=None)  
    else:  
        states_list = pd.read_csv("data/states.csv", header=None)
    selected_state = st.selectbox(label='Estado', options=states_list, placeholder="Escolha um estado", index=None)
    st.session_state['Estado'] = selected_state

    if(selected_state=="SP"):
        cities_list = pd.read_csv("data/cities_sp.csv", header=None)    
    else:
        cities_list = pd.read_csv("data/cities.csv", header=None)
    selected_city = st.selectbox(label='Município', options=cities_list, placeholder="Escolha um município", index=None)
    st.session_state['Municipio'] = selected_city

    # add_vertical_space(11)
    # st.image("images/iara_logo.png", use_container_width=True)

# Carregar a pagina selecionada, padrao é a de caracteristicas demograficas
with st.container(border=False):
    pg.run()

# Linkar as paginas no final do conteudo
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
