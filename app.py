from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import geopandas as gpd
import pandas as pd

stemmen_pivot = pd.read_csv("stemmen_pivot.csv")
gemeente_2023 = gpd.read_file("gemeente_2023.geojson")
c = gpd.read_file("cartogram.geojson")

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import geopandas as gpd

# —————————————————————————————————————————————
# Assume you have already read in/created:
#   • c               — your cartogram GeoDataFrame
#   • gemeente_2023   — your normal-boundary GeoDataFrame
#   • stemmen_pivot   — your election results pivot table
# and that they all have a "statcode" column matching your RegioCode values.
# —————————————————————————————————————————————

# Convert GeoDataFrames to GeoJSON format
geojson_data_cartogram = c.set_index("statcode").__geo_interface__
geojson_data_normal   = gemeente_2023.set_index("statcode").__geo_interface__

# List of all party columns in your pivoted DataFrame
party_columns = [
    col for col in stemmen_pivot.columns
    if col not in ['LijstNaam', 'RegioCode', 'Regio', 'x', 'y']
]

# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    # Left panel: party selector
    html.Div([
        html.H4("Parties"),
        dcc.RadioItems(
            id='party-list',
            options=[{'label': p, 'value': p} for p in party_columns],
            value=party_columns[0],
            labelStyle={'display': 'block', 'margin-bottom': '5px'}
        )
    ], style={
        'width': '20%', 'display': 'inline-block',
        'verticalAlign': 'top', 'padding': '10px'
    }),

    # Right panel: map-type selector + graphs
    html.Div([
        # Map-type toggle
        html.Div([
            html.Label("Map Type:"),
            dcc.RadioItems(
                id='map-type',
                options=[
                    {'label': 'Standard', 'value': 'normal'},
                    {'label': 'Cartogram', 'value': 'cartogram'}
                ],
                value='normal',
                labelStyle={'display': 'inline-block', 'margin-right': '15px'}
            )
        ], style={'textAlign': 'right', 'marginBottom': '10px'}),

        # Scatter plot and map side by side
        dcc.Graph(id='scatter_plot', style={
            'width': '49%', 'display': 'inline-block'
        }),
        dcc.Graph(id='election_map', style={
            'width': '49%', 'display': 'inline-block'
        })
    ], style={
        'width': '75%', 'display': 'inline-block',
        'padding': '10px'
    })
])

# —————————————————————————————————————————————
# Callback: update scatter plot when party changes
# —————————————————————————————————————————————
@app.callback(
    Output('scatter_plot', 'figure'),
    Input('party-list', 'value')
)
def update_scatter(selected_party):
    fig = px.scatter(
        data_frame=stemmen_pivot,
        x="x",
        y="y",
        hover_name="Regio",
        color=selected_party,
        hover_data={"x": False, "y": False, selected_party: True}
    )
    fig.update_layout(
        width=700,
        height=700,
        xaxis=dict(scaleanchor="y"),
        showlegend=False,
        dragmode="select"
    )
    return fig

# —————————————————————————————————————————————
# Callback: update map when party, selection, or map type changes
# —————————————————————————————————————————————
@app.callback(
    Output('election_map', 'figure'),
    [
        Input('party-list', 'value'),
        Input('scatter_plot', 'selectedData'),
        Input('map-type', 'value')
    ]
)
def update_map(selected_party, selected_data, map_type):
    # get selected regions
    if selected_data and 'points' in selected_data:
        selected_regions = [p['hovertext'] for p in selected_data['points']]
    else:
        selected_regions = []

    # filter data if needed
    df = (stemmen_pivot
          if not selected_regions
          else stemmen_pivot[stemmen_pivot['Regio'].isin(selected_regions)]
         )

    # choose normal vs cartogram geometry
    gj = (geojson_data_normal
          if map_type == 'normal'
          else geojson_data_cartogram)

    # build choropleth
    map_fig = px.choropleth(
        df,
        geojson=gj,
        locations="RegioCode",
        color=selected_party,
        featureidkey="id",
        projection="mercator",
        hover_name="Regio",
        hover_data={selected_party: True, "RegioCode": False}
    )

    # ---- hide Europe & all other background geography ----
    map_fig.update_geos(
        fitbounds="geojson",
        showcountries=False,
        showcoastlines=False,
        showsubunits=False,
        showframe=False,
        showland=True,         # keep your regions’ land fill
        landcolor="white"      # white‑out everything else
    )

    map_fig.update_layout(
        geo=dict(
            center=dict(lat=52.3784, lon=4.9009),
            projection_scale=6,
            lonaxis=dict(range=[3, 8]),
            lataxis=dict(range=[50, 54])
        ),
        uirevision="fixed",
        margin={"r":0, "t":0, "l":0, "b":0},
        width=700,
        height=700
    )

    return map_fig


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
