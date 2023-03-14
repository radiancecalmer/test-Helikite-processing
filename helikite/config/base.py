from typing import Dict, Any, List, Optional, Union, Callable
from pydantic import BaseModel
from pandas import DataFrame
from plotly.graph_objects import Figure


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
    file_identifier: Callable[[List[str]], bool]  # Function to ID the file
    create_plots: Callable[[DataFrame], Figure] | None  # Function to generate plots
    dataframe_corrections: Callable[[DataFrame], DataFrame] | None  # Function to perform corrections on the data (adjust time etc)
