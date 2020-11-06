from dash.dependencies import Input, Output
from plotly_figures.maps import *

from app import app, cache, cache_timeout, get_assets_dir
from app import counties_geojson, counties_metadf


# Callbacks
# Hidden div
@app.callback(
    Output(component_id='date_picker_output_container', component_property='children'),
    [Input(component_id='date_picker', component_property='date')])
def update_date_picker(date):
    if date is not None:
        return get_assets_dir(date)
    else:
        return init_assets_dir
    
    
# Callback maps
# BSTIM map
@app.callback(
     Output(component_id='bstim_map_tab_graph', component_property='figure'),
    [Input(component_id='date_picker', component_property='date')])
@cache.memoize(timeout=cache_timeout)
def update_bstim_map(date):
    if date is not None:
        assets_dir = get_assets_dir(date)
        mapcsv_path = "assets/figures/{}map.csv".format(assets_dir)
    else:
        mapcsv_path = "assets/placeholders/map_empty.csv"
    mapfig = create_map_figure(
        counties_geojson, counties_metadf, mapcsv_path, column='newInf100k',)
#         width=500, height=450)
    return mapfig

# RKI map
@app.callback(
    Output(component_id='rki_map_tab_graph', component_property='figure'),
    [Input(component_id='date_picker', component_property='date')])
@cache.memoize(timeout=cache_timeout)
def update_rki_map(date):
    if date is not None:
        assets_dir = get_assets_dir(date)
        mapcsv_path = "assets/figures/{}map.csv".format(assets_dir)
    else:
        mapcsv_path = "assets/placeholders/map_empty.csv"
    mapfig = create_map_figure(
        counties_geojson, counties_metadf, mapcsv_path, column='newInf100k_RKI',)
#         width=500, height=450)
    return mapfig


# Callbacks interaction kernel
# @app.callback(
#     [Output(component_id='ikernel_tab_img', component_property='src'),
#      Output(component_id='ikernel_tab_modal_img', component_property='src')],
#     [Input(component_id='date_picker', component_property='date')])
# def update_ikernel_tab_img(date):
#     imgUrl=""
#     if date is not None:
#         assets_dir = get_assets_dir(date)
#         imgUrl = "figures/" + assets_dir + "interaction_kernel.png"
#     if not os.path.isfile("assets/" + imgUrl): 
#         imgUrl = "placeholders/plot_not_found.png"
#     imgUrl = asset_url + imgUrl
#     return imgUrl, imgUrl