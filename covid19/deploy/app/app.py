import dash
import dash_bootstrap_components as dbc
import os
import pandas as pd

from flask_caching import Cache
from pathlib import Path

# Import for initial data
from datetime import datetime as dt, timedelta
from plotly_figures.maps import *


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    update_title=None,
    suppress_callback_exceptions=True, # because of multi-page setup
)
app.title = 'Covid-19-Interaktionsmodell'

# cache_dir = "./cache"  # JupyterLab
cache_dir = "/app/cache"  # Deploy
Path(cache_dir).mkdir(parents=True, exist_ok=True)
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': cache_dir,
})
cache_timeout=1 #86400  # one day in secounds
cache.clear()

server = app.server


# Initial data

# Asset URL.
base_url = os.getenv('BASE_URL')
prefix_path = os.getenv('PREFIX_PATH')

if base_url is not None and prefix_path is not None:
    asset_url = "{}{}assets/".format(base_url, prefix_path)
else:
    asset_url = "https://jupyter-jsc.fz-juelich.de" \
        + os.getenv('JUPYTERHUB_SERVICE_PREFIX') \
        + "proxy/8050/assets/"


# Initial county id.
init_countyid = 11001  # Berlin Mitte


# Days and dates.
deltadays = 25

# Minimum date.
if os.environ.get('MIN_DATE') is not None:
    min_date = dt.strptime(os.environ.get('MIN_DATE'), '%Y_%m_%d').date() 
else:
    min_date = dt.strptime("2020_02_23", "%Y_%m_%d").date()
# Maximum date.
if os.environ.get('MAX_DATE') is not None:
    max_date = dt.strptime(os.environ.get('MAX_DATE'), '%Y_%m_%d').date() 
else:
    max_date = dt.today().date()
# Initial date.
if os.environ.get('INIT_DATE') is not None:
    init_date = dt.strptime(os.environ.get('INIT_DATE'), '%Y_%m_%d').date() 
else:
    init_date = dt.today().date()
init_date = init_date - timedelta(days=deltadays)  # Can comment out for develop version


# Initial assets dir based on intial date.
init_assets_dir = init_date.strftime('%Y_%m_%d') + "/"

# Calculate correct date for assets directory.
def get_assets_dir(date):
    date = dt.strptime(date.split(' ')[0], '%Y-%m-%d')
    assets_dir = (date - timedelta(days=deltadays)).strftime('%Y_%m_%d') + "/"
    return assets_dir


# CSV data and maps.
metadata_path ="assets/metadata.csv"
metadata = pd.read_csv(metadata_path)

geojson_path = "assets/DE-Landkreise_RKI.geojson.json"
mapcsv_path = "assets/figures/{}map.csv".format(init_assets_dir)
counties_geojson, counties_metadf = create_static_map_data(geojson_path)

# Initial maps.
init_mapfig_bstim = create_map_figure(
    counties_geojson, counties_metadf, mapcsv_path, column='newInf100k',)
#     width=500, height=450)
init_mapfig_rki = create_map_figure(
    counties_geojson, counties_metadf, mapcsv_path, column='newInf100k_RKI',)
#     width=500, height=450)


# import layout at the end of this file is important to deploy it with gunicorn
import index
