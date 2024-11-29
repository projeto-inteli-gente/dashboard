import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

label_indicador = { "Água e esgoto" : 'agua',
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
                                                        options=["Água e esgoto",
                                                                "Resíduos sólidos",
                                                                "Área verde",
                                                                "Qualidade do ar",
                                                                "Energia"], 
                                                        label_visibility='hidden')]

# Gráficos
with col2:
    with st.container():
        # Data
        moc_data = {
            'Índice de volume de esgoto coletado': 1,
            'Consumo médio per capita de água': 6,
            'Soluções inteligentes para gestão na distribuição e consumo de água': 4,
            'Índice de perdas na distribuição de água': 2,
            'Índice de volume de esgoto tratado': 3,
        }

        # State to keep track of selected bar
        if "selected_bar" not in st.session_state:
            st.session_state.selected_bar = None

        # Function to render the figure
        def render_chart(selected_bar):
            x_values = list(moc_data.keys())
            y_values = list(moc_data.values())

            # Highlight colors
            bar_colors = ["#84ccfc" if x != selected_bar else "white" for x in x_values]

            # Create figure
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=x_values,
                        y=y_values,
                        marker=dict(color=bar_colors),
                        text=[x if x == selected_bar else "" for x in x_values],
                        textposition="outside",
                    )
                ]
            )

            # Update layout
            fig.update_layout(
                width=700,
                height=300,
                xaxis=dict(title="", showticklabels=False),
                yaxis=dict(title="Values"),
                yaxis_range=[0,7]
            )

            return fig
        
        # Simulate click (temporary solution with Streamlit selectbox)
        selected_bar = st.radio(
            "Selecione o indicador",
            list(moc_data.keys()),
            index=0,
            horizontal=False,  # Native Streamlit option to display horizontally
            label_visibility='hidden'
        )
        st.session_state.selected_bar = selected_bar

        # Display the chart
        fig = render_chart(st.session_state.selected_bar)
        clicked_bar = st.plotly_chart(fig, use_container_width=True)

        

        # Re-render the chart with the selected bar
        # st.plotly_chart(render_chart(selected_bar), use_container_width=True)


        # moc_data = {
        #     'Índice de volume de esgoto coletado' : 6,
        #     'Consumo médio per capita de água' : 4,
        #     'Soluções inteligentes para gestão na distribuição e consumo de água' : 5,
        #     'Índice de perdas na distribuição de água' : 2,
        #     'Índice de volume de esgoto tratad' : 3,
        # }
        
        # fig = go.Figure(data=[
        #     go.Bar(
        #         x=list(moc_data.keys()),  # Categories (x-axis)
        #         y=list(moc_data.values()),  # Values (y-axis)
                
        #     ),
            
        # ])
        # fig.update_layout(
        #     width=700,   # Set the width (in pixels)
        #     height=300   # Set the height (in pixels)
        # )
        
        # st.plotly_chart(fig, use_container_width=True)

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
            
            
            # TODO quando tiver back end, acessar dados reais
            if('Indicador demografico' in st.session_state):
                dados = pd.read_csv(f'data/br_idh.csv')
                dados.columns = ['Anos', st.session_state['Indicador demografico']]
                fig = px.line(dados, x='Anos', y=st.session_state['Indicador demografico'])
                fig.update_layout(height=300)
                st.plotly_chart(fig)

        with subcol2:

            np.random.seed(42)
            data = {
                "Values": np.random.normal(loc=50, scale=10, size=1000)
            }
            df = pd.DataFrame(data)
            fig = px.histogram(df, x="Values", nbins=30)
            fig.update_layout(height=300)
            st.plotly_chart(fig)