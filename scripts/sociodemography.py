import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.express as px
import pandas as pd
import requests

API_BASE_URL = "http://backend_container:8000/api/sociodemography"

# Traduz entre o nome de apresentação do indicador e o código da API do indicador
indicator_name_to_code = {
    "IDH"                       : 'idh',
    "GINI"                      : 'gini',
    "PIB per capita"            : 'pib_per_capita',
    "Vínculo formal"            : 'porcentagem_vinculo_formal',
    "Capacidade de pagamento"   : 'capacidade_pagamento'
}

# Aplicar CSS na página
with open('style/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

# Divide para colocar na esquerda nível geral e seleção de indicadores, e na direita gráficos
col1, col2 = st.columns(spec=[1, 4], gap="medium")

# Nível geral e seleção de indicadores
with col1:

    # TODO fazer imagens para cada nivel e acessar o back para recuperar o nivel
    st.image('images/grafico_niveis/nivel3.png')

    add_vertical_space(2)

    selected_indicator_name = st.radio("Selecione o indicador", 
                                        options=[
                                            "IDH", 
                                            "GINI", 
                                            "PIB per capita", 
                                            "Vínculo formal",
                                            "Capacidade de pagamento"
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
        years = [item['year'] for item in data_response.json()]
        indicator_values = [item['value'] for item in data_response.json()]

            

        data_dict = {'Anos' : years, st.session_state['indicator'] : indicator_values}
        data_df = pd.DataFrame(data_dict)

        proportion = 8
        # Plota o gráfico
        if len(years) >= 5:
            fig = px.line(data_df, x='Anos', y=st.session_state['indicator'], height=500)
        else:
            fig = px.bar(data_df,x='Anos',y=st.session_state['indicator'],height=500)
            fig.update_xaxes(type='category')
            proportion = 3

        
        fig.update_layout(xaxis=dict(
                                title_text='Anos', 
                                title_font_size=18,  
                                tickfont_size=14,  
                            ),
                            yaxis=dict(
                                title_text=st.session_state['indicator'],
                                title_font_size=18,  
                                tickfont_size=14, 
                            ),
                            autosize=True)

        # Configuração para responsividade
        config = {"responsive": True}

        container = st.container()
        with container:
            col_left, col_center, col_right = st.columns([1, proportion, 1])
            with col_center:
                st.plotly_chart(fig, use_container_width=True, config=config)