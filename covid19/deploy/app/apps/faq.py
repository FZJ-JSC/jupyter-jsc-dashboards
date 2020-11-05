import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import asset_url

with open('txt/faq.md') as md_file:
    faq_md = md_file.read()
    
faq_layout = dbc.Container(
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
                ]
            ),   
        ]),
        dbc.Row([
            dbc.Col(
                width=4,
                children=[
                    html.Img(
                        src=asset_url+"uniosnab-logo.png",
                        height='48', # width='500',
                        style={
                            'display':'block',
                            'margin-left': 'auto',
                            'margin-right': 'auto'
                        },
                    ),
                ]
            ),
            dbc.Col(width=4),   
            dbc.Col(
                width=4,
                children=[
                    html.Img(
                        src=asset_url+"jsc-logo.png",
                        height='48', # width='500',
                        style={
                            'display':'block',
                            'margin-left': 'auto',
                            'margin-right': 'auto'
                        },
                    ),
                ]
            ),
        ]),
        dbc.Row(
            style={ 'marginTop': 30 },
            children=[
                dcc.Markdown(faq_md),
            ],
        ),
    ],
)  