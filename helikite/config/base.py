from typing import Dict, Any, List, Optional, Union, Callable
from pydantic import BaseModel
from pandas import DataFrame
from plotly.graph_objects import Figure


def default_corrections(df):
    ''' Default callback function for data corrections.

    Return with no changes
    '''

    return df

def default_plots(df: DataFrame):
    ''' Default callback for generated figures from dataframes

    Return nothing, as anything else will populate the list that is written out
    to HTML.
    '''

    return

def default_file_identifier(first_lines_of_csv: List[str]):
    ''' Default file identifier callback

    Must return false. True would provide false positives.
    '''

    return False


class InstrumentConfig(BaseModel):
    ''' Define an instrument configuration with explicit default values

    The keys maintain the relationship to Pandas' read_csv() parameters
    https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
    '''

    dtype: Dict[Any, Any] = {}              # Mapping of column to data type
    na_values: List[Any] | None = None      # List of values to consider as null
    header: int | None = 0                  # Row ID for the header
    delimiter: str = ","                    # String delimiter
    lineterminator: str | None = None       # The character to define EOL
    comment: str | None = None              # Ignore anything after set char
    names: List[str] | None = None          # Names of headers if non existant
    index_col: bool | int | None = None     # The column ID of the index

    # Callback functions to offer bespoke configurations for each instrument
    # Defaults defined above
    file_identifier: Callable[[List[str]], bool] = default_file_identifier
    create_plots: Callable[[DataFrame], Figure] = default_plots
    data_corrections: Callable[[DataFrame], DataFrame] = default_corrections


