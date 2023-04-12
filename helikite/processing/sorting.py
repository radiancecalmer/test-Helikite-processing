import pandas as pd
from typing import List, Tuple
from constants import constants
import logging

logger = logging.getLogger(__name__)
logger.setLevel(constants.LOGLEVEL_CONSOLE)


def df_column_sort_key(
        export_df: Tuple[pd.DataFrame, int, List[str], List[str] | None]
    ) -> pd.DataFrame:
    ''' Sort key for ordering of exported dataframes

    Uses value in the second position of the tuple to define sort 'height'
    ie. (df, 100) is sorted higher than (df, 50)

    Parameters
    ----------
    export_df : Tuple[pd.DataFrame, int, List[str], List[str] | None]
        Tuple of dataframe, sort order, col for housekeeping, cols for export

    Returns
    -------
    int
        Sort order

    '''


    if export_df[1] is None:
        # If no order set, push it to the end
        logger.info(
            f"There is no sort key for columns {export_df[0].columns}. "
            "Placing them at the end.")
        return 999999

    return export_df[1]