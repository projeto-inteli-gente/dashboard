import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

moc_data = {
    'Índice de volume de esgoto coletado' : 6,
    'Consumo médio per capita de água' : 4,
    'Soluções inteligentes para gestão na distribuição e consumo de água' : 5,
    'Índice de perdas na distribuição de água' : 2,
    'Índice de volume de esgoto tratad' : 3,
}

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

label_indicador = { "Água e escoto" : 'agua',
                    "Resíduos sólidos" : 'residuos',
                    "Área verde" : 'verde',
                    "Qualidade do ar" : 'ar',
                    "Energia" : 'energia'}

# DIvide para colocar nível geral e seleção de indicadores na esquerda e gráficos na direita
col1, col2 = st.columns(spec=[1, 4], gap="medium")

# Nível geral e seleção de indicadores
with col1:

    # TODO fazer imagens para cada nivel e acessar o back para recuperar o nivel
    st.image('images/grafico_niveis/grafico_nivel05.png')

    add_vertical_space(2)

    st.session_state['Indicador demografico'] = label_indicador[st.radio("Selecione o indicador", 
                                                        options=["Água e escoto",
                                                                "Resíduos sólidos",
                                                                "Área verde",
                                                                "Qualidade do ar",
                                                                "Energia"], 
                                                        label_visibility='hidden')]

# Gráficos
with col2:
    with st.container():
        fig = go.Figure(data=[
            go.Bar(
                x=list(moc_data.keys()),  # Categories (x-axis)
                y=list(moc_data.values()),  # Values (y-axis)
            )
        ])
        st.plotly_chart(fig)
        clicked_data = st.session_state.get("plotly_click_event")
        
        if clicked_data:
            st.text(clicked_data)

    # with st.container():

    #     subcol1, subcol2 = st.columns(spec=[1, 1], gap="medium")

    #     with subcol1:
    #         # Determina o escopo mais especifico selecionado, se nenhum for selecionado é o brasil inteiro
    #         escope = None
    #         if('Municipio' in st.session_state and st.session_state['Municipio'] != None):
    #             escope = st.session_state['Municipio']
    #         elif('Estado' in st.session_state and st.session_state['Estado'] != None):
    #             escope = st.session_state['Estado']
    #         elif('Região' in st.session_state and st.session_state['Região'] != None):
    #             escope = st.session_state['Região']
    #         if(escope==None):
    #             escope = 'br'

    #         # Para mostrar no eixo y do grafico
            
            
    #         # TODO quando tiver back end, acessar dados reais
    #         if('Indicador demografico' in st.session_state):
    #             dados = pd.read_csv(f'data/br_idh.csv')
    #             dados.columns = ['Anos', st.session_state['Indicador demografico']]
    #             st.plotly_chart(px.line(dados, x='Anos', y=st.session_state['Indicador demografico']))