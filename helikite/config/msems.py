'''
4) mSEMS ->     mSEMS_103_220929_101343_INVERTED.txt (data to be plotted) (has pressure)
        mSEMS_103_220929_101343_READINGS.txt (high resolution raw data with houskeeping info, error messages) (has pressure)
        mSEMS_103_220929_101343_SCANS.txt (raw scan data with some houskeeping varaibles)

The mSEMS measures particles size distribution for particles from 8 nanometers to roughly 300 nm. The number of bins can vary. Typically we use 60 log-spaced bins but
it can change. The time resolution depends on the amount of bins and the scan time but it is typically between 1 and 2 minutes. I mormally do not merge this data
with the rest because of the courser time resolution and the amount of variables.

The file provides some information on temperature, pressure etc. It then gives the center diamater of each bin (i.e. Bin_Dia1, Bin_Dia2, ...) and then the numbe rof particles
per bin (i.e. Bin_Conc1, Bin_Conc2, ...).

-> because of the coarser time resolution, data is easier to be displayed as a timeseries (with the addition of total particle concentration and altitude).

Houskeeping file: Look at READINGS (look at msems_err / cpc_err)

'''

from .base import InstrumentConfig
from typing import Dict, Any, List
import pandas as pd


def file_identifier_inverted(first_lines_of_csv):
    # To match "...INVERTED.txt" file
    if "#Date\tTime\tTemp(C)\tPress(hPa)\tNumBins\tBin_Dia1\tBin_Dia2\tBin_Dia3" in first_lines_of_csv[0]:
        return True


def file_identifier_readings(first_lines_of_csv):
    # To match a "...READINGS.txt" file
    if ("#mSEMS" in first_lines_of_csv[0]
        and "#YY/MM/DD" in first_lines_of_csv[31]
    ):
        return True

def apply_dataframe_corrections_readings(
    df: pd.DataFrame
) -> pd.DataFrame:

    df['DateTime'] = pd.to_datetime(df['#YY/MM/DD'] + ' ' + df['HR:MN:SC'],
                                    format='%y/%m/%d %H:%M:%S')
    df.drop(columns=["#YY/MM/DD", "HR:MN:SC"], inplace=True)

    return df


# To match a "...READINGS.txt" file
MSEMSReadings = InstrumentConfig(
    header=31,
    delimiter="\t",
    dtype={
        "#YY/MM/DD": "str",
        "HR:MN:SC": "str",
        "msems_mode": "Int64",
        "mono_dia": "Int64",
        "sheath_sp": "Float64",
        "sheath_rh": "Int64",
        "sheath_temp": "Float64",
        "pressure": "Int64",
        "lfe_temp": "Float64",
        "sheath_flow": "Float64",
        "sheath_pwr": "Int64",
        "impct_prs": "Float64",
        "hv_volts": "Float64",
        "hv_dac": "Int64",
        "sd_install": "Int64",
        "ext_volts": "Float64",
        "msems_errs": "Float64",
        "mcpc_hrtb": "Float64",
        "mcpc_smpf": "Float64",
        "mcpc_satf": "Float64",
        "mcpc_cndt": "Float64",
        "mcpc_satt": "Float64",
        "mcpcpwr": "Int64",
        "mcpcpmp": "Int64",
        "sd_save": "Int64",
        "mcpc_errs": "Int64",
        "mcpc_a_conc": "Float64",
        "mcpc_a_cnt": "Int64",
    },
    file_identifier=file_identifier_readings,
    data_corrections=apply_dataframe_corrections_readings)

# To match a "...READINGS.txt" file
MSEMSInverted = InstrumentConfig(
    # header=31,
    delimiter="\t",
    dtype={
        "#Date": "str",
        "Time": "str",
        "Temp(C)": "Float64",
        "Press(hPa)": "Float64",
        "NumBins": "Int64",
        "Bin_Dia1": "Float64",
        "Bin_Dia2": "Float64",
        "Bin_Dia3": "Float64",
        "Bin_Dia4": "Float64",
        "Bin_Dia5": "Float64",
        "Bin_Dia6": "Float64",
        "Bin_Dia7": "Float64",
        "Bin_Dia8": "Float64",
        "Bin_Dia9": "Float64",
        "Bin_Dia10": "Float64",
        "Bin_Dia11": "Float64",
        "Bin_Dia12": "Float64",
        "Bin_Dia13": "Float64",
        "Bin_Dia14": "Float64",
        "Bin_Dia15": "Float64",
        "Bin_Dia16": "Float64",
        "Bin_Dia17": "Float64",
        "Bin_Dia18": "Float64",
        "Bin_Dia19": "Float64",
        "Bin_Dia20": "Float64",
        "Bin_Dia21": "Float64",
        "Bin_Dia22": "Float64",
        "Bin_Dia23": "Float64",
        "Bin_Dia24": "Float64",
        "Bin_Dia25": "Float64",
        "Bin_Dia26": "Float64",
        "Bin_Dia27": "Float64",
        "Bin_Dia28": "Float64",
        "Bin_Dia29": "Float64",
        "Bin_Dia30": "Float64",
        "Bin_Dia31": "Float64",
        "Bin_Dia32": "Float64",
        "Bin_Dia33": "Float64",
        "Bin_Dia34": "Float64",
        "Bin_Dia35": "Float64",
        "Bin_Dia36": "Float64",
        "Bin_Dia37": "Float64",
        "Bin_Dia38": "Float64",
        "Bin_Dia39": "Float64",
        "Bin_Dia40": "Float64",
        "Bin_Dia41": "Float64",
        "Bin_Dia42": "Float64",
        "Bin_Dia43": "Float64",
        "Bin_Dia44": "Float64",
        "Bin_Dia45": "Float64",
        "Bin_Dia46": "Float64",
        "Bin_Dia47": "Float64",
        "Bin_Dia48": "Float64",
        "Bin_Dia49": "Float64",
        "Bin_Dia50": "Float64",
        "Bin_Dia51": "Float64",
        "Bin_Dia52": "Float64",
        "Bin_Dia53": "Float64",
        "Bin_Dia54": "Float64",
        "Bin_Dia55": "Float64",
        "Bin_Dia56": "Float64",
        "Bin_Dia57": "Float64",
        "Bin_Dia58": "Float64",
        "Bin_Dia59": "Float64",
        "Bin_Dia60": "Float64",
        "Bin_Conc1": "Float64",
        "Bin_Conc2": "Float64",
        "Bin_Conc3": "Float64",
        "Bin_Conc4": "Float64",
        "Bin_Conc5": "Float64",
        "Bin_Conc6": "Float64",
        "Bin_Conc7": "Float64",
        "Bin_Conc8": "Float64",
        "Bin_Conc9": "Float64",
        "Bin_Conc10": "Float64",
        "Bin_Conc11": "Float64",
        "Bin_Conc12": "Float64",
        "Bin_Conc13": "Float64",
        "Bin_Conc14": "Float64",
        "Bin_Conc15": "Float64",
        "Bin_Conc16": "Float64",
        "Bin_Conc17": "Float64",
        "Bin_Conc18": "Float64",
        "Bin_Conc19": "Float64",
        "Bin_Conc20": "Float64",
        "Bin_Conc21": "Float64",
        "Bin_Conc22": "Float64",
        "Bin_Conc23": "Float64",
        "Bin_Conc24": "Float64",
        "Bin_Conc25": "Float64",
        "Bin_Conc26": "Float64",
        "Bin_Conc27": "Float64",
        "Bin_Conc28": "Float64",
        "Bin_Conc29": "Float64",
        "Bin_Conc30": "Float64",
        "Bin_Conc31": "Float64",
        "Bin_Conc32": "Float64",
        "Bin_Conc33": "Float64",
        "Bin_Conc34": "Float64",
        "Bin_Conc35": "Float64",
        "Bin_Conc36": "Float64",
        "Bin_Conc37": "Float64",
        "Bin_Conc38": "Float64",
        "Bin_Conc39": "Float64",
        "Bin_Conc40": "Float64",
        "Bin_Conc41": "Float64",
        "Bin_Conc42": "Float64",
        "Bin_Conc43": "Float64",
        "Bin_Conc44": "Float64",
        "Bin_Conc45": "Float64",
        "Bin_Conc46": "Float64",
        "Bin_Conc47": "Float64",
        "Bin_Conc48": "Float64",
        "Bin_Conc49": "Float64",
        "Bin_Conc50": "Float64",
        "Bin_Conc51": "Float64",
        "Bin_Conc52": "Float64",
        "Bin_Conc53": "Float64",
        "Bin_Conc54": "Float64",
        "Bin_Conc55": "Float64",
        "Bin_Conc56": "Float64",
        "Bin_Conc57": "Float64",
        "Bin_Conc58": "Float64",
        "Bin_Conc59": "Float64",
        "Bin_Conc60": "Float64",
    },
    file_identifier=file_identifier_inverted,)
    # data_corrections=apply_dataframe_corrections)
