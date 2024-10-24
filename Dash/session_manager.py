import streamlit as st
from Data.data import df as initial_df
from dataclasses import dataclass
from Data.get_env_vars import GetEnvVars


@dataclass
class SessionManager(GetEnvVars):
    """Manages session state initialization."""
    
    def initialize_session_state(self):
        
        defaults = {
                        'df': initial_df.copy(),
                        'map_box_key': self.map_box_key
                    }
        for key, default in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default