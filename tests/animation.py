import pandas as pd
import plotly.graph_objects as go

# Load the dummy movement data
df = pd.read_csv("dummy_data.csv")

# Create frames for each point in time
frames = []
for i in range(1, len(df)):
    frames.append(
        go.Frame(
            data=[
                # Line connecting all previous points
                go.Scattermapbox(
                    mode="lines+markers",
                    lat=df["latitude"][: i + 1],  # Include all previous points
                    lon=df["longitude"][: i + 1],
                    line=dict(width=2, color="blue"),
                    marker=dict(size=8, color="blue"),
                    name="Trajectory",
                ),
                # Highlight the current point
                go.Scattermapbox(
                    mode="markers",
                    lat=[df["latitude"][i]],
                    lon=[df["longitude"][i]],
                    marker=dict(size=15, color="red", symbol="circle"),
                    name="Current Position",
                ),
            ],
            name=f"Time: {df['time'][i]}",  # Frame name for each timestamp
        )
    )

# Create the initial figure
fig = go.Figure(
    data=[
        go.Scattermapbox(
            mode="lines+markers",
            lat=[df["latitude"][0]],
            lon=[df["longitude"][0]],
            line=dict(width=2, color="blue"),
            marker=dict(size=8, color="blue"),
            name="Trajectory",
        ),
        go.Scattermapbox(
            mode="markers",
            lat=[df["latitude"][0]],
            lon=[df["longitude"][0]],
            marker=dict(size=15, color="red", symbol="circle"),
            name="Current Position",
        ),
    ],
    layout=go.Layout(
        mapbox=dict(
            style="carto-darkmatter",  # Dark-themed map style
            zoom=3,
            center=dict(lat=df["latitude"].mean(), lon=df["longitude"].mean()),
        ),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(label="Play", method="animate", args=[None, dict(frame=dict(duration=500, redraw=True))]),
                    dict(label="Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False))]),
                ],
            )
        ],
    ),
    frames=frames,
)

# Show the figure
fig.show()
