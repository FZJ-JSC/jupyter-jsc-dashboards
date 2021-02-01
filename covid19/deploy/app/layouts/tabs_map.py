import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import init_mapfig_bstim, init_mapfig_rki


# Maps
def create_map_tab(tab_name, figure):
    return dbc.Card(
        outline=True,
        color='light',
        className='mt-3',
        children=[ 
            dbc.CardBody(
                style={'padding': 0},
                children=[
                    html.Div(
                        id=f"{tab_name}_img_div",
                        children=[
                            dcc.Loading(
                                id=f"{tab_name}_loading_graph", 
                                children=[
                                    # Use a dummy div to time rendering of graph after
                                    # the children of dummy div have been determined.
                                    # This will render the graph in the correct size.
                                    html.Div(
                                        id=f"{tab_name}_dummy_div",
                                        style={'display': 'none'}
                                    ),
                                    dcc.Graph(
                                        id=f"{tab_name}_graph", 
                                        figure=figure, 
                                        style={
                                            'width': '100%', 
                                            'height': '100%',
                                            'display': 'inline-block'
                                        }
                                    ),
                                ],
                                type='circle', # 'graph', 'cube', 'circle', 'dot', 'default'
                                color='#343A40',
                                style={'height': '450px'},
                        ),
                    ]),
            ]),
        ])


rki_map_tab_left = create_map_tab('rki_map_tab_left', init_mapfig_rki)
bstim_map_tab_left = create_map_tab('bstim_map_tab_left', init_mapfig_bstim)

rki_map_tab_right = create_map_tab('rki_map_tab_right', init_mapfig_rki)
bstim_map_tab_right = create_map_tab('bstim_map_tab_right', init_mapfig_bstim)