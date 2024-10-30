import sys
import os
import pytest

# Append the root directory of your project to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helikite.processing.conversions import pressure_to_altitude  # noqa


def test_pressure_to_altitude():
    """Test the conversion of pressure to altitude"""

    pressure_at_start = 977
    temperate_at_start = 6
    altitude_at_start = 500

    assert pressure_to_altitude(
        pressure=977,
        pressure_at_start=pressure_at_start,
        temperature_at_start=temperate_at_start,
        altitude_at_start=altitude_at_start,
    ) == pytest.approx(500, 0.1)

    # Add a test with realistic values
