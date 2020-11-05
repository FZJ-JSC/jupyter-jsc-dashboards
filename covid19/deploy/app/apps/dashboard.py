import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import asset_url
from layouts.date_picker import date_picker
from layouts.tabs_map import bstim_map_tab, rki_map_tab
from layouts.top_section import explanations_bstim, explanations_right
from layouts.plots import geglaettet_tab, ungeglaettet_tab, inzidenz_tab
from layouts.position_controls import pos_controls


tab_height = '5vh'

with open('txt/warning.txt') as txt_file:
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
#         ikernel_inter1_modal,
#         ikernel_inter2_modal,
#         ikernel_inter3_modal,
        
        dbc.Row([
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
                            date_picker,
                        ),
                        dbc.CardBody(
                            className='mt-3',
                            children=[
                                dbc.Tabs(
                                    id='date_card_tabs',
                                    active_tab='tab-0',                                            
                                        children=[
                                            dbc.Tab(
                                                rki_map_tab, 
                                                label="Meldedaten RKI", 
                                                style={'padding': '0', 'height': '450px'}),
                                            dbc.Tab(
                                                bstim_map_tab, 
                                                label="Nowcast BSTIM", 
                                                style={'padding': '0', 'height': '450px'}),
#                                             dbc.Tab(
#                                                 ikernel_tab, 
#                                                 label="Interaktionskernel", 
#                                                 style={'padding': '0', 'height': '450px'}),                                             
                                        ]),
                                html.P(
                                    id='card_separator',
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
                                            pos_controls,
                                        ),
                                        dbc.CardBody(
                                            className='mt-3',
                                            children=[
                                                dbc.Tabs(
                                                    id='pos_card_tabs',
                                                    active_tab='tab-0',                                                   
                                                            children=[
                                                                dbc.Tab(
                                                                    geglaettet_tab, 
                                                                    label="geglättet",    
                                                                    style={'padding': '0'} # height': '450px'}
                                                                ), 
                                                                dbc.Tab(
                                                                    ungeglaettet_tab, 
                                                                    label="ungeglättet",  
                                                                    style={'padding': '0'} # height': '450px'}
                                                                ),
                                                                dbc.Tab(
                                                                    inzidenz_tab, 
                                                                    label="7 Tage Inzidenz",  
                                                                    style={'padding': '0'} # height': '450px'}
                                                                ),
                                                            ]),
                                                html.P(
                                                    id='pos_card_content',
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