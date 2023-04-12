'''
6)  mCPC -> 220202A0.TXT (pressure should be ok to be used)

Particle counter

Time resoslution: 1 sec
Variables to keep: aveconc, concent, rawconc, condtmp, satttmp, pressur, fillcnt, err_num

'''

from .base import Instrument
from typing import Dict, Any, List
import pandas as pd


class MCPC(Instrument):
    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.name = 'mcpc'

    def file_identifier(
        self,
        first_lines_of_csv
    ) -> bool:
        if "#MCPC-UAV" in first_lines_of_csv[0]:
            return True

    def data_corrections(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        df['DateTime'] = pd.to_datetime(df['#YY/MM/DD'] + ' ' + df['HR:MN:SC'],
                                        format='%y/%m/%d %H:%M:%S')
        df.drop(columns=["#YY/MM/DD", "HR:MN:SC"], inplace=True)

        return df

mcpc = MCPC(
    header=13,
    delimiter="\t",
    dtype={
        '#YY/MM/DD': 'str',
        'HR:MN:SC': 'str',
        'aveconc': "Int64",
        'concent': "Int64",
        'rawconc': "Int64",
        'cnt_sec': "Int64",
        'condtmp': "Float64",
        'satttmp': "Float64",
        'satbtmp': "Float64",
        'optctmp': "Float64",
        'inlttmp': "Float64",
        'smpflow': "Int64",
        'satflow': "Int64",
        'pressur': "Int64",
        'condpwr': "Int64",
        'sattpwr': "Int64",
        'satbpwr': "Int64",
        'optcpwr': "Int64",
        'satfpwr': "Int64",
        'exhfpwr': "Int64",
        'fillcnt': "Int64",
        'err_num': "Int64",
        'mcpcpmp': "Int64",
        'mcpcpwr': "Int64",
        },
    export_order=200)
