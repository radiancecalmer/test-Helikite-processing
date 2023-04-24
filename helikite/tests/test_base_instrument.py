import pandas as pd
import pytest
import os
import sys
from io import StringIO
import datetime


def test_read_data(campaign_file_paths_and_instruments):
    for instrument, filepath in campaign_file_paths_and_instruments.values():

        instrument.filename = filepath
        df = instrument.read_data()

        assert isinstance(df, pd.DataFrame), "Data is not a pandas DataFrame"
        assert df.empty == False, "No data found in file"
