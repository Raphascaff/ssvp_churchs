import streamlit as st
import plotly.express as px
from Data.data import df
from Data.get_env_vars import GetEnvVars
from dataclasses import dataclass


@dataclass
class Dash(GetEnvVars):

    def __call__(self):
        self.dash()
        
    def dash(self):
        st.set_page_config(layout="wide", initial_sidebar_state="expanded")

        st.markdown("<h1 style='text-align: center; color: white;'> Igrejas do Brasil </h1>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Data", "Map"])

        with tab1:
            st.write("### DataFrame")
            st.data_editor(df)

        with tab2:
            fig = px.scatter_mapbox(df, 
                                    lat='LATITUDE', 
                                    lon='LONGITUDE', 
                                    hover_name='TITLE',
                                    zoom=12, 
                                    width=5000, 
                                    height=1000,
                                    hover_data={
                                        'LATITUDE': False,
                                        'LONGITUDE': False
                                    }
                                )

            px.set_mapbox_access_token(self.map_box_key)

            fig.update_layout(mapbox_style="basic")

            st.plotly_chart(fig)
