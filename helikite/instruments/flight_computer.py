'''

1) Flight computer -> LOG_20220929.txt (has pressure)

Data from the onboard microcontroller. Resolution: 1 sec
DateTime in seconds since 1970-01-01 (to be verified)

Variables to keep: DateTime, P_baro, CO2, TEMP1, TEMP2, TEMPsamp, RH1, RH2, RHsamp, mFlow
Houskeeping variables: TEMPbox, vBat
'''

from instruments.base import Instrument
from typing import Dict, Any, List
import plotly.graph_objects as go
from plotly.graph_objects import Figure
import plotly.express as px
import pandas as pd
from processing.conversions import pressure_to_altitude
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

        print(df.index)
        # Create altitude column by using average of first 10 seconds of data

        first_10s = df.loc[
            df.index[0]:df.index[0] + pd.Timedelta(seconds=10)
        ]
        average_first_10s = first_10s.mean()

        print(average_first_10s[self.pressure_variable])
        print(average_first_10s.TEMP1)
        print(average_first_10s)
        df['Altitude'] = df[self.pressure_variable].apply(
            pressure_to_altitude,
            pressure_at_start=average_first_10s[self.pressure_variable],
            temperature_at_start=average_first_10s.TEMP1,
            altitude_at_start=0
        )

        return df

    def set_time_as_index(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        ''' Set the DateTime as index of the dataframe and correct if needed

        Using values in the time_offset variable, correct DateTime index
        '''

        # Flight computer uses seconds since 1970-01-01
        df['DateTime'] = pd.to_datetime(df['DateTime'], unit='s')

        # Define the datetime column as the index
        df.set_index('DateTime', inplace=True)

        return df

    # def create_plots(
    #     self,
    #     df: pd.DataFrame
    # ) -> List[Figure | None]:
    #     figlist = []
    #     fig = go.Figure()

    #     # # Add TEMPBox
    #     # fig.add_trace(
    #     #     go.Scatter(
    #     #         x=df.index,
    #     #         y=df.TEMPbox,
    #     #         name="TEMPBox"))

    #     # # Add TEMPBox
    #     # fig.add_trace(
    #     #     go.Scatter(
    #     #         x=df.index,
    #     #         y=df.vBat,
    #     #         name="vBat",
    #     #         ))

    # #    # Add TEMPBox
    # #     fig.add_trace(
    # #         go.Scatter(
    # #             x=df.index,
    # #             y=df.P_baro,
    # #             name="P_baro"))

    #     fig.update_layout(title="Flight Computer")

    #     figlist.append(fig)


    #     fig = go.Figure()

    #     # Add TEMPBox
    #     fig.add_trace(
    #         go.Scatter(
    #             x=df.index,
    #             y=df.Altitude,
    #             name="TEMPBox"))

    #     fig.update_layout(title="Altitude")

    #     figlist.append(fig)

    #     # Plot these vars over pressure
    #     for var in ['CO2', 'TEMP1', 'TEMP2', 'TEMPsamp', 'RH1', 'RH2']:
    #         fig = go.Figure()

    #         color_scale = px.colors.sequential.Rainbow
    #         normalized_index = (df.index - df.index.min()) / (df.index.max() - df.index.min())
    #         colors = [color_scale[int(x * (len(color_scale)-1))] for x in normalized_index]

    #         # Add CO2
    #         fig.add_trace(
    #             go.Scatter(
    #                 x=df[var],
    #                 y=df.P_baro,
    #                 name=var,
    #                 mode="markers",
    #                 marker=dict(
    #                     color=colors,
    #                     size=2,
    #                     showscale=True
    #                 )))

    #         fig.update_layout(title=var)
    #         figlist.append(fig)

    #     return figlist

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
    na_values=["NA", "-9999.00"],
    comment="#",
    # cols_housekeeping=["TEMPbox", "vBat", "P_baro"],
    cols_export=["P_baro", "CO2", "TEMP1", "TEMP2",
                 "TEMPsamp", "RH1", "RH2", "RHsamp", "mFlow"],
    export_order=100,
    pressure_variable='P_baro')
