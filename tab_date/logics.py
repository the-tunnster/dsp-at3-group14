# tab_date/logics.py

import pandas as pd
import altair as alt

class DateColumn:
    def __init__(self, file_path=None, df=None):
        """
        Class constructor to initialize the DateColumn object.
        """
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_min = None
        self.col_max = None
        self.n_weekend = None
        self.n_weekday = None
        self.n_future = None
        self.n_empty_1900 = None
        self.n_empty_1970 = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])
    
    def find_date_cols(self):
        """
        Method to find columns of datetime data type in the dataframe.
        If no datetime columns are found, it looks for text columns.
        """
        if self.df is None:
            if self.file_path is not None:
                self.df = pd.read_csv(self.file_path)
            else:
                return

        date_cols = self.df.select_dtypes(include=['datetime']).columns
        if len(date_cols) == 0:
            # If no datetime columns found, look for text columns
            text_cols = self.df.select_dtypes(include=['object']).columns
            self.cols_list = text_cols.tolist()
        else:
            self.cols_list = date_cols.tolist()

    def set_data(self, col_name):
        """
        Method to set data for analysis based on the selected column name.
        """
        if self.df is None:
            return

        if col_name in self.cols_list:
            self.serie = self.df[col_name].dropna()  # Drop rows with null values
            self.convert_serie_to_date()
            self.set_unique()
            self.set_missing()
            self.set_min()
            self.set_max()
            self.set_weekend()
            self.set_weekday()
            self.set_future()
            self.set_empty_1900()
            self.set_empty_1970()
            self.set_barchart()
            self.set_frequent()

    def convert_serie_to_date(self):
        """
        Method to convert a Pandas Series to datetime data type.
        """
        if self.serie is not None:
            self.serie = pd.to_datetime(self.serie, errors='coerce')

    def is_serie_none(self):
        """
        Method to check if self.serie is empty or None.
        """
        return self.serie is None

    def set_unique(self):
        """
        Method to compute the number of unique values in a series.
        """
        if not self.is_serie_none():
            self.n_unique = self.serie.nunique()

    def set_missing(self):
        """
        Method to compute the number of missing values in a series.
        """
        if not self.is_serie_none():
            self.n_missing = self.serie.isnull().sum()

    def set_min(self):
        """
        Method to compute the minimum value in a series.
        """
        if not self.is_serie_none():
            self.col_min = self.serie.min()

    def set_max(self):
        """
        Method to compute the maximum value in a series.
        """
        if not self.is_serie_none():
            self.col_max = self.serie.max()

    def set_weekend(self):
        """
        Method to compute the number of times a series has dates falling during the weekend.
        """
        if not self.is_serie_none():
            self.n_weekend = self.serie.dt.weekday.isin([5, 6]).sum()

    def set_weekday(self):
        """
        Method to compute the number of times a series has dates not falling during the weekend.
        """
        if not self.is_serie_none():
            self.n_weekday = (~self.serie.dt.weekday.isin([5, 6])).sum()

    def set_future(self):
        """
        Method to compute the number of times a series has dates falling in the future.
        """
        if not self.is_serie_none():
            today = pd.to_datetime('today').normalize()
            self.n_future = (self.serie > today).sum()

    def set_empty_1900(self):
        """
        Method to compute the number of times a series has dates equal to '1900-01-01'.
        """
        if not self.is_serie_none():
            self.n_empty_1900 = (self.serie == '1900-01-01').sum()

    def set_empty_1970(self):
        """
        Method to compute the number of times a series has only numeric characters.
        """
        if not self.is_serie_none():
            if self.serie.dtype.kind in 'iufc':  # Check if the dtype is numeric
                self.n_empty_1970 = 0
            else:
                self.n_empty_1970 = self.serie.astype(str).str.isnumeric().sum()


    def set_barchart(self):
        """
        Method to compute the Altair barchart displaying the count for each value in a series.
        """
        if not self.is_serie_none():
            chart = alt.Chart(self.df).mark_bar().encode(
                alt.X(f'{self.serie.name}:O', title='Date'),
                alt.Y('count():Q', title='Count')  # Use Quantitative (numeric) encoding for Y-axis
            )
            self.barchart = chart

    def set_frequent(self, end=20):
        """
        Method to compute the dataframe containing the most frequent values in a series.
        """
        if not self.is_serie_none():
            values_count = self.serie.value_counts().reset_index()
            values_count.columns = ['value', 'occurrence']
            values_count['percentage'] = values_count['occurrence'] / len(self.serie) * 100
            self.frequent = values_count.head(end)

    def get_summary(self):
        """
        Method to format all requested information from self.serie for display.
        Returns a Pandas dataframe with two columns: Description and Value.
        """
        data = {
            'Description': ['Number of Unique Values', 'Number of Missing Values', 'Min Value', 'Max Value',
                             'Number of Weekend Dates', 'Number of Weekday Dates', 'Number of Future Dates',
                             "Number of '1900-01-01' Dates", 'Number of Numeric Dates'],
            'Value': [self.n_unique, self.n_missing, self.col_min, self.col_max,
                      self.n_weekend, self.n_weekday, self.n_future,
                      self.n_empty_1900, self.n_empty_1970]
        }

        summary_df = pd.DataFrame(data)
        return summary_df
