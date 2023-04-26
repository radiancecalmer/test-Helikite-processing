from pydantic import BaseSettings
from pathlib import Path
import logging


class Constants(BaseSettings):
    INPUTS_FOLDER: Path = Path.cwd().joinpath("inputs")
    OUTPUTS_FOLDER: Path = Path.cwd().joinpath("outputs")
    OUTPUTS_INSTRUMENT_SUBFOLDER: str = 'instruments'
    CONFIG_FILE: str = "config.yaml"
    MASTER_CSV_FILENAME: str = "helikite-data.csv"
    HOUSEKEEPING_CSV_FILENAME: str = "helikite-housekeeping.csv"
    HOUSEKEEPING_VAR_PRESSURE: str = "housekeeping_pressure"
    LOGFILE_NAME: str = "helikite.log"
    LOGLEVEL_CONSOLE: str = "INFO"
    LOGLEVEL_FILE: str = "DEBUG"

    # Column names
    ALTITUDE_GROUND_LEVEL_COL: str = "flight_computer_Altitude_agl"
    ALTITUDE_SEA_LEVEL_COL: str = "flight_computer_Altitude"

    # Plots
    QUICKLOOK_PLOT_FILENAME: str = "helikite-quicklooks.html"
    QUALITYCHECK_PLOT_FILENAME: str = "helikite-qualitycheck.html"
    PLOT_LAYOUT_COMMON: dict = {
        'font': {
            'size': 16,
            'family': 'Arial',
            },
        'template': 'plotly_white',
        'height': 600
    }
    PLOT_MARKER_SIZE: int = 8

    # Logging
    LOGFORMAT_CONSOLE: logging.Formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-7.7s] %(message)s"
    )
    LOGFORMAT_FILE = logging.Formatter(
        "%(asctime)s [%(levelname)-7.7s] (%(name)25.25s) %(message)s"
    )


constants = Constants()
