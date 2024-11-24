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

    # Attach the callback to all traces
    for trace in fig.data:
        # Only allow the reference instrument to be clickable
        # if trace.name == self.reference_instrument.name:
        trace.on_click(select_point_callback)
        print(f"Callback attached to trace: {trace.name}")

    variable_list = []
    df = df.fillna("")
    for variable in df.columns:
        if (
            variable == y
            or variable == x
            or not pd.api.types.is_numeric_dtype(df[variable])
            or not df[variable].dtype in (int, float)
            or df[variable].isnull().all()  # Has no values
        ):
            continue
        # Replace null values with None to make them JSON compatible
        # df[variable] = df[variable].where(pd.notnull(df[variable]), None)

        # print("Variable: ", variable, df[variable].dtype)
        variable_list.append(
            dict(
                args=[{x: df[x], y: df[variable]}],
                label=variable,
                method="update",
            )
        )
    limited_variable_list = variable_list[0:11]
    [
        print("Variable: ", variable["label"])
        for variable in limited_variable_list
    ]
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=limited_variable_list,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top",
            ),
        ]
    )

    # fig.update_layout(
    #     updatemenus=[
    #         dict(
    #             buttons=list(
    #                 [
    #                     dict(
    #                         args=["type", "surface"],
    #                         label="3D Surface",
    #                         method="restyle",
    #                     ),
    #                     dict(
    #                         args=["type", "heatmap"],
    #                         label="Heatmap",
    #                         method="restyle",
    #                     ),
    #                 ]
    #             ),
    #             direction="down",
    #             pad={"r": 10, "t": 10},
    #             showactive=True,
    #             x=0.1,
    #             xanchor="left",
    #             y=1.1,
    #             yanchor="top",
    #         ),
    #     ]
    # )
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
