'''

2) SmartTether -> LOG_20220929_A.csv (has pressure)

The SmartTether is a weather sonde. time res 2 seconds if lon lat recorded. 1 sec if not.

Important variables to keep:
Time, Comment, P (mbar), T (deg C), RH (%), Wind (degrees), Wind (m/s), UTC Time, Latitude (deg), Longitude (deg)

!!! Date is not reported in the data, but only in the header (yes, it's a pity)
-> therefore, I wrote a function that to includes the date but it needs to change date if we pass midnight (not implemented yet).

'''

from .base import Instrument
from typing import Dict, Any, List
import datetime
import pandas as pd


class SmartTether(Instrument):
    def date_extractor(
        self,
        first_lines_of_csv
    ) -> datetime:
        date_line = first_lines_of_csv[1]
        date_string = date_line.split(' ')[-1].strip()

        return datetime.datetime.strptime(date_string, "%m/%d/%Y")


    def file_identifier(
        self,
        first_lines_of_csv
    ) -> bool:
        if (first_lines_of_csv[0] == "SmartTether log file\n"
            and first_lines_of_csv[3] == "Time,Comment,Module ID,Alt (m),P (mbar),T (deg C),%RH,Wind (degrees),Wind (m/s),Supply (V),UTC Time,Latitude (deg),Longitude (deg),Course (deg),Speed (m/s)\n"):
            return True


    def data_corrections(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        # Date from header (stored in self.date), then add time
        df['DateTime'] = pd.to_datetime(self.date + pd.to_timedelta(df['Time']))
        df.drop(columns=["Time"], inplace=True)

        return df

smart_tether = SmartTether(
    dtype={
        "Time": "str",
        "Comment": "str",
        "Module ID": "str",
        "Alt (m)": "Int64",
        "P (mbar)": "Float64",
        "T (deg C)": "Float64",
        "%RH": "Float64",
        "Wind (degrees)": "Int64",
        "Wind (m/s)": "Float64",
        "Supply (V)": "Float64",
        "UTC Time": "str",
        "Latitude (deg)": "Float64",
        "Longitude (deg)": "Float64",
        "Course (deg)": "Float64",
        "Speed (m/s)": "Float64",
    },
    header=2)
