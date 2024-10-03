from helikite.classes.cleaning import Cleaner
from helikite.tests.cleaner.mock import MockInstrument
import datetime


def test_cleaner_state(capfd):
    instrument1 = MockInstrument("inst1")
    cleaner = Cleaner(
        instruments=[instrument1],
        reference_instrument=instrument1,
        input_folder="dummy_folder",
        flight_date=datetime.date(2023, 1, 1),
    )

    cleaner.state()
    captured = capfd.readouterr()
    assert "Instrument" in captured.out
    assert "inst1" in captured.out


def test_cleaner_help(capfd):
    instrument1 = MockInstrument("inst1")
    cleaner = Cleaner(
        instruments=[instrument1],
        reference_instrument=instrument1,
        input_folder="dummy_folder",
        flight_date=datetime.date(2023, 1, 1),
    )

    cleaner.help()
    captured = capfd.readouterr()
    assert (
        "There are several methods available to clean the data:"
        in captured.out
    )
