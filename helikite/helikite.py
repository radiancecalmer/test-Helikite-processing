#!/usr/bin/env python3

import yaml
import glob
import config
import importlib
import os
from config.flight_computer import FlightComputer


def get_columns_from_dtype(instrument: config.base.InstrumentConfig):
    ''' Gets the column names from the instrument config '''

    return list(instrument.dtype)


# Open YAML
with open(
    os.path.join(
        os.getcwd(), config.constants.INPUT_FOLDER, config.constants.CONFIG_FILE
), 'r') as in_yaml:
    yaml_config = yaml.load(in_yaml, Loader=yaml.Loader)

# Hold a list of the loaded instrument objects
instruments = {}
for instrument, props in yaml_config['instruments'].items():
    instruments[instrument] = getattr(config, props['config'])
    # print(instrument_config)
    # print(instrument, get_columns_from_dtype(getattr(config, props['config'])))
    # print(instrument, props)


for filename in glob.iglob('../data/**'):
    print(f"Determining instrument for {filename}")
    instrument_match_count = 0  # Count how many matches, err if > 0
    # Hold a list of instrument name matches as to not match more than once
    successful_matches = []
    with open(filename) as in_file:
        # Read the first set of lines for headers
        header_lines = [next(in_file) for x in range(50)]
        for name, obj in instruments.items():
            if obj.file_identifier(header_lines):
                # Increment count of matches and also add match to list
                print("Instrument:", name)
                if instrument_match_count > 0:
                    raise ValueError(
                        f"Filename: {filename} matched too many instrument "
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
                yaml_config['instruments'][name]['file'] = filename


print(yaml.dump(yaml_config))

# Update YAML (will remove all commented out inputs)
with open(
    os.path.join(
        os.getcwd(), config.constants.INPUT_FOLDER, config.constants.CONFIG_FILE
), 'w') as in_yaml:
    yaml.dump(yaml_config, in_yaml)
