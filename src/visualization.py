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
    
    # Create a Plotly figure
    fig = go.Figure()

    # Plot the waypoints as blue markers
    fig.add_trace(go.Scatter(
        x=x_coords, y=y_coords, 
        mode='markers+lines',  # Show markers and lines connecting them
        marker=dict(size=6, color='blue', opacity=0.8),
        line=dict(color='blue', width=2),
        name="Flight Path"
    ))

    # Add labels to the waypoints (optional)
    for i, wp in enumerate(photo_plans):
        fig.add_annotation(
            x=wp.x, y=wp.y,
            text=str(i+1),  # Label each waypoint with its index (1-based)
            showarrow=True,
            arrowhead=2,
            ax=0, ay=-10,  # Offset the annotation from the waypoint
            font=dict(size=12, color="black"),
            arrowcolor="black"
        )

    # Update layout for better visualization
    fig.update_layout(
        title="2D Flight Plan",
        xaxis_title='X (meters)',
        yaxis_title='Y (meters)',
        showlegend=False,
        height=800,
        margin=dict(l=0, r=0, b=0, t=50)
    )

    
    
    return fig
