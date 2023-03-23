'''
3) POPS ->  HK_20220929x001.csv (has pressure)

The POPS is an optical particle counter. It provides information on the particle number concentration (how many particles per cubic centimeter)
and the size distribution for particles larger than 180 nm roughly. Resolution: 1 sec

Important variables to keep:
DateTime, P, POPS_Flow, b0 -> b15

PartCon needs to be re-calculated by adding b3 to b15 and deviding by averaged POPS_Flow
(b0 -> b15 can be converted to dN/dlogDp values with conversion factors I have)

Housekeeping variables to look at:
POPS_flow -> flow should be just below 3, and check for variability increase
'''

from .base import Instrument
from typing import Dict, Any, List
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure


class POPS(Instrument):
    def file_identifier(
        self,
        first_lines_of_csv
    ) -> bool:
        if first_lines_of_csv[0] == "DateTime, Status, PartCt, PartCon, BL, BLTH, STD, P, TofP, POPS_Flow, PumpFB, LDTemp, LaserFB, LD_Mon, Temp, BatV, Laser_Current, Flow_Set,PumpLife_hrs, BL_Start, TH_Mult, nbins, logmin, logmax, Skip_Save, MinPeakPts,MaxPeakPts, RawPts,b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15\n":
            return True

    def data_corrections(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        df['DateTime'] = pd.to_datetime(df['DateTime'], unit='s')
        # df.drop(columns=["date", "time"], inplace=True)

        df.columns = df.columns.str.strip()

        return df

    def create_plots(
        self,
        df: pd.DataFrame
    ) -> Figure:
        fig = go.Figure()

        for var in ["POPS_Flow"]:
            fig.add_trace(
            go.Scatter(
                x=df.DateTime,
                y=df[var],
                name=var))

        fig.update_layout(title="POPS")

        return fig

pops = POPS(
    dtype={
        "DateTime": "Float64",
        "Status": "Int64",
        "PartCt": "Int64",
        "PartCon": "Float64",
        "BL": "Int64",
        "BLTH": "Int64",
        "STD": "Float64",
        "P": "Float64",
        "TofP": "Float64",
        "POPS_Flow": "Float64",
        "PumpFB": "Int64",
        "LDTemp": "Float64",
        "LaserFB": "Int64",
        "LD_Mon": "Int64",
        "Temp": "Float64",
        "BatV": "Float64",
        "Laser_Current": "Float64",
        "Flow_Set": "Float64",
        "PumpLife_hrs": "Float64",
        "BL_Start": "Int64",
        "TH_Mult": "Int64",
        "nbins": "Int64",
        "logmin": "Float64",
        "logmax": "Float64",
        "Skip_Save": "Int64",
        "MinPeakPts": "Int64",
        "MaxPeakPts": "Int64",
        "RawPts": "Int64",
        "b0": "Int64",
        "b1": "Int64",
        "b2": "Int64",
        "b3": "Int64",
        "b4": "Int64",
        "b5": "Int64",
        "b6": "Int64",
        "b7": "Int64",
        "b8": "Int64",
        "b9": "Int64",
        "b10": "Int64",
        "b11": "Int64",
        "b12": "Int64",
        "b13": "Int64",
        "b14": "Int64",
        "b15": "Int64",
        })

