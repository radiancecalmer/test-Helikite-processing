''' Single Channel Tricolor Absorption Photometer (STAP)
The STAP measures the light absorption of particles deposited on a filter.

Resolution: 1 sec

Variables to keep: Everything

Time is is seconds since 1904-01-01 (weird starting date for Igor software)
'''

from .base import Instrument
from typing import Dict, Any, List
import pandas as pd


class STAP(Instrument):
    def file_identifier(
        self,
        first_lines_of_csv
    ) -> bool:
        if first_lines_of_csv[0] == "datetimes,sample_press_mbar,sample_temp_C,sigmab,sigmag,sigmar,sigmab_smth,sigmag_smth,sigmar_smth\n":
            return True


    def set_time_as_index(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        ''' Set the DateTime as index of the dataframe and correct if needed

        Using values in the time_offset variable, correct DateTime index
        '''
        # Column 'datetimes' represents seconds since 1904-01-01
        df['DateTime'] = pd.to_datetime(
            pd.Timestamp("1904-01-01")
            + pd.to_timedelta(df['datetimes'], unit='s'))
        df.drop(columns=["datetimes"], inplace=True)

        # Define the datetime column as the index
        df.set_index('DateTime', inplace=True)

        return df

stap = STAP(
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
    export_order=500,
    pressure_variable='sample_press_mbar')
