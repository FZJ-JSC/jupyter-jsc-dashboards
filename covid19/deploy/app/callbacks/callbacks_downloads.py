import dash_html_components as html

from dash.dependencies import Input, Output, State
from datetime import datetime as dt

from app import app, get_assets_datadir
from app import counties_metadf, threshold_date


def update_download_link(value, assets_dir):
    selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
    if (threshold_date is not None) and (selected_date <= threshold_date):
        return "", "", "", {'display': 'none'}

    assets_datadir = get_assets_datadir(selected_date)
    county_id = '{:05d}'.format(value)
    county_series = counties_metadf.loc[counties_metadf['cca'] == county_id].names
    county = county_series.tolist()[0]
    file_name = '{}_{}.csv'.format(county_id, county)
    csv_path = f"assets/{assets_datadir}{file_name}"

    text = "Rohdaten für {} vom {} als CSV Datei".format(
        county, selected_date.strftime('%d.%m.%Y'))
    return file_name, csv_path, html.Small(text), {'display': 'inline'}


for side in ['left', 'right']:
    app.callback(
        [Output(f"download_{side}_download", 'download'),
         Output(f"download_{side}_download", 'href'),
         # Disable button and change text for unavailable csv files
         Output(f"download_{side}_download", 'children'),
         Output(f"download_{side}_erklaerung", 'style')
        ],
        [Input(f"pos_control_{side}_variable", 'value'),
         Input(f"date_picker_{side}_output_container", 'children')]
    )(update_download_link)

