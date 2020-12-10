import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import min_date, max_date, init_date, deltadays
from app import init_countyid, metadata
from datetime import timedelta


def create_depiction_toggle(toggle_name):
    return dbc.FormGroup([
        dbc.Label(
            id=f"{toggle_name}_label",
            children=["Darstellung:"],
        ),
        html.Br(),
        dbc.ButtonGroup(
            id=f"{toggle_name}_7_days",
            children=[
                dbc.Button(
                    "7 Tage Inzidenz",
                    id=f"{toggle_name}_7_days_button1"
                ), 
                dbc.Button(
                    "Neuinfektionen",
                    id=f"{toggle_name}_7_days_button2"
                )]
        ),
        html.Br(),
        dbc.ButtonGroup(
            id=f"{toggle_name}_100k",
            className="mt-2",
            children=[
                dbc.Button(
                    "per 100.000",
                    id=f"{toggle_name}_100k_button1"
                ), 
                dbc.Button(
                    "Absolut",
                    id=f"{toggle_name}_100k_button2"
                )]
        ),
    ])


def create_date_picker(date_picker_name):
    return dbc.FormGroup([
        dbc.Label(
            id=f"{date_picker_name}_label",
            children=["Vorhersagebeginn:"],
        ),
        dcc.DatePickerSingle(
            id=date_picker_name,
            style={'width': '100%'},
            display_format='DD. MMM YYYY',
            first_day_of_week=1,
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            initial_visible_month=init_date,
            date=init_date+timedelta(days=deltadays),
        ),
        html.Div(
            id=f"{date_picker_name}_output_container",
            style={'display': 'none'},
            children=[
                (init_date + timedelta(days=deltadays)).strftime('%Y_%m_%d')],
        ),
        dbc.Label(
            id=f"{date_picker_name}_label2",
            children=["(auf Basis der Daten des vorherigen 3-Wochenfensters)"],
        ),
    ])


def create_position_controls(position_control_name):
    return dbc.FormGroup([
    dbc.Label(
        id='{}_label'.format(position_control_name),
        children=["Wähle Landkreis:"],
    ),
    dcc.Dropdown(
        id='{}_variable'.format(position_control_name),
        value=init_countyid,
        options=[
            {"label": row['LKName'] + " (" + row['LKType'] + ")", "value": row['countyID']} 
            for index, row in metadata.iterrows()
        ]
    ),
])


toggle_left = create_depiction_toggle('toggle_left')
toggle_right = create_depiction_toggle('toggle_right')

date_picker_left = create_date_picker('date_picker_left')
date_picker_right = create_date_picker('date_picker_right')

pos_controls_left = create_position_controls('pos_control_left')
pos_controls_right = create_position_controls('pos_control_right')