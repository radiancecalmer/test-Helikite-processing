import pandas as pd
import pytest
import os
import sys
from io import StringIO
import datetime

# Append the root directory of your project to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from instruments.smart_tether import SmartTether, smart_tether


@pytest.fixture
def test_data():
    # Set date that would usually happen in the config file/preprocess step
    smart_tether.date = datetime.datetime.strptime("9/29/2022", "%m/%d/%Y")
    smart_tether.filename = "./tests/resources/smart_tether_during_midnight.csv"

    df = smart_tether.read_data()

    return df

def test_set_time_as_index(test_data):
    # call the function under test
    df = smart_tether.set_time_as_index(test_data)

    # check that the datetime column is set as the index
    assert df.index.name == "DateTime"

    # check that the date after midnight is set correctly
    assert df.iloc[0].name == pd.to_datetime("2022-09-29 23:59:58")
    assert df.iloc[1].name == pd.to_datetime("2022-09-29 23:59:59")
    assert df.iloc[2].name == pd.to_datetime("2022-09-30 00:00:01")
    assert df.iloc[3].name == pd.to_datetime("2022-09-30 00:00:02")