import dash_html_components as html

from dash.dependencies import Input, Output, State
from datetime import datetime as dt

from app import app, get_assets_datadir, threshold_date


def update_download_link(value, assets_dir):
    selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
    assets_datadir = get_assets_datadir(selected_date)
    file_name = '{:05d}.csv'.format(value)
    csv_path = f"assets/{assets_datadir}{file_name}"
    
    if (threshold_date is not None) and (selected_date <= threshold_date):
        className = "btn btn-secondary disabled mt-2"
        children = [html.I(className='fa fa-download mr-2'), 'Nicht verfügbar']
    else:
        className = "btn btn-primary mt-2"
        children = [html.I(className='fa fa-download mr-2'), 'CSV Datei']
    return file_name, csv_path, className, children
   


for side in ['left', 'right']:
    app.callback(    
        [Output(f"pos_control_{side}_download", 'download'),
         Output(f"pos_control_{side}_download", 'href'),
         # Disable button and change text for unavailable csv files
         Output(f"pos_control_{side}_download", 'className'),
         Output(f"pos_control_{side}_download", 'children')
        ],
        [Input(f"pos_control_{side}_variable", 'value'),
         Input(f"date_picker_{side}_output_container", 'children')]
    )(update_download_link)

