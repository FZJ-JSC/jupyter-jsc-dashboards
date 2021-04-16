from dash.dependencies import Input, Output, State

from app import app
from layouts.top_section import youtube_video


@app.callback(
    [Output("video-container", "children"),
     Output("youtube-consent-overlay", "style")],
    Input("youtube-consent-overlay", "n_clicks"),
    prevent_initial_call=True
)
def set_video(n_clicks):
    return youtube_video, {"display": "none"}