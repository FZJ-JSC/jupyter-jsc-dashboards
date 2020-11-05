import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app


# Top section disclaimer 
@app.callback(
    Output('disclaimer_modal', 'is_open'),
    [Input('disclaimer_modal_open', 'n_clicks'), Input('disclaimer_modal_close', 'n_clicks')],
    [State('disclaimer_modal', 'is_open')],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Plots
@app.callback(
    Output('geglaettet_modal', 'is_open'),
    [Input('geglaettet_img_div', 'n_clicks'), 
     Input('geglaettet_modal_open', 'n_clicks'), 
     Input('geglaettet_modal_close', 'n_clicks')],
    [State('geglaettet_modal', 'is_open')],
)
def toggle_modal(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open

@app.callback(
    Output("ungeglaettet_modal", "is_open"),
    [Input("ungeglaettet_img_div", "n_clicks"), 
     Input("ungeglaettet_modal_open", "n_clicks"), 
     Input("ungeglaettet_modal_close", "n_clicks")],
    [State("ungeglaettet_modal", "is_open")],
)
def toggle_modal(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open


# # Ikernel
# @app.callback(
#     Output('ikernel_tab_modal', 'is_open'),
#     [Input('ikernel_tab_img_div', 'n_clicks'), 
#      Input('ikernel_tab_modal_open', 'n_clicks'), 
#      Input('ikernel_tab_modal_close', 'n_clicks')],
#     [State('ikernel_tab_modal', 'is_open')],
# )
# def toggle_modal(n1, n2, n3, is_open):
#     if n1 or n2 or n3:
#         return not is_open
#     return is_open

# # Ikernel interpretation helpers
# @app.callback(
#     Output("ikernel_inter1_modal", "is_open"),
#     [Input("ikernel_inter1_div", "n_clicks"),
#      Input("ikernel_inter1_modal_close", "n_clicks")],
#     [State("ikernel_inter1_modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open

# @app.callback(
#     Output("ikernel_inter2_modal", "is_open"),
#     [Input("ikernel_inter2_div", "n_clicks"), 
#      Input("ikernel_inter2_modal_close", "n_clicks")],
#     [State("ikernel_inter2_modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open

# @app.callback(
#     Output("ikernel_inter3_modal", "is_open"),
#     [Input("ikernel_inter3_div", "n_clicks"), 
#      Input("ikernel_inter3_modal_close", "n_clicks")],
#     [State("ikernel_inter3_modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open