import dash
from dash import dcc, html
import dash.dependencies as dd
from dash import dash_table
import plotly.express as px
import json
import pandas as pd

# Load geojson and data
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
            "Bevolking": True,
            "Land": True,
            "Stationsdichtheid": False
        }
    )
    # Update map layout
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


# Create the initial scatter plot for Bevolking and Land
scatter_fig = px.scatter(
    gdf,
    x="Bevolking",
    y="Land",
    color="Stations",
    hover_name="Gemeentenaam",
    title="Scatter Plot: Bevolking vs. Land"
)

display_columns = ["Gemeentenaam", "Provincienaam",
                   "Bevolking", "Land", "Bevolkingsdichtheid", "Stations"]

# Define the layout with three columns
app.layout = html.Div([
    html.H1("Stationsdichtheid in Nederland"),
    html.Div([
        # Left column: Data table with sorting enabled
        html.Div([
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": col, "id": col} for col in display_columns],
                data=gdf.to_dict('records'),
                page_size=10,
                sort_action="native",  # Enable native column sorting
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'}
            )
        ], style={'width': '30%', 'display': 'inline-block',
                  'verticalAlign': 'top', 'padding': '0 10px'}),

        # Middle column: Scatter plot (zoomable)
        html.Div([
            dcc.Graph(
                id='scatter-graph',
                figure=scatter_fig,
                config={'scrollZoom': True}  # Enable scroll zoom
            )
        ], style={'width': '30%', 'display': 'inline-block',
                  'verticalAlign': 'top', 'padding': '0 10px'}),

        # Right column: Choropleth map with dropdown
        html.Div([
            dcc.Dropdown(
                id="color-dropdown",
                options=color_options,
                value="Stationsdichtheid",  # Default value
                clearable=False,
                style={'marginBottom': '10px'}
            ),
            dcc.Graph(
                id="map-graph",
                figure=create_figure("Stationsdichtheid")
            )
        ], style={'width': '40%', 'display': 'inline-block',
                  'verticalAlign': 'top', 'padding': '0 10px'})
    ], style={'display': 'flex'})
])


# Define callback to update the choropleth map based on dropdown selection
@app.callback(
    dd.Output("map-graph", "figure"),
    dd.Input("color-dropdown", "value")
)
def update_map(color_column):
    return create_figure(color_column)


server = app.server  # Expose the WSGI app

if __name__ == "__main__":
    app.run(debug=True)
