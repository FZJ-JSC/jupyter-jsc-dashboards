import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import min_date, max_date, init_date, deltadays
from app import init_countyid, metadata
from datetime import timedelta


def create_depiction_toggle(toggle_name):
    return html.Div(
        id=f"{toggle_name}",
        children = [
            dbc.Row(
                id=f"{toggle_name}_toggle_buttons",
                children=[
                    dbc.Col(
                        dbc.ButtonGroup(
                            id=f"{toggle_name}_7_days",
                            children=[
                                dbc.Button(
                                    "7-Tage-Inzidenz",
                                    id=f"{toggle_name}_7_days_button1",
                                    className="col-6"
                                ),
                                dbc.Button(
                                    "Neuinfektionen des Tages",
                                    id=f"{toggle_name}_7_days_button2",
                                    className="col-6"
                                )],
                            size='sm',
                            style={'width': '100%'}
                        ),
                        width=12
                    ),
        #         ),
        #         dbc.Row(
                    dbc.Col(
        #                 dbc.Collapse(
                            dbc.ButtonGroup(
                                id=f"{toggle_name}_100k",
                                children=[
                                    dbc.Button(
                                        "pro 100.000",
                                        id=f"{toggle_name}_100k_button1",
                                        className="col-6"
                                    ), 
                                    dbc.Button(
                                        "absolut",
                                        id=f"{toggle_name}_100k_button2",
                                        className="col-6"
                                    )],
                                size='sm',
                                className="mr-2 mt-2",
                                style={'width': '100%'}
                            ),
        #                     id=f"{toggle_name}_collapse",
        #                 ),
        #                 width={"size": 7, "offset": 5},
                        width=12
                    )
                ],
                style={'display': 'flex'}
            ),
            html.Div(
                dbc.FormText(
                    id=f"{toggle_name}_no_toggle_text",
                    children=[
                        html.Center("Neuinfektionen des Tages pro 100.000 Einwohner")
                    ],
                    color="secondary",
                    style={'display': 'none'}
                ),
                style={'width': '100%'}
            )
        ])

def create_date_picker(date_picker_name):
    return dbc.FormGroup([
        dbc.Label(
            id=f"{date_picker_name}_label",
            children=["Vorhersagebeginn:"],
            width=5
        ),
        dbc.Col(
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
            width=7,
            align="center"
        ),
        html.Div(
            id=f"{date_picker_name}_output_container",
            style={'display': 'none'},
            children=[
                (init_date + timedelta(days=deltadays)).strftime('%Y_%m_%d')],
        ),
        dbc.FormText(
            children=[
                html.Center("(auf Basis der Daten des vorherigen 3-Wochenfensters)")
            ],
            color="secondary",
            style={'width': '100%'}
        )],
        row=True
    )


def create_position_controls(position_control_name):
    return dbc.FormGroup([
        dbc.Label(
            id='{}_label'.format(position_control_name),
            children=["Landkreis:"],
            width=5
        ),
        dbc.Col(        
            dcc.Dropdown(
                id='{}_variable'.format(position_control_name),
                value=init_countyid,
                options=[
                    {"label": row['LKName'] + " (" + row['LKType'] + ")", "value": row['countyID']} 
                    for index, row in metadata.iterrows()
                ]
            ),
            width=7
        )],
        row=True,
        style={'margin-top': '0.5rem', 'margin-bottom': '0.5rem'}
    )


toggle_left = create_depiction_toggle('toggle_left')
toggle_right = create_depiction_toggle('toggle_right')

date_picker_left = create_date_picker('date_picker_left')
date_picker_right = create_date_picker('date_picker_right')

pos_controls_left = create_position_controls('pos_control_left')
pos_controls_right = create_position_controls('pos_control_right')