from helikite.instruments import flight_computer_v2
import pandas as pd


def test_read_csv(campaign_file_paths_and_instruments_2024: str):
    """Test the reading of a CSV file"""

    # Test the reading of a CSV file
    df = flight_computer_v2.read_data()

    assert df is not None, "The DataFrame is None"
    assert (
        len(df) == 758 - 15 - 1
    ), "The number of rows in the DataFrame is not correct. "
    "(Total lines of CSV) - (occurrences of errors) - (header line)"


def test_set_time(campaign_file_paths_and_instruments_2024: str):
    """Test the setting of the time"""

    # Test the setting of the time
    df = flight_computer_v2.read_data()
    df = flight_computer_v2.set_time_as_index(df)

    assert df is not None, "The DataFrame is None"
    assert df.index.name == "DateTime", "The index name is not correct"

    # Assert first value 240926-141333 is 2024-09-26 14:13:33
    assert df.index[0] == pd.Timestamp(
        "2024-09-26 14:13:33"
    ), "The first value is not correct"

    # Assert last value 240926-163903 is 2024-09-26 16:39:03
    assert df.index[-1] == pd.Timestamp(
        "2024-09-26 16:39:03"
    ), "The last value is not correct"
