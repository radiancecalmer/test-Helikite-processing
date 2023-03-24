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
    fig.update_layout(title=title)

    return fig

def write_plots_to_html(
    figures: List[go.Figure],
    filename: str
) -> None:

    # Remove all None items in figures list. These are None because an
    # instrument may not have a figure to create, None is default
    figures = [i for i in figures if i is not None]

    print(f"Writing {len(figures)} figures to {filename}")
    # Write out all of the figures to HTML
    with open(filename, 'w') as f:
        # Write figures. They'll be sorted by the order they were added
        for fig in figures:
            f.write(fig.to_html(full_html=False, include_plotlyjs=True))
