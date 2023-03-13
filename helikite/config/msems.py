'''
4) mSEMS -> 	mSEMS_103_220929_101343_INVERTED.txt (data to be plotted) (has pressure)
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


def file_identifier(first_lines_of_csv):
	# To match a "...READINGS.txt" file
    if (
		"#mSEMS" in first_lines_of_csv[0]
		and "#YY/MM/DD" in first_lines_of_csv[31]
	):
        return True

# To match a "...READINGS.txt" file
MSEMS = InstrumentConfig(
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
    file_identifier=file_identifier)

