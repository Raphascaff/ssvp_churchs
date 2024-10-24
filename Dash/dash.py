import streamlit as st
from dataclasses import dataclass
from Dash.session_manager import SessionManager
from Dash.data_tab import DataTab
from Dash.map_tab import MapTab

@dataclass
class Dashboard:
    """Main dashboard class that sets up and renders the tabs."""

    def __call__(self):
        
        self.render()

    def render(self):
        """Main dashboard method to render Streamlit app."""
        self._setup_page()

        # Ensure session state is initialized
        session_manager = SessionManager()
        session_manager.initialize_session_state()

        # Create the tabs
        tab1, tab2 = st.tabs(["Data", "Map"])

        with tab1:
            data_tab = DataTab()
            data_tab.render()

        with tab2:
            map_tab = MapTab()
            map_tab.render()

    def _setup_page(self):
        """Configure the Streamlit page layout and title."""
        st.set_page_config(layout="wide", initial_sidebar_state="expanded")
        st.markdown("<h1 style='text-align: center; color: white;'> Igrejas do Brasil </h1>", unsafe_allow_html=True)