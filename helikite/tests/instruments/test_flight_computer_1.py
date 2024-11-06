from helikite.instruments import flight_computer_v2

def test_read_csv(campaign_file_paths_and_instruments_2024: str):
    """Test the reading of a CSV file"""

    # Test the reading of a CSV file
    flight_computer_v2.read_data()