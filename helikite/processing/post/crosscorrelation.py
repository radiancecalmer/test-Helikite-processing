import pandas as pd
import numpy as np


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

    # Add columns to the reference, so we know which to delete later
    # df_reference.columns = [f"{col}_ref" for col in df_reference.columns]
    df_instrument = df_instrument.copy()

    df_reference = df_reference.copy()
    # Match timestamp resolution of the reference data
    df_instrument.index = df_instrument.index.astype(df_reference.index.dtype)

    # Merge the two dataframes
    df = pd.merge_asof(
        df_reference,
        df_instrument,
        left_index=True,
        right_index=True,
        suffixes=("", "_ref"),
    )

    df_syn = df.shift(periods=index, axis=0)
    columns_to_drop = [col for col in df.columns if "_ref" in col]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)

    return df_syn


# correct the other instrument pressure with the reference pressure
def matchpress(dfpressure, refpresFC, takeofftimeFL, walktime):
    try:
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


def presdetrend(dfpressure, takeofftimeFL, landingtimeFL):
    """detrend instrument pressure measurements"""
    print("take off location", dfpressure.loc[takeofftimeFL])
    print("landing location", dfpressure.loc[landingtimeFL])
    print("length of dfpressure", len(dfpressure))

    # Check for NA values and handle them
    start_pressure = dfpressure.loc[takeofftimeFL]
    end_pressure = dfpressure.loc[landingtimeFL]

    # TODO: How to handle NA. Should there even be NA in the pressure data?
    if pd.isna(start_pressure) or pd.isna(end_pressure):
        print(
            "Warning: NA values found in pressure data at takeoff or landing time."
        )
        # Use the first and last non-NA values as fallback
        start_pressure = dfpressure.dropna().iloc[0]
        end_pressure = dfpressure.dropna().iloc[-1]

    linearfit = np.linspace(
        start_pressure,
        end_pressure,
        len(dfpressure),
    )

    dfdetrend = dfpressure - linearfit + start_pressure

    return dfdetrend
