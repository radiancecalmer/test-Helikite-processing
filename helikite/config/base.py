from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel


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
