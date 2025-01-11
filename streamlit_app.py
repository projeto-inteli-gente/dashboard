import streamlit as st
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space
import requests

API_BASE_URL = "http://127.0.0.1:8000/api"


# Definir as páginas
page_sociodemagraphy = st.Page("scripts/sociodemography.py",          title="Características sociodemografia")
page_economy         = st.Page("scripts/dimensions/economic.py",      title="Economia")
page_sociocultural   = st.Page("scripts/dimensions/sociocultural.py", title="Sociocultural")
page_environment     = st.Page("scripts/dimensions/environment.py",   title="Meio ambiente")
page_institutional   = st.Page("scripts/dimensions/institutional.py", title="Capacidades institucionais")
pg = st.navigation([page_sociodemagraphy, 
                    page_economy, 
                    page_sociocultural, 
                    page_environment, 
                    page_institutional], 
                    position="hidden")
st.set_page_config(page_title="Dashboard IARA", layout="wide")

# Aplicar CSS
with open('style/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

# Sidebar, onde é feita a selecao do escopo para os graficos de todas as paginas
with st.sidebar:

    regions_response = requests.get(f"{API_BASE_URL}/places/regions")

    if regions_response.status_code == 200:
        regions = [region["name"] for region in regions_response.json()]
        selected_region = st.selectbox(label='Região', options=regions, placeholder="Escolha uma região", index=None)
        st.session_state['Região'] = selected_region
    else:
        st.error("Falha em carregar regiões.")



    if selected_region != None:
        route_states = f"states?region={selected_region}"
    else:
        route_states = "states"
    states_response = requests.get(f"{API_BASE_URL}/places/{route_states}")

    if states_response.status_code == 200:
        states = [state["name"] for state in states_response.json()]
        selected_state = st.selectbox(label='Estado', options=states, placeholder="Escolha um estado", index=None)
        st.session_state['Estado'] = selected_state
    else:
        st.error("Falha em carregar estados.")



    if selected_state != None:
        route_cities = f"cities?state={selected_state}"
    elif selected_region != None:
        route_cities = f"cities?region={selected_region}"
    else:
        route_cities = "cities"
    cities_response = requests.get(f"{API_BASE_URL}/places/{route_cities}")

    if cities_response.status_code == 200:
        cities = [city["name"] for city in cities_response.json()]
        selected_city = st.selectbox(label='Município', options=cities, placeholder="Escolha um município", index=None)
        st.session_state['Municipio'] = selected_city
    else:
        st.error("Falha em carregar municípios.")

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
