import dash
import dash_bootstrap_components as dbc
import os
import pandas as pd

from flask_caching import Cache
from pathlib import Path

# Import for initial data
from datetime import datetime as dt, timedelta
from plotly_figures.maps import *

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

## JupyterLab
# from jupyter_dash import JupyterDash
# dash_app = JupyterDash(
app = dash.Dash(  # Deploy
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME],
    update_title=None,
    suppress_callback_exceptions=True, # because of multi-page setup
)
# app = dash_app  # JupyterLab
app.title = 'Covid-19-Interaktionsmodell'

# cache_dir = "./cache"  # JupyterLab
cache_dir = "/app/cache"  # Deploy
Path(cache_dir).mkdir(parents=True, exist_ok=True)
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': cache_dir,
    # 'CACHE_THRESHOLD': 10000, # max. no. items stored before deletion starts (only for SimpleCache and FileSystemCache)
    ## try 'redis' if you want to use a database for caching
    # 'CACHE_TYPE': 'redis'
    # 'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '')  
})
# cache_timeout = 1 # JupyterLab
cache_timeout = 86400  # one day in secounds
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

# zmax
zmax = 100

# set fixed width and height of plot
# (needed to ensure users do not see the plot too large first on Firefox)
fixed_plot_width = 450
fixed_plot_height = 300

# Days and dates.
deltadays = 0  # 25

# Threshold date (switch from figures to csv)
threshold_date = os.getenv('THRESHOLD_DATE')
if threshold_date is not None:
    threshold_date = dt.strptime(threshold_date, '%Y_%m_%d')

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


# Calculate correct date for assets directory.
def get_assets_dir(date):
    date = dt.strptime(date.split(' ')[0], '%Y-%m-%d')
    assets_dir = (date - timedelta(days=deltadays)).strftime('%Y_%m_%d') + "/"
    return assets_dir


# get the data dir (assets/figures or assets/csv) depending on threshold_date
def get_assets_datadir(date):
    data_dir = ''
    if (threshold_date is not None) and (date <= threshold_date):
        assets_dir = (date - timedelta(days=25)).strftime('%Y_%m_%d') + "/"
        data_dir = "figures/{}".format(assets_dir)
    else:
        assets_dir = date.strftime('%Y_%m_%d') + "/"
        data_dir = "csv/{}".format(assets_dir)
    return data_dir


# Initial assets dir based on initial date (e.g. "2020_11_01/")
init_date_dt = dt(init_date.year, init_date.month, init_date.day)
if (threshold_date is not None) and (init_date_dt <= threshold_date):
    init_assets_dir = (init_date - timedelta(days=25)).strftime('%Y_%m_%d') + "/"
else:
    init_assets_dir = init_date.strftime('%Y_%m_%d') + "/"

# Initial assets path based on initial date (e.g. "assets/csv/2020_11_01/")
init_assets_path = "assets/" + get_assets_datadir(dt(init_date.year, init_date.month, init_date.day))

# CSV data and maps.
metadata_path = "assets/metadata.csv"
metadata = pd.read_csv(metadata_path)

geojson_path = "assets/DE-Landkreise_RKI.geojson.json"
mapcsv_path = "{}map.csv".format(init_assets_path)
counties_geojson, counties_metadf = create_static_map_data(geojson_path)

# Get n_people df from a chosen date
metadata_csv = pd.read_csv("assets/csv/2020_10_19/metadata.csv")
n_people_array = []
# Get no. people for each county from mapcsv 
for feat in counties_geojson['features']:
    # Need the county id to find the corresponding value in metadata_csv
    cca_str = feat['properties'].get('RS')
    if cca_str is not None:
        cca_filtered_df = metadata_csv.loc[metadata_csv['countyID']==int(cca_str), 'n_people']
        cca_value = next(iter(cca_filtered_df), 0.0)
        n_people_array.append(cca_value)
    else:
        n_people_array.append(0.0)
n_people_df = pd.DataFrame(data={'n_people': n_people_array})

# Initial maps.
init_mapfig_bstim = create_map_figure(
    counties_geojson, counties_metadf, mapcsv_path,
    n_people=n_people_df, column='newInf100k',
    width=500, height=450)  # size is important to ensure, that figure is created _now_ and not on resize-event
init_mapfig_rki = create_map_figure(
    counties_geojson, counties_metadf, mapcsv_path, 
    n_people=n_people_df, column='newInf100k_RKI',
    width=500, height=450)  # size is important to ensure, that figure is created _now_ and not on resize-event

# import layout at the end of this file is important to deploy it with gunicorn
import index
