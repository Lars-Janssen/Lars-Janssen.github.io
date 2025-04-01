import dash
from dash import dcc, html
import dash.dependencies as dd
import plotly.express as px
import json
import pandas as pd


with open("gemeente_2025.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

gdf = pd.read_csv("gdf.csv")

# Create the Dash app
app = dash.Dash(__name__)

# Define the options for the dropdown
color_options = [
    {"label": "Bevolking", "value": "Bevolking"},
    {"label": "Stations", "value": "Stations"},
    {"label": "Land", "value": "Land"},
    {"label": "Stationsdichtheid", "value": "Stationsdichtheid"},
    {"label": "Bevolkingsdichtheid", "value": "Bevolkingsdichtheid"}
]


# Define function to create choropleth
def create_figure(color_column):
    fig = px.choropleth(
        gdf,
        geojson=geojson,
        color=color_column,  # Color based on selected column
        locations="Gemeentecode",
        featureidkey="properties.statcode",
        projection="mercator",
        hover_name="Gemeentenaam",
        hover_data={
            "Stations": True,
            "Gemeentecode": False,
            "Bevolking_fmt": True,
            "Land": True,
            "Stationsdichtheid": False
        }
    )

    # Update hover template
    fig.for_each_trace(
        lambda t: t.update(hovertemplate=t.
                           hovertemplate.replace("Bevolking_fmt", "Bevolking"))
        if t.hovertemplate else None
    )

    # Update map layout
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


# Define the layout of the app
app.layout = html.Div([
    html.H1("Stationsdichtheid in Nederland"),

    # Dropdown to select color column
    dcc.Dropdown(
        id="color-dropdown",
        options=color_options,
        value="Stationsdichtheid",  # Default value
        clearable=False
    ),

    # Graph for the choropleth
    dcc.Graph(id="map-graph")
])


# Define callback to update the figure
@app.callback(
    dd.Output("map-graph", "figure"),
    dd.Input("color-dropdown", "value")
)
def update_map(color_column):
    return create_figure(color_column)


server = app.server  # Required for deployment

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


