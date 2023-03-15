'''
7) Pico -> Pico100217_220204_152813Eng.txt / Pico100217_220219_123139Eng.txt (doesn't have pressure)

Gas monitor measuring CO, N2O and H2O

Can operate in two different modes. When it opeartes in differentioal mode, there an additional variable called Differential.CO and should be used for the CO reading.
In manual mode, look at CO_ppm (however, in this case, the baseline need to be substracted but this might require some more conversation on how to do it.)

For quality check -> plot the following variables: win1Fit7 and win1Fit8 (if win1Fit8 has a sudden jump (very noticeable) this indicates a bad fit)
'''

from .base import InstrumentConfig
from typing import Dict, Any, List

def file_identifier(first_lines_of_csv):
    ## win0Fit0,win0Fit1,win0Fit2,win0Fit3,win0Fit4,win0Fit5,win0Fit6,win0Fit7,win0Fit8,win0Fit9,win1Fit0,win1Fit1,win1Fit2 always there
    if first_lines_of_csv[0] == "Time Stamp,Inlet Number,P (mbars),T0 (degC),T5 (degC),Tgas(degC),Laser PID Readout,Det PID Readout,win0Fit0,win0Fit1,win0Fit2,win0Fit3,win0Fit4,win0Fit5,win0Fit6,win0Fit7,win0Fit8,win0Fit9,win1Fit0,win1Fit1,win1Fit2,win1Fit3,win1Fit4,win1Fit5,win1Fit6,win1Fit7,win1Fit8,win1Fit9,Det Bkgd,Ramp Ampl,N2O (ppm),H2O (ppm),CO (ppm),Battery Charge (V),Power Input (mV),Current (mA),SOC (%),Battery T (degC),FET T (degC)\n":
        return True

Pico = InstrumentConfig(
    dtype={
        "Time Stamp": "str",
        "Inlet Number": "Int64",
        "P (mbars)": "Float64",
        "T0 (degC)": "Float64",
        "T5 (degC)": "Float64",
        "Tgas(degC)": "Float64",
        "Laser PID Readout": "Int64",
        "Det PID Readout": "Int64",
        "win0Fit0": "Float64",
        "win0Fit1": "Float64",
        "win0Fit2": "Float64",
        "win0Fit3": "Float64",
        "win0Fit4": "Float64",
        "win0Fit5": "Float64",
        "win0Fit6": "Float64",
        "win0Fit7": "Float64",
        "win0Fit8": "Float64",
        "win0Fit9": "Float64",
        "win1Fit0": "Float64",
        "win1Fit1": "Float64",
        "win1Fit2": "Float64",
        "win1Fit3": "Float64",
        "win1Fit4": "Float64",
        "win1Fit5": "Float64",
        "win1Fit6": "Float64",
        "win1Fit7": "Float64",
        "win1Fit8": "Float64",
        "win1Fit9": "Float64",
        "Det Bkgd": "Float64",
        "Ramp Ampl": "Float64",
        "N2O (ppm)": "Float64",
        "H2O (ppm)": "Float64",
        "CO (ppm)": "Float64",
        "Battery Charge (V)": "Int64",
        "Power Input (mV)": "Int64",
        "Current (mA)": "Int64",
        "SOC (%)": "Int64",
        "Battery T (degC)": "Float64",
        "FET T (degC)": "Float64",
        },
    file_identifier=file_identifier)

