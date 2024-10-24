import streamlit as st
from dataclasses import dataclass
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

@dataclass
class DataTab:
    """Handles the 'Data' tab functionalities."""
    
    def render(self):
        st.write("### DataFrames")
        self.display_data_grid()
        input_text = st.text_input(label="Column Name: ")
        position = st.number_input(label=f"Position: 0 to {len(st.session_state.df.columns)}:", 
                                   value=len(st.session_state.df.columns))
        c1, c2 = st.columns([2, 26])
        self.render_buttons(c1, c2, input_text, position)

    def display_data_grid(self):
        """Displays editable AgGrid with the current DataFrame and updates session state upon changes."""
        gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
        gb.configure_pagination()
        gb.configure_default_column(editable=True)
        gridOptions = gb.build()

        grid_response = AgGrid(
            st.session_state.df,
            gridOptions=gridOptions,
            editable=True,
            update_mode=GridUpdateMode.MODEL_CHANGED, 
            fit_columns_on_grid_load=True,
            return_data=True,
        )

        st.session_state['df'] = grid_response['data']

    def render_buttons(self, c1, c2, input_text, position):
        with c1:
            self.render_save_button()

        with c2:
            self.render_create_column_button(input_text, position)

    def render_save_button(self):
        save_button = st.button(label="Save JSON", type="primary")
        if save_button:
            result = st.session_state.df.to_json(force_ascii=False, indent=4)
            with open('Scrappers/results.json', 'w', encoding='utf-8') as json_file:
                json_file.write(result)
            st.success("Data was successfully saved!")

    def render_create_column_button(self, input_text, position):
        create_column_button = st.button(
            label="Create Column", 
            type="primary", 
            disabled=not (input_text and position is not None and 0 <= position <= len(st.session_state.df.columns))
        )
        if create_column_button:
            st.session_state['df'].insert(int(position), input_text, value="")
            st.success(f"Column '{input_text}' added at position {position}!")