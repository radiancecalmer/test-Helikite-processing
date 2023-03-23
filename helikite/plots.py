import plotly.graph_objects as go
import pandas as pd
from typing import List


def plot_scatter_from_variable_list_by_index(
    df: pd.DataFrame,
    title: str,
    variables: List[str],
) -> go.Figure:

    fig = go.Figure()
    for var in variables:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[var],
                name=var))
    fig.update_layout(title="Pressure variables")

    return fig
