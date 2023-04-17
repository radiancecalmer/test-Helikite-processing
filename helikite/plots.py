import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any
import logging
from constants import constants
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(constants.LOGLEVEL_CONSOLE)


def plot_scatter_from_variable_list_by_index(
    df: pd.DataFrame,
    title: str,
    variables: List[str],
) -> go.Figure:

    fig = go.Figure()
    for var in variables:
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
    df: pd.DataFrame
) -> go.Figure:

    colors = generate_normalised_colours(df)

    fig = make_subplots(rows=2, cols=4, shared_yaxes=False)

    fig.add_trace(go.Scattergl(
        x=df["flight_computer_TEMP1"],
        y=df["flight_computer_Altitude"],
        name="Temperature1 (Flight Computer)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            line_width=2,
            showscale=False,
            symbol="circle-open"
        )),
        row=1, col=1)

    fig.add_trace(go.Scattergl(
        x=df["flight_computer_TEMP2"],
        y=df["flight_computer_Altitude"],
        name="Temperature2 (Flight Computer)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            line_width=2,
            showscale=False,
            symbol="x-open"
        )),
        row=1, col=1)

    fig.add_trace(go.Scattergl(
        x=df["flight_computer_TEMPsamp"],
        y=df["flight_computer_Altitude"],
        name="TemperatureSamp (Flight Computer)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            line_width=2,
            showscale=False,
            symbol="square-x-open"
        )),
        row=1, col=1)

    fig.add_trace(go.Scattergl(
        x=df["smart_tether_T (deg C)"],
        y=df["flight_computer_Altitude"],
        name="Temperature (Smart Tether)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            line_width=2,
            showscale=False,
            symbol="diamond-open"
        )),
        row=1, col=1)

    fig.add_trace(go.Scattergl(
        x=df["flight_computer_RH1"],
        y=df["flight_computer_Altitude"],
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
        y=df["flight_computer_Altitude"],
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

    fig.add_trace(go.Scattergl(
        x=df["smart_tether_%RH"],
        y=df["flight_computer_Altitude"],
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
        y=df["flight_computer_Altitude"],
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
        y=df["flight_computer_Altitude"],
        name="Wind direction (Smart Tether)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            showscale=False
        )),

        row=1, col=4)

    fig.add_trace(go.Scattergl(
        x=df["flight_computer_TEMP1"],
        y=df["flight_computer_Altitude"],
        name="Temperature1 (Flight Computer)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            line_width=2,
            showscale=False,
            symbol="circle-open"
        )),
        row=2, col=1)

    fig.add_trace(go.Scattergl(
        x=df["flight_computer_TEMP2"],
        y=df["flight_computer_Altitude"],
        name="Temperature2 (Flight Computer)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            line_width=2,
            showscale=False,
            symbol="x-open"
        )),
        row=2, col=1)

    fig.add_trace(go.Scattergl(
        x=df["flight_computer_TEMPsamp"],
        y=df["flight_computer_Altitude"],
        name="TemperatureSamp (Flight Computer)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            line_width=2,
            showscale=False,
            symbol="square-x-open"
        )),
        row=2, col=1)

    fig.add_trace(go.Scattergl(
        x=df["smart_tether_T (deg C)"],
        y=df["flight_computer_Altitude"],
        name="Temperature (Smart Tether)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            line_width=2,
            showscale=False,
            symbol="diamond-open"
        )),
        row=2, col=1)

    fig.add_trace(go.Scattergl(
        x=df['pops_PartCon_186'],
        y=df["flight_computer_Altitude"],
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
        y=df["flight_computer_Altitude"],
        name="CO2 (Flight Computer)",
        mode="markers",
        marker=dict(
            color=colors,
            size=constants.PLOT_MARKER_SIZE,
            showscale=False
        )),
        row=2, col=3)

    fig.add_trace(go.Scattergl(
        x=df['stap_sigmab_smth'],
        y=df["flight_computer_Altitude"],
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
        y=df["flight_computer_Altitude"],
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
        y=df["flight_computer_Altitude"],
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
    # Give each plot a border and white background
    for row in [1, 2]:
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
    z = df[[f"msems_inverted_Bin_Conc{x}" for x in range(1, 60)]].dropna()
    y = df[[f"msems_inverted_Bin_Lim{x}" for x in range(1, 60)]].dropna()
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

    z = df[[f"msems_scan_bin{x}" for x in range(1, 60)]].dropna()
    y = df[[f"msems_inverted_Bin_Lim{x}" for x in range(1, 60)]].dropna()
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
    timestamp_end: pd.Timestamp
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


    Returns
    -------
    go.Figure
        Plotly figure
    '''

    # Take sample of dataframe of the given time period
    df = df[timestamp_start:timestamp_end]

    # Get number of bins
    df['msems_inverted_NumBins'].mean()
    bins = df.groupby('msems_inverted_NumBins').all().index.to_list()
    if len(bins) > 60:
        raise ValueError("Unable to determine exact number of bins. "
                         "There are various quantities for each row")
    else:
        bins = bins[0]

    x = df[[f"msems_inverted_Bin_Lim{x}" for x in range(1, bins)]].mean(
        numeric_only=True)
    y = df[[f"msems_inverted_Bin_Conc{x}" for x in range(1, bins)]].mean(
        numeric_only=True)

    fig = go.Figure(data=go.Scatter(
            x=x.to_numpy().flatten(),
            y=y.to_numpy().flatten()))
    fig.update_layout(**constants.PLOT_LAYOUT_COMMON,
                      title=f"{title}: ({timestamp_start} to {timestamp_end})")
    fig.update_layout(height=600)
    fig.update_xaxes(title_text="Bin size")
    fig.update_yaxes(title_text="Particle concentration")

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
) -> go.Figure:

    colors = generate_normalised_colours(df)

    fig = go.Figure()
    fig.add_trace(
        go.Scattergl(
            x=df.index,
            y=df["flight_computer_Altitude"],
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
