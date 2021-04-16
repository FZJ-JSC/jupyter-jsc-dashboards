import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_player

with open('txt/bstim_covid19.md') as md_file:
    bstim_covid19_md = md_file.read()
    index = bstim_covid19_md.find('\n')
    bstim_covid19_title = bstim_covid19_md[:index]
    bstim_covid19_text = bstim_covid19_md[index:]

with open('txt/disclaimer.md') as md_file:
    disclaimer_md = md_file.read()


# BSTIM
explanations_bstim = html.Div([
    html.Hr(),
    dbc.Row([
        dcc.Markdown(
            bstim_covid19_title,
            className='pt-1',
        ),
        dbc.Button(
                "Disclaimer", 
                id='disclaimer_modal_open', 
                outline=True, 
                color='secondary', 
                className='mt-0'
        )],
        align="center",
        justify="between",
        style={'margin': 0},
    ),
    html.Hr(),
    dcc.Markdown(bstim_covid19_text),
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


# Vorhersage und Analyse
youtube_video = dash_player.DashPlayer(
    id="video-player",
    url="https://youtu.be/0jvH3nkjR9I",
    controls=True,
    playing=True
)

youtube_screenshot = html.Img(
    id="video-screenshot",
    src="assets/video.png",
    width="100%", height="100%"
)

youtube_consent_overlay = html.Div(
    [
        html.I(className="play"),
        html.Span("""
            Klicken Sie auf den Video-Banner, um das YouTube-Video zu laden 
            und das Video zu starten. Damit akzeptieren Sie die 
            Datenschutzerklärung von YouTube.
            """, className="text-center")
    ],
    className="overlay",
    id="youtube-consent-overlay",
    title="YouTube-Video laden und starten"
)


explanations_right = html.Div([
    html.Hr(),
    dbc.Row(
        dcc.Markdown(
            "#####  Wie funktioniert die Vorhersage und Analyse",
            className='pt-1',
        ),
        align="center",
        style={'height': '38px', 'margin': 0},
    ),
    html.Hr(),
    html.Div(
        style={
            'width': '100%',
            'float': 'left',
            'margin': '0% 0% 5% 0%'  # top, right, bottom, left
        },
        children=[
            html.Div(
                [
                    youtube_screenshot,
                    youtube_consent_overlay
                ],
                id="video-container",
                className="video-container"
            ),
            dcc.Markdown(
                f"""
                Das Video ist unter folgendem Link auch unter YouTube verfügbar:  
                ["BSTIM Covid-19 Model zur Analyse der Ausbreitung der Infektion"](https://youtu.be/0jvH3nkjR9I)
                """,
                style={
                   'margin': '5% 0% 0% 0%'  # top, right, bottom, left
                },
            ),
        ]),
])