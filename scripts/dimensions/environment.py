import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from style import colors

with open('style/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 



label_indicador = { "Água e esgoto" : 'agua',
                    "Resíduos sólidos" : 'residuos',
                    "Área verde" : 'verde',
                    "Qualidade do ar" : 'ar',
                    "Energia" : 'energia'}

# Divide para colocar nível geral e seleção de indicadores na esquerda e gráficos na direita
col1, col2 = st.columns(spec=[1, 3], gap="medium")

# Nível geral e seleção de indicadores
with col1:

    # TODO fazer imagens para cada nivel e acessar o back para recuperar o nivel
    st.image('images/grafico_niveis/nivel5.png')

    add_vertical_space(2)   

    st.session_state['Indicador demografico'] = label_indicador[
        st.radio("Selecione o indicador", 
            options=["Água e esgoto",
                    "Resíduos sólidos",
                    "Área verde",
                    "Qualidade do ar",
                    "Energia"], 
            label_visibility='hidden'
        )
    ]

# Gráficos
with col2:
    with st.container():
        # Data
        moc_data = {
            'Índice de volume de esgoto coletado': 4,
            'Consumo médio per capita de água': 3,
            'Soluções inteligentes para gestão na distribuição e consumo de água': 7,
            'Índice de perdas na distribuição de água': 2,
            'Índice de volume de esgoto tratado': 5,
        }

        # State to keep track of selected bar
        if "selected_bar" not in st.session_state:
            st.session_state.selected_bar = None

        def render_chart(selected_bar):
            x_values = list(moc_data.keys())
            y_values = list(moc_data.values())

            bar_colors = [colors.levels[y] for y in y_values]

            fig = go.Figure(
                data=[
                    go.Bar(
                        x=x_values,
                        y=y_values,
                        marker=dict(color=bar_colors),
                        text=["↓" if x == selected_bar else "" for x in x_values],
                        textposition="outside",
                    )
                ]
            )

            fig.update_layout(
                height=300,
                xaxis=dict(title="", showticklabels=False),
                yaxis=dict(title="Values"),
                yaxis_range=[0,10],
                font=dict(
                    size=38
                ),
                autosize=True
            )

            return fig

        selected_bar = st.selectbox(
            "Selecione o indicador",
            list(moc_data.keys())
        )
        st.session_state.selected_bar = selected_bar

        # Configuração para responsividade
        config = {"responsive": True}

        # TODO quando tiver back end, acessar dados reais
        if('Indicador demografico' in st.session_state):
                dados = pd.read_csv(f'data/br_idh.csv')
                dados.columns = ['Anos', st.session_state['Indicador demografico']]
                fig = px.line(dados, x='Anos', y=st.session_state['Indicador demografico'])
                fig.update_layout(height=300, autosize=True)
                st.plotly_chart(fig, use_container_width=True, config=config)

        

    with st.container():

        subcol1, subcol2 = st.columns(spec=[1, 1], gap="small")

        with subcol1:
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
            
            
            # Display the chart
            fig = render_chart(st.session_state.selected_bar)
            clicked_bar = st.plotly_chart(fig, use_container_width=True, config=config)

        with subcol2:

            x_values = [1, 2, 3,4 ,5, 6,7]
            y_values = [3, 3, 5, 7, 2, 6, 8]

            bar_colors = [colors.levels[x] for x in x_values]

            fig = go.Figure(
                data=[
                    go.Bar(
                        x=x_values,
                        y=y_values,
                        marker=dict(color=bar_colors),
                        text=["↓" if x == moc_data[st.session_state.selected_bar] else "" for x in x_values],
                        textposition="outside",
                    )
                ]
            )

            fig.update_layout(
                height=300,
                xaxis=dict(title="", showticklabels=False),
                yaxis=dict(title="Values"),
                yaxis_range=[0,max(y_values)*1.5],
                font=dict(
                    size=38
                ),
                autosize=True
            )

            st.plotly_chart(fig, use_container_width=True, config=config)