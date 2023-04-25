import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any, Tuple
import logging
from constants import constants
import numpy as np
from processing.helpers import reduce_column_to_single_unique_value


logger = logging.getLogger(__name__)
logger.setLevel(constants.LOGLEVEL_CONSOLE)


def plot_scatter_from_variable_list_by_index(
    df: pd.DataFrame,
    title: str,
    variables: List[str],
) -> go.Figure:

    fig = go.Figure()
    for var in variables:
        if var is not None:
            fig.add_trace(
                go.Scattergl(
                    x=df.index,
                    y=df[var],
                    name=var,
                    mode='markers',
                    marker=dict(
                        size=constants.PLOT_MARKER_SIZE,
                    ))
            )
    fig.update_yaxes(mirror=True, showline=True, linecolor='black', linewidth=2)
    fig.update_xaxes(mirror=True, showline=True, linecolor='black', linewidth=2)
    fig.update_layout(**constants.PLOT_LAYOUT_COMMON,
                      title=title,
                      showlegend=True)

    return fig


def generate_grid_plot(
    df: pd.DataFrame,
    all_instruments: List[str],
    altitude_col: str = "flight_computer_Altitude",
) -> go.Figure:

    colors = generate_normalised_colours(df)

    fig = make_subplots(rows=3, cols=4, shared_yaxes=False)

    # Add the same temperature plots to all three rows
    for row_id in range(1, 4):

        fig.add_trace(go.Scattergl(
            x=df["flight_computer_TEMP1"],
            y=df[altitude_col],
            name="Temperature1 (Flight Computer)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                line_width=2,
                showscale=False,
                symbol="circle-open"
            )),
            row=row_id, col=1)

        fig.add_trace(go.Scattergl(
            x=df["flight_computer_TEMP2"],
            y=df[altitude_col],
            name="Temperature2 (Flight Computer)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                line_width=2,
                showscale=False,
                symbol="x-open"
            )),
            row=row_id, col=1)

        fig.add_trace(go.Scattergl(
            x=df["flight_computer_TEMPsamp"],
            y=df[altitude_col],
            name="TemperatureSamp (Flight Computer)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                line_width=2,
                showscale=False,
                symbol="square-x-open"
            )),
            row=row_id, col=1)

        if "smart_tether" in all_instruments:
            fig.add_trace(go.Scattergl(
                x=df["smart_tether_T (deg C)"],
                y=df[altitude_col],
                name="Temperature (Smart Tether)",
                mode="markers",
                marker=dict(
                    color=colors,
                    size=constants.PLOT_MARKER_SIZE,
                    line_width=2,
                    showscale=False,
                    symbol="diamond-open"
                )),
                row=row_id, col=1)

    fig.add_trace(go.Scattergl(
        x=df["flight_computer_RH1"],
        y=df[altitude_col],
        name="Relative Humidity1 (Flight Computer)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            line_width=2,
            showscale=False,
            symbol="circle-open"
        )),
        row=1, col=2)

    fig.add_trace(go.Scattergl(
        x=df["flight_computer_RH2"],
        y=df[altitude_col],
        name="Relative Humidity2 (Flight Computer)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            line_width=2,
            showscale=False,
            symbol="x-open"
        )),
        row=1, col=2)

    if "pops" in all_instruments:
        fig.add_trace(go.Scattergl(
            x=df['pops_PartCon_186'],
            y=df[altitude_col],
            name="PartCon_186 (POPS)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                showscale=False
            )),
            row=2, col=2)

    fig.add_trace(go.Scattergl(
        x=df['flight_computer_CO2'],
        y=df[altitude_col],
        name="CO2 (Flight Computer)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            showscale=False
        )),
        row=2, col=3)

    # Add smart tether data if it exists
    if "smart_tether" in all_instruments:
        fig.add_trace(go.Scattergl(
            x=df["smart_tether_%RH"],
            y=df[altitude_col],
            name="Relative Humidity (Smart Tether)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                line_width=2,
                showscale=False,
                symbol="diamond-open"
            )),
            row=1, col=2)

        fig.add_trace(go.Scattergl(
            x=df["smart_tether_Wind (m/s)"],
            y=df[altitude_col],
            name="Wind speed (Smart Tether)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                showscale=False
            )),
            row=1, col=3)

        fig.add_trace(go.Scattergl(
            x=df["smart_tether_Wind (degrees)"],
            y=df[altitude_col],
            name="Wind direction (Smart Tether)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                showscale=False
            )),
            row=1, col=4)


    # Add STAP data if it exists
    if "stap" in all_instruments:
        fig.add_trace(go.Scattergl(
            x=df['stap_sigmab_smth'],
            y=df[altitude_col],
            name="sigmab_smth (STAP)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                line_width=2,
                showscale=False,
                symbol="circle-open"
            )),
            row=2, col=4)

        fig.add_trace(go.Scattergl(
            x=df['stap_sigmag_smth'],
            y=df[altitude_col],
            name="sigmag_smth (STAP)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                line_width=2,
                showscale=False,
                symbol="x-open"
            )),
            row=2, col=4)

        fig.add_trace(go.Scattergl(
            x=df['stap_sigmar_smth'],
            y=df[altitude_col],
            name="sigmar_smth (STAP)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                line_width=2,
                showscale=False,
                symbol="diamond-open"
            )),
            row=2, col=4)

    if "pico" in all_instruments:
        fig.add_trace(go.Scattergl(
            x=df['pico_CO (ppm)'],
            y=df[altitude_col],
            name="CO (Pico)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                showscale=False
            )),
            row=3, col=2)

        fig.add_trace(go.Scattergl(
            x=df['pico_N2O (ppm)'],
            y=df[altitude_col],
            name="N2O (Pico)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                showscale=False
            )),
            row=3, col=3)

    if "ozone" in all_instruments:
        fig.add_trace(go.Scattergl(
            x=df['ozone_ozone'],
            y=df[altitude_col],
            name="Ozone (Ozone)",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                showscale=False
            )),
            row=3, col=4)

    # Give each plot a border and white background
    for row in [1, 2, 3]:
        for col in [1, 2, 3, 4]:
            fig.update_yaxes(
                row=row, col=col,
                mirror=True, showline=True, linecolor='black', linewidth=2)
            fig.update_xaxes(
                row=row, col=col,
                mirror=True, showline=True, linecolor='black', linewidth=2)

    fig.update_yaxes(title_text="Altitude (m)", row=1, col=1)
    fig.update_xaxes(title_text="Temperature (°C)", row=1, col=1)
    fig.update_xaxes(title_text="Relative Humidity (%)", row=1, col=2)
    fig.update_xaxes(title_text="Wind Speed (m/s)", row=1, col=3)
    fig.update_xaxes(title_text="Wind Direction (degrees)", row=1, col=4)
    fig.update_xaxes(title_text="Temperature (°C)", row=2, col=1)
    fig.update_xaxes(title_text="Particle Concentration 186", row=2, col=2)
    fig.update_xaxes(title_text="CO2", row=2, col=3)
    fig.update_xaxes(title_text="STAP", row=2, col=4)
    fig.update_xaxes(title_text="Temperature (°C)", row=3, col=1)
    fig.update_xaxes(title_text="CO", row=3, col=2)
    fig.update_xaxes(title_text="N2O", row=3, col=3)
    fig.update_xaxes(title_text="Ozone", row=3, col=4)

    layout = constants.PLOT_LAYOUT_COMMON
    layout['height'] = 1000

    fig.update_layout(**layout,
                      coloraxis=dict(colorbar=dict(orientation='h', y=-0.15)),
                      )

    return fig


def generate_particle_heatmap(
    df: pd.DataFrame,
    props_msems_inverted: Dict[str, Any],
    props_msems_scan: Dict[str, Any],
) -> go.Figure:

    figlist = []

    # Get number of bins
    bins = reduce_column_to_single_unique_value(df, 'msems_inverted_NumBins')

    z = df[[f"msems_inverted_Bin_Conc{x}" for x in range(1, bins)]].dropna()
    y = df[[f"msems_inverted_Bin_Lim{x}" for x in range(1, bins)]].dropna()
    x = df[['msems_inverted_StartTime']].dropna()
    fig = go.Figure(
        data=go.Heatmap(
        z=z.T,
        x=x.index.values,
        y=y.mean(), colorscale = 'Viridis',
        **props_msems_inverted
        ))
    fig.update_yaxes(type='log',
                    range=(np.log10(y.mean()[0]), np.log10(y.mean()[-1])),
                    tickformat="f",
                    nticks=4
                    )
    fig.update_layout(**constants.PLOT_LAYOUT_COMMON,
                      title=f"Bin concentrations (msems_inverted)")

    fig.update_yaxes(title_text="D<sub>p</sub> [nm]")
    fig.update_xaxes(title_text="Time")
    fig.update_layout(height=600)

    figlist.append(fig)

    z = df[[f"msems_scan_bin{x}" for x in range(1, bins)]].dropna()
    y = df[[f"msems_inverted_Bin_Lim{x}" for x in range(1, bins)]].dropna()
    x = df[['msems_inverted_StartTime']].dropna()

    fig = go.Figure(
        data=go.Heatmap(
        z=z.T,
        x=x.index.values,
        y=y.mean(), colorscale = 'Viridis',
        **props_msems_scan
        ))
    fig.update_yaxes(type='log',
                    range=(np.log10(y.mean()[0]), np.log10(y.mean()[-1])),
                    tickformat="f",
                    nticks=4
                    )
    fig.update_layout(**constants.PLOT_LAYOUT_COMMON,
                      title=f"Bin readings (msems_scan)")

    fig.update_yaxes(title_text="D<sub>p</sub> [nm]")
    fig.update_xaxes(title_text="Time")
    fig.update_layout(height=600)

    figlist.append(fig)

    return figlist

def generate_average_bin_concentration_plot(
    df: pd.DataFrame,
    title: str,
    timestamp_start: pd.Timestamp,
    timestamp_end: pd.Timestamp,
    bin_limit_col_prefix: str = 'msems_inverted_Bin_Lim',
    bin_concentration_col_prefix: str = 'msems_inverted_Bin_Conc',
    bin_quantity_col: str = 'msems_inverted_NumBins',
    y_logscale: bool = False,
) -> go.Figure:
    ''' With a given timestamp, generate an average of MSEM bin concentrations

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing the data
    title : str
        Title of plot
    timestamp_start : str
        Start timestamp of period to average
    timestamp_end : str
        End timestamp of period to average
    bin_limit_col_prefix : str, optional
        Prefix of column containing bin limits, default 'msems_inverted_Bin_Lim'
    bin_concentration_col_prefix : str, optional
        Prefix of column containing bin concentrations,
        default 'msems_inverted_Bin_Conc'
    bin_quantity_col : str, optional
        Column containing number of bins, default 'msems_inverted_NumBins'
    y_logscale : bool, optional
        Whether to use a log scale for the y axis, default False


    Returns
    -------
    go.Figure
        Plotly figure
    '''

    # Take sample of dataframe of the given time period
    df = df[timestamp_start:timestamp_end]

    # Get number of bins
    bins = reduce_column_to_single_unique_value(df, bin_quantity_col)

    x = df[[f"{bin_limit_col_prefix}{x}" for x in range(1, bins)]]
    y = df[[f"{bin_concentration_col_prefix}{x}" for x in range(1, bins)]]

    fig = go.Figure()

    num_records = min(len(x), len(y))
    logger.info(f"Generating mean MSEMS plot for {title} with {num_records} "
                "records")
    for i in range(0, num_records):
        recordx = x.iloc[i]
        recordy = y.iloc[i]
        fig.add_trace(go.Scattergl(
            x=recordx.to_numpy().flatten(),
            y=recordy.to_numpy().flatten(),
            name=str(recordx.name),
            line={
                "color": "rgba(143, 82, 244 ,0.2)",
                "width": 2.5
            },
        )
        )

    # Plot the mean
    fig.add_trace(go.Scattergl(
        x=x.mean(numeric_only=True).to_numpy().flatten(),
        y=y.mean(numeric_only=True).to_numpy().flatten(),
        line={
            "width": 5,
            "color": "rgba(255, 0, 0, 1)"
        },
        name="Mean"
    ))

    fig.update_layout(title=f"{title}: ({num_records} records; "
                            f"{timestamp_start} to {timestamp_end})")
    fig.update_layout(height=600)
    fig.update_xaxes(title_text="Bin size",
                     type='log',
                     range=(np.log10(x.mean()[0]), np.log10(x.mean()[-1])),
                     tickformat="f",
                     nticks=4
    )
    fig.update_yaxes(title_text="Particle concentration")

    if y_logscale:
        fig.update_yaxes(type='log')


    return fig


def write_plots_to_html(
    figures: List[go.Figure],
    filename: str
) -> None:

    # Remove all None items in figures list. These are None because an
    # instrument may not have a figure to create, None is default
    figures = [i for i in figures if i is not None]

    logger.info(f"Writing {len(figures)} figures to {filename}")
    # Write out all of the figures to HTML
    with open(filename, 'w') as f:
        # Write figures. They'll be sorted by the order they were added
        for fig in figures:
            f.write(fig.to_html(full_html=False, include_plotlyjs=True))

def generate_altitude_plot(
    df: pd.DataFrame,
    altitude_col: str = "flight_computer_Altitude",
) -> go.Figure:

    colors = generate_normalised_colours(df)

    fig = go.Figure()
    fig.add_trace(
        go.Scattergl(
            x=df.index,
            y=df[altitude_col],
            name="smart_tether_Wind",
            mode="markers",
            marker=dict(
                color=colors,
                size=constants.PLOT_MARKER_SIZE,
                showscale=False),
        )
    )

    # Update background to white and add black border
    fig.update_layout(
        **constants.PLOT_LAYOUT_COMMON,
        title="Altitude",
        xaxis=dict(
            title="Time",
            mirror=True,
            showline=True,
            linecolor='black',
            linewidth=2
        ),
        yaxis=(dict(
            title="Altitude (m)",
            mirror=True,
            showline=True,
            linecolor='black',
            linewidth=2
        )),
    )

    return fig

def generate_altitude_concentration_plot(
    df: pd.DataFrame,
    bins: List[Tuple[str, str, str]],
    height: int = 400,
    altitude_col: str = "flight_computer_Altitude",
) -> go.Figure:

    colors = generate_normalised_colours(df)

    fig = generate_altitude_plot(df, altitude_col)

    # Set line markers to single solid colour
    fig.update_traces(marker=dict(color='rgb(31, 119, 180)'))

    for title, time_start, time_end in bins:
        # Ignore any that don't have a start or end time
        if time_start is None or time_end is None:
            continue

        fig.add_vrect(
            x0=time_start, x1=time_end,
            annotation_text=title, annotation_position="top left",
            fillcolor="green", opacity=0.25, line_width=0
        )

    fig.update_layout(height=height)

    return fig


def generate_normalised_colours(
    df: pd.DataFrame,
    convert_nan_to: int = 0
) -> List[str]:
    ''' Generate a list of colours for a plot based on index of dataframe '''

    color_scale = px.colors.sequential.Rainbow
    normalized_index = (
        (df.index - df.index.min())
        / (df.index.max() - df.index.min())
    )

    # If there are NaN values in the index, convert them to the given value
    normalized_index = normalized_index.fillna(convert_nan_to)
    colors = [color_scale[int(x * (len(color_scale)-1))]
              for x in normalized_index]


    return colors
