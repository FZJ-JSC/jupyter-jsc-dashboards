import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import asset_url
from layouts.top_section import explanations_bstim, explanations_right
from layouts.tabs_map import bstim_map_tab_left, rki_map_tab_left
from layouts.tabs_map import bstim_map_tab_right, rki_map_tab_right
from layouts.tabs_ikernel import ikernel_inter1_modal, ikernel_inter2_modal, ikernel_inter3_modal
from layouts.tabs_ikernel import ikernel_tab_left, ikernel_tab_right
from layouts.plots import geglaettet_tab_left, ungeglaettet_tab_left
from layouts.plots import geglaettet_tab_right, ungeglaettet_tab_right
from layouts.date_picker import date_picker_left, date_picker_right
from layouts.position_controls import pos_controls_left, pos_controls_right


tab_height = '5vh'

with open('assets/warning.txt') as txt_file:
    warning_txt = txt_file.read()

body_layout = dbc.Container(
    style={'marginTop': 100, 'marginBottom': 20},
    children=[
        #####################
        # Introduction
        #####################
        dbc.Row([
            dbc.Col(
                style={
                    'marginBottom': 10,
                    'width': 12,
                },  
                children=[
                    dcc.Markdown(
                        f"""
                        #####  **Ein Gemeinschaftsprojekt der Arbeitsgruppe [Neuroinformatik an der Universität Osnabrück](https://www.ikw.uni-osnabrueck.de/en/research_groups/neuroinformatics)**  
                        #####  **und des [Jülich Supercomputing Centre](https://www.fz-juelich.de/jsc), auf Basis der Daten des [RKI](https://www.rki.de/DE/Content/Infekt/IfSG/Signale/Projekte/Signale_Projekte_node.html;jsessionid=C61DE534E8208B0D69BEAD299FC753F9.internet091)**
                        """
                    ),
                    dbc.Alert(
                        html.H5(warning_txt, className='alert-heading'),
                        color='danger',
                        style={'display': 'block' if warning_txt != '' else 'none'},
                    ),
                ]
            ), 
        ]),
        dbc.Row([
            dbc.Col(
                width=4,
                children=[
                    html.A([
                        html.Img(
                            src=asset_url + "uniosnab-logo.png",
                            height='48', # width='500',
                            style={
                                'display':'block',
                                'margin-left': 'auto',
                                'margin-right': 'auto'
                            },
                        )
                    ], 
                    href='https://www.ikw.uni-osnabrueck.de/en/research_groups/neuroinformatics'),
                ]
            ),
            dbc.Col(width=4), 
            dbc.Col(
                width=4,
                children=[
                    html.A([ 
                        html.Img(
                            src=asset_url + "jsc-logo.png",
                            height='48', # width='500',
                            style={
                                'display':'block',
                                'margin-left': 'auto',
                                'margin-right': 'auto'
                            },
                        ),
                    ], 
                    href='https://www.fz-juelich.de/jsc'),
                ]),
            ]),
        dbc.Row([
            dbc.Col(
                style={
                    'marginTop': 30,
                    'width': 6,
                },
                children=[explanations_bstim]),
            dbc.Col(
                style={
                    'marginTop': 30,
                    'width': 6,
                },
                children=[explanations_right]),
        ]),

        #####################
        # Maps and interaction kernel Section
        #####################
        ikernel_inter1_modal,
        ikernel_inter2_modal,
        ikernel_inter3_modal,

        dbc.Row([
            # Left column
            dbc.Col([
                dbc.Card(
                    style={
                        'margin': '0% 0% 0% 0%', # top, right, bottom, left
                        'padding': '0',
                    },
                    body=True,   
                    children=[
                        # --- Zeitangabe  ---
                        dbc.CardHeader(
                            date_picker_left,
                        ),
                        dbc.CardBody(
                            className='mt-3',
                            children=[
                                dbc.Tabs(
                                    id='date_card_left_tabs',
                                    active_tab='tab-1',
                                        children=[
                                            dbc.Tab(
                                                rki_map_tab_left, 
                                                label="Meldedaten RKI", 
                                                style={'padding': '0', 'height': '450px'}),
                                            dbc.Tab(
                                                bstim_map_tab_left, 
                                                label="Nowcast BSTIM", 
                                                style={'padding': '0', 'height': '450px'}),
                                            dbc.Tab(
                                                ikernel_tab_left,
                                                label="Interaktionskernel", 
                                                style={'padding': '0', 'height': '450px'}),
                                        ]),
                                html.P(
                                    id='card_separator_left',
                                    className='card-text',
                                ),       
                                # Ortsangabe
                                dbc.Card(
                                    style={
                                        'margin': '0% 0% 0% 0%', # top, right, bottom, left
                                        'padding': '0',
                                    },
                                    children=[
                                        dbc.CardHeader(
                                            pos_controls_left,
                                        ),
                                        dbc.CardBody(
                                            className='mt-3',
                                            children=[
                                                dbc.Tabs(
                                                    id='pos_card_left_tabs',
                                                    active_tab='tab-0',
                                                            children=[
                                                                dbc.Tab(
                                                                    geglaettet_tab_left,
                                                                    label="geglättet",
                                                                    style={'padding': '0'} # height': '450px'}
                                                                ), 
                                                                dbc.Tab(
                                                                    ungeglaettet_tab_left,
                                                                    label="ungeglättet",
                                                                    style={'padding': '0'} # height': '450px'}
                                                                ),
                                                            ]),
                                                html.P(
                                                    id='pos_card_left_content',
                                                    className="card-text",
                                                ),
                                            ]),
                                    ]),
                            ]),
                    ]),
            ]),
            # Right column
            dbc.Col([
                dbc.Card(
                    style={
                        'margin': '0% 0% 0% 0%', # top, right, bottom, left
                        'padding': '0',
                    },
                    body=True,
                    children=[
                        # --- Zeitangabe  ---
                        dbc.CardHeader(
                            date_picker_right,
                        ),
                        dbc.CardBody(
                            className='mt-3',
                            children=[
                                dbc.Tabs(
                                    id='date_card_right_tabs',
                                    active_tab='tab-1',
                                        children=[
                                            dbc.Tab(
                                                rki_map_tab_right, 
                                                label="Meldedaten RKI", 
                                                style={'padding': '0', 'height': '450px'}),
                                            dbc.Tab(
                                                bstim_map_tab_right, 
                                                label="Nowcast BSTIM", 
                                                style={'padding': '0', 'height': '450px'}),
                                            dbc.Tab(
                                                ikernel_tab_right, 
                                                label="Interaktionskernel", 
                                                style={'padding': '0', 'height': '450px'}),
                                        ]),
                                html.P(
                                    id='card_separator_right',
                                    className='card-text',
                                ),
                                # Ortsangabe
                                dbc.Card(
                                    style={
                                        'margin': '0% 0% 0% 0%', # top, right, bottom, left
                                        'padding': '0',
                                    },
                                    children=[
                                        dbc.CardHeader(
                                            pos_controls_right,
                                        ),
                                        dbc.CardBody(
                                            className='mt-3',
                                            children=[
                                                dbc.Tabs(
                                                    id='pos_card_right_tabs',
                                                    active_tab='tab-0',
                                                            children=[
                                                                dbc.Tab(
                                                                    geglaettet_tab_right, 
                                                                    label="geglättet",    
                                                                    style={'padding': '0'} # height': '450px'}
                                                                ), 
                                                                dbc.Tab(
                                                                    ungeglaettet_tab_right, 
                                                                    label="ungeglättet",  
                                                                    style={'padding': '0'} # height': '450px'}
                                                                ),
                                                            ]),
                                                html.P(
                                                    id='pos_card_right_content',
                                                    className="card-text",
                                                ),
                                            ]),
                                    ]),
                            ]),
                    ]),
            ]),
        ]),
    ])


# Note that if the container itself is resizable, the graph will not be replotted/resized.
# There isn’t a reliable way to tell if a graph’s container has changed size in JavaScript yet, 
# so we’re just checking if the window is resized.
# We have to call a synthetic resize event to ensure, the graph is informed.
# Solution found here: https://community.plotly.com/t/update-div-size-with-graph-in-it/22671
# app.clientside_callback(
#     """
#     function syntheticResize() {
#         var evt = window.document.createEvent('UIEvents');
#         evt.initUIEvent('resize', true, false, window, 0);
#         window.dispatchEvent(evt);
#         return "updated";
#     }
#     """,
#     Output('right_pos-card-hidden', 'children'),
#     [Input('left_date-card-tabs', 'active_tab'),
#      Input('right_date-card-tabs', 'active_tab')]
# )