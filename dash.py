import streamlit as st
from data import df
import plotly.express as px

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

with st.container(border=True):
    st.markdown("<h1 style='text-align: center; color: white;'>Igrejas do Brasil</h1>", unsafe_allow_html=True)

    fig = px.scatter_mapbox(df, 
                            lat='LATITUDE', 
                            lon='LONGITUDE', 
                            hover_name='TITLE', 
                            zoom=10, 
                            width=10000, 
                            height=1000
    )

    px.set_mapbox_access_token('pk.eyJ1IjoicmFwaGFlbHNjYWZmIiwiYSI6ImNtMjI3YW1leTAzeXAybXBwa3EyNndoZjkifQ.kX4V45OzubMncdDvEnM-3w')

    fig.update_layout(mapbox_style="basic")

    st.plotly_chart(fig)
