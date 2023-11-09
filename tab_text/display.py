import streamlit as st

from tab_text.logics import TextColumn

def display_tab_text_content(file_path=None, df=None):
    
    # Instantiates the TextColumn object
    if st.session_state.text_column is None:
        st.session_state.text_column = TextColumn(file_path=file_path, df=df) # Change df to state

    # Calls find_text_cols method to generate list of text columns
    st.session_state.text_column.find_text_cols()

    # Drop down list from text columns
    st.session_state.selected_text_col = st.selectbox(
        'Which text column do you want to explore',
        st.session_state.text_column.cols_list
    )

    # Setting up the data for the selected column
    st.session_state.text_column.set_data(col_name=st.session_state.selected_text_col)

    # First Streamlit Expander container
    with st.expander('Text Column', expanded=True):
        # Display the summary as a Streamlit table
        st.table(st.session_state.text_column.get_summary())

        # Display the bar chart
        st.write('**Bar Chart**')
        st.altair_chart(st.session_state.text_column.barchart, use_container_width=True)

        # Display the most frequent values dataframe
        st.write('**Most Frequent Values**')
        st.dataframe(st.session_state.text_column.frequent)