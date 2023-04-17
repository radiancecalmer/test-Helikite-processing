import pytest
import os
import sys
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from instruments.flight_computer import flight_computer
from instruments.smart_tether import SmartTether, smart_tether


@pytest.fixture
def campaign_data_location():

    return os.path.join(
        os.path.dirname(__file__), "resources", "campaigns", "20220929")

@pytest.fixture
def fc_data(campaign_data_location: str):
    # Import flight computer data from the campaign data folder

    flight_computer.filename = os.path.join(campaign_data_location,
                                            "LOG_20220929.txt")
    df = flight_computer.read_data()

    return df


@pytest.fixture
def st_data():
    # Set date that would usually happen in the config file/preprocess step
    smart_tether.date = datetime.datetime.strptime("9/29/2022", "%m/%d/%Y")
    smart_tether.filename = "./tests/resources/smart_tether_during_midnight.csv"

    df = smart_tether.read_data()

    return df