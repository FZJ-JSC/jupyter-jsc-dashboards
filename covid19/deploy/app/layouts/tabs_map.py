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
                        id='{}_img_div'.format(tab_name),
                        children=[
                            dcc.Loading(
                                id='{}_loading_graph'.format(tab_name), 
                                children=[
                                    # might need div around graph?
                                    dcc.Graph(
                                        id='{}_graph'.format(tab_name), 
                                        figure=init_mapfig_bstim, 
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