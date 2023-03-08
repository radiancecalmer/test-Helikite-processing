from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel


class ConfigType(str, Enum):
    instrument = "instrument"


# @dataclass
class InstrumentConfig(BaseModel):
    ''' Define an instrument configuration with explicit default values

    The keys maintain the relationship to Pandas' read_csv() parameters
    https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
    '''

    # type: ConfigType = "instrument"
    dtype: Dict[Any, Any] = {}
    na_values: List[Any] = []
    header: int = 0  # Row ID for the header
    delimiter: str = ","
    lineterminator: Optional[str] = None
    comment: Optional[str] = None
