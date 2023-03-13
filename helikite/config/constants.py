from pydantic import BaseSettings
from pathlib import Path

class Constants(BaseSettings):
    INPUT_FOLDER: Path = Path.cwd().joinpath("input")
    OUTPUT_FOLDER: Path = Path.cwd().joinpath("output")
    CONFIG_FILE: Path = Path.cwd().joinpath("input").joinpath("config.yaml")


constants = Constants()
