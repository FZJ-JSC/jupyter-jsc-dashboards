import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import app, asset_url, get_assets_datadir, init_date
from dash.dependencies import Input, Output, State
from datetime import datetime as dt


def create_interpretation_help(no, markdown):
    return html.Div([
        dbc.Modal(
            id=f"ikernel_inter{no}_modal",
            size='xl',
            children=[
                dbc.ModalHeader("Interpretationshilfe"),
                dbc.ModalBody([
                    dbc.Col(
                        html.Img(
                            src=asset_url+f"ikernel-{no}.png",
                            style={'width':'80%', 'height':'80%'},
                        ),
                        width={'size': 4, 'offset': 8},
                    ),   
                    dcc.Markdown(markdown),
                ]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Schließen", 
                        id=f"ikernel_inter{no}_modal_close", 
                        className='ml-auto'
                    )
                ),
            ]
        ),
])


def create_inter_help_columns(tab_name, no):
    return dbc.Col(
        html.Div(
            id=f"{tab_name}_inter{no}_div",
            children=[
                html.Img(
                    id=f"{tab_name}_inter{no}",
                    src=asset_url+f"ikernel-{no}-border.png",
                    style={'width': '80%', 'height': '80%'},
                ),
            ],
        ),
        width={'size': 3, 'offset': 1},
    )


# Modal large view of kernel
def create_ikernel_tab_modal_and_tooltip(tab_name, tooltip):
    return dbc.Row([
        # Modal
        dbc.Button(
             html.Span([
                html.I(className="fa fa-search-plus mr-2"),
                "Vergrößern",
            ]),
            id=f"{tab_name}_modal_open", 
            outline=True, 
            color='secondary', 
            className='mr-1'),
        dbc.Modal(
            id=f"{tab_name}_modal",
            size='xl',
            children=[
                dbc.ModalHeader("Interaktionskernel"),
                dbc.ModalBody([
                    html.Img(
                        id=f"{tab_name}_modal_img",
                        src = asset_url + get_assets_datadir(dt(init_date.year, init_date.month, init_date.day)) + "/interaction_kernel.png",
                        style={'width': '100%', 'height': '100%'},
                    ),
                ]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Schließen", 
                        id=f"{tab_name}_modal_close", 
                        className='ml-auto')
                ),
            ],
        ),
        # Tooltip
        html.I(
            className="fa fa-question-circle fa-lg mr-2",
            id=f"{tab_name}_target",
            style={
                'color':'var(--secondary)',
                'align-self': 'center'
            },
        ),
        dbc.Tooltip(
            tooltip, 
            target=f"{tab_name}_target", 
            style = {
                'maxWidth': 600,
                'width': 600
                }
        )
    ])


def create_ikernel_tab(tab_name, tooltip):
    return dbc.Card(
        outline=True,
        color="light",
        className="mt-3",    
        children=[ 
            dbc.CardBody([
                html.Div(
                    id=f"{tab_name}_img_div",
                    children=[
                        create_ikernel_tab_modal_and_tooltip(tab_name, tooltip),
                        dcc.Loading(
                            id=f"{tab_name}_loading_img", 
                            children=[
                                html.Img(
                                    id=f"{tab_name}_img",
                                    src = asset_url + get_assets_datadir(dt(init_date.year, init_date.month, init_date.day)) + "/interaction_kernel.png",
                                    style={'width': '100%', 'height': '100%'},
                                ),
                            ],
                            type='circle', # 'graph', 'cube', 'circle', 'dot', 'default'
                            color='#343A40',
                            style={'height': '450px'},
                        ),
                    ]),
                html.Div([
                    dbc.Row(
                        dbc.Col(
                            html.Div("Klick ähnliche Darstellung für Interpretationshilfe:"),
                            width={'size': 11, 'offset': 1},
                        )
                    ),
                    dbc.Row([create_inter_help_columns(tab_name, i) for i in [1, 2, 3]]),
                ]),
            ]),
        ])


# Interpretation help
with open('txt/ikernel_inter1.md') as md_file:
    ikernel_inter1_md = md_file.read()
ikernel_inter1_modal = create_interpretation_help(1, ikernel_inter1_md)

with open('txt/ikernel_inter2.md') as md_file:
    ikernel_inter2_md = md_file.read()
ikernel_inter2_modal = create_interpretation_help(2, ikernel_inter2_md)

with open('txt/ikernel_inter3.md') as md_file:
    ikernel_inter3_md = md_file.read()
ikernel_inter3_modal = create_interpretation_help(3, ikernel_inter3_md)


# Ikernel Tabs
with open('txt/ikernel_tooltip.txt') as txt_file:
    ikernel_tooltip = txt_file.read()
ikernel_tab_left = create_ikernel_tab('ikernel_tab_left', ikernel_tooltip)
ikernel_tab_right = create_ikernel_tab('ikernel_tab_right', ikernel_tooltip)