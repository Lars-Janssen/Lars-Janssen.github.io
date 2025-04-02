from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import geopandas as gpd
import pandas as pd

# Initialize Dash app
app = Dash()

stemmen_pivot = pd.read_csv("stemmen_pivot.csv")
gemeente_2023 = gpd.read_file("gemeente_2023.geojson")

# Convert GeoDataFrame to GeoJSON format
geojson_data = gemeente_2023.set_index("statcode").__geo_interface__

# List of all columns except for LijstNaam, RegioCode, Regio, x, y
party_columns = [col for col in stemmen_pivot.columns if col not in
                 ['LijstNaam', 'RegioCode', 'Regio', 'x', 'y']]

# Layout
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='party-dropdown',
            options=[{'label': party, 'value': party} for party
                     in party_columns],
            value=party_columns[0],  # Default to the first party
            style={'width': '50%', 'margin-bottom': '10px'}
        )
    ], style={'textAlign': 'center'}),

    html.Div([
        # Scatter plot on the left
        dcc.Graph(id='scatter_plot', style={'flex': '1'}),
        # Map on the right
        dcc.Graph(id='election_map', style={'flex': '1'})
    ], style={'display': 'flex',
              'flex-direction': 'row',
              'justify-content': 'center',
              'gap': '10px'})
])


# Callback to update the scatter plot when the party changes
@app.callback(
    Output('scatter_plot', 'figure'),
    Input('party-dropdown', 'value')
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
    [Input('party-dropdown', 'value'),
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


server = app.server  # Expose the WSGI app

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
