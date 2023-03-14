'''

1) Flight computer -> LOG_20220929.txt (has pressure)

Data from the onboard microcontroller. Resolution: 1 sec
DateTime in seconds since 1970-01-01 (to be verified)

Variables to keep: DateTime, P_baro, CO2, TEMP1, TEMP2, TEMPsamp, RH1, RH2, RHsamp, mFlow
Houskeeping variables: TEMPbox, vBat

'''

from .base import InstrumentConfig
from typing import Dict, Any, List
import plotly.graph_objects as go
from plotly.graph_objects import Figure
import pandas as pd


def file_identifier(first_lines_of_csv):
    if first_lines_of_csv[0] == "SBI,DateTime,PartCon,CO2,P_baro,TEMPbox,mFlow,TEMPsamp,RHsamp,TEMP1,RH1,TEMP2,RH2,vBat\n":
        return True

def apply_dataframe_corrections(
    df: pd.DataFrame
) -> pd.DataFrame:

    df['DateTime'] = pd.to_datetime(df['DateTime'], unit='s')

    return df


def create_plots(
    df: pd.DataFrame
) -> Figure:
    fig = go.Figure()

    # Add TEMPBox
    fig.add_trace(
        go.Scatter(
            x=df.DateTime,
            y=df.TEMPbox,
            name="TEMPBox"))

    # Add TEMPBox
    fig.add_trace(
        go.Scatter(
            x=df.DateTime,
            y=df.vBat,
            name="vBat"))

    fig.update_layout(title="Flight Computer")

    return fig

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
    file_identifier=file_identifier,
    create_plots=create_plots,
    dataframe_corrections=apply_dataframe_corrections)
