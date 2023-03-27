from pydantic import BaseSettings
from pathlib import Path
from typing import List

class Constants(BaseSettings):
    INPUTS_FOLDER: Path = Path.cwd().joinpath("inputs")
    OUTPUTS_FOLDER: Path = Path.cwd().joinpath("outputs")
    CONFIG_FILE: str = "config.yaml"
    HTML_OUTPUT_FILENAME: str = "housekeeping-check.html"
    MASTER_CSV_FILENAME: str = "helikite-master.csv"
    HOUSEKEEPING_CSV_FILENAME: str = "housekeeping.csv"

constants = Constants()
