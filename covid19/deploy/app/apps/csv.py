import dash_bootstrap_components as dbc

from layouts.csv_erklaerungen import landkreis_csv, karten_csv, metadaten_csv


csv_layout = dbc.Container(
    style={'marginTop': 100, 'marginBottom': 20},
    children=[
        landkreis_csv,
        karten_csv,
        metadaten_csv
    ]
)