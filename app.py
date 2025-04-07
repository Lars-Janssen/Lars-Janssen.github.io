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

# Layout: Flex container with graphs on the left and party list on the right
app.layout = html.Div([
    # Dashboard container with a border and fixed height
    html.Div([
        # Party list container (on the right) with fixed height and scrollable overflow
        html.Div([
            html.H4("Partijen"),
            dcc.RadioItems(
                id='party-list',
                options=[{'label': party, 'value': party} for party in party_columns],
                value=party_columns[0],
                labelStyle={'display': 'block', 'margin-bottom': '5px'}
            )
        ], style={
            'width': '20%',
            'padding': '10px',
            'overflowY': 'scroll'
        }),
        # Graphs container
        html.Div([
            dcc.Graph(id='scatter_plot', style={'width': '49%', 'display': 'inline-block'}),
            dcc.Graph(id='election_map', style={'width': '49%', 'display': 'inline-block'})
        ], style={
            'flex': '1',
            'padding': '10px'
        })
    ], style={
        'display': 'flex',
        'height': '750px',
        'border': '10px solid black',  # Adjust border thickness and color as needed
        'margin-bottom': '20px'
    }),

    # Explanation text below the dashboard
    html.Div([
        html.P(
            "Dit dashboard visualiseert de uitslag van de Tweede Kamerverkiezingen op het gebied van gemeenten. "
            "Links kunt u een partij kiezen waarvan u de uitslag wilt bekijken."
        ),
        html.P(
            "De grafiek in het midden vergt wat uitleg. In de onderstaande tabel ziet u de uitslag van de gemeente Amsterdam "
            "in percentages van de totale hoeveelheid stemmen. Dit geeft de gemeente Amsterdam een coördinaat in 26 dimensies, "
            "aangezien er 26 partijen waren deze verkiezing. Om dit in een grafiek te laten zien gebruiken we het TSNE algoritme. "
            "Dit perst de coördinaten van 26D naar 2D en probeert te zorgen dat coördinaten die dicht bij elkaar staan dicht bij elkaar blijven. "
            "Deze grafiek is vooral interessant om te bekijken voor partijen waarvan de aanhang geconcentreerd is, zoals bijvoorbeeld de SGP, ChristenUnie, "
            "Volt, Nieuw Sociaal Contract, of BIJ1. Ook bij de VVD zijn bijvoorbeeld de rijkste gemeenten van Nederland goed te herkennen."
        ),
        html.P(
            "Op de kaart aan de rechterkant is vervolgens te zien welk percentage van de stemmen de partij in alle gemeenten heeft gekregen. "
            "Let hierbij wel op dat de schaal aan de rechterkant varieert, omdat anders de verschillen voor kleine partijen niet te zien zou zijn. "
            "U kunt gemeenten selecteren in de grafiek in het midden, waarna de kaart aan de rechterkant alleen de geselecteerde gemeenten laat zien. "
            "Als u de bovenste gemeenten selecteert zult u de Bijbelgordel zien en de onderste gemeenten komen overeen met Twente."
        )
    ], style={
        'width': '75%',
        'margin': 'auto',
        'padding': '20px',
        'textAlign': 'center'
    })
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
        xaxis=dict(visible=False),  # Hide x-axis
        yaxis=dict(visible=False),  # Hide y-axis
        showlegend=False,
        dragmode="select",  # Enable box/lasso selection
    )
    # Remove the colorbar from the scatter plot
    scatter_fig.update(layout_coloraxis_showscale=False)
    return scatter_fig


# Callback to update the map based on party selection and scatter plot selection
@app.callback(
    Output('election_map', 'figure'),
    [Input('party-list', 'value'),
     Input('scatter_plot', 'selectedData')]
)
def update_map(selected_party, selected_data):
    # Determine the selected regions from the scatter plot selection (using hover text, which is 'Regio')
    selected_regions = []
    if selected_data and 'points' in selected_data:
        selected_regions = [point['hovertext'] for point in selected_data['points']]

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
    # Remove the colorbar title (name above the scale)
    map_fig.update_coloraxes(colorbar_title="")
    return map_fig


server = app.server

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
