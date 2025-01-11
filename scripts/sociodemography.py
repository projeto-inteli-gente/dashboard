import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.express as px
import pandas as pd

with open('style/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

label_indicador = { "IDH" : 'idh',
                    "GINI" : 'gini',
                    "PIB per capita" : 'pib',
                    "Vínculo formal" : 'formal',
                    "Pagamento" : 'pay'}

# DIvide para colocar nível geral e seleção de indicadores na esquerda e gráficos na direita
col1, col2 = st.columns(spec=[1, 4], gap="medium")

# Nível geral e seleção de indicadores
with col1:

    # TODO fazer imagens para cada nivel e acessar o back para recuperar o nivel
    st.image('images/grafico_niveis/grafico_nivel05.png')

    add_vertical_space(2)

    st.session_state['Indicador demografico'] = label_indicador[st.radio("Selecione o indicador", 
                                                        options=["IDH", 
                                                                 "GINI", 
                                                                 "PIB per capita", 
                                                                 "Vínculo formal",
                                                                 "Pagamento"], 
                                                        label_visibility='hidden')]

# Gráficos
with col2:
    # Determina o escopo mais especifico selecionado, se nenhum for selecionado é o brasil inteiro
    escope = None
    if('Municipio' in st.session_state and st.session_state['Municipio'] != None):
        escope = st.session_state['Municipio']
    elif('Estado' in st.session_state and st.session_state['Estado'] != None):
        escope = st.session_state['Estado']
    elif('Região' in st.session_state and st.session_state['Região'] != None):
        escope = st.session_state['Região']
    if(escope==None):
        escope = 'br'

    # Para mostrar no eixo y do grafico
    
    
    # TODO quando tiver back end, acessar dados reais
    if('Indicador demografico' in st.session_state):
        place = escope.lower()
        stat = st.session_state['Indicador demografico']
        # dados = pd.read_csv(f'data/{place}_{stat}.csv')
        dados = pd.read_csv(f'data/br_{stat}.csv')
        dados.columns = ['Anos', st.session_state['Indicador demografico']]
        st.plotly_chart(px.line(dados, x='Anos', y=st.session_state['Indicador demografico']))