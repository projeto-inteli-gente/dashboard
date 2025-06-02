import streamlit as st
import pandas as pd
import requests

API_BASE_URL = "http://backend_container:8000/api/names"


# Definir as páginas
page_sociodemagraphy = st.Page("scripts/sociodemography.py",          title="Caracterização sociodemográfica")
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

# ── Barra de progresso vertical de rolagem ──────────────────────────────────────
st.components.v1.html(
    """
    <style>
      /* contêiner da barra (uma faixa transparente ocupando 100 % da altura) */
      #progressBarContainer {
          position: fixed;
          top: 0;
          right: 0;              /* gruda na lateral direita */
          width: 4px;            /* espessura da barra */
          height: 100%;
          background: rgba(0,0,0,0.08);   /* trilho leve */
          z-index: 9999;         /* fica acima de tudo */
      }
      /* a barra em si (altura varia com o scroll) */
      #progressBar {
          width: 100%;
          height: 0%;            /* será atualizado via JS */
          background: #ff4b4b;   /* cor da barra – mude à vontade */
          transition: height 0.1s linear;  /* suaviza a animação */
      }
    </style>

    <div id="progressBarContainer"><div id="progressBar"></div></div>

    <script>
      // Atualiza a altura da barra sempre que o usuário rolar a página
      window.addEventListener('scroll', () => {
        const doc      = document.documentElement;
        const total    = doc.scrollHeight - doc.clientHeight;   // pixels totais de rolagem
        const scrolled = (window.scrollY / total) * 100;        // % rolada
        document.getElementById('progressBar').style.height = scrolled + '%';
      });
    </script>
    """,
    height=0,  # não ocupa espaço no layout Streamlit
)

# Aplicar CSS
with open('style/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

st.session_state['region_id'] = None
st.session_state['state_id'] = None
st.session_state['city_id'] = None
st.session_state['smallest_scope_route'] = None

# Sidebar, onde é feita a selecao do escopo para os graficos de todas as paginas
with st.sidebar:

    # Carregar lista de regiões e selecionar região

    regions_response = requests.get(f"{API_BASE_URL}/regions")

    if regions_response.status_code == 200:

        regions_names = [region['name'] for region in regions_response.json()]

        selected_region_name = st.selectbox(
            label='Região', 
            placeholder="Escolha uma região", 
            options=regions_names, 
            index=None
        )
        if selected_region_name:
            st.session_state['nome_regiao'] = selected_region_name
        else:
            st.session_state['nome_regiao'] = None

    else:
        st.error("Falha em carregar regiões.")



    # Carregar lista de estados e selecionar estado

    if st.session_state['nome_regiao'] != None:
        query_string_states = f"?nome_regiao={st.session_state['nome_regiao']}"
    else:
        query_string_states = ""
    states_response = requests.get(f"{API_BASE_URL}/states{query_string_states}")

    if states_response.status_code == 200:

        states_names = [state["nome_uf"] for state in states_response.json()]
        states_ufs = [state["sigla_uf"] for state in states_response.json()]
        states = dict(zip(states_names, states_ufs))

        selected_state_name = st.selectbox(
            label='Estado', 
            placeholder="Escolha um estado", 
            options=states_names, 
            index=None
        )
        if selected_state_name:
            st.session_state['sigla_uf'] = states[selected_state_name]
        else:
            st.session_state['sigla_uf'] = None

    else:
        st.error("Falha em carregar estados.")



    # Carregar lista de cidades e selecionar cidade

    if st.session_state['sigla_uf'] != None:
        query_string_cities = f"?sigla_uf={st.session_state['sigla_uf']}"
    elif st.session_state['nome_regiao'] != None:
        query_string_cities = f"?nome_regiao={st.session_state['nome_regiao']}"
    else:
        query_string_cities = ""
    cities_response = requests.get(f"{API_BASE_URL}/cities{query_string_cities}")

    if cities_response.status_code == 200:

        cities_names = [city["nome_municipio"] for city in cities_response.json()]
        cities_ids = [city["municipio_id"] for city in cities_response.json()]
        cities = dict(zip(cities_names, cities_ids))

        selected_city_name = st.selectbox(
            label='Município', 
            placeholder="Escolha um município", 
            options=cities_names, 
            index=None
        )
        if selected_city_name:
            st.session_state['municipio_id'] = cities[selected_city_name]
        else:
            st.session_state['municipio_id'] = None

    else:
        st.error("Falha em carregar municípios.")



    # Determina o escopo mais especifico selecionado
    st.session_state['smallest_scope_route'] = ""
    if st.session_state['municipio_id'] != None:
        st.session_state['smallest_scope_route'] = f"city/{st.session_state['municipio_id']}"
    elif st.session_state['sigla_uf'] != None:
        st.session_state['smallest_scope_route'] = f"state/{st.session_state['sigla_uf']}"
    elif st.session_state['nome_regiao'] != None:
        st.session_state['smallest_scope_route'] = f"region/{st.session_state['nome_regiao']}"



# Carregar a pagina selecionada, padrao é a de caracteristicas demograficas
with st.container(border=False):
    pg.run()

# Linkar as paginas no final do conteudo
with st.container():
    col1, col2, col3, col4, col5 = st.columns(spec=[19, 10, 11, 11, 14], gap="medium")
    with col1:
        st.page_link(page_sociodemagraphy)
        pass
    with col2:
        st.page_link(page_economy)
    with col3:
        st.page_link(page_sociocultural)
    with col4:
        st.page_link(page_environment)
    with col5:
        st.page_link(page_institutional)
