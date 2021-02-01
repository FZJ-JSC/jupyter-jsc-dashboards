import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from plotly_figures.curves import *


def create_plot_modal_and_tooltip(component_name, title, tooltip):
    return dbc.Row([
        # Modal
        dbc.Button(
            html.Span([
                html.I(className="fa fa-search-plus mr-2"),
                "Vergrößern",
            ]),
            id=f"{component_name}_modal_open", 
            outline=True,
            size='sm',
            color='secondary', 
            className='mr-1'),
        dbc.Modal(
            id=f"{component_name}_modal",
            size='xl',
            style={'max-width': '800px'},
            children=[
                dbc.ModalHeader(title),
                dbc.ModalBody(
                    id=f"{component_name}_modal_img",
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Schließen", 
                        id=f"{component_name}_modal_close", 
                        className='ml-auto'
                    )
                ),
            ]
        ),
        # Tooltip
        html.I(
            className="fa fa-question-circle fa-lg mr-2",
            id=f"{component_name}_target",
            style={
                'color':'var(--secondary)',
                'align-self': 'center'
            },
        ),
        dbc.Tooltip(
            tooltip, 
            target=f"{component_name}_target", 
            style = {
                'maxWidth': 600,
                'width': 600
            }
        )
    ]) 


def create_plot_tab(component_name, title, tooltip):
    return dbc.Card(
        outline=True,
        color='light',
        className='mt-3',
        children=[ 
            dbc.CardBody([
                html.Div(
                    id=f"{component_name}_img_div",
                    children=[
                        create_plot_modal_and_tooltip(component_name, title, tooltip),
                        dcc.Loading(
                            id=f"{component_name}_loading_img", 
                            children=[
                                html.Div(id=f"{component_name}_img"),
                            ],
                            type='circle', # 'graph', 'cube', 'circle', 'dot', 'default'
                            color='#343A40',
                            style={'height': '600px'},
                        ),  
                        html.Div(
                            dcc.Markdown(
                                id=f"{component_name}_txt",
                                children=[''],
                            )
                        ),
                    ]),
            ])
        ])


# Geglättet
with open('txt/plot_tooltip_trend.md') as md_file:
    geglaettet_tab_tooltip = md_file.read()
geglaettet_tab_left = create_plot_tab('geglaettet_left', 'geglättet', geglaettet_tab_tooltip)
geglaettet_tab_right = create_plot_tab('geglaettet_right', 'geglättet', geglaettet_tab_tooltip)


# Ungeglättet
with open('txt/plot_tooltip_raw.md') as md_file:
    ungeglaettet_tab_tooltip = md_file.read()
ungeglaettet_tab_left = create_plot_tab('ungeglaettet_left', 'ungeglättet', ungeglaettet_tab_tooltip)
ungeglaettet_tab_right = create_plot_tab('ungeglaettet_right', 'ungeglättet', ungeglaettet_tab_tooltip)
