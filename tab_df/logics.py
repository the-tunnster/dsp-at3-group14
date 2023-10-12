import pandas as pd


class Dataset:
    """
    --------------------
    Description
    --------------------
    -> Dataset (class): Class that manages a dataset loaded from Postgres

    --------------------
    Attributes
    --------------------
    -> file_path (str): Path to the uploaded CSV file (mandatory)
    -> df (pd.Dataframe): Pandas dataframe (default set to None)
    -> cols_list (list): List of columns names of dataset (default set to empty list)
    -> n_rows (int): Number of rows of dataset (default set to 0)
    -> n_cols (int): Number of columns of dataset (default set to 0)
    -> n_duplicates (int): Number of duplicated rows of dataset (default set to 0)
    -> n_missing (int): Number of missing values of dataset (default set to 0)
    -> n_num_cols (int): Number of columns that are numeric type (default set to 0)
    -> n_text_cols (int): Number of columns that are text type (default set to 0)
    -> table (pd.Series): Pandas DataFrame containing the list of columns, their data types and memory usage from dataframe (default set to None)
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cols_list = []
        self.n_rows = 0
        self.n_cols = 0
        self.n_duplicates = 0
        self.n_missing = 0
        self.n_num_cols = 0
        self.n_text_cols = 0
        self.table = None

    def set_data(self):
        if self.df is None:
            raise ValueError("No dataframe loaded. Use `load_data` method to load the dataframe first.")

        # Update the columns list
        self.cols_list = self.df.columns.tolist()

        # Update the number of rows and columns
        self.n_rows = len(self.df)
        self.n_cols = len(self.cols_list)

        # Compute the number of duplicated rows
        self.n_duplicates = self.df.duplicated().sum()

        # Compute the number of missing values in the dataframe
        self.n_missing = self.df.isnull().sum().sum()

        # Compute the number of numeric columns
        self.n_num_cols = self.df.select_dtypes(include=["number"]).shape[1]

        # Compute the number of text columns
        self.n_text_cols = self.df.select_dtypes(exclude=["number"]).shape[1]

        # Update the table with column information
        self.create_table()
        
        
    def set_df(self):
        if self.df is not None:
            print("Dataframe already loaded.")
            return

        try:
            self.df = pd.read_csv(self.file_path)
            print("Dataframe loaded successfully from", self.file_path)
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
        except Exception as e:
            print(f"An error occurred while loading the dataframe: {e}")

        

    def is_df_none(self):
        if self.df is None:
            return True
        
        if self.df.empty:
            return True

        return False
        

    def set_columns(self):
        """
        Extracts the list of columns names from self.df and stores the results in the relevant attribute (self.cols_list) if self.df is not empty nor None.
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to extract columns.")
            return

        self.cols_list = self.df.columns.tolist()
        print("Columns extracted and stored in self.cols_list.")
        

    def set_dimensions(self):
        """
        Computes the dimensions (number of columns and rows) of self.df and stores the results in the relevant attributes (self.n_rows, self.n_cols) if self.df is not empty nor None.
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to compute dimensions.")
            return

        self.n_rows, self.n_cols = self.df.shape
        print(f"Dimensions computed. Rows: {self.n_rows}, Columns: {self.n_cols}.")

            

    def set_duplicates(self):
        """
        Computes the number of duplicated rows in self.df and stores the result in the relevant attribute (self.n_duplicates) if self.df is not empty nor None.
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to compute number of duplicates.")
            return

        self.n_duplicates = self.df.duplicated().sum()
        print(f"Number of duplicated rows computed: {self.n_duplicates}.")

        

    def set_missing(self):
        """
        Computes the number of missing values in self.df and stores the result in the relevant attribute (self.n_missing) if self.df is not empty nor None.
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to compute number of missing values.")
            return

        self.n_missing = self.df.isnull().sum().sum()
        print(f"Number of missing values computed: {self.n_missing}.")

        

    def set_numeric(self):
        """
        Computes the number of columns that are numeric type in self.df and stores the result in the relevant attribute (self.n_num_cols) if self.df is not empty nor None.
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to compute number of numeric columns.")
            return

        self.n_num_cols = self.df.select_dtypes(include=['number']).shape[1]
        print(f"Number of numeric columns computed: {self.n_num_cols}.")

        

    def set_text(self):
        """
        Computes the number of columns that are text type in self.df and stores the result in the relevant attribute (self.n_text_cols) if self.df is not empty nor None.
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to compute number of text columns.")
            return

        self.n_text_cols = self.df.select_dtypes(include=['object']).shape[1]
        print(f"Number of text columns computed: {self.n_text_cols}.")

        

    def get_head(self, n=5):
        """
        Computes the first rows of self.df according to the provided number of rows specified as parameter (default: 5) if self.df is not empty nor None.

        Parameters:
        n (int): Number of rows to be returned. Default is 5.

        Returns:
        pd.DataFrame: First 'n' rows of self.df.
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to retrieve first rows.")
            return pd.DataFrame()  # Return empty dataframe as a fallback

        return self.df.head(n)

        

    def get_tail(self, n=5):
        """
        Computes the last rows of self.df according to the provided number of rows specified as parameter (default: 5) if self.df is not empty nor None.

        Parameters:
        n (int): Number of rows to be returned. Default is 5.

        Returns:
        pd.DataFrame: Last 'n' rows of self.df.
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to retrieve last rows.")
            return pd.DataFrame()  # Return empty dataframe as a fallback

        return self.df.tail(n)

        

    def get_sample(self, n=5):
        """
        Computes a random sample of rows from self.df according to the provided number of rows specified as parameter (default: 5) if self.df is not empty nor None.

        Parameters:
        n (int): Number of rows to be sampled. Default is 5.

        Returns:
        pd.DataFrame: Random 'n' rows sample from self.df.
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to retrieve a sample.")
            return pd.DataFrame()  # Return empty dataframe as a fallback

        return self.df.sample(n)

        


    def set_table(self):
        """
        Computes a DataFrame containing the list of columns with their data types and memory usage. The result is stored in the attribute (self.table) if self.df is not empty nor None.

        Returns:
        None
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to compute the table.")
            return

        data_types = self.df.dtypes
        memory_usage = self.df.memory_usage(deep=True)

        self.table = pd.DataFrame({
            "Column Name": self.df.columns,
            "Data Type": data_types,
            "Memory Usage (Bytes)": memory_usage
        }).reset_index(drop=True)

        print("Table computed and stored in self.table.")



    def get_summary(self):
        """
        Formats all requested information from self.df to be displayed in the Dataframe tab of Streamlit app as a Pandas dataframe with 2 columns: Description and Value.

        Returns:
        pd.DataFrame: Formatted dataframe to be displayed on the Streamlit app.
        """
        if self.is_df_none():
            print("self.df is None or empty. Unable to compute the summary.")
            return pd.DataFrame(columns=["Description", "Value"])

        # Gather the data in lists
        descriptions = [
            "Number of Rows",
            "Number of Columns",
            "Number of Duplicated Rows",
            "Number of Missing Values",
            "Number of Numeric Columns",
            "Number of Text Columns"
        ]
        values = [
            self.n_rows,
            self.n_cols,
            self.n_duplicates,
            self.n_missing,
            self.n_num_cols,
            self.n_text_cols
        ]

        # Convert to DataFrame
        summary_df = pd.DataFrame({
            "Description": descriptions,
            "Value": values
        })

        return summary_df

