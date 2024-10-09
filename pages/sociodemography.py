import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

idh = False
gini = False
pib = False
formal_jobs = False
payment_capability = False

# DIvide para colocar nível geral e seleção de indicadores na esquerda e gráficos na direita
col1, col2 = st.columns(spec=[1, 4], gap="medium")

# Nível geral e seleção de indicadores
with col1:

    st.image('images/circle.png')

    add_vertical_space(2)

    if st.button("IDH", use_container_width=True):
        idh = True
    else:
        idh = False

    if st.button("GINI", use_container_width=True):
        gini = True
    else:
        gini = False

    if st.button("PIB per capita", use_container_width=True):
        pib = True
    else:
        pib = False

    if st.button("Vínculo formal", use_container_width=True):
        formal_jobs = True
    else:
        formal_jobs = False

    if st.button("Pagamento", use_container_width=True):
        payment_capability = True
    else:
        payment_capability = False


# Gráficos
with col2:
    escope = None
    if(st.session_state['Municipio']):
        escope = st.session_state['Municipio']
    elif(st.session_state['Estado']):
        escope = st.session_state['Estado']
    elif(st.session_state['Região']):
        escope = st.session_state['Região']

    if(escope):
        if(idh):
            # TODO quando tiver back end, acessar dados com escopo e o indicador
            dados = pd.read_csv(f'data/{escope.lower()}_idh.csv')
            dados.columns = ['Anos', 'IDH']
            st.plotly_chart(px.line(dados, x='Anos', y='IDH'))
        if(gini):
            dados = pd.read_csv(f'data/{escope.lower()}_gini.csv')
            dados.columns = ['Anos', 'GINI']
            st.plotly_chart(px.line(dados, x='Anos', y='GINI'))
        if(pib):
            dados = pd.read_csv(f'data/{escope.lower()}_pib.csv')
            dados.columns = ['Anos', 'PIB per capita']
            st.plotly_chart(px.line(dados, x='Anos', y='PIB per capita'))
        if(formal_jobs):
            dados = pd.read_csv(f'data/{escope.lower()}_formal.csv')
            dados.columns = ['Anos', 'Porcentagem da população com vínculo formal']
            st.plotly_chart(px.line(dados, x='Anos', y='Porcentagem da população com vínculo formal'))
        if(payment_capability):
            dados = pd.read_csv(f'data/{escope.lower()}_pay.csv')
            dados.columns = ['Anos', 'Capacidade de pagamento']
            st.plotly_chart(px.line(dados, x='Anos', y='Capacidade de pagamento'))