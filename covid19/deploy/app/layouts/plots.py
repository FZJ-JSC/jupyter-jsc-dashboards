import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from plotly_figures.curves import *


def create_plot_modal(type_):
    return html.Div([
        dbc.Button(
            "Vergrößern", 
            id='{}_modal_open'.format(type_), 
            outline=True, 
            color='secondary', 
            className='mr-1'),
        dbc.Modal(
            id='{}_modal'.format(type_),
            size='xl',
            children=[
                dbc.ModalHeader(type_),
                dbc.ModalBody( 
                    id='{}_modal_img'.format(type_),
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Schließen", 
                        id='{}_modal_close'.format(type_), 
                        className='ml-auto')
                ),
            ]
        ),   
    ]) 


def create_plot_tab(type_, tooltip):
    return dbc.Card(
        outline=True,
        color='light',
        className='mt-3',
        children=[ 
            dbc.CardBody([
                html.Div(
                    id='{}_img_div'.format(type_),
                    children=[
                        create_plot_modal(type_),
                        dcc.Loading(
                            id='{}_loading_img'.format(type_), 
                            children=[
                                html.Div(id='{}_img'.format(type_)),
                            ],
                            type='circle', # 'graph', 'cube', 'circle', 'dot', 'default'
                            color='#343A40',
                            style={'height': '600px'},
                        ),  
                        html.Div(
                            dcc.Markdown(
                                id='{}_txt'.format(type_),
                                children=[''],
                            )
                        ),
                        dbc.Tooltip(
                            tooltip,
                            target='{}_img'.format(type_),
                            style={'width': '600px'},
                            placement='left',
                        ),
                    ]),
            ]),
        ])


# Geglättet
with open('txt/plot_tooltip_trend.md') as md_file:
    geglaettet_tab_tooltip = md_file.read()
geglaettet_tab_left = create_plot_tab('geglaettet_left', geglaettet_tab_tooltip)
geglaettet_tab_right = create_plot_tab('geglaettet_right', geglaettet_tab_tooltip)


# Ungeglättet
with open('txt/plot_tooltip_raw.md') as md_file:
    ungeglaettet_tab_tooltip = md_file.read()
ungeglaettet_tab_left = create_plot_tab('ungeglaettet_left', ungeglaettet_tab_tooltip)
ungeglaettet_tab_right = create_plot_tab('ungeglaettet_right', ungeglaettet_tab_tooltip)
