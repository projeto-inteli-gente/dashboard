import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.express as px
import pandas as pd
import requests

API_BASE_URL = "http://127.0.0.1:8000/api/sociodemography"

# Traduz entre o nome de apresentação do indicador e o código da API do indicador
indicator_name_to_code = {
    "IDH"                       : 'idh',
    "GINI"                      : 'gini',
    "PIB per capita"            : 'pib_per_capita',
    "Vínculo formal"            : 'porcentagem_vinculo_formal',
    "Capacidade de pagamento"   : 'capag'
}

# Aplicar CSS na página
with open('style/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

# Divide para colocar na esquerda nível geral e seleção de indicadores, e na direita gráficos
col1, col2 = st.columns(spec=[1, 4], gap="medium")

# Nível geral e seleção de indicadores
with col1:

    # TODO fazer imagens para cada nivel e acessar o back para recuperar o nivel
    st.image('images/grafico_niveis/nivel6.png')

    add_vertical_space(2)

    selected_indicator_name = st.radio("Selecione o indicador", 
                                        options=[
                                            "IDH", 
                                            "GINI", 
                                            "PIB per capita", 
                                            "Vínculo formal",
                                            "Pagamento"
                                        ], 
                                        label_visibility='hidden'
                                )

    st.session_state['indicator'] = selected_indicator_name

# Gráficos
with col2:
    
    if 'indicator' in st.session_state:

        # Traduz o nome do indicador para o código na API
        indicator_code_name = indicator_name_to_code[st.session_state['indicator']]

        # Acessa a API
        data_response = requests.get(f"{API_BASE_URL}/{indicator_code_name}/{st.session_state['smallest_scope_route']}")

        # Transforma os dados em DataFrame
        print(data_response)
        years = [item['year'] for item in data_response.json()]
        indicator_values = [item[indicator_code_name] for item in data_response.json()]
        data_dict = {'Anos' : years, st.session_state['indicator'] : indicator_values}
        data_df = pd.DataFrame(data_dict)

        # Plota o gráfico
        st.plotly_chart(px.line(data_df, x='Anos', y=st.session_state['indicator']))