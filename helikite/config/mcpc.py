'''
6)  mCPC -> 220202A0.TXT (pressure should be ok to be used)

Particle counter

Time resoslution: 1 sec
Variables to keep: aveconc, concent, rawconc, condtmp, satttmp, pressur, fillcnt, err_num

'''

from .base import InstrumentConfig
from typing import Dict, Any, List

MCPC = InstrumentConfig(
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
        }
)
