from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import geopandas as gpd
import pandas as pd


stemmen_pivot = pd.read_csv("stemmen_pivot.csv")
gemeente_2023 = gpd.read_file("gemeente_2023.geojson")

# Initialize Dash app
app = Dash(__name__)

# Convert GeoDataFrame to GeoJSON format
geojson_data = gemeente_2023.set_index("statcode").__geo_interface__

# List of all columns except for LijstNaam, RegioCode, Regio, x, y
party_columns = [col for col in stemmen_pivot.columns
                 if col not in ['LijstNaam', 'RegioCode', 'Regio', 'x', 'y']]

# Layout: Left side for parties list, right side for graphs
app.layout = html.Div([
    html.Div([
        html.H4("Parties"),
        dcc.RadioItems(
            id='party-list',
            options=[{'label': party, 'value': party} for party
                     in party_columns],
            value=party_columns[0],
            labelStyle={'display': 'block', 'margin-bottom': '5px'}
        )
    ], style={'width': '20%',
              'display': 'inline-block',
              'verticalAlign': 'top',
              'padding': '10px'}),

    html.Div([
        dcc.Graph(id='scatter_plot', style={'width': '49%',
                                            'display': 'inline-block'}),
        dcc.Graph(id='election_map', style={'width': '49%',
                                            'display': 'inline-block'})
    ], style={'width': '75%', 'display': 'inline-block', 'padding': '10px'})
])


# Callback to update the scatter plot when the party selection changes
@app.callback(
    Output('scatter_plot', 'figure'),
    Input('party-list', 'value')
)
def update_scatter(selected_party):
    scatter_fig = px.scatter(
        data_frame=stemmen_pivot,
        x="x",
        y="y",
        hover_name="Regio",
        color=selected_party,
        hover_data={"x": False, "y": False, selected_party: True}
    )
    scatter_fig.update_layout(
        width=700,
        height=700,
        xaxis=dict(scaleanchor="y"),
        showlegend=False,
        dragmode="select"  # Enable box/lasso selection
    )
    return scatter_fig


# Callback to update the map based on party selection
# and scatter plot selection
@app.callback(
    Output('election_map', 'figure'),
    [Input('party-list', 'value'),
     Input('scatter_plot', 'selectedData')]
)
def update_map(selected_party, selected_data):
    # Determine the selected regions from the scatter plot selection
    # (using hover text, which is 'Regio')
    selected_regions = []
    if selected_data and 'points' in selected_data:
        selected_regions = [point['hovertext'] for point
                            in selected_data['points']]

    # Filter the data only if there is an active selection
    filtered_data = stemmen_pivot if not selected_regions else \
        stemmen_pivot[stemmen_pivot['Regio'].isin(selected_regions)]

    map_fig = px.choropleth(
        filtered_data,
        geojson=geojson_data,
        locations="RegioCode",
        color=selected_party,
        featureidkey="id",
        projection="mercator",
        hover_name="Regio",
        hover_data={"Regio": False, selected_party: True, "RegioCode": False}
    )
    map_fig.update_geos(
        fitbounds="geojson",
        visible=True,
        showcountries=False,
        showland=True,
        landcolor="white"
    )
    map_fig.update_layout(
        geo=dict(
            center=dict(lat=52.3784, lon=4.9009),
            projection_scale=6,
            visible=False,
            lonaxis=dict(range=[3, 8]),
            lataxis=dict(range=[50, 54])
        ),
        uirevision="fixed",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        width=700,
        height=700
    )

    return map_fig


server = app.server

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
