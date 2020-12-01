import os
from dash.dependencies import Input, Output
from plotly_figures.maps import *

from app import app, asset_url, get_assets_dir, init_assets_dir, zmax
from app import cache, cache_timeout, threshold_date
from app import counties_geojson, counties_metadf
from app import get_assets_datadir
from callbacks.logging import setup_logger
from datetime import datetime as dt, timedelta


logger = setup_logger()


# Hidden div
@app.callback(
    Output(component_id='date_picker_left_output_container', component_property='children'),
    [Input(component_id='date_picker_left', component_property='date')])
def update_date_picker(date):
    if date is not None:
        return get_assets_dir(date)
    else:
        return init_assets_dir

@app.callback(
    Output(component_id='date_picker_right_output_container', component_property='children'),
    [Input(component_id='date_picker_right', component_property='date')])
def update_date_picker(date):
    if date is not None:
        return get_assets_dir(date)
    else:
        return init_assets_dir


# Callback maps
def update_map(assets_dir, column):
    selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
    assets_datadir = get_assets_datadir(selected_date)

    mapcsv_path = "assets/" + assets_datadir + "map.csv"
    logger.debug("Update map: Looking for {}".format(mapcsv_path))
    mapfig = create_map_figure(
        counties_geojson, counties_metadf, mapcsv_path, column=column,
        zmax=zmax
    )
    return mapfig


# BSTIM map
# Use date picker as Input and not its output container to  
# prevent rerendering of the map when the window is resized.
@app.callback(
     Output(component_id='bstim_map_tab_left_graph', component_property='figure'),
    [Input(component_id='date_picker_left', component_property='date')])
@cache.memoize(timeout=cache_timeout)
def update_bstim_map(date):
    assets_dir = get_assets_dir(date)
    return update_map(assets_dir, column='newInf100k')

@app.callback(
     Output(component_id='bstim_map_tab_right_graph', component_property='figure'),
    [Input(component_id='date_picker_right', component_property='date')])
@cache.memoize(timeout=cache_timeout)
def update_bstim_map(date):
    assets_dir = get_assets_dir(date)
    return update_map(assets_dir, column='newInf100k')


# RKI map
@app.callback(
    Output(component_id='rki_map_tab_left_graph', component_property='figure'),
    [Input(component_id='date_picker_left', component_property='date')])
@cache.memoize(timeout=cache_timeout)
def update_rki_map(date):
    assets_dir = get_assets_dir(date)
    return update_map(assets_dir, column='newInf100k_RKI')

@app.callback(
    Output(component_id='rki_map_tab_right_graph', component_property='figure'),
    [Input(component_id='date_picker_right', component_property='date')])
@cache.memoize(timeout=cache_timeout)
def update_rki_map(date):
    assets_dir = get_assets_dir(date)
    return update_map(assets_dir, column='newInf100k_RKI')


# Callbacks interaction kernel
def get_ikernel_img_url(assets_dir):
    imgUrl = ""
    if assets_dir is not None:
        imgUrl = "figures/" + assets_dir + "interaction_kernel.png"
    if not os.path.isfile("assets/" + imgUrl): 
        imgUrl = "placeholders/plot_not_found.png"
    imgUrl = asset_url + imgUrl
    return imgUrl, imgUrl

@app.callback(
    [Output(component_id='ikernel_tab_left_img', component_property='src'),
     Output(component_id='ikernel_tab_left_modal_img', component_property='src')],
    [Input(component_id='date_picker_left_output_container', component_property='children')])
def update_ikernel_tab_img(assets_dir):
    return get_ikernel_img_url(assets_dir)

@app.callback(
    [Output(component_id='ikernel_tab_right_img', component_property='src'),
     Output(component_id='ikernel_tab_right_modal_img', component_property='src')],
    [Input(component_id='date_picker_right_output_container', component_property='children')])
def update_ikernel_tab_img(assets_dir):
    return get_ikernel_img_url(assets_dir)