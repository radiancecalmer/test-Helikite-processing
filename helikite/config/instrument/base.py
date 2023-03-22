from typing import Dict, Any, List, Optional, Union, Callable
from pydantic import BaseModel
from pandas import DataFrame
from plotly.graph_objects import Figure
from datetime import datetime


class Instrument:
    def __init__(
        self,
        dtype: Dict[Any, Any]={},             # Mapping of column to data type
        na_values: List[Any] | None = None,   # List of values to consider null
        header: int | None = 0,               # Row ID for the header
        delimiter: str = ",",                 # String delimiter
        lineterminator: str | None = None,    # The character to define EOL
        comment: str | None = None,           # Ignore anything after set char
        names: List[str] | None = None,       # Names of headers if non existant
        index_col: bool | int | None = None,  # The column ID of the index
    ) -> None:

        self.dtype = dtype
        self.na_values = na_values
        self.header = header
        self.delimiter = delimiter
        self.lineterminator = lineterminator
        self.comment = comment
        self.names = names
        self.index_col = index_col

        # Properties that are not part of standard config, can be added
        self.filename: str | None = None
        self.date: datetime | None = None



    def data_corrections(self, df):
        ''' Default callback function for data corrections.

        Return with no changes
        '''

        return df

    def create_plots(self, df: DataFrame):
        ''' Default callback for generated figures from dataframes

        Return nothing, as anything else will populate the list that is written out
        to HTML.
        '''

        return

    def file_identifier(self, first_lines_of_csv: List[str]):
        ''' Default file identifier callback

        Must return false. True would provide false positives.
        '''

        return False

    def date_extractor(self, first_lines_of_csv: List[str]):
        ''' Returns the date of the data sample from a CSV header

        Can be used for an instrument that reports the date in header
        instead of in the data field.

        Return None if there is nothing to do here
        '''

        return None
