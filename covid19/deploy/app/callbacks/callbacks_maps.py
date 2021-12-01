import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from dash.dependencies import Input, Output, State
from datetime import datetime as dt

from app import app, cache, cache_timeout
from app import get_assets_datadir, init_countyid
from app import counties_geojson, counties_metadf, n_people_df
from app import threshold_date
from callbacks.logging import setup_logger
from plotly_figures.maps import create_map_figure

logger = setup_logger()

def calculate_daily_zmax_values(assets_dir):
    columns = [
        '7DayInf100k', 'newInf100k', '7DayInfRaw', 'newInfRaw',
        '7DayInf100k_RKI', 'newInf100k_RKI', '7DayInfRaw_RKI', 'newInfRaw_RKI'
    ]

    zmax_dict = {col: 0 for col in columns}

    selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
    assets_datadir = get_assets_datadir(selected_date)
    mapcsv_path = "assets/" + assets_datadir + "map.csv"
    mapcsv = pd.read_csv(mapcsv_path)

    for column in columns:
        # Get no. infections for each county from mapcsv 
        for feat in counties_geojson['features']:
            # Need the county id to find the corresponding value in mapcsv
            cca_str = feat['properties'].get('RS')
            if cca_str is not None:
                try:
                    cca_filtered_df = mapcsv.loc[mapcsv['countyID']==int(cca_str), column]
                except KeyError as e:
                    if e.args[0] == '7DayInfRaw_RKI':
                        cca_filtered_df = mapcsv.loc[mapcsv['countyID']==int(cca_str), '7DayInf100kRaw_RKI']
                    elif e.args[0] == 'newInfRaw_RKI':
                        cca_filtered_df = mapcsv.loc[mapcsv['countyID']==int(cca_str), 'newInf100kRaw_RKI']
                cca_value = next(iter(cca_filtered_df), 0.0)
                if cca_value > zmax_dict[column]:
                    zmax_dict[column] = cca_value

    if zmax_dict['7DayInf100k'] > zmax_dict['7DayInf100k_RKI']:
        zmax_dict['7DayInf100k_RKI'] = zmax_dict['7DayInf100k']
    else:
        zmax_dict['7DayInf100k'] = zmax_dict['7DayInf100k_RKI']

    if zmax_dict['newInf100k'] > zmax_dict['newInf100k_RKI']:
        zmax_dict['newInf100k_RKI'] = zmax_dict['newInf100k']
    else:
        zmax_dict['newInf100k'] = zmax_dict['newInf100k_RKI']

    if zmax_dict['7DayInfRaw'] > zmax_dict['7DayInfRaw_RKI']:
        zmax_dict['7DayInfRaw_RKI'] = zmax_dict['7DayInfRaw']
    else:
        zmax_dict['7DayInfRaw'] = zmax_dict['7DayInfRaw_RKI']

    if zmax_dict['newInfRaw'] > zmax_dict['newInfRaw_RKI']:
        zmax_dict['newInfRaw_RKI'] = zmax_dict['newInfRaw']
    else:
        zmax_dict['newInfRaw'] = zmax_dict['newInfRaw_RKI']

    return zmax_dict


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
    # Change the children attribute of the dummy divs
    # when the user selects a change.
    # Maps will update after the dummy divs children have updated. 
    @app.callback(
        [Output(f"rki_map_tab_{side}_dummy_div", 'children'),
         Output(f"bstim_map_tab_{side}_dummy_div", 'children')],
        [Input(f"date_card_{side}_tabs", 'active_tab'),
         Input(f"toggle_{side}_incidence", 'color'),
         Input(f"toggle_{side}_7_days_switch", 'on'),
         Input(f"date_picker_{side}_output_container", 'children')],
        [State(f"rki_map_tab_{side}_dummy_div", 'children'),
         State(f"bstim_map_tab_{side}_dummy_div", 'children')],
    )
    def update_dummy_div(active_tab, color, switch, date, tab_0, tab_1):
        ctx = dash.callback_context
        # We switched between bstim and rki tab
        if ctx.triggered[0]['prop_id'].endswith('active_tab'):
            if active_tab == 'tab-0':
                if tab_0 == 'tab-0':  # Tab has already been rendered
                    return dash.no_update
                return 'tab-0', dash.no_update
            if active_tab == 'tab-1':
                if tab_1 == 'tab-1': # Tab has already been rendered
                    return dash.no_update
                return dash.no_update, 'tab-1'
        
        # If the selection of incidence or 7 day values changed,
        # we update both tabs to force a rerender ('' for empty graph)
        if active_tab == 'tab-0':
            return 'tab-0', ''
        if active_tab == 'tab-1':
            return '', 'tab-1'

    
    # Calculate daily zmax_values and save them in hidden div
    @app.callback(
        Output(f"zmax_values_{side}", 'data'),
        Input(f"date_picker_{side}_output_container", 'children')
    )
    @cache.memoize(timeout=cache_timeout)
    def update_zmax_values(assets_dir):
        return calculate_daily_zmax_values(assets_dir)


    # Update map figure
    @app.callback(
        Output(f"bstim_map_tab_{side}_graph", 'figure'),
        # When the button color changes, we toggled incidence values
        Input(f"bstim_map_tab_{side}_dummy_div", 'children'),
        Input(f"zmax_values_{side}", 'data'),
        [State(f"toggle_{side}_incidence", 'color'),
         State(f"toggle_{side}_7_days_switch", 'on'),
         State(f"date_picker_{side}_output_container", 'children')],
    )
    @cache.memoize(timeout=cache_timeout)
    def update_bstim_maps(dummy_div, zmax_values, btn_color_incidence, switch_value, assets_dir):
        if dummy_div == '':
            # Return an empty graph to prevent briefly seeing old map
            return {
                "layout": {
                    "xaxis": {
                        "visible": False
                    },
                    "yaxis": {
                        "visible": False
                    },
                    "height": 450
                }
            }

        selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
        if (threshold_date is not None) and (selected_date <= threshold_date):
            bstim_map = update_map_figure(
                assets_dir, column='newInf100k', incidence_values=False, 
                zmax=zmax_values['newInf100k'])
            return bstim_map

        if btn_color_incidence == 'primary':  # incidence values selected
            if not switch_value:  # 7 day values selected
                bstim_map = update_map_figure(
                    assets_dir, column='7DayInf100k', seven_days=True, 
                    incidence_values=True, zmax=zmax_values['7DayInf100k'])
            else:  # per day values selected
                bstim_map = update_map_figure(
                    assets_dir, column='newInf100k', 
                    incidence_values=True, zmax=zmax_values['newInf100k'])

        else:  # Number of cases selected
            if not switch_value:   # 7 day values selected
                bstim_map = update_map_figure(
                    assets_dir, column='7DayInfRaw', seven_days=True, zmax=zmax_values['7DayInfRaw'])
            else:  # per day values selected               
                bstim_map = update_map_figure(
                    assets_dir, column='newInfRaw', zmax=zmax_values['newInfRaw'])
        return bstim_map
        

    # Update map figure
    @app.callback(
         Output(f"rki_map_tab_{side}_graph", 'figure'),
        # When the button color changes, we toggled incidence values
        Input(f"rki_map_tab_{side}_dummy_div", 'children'),
        Input(f"zmax_values_{side}", 'data'),
        [State(f"toggle_{side}_incidence", 'color'),
         State(f"toggle_{side}_7_days_switch", 'on'),
         State(f"date_picker_{side}_output_container", 'children')],
    )
    @cache.memoize(timeout=cache_timeout)
    def update_rki_maps(dummy_div, zmax_values, btn_color_incidence, switch_value, assets_dir):
        if dummy_div == '':
            # Return an empty graph to prevent briefly seeing old map
            return {
                "layout": {
                    "xaxis": {
                        "visible": False
                    },
                    "yaxis": {
                        "visible": False
                    },
                    "height": 450
                }
            }
        
        selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
        if (threshold_date is not None) and (selected_date <= threshold_date):
            rki_map = update_map_figure(
                assets_dir, column='newInf100k_RKI', incidence_values=False, 
                zmax=zmax_values['newInf100k_RKI'])
            return bstim_map, rki_map

        if btn_color_incidence == 'primary':  # incidence values selected
            if not switch_value:  # 7 day values selected
                rki_map = update_map_figure(
                    assets_dir, column='7DayInf100k_RKI',
                    seven_days=True, incidence_values=True, zmax=zmax_values['7DayInf100k_RKI'])
            else:  # per day values selected
                rki_map = update_map_figure(
                    assets_dir, column='newInf100k_RKI', 
                    incidence_values=True, zmax=zmax_values['newInf100k_RKI'])

        else:  # Number of cases selected
            if not switch_value:   # 7 day values selected
                try:
                    rki_map = update_map_figure(
                        assets_dir, column='7DayInfRaw_RKI', seven_days=True, 
                        zmax=zmax_values['7DayInfRaw_RKI'])
                except KeyError:
                    rki_map = update_map_figure(
                        assets_dir, column='7DayInf100kRaw_RKI', seven_days=True, 
                        zmax=zmax_values['7DayInfRaw_RKI'])
            else:  # per day values selected
                try:
                    rki_map = update_map_figure(assets_dir, column='newInfRaw_RKI', 
                    zmax=zmax_values['newInfRaw_RKI'])
                except KeyError:
                    rki_map = update_map_figure(assets_dir, column='newInf100kRaw_RKI', 
                    zmax=zmax_values['newInfRaw_RKI'])
        return rki_map
            

    # Update scale text
    @app.callback(
        Output(f"card_separator_{side}", 'children'),
        Input(f"toggle_{side}_incidence", 'color'),
        Input(f"toggle_{side}_7_days_switch", 'on'),
        Input(f"zmax_values_{side}", 'data')
    )
    def update_scale_text(btn_color_incidence, switch_value, zmax_values):
        if zmax_values == None:
            return ''

        if btn_color_incidence == 'primary':  # incidence values selected
            if not switch_value:  # 7 day values selected
                zmax = zmax_values['7DayInf100k']
            else:  # per day values selected
                zmax = zmax_values['newInf100k']
        else:  # Number of cases selected
            if not switch_value:  # 7 day values selected
                zmax = zmax_values['7DayInfRaw']
            else:  # per day values selected
                zmax = zmax_values['newInfRaw']
        zmax = (zmax + 90) // 100 * 100
        return html.Small(f"Skala variiert - aktuell: 0 bis {int(zmax)}")

    
    # Update dropbox value
    app.callback(
        Output(f"pos_control_{side}_variable", 'value'),
        [Input(f"rki_map_tab_{side}_graph", 'clickData'),
         Input(f"bstim_map_tab_{side}_graph", 'clickData')]
    )(update_mapclick)

