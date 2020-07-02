#!/usr/bin/env python
# coding: utf-8

# # Covid19dynstat - JupyterDash

# The `jupyter-dash` package makes it easy to develop Plotly Dash apps from the Jupyter Notebook and JupyterLab.
# Just replace the standard `dash.Dash` class with the `jupyter_dash.JupyterDash` subclass.

# In[1]:


#from jupyter_dash import JupyterDash


# In[2]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
#import flask
#import pandas as pd


# When running in JupyterHub (or Binder), call the `infer_jupyter_config` function to detect the proxy configuration. This will detect the proper request_pathname_prefix and server_url values to use when displaying Dash apps. For example:  
# server_url = `https://jupyter-jsc.fz-juelich.de`  
# request_pathname_prefix = `/user/j.goebbert@fz-juelich.de/jureca_login/`  
# For details please check the source here https://github.com/plotly/jupyter-dash/blob/v0.2.1.post1/jupyter_dash/comms.py#L33

# In[ ]:


#JupyterDash.infer_jupyter_proxy_config()


# **Attention:** I have to run this cell twice: first press play, wait a bit and hit play again while it still shows `[*]`

# #### Create a Dash Flask server
# Requests the browser to load Bootstrap 

# In[4]:


# select a theme
import os
base_url=os.getenv("BASE_URL")
#base_url="http://localhost:8050"
prefix_path=os.getenv("PREFIX_PATH")
#prefix_path="/"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# external_stylesheets=[dbc.themes.BOOTSTRAP] -> default theme
# external_stylesheets=[dbc.themes.CYBORG]    -> dark theme

# start the server
server = app.server
#server = flask.Flask(__name__)
#print(app.get_asset_url('aaa'))


# #### Define the top navigation bar

# In[5]:


# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink(
                "Article",
                href="https://nbviewer.jupyter.org/github/neuroinfo-os/BSTIM-Covid19/blob/master/notebooks/visualization_final.ipynb",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                "Source Code",
                href="https://github.com/neuroinfo-os/BSTIM-Covid19",
            )
        ),
    ],
    brand="Bayesian spatial-temporal interaction model for Covid-19",
    brand_href="#",
    color="dark",
    fixed="top",
    dark=True,
)


# #### Define the main body of the webpage  
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/  
# Layout in Bootstrap is controlled using the grid system.
# The Bootstrap grid has **twelve** columns, and **five** responsive tiers (allowing you to specify different behaviours on different screen sizes, see below).

# In[6]:


from datetime import datetime as dt
left_date_card = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        dcc.DatePickerSingle(
                                            id='left_date-picker',
                                            display_format='DD. MMM YYYY',
                                            min_date_allowed=dt(2020, 3, 30),
                                            max_date_allowed=dt(2020, 6, 24),
                                            initial_visible_month=dt(2020, 6, 24),
                                            date=str(dt(2020, 6, 24, 00, 00, 00)),
                                        ),
                                        html.Div(id='left_output-container-date-picker'),
                                    ]
                                ), 
                            ]
                        ),       
                    ],
                    style={"marginTop": 5},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(
                                    #src='data:image/png;base64,{}'.format(encoded_image),
                                    src=app.get_asset_url('2020_143/map_day143.png'),
                                    style={'width':'100%', 'height':'100%'},
                                    #height=300,
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Img(
                                    #src='data:image/png;base64,{}'.format(encoded_image),
                                    src=app.get_asset_url('2020_143/interaction_kernel_day143.png'),
                                    style={'width':'100%', 'height':'100%'},
                                    #height=300,
                                ),
                            ]
                        ),                    
                    ],
                    style={"marginTop": 30},
                ),    
            ],
        ),
    ],
    style={"marginTop": 10},
    body=True,
)


# In[7]:


right_date_card = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        dcc.DatePickerSingle(
                                            id='right_date-picker',
                                            display_format='DD. MMM YYYY',
                                            min_date_allowed=dt(2020, 3, 30),
                                            max_date_allowed=dt(2020, 6, 24),
                                            initial_visible_month=dt(2020, 6, 24),
                                            date=str(dt(2020, 6, 24, 00, 00, 00)),
                                        ),
                                        html.Div(id='right_output-container-date-picker'),
                                    ]
                                ), 
                            ]
                        ),       
                    ],
                    style={"marginTop": 5},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(
                                    #src='data:image/png;base64,{}'.format(encoded_image),
                                    src=app.get_asset_url('2020_143/map_day143.png'),
                                    style={'width':'100%', 'height':'100%'},
                                    #height=300,
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                html.Img(
                                    #src='data:image/png;base64,{}'.format(encoded_image),
                                    src=app.get_asset_url('2020_143/interaction_kernel_day143.png'),
                                    style={'width':'100%', 'height':'100%'},
                                    #height=300,
                                ),
                            ]
                        ),                    
                    ],
                    style={"marginTop": 30},
                ),    
            ],
        ),
    ],
    style={"marginTop": 10},
    body=True,
)


# In[11]:


import base64

#image_filename = 'assets/covid19-example-img.png' # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#asset_url=app.get_asset_url('')
#echo $JUPYTERHUB_SERVICE_PREFIX 
#  /user/t.kreuzer@fz-juelich.de/jupyterlab_7/
#asset_url="https://jupyter-jsc.fz-juelich.de/user/t.kreuzer@fz-juelich.de/jupyterlab_7/proxy/8050/assets/"

asset_url="{}{}assets/".format(base_url, prefix_path)

left_date_controls = dbc.FormGroup(
            [
                dbc.Label("Postcode - Country"),
                                html.Div(
                                    [
                                        dcc.DatePickerSingle(
                                            id='left_date-picker',
                                            display_format='DD. MMM YYYY',
                                            min_date_allowed=dt(2020, 3, 30),
                                            max_date_allowed=dt(2020, 6, 24),
                                            initial_visible_month=dt(2020, 6, 24),
                                            date=str(dt(2020, 6, 24, 00, 00, 00)),
                                        ),
                                        html.Div(id='left_output-container-date-picker'),
                                    ]
                                ), 
            ],
            style={"marginTop": 10},
)

right_date_controls = dbc.FormGroup(
            [
                dbc.Label("Postcode - Country"),
                                html.Div(
                                    [
                                        dcc.DatePickerSingle(
                                            id='right_date-picker',
                                            display_format='DD. MMM YYYY',
                                            min_date_allowed=dt(2020, 3, 30),
                                            max_date_allowed=dt(2020, 6, 24),
                                            initial_visible_month=dt(2020, 6, 24),
                                            date=str(dt(2020, 6, 24, 00, 00, 00)),
                                        ),
                                        html.Div(id='right_output-container-date-picker'),
                                    ]
                                ), 
            ],
            style={"marginTop": 10},
)

left_pos_controls = dbc.FormGroup(
            [
                dbc.Label("Postcode - Country"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[
                        {"label": col, "value": col} for col in range(10)
                    ],
                    value="sepal length (cm)",
                ),
            ]
)

right_pos_controls = dbc.FormGroup(
            [
                dbc.Label("Postcode - Country"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in range(10)
                    ],
                    value="sepal length (cm)",
                ),
            ]
)

left_img = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Img(
                    #src='data:image/png;base64,{}'.format(encoded_image),
                    src=asset_url+'covid19-example-img.png',
                    style={'width':'90%'},
                    #height=600,
                ),
            ],
            style={'textAlign': 'center'},
        ),
    ],
    body=True,
    style={"marginTop": 20},
)

right_img = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Img(
                    #src='data:image/png;base64,{}'.format(encoded_image),
                    src=asset_url+'covid19-example-img.png',
                    style={'width':'90%'},
                    #height=600,
                ),
            ],
            style={'textAlign': 'center'},
        ),
    ],
    body=True,
    style={"marginTop": 20},
)

#####################################

left_date_tab1 = dbc.Card(
    dbc.CardBody(
        [
                                html.Img(
                                    #src='data:image/png;base64,{}'.format(encoded_image),
                                    src=asset_url+'2020_143/map_day143.png',
                                    style={'width':'100%', 'height':'100%'},
                                    #height=300,
                                ),
        ]
    ),
    className="mt-3",
)

left_date_tab2 = dbc.Card(
    dbc.CardBody(
        [
                                html.Img(
                                    #src='data:image/png;base64,{}'.format(encoded_image),
                                    src=asset_url+'2020_143/interaction_kernel_day143.png',
                                    style={'width':'100%', 'height':'100%'},
                                    #height=300,
                                ),
        ]
    ),
    className="mt-3",
)

right_date_tab1 = dbc.Card(
    dbc.CardBody(
        [
                                html.Img(
                                    #src='data:image/png;base64,{}'.format(encoded_image),
                                    src=asset_url+'2020_143/map_day143.png',
                                    style={'width':'100%', 'height':'100%'},
                                    #height=300,
                                ),
        ]
    ),
    className="mt-3",
)

right_date_tab2 = dbc.Card(
    dbc.CardBody(
        [
                                html.Img(
                                    #src='data:image/png;base64,{}'.format(encoded_image),
                                    src=asset_url+'2020_143/interaction_kernel_day143.png',
                                    style={'width':'100%', 'height':'100%'},
                                    #height=300,
                                ),
        ]
    ),
    className="mt-3",
)

###############################

left_pos_tab1 = dbc.Card(
    dbc.CardBody(
        [
            html.Img(
                #src='data:image/png;base64,{}'.format(encoded_image),
                src=asset_url+'2020_143/plot_green_12345.png',
                style={'width':'100%', 'height':'100%'},
                #height=300,
            ),
        ]
    ),
    className="mt-3",
)

left_pos_tab2 = dbc.Card(
    dbc.CardBody(
        [
            html.Img(
                #src='data:image/png;base64,{}'.format(encoded_image),
                src=asset_url+'2020_143/plot_orange_12345.png',
                style={'width':'100%', 'height':'100%'},
                #height=300,
            ),
        ]
    ),
    className="mt-3",
)

right_pos_tab1 = dbc.Card(
    dbc.CardBody(
        [
            html.Img(
                #src='data:image/png;base64,{}'.format(encoded_image),
                src=asset_url+'2020_143/plot_green_12345.png',
                style={'width':'100%', 'height':'100%'},
                #height=300,
            ),
        ]
    ),
    className="mt-3",
)

right_pos_tab2 = dbc.Card(
    dbc.CardBody(
        [
            html.Img(
                #src='data:image/png;base64,{}'.format(encoded_image),
                src=app.get_asset_url('2020_143/plot_orange_12345.png'),
                style={'width':'100%', 'height':'100%'},
                #height=300,
            ),
        ]
    ),
    className="mt-3",
)

###############################

body_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    dcc.Markdown(
                        f"""
                -----
                #####  BSTIM-Covid19 
                -----
                Daily updated new infection cases of COVID-19 for cities or counties in Germany.
                The model uses the daily updates of the [database](https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0/data?orderBy=Meldedatum) provided by the Robert-Koch institute.
                The model is Bayesian implying that it models the probability of all with the model compatible outcomes.
                The work presented here is based on an adaptation of the [BSTIM model](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0225838#pone.0225838.ref009) adapted to the COVID-19 outbreak scenario.  
                
                -----
                """
                    )
                ],
                width=12,
            ),
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Alert("Basisauswahl", color="primary")),
                dbc.Col(dbc.Alert("Vergleichsauswahl", color="primary")),
            ]
        ),
        #dbc.Row(
        #    [
        #        dbc.Col(left_date_card),
        #        dbc.Col(right_date_card),
        #    ]
        #),

        ### Plots
        dbc.Row(
            [
                dbc.Col(
                    [
                         # --- Zeitangabe (left) ---
                        dbc.Card(
                            [
                                dbc.Col(left_date_controls),
                                dbc.CardHeader(
                                    dbc.Tabs(
                                        [
                                            dbc.Tab(left_date_tab1, label="Infektionen"),
                                            dbc.Tab(left_date_tab2, label="Interaktionskernel"),
                                        ],
                                        id="left_date-card-tabs",
                                        card=True,
                                        active_tab="tab-1",
                                    )
                                ),
                                dbc.CardBody(html.P(id="left_date-card-content", className="card-text")),
                                        
                        # --- Ortsangabe (left) ---
                        dbc.Card(
                            [
                                dbc.Col(left_pos_controls),
                                dbc.CardHeader(
                                    dbc.Tabs(
                                        [
                                            dbc.Tab(left_pos_tab1, label="geglättet"),
                                            dbc.Tab(left_pos_tab2, label="ungeglättet"),
                                        ],
                                        id="left_pos-card-tabs",
                                        card=True,
                                        active_tab="tab-1",
                                    )
                                ),
                                dbc.CardBody(html.P(id="left_pos-card-content", className="card-text")),
                            ],
                            #style={"marginTop": 10},
                            #body=True,
                        ),
                      
                                
                                
                            ],
                            style={"marginTop": 10},
                            body=True,
                        ),
                    ]
                ),

                
                dbc.Col(
                    [
                        # --- Zeitangabe (rechts) ---
                        dbc.Card(
                            [
                                dbc.Col(right_date_controls),
                                dbc.CardHeader(
                                    dbc.Tabs(
                                        [
                                            dbc.Tab(right_date_tab1, label="Infektionen"),
                                            dbc.Tab(right_date_tab2, label="Interaktionskernel"),
                                        ],
                                        id="right_date_card-tabs",
                                        card=True,
                                        active_tab="tab-1",
                                    )
                                ),
                                dbc.CardBody(html.P(id="right_date_card-content", className="card-text")),
                                
                                
                        # --- Ortsangabe (rechts) ---     
                        dbc.Card(
                            [
                                dbc.Col(right_pos_controls),
                                dbc.CardHeader(
                                    dbc.Tabs(
                                        [
                                            dbc.Tab(right_pos_tab1, label="geglättet"),
                                            dbc.Tab(right_pos_tab2, label="ungeglättet"),
                                        ],
                                        id="right_pos-card-tabs",
                                        card=True,
                                        active_tab="tab-1",
                                    )
                                ),
                                dbc.CardBody(html.P(id="right_pos-card-content", className="card-text")),
                            ],
                            #style={"marginTop": 10},
                            #body=True,
                        ),                                
                                
                                
                            ],
                            style={"marginTop": 10},
                            body=True,
                        ),
                    ]
                ),
            ]
        ),

    ],
    style={"marginTop": 100},
    #fluid=True,
)

app.layout = html.Div([navbar, body_layout])


# #### Start the app

# In[12]:


if __name__ == "__main__":
    app.run_server(debug=True)
# mode="jupyterlab" -> will open the app in a tab in JupyterLab
# mode="inline"     -> will open the app below this cell
# mode="external"   -> will displays a URL that you can click on to open the app in a browser tab


# --------------------------
# **Attention**  
# If you get the error "adress in use" this can also be the case because simply your layout has an error so that a dash-app could not been started. Open the app in a new browser-tab with the url
# `<base-url>/proxy/<port>` where \<base-url\> derives from the url of your jupyterlab and \<port\> is by default 8050.  
# For example: `https://jupyter-jsc.fz-juelich.de/user/j.goebbert@fz-juelich.de/jureca_login/proxy/8050`  
# This will show the full error log.
# 
# --------------------------

# Show the Dash Flask server is listening

# In[ ]:


#get_ipython().system('echo "COMMAND     PID      USER   FD   TYPE   DEVICE SIZE/OFF NODE NAME"')
#get_ipython().system('lsof -i -P -n | grep LISTEN')

