import dash

from dash.dependencies import Input, Output
from datetime import datetime as dt
from plotly_figures.maps import create_map_figure

from app import app, cache, cache_timeout
from app import get_assets_datadir, init_countyid, zmax
from app import counties_geojson, counties_metadf
from callbacks.logging import setup_logger


logger = setup_logger()


def update_map_figure(assets_dir, column, normed_to_100k=True):
    selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
    assets_datadir = get_assets_datadir(selected_date)

    mapcsv_path = "assets/" + assets_datadir + "map.csv"
    logger.debug("Update map: Looking for {}".format(mapcsv_path))
    mapfig = create_map_figure(
        counties_geojson, counties_metadf, mapcsv_path, column=column,
        normed_to_100k=normed_to_100k, 
        zmax=zmax
    )
    return mapfig


# Change dropbox value on map-click
def update_mapclick(choro1_click, choro2_click):
    ctx = dash.callback_context
    if not ctx.triggered:
        id_str = init_countyid
    else:
        cid = ctx.triggered[0]['value']['points'][0]['location']
        id_str = counties_metadf['cca'][cid]
    return int(id_str)


for side in ['left', 'right']:
    # Update map figure
    @app.callback(
        [Output(f"bstim_map_tab_{side}_graph", 'figure'),
         Output(f"rki_map_tab_{side}_graph", 'figure')],
        # When the button color changes, we toggled incidence values
        [Input(f"toggle_{side}_7_days_button1", 'color'),
         Input(f"toggle_{side}_100k_button1", 'color'),
         Input(f"date_picker_{side}_output_container", 'children')],
    )    
    @cache.memoize(timeout=cache_timeout)
    def update_bstim_map(btn_color_7_days, btn_color_100k, assets_dir):
        if btn_color_7_days == 'primary':  # 7 day incidence is selected
            if btn_color_100k == 'primary':  # 100k is selected
                bstim_map = update_map_figure(assets_dir, column='7DayInf100k')
                rki_map = update_map_figure(assets_dir, column='7DayInf100k_RKI')
            else:
                bstim_map = update_map_figure(
                    assets_dir, column='7DayInfRaw', normed_to_100k=False)
                rki_map = update_map_figure(
                    assets_dir, column='7DayInf100kRaw_RKI', normed_to_100k=False)
        else:
            if btn_color_100k == 'primary':  # 100k is selected
                bstim_map = update_map_figure(assets_dir, column='newInf100k')
                rki_map = update_map_figure(assets_dir, column='newInf100k_RKI')
            else:
                bstim_map = update_map_figure(
                    assets_dir, column='newInfRaw', normed_to_100k=False)
                rki_map = update_map_figure(
                    assets_dir, column='newInf100kRaw_RKI', normed_to_100k=False)
        return bstim_map, rki_map

    # Update dropbox value
    app.callback(
        Output(f"pos_control_{side}_variable", 'value'),
        [Input(f"rki_map_tab_{side}_graph", 'clickData'),
         Input(f"bstim_map_tab_{side}_graph", 'clickData')]
    )(update_mapclick)