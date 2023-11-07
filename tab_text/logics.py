import pandas as pd
import altair as alt

class TextColumn:

    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.n_empty  = None
        self.n_mode = None
        self.n_space = None
        self.n_lower = None
        self.n_upper = None
        self.n_alpha = None
        self.n_digit = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])
    

    def find_text_cols(self):

        # Checks if df was passed when object instantiated
        if self.df is not None:
            print("Dataframe already loaded.")
            self.cols_list = self.df.select_dtypes(include=['object', 'string']).columns
            return

        # If not load the file from the file path
        try:
            self.df = pd.read_csv(self.file_path)
            print("Dataframe loaded successfully from", self.file_path)
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
        except Exception as e:
            print(f"An error occurred while loading the dataframe: {e}")

        # updates all columns with strings/objects
        self.cols_list = self.df.select_dtypes(include=['object', 'string']).columns
        

    def set_data(self, col_name):

        # Set up column we are investigating
        self.serie = self.df[col_name]
        self.convert_serie_to_text()

        # Check if column is empty
        if(self.is_serie_none()):
            print('Column is Empty')
        else:
            print('Column is not empty')
            # Set Values from selected column
            self.set_unique()
            self.set_missing()
            self.set_empty()
            self.set_mode()
            self.set_whitespace()
            self.set_lowercase()
            self.set_uppercase()
            self.set_alphabet()
            self.set_digit()
            self.set_barchart()
            self.set_frequent()
        

    def convert_serie_to_text(self):

        # Converts series to string values, whilst keeping NaN as is (to count for missing values)
        self.serie = self.serie.where(self.serie.isna(), self.serie.astype(str))
        

    def is_serie_none(self):

        # Checks if the series is None or if an empty pandas Series
        if self.serie is None:
            return True
        elif isinstance(self.serie, pd.Series):
            return self.serie.dropna().empty
        else:
            return False
        

    def set_unique(self):

        # Counts unique values in series and stores in n_unique attribute.
        self.n_unique = self.serie.nunique()
        

    def set_missing(self):

        # Counts NaN values in series and stores in n_missing attribute.
        self.n_missing = self.serie.isnull().sum()
        

    def set_empty(self):

        # Counts empty string in series and stores in n_empty attribute.
        self.n_empty = (self.serie=="").sum()


    def set_mode(self):

        # Counts the first most frequently occurring value in series and stores in n_mode attribute.
        self.n_mode = self.serie.mode()[0]


    def set_whitespace(self):

        # Counts whitespace in series and stores in n_space attribute.
        self.n_space = self.serie.str.isspace().sum()
        

    def set_lowercase(self):

        # Counts rows with all lower case characters in series and stores in n_lower attribute.
        self.n_lower = self.serie.str.islower().sum()


    def set_uppercase(self):

        # Counts rows with all upper case characters in series and stores in n_upper attribute.
        self.n_upper = self.serie.str.isupper().sum()

    
    def set_alphabet(self):

        # Counts rows with only alphabetic characters in series and stores in n_alpha attribute.
        self.n_alpha = self.serie.str.isalpha().sum()


    def set_digit(self):

        # Counts rows with only numeric characters in series and stores in n_digit attribute.
        self.n_digit = self.serie.str.isdigit().sum()
        

    def set_barchart(self):  

        # Creates dataframe with unique value for rows and a colummn with the count
        agg_serie = self.serie.value_counts().reset_index()
        agg_serie.rename(columns={agg_serie.columns[0]:self.serie.name, 
                                  agg_serie.columns[1]:'Count of Records'}, 
                         inplace=True)

        # Creates the barchart and stores in barchart object
        self.barchart = (
        alt.Chart(agg_serie).mark_bar().encode(
            x=alt.X(agg_serie.columns[0], sort='-y'),
            y='Count of Records'
            )
        )

      
    def set_frequent(self, end=20):

        # Create dataframe with rows of unique values and column with count
        str_counts = self.serie.value_counts()
        # Create a column of percentages
        str_percentage = str_counts/len(self.serie)

        # Creates the dataframe with summary values
        self.frequent = (pd.DataFrame({'occurrence': str_counts,
                                'percentage': str_percentage})
                                .reset_index(names=['value'])
                                .head(end))
        

    def get_summary(self):

        # Creating the dataframe that shows the summary values.
        dataframe = pd.DataFrame(data={'Description':['Number of Unique Values',
                                            'Number of Rows with Missing Values',
                                            'Number of Empty Rows',
                                            'Number of Rows with Only Whitespace',
                                            'Number of Rows with Only Lowercases',
                                            'Number of Rows with Only Uppercases',
                                            'Number of Rows with Only Alphabet',
                                            'Number of Rows with Only Digits',
                                            'Mode Value'],
                             'Value':[self.n_unique,
                                      self.n_missing,
                                      self.n_empty,
                                      self.n_space,
                                      self.n_lower,
                                      self.n_upper,
                                      self.n_alpha,
                                      self.n_digit,
                                      self.n_mode]},
                             dtype='object'
                            ).astype(str)
        
        return dataframe