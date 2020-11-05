import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from app import app, asset_url, init_countyid
from dash.dependencies import Input, Output, State
from plotly_figures.curves import *


# Change dropbox value on map-click
@app.callback(
    Output(component_id='pos_control_variable', component_property='value'),
    [Input(component_id='rki_map_tab_graph', component_property='clickData'),
     Input(component_id='bstim_map_tab_graph', component_property='clickData')]
)
def update_mapclick(choro1_click, choro2_click):
    ctx = dash.callback_context
    if not ctx.triggered:
        id_str = init_countyid
    else:
        cid = ctx.triggered[0]['value']['points'][0]['location']
        id_str = counties_metadf['cca'][cid]
    return int(id_str)


# Plot geglättet
@app.callback(
    [Output(component_id='geglaettet_img', component_property='children'),
     Output(component_id='geglaettet_modal_img', component_property='children')],
    [Input(component_id='pos_control_variable', component_property='value'),
     Input(component_id='date_picker_output_container', component_property='children')])
def update_geglaettet_img(value, assets_dir):
    try:
        df_curve = pd.read_csv('assets/csv/{0}{1:05d}.csv'.format(assets_dir, value))
    except FileNotFoundError:
        img = html.Img(
            src=asset_url+"placeholders/plot_not_found.png",
            style={'width': '100%', 'height': '100%'},
        )
        return img, img
    
    fig_trend = plotly_curves.plotit(df_curve, plotly_curves.column_dict_trend)
    fig_trend_fixedrange = plotly_curves.plotit(
        df_curve, plotly_curves.column_dict_trend, 
        fixedrange=True,
    )
    plotly_curves.minimize(fig_trend_fixedrange)
    
    graph_small = dcc.Graph(
        figure=fig_trend_fixedrange,
        config={
            'modeBarButtonsToRemove': [
                'select2d', 'lasso2d', 'toggleSpikelines'
            ], 
            'displaylogo': False
        },
        style={'width': '100%', 'height': '300px'}
    )    
    graph =  dcc.Graph(
        figure=fig_trend,
        style={'width': '100%', 'height': '100%'},
        config={
            'displayModeBar': True, 
            'staticPlot': False, 
            'responsive': True,
            'modeBarButtonsToRemove': ['autoScale2d', 'toggleSpikelines']
        }
    )
    return graph_small, graph


# Plot ungeglättet
@app.callback(
   [Output(component_id='ungeglaettet_img', component_property='children'),
     Output(component_id='ungeglaettet_modal_img', component_property='children')],
    [Input(component_id='pos_control_variable', component_property='value'),
     Input(component_id='date_picker_output_container', component_property='children')])
def update_ungeglaettet_img(value, assets_dir):
    try:
        df_curve = pd.read_csv('assets/csv/{0}{1:05d}.csv'.format(assets_dir, value))
    except FileNotFoundError:
        img = html.Img(
            src=asset_url+"placeholders/plot_not_found.png",
            style={'width': '100%', 'height': '100%'},
        )
        return img, img
    
    fig_raw = plotly_curves.plotit(df_curve, plotly_curves.column_dict_raw)
    fig_raw_fixedrange = plotly_curves.plotit(
        df_curve, plotly_curves.column_dict_raw, 
        fixedrange=True,
    )
    plotly_curves.minimize(fig_raw_fixedrange)
    
    graph_small = dcc.Graph(
        figure=fig_raw_fixedrange,
        config={
            'modeBarButtonsToRemove': [
                'select2d', 'lasso2d', 'toggleSpikelines'
            ], 
            'displaylogo': False
        },
        style={'width': '100%', 'height': '300px'}
    )    
    graph =  dcc.Graph(
        figure=fig_raw,
        style={'width': '100%', 'height': '100%'},
        config={
            'displayModeBar': True, 
            'staticPlot': False, 
            'responsive': True,
            'modeBarButtonsToRemove': ['autoScale2d', 'toggleSpikelines']
        }
    )
    return graph_small, graph


# Plot 7 Tage Inzidenz
@app.callback(
    [Output(component_id='inzidenz_img', component_property='children'),
     Output(component_id='inzidenz_modal_img', component_property='children')],
    [Input(component_id='pos_control_variable', component_property='value'),
     Input(component_id='date_picker_output_container', component_property='children')])
def update_inzidenz_img(value, assets_dir):
    try:
        df_curve = pd.read_csv('assets/csv/{0}{1:05d}.csv'.format(assets_dir, value))
    except FileNotFoundError:
        img = html.Img(
            src=asset_url+"placeholders/plot_not_found.png",
            style={'width': '100%', 'height': '100%'},
        )
        return img, img
    
    try:
        fig_inzidenz = plotly_curves.plotit(
            df_curve, plotly_curves.column_dict_7days,
            rki=False, sevendays=True
        )
        fig_inzidenz_fixedrange = plotly_curves.plotit(
            df_curve, plotly_curves.column_dict_7days, 
            rki=False, sevendays=True, fixedrange=True,
        )
        plotly_curves.minimize(fig_inzidenz_fixedrange)
    except KeyError:
        img = html.Img(
            src=asset_url+"placeholders/plot_not_found.png",
            style={'width': '100%', 'height': '100%'},
        )
        return img, img
    
    graph_small = dcc.Graph(
        figure=fig_inzidenz_fixedrange,
        config={
            'modeBarButtonsToRemove': [
                'select2d', 'lasso2d', 'toggleSpikelines'
            ], 
            'displaylogo': False
        },
        style={'width': '100%', 'height': '300px'}
    )    
    graph =  dcc.Graph(
        figure=fig_inzidenz,
        style={'width': '100%', 'height': '100%'},
        config={
            'displayModeBar': True, 
            'staticPlot': False, 
            'responsive': True,
            'modeBarButtonsToRemove': ['autoScale2d', 'toggleSpikelines']
        }
    )
    return graph_small, graph


# Print meta-information
@app.callback(
    [Output(component_id='geglaettet_txt', component_property='children'),
     Output(component_id='ungeglaettet_txt', component_property='children'),
     Output(component_id='inzidenz_txt', component_property='children')], 
    [Input(component_id='pos_control_variable', component_property='value'),
     Input(component_id='date_picker_output_container', component_property='children')])
def update_left_pos_txt(value, assets_dir):
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
    return msg, msg, msg


