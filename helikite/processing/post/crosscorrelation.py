import pandas as pd


def crosscorr(datax, datay, lag=10):
    """Lag-N cross correlation.
    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length

    Returns
    ----------
    crosscorr : float
    """

    return datax.corr(datay.shift(lag))


def df_derived_by_shift(df_init, lag=0, NON_DER=[]):
    df = df_init.copy()
    if not lag:
        return df
    cols = {}
    for i in range(1, 2 * lag + 1):
        for x in list(df.columns):
            if x not in NON_DER:
                if x not in cols:
                    cols[x] = ["{}_{}".format(x, i)]
                else:
                    cols[x].append("{}_{}".format(x, i))
    for k, v in cols.items():
        columns = v
        dfn = pd.DataFrame(data=None, columns=columns, index=df.index)
        i = -lag
        for c in columns:
            dfn[c] = df[k].shift(periods=i)
            i += 1
        df = pd.concat([df, dfn], axis=1)  # , join_axes=[df.index])
    return df


def df_findtimelag(df, range, instname=""):
    filter_inst = [col for col in df if col.startswith(instname)]
    df_inst = df[filter_inst].iloc[0]
    # print(len(df_inst),len(range),df_inst.loc[df_inst.idxmax(axis=0)])
    df_inst = df_inst.set_axis(range, copy=False)
    max_inst = max(df_inst)
    lag_inst = df_inst.loc[df_inst.idxmax(axis=0)]
    # print(lag_inst)
    return df_inst  # ,max_inst,lag_inst
