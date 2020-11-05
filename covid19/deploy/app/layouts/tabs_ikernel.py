import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import app
from dash.dependencies import Input, Output, State


def create_interpretation_help(no, markdown):
    return html.Div([
        dbc.Modal(
            id='ikernel_inter{}_modal'.format(no),
            size='xl',
            children=[
                dbc.ModalHeader("Interpretationshilfe"),
                dbc.ModalBody([
                    dbc.Col(
                        html.Img(
                            src=asset_url+"ikernel-{}.png".format(no),
                            style={'width':'80%', 'height':'80%'},
                        ),
                        width={'size': 4, 'offset': 8},
                    ),   
                    dcc.Markdown(markdown),
                ]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Schließen", 
                        id='ikernel_inter{}_modal_close'.format(no), 
                        className='ml-auto'
                    )
                ),
            ]
        ),
])


def create_inter_help_columns(no):
    return dbc.Col(
        html.Div(
            id='ikernel_inter{}_div'.format(no),
            children=[
                html.Img(
                    id='ikernel_inter{}'.format(no),
                    src=asset_url+"ikernel-{}-border.png".format(no),
                    style={'width': '80%', 'height': '80%'},
                ),
            ],
        ),
        width={'size': 3, 'offset': 1},
    )


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


# Modal large view of kernel
ikernel_tab_modal = html.Div([
    dbc.Button(
        "Vergrößern", 
        id='ikernel_tab_modal_open', 
        outline=True, 
        color='secondary', 
        className='mr-1'),
    dbc.Modal(
        id='ikernel_tab_modal',
        size='xl',
        children=[
            dbc.ModalHeader("Interaktionskernel"),
            dbc.ModalBody([
                html.Img(
                    id='ikernel_tab_modal_img',
                    src=asset_url+"figures/"+init_date.strftime('%Y_%m_%d')+"/interaction_kernel.png",
                    style={'width': '100%', 'height': '100%'},
                ),
            ]),
            dbc.ModalFooter(
                dbc.Button(
                    "Schließen", 
                    id='ikernel_tab_modal_close', 
                    className='ml-auto')
            ),
        ],
    ),
]) 


# Ikernel Tab
ikernel_tab = dbc.Card(
    outline=True,
    color="light",
    className="mt-3",    
    children=[ 
        dbc.CardBody([
            html.Div(
                id='ikernel_tab_img_div',
                children=[
                    ikernel_tab_modal,
                    dcc.Loading(
                        id='ikernel_tab_loading_img', 
                        children=[
                            html.Img(
                                id="ikernel_tab_img",
                                src=asset_url + "figures/" + init_date.strftime('%Y_%m_%d') + "/interaction_kernel.png",
                                style={'width': '100%', 'height': '100%'},
                            ),
                        ],
                        type='circle', # 'graph', 'cube', 'circle', 'dot', 'default'
                        color='#343A40',
                        style={'height': '450px'},
                    ),
                    dbc.Tooltip(
                        ikernel_tab_tooltip,
                        target='ikernel_tab_img',
                        style={'width': '200%'},
                        placement='left',
                    ),
                ]),
            html.Div([
                dbc.Row(
                    dbc.Col(
                        html.Div("Klick ähnliche Darstellung für Interpretationshilfe:"),
                        width={'size': 11, 'offset': 1},
                    )
                ),
                dbc.Row([create_inter_help_columns(i) for i in [1, 2, 3]]),
            ]),
        ]),
    ])