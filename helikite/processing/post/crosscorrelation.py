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
                if not x in cols:
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


def df_findtimelag(df, range_list, instname=""):
    filter_inst = [col for col in df if col.startswith(instname)]
    df_inst = df[filter_inst].iloc[0]

    df_inst = df_inst.set_axis(range_list, copy=False)

    return df_inst


def df_lagshift(df_instrument, df_reference, index, instname=""):
    """
    Create a df that merges the df with the df_struncresampn using merge_asof
    to match the timestamps of the two dataframes, and then shift the df by the
    index value to create the synthetic data
    """
    print(f"Shifting {instname} by {index} index")

    # Match timestamp resolution of the reference data
    df_instrument.index = df_instrument.index.astype(df_reference.index.dtype)
    df = pd.merge_asof(
        df_reference,
        df_instrument,
        left_index=True,
        right_index=True,
    )

    df_syn = df.shift(periods=index, axis=0)
    df_syn = df_syn.set_index(df_reference.index)

    return df_syn


# correct the other instrument pressure with the reference pressure
def matchpress(dfpressure, refpresFC, takeofftimeFL, walktime):
    try:
        # if df.empty:
        #     # df_n=df.copy()
        #     # diffpress = 0
        #     pass
        # else:
        # df_n=df.copy()
        diffpress = (
            dfpressure.loc[takeofftimeFL - walktime : takeofftimeFL].mean()
            - refpresFC
        )
        dfprescorr = dfpressure.sub(np.float64(diffpress))  # .iloc[0]
    # catch when df1 is None
    except AttributeError:
        pass
    # catch when it hasn't even been defined
    except NameError:
        pass
    return dfprescorr


# # detrend mSEMS and STAP pressure measurements
def presdetrend(dfpressure, takeofftimeFL, landingtimeFL, preschange):
    linearfit = np.linspace(
        dfpressure.loc[takeofftimeFL],
        dfpressure.loc[landingtimeFL],
        len(dfpressure),
    )  # landingtimeFL -preschange
    # linearfit=np.linspace(dfpressure.loc[takeofftimeFL],dfpressure.dropna().iloc[-1]-preschange,len(dfpressure))#landingtimeFL
    dfdetrend = dfpressure - linearfit + dfpressure.loc[takeofftimeFL]
    return dfdetrend
