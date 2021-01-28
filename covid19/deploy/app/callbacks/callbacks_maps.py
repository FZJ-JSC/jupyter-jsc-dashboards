import dash
import pandas as pd

from dash.dependencies import Input, Output
from datetime import datetime as dt
from plotly_figures.maps import create_map_figure

from app import app, cache, cache_timeout
from app import get_assets_datadir, init_countyid
from app import counties_geojson, counties_metadf, n_people_df
from app import threshold_date
from callbacks.logging import setup_logger


logger = setup_logger()


def update_map_figure(assets_dir, column, zmax=None,
                      seven_days=False, incidence_values=False):
    selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
    assets_datadir = get_assets_datadir(selected_date)
    mapcsv_path = "assets/" + assets_datadir + "map.csv"
    logger.debug("Update map: Looking for {}".format(mapcsv_path))
    mapfig = create_map_figure(
        counties_geojson, counties_metadf, mapcsv_path, 
        column=column, n_people=n_people_df,
        seven_days=seven_days, incidence_values=incidence_values,
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
        [Input(f"toggle_{side}_incidence", 'color'),
         Input(f"toggle_{side}_7_days_switch", 'on'),
         Input(f"date_picker_{side}_output_container", 'children')],
    )
    @cache.memoize(timeout=cache_timeout)
    def update_maps(btn_color_incidence, switch_value, assets_dir):
        selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
        if (threshold_date is not None) and (selected_date <= threshold_date):
            bstim_map = update_map_figure(
                assets_dir, column='newInf100k', incidence_values=False, zmax=100)
            rki_map = update_map_figure(
                assets_dir, column='newInf100k_RKI', incidence_values=False)
            return bstim_map, rki_map

        if btn_color_incidence == 'primary':  # incidence values selected
            if not switch_value:  # 7 day values selected
                bstim_map = update_map_figure(
                    assets_dir, column='7DayInf100k', 
                    seven_days=True, incidence_values=True, zmax=250)
                rki_map = update_map_figure(
                    assets_dir, column='7DayInf100k_RKI',
                    seven_days=True, incidence_values=True, zmax=250)
            else:  # per day values selected
                bstim_map = update_map_figure(
                    assets_dir, column='newInf100k', 
                    incidence_values=True, zmax=100)
                rki_map = update_map_figure(
                    assets_dir, column='newInf100k_RKI', 
                    incidence_values=True, zmax=100)

        else:  # Number of cases selected
            if not switch_value:   # 7 day values selected
                bstim_map = update_map_figure(
                    assets_dir, column='7DayInfRaw', seven_days=True)
                try:
                    rki_map = update_map_figure(
                        assets_dir, column='7DayInfRaw_RKI', seven_days=True)
                except KeyError:
                    rki_map = update_map_figure(
                        assets_dir, column='7DayInf100kRaw_RKI', seven_days=True)
            else:  # per day values selected
                bstim_map = update_map_figure(assets_dir, column='newInfRaw')
                try:
                    rki_map = update_map_figure(assets_dir, column='newInfRaw_RKI')
                except KeyError:
                    rki_map = update_map_figure(assets_dir, column='newInf100kRaw_RKI')
        return bstim_map, rki_map

    # Update dropbox value
    app.callback(
        Output(f"pos_control_{side}_variable", 'value'),
        [Input(f"rki_map_tab_{side}_graph", 'clickData'),
         Input(f"bstim_map_tab_{side}_graph", 'clickData')]
    )(update_mapclick)