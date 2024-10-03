import pandas as pd
from helikite.instruments.base import Instrument


# Mock Instrument class for testing purposes
class MockInstrument(Instrument):
    def __init__(self, name, data=None, **kwargs):
        # Initialize the base Instrument class with given parameters
        super().__init__(**kwargs)
        self.name = name
        # Initialize the DataFrame from provided data or set to an empty DataFrame
        self.df_raw = pd.DataFrame(
            data if data else {"time": [], "pressure": []}
        )
        self.df = self.df_raw.copy()

    def file_identifier(self, first_lines_of_csv):
        # Assume mock instrument always identifies its file for simplicity
        return True

    def read_data(self):
        # Return the raw DataFrame for testing
        return self.df_raw

    def data_corrections(self, df, **kwargs):
        # Apply a mock correction, for instance adding a constant to pressure
        df["pressure"] += 10
        return df

    def set_time_as_index(self, df):
        # Set the "time" column as the index
        df.index = pd.to_datetime(df["time"])
        return df
