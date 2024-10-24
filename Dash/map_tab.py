import streamlit as st
import plotly.express as px
from dataclasses import dataclass

@dataclass
class MapTab:
    """Handles the 'Map' tab functionalities."""
    map_box_key:str = st.session_state.get('map_box_key', None)

    def render(self):
        
        if not self.map_box_key:
            st.error("Mapbox access token is missing!")
            return

        px.set_mapbox_access_token(self.map_box_key)
        fig = px.scatter_mapbox(
            data_frame=st.session_state.df, 
            lat='LATITUDE', 
            lon='LONGITUDE', 
            hover_name='TITLE',
            zoom=12,
            size_max=15,
            size=[10]*len(st.session_state.df),
            width=5000, 
            height=1000,
            hover_data={'LATITUDE': False, 'LONGITUDE': False}
        )
        fig.update_layout(mapbox_style="basic")        
        st.plotly_chart(fig)