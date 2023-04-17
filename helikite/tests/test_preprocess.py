import pandas as pd
import pytest
import os
import sys
from io import StringIO
import datetime

# Append the root directory of your project to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from instruments import (
    smart_tether, flight_computer, msems_inverted, msems_readings, msems_scan,
    pops, stap, mcpc
)


def test_detect_file(campaign_data_location: str):
    ''' Test that the correct file type is detected '''

    for filename in os.listdir(campaign_data_location):
        full_path = os.path.join(campaign_data_location, filename)

        with open(full_path) as in_file:
            # Read the first set of lines for headers
            header_lines = [next(in_file) for x in range(50)]


        if filename == 'LOG_20220929.txt':
            assert flight_computer.file_identifier(header_lines) is True
        if filename == 'mSEMS_103_220929_101343_INVERTED.txt':
            assert msems_inverted.file_identifier(header_lines) is True
        if filename == 'mSEMS_103_220929_101343_READINGS.txt':
            assert msems_readings.file_identifier(header_lines) is True
        if filename == 'mSEMS_103_220929_101343_SCAN.txt':
            assert msems_scan.file_identifier(header_lines) is True
        if filename == 'LOG_20220929_A.csv':
            assert smart_tether.file_identifier(header_lines) is True
        if filename == 'HK_20220929x001.csv':
            assert pops.file_identifier(header_lines) is True
        if filename == 'STAP_220929A0_processed.txt':
            assert stap.file_identifier(header_lines) is True


def test_detect_file_collisions(campaign_data_location: str):
        ''' Test that only one instrument is identified '''
        for filename in os.listdir(campaign_data_location):
            full_path = os.path.join(campaign_data_location, filename)

        with open(full_path) as in_file:
            # Read the first set of lines for headers
            header_lines = [next(in_file) for x in range(50)]

        for instrument in [flight_computer, msems_inverted, msems_readings,
                           msems_scan, smart_tether, pops, stap]:
            instrument_detected = []
            if instrument.file_identifier(header_lines) is True:
                instrument_detected.append(instrument.name)

                assert len(instrument_detected) == 1, (
                    f"{len(instrument_detected)} instrument(s) identified the "
                    f"file {filename}"
                )