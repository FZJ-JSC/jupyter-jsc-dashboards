from dash.dependencies import Input, Output, State

from app import app


# Toggle modal for two inputs
def toggle_modal_2(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Toggle modal for three inputs
def toggle_modal_3(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open 


# Top section disclaimer
app.callback(
    Output('disclaimer_modal', 'is_open'),
    [Input('disclaimer_modal_open', 'n_clicks'), 
     Input('disclaimer_modal_close', 'n_clicks')],
    [State('disclaimer_modal', 'is_open')],
)(toggle_modal_2)

# Footer
app.callback(
    Output('datenschutz_modal', 'is_open'),
    [Input('datenschutz_modal_open', 'n_clicks'), 
     Input('datenschutz_modal_close', 'n_clicks')],
    [State('datenschutz_modal', 'is_open')],
)(toggle_modal_2)

app.callback(
    Output('impressum_modal', 'is_open'),
    [Input('impressum_modal_open', 'n_clicks'), 
     Input('impressum_modal_close', 'n_clicks')],
    [State('impressum_modal', 'is_open')],
)(toggle_modal_2)


# Plots
for component in [
    'geglaettet_left', 'geglaettet_right',
    'ungeglaettet_left', 'ungeglaettet_right',
    # and Ikernel
    'ikernel_tab_left', 'ikernel_tab_right']:
    app.callback(
        Output(f"{component}_modal", "is_open"),
        [Input(f"{component}_img", 'n_clicks'),
         Input(f"{component}_modal_open", 'n_clicks'),
         Input(f"{component}_modal_close", 'n_clicks')],
        [State(f"{component}_modal", 'is_open')],
        )(toggle_modal_3)


# Ikernel interpretation helpers
for i in range(1,4):
    app.callback(
        Output(f"ikernel_inter{i}_modal", "is_open"),
        [Input(f"ikernel_tab_left_inter{i}_div", "n_clicks"),
         Input(f"ikernel_tab_right_inter{i}_div", "n_clicks"),
         Input(f"ikernel_inter{i}_modal_close", "n_clicks")],
        [State(f"ikernel_inter{i}_modal", "is_open")],
    )(toggle_modal_3)