from pydantic import BaseSettings
from pathlib import Path
from typing import List
import logging

class Constants(BaseSettings):
    INPUTS_FOLDER: Path = Path.cwd().joinpath("inputs")
    OUTPUTS_FOLDER: Path = Path.cwd().joinpath("outputs")
    OUTPUTS_INSTRUMENT_SUBFOLDER: str = 'instruments'
    CONFIG_FILE: str = "config.yaml"
    HTML_OUTPUT_FILENAME: str = "housekeeping-check.html"
    MASTER_CSV_FILENAME: str = "helikite-data.csv"
    HOUSEKEEPING_CSV_FILENAME: str = "helikite-housekeeping.csv"
    HOUSEKEEPING_VAR_PRESSURE: str = "housekeeping_pressure"
    LOGFILE_NAME: str = "helikite.log"
    LOGLEVEL_CONSOLE: str = "INFO"
    LOGLEVEL_FILE: str = "DEBUG"

    LOGFORMAT_CONSOLE: logging.Formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-7.7s] %(message)s"
    )
    LOGFORMAT_FILE = logging.Formatter(
        "%(asctime)s [%(levelname)-7.7s] (%(name)25.25s) %(message)s"
    )
constants = Constants()
