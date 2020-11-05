import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_player

from dash.dependencies import Input, Output, State


with open('txt/bstim_covid19.md') as md_file:
    bstim_covid19_md = md_file.read()
with open('txt/disclaimer.md') as md_file:
    disclaimer_md = md_file.read()
    

# BSTIM
explanations_bstim = html.Div([
    dcc.Markdown(bstim_covid19_md),
    html.Span(
        dbc.Button(
            "Disclaimer", 
            id='disclaimer_modal_open', 
            outline=True, 
            color='secondary', 
            className='mt-0'
        ),
        style={
            'float': 'right',
            'marginTop': 0,
            'marginBottom': 10,
        },
    ),
    dbc.Modal(
        id='disclaimer_modal',
        size='xl',
        children=[
            dbc.ModalHeader("Disclaimer"),
            dbc.ModalBody(
                dcc.Markdown(disclaimer_md),
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Schließen", 
                    id='disclaimer_modal_close', 
                    className="ml-auto")
            ),
        ]
    ),
])

# @app.callback(
#     Output('disclaimer_modal', 'is_open'),
#     [Input('disclaimer_modal_open', 'n_clicks'), Input('disclaimer_modal_close', 'n_clicks')],
#     [State('disclaimer_modal', 'is_open')],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open


# Vorhersage und Analyse
explanations_right = html.Div([
    dcc.Markdown(
        f"""
        -----
        #####  Wie funktioniert die Vorhersage und Analyse
        -----
        """
    ),
    html.Div(
        style={
            'width': '100%',
            'float': 'left',
            'margin': '0% 0% 5% 0%' # top, right, bottom, left
        },
        children=[
            dash_player.DashPlayer(
                id='video-player',
                url="https://youtu.be/0jvH3nkjR9I",
                controls=True,
                width='100%'
            ),
            dcc.Markdown(
                f"""
                Das Video ist unter folgendem Link auch unter YouTube verfügbar:  
                ["BSTIM Covid-19 Model zur Analyse der Ausbreitung der Infektion"](https://youtu.be/0jvH3nkjR9I)
                """,
                style={
                   'margin': '5% 0% 0% 0%' # top, right, bottom, left
                },
            ),                              
        ]), 
])