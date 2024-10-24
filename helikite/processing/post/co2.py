import numpy as np

# # CO2 monitor correction


def stp_convert_dry(x, t, p1):
    """Converts a scalar measurement to STP conditions

    Function: `stp.convert.dry` from Roman Pohorsky

    Pressure in hPa
    Temperature in °C

    Usage example:
    CO2_dry=stp_convert_dry(df_level0['FC_CO2'],df_level0['T ref'],df_level0['FC_P corr'])
    """

    p = p1 * 100
    t = t + 273.15
    v_stp = (273.15 / t) * (p / 101315)
    x_stp = x / v_stp
    return x_stp


def stp_convert_moist(x, t, p1, rh):
    """Converts a scalar measurement to STP conditions with humidity

    Pressure in hPa
    Temperature in °C
    """

    p = p1 * 100
    t = t + 273.15
    if t > 273.15:
        e_s = (
            np.exp(34.494 - (4924.9 / ((t - 273.15) + 237.1)))
            / ((t - 273.15) + 105) ** 1.57
        )
    else:
        e_s = (
            np.exp(43.494 - (6545.8 / ((t - 273.15) + 278)))
            / ((t - 273.15) + 868) ** 2
        )
    e = (rh * e_s) / 100
    t_v = t / (1 - (e / p) * (1 - 0.622))
    v_stp = (273.15 / t_v) * (p / 1013.15)
    x_stp = x / v_stp
    return x_stp


def stp_moist_test(x, t, p1, rh):
    """Converts a vector measurement to STP conditions with humidity"""
    p = p1 * 100  # in Pa
    t = t + 273.15  # in K

    for i in range(len(t)):
        if t.iloc[i] > 273.15:
            e_s = (
                np.exp(34.494 - (4924.9 / ((t.iloc[i] - 273.15) + 237.1)))
                / ((t.iloc[i] - 273.15) + 105) ** 1.57
            )
        else:
            e_s = (
                np.exp(43.494 - (6545.8 / ((t.iloc[i] - 273.15) + 278)))
                / ((t.iloc[i] - 273.15) + 868) ** 2
            )

        e = (rh * e_s) / 100
        t_v = t / (1 - (e / p) * (1 - 0.622))
        v_stp = (273.15 / t_v) * (p / 101315)
        x_stp = x / v_stp
    return x_stp
