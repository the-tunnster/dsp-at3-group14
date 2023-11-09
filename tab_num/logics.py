import pandas as pd
import altair as alt
import streamlit as st


class NumericColumn:
    """
    --------------------
    Description
    --------------------
    -> NumericColumn (class): Class that manages a column of numeric data type

    --------------------
    Attributes
    --------------------
    -> file_path (str): Path to the uploaded CSV file (optional)
    -> df (pd.Dataframe): Pandas dataframe (optional)
    -> cols_list (list): List of columns names of dataset that are numeric type (default set to empty list)
    -> serie (pd.Series): Pandas serie where the content of a column has been loaded (default set to None)
    -> n_unique (int): Number of unique value of a serie (default set to None)
    -> n_missing (int): Number of missing values of a serie (default set to None)
    -> col_mean (int): Average value of a serie (default set to None)
    -> col_std (int): Standard deviation value of a serie (default set to None)
    -> col_min (int): Minimum value of a serie (default set to None)
    -> col_max (int): Maximum value of a serie (default set to None)
    -> col_median (int): Median value of a serie (default set to None)
    -> n_zeros (int): Number of times a serie has values equal to 0 (default set to None)
    -> n_negatives (int): Number of times a serie has negative values (default set to None)
    -> histogram (alt.Chart): Altair histogram displaying the count for each bin value of a serie (default set to empty)
    -> frequent (pd.DataFrame): Datframe containing the most frequest value of a serie (default set to empty)

    """
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_mean = None
        self.col_std = None
        self.col_min = None
        self.col_max = None
        self.col_median = None
        self.n_zeros = None
        self.n_negatives = None
        self.histogram = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])

    def find_num_cols(self):

        if self.df is None:
            # Load the uploaded CSV file into a Pandas DataFrame
            # You can use streamlit's file_uploader for this
            uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
            if uploaded_file:
                self.df = pd.read_csv(uploaded_file)

        # Find columns of numeric data type
        if self.df is not None:
            numeric_columns = self.df.select_dtypes(include=['float64', 'int64']).columns
            self.cols_list = list(numeric_columns)

    def set_data(self, col_name):
        
        if self.df is not None and col_name in self.cols_list:
            self.serie = self.df[col_name]

            # Compute requested information from self.serie
            self.n_unique = self.serie.nunique()
            self.n_missing = self.serie.isna().sum()
            self.col_mean = self.serie.mean()
            self.col_std = self.serie.std()
            self.col_min = self.serie.min()
            self.col_max = self.serie.max()
            self.col_median = self.serie.median()
            self.n_zeros = (self.serie == 0).sum()
            self.n_negatives = (self.serie < 0).sum()

    def convert_serie_to_num(self):
        
        if self.serie is not None:
            # Attempt to convert the series to numeric type
            try:
                self.serie = pd.to_numeric(self.serie, errors='coerce')
            except ValueError:
                st.warning("Conversion to numeric type failed. Check the data in the series.")

    def is_serie_none(self):
        
        if self.serie is not None and not self.serie.empty:
            return False
        else:
            return True

    def set_unique(self):
        
        if self.serie is not None and not self.serie.empty:
            self.n_unique = self.serie.nunique()

    def set_missing(self):
       
        if self.serie is not None and not self.serie.empty:
            self.n_missing = self.serie.isna().sum()  

    def set_zeros(self):
        
        if self.serie is not None and not self.serie.empty:
            self.n_zeros = (self.serie == 0).sum()
        
    def set_negatives(self):
       
        if self.serie is not None and not self.serie.empty:
            self.n_negatives = (self.serie < 0).sum()   

    def set_mean(self):
        
        if self.serie is not None and not self.serie.empty:
            self.col_mean = self.serie.mean()    

    def set_std(self):
        
        if self.serie is not None and not self.serie.empty:
            self.col_std = self.serie.std()  
    
    def set_min(self):
       
        if self.serie is not None and not self.serie.empty:
            self.col_min = self.serie.min() 

    def set_max(self):
       
        if self.serie is not None and not self.serie.empty:
            self.col_max = self.serie.max()  

    def set_median(self):
        
        if self.serie is not None and not self.serie.empty:
            self.col_median = self.serie.median()

    def set_histogram(self):
        
        if self.serie is not None and not self.serie.empty:
            chart = alt.Chart(self.df).mark_bar().encode(
                alt.X(f"{self.serie.name}:Q", bin=alt.Bin(maxbins=20)),
                y="count()",
            ).properties(
                width=600,
                height=400
            )
            self.histogram = chart

    def set_frequent(self, end=20):
        
        if self.serie is not None and not self.serie.empty:
            frequent_values = self.serie.value_counts().reset_index()
            frequent_values.columns = ["value", "occurrence"]
            frequent_values["percentage"] = (frequent_values["occurrence"] / len(self.serie)) * 100
            self.frequent = frequent_values.head(end)
        
    def get_summary(self,):
        
        if self.serie is not None and not self.serie.empty:
            summary_df = pd.DataFrame({
                "Description": ["Number of Unique Values", "Number of Missing Values", "Average Value",
                                "Standard Deviation", "Minimum Value", "Maximum Value", "Median Value",
                                "Number of Zeros", "Number of Negatives"],
                "Value": [self.n_unique, self.n_missing, self.col_mean, self.col_std, self.col_min,
                          self.col_max, self.col_median, self.n_zeros, self.n_negatives]
            })

            # Format the numeric values in the summary table as two decimal places
            summary_df["Value"] = summary_df["Value"].apply(lambda x: f"{x:.2f}")
            

        return summary_df

