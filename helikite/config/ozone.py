'''
8) Ozone monitor -> LOG46.txt (can't use pressure)

Resolution: 2 sec

Headers: "ozone","cell_temp","cell_pressure","flow_rate","date","time"

(last column is nothing)
'''

from .base import InstrumentConfig
from typing import Dict, Any, List


OzoneMonitor = InstrumentConfig(
    na_values=["-"],
    index_col=0,
    header=None,
    names=["ozone",
           "cell_temp",
           "cell_pressure",
           "flow_rate",
           "date",
           "time",
           "unused"
    ],
    dtype={
        "ozone": "Float64",
        "cell_temp": "Float64",
        "cell_pressure": "Float64",
        "flow_rate": "Int64",
        "date": "str",
        "time": "str",
    },
)
