import streamlit as st
from tab_num.logics import NumericColumn

def display_tab_num_content(file_path=None, df=None):
    st.title("Numeric Columns Analysis")

    # Instantiate the NumericColumn class based on file_path or df
    if file_path:
        numeric_col = NumericColumn(file_path=file_path)
    elif df is not None:
        numeric_col = NumericColumn(df=df)
    else:
        st.warning("Please upload a CSV file or provide a dataframe to analyze numeric columns.")
        return

    # Find all numeric columns
    numeric_col.find_num_cols()

    # Display a select box to choose a numeric column
    selected_col = st.selectbox("Which numeric column do you want to explore?", numeric_col.cols_list)

    if selected_col:
        # Set the selected column data
        numeric_col.set_data(selected_col)

        # Display an Expander container with results
        with st.expander("Numeric Column Analysis Results"):
            st.subheader(f"Summary of {selected_col}")
            summary_df = numeric_col.get_summary()
            st.table(summary_df)

            st.subheader(f"Histogram of {selected_col}")
            numeric_col.set_histogram()
            st.altair_chart(numeric_col.histogram, use_container_width=True)

            st.subheader(f"Most Frequent Values in {selected_col}")
            numeric_col.set_frequent()
            st.write(numeric_col.frequent)

if __name__ == '__main__':
    display_tab_num_content()
    