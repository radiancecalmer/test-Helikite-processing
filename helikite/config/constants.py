from pydantic import BaseSettings
from pathlib import Path

class Constants(BaseSettings):
    INPUTS_FOLDER: Path = Path.cwd().joinpath("inputs")
    OUTPUTS_FOLDER: Path = Path.cwd().joinpath("outputs")
    CONFIG_FILE: str = "config.yaml"
    HTML_OUTPUT_FILENAME: str = "helikite.html"

constants = Constants()
