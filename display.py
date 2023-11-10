import streamlit as st
from tab_date.logics import DateColumn

def display_tab_date_content(file_path=None, df=None):
   
    # Instantiates the DateColumn object
    if st.session_state.date_column is None:
        st.session_state.date_column = DateColumn(file_path=file_path, df=df)
    
    # Calls find_date_cols method to generate a list of datetime columns
    st.session_state.date_column.find_date_cols()

    # Dropdown list for datetime columns
    st.session_state.selected_date_col = st.selectbox(
        'Which datetime column do you want to explore',
        st.session_state.date_column.cols_list
    )

    # Setting up the data for the selected column
    st.session_state.date_column.set_data(col_name=st.session_state.selected_date_col)

    # First Streamlit Expander container
    with st.expander('Datetime Column', expanded=True):
        # Display the summary as a Streamlit table
        st.table(st.session_state.date_column.get_summary())

        # Display the bar chart
        st.write('**Bar Chart**')
        st.altair_chart(st.session_state.date_column.barchart, use_container_width=True)

        # Display the most frequent values dataframe
        st.write('**Most Frequent Values**')
        st.dataframe(st.session_state.date_column.frequent)

if __name__ == '__main__':
    display_tab_date_content()
