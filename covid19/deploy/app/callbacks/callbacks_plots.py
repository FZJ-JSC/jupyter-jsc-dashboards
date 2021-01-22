import dash_core_components as dcc
import dash_html_components as html
import os
import pandas as pd

from dash.dependencies import Input, Output, State
from datetime import datetime as dt

from app import app, asset_url
from app import fixed_plot_width, fixed_plot_height, threshold_date
from app import get_assets_datadir
from callbacks.logging import setup_logger
from plotly_figures import curves


logger = setup_logger()


def update_plot(value, selected_date, column_dict, smaller_threshold=False):
#     selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
    assets_datadir = get_assets_datadir(selected_date)
    placeholder_img = html.Img(
        src=asset_url + "placeholders/plot_not_found.png",
        style={'width': '100%', 'height': '100%'},
    )

    if smaller_threshold:
        if 'Trend' in column_dict['mean']['column']:
            img_path = assets_datadir + "curve_trend_{0:05d}.png".format(value)
        else:
            img_path = assets_datadir + "curve_{0:05d}.png".format(value)
        logger.debug("Update plot: Looking for {}".format(img_path))
        if os.path.isfile(os.path.join('assets', img_path)):
            img = html.Img(
                src=asset_url + img_path,
                style={'width': '100%', 'height': '100%'},
            )
        else:
            img = placeholder_img
            logger.debug("Could not find {}. Falling back to {}".format(
                img_path, asset_url+"placeholders/plot_not_found.png"))
        return img, img

    try:
        logger.debug("Update plot: Looking for assets/{0}{1:05d}.csv".format(
            assets_datadir, value))
        df_curve = pd.read_csv('assets/{0}{1:05d}.csv'.format(assets_datadir, value))       
    except FileNotFoundError:
        logger.debug("Could not find assets/{0}{1:05d}.csv. Falling back to {2}".format(
            assets_datadir, value, asset_url + "placeholders/plot_not_found.png"))
        return placeholder_img, placeholder_img

#     try:
    fig = curves.plotit(df_curve, column_dict)
    fig_fixedrange = curves.plotit(df_curve, column_dict, fixedrange=True,)
    curves.minimize(fig_fixedrange, width=fixed_plot_width, height=fixed_plot_height)
#     except KeyError:
#         return placeholder_img, placeholder_img

    graph_small = dcc.Graph(
        figure=fig_fixedrange,
        config={
            'modeBarButtonsToRemove': [
                'select2d', 'lasso2d', 'toggleSpikelines'
            ], 
            'displaylogo': False
        },
        style={'width': '100%', 'height': '300px'}
    )
    graph = dcc.Graph(
        figure=fig,
        style={'width': '100%', 'height': '100%'},
        config={
            'displayModeBar': True, 
            'staticPlot': False, 
            'responsive': True,
            'modeBarButtonsToRemove': ['autoScale2d', 'toggleSpikelines']
        }
    )
    return graph_small, graph


# Update meta-information
def update_pos_txt(value, assets_dir):
    msg = " "
    if value is not None:
        try:
            assets_datadir = get_assets_datadir(dt.strptime(assets_dir, '%Y_%m_%d/'))
            metadata_path = "./assets/" + assets_datadir + "/metadata.csv"
            mdat = pd.read_csv(metadata_path)
            # Need to increase column width so that string doesn't get truncated
            pd.set_option('max_colwidth', 100)
            msg = mdat.loc[mdat['countyID'] == value]['probText'].to_string(index=False)
            try:
                val = float(msg)
                absVal = abs(val)
                if val < 0.0:
                    if 95.0 < absVal <= 100.0:
                        msg = 'Es gibt eine deutliche Tendenz von **fallenden** \
                        Infektionszahlen mit einer Wahrscheinlichkeit \
                        von grösser **95%**.'
                    elif 75.0 < absVal <= 95.0:
                        msg = 'Es gibt eine Tendenz von **fallenden** \
                        Infektionszahlen mit einer Wahrscheinlichkeit \
                        von grösser **75%**.'
                    elif 50.0 < absVal <= 75.0:
                        msg = 'Es gibt eine Tendenz von **fallenden** \
                        Infektionszahlen mit einer Wahrscheinlichkeit \
                        von grösser **50%**.'
                    else:
                        msg = 'Die Infektionszahlen werden mit einer \
                        Wahrscheinlichkeit von **{:.1f}%** fallen.'.format(absVal)
                else:
                    if 95.0 < absVal <= 100.0:
                        msg = 'Es gibt eine deutliche Tendenz von \
                        **steigenden** Infektionszahlen mit einer \
                        Wahrscheinlichkeit von grösser **95%**.'
                    elif 75.0 < absVal <= 95.0:
                        msg = 'Es gibt eine Tendenz von \
                        **steigenden** Infektionszahlen mit einer \
                        Wahrscheinlichkeit von grösser **75%**.'
                    elif 50.0 < absVal <= 75.0:
                        msg = 'Es gibt eine Tendenz von \
                        **steigenden** Infektionszahlen mit einer \
                        Wahrscheinlichkeit von grösser **50%**.'
                    else:
                        msg = 'Die Infektionszahlen werden mit einer \
                        Wahrscheinlichkeit von **{:.1f}%** fallen.'.format(absVal)
            except:
                print("Exception in update_pos_txt")
                msg += '.'
                msg = msg.replace('\\%', '%')
                pass
        except:
            pass
    return msg, msg


for side in ['left', 'right']:
    # Plots geglaettet
    @app.callback(
        [Output(f"geglaettet_{side}_img", 'children'),
         Output(f"geglaettet_{side}_modal_img", 'children'),
         Output(f"ungeglaettet_tab_{side}", 'disabled'),
         Output(f"pos_card_{side}_tabs", 'active_tab')],
        [Input(f"pos_control_{side}_variable", 'value'),
         # When the button color changes, we toggled incidence values
         Input(f"toggle_{side}_7_days_button1", 'color'),
         Input(f"toggle_{side}_100k_button1", 'color'),
         Input(f"date_picker_{side}_output_container", 'children')],
        State(f"pos_card_{side}_tabs", 'active_tab')
    )
    def update_geglaettet(value, btn_color_7_days, btn_color_100k,
                          assets_dir, current_active_tab):
        selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
        if (threshold_date is not None) and (selected_date <= threshold_date):
            plots = update_plot(value, selected_date, curves.column_dict_trend, 
                                smaller_threshold=True)
            return plots + (False, current_active_tab)

        if btn_color_7_days == 'primary':  # 7 day incidence is selected
            if btn_color_100k == 'primary':  # 100k is selected
                plots = update_plot(value, selected_date, curves.column_dict_7days_100k)
            else:
                plots = update_plot(value, selected_date, curves.column_dict_7days)
            return plots + (True, 'tab-0')  # Disable 2nd tab and switch to 1st

        if btn_color_100k == 'primary':  # 100k is selected
            plots = update_plot(value, selected_date, curves.column_dict_trend_100k)
        else:
            plots = update_plot(value, selected_date, curves.column_dict_trend)
        return plots + (False, current_active_tab)  # Enable 2nd tab

    # Plots ungeglaettet
    @app.callback(
        [Output(f"ungeglaettet_{side}_img", 'children'),
         Output(f"ungeglaettet_{side}_modal_img", 'children')],
        [Input(f"pos_control_{side}_variable", 'value'),
         Input(f"toggle_{side}_100k_button1", 'color'),
         Input(f"date_picker_{side}_output_container", 'children')]
    )
    def update_ungeglaettet(value, btn_color_100k, assets_dir):
        selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
        if (threshold_date is not None) and (selected_date <= threshold_date):
            plots = update_plot(value, selected_date, curves.column_dict_raw,
                                smaller_threshold=True)
            return plots

        if btn_color_100k == 'primary':  # 100k is selected
            plots = update_plot(value, selected_date, curves.column_dict_raw_100k)
        else:
            plots = update_plot(value, selected_date, curves.column_dict_raw)
        return plots

    # Update meta-information
    app.callback(
        [Output(f"geglaettet_{side}_txt", 'children'),
         Output(f"ungeglaettet_{side}_txt", 'children')],
        [Input(f"pos_control_{side}_variable", 'value'),
         Input(f"date_picker_{side}_output_container", 'children')]
    )(update_pos_txt)