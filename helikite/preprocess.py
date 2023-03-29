#!/usr/bin/env python3

import yaml
import glob
import config
import importlib
import os
from typing import Any, Dict

def get_columns_from_dtype(instrument: config.instrument.base.Instrument):
    ''' Gets the column names from the instrument config '''

    return list(instrument.dtype)

def read_yaml_config(file_path):
    # Open YAML
    with open(file_path, 'r') as in_yaml:
        yaml_config = yaml.load(in_yaml, Loader=yaml.Loader)

    return yaml_config

def preprocess():
    yaml_config = read_yaml_config(
        os.path.join(config.constants.INPUTS_FOLDER,
                     config.constants.CONFIG_FILE)
    )

    # Hold a list of the loaded instrument objects
    instruments = {}
    for instrument, props in yaml_config['instruments'].items():
        instruments[instrument] = getattr(config.instrument, props['config'])


    for filename in os.listdir(config.constants.INPUTS_FOLDER):
        # Ignore any yaml or keep files
        if filename.endswith('yaml') or filename.endswith('.keep'):
            continue

        full_path = os.path.join(config.constants.INPUTS_FOLDER, filename)
        print(f"Determining instrument for {filename:40} ... ", end='')

        # Hold a list of name matches as to not match more than once for safeguard
        successful_matches = []
        instrument_match_count = 0  # Count how many matches, err if > 0

        with open(full_path) as in_file:
            # Read the first set of lines for headers
            header_lines = [next(in_file) for x in range(50)]
            for name, obj in instruments.items():
                if obj.file_identifier(header_lines):
                    # Increment count of matches and also add match to list
                    print("Instrument:", name)
                    if instrument_match_count > 0:
                        raise ValueError(
                            f"Filename: {full_path} matched too many instrument "
                            "configurations. Check that there are no duplicate "
                            "files in the input directory, or that the "
                            "file_identifier function for the instrument is not "
                            "too weak in matching."
                        )
                    if name in successful_matches:
                        raise ValueError(
                            f"Instrument: {name} matched more than once. Check "
                            "that there are no duplicate files in the input "
                            "directory, or that the file_identifier function for "
                            "the instrument is not too weak in matching."
                        )
                    successful_matches.append(name)
                    instrument_match_count += 1
                    props = yaml_config['instruments'][name]

                    # Set filename in config
                    props['file'] = full_path

                    # Get the date if it is in the header
                    props['date'] = obj.date_extractor(header_lines)

            if instrument_match_count == 0:
                print("!! Not found !!")

    # Write out the updated yaml configuration
    print_preprocess_stats(yaml_config)
    export_yaml_config(yaml_config,
                       os.path.join(config.constants.INPUTS_FOLDER,
                                    config.constants.CONFIG_FILE))

def print_preprocess_stats(yaml_config):
    found = []
    not_found = []
    for instrument, props in yaml_config['instruments'].items():
        if props['file'] is None:
            not_found.append(instrument)
        else:
            found.append(instrument)

    print()
    print("File preprocessing statistics:")
    print(f"Missing: {len(not_found)}: {', '.join(not_found)}")
    print(f"Found:   {len(found)}: {', '.join(found)}")
    print()

def export_yaml_config(yaml_config, out_location=config.constants.CONFIG_FILE):
    print(f"Writing YAML config to {out_location}")
    # Update YAML (will remove all commented out inputs)
    with open(out_location, 'w') as in_yaml:
        yaml.dump(yaml_config, in_yaml)


def generate_config(
    overwrite=False,
    path=os.path.join(
        config.constants.INPUTS_FOLDER,
        config.constants.CONFIG_FILE)
) -> None:
    ''' Write out the configuration file

    If overwrite is True, the configuration file in the path argument is
    overwritten

    '''

    if overwrite is False and os.path.exists(path):
        # Escape if overwrite if false and the file exists
        return

    print("Creating config YAML file...\n")

    # Go through each instrument in the __init__ of config.instrument
    instruments = config.instrument.__dict__.items()
    yaml_config: Dict[str, Any] = {}
    yaml_config['instruments'] = {}
    yaml_config['global'] = {
        'time_trim': {
            'start': None,
            'end': None,
        }
    }

    for instrument, obj in instruments:
        # If the imported object is actually an Instrument, then proceed
        if isinstance(obj, config.instrument.base.Instrument):
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
