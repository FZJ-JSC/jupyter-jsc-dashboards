import dash_bootstrap_components as dbc
import dash_core_components as dcc

from app import init_countyid, metadata


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

pos_controls_left = create_position_controls('pos_control_left')
pos_controls_right = create_position_controls('pos_control_right')

