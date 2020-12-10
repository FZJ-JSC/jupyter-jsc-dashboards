from app import app, get_assets_dir, init_assets_dir
from dash.dependencies import Input, Output


# Update date output container
def update_date_picker(date):
    if date is not None:
        return get_assets_dir(date)
    else:
        return init_assets_dir


# Update button colors upon toggle
def update_toggle(btn1, btn2):
    # No timestamps because one or both buttons have not been clicked yet
    if btn1 is None or btn2 is None:
        if btn2 is not None:
            return "secondary", "primary"
        else:
            return "primary", "secondary"

    if int(btn1) > int(btn2):
        return "primary", "secondary"
    else:
        return "secondary", "primary"


for side in ['left', 'right']:
    # Date output container
    app.callback(
        Output(f"date_picker_{side}_output_container", 'children'),
        Input(f"date_picker_{side}", 'date')
    )(update_date_picker)
    # Button colors
    app.callback(
        [Output(f"toggle_{side}_7_days_button1", 'color'),
         Output(f"toggle_{side}_7_days_button2", 'color')],
        [Input(f"toggle_{side}_7_days_button1", 'n_clicks_timestamp'),
         Input(f"toggle_{side}_7_days_button2", 'n_clicks_timestamp')]
    )(update_toggle)
    app.callback(
        [Output(f"toggle_{side}_100k_button1", 'color'),
         Output(f"toggle_{side}_100k_button2", 'color')],
        [Input(f"toggle_{side}_100k_button1", 'n_clicks_timestamp'),
         Input(f"toggle_{side}_100k_button2", 'n_clicks_timestamp')]
    )(update_toggle)