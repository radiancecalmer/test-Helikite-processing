import plotly.graph_objects as go
from ipywidgets import Output, VBox
import pandas as pd


def choose_outliers(df, x, y):
    """Creates a plot to interactively select outliers in the data

    A plot is generated, where two variables are plotted, and the user can
    click on points to select them as outliers. The selected points are
    stored in a list, which can be accessed later.

    Args:
        df (pandas.DataFrame): The dataframe containing the data
        x (str): The column name of the x-axis variable
        y (str): The column name of the y-axis variable

    """
    # Create a figure widget for interactive plotting
    fig = go.FigureWidget()
    out = Output()
    out.append_stdout("Click on a point to set as outlier.\n")
    df = df.copy()

    # Index must be a datetime object for the plot to work
    if not isinstance(df.index, pd.DatetimeIndex):
        potential_columns = []
        for col in df.columns:
            try:
                if "time" in col.lower() or "date" in col.lower():
                    potential_columns.append(col)
            except ValueError:
                continue
        raise ValueError(
            "Index must be a DatetimeIndex for interactive plot to work. "
            "Use command `df.index = pd.to_datetime(df.index)` to convert "
            "index to datetime. It may be necessary to set the index to a "
            "datetime column in the dataframe first. Potential columns to use "
            "as index:\n"
            f"\n\t{"\n\t".join(potential_columns)}"
        )
    selected_points = []

    @out.capture(clear_output=True)
    def select_point_callback(trace, points, selector):
        # Callback function for click events to select points
        if points.point_inds:
            point_index = points.point_inds[0]
            print(f"Point index: {point_index}")
            print("Trace", trace)
            selected_x = trace.x[point_index]
            selected_y = trace.y[point_index]

            # Get the index of the selected point from the dataframe
            selected_index = df[(df[x] == selected_x) & (df[y] == selected_y)]
            print(f"Selected DF index: {selected_index}")

            selected_points.append((selected_x, selected_y))
            print(f"Selected point: {selected_x}")
            print("Points selected: ", selected_points)

    fig.add_trace(
        go.Scattergl(
            x=df[x],
            y=df[y],
            name=y,
            # line=dict(width=2, color="red"),
            opacity=1,
            mode="markers",
            # hoverinfo="skip",
        )
    )

    for trace in fig.data:
        # Attach the callback to the traces
        trace.on_click(select_point_callback)

    variable_list = []
    df = df.fillna("")
    for variable in df.columns:
        if variable == y or variable == x:
            print("Skipping variable: ", variable)
            continue

        variable_list.append(
            dict(
                args=[{"x": [df[variable]]}],
                label=variable,
                method="restyle",
            )
        )

    limited_variable_list = variable_list
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=limited_variable_list,
                direction="down",
                pad={"r": 5, "t": 5},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top",
            ),
        ]
    )

    fig.update_layout(
        annotations=[
            dict(
                text="Variable:",
                showarrow=False,
                x=0,
                y=1.085,
                yref="paper",
                align="left",
            )
        ]
    )

    # Customize plot layout
    fig.update_layout(
        title=f"{y} vs {x}",
        xaxis_title=x,
        yaxis_title=y,
        hovermode="closest",
        showlegend=True,
        height=600,
        width=800,
    )

    # Show plot with interactive click functionality
    return VBox([fig, out])  # Use VBox to stack the plot and output
