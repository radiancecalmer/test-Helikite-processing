import pandas as pd
import numpy
from helikite.plots import generate_normalised_colours


def test_nan_for_colourmap(fc_data: pd.DataFrame):
    """Test that NaN values do not break the colourmap generator"""

    # Convert the TEMP2 column to float
    fc_data.loc[:, "TEMP2"] = fc_data["TEMP2"].astype(float)

    # Add some nan values to the TEMP2 column
    fc_data.loc[0, "TEMP2"] = float("nan")
    fc_data.loc[1, "TEMP2"] = float("nan")

    # Assert there are nan values in the TEMP2 column
    assert fc_data["TEMP2"].isnull().values.any() is numpy.bool_(
        True
    ), "There are no NaN values to test with"

    # Execute function to ensure it does not raise ValueError
    generate_normalised_colours(fc_data)
