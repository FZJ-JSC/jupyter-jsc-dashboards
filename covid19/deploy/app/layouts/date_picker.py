import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import min_date, max_date, init_date, deltadays
from datetime import timedelta


def create_date_picker(date_picker_name):
    return dbc.FormGroup([
        dbc.Label(
            id='{}_label'.format(date_picker_name),
            children=["Vorhersagebeginn:"],
        ),
        dcc.DatePickerSingle(
            id=date_picker_name,
            style={'width': '100%'},
            display_format='DD. MMM YYYY',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            initial_visible_month=init_date,
            date=init_date+timedelta(days=deltadays),
        ),
        html.Div(
            id='{}_output_container'.format(date_picker_name),
            style={'display': 'none'},
            children=[(init_date +timedelta(days=deltadays)).strftime('%Y_%m_%d')],
        ),
        dbc.Label(
            id='{}_label2'.format(date_picker_name),
            children=["(auf Basis der Daten des vorherigen 3-Wochenfensters)"],
        ),
    ])


date_picker = create_date_picker('date_picker')