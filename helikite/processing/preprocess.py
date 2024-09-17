#!/usr/bin/env python3

import yaml
from helikite.constants import constants
from helikite import instruments
import os
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)
logger.setLevel(constants.LOGLEVEL_CONSOLE)


def get_columns_from_dtype(instrument: instruments.base.Instrument):
    """Gets the column names from the instrument config"""

    return list(instrument.dtype)


def read_yaml_config(file_path):
    # Open YAML
    with open(file_path, "r") as in_yaml:
        yaml_config = yaml.load(in_yaml, Loader=yaml.Loader)

    return yaml_config


def preprocess(
    input_folder=constants.INPUTS_FOLDER,
    config_file=constants.CONFIG_FILE,
):
    yaml_config = read_yaml_config(os.path.join(input_folder, config_file))

    # Hold a list of the loaded instrument objects
    instrument_objects = {}
    for instrument, props in yaml_config["instruments"].items():
        instrument_objects[instrument] = getattr(instruments, props["config"])

    for filename in os.listdir(constants.INPUTS_FOLDER):
        # Ignore any yaml or keep files
        if filename.endswith("yaml") or filename.endswith(".keep"):
            continue

        full_path = os.path.join(constants.INPUTS_FOLDER, filename)
        logger.info(f"Determining instrument for {filename:40} ... ")

        # Hold a list of name matches as to not match more than once
        successful_matches = []
        instrument_match_count = 0  # Count how many matches, err if > 0

        with open(full_path) as in_file:
            # Read the first set of lines for headers
            try:
                line_qty_breached = False  # If exception called, flag as true
                header_lines = []
                for x in range(constants.QTY_LINES_TO_IDENTIFY_INSTRUMENT):
                    header_lines.append(next(in_file))
            except (IndexError, StopIteration):
                logger.warning(
                    "Instrument has less than "
                    f"{constants.QTY_LINES_TO_IDENTIFY_INSTRUMENT} lines to "
                    f"scan for headers. Stopping at line {x} and continuing. "
                )
                line_qty_breached = True
            for name, obj in instrument_objects.items():
                try:
                    if obj.file_identifier(header_lines):
                        # Increment count of matches and also add match to list
                        logger.info(f"Instrument: {name}")
                        if instrument_match_count > 0:
                            raise ValueError(
                                f"Filename: {full_path} matched too many "
                                "instrument configurations. Check that there "
                                "are no duplicate files in the input "
                                "directory, or that the file_identifier "
                                "function for the instrument is not too weak "
                                "in matching."
                            )
                        if name in successful_matches:
                            raise ValueError(
                                f"Instrument: {name} matched more than once. "
                                "Check that there are no duplicate files in "
                                "the input directory, or that the "
                                "file_identifier function for the instrument "
                                "is not too weak in matching."
                            )
                        successful_matches.append(name)
                        instrument_match_count += 1
                        props = yaml_config["instruments"][name]

                        # Set filename in config
                        props["file"] = full_path

                        # Get the date if it is in the header
                        props["date"] = obj.date_extractor(header_lines)
                except IndexError:
                    if line_qty_breached is True:
                        logger.warning(
                            "Due to an input file found smaller than the "
                            "configuration defined value of "
                            f"{constants.QTY_LINES_TO_IDENTIFY_INSTRUMENT} "
                            f"lines. The instrument {name} has been skipped "
                            f"when looking in {full_path} as it requires "
                            "more lines to validate its header. If no "
                            "instrument is found in this iteration of the "
                            "instrument search, consider adding the path of "
                            "this instrument's file manually in the "
                            "config.yaml. Another warning message should show "
                            "after checking all files, if this is necessary."
                        )

            if instrument_match_count == 0:
                if line_qty_breached is True:
                    logger.warning(
                        "After searching a short file, no instrument was "
                        "found. Consider adding this instrument file"
                        "in manually"
                    )
                else:
                    logger.warning("No instrument found !!")

    # Write out the updated yaml configuration
    print_preprocess_stats(yaml_config)
    export_yaml_config(
        yaml_config,
        os.path.join(constants.INPUTS_FOLDER, constants.CONFIG_FILE),
    )


def print_preprocess_stats(yaml_config):
    found = []
    not_found = []
    for instrument, props in yaml_config["instruments"].items():
        if props["file"] is None:
            not_found.append(instrument)
        else:
            found.append(instrument)

    logger.info("File preprocessing statistics:")
    logger.info(f"Missing: {len(not_found)}: {', '.join(not_found)}")
    logger.info(f"Found:   {len(found)}: {', '.join(found)}")


def export_yaml_config(yaml_config, out_location=constants.CONFIG_FILE):
    logger.info(f"Writing YAML config to {out_location}")
    # Update YAML (will remove all commented out inputs)
    with open(out_location, "w") as in_yaml:
        yaml.dump(yaml_config, in_yaml)


def generate_config(
    overwrite=False,
    input_folder=constants.INPUTS_FOLDER,
    config_file=constants.CONFIG_FILE,
) -> None:
    """Write out the configuration file

    If overwrite is True, the configuration file in the path argument is
    overwritten

    """
    path = os.path.join(input_folder, config_file)
    if overwrite is False and os.path.exists(path):
        # Escape if overwrite if false and the file exists
        return

    logger.info("Creating config YAML file...\n")

    # Go through each instrument in the __init__ of config.instrument
    instrument_objects = instruments.__dict__.items()
    yaml_config: Dict[str, Any] = {}
    yaml_config["instruments"] = {}
    yaml_config["global"] = {
        "time_trim": {
            "start": None,
            "end": None,
        },
    }
    yaml_config["ground_station"] = {
        "altitude": None,
        "temperature": None,
        "pressure": None,
    }
    yaml_config["plots"] = {
        "altitude_ground_level": False,
        "grid": {"resample_seconds": None},
        "heatmap": {
            "msems_inverted": {
                "zmin": None,
                "zmax": None,
                "zmid": None,
            },
            "msems_scan": {
                "zmin": None,
                "zmax": None,
                "zmid": None,
            },
        },
        "msems_readings_averaged": {
            "Title1": {
                "time_start": None,
                "time_end": None,
                "log_y": False,
            }
        },
    }

    for instrument, obj in instrument_objects:
        # If the imported object is actually an Instrument, then proceed
        if isinstance(obj, instruments.base.Instrument):
            yaml_config["instruments"][instrument] = {
                "config": instrument,
                "file": None,
                "date": None,
                "time_offset": {
                    "hour": 0,
                    "minute": 0,
                    "second": 0,
                },
                "pressure_offset": None,
            }
    export_yaml_config(yaml_config, path)
