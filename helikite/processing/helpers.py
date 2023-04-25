import pandas as pd
from typing import Any


def reduce_column_to_single_unique_value(
    df: pd.DataFrame,
    col: str
) -> Any:
    """Reduce a column to a single value, if possible.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to reduce.
    col : str
        Column to reduce.

    Returns
    -------
    Any
        Single value if possible, else the original column.

    Raises
    ------
    ValueError
        If the column cannot be reduced to a single value.
    """

    # Get number of bins
    values = df.groupby(col).all().index.to_list()
    if len(values) == 1:
        return values[0]
    else:
        raise ValueError(f"Unable to reduce column '{col}' to a single value. "
                         f"All values: {values}")