#!/usr/bin/env python3

import yaml
import glob
from constants import constants
import instruments
import importlib
import os
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)
logger.setLevel(constants.LOGLEVEL_CONSOLE)


def get_columns_from_dtype(instrument: instruments.base.Instrument):
    ''' Gets the column names from the instrument config '''

    return list(instrument.dtype)

def read_yaml_config(file_path):
    # Open YAML
    with open(file_path, 'r') as in_yaml:
        yaml_config = yaml.load(in_yaml, Loader=yaml.Loader)

    return yaml_config

def preprocess():
    yaml_config = read_yaml_config(
        os.path.join(constants.INPUTS_FOLDER,
                     constants.CONFIG_FILE)
    )

    # Hold a list of the loaded instrument objects
    instrument_objects = {}
    for instrument, props in yaml_config['instruments'].items():
        instrument_objects[instrument] = getattr(instruments, props['config'])


    for filename in os.listdir(constants.INPUTS_FOLDER):
        # Ignore any yaml or keep files
        if filename.endswith('yaml') or filename.endswith('.keep'):
            continue

        full_path = os.path.join(constants.INPUTS_FOLDER, filename)
        logger.info(f"Determining instrument for {filename:40} ... ")

        # Hold a list of name matches as to not match more than once for safeguard
        successful_matches = []
        instrument_match_count = 0  # Count how many matches, err if > 0

        with open(full_path) as in_file:
            # Read the first set of lines for headers
            header_lines = [next(in_file) for x in range(50)]
            for name, obj in instrument_objects.items():
                if obj.file_identifier(header_lines):
                    # Increment count of matches and also add match to list
                    logger.info(f"Instrument: {name}")
                    if instrument_match_count > 0:
                        raise ValueError(
                            f"Filename: {full_path} matched too many "
                            "instrument configurations. Check that there are "
                            "no duplicate files in the input directory, or "
                            "that the file_identifier function for the "
                            "instrument is not too weak in matching."
                        )
                    if name in successful_matches:
                        raise ValueError(
                            f"Instrument: {name} matched more than once. "
                            "Check that there are no duplicate files in the "
                            "input directory, or that the file_identifier "
                            "function for the instrument is not too weak in "
                            "matching."
                        )
                    successful_matches.append(name)
                    instrument_match_count += 1
                    props = yaml_config['instruments'][name]

                    # Set filename in config
                    props['file'] = full_path

                    # Get the date if it is in the header
                    props['date'] = obj.date_extractor(header_lines)

            if instrument_match_count == 0:
                logger.warning("No instrument found !!")

    # Write out the updated yaml configuration
    print_preprocess_stats(yaml_config)
    export_yaml_config(yaml_config,
                       os.path.join(constants.INPUTS_FOLDER,
                                    constants.CONFIG_FILE))

def print_preprocess_stats(yaml_config):
    found = []
    not_found = []
    for instrument, props in yaml_config['instruments'].items():
        if props['file'] is None:
            not_found.append(instrument)
        else:
            found.append(instrument)

    logger.info("File preprocessing statistics:")
    logger.info(f"Missing: {len(not_found)}: {', '.join(not_found)}")
    logger.info(f"Found:   {len(found)}: {', '.join(found)}")

def export_yaml_config(yaml_config, out_location=constants.CONFIG_FILE):
    logger.info(f"Writing YAML config to {out_location}")
    # Update YAML (will remove all commented out inputs)
    with open(out_location, 'w') as in_yaml:
        yaml.dump(yaml_config, in_yaml)


def generate_config(
    overwrite=False,
    path=os.path.join(
        constants.INPUTS_FOLDER,
        constants.CONFIG_FILE)
) -> None:
    ''' Write out the configuration file

    If overwrite is True, the configuration file in the path argument is
    overwritten

    '''

    if overwrite is False and os.path.exists(path):
        # Escape if overwrite if false and the file exists
        return

    logger.info("Creating config YAML file...\n")

    # Go through each instrument in the __init__ of config.instrument
    instrument_objects = instruments.__dict__.items()
    yaml_config: Dict[str, Any] = {}
    yaml_config['instruments'] = {}
    yaml_config['global'] = {
        'time_trim': {
            'start': None,
            'end': None,
        },
    }
    yaml_config['ground_station'] = {
        'altitude': None,
        'temperature': None,
        'pressure': None
    }
    yaml_config['plots'] = {
        'heatmap': {
            'msems_inverted': {
                'zmin': None,
                'zmax': None,
                'zmid': None,
            },
            'msems_scan': {
                'zmin': None,
                'zmax': None,
                'zmid': None,
            },
        },
        'msems_readings_averaged': {
            'Title1': {
                'time_start': None,
                'time_end': None,
                'log_y': False,
        }}
    }

    for instrument, obj in instrument_objects:
        # If the imported object is actually an Instrument, then proceed
        if isinstance(obj, instruments.base.Instrument):
            yaml_config['instruments'][instrument] = {
                'config': instrument,
                'file': None,
                'date': None,
                'time_offset': {
                    'hour': 0,
                    'minute': 0,
                    'second': 0,
                },
                'pressure_offset': None
            }
    export_yaml_config(yaml_config, path)
