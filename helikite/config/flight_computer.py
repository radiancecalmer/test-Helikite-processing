'''

1) Flight computer -> LOG_20220929.txt (has pressure)

Data from the onboard microcontroller. Resolution: 1 sec
DateTime in seconds since 1970-01-01 (to be verified)

Variables to keep: DateTime, P_baro, CO2, TEMP1, TEMP2, TEMPsamp, RH1, RH2, RHsamp, mFlow
Houskeeping variables: TEMPbox, vBat

'''

from .base import InstrumentConfig
from typing import Dict, Any, List


def file_identifier(first_lines_of_csv):
    if first_lines_of_csv[0] == "SBI,DateTime,PartCon,CO2,P_baro,TEMPbox,mFlow,TEMPsamp,RHsamp,TEMP1,RH1,TEMP2,RH2,vBat\n":
        return True

FlightComputer = InstrumentConfig(
    dtype={
        'SBI': "str",
        'DateTime': "Int64",
        'PartCon': "Int64",
        'CO2': "Float64",
        'P_baro': "Float64",
        'TEMPbox': "Float64",
        'mFlow': "str",
        'TEMPsamp': "Float64",
        'RHsamp': "Float64",
        'TEMP1': "Float64",
        'RH1': "Float64",
        'TEMP2': "Float64",
        'RH2': "Float64",
        'vBat': "Float64",
    },
    na_values=["NA"],
    comment="#",
    file_identifier=file_identifier)
