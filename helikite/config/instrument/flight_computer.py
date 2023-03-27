'''

1) Flight computer -> LOG_20220929.txt (has pressure)

Data from the onboard microcontroller. Resolution: 1 sec
DateTime in seconds since 1970-01-01 (to be verified)

Variables to keep: DateTime, P_baro, CO2, TEMP1, TEMP2, TEMPsamp, RH1, RH2, RHsamp, mFlow
Houskeeping variables: TEMPbox, vBat
'''

from .base import Instrument
from typing import Dict, Any, List
import plotly.graph_objects as go
from plotly.graph_objects import Figure
import pandas as pd
from io import StringIO
import csv


CSV_HEADER = "SBI,DateTime,PartCon,CO2,P_baro,TEMPbox,mFlow,TEMPsamp,RHsamp,TEMP1,RH1,TEMP2,RH2,vBat\n"


class FlightComputer(Instrument):
    def file_identifier(
        self,
        first_lines_of_csv
    ) -> bool:
        if first_lines_of_csv[0] == CSV_HEADER:
            return True

    def data_corrections(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        df['DateTime'] = pd.to_datetime(df['DateTime'], unit='s')

        return df


    def create_plots(
        self,
        df: pd.DataFrame
    ) -> Figure:
        fig = go.Figure()

        # Add TEMPBox
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df.TEMPbox,
                name="TEMPBox"))

        # Add TEMPBox
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df.vBat,
                name="vBat"))

        fig.update_layout(title="Flight Computer")

        return fig

    def read_data(
        self
    ) -> pd.DataFrame:
        ''' Read data into dataframe '''

        # Parse the file first removing the duplicate header cols
        cleaned_csv = StringIO()
        header_counter = 0

        with open(self.filename, 'r') as csv_data:
            for row in csv_data:
                if row == CSV_HEADER:
                    if header_counter == 0:
                        # Only append the first header, ignore all others
                        cleaned_csv.write(row)
                    header_counter += 1
                else:
                    cleaned_csv.write(row)

        # Seek back to start of memory object
        cleaned_csv.seek(0)

        df = pd.read_csv(
            cleaned_csv,  # Load the StringIO object created above
            dtype=self.dtype,
            na_values=self.na_values,
            header=self.header,
            delimiter=self.delimiter,
            lineterminator=self.lineterminator,
            comment=self.comment,
            names=self.names,
            index_col=self.index_col,
        )

        return df


flight_computer = FlightComputer(
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
    cols_housekeeping=["TEMPbox", "vBat"],
    cols_export=["P_baro", "CO2", "TEMP1", "TEMP2", 
                 "TEMPsamp", "RH1", "RH2", "RHsamp", "mFlow"],
    export_order=100)
