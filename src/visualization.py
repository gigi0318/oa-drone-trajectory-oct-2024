"""Utility to visualize photo plans.
"""

import typing as T

import plotly.graph_objects as go

from src.data_model import Waypoint


def plot_photo_plan(photo_plans: T.List[Waypoint]) -> go.Figure:
    """Plot the photo plan on a 2D grid.

    Args:
        photo_plans (T.List[Waypoint]): List of waypoints for the photo plan.

    Returns:
        T.Any: Plotly figure object.
    """
    # Extracting x and y coordinates of the waypoints
    x_coords = [wp.x for wp in photo_plans]
    y_coords = [wp.y for wp in photo_plans]
    
    fig = go.Figure(data=go.Scatter(x=x_coords, y=y_coords,mode='lines+markers'))
    # Edit the layout
    fig.update_layout(
            xaxis=dict(
                title=dict(
                    text='X(metres)'
                )
            ),
            yaxis=dict(
                title=dict(
                    text='Y(metres)'
                )
            ),
    )
    fig.show()
    return fig
