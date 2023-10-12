import streamlit as st
from tab_df.logics import Dataset

def display_tab_df_content(file_path):
    # Instantiate Dataset class and save it in Streamlit session state
    dataset = Dataset(file_path)
    if "dataset" not in st.session_state:
        st.session_state.dataset = dataset

    # Compute all the information to be displayed
    st.session_state.dataset.set_data()

    # First Streamlit Expander container
    with st.expander("Dataset Summary"):
        # Display the summary as a Streamlit table
        st.table(st.session_state.dataset.get_summary())
        
        # Display the table attribute using Streamlit.write()
        st.write(st.session_state.dataset.table)

    # Second Streamlit Expander container
    with st.expander("View Data"):
        # Slider to select the number of rows
        n_rows = st.slider("Select number of rows to display:", 1, 100, 5)
        
        # Radio button to select the method
        method = st.radio("Select method to view data:", ["head", "tail", "sample"])

        # Display the subset of the dataframe based on the selected method
        if method == "head":
            st.dataframe(st.session_state.dataset.df.head(n_rows))
        elif method == "tail":
            st.dataframe(st.session_state.dataset.df.tail(n_rows))
        elif method == "sample":
            st.dataframe(st.session_state.dataset.df.sample(n_rows))
