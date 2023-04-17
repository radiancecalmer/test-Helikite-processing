import pandas as pd
import pytest
import os
import sys
from io import StringIO
import datetime

# Append the root directory of your project to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plots import generate_normalised_colours


def test_nan_for_colourmap(fc_data: pd.DataFrame):
    ''' Test that NaN values do not break the colourmap generator '''

    pd.set_option('mode.chained_assignment', None)  # Disable copy slice warning

    # Convert the TEMP2 column to float
    fc_data['TEMP2'] = fc_data['TEMP2'].astype(float)

    # Add some nan values to the TEMP2 column
    fc_data['TEMP2'][0] = float('nan')
    fc_data['TEMP2'][1] = float('nan')

    # Assert there are nan values in the TEMP2 column
    assert fc_data['TEMP2'].isnull().values.any() == True, (
        "There are no NaN values to test with")

    # Execute function to ensure it does not raise ValueError
    generate_normalised_colours(fc_data)
