import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import pandas as pd

from app import app, asset_url, counties_metadf, init_countyid
from callbacks.logging import setup_logger
from dash.dependencies import Input, Output
from datetime import datetime as dt, timedelta
from plotly_figures import curves


logger = setup_logger()


# Change dropbox value on map-click
@app.callback(
    Output(component_id='pos_control_left_variable', component_property='value'),
    [Input(component_id='rki_map_tab_left_graph', component_property='clickData'),
     Input(component_id='bstim_map_tab_left_graph', component_property='clickData')]
)
def update_mapclick(choro1_click, choro2_click):
    ctx = dash.callback_context
    if not ctx.triggered:
        id_str = init_countyid
    else:
        cid = ctx.triggered[0]['value']['points'][0]['location']
        id_str = counties_metadf['cca'][cid]
    return int(id_str)

@app.callback(
    Output(component_id='pos_control_right_variable', component_property='value'),
    [Input(component_id='rki_map_tab_right_graph', component_property='clickData'),
     Input(component_id='bstim_map_tab_right_graph', component_property='clickData')]
)
def update_mapclick(choro1_click, choro2_click):
    ctx = dash.callback_context
    if not ctx.triggered:
        id_str = init_countyid
    else:
        cid = ctx.triggered[0]['value']['points'][0]['location']
        id_str = counties_metadf['cca'][cid]
    return int(id_str)


# Callback plots
def update_plot(value, assets_dir, column_dict):
    threshhold_date = os.getenv('THRESHHOLD_DATE')    
    if threshhold_date is not None:
        threshhold_date = dt.strptime(threshhold_date, '%Y_%m_%d')
        selected_date = dt.strptime(assets_dir, '%Y_%m_%d/')
        if selected_date <= threshhold_date:
            assets_dir = (selected_date - timedelta(days=25)).strftime('%Y_%m_%d') + "/"
            img_path = "figures/" + assets_dir + "curve_trend_{0:05d}.png".format(value)
            logger.debug("Update plot: Looking for {}".format(img_path))
            if os.path.isfile(os.path.join('assets', img_path)):
                img = html.Img(
                    src=asset_url+img_path,
                    style={'width': '100%', 'height': '100%'},
                )
            else:
                img = html.Img(
                    src=asset_url+"placeholders/plot_not_found.png",
                    style={'width': '100%', 'height': '100%'},
                )
                logger.debug("Could not find {}. Falling back to {}".format(
                    img_path, asset_url+"placeholders/plot_not_found.png"))
            return img, img
    
    try:
        logger.debug("Update plot: Looking for assets/csv/{0}{1:05d}.csv".format(
            assets_dir, value))
        df_curve = pd.read_csv('assets/csv/{0}{1:05d}.csv'.format(assets_dir, value))
    except FileNotFoundError:
        img = html.Img(
            src=asset_url+"placeholders/plot_not_found.png",
            style={'width': '100%', 'height': '100%'},
        )
        logger.debug("Could not find assets/csv/{0}{1:05d}.csv. Falling back to {2}".format(
            assets_dir, value, asset_url+"placeholders/plot_not_found.png"))
        return img, img
    
    fig = curves.plotit(df_curve, column_dict)
    fig_fixedrange = curves.plotit(df_curve, column_dict, fixedrange=True,)
    curves.minimize(fig_fixedrange)

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


# Plot geglättet
@app.callback(
    [Output(component_id='geglaettet_left_img', component_property='children'),
     Output(component_id='geglaettet_left_modal_img', component_property='children')],
    [Input(component_id='pos_control_left_variable', component_property='value'),
     Input(component_id='date_picker_left_output_container', component_property='children')])
def update_geglaettet_left_img(value, assets_dir):
    return update_plot(value, assets_dir, curves.column_dict_trend)

@app.callback(
    [Output(component_id='geglaettet_right_img', component_property='children'),
     Output(component_id='geglaettet_right_modal_img', component_property='children')],
    [Input(component_id='pos_control_right_variable', component_property='value'),
     Input(component_id='date_picker_right_output_container', component_property='children')])
def update_geglaettet_right_img(value, assets_dir):
    return update_plot(value, assets_dir, curves.column_dict_trend)


# Plot ungeglättet
@app.callback(
    [Output(component_id='ungeglaettet_left_img', component_property='children'),
     Output(component_id='ungeglaettet_left_modal_img', component_property='children')],
    [Input(component_id='pos_control_left_variable', component_property='value'),
     Input(component_id='date_picker_left_output_container', component_property='children')])
def update_ungeglaettet_left_img(value, assets_dir):
    return update_plot(value, assets_dir, curves.column_dict_raw)

@app.callback(
    [Output(component_id='ungeglaettet_right_img', component_property='children'),
     Output(component_id='ungeglaettet_right_modal_img', component_property='children')],
    [Input(component_id='pos_control_right_variable', component_property='value'),
     Input(component_id='date_picker_right_output_container', component_property='children')])
def update_ungeglaettet_right_img(value, assets_dir):
    return update_plot(value, assets_dir, curves.column_dict_raw)

    
# Callbacks meta-information
def update_pos_txt(value, assets_dir):
    msg = " "
    if value is not None:
        try:
            mdat = pd.read_csv("./assets/figures/" + assets_dir + "/metadata.csv")
            msg = mdat.loc[mdat['countyID'] == value]['probText'].to_string(index=False)
            try:
                val = float(msg)
                absVal = abs(val)
                if val<0.0:
                    if 95.0 < absVal <= 100.0:
                        msg = 'Es gibt eine deutliche Tendenz von **fallenden** Infektionszahlen mit einer Wahrscheinlichkeit von grösser **95%**.'
                    elif 75.0 < absVal <= 95.0:
                        msg = 'Es gibt eine Tendenz von **fallenden** Infektionszahlen mit einer Wahrscheinlichkeit von grösser **75%**.'
                    elif 50.0 < absVal <= 75.0:
                        msg = 'Es gibt eine Tendenz von **fallenden** Infektionszahlen mit einer Wahrscheinlichkeit von grösser **50%**.'
                    else:
                        msg = 'Die Infektionszahlen werden mit einer Wahrscheinlichkeit von **{:.1f}%** fallen.'.format(absVal)
                else:
                    if 95.0 < absVal <= 100.0:
                        msg = 'Es gibt eine deutliche Tendenz von **steigenden** Infektionszahlen mit einer Wahrscheinlichkeit von grösser **95%**.'
                    elif 75.0 < absVal <= 95.0:
                        msg = 'Es gibt eine Tendenz von **steigenden** Infektionszahlen mit einer Wahrscheinlichkeit von grösser **75%**.'
                    elif 50.0 < absVal <= 75.0:
                        msg = 'Es gibt eine Tendenz von **steigenden** Infektionszahlen mit einer Wahrscheinlichkeit von grösser **50%**.'
                    else:
                        msg = 'Die Infektionszahlen werden mit einer Wahrscheinlichkeit von **{:.1f}%** fallen.'.format(absVal)
            except:
                print("Exception in update_right_pos_txt")
                pass
        except:
            pass
    return msg, msg

# Print meta-information
@app.callback(
    [Output(component_id='geglaettet_left_txt', component_property='children'),
     Output(component_id='ungeglaettet_left_txt', component_property='children')],
    [Input(component_id='pos_control_left_variable', component_property='value'),
     Input(component_id='date_picker_left_output_container', component_property='children')])
def update_left_pos_txt(value, assets_dir):
    return update_pos_txt(value, assets_dir)

@app.callback(
    [Output(component_id='geglaettet_right_txt', component_property='children'),
     Output(component_id='ungeglaettet_right_txt', component_property='children')],
    [Input(component_id='pos_control_right_variable', component_property='value'),
     Input(component_id='date_picker_right_output_container', component_property='children')])
def update_right_pos_txt(value, assets_dir):
    return update_pos_txt(value, assets_dir)