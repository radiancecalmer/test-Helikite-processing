from helikite.classes.cleaning import Cleaner
from helikite.tests.cleaner.mock import MockInstrument
import pandas as pd
import datetime


def test_merge_instruments():
    instrument1 = MockInstrument(
        "inst1",
        data={
            "time": pd.date_range("2023-01-01", periods=3, freq="T"),
            "pressure": [100, 101, 102],
        },
    )
    instrument2 = MockInstrument(
        "inst2",
        data={
            "time": pd.date_range("2023-01-01", periods=3, freq="T"),
            "pressure": [200, 201, 202],
        },
    )

    cleaner = Cleaner(
        instruments=[instrument1, instrument2],
        reference_instrument=instrument1,
        input_folder="dummy_folder",
        flight_date=datetime.date(2023, 1, 1),
    )

    cleaner.set_time_as_index()
    cleaner.merge_instruments()
    assert len(cleaner.master_df) == 3
    assert "inst1_pressure" in cleaner.master_df.columns
    assert "inst2_pressure" in cleaner.master_df.columns
