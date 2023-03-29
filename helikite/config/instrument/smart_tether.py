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

    def set_time_as_index(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        ''' Set the DateTime as index of the dataframe and correct if needed

        Using values in the time_offset variable, correct DateTime index
        '''

        # Date from header (stored in self.date), then add time
        df['DateTime'] = pd.to_datetime(self.date + pd.to_timedelta(df['Time']))
        df.drop(columns=["Time"], inplace=True)

        # Define the datetime column as the index
        df.set_index('DateTime', inplace=True)

        if (
            self.time_offset['hour'] != 0
            or self.time_offset['minute'] != 0
            or self.time_offset['second'] != 0
        ):
            print(f"Shifting the time offset by {self.time_offset}")

            df.index = df.index + pd.DateOffset(
                hours=self.time_offset['hour'],
                minutes=self.time_offset['minute'],
                seconds=self.time_offset['second'])


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
    header=2,
    export_order=600,
    pressure_variable='P (mbar)')
