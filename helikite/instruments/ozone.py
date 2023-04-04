'''
8) Ozone monitor -> LOG46.txt (can't use pressure)

Resolution: 2 sec

Headers: "ozone","cell_temp","cell_pressure","flow_rate","date","time"

(last column is nothing)
'''

from .base import Instrument
from typing import Dict, Any, List
import pandas as pd


class OzoneMonitor(Instrument):
    def file_identifier(
        self,
        first_lines_of_csv
    ) -> bool:
        # This one is tricky. There is no header! May run into conflicts later
        # Check there are six commas in the first line, and ends in 0, and only a
        # newline in the second
        if (first_lines_of_csv[0][-2] == '0'
            and first_lines_of_csv[0].count(',') == 6
            and first_lines_of_csv[1] == '\n'
        ):
            return True


    def data_corrections(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:


        df['DateTime'] = pd.to_datetime(
            df['date'] + ' ' + df['time'],
            format="%d/%m/%y %H:%M:%S")
        df.drop(columns=["date", "time"], inplace=True)

        return df

ozone_monitor = OzoneMonitor(
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
    })
