from flask import Flask, render_template
import dash
from dash import dcc, html
import plotly.graph_objs as go
import numpy as np

# Initialize Flask app
flask_app = Flask(__name__)

# Initialize Dash app
app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dash/')

# Planetary data with realistic colors
planets = {
    "Mercury": {"distance": 0.39, "color": "#b1b1b1", "size": 0.383},  # Gray
    "Venus": {"distance": 0.72, "color": "#e3db77", "size": 0.949},    # Pale yellow
    "Earth": {"distance": 1.0, "color": "#1f77b4", "size": 1.0},       # Blue
    "Mars": {"distance": 1.52, "color": "#d62728", "size": 0.532},     # Red
    "Jupiter": {"distance": 5.2, "color": "#ff7f0e", "size": 11.21},   # Orange-brown
    "Saturn": {"distance": 9.58, "color": "#e2c5a2", "size": 9.45},    # Pale golden
    "Uranus": {"distance": 19.2, "color": "#7f7fff", "size": 4.0},     # Light blue
    "Neptune": {"distance": 30.05, "color": "#1f77b4", "size": 3.88}   # Blue
}

# Sun data
sun = {"color": "#ffff00", "size": 10}  # Yellow

# Create 3D figure for the Solar System
fig = go.Figure()

# Add the Sun at the center
fig.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers',
    marker=dict(
        size=sun["size"] * 10,  # Scale the Sun size
        color=sun["color"],  # Sun's yellow color
        symbol='circle',
        opacity=1
    ),
    name='Sun'
))

# Add planets and orbits to the plot
for planet, data in planets.items():
    # Orbit path (simplified as a circle)
    orbit_theta = np.linspace(0, 2 * np.pi, 360)  # Full circle in radians
    orbit_x = data["distance"] * np.cos(orbit_theta)
    orbit_y = data["distance"] * np.sin(orbit_theta)
    orbit_z = np.zeros(360)  # Orbits are in the XY plane

    # Add orbit trace
    fig.add_trace(go.Scatter3d(
        x=orbit_x, y=orbit_y, z=orbit_z,
        mode='lines',
        line=dict(color='white', width=1.5),
        name=f'{planet} Orbit'
    ))

    # Add planet markers (with approximate real-life colors)
    fig.add_trace(go.Scatter3d(
        x=[data["distance"]],
        y=[0],
        z=[0],
        mode='markers',
        marker=dict(
            size=10 * data["size"],  # Scale planet size
            color=data["color"],  # Realistic color for each planet
            symbol='circle',
            opacity=1
        ),
        name=planet
    ))

# Layout configuration for 3D plot
fig.update_layout(scene=dict(
    xaxis=dict(title='X (AU)', showbackground=False, visible=False),
    yaxis=dict(title='Y (AU)', showbackground=False, visible=False),
    zaxis=dict(title='Z (AU)', showbackground=False, visible=False),
    aspectratio=dict(x=1, y=1, z=1),
    camera=dict(eye=dict(x=2, y=2, z=0.1)),  # Camera positioning
),
    title="Realistic 3D Solar System Orrery",
    template="plotly_dark",
    margin=dict(l=0, r=0, b=0, t=0),
    height=800,
    width=1200
)

# Dash layout for the app
app.layout = html.Div(children=[
    html.H1(children='Realistic 3D Solar System Orrery'),
    dcc.Graph(
        id='solar-system-orrery',
        figure=fig
    )
])

# Flask route for the homepage
@flask_app.route('/')
def index():
    return render_template('index.html')

# Run the Flask-Dash app
if __name__ == '__main__':
    flask_app.run(debug=True)