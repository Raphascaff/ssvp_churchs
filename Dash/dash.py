import streamlit as st
import plotly.express as px
from Data.data import df as initial_df
from Data.get_env_vars import GetEnvVars
from dataclasses import dataclass
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder


@dataclass
class Dash(GetEnvVars):

    def __call__(self):
        self.dash()
        
    def dash(self):
        """Main dashboard method to render Streamlit app."""
        self._setup_page()
        self._initialize_session_state()
        
        tab1, tab2 = st.tabs(["Data", "Map"])

        with tab1:
            self._render_data_tab()

        with tab2:
            self._render_map_tab()

    def _setup_page(self):
        """Configure the Streamlit page layout and title."""
        st.set_page_config(layout="wide", initial_sidebar_state="expanded")
        st.markdown("<h1 style='text-align: center; color: white;'> Igrejas do Brasil </h1>", unsafe_allow_html=True)

    def _initialize_session_state(self):
        """Initialize session state for DataFrame if not already done."""
        if 'df' not in st.session_state:
            st.session_state.df = initial_df.copy()

    def _render_data_tab(self):
        """Render the Data tab with DataFrame and controls."""
        st.write("### DataFrames")
        self._display_data_grid()

        # Input for creating a new column
        input_text = st.text_input(label="Column Name: ")
        position = st.number_input(label=f"Position: 0 to {len(st.session_state.df.columns)}:", 
                                    value=len(st.session_state.df.columns))

        c1, c2 = st.columns([2, 26])
        self._render_buttons(c1, c2, input_text, position)

    def _display_data_grid(self):
        """Display the DataFrame in an editable grid."""
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
        gb.configure_pagination()
        gridOptions = gb.build()
        AgGrid(st.session_state.df, gridOptions=gridOptions, editable=True, update_mode='MODEL_CHANGED')

    def _render_buttons(self, c1, c2, input_text, position):
        """Render buttons for saving JSON and creating a new column."""
        with c1:
            self._render_save_button()

        with c2:
            self._render_create_column_button(input_text, position)

    def _render_save_button(self):
        """Render the button to save the DataFrame as JSON."""
        save_button = st.button(label="Save JSON", type="primary")
        if save_button:
            self._save_data_as_json()
            st.success("Data was successfully saved!")

    def _save_data_as_json(self):
        """Save the DataFrame to a JSON file."""
        result = st.session_state.df.to_json(force_ascii=False, indent=4)
        with open('Scrappers/results.json', 'w', encoding='utf-8') as json_file:
            json_file.write(result)

    def _render_create_column_button(self, input_text, position):
        """Render the button to create a new column in the DataFrame."""
        create_column_button = st.button(
            label="Create Column", 
            type="primary", 
            disabled=not (input_text and position is not None and 0 <= position <= len(st.session_state.df.columns))
        )

        if create_column_button:
            self._add_new_column(input_text, position)

    def _add_new_column(self, column_name, position):
        """Add a new column to the DataFrame."""
        st.session_state.df.insert(int(position), column_name, value="")
        st.success(f"Column '{column_name}' added at position {position}!")

    def _render_map_tab(self):
        """Render the Map tab with a scatter mapbox plot."""
        fig = px.scatter_mapbox(
            st.session_state.df, 
            lat='LATITUDE', 
            lon='LONGITUDE', 
            hover_name='TITLE',
            zoom=12, 
            width=5000, 
            height=1000,
            hover_data={'LATITUDE': False, 'LONGITUDE': False}
        )

        px.set_mapbox_access_token(self.map_box_key)
        fig.update_layout(mapbox_style="basic")
        st.plotly_chart(fig)