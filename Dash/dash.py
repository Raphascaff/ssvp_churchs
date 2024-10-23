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
        st.set_page_config(layout="wide", initial_sidebar_state="expanded")

        st.markdown("<h1 style='text-align: center; color: white;'> Igrejas do Brasil </h1>", unsafe_allow_html=True)

        # Use session state to hold the DataFrame
        if 'df' not in st.session_state:
            st.session_state.df = initial_df.copy()

        tab1, tab2 = st.tabs(["Data", "Map"])

        with tab1:
            st.write("### DataFrames")

            # Configure AgGrid with the DataFrame from session state
            gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
            gb.configure_pagination()
            gridOptions = gb.build()

            # Make AgGrid editable
            AgGrid(st.session_state.df, gridOptions=gridOptions, editable=True, update_mode='MODEL_CHANGED')

            # Inputs for creating a new column
            input_text = st.text_input(label="Column Name: ")
            position = st.number_input(label=f"Position: 0 to {len(st.session_state.df.columns)}:", value=len(st.session_state.df.columns))

            c1, c2 = st.columns([2, 26])
            with c1:
                save_button = st.button(label="Save JSON", type="primary")
                if save_button:
                    result = st.session_state.df.to_json(force_ascii=False, indent=4)
                    with open('Scrappers/results.json', 'w', encoding='utf-8') as json_file:
                        json_file.write(result)
                        st.success("Data was successfully saved!")
            with c2:
                # Enable the button based on the validity of the input
                create_column_button = st.button(label="Create Column", type="primary", 
                                                  disabled=not (input_text and position is not None and 0 <= position <= len(st.session_state.df.columns)))

                if create_column_button:
                    st.session_state.df.insert(int(position), input_text, value="")
                    st.success(f"Column '{input_text}' added at position {position}!")

        with tab2:
            fig = px.scatter_mapbox(st.session_state.df, 
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