''' Single Channel Tricolor Absorption Photometer (STAP)
The STAP measures the light absorption of particles deposited on a filter.

Resolution: 1 sec

Variables to keep: Everything

Time is is seconds since 1904-01-01 (weird starting date for Igor software)
'''

from .base import InstrumentConfig
from typing import Dict, Any, List

STAP = InstrumentConfig(
    dtype={
        "datetimes": "Int64",
        "sample_press_mbar": "Float64",
        "sample_temp_C": "Float64",
        "sigmab": "Float64",
        "sigmag": "Float64",
        "sigmar": "Float64",
        "sigmab_smth": "Float64",
        "sigmag_smth": "Float64",
        "sigmar_smth": "Float64",
    },
    na_values=["NAN"],
    )
