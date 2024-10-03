from helikite.classes.cleaning import Cleaner
from helikite.tests.cleaner.mock import MockInstrument
import pandas as pd
import datetime


def test_set_pressure_column():
    instrument1 = MockInstrument(
        name="inst1",
        data={
            "time": pd.date_range("2023-01-01", periods=5, freq="T"),
            "pressure": [100, 101, 102, 103, 104],
        },
        dtype={"time": "datetime64[ns]", "pressure": "float64"},
        cols_export=["time", "pressure"],
        cols_housekeeping=["pressure"],
        pressure_variable="pressure",
    )

    cleaner = Cleaner(
        instruments=[instrument1],
        reference_instrument=instrument1,
        input_folder="dummy_folder",
        flight_date=datetime.date(2023, 1, 1),
    )

    cleaner.set_pressure_column(column_name="pressure")
    assert "pressure" in instrument1.df.columns


def test_set_time_as_index():
    instrument1 = MockInstrument(
        name="inst1",
        data={
            "time": pd.date_range("2023-01-01", periods=5, freq="T"),
            "pressure": [100, 101, 102, 103, 104],
        },
        dtype={"time": "datetime64[ns]", "pressure": "float64"},
        cols_export=["time", "pressure"],
        cols_housekeeping=["pressure"],
        pressure_variable="pressure",
    )
    cleaner = Cleaner(
        instruments=[instrument1],
        reference_instrument=instrument1,
        input_folder="dummy_folder",
        flight_date=datetime.date(2023, 1, 1),
    )

    cleaner.set_time_as_index()
    assert instrument1.df.index.name == "time"


def test_correct_time():
    instrument1 = MockInstrument(
        name="inst1",
        data={
            "time": pd.date_range("2023-01-01", periods=5, freq="T"),
            "pressure": [100, 101, 102, 103, 104],
        },
        dtype={"time": "datetime64[ns]", "pressure": "float64"},
        cols_export=["time", "pressure"],
        cols_housekeeping=["pressure"],
        pressure_variable="pressure",
    )
    cleaner = Cleaner(
        instruments=[instrument1],
        reference_instrument=instrument1,
        input_folder="dummy_folder",
        flight_date=datetime.date(2023, 1, 1),
        time_trim_from=pd.Timestamp("2023-01-01 00:02:00"),
        time_trim_to=pd.Timestamp("2023-01-01 00:04:00"),
    )

    cleaner.set_time_as_index()
    cleaner.correct_time()
    assert (
        len(instrument1.df) == 3
    )  # Only rows from 00:02:00 to 00:04:00 should be left


def test_data_corrections():
    instrument1 = MockInstrument(
        name="inst1",
        data={
            "time": pd.date_range("2023-01-01", periods=5, freq="T"),
            "pressure": [100, 101, 102, 103, 104],
        },
        dtype={"time": "datetime64[ns]", "pressure": "float64"},
        cols_export=["time", "pressure"],
        cols_housekeeping=["pressure"],
        pressure_variable="pressure",
    )
    cleaner = Cleaner(
        instruments=[instrument1],
        reference_instrument=instrument1,
        input_folder="dummy_folder",
        flight_date=datetime.date(2023, 1, 1),
    )

    cleaner.data_corrections()
    assert all(
        instrument1.df["pressure"] == [110, 111, 112, 113, 114]
    )  # Pressure increased by 10
