import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import app
from dash.dependencies import Input, Output, State


def create_modal_footer_content(content_name, modal_title, markdown):
    return html.Div([
        dbc.Button(
            content_name.capitalize(), 
            id='{}_modal_open'.format(content_name), 
            outline=True, 
            color='secondary', 
            className='mr-1'
        ),
        dbc.Modal(
            id='{}_modal'.format(content_name),
            size='xl',
            children=[
                dbc.ModalHeader(modal_title),
                dbc.ModalBody(
                    dcc.Markdown(markdown)
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        'Schließen', 
                        id='{}_modal_close'.format(content_name), 
                        className='ml-auto'
                    )
                ),
            ]
        ),
    ])


# Impressum
with open('txt/impressum.md') as md_file:
    impressum_md = md_file.read()
impressum_modal = create_modal_footer_content('impressum', "Impressum und Haftungsausschluss", impressum_md)

@app.callback(
    Output('impressum_modal', 'is_open'),
    [Input('impressum_modal_open', 'n_clicks'), 
     Input('impressum_modal_close', 'n_clicks')],
    [State('impressum_modal', 'is_open')],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Datenschutzerklärung
with open('txt/datenschutzerklaerung.md') as md_file:
    datenschutz_md = md_file.read()
datenschutz_modal = create_modal_footer_content('datenschutz', "Datenschutzerklärung", datenschutz_md)

@app.callback(
    Output('datenschutz_modal', 'is_open'),
    [Input('datenschutz_open', 'n_clicks'), 
     Input('datenschutz_close', 'n_clicks')],
    [State('datenschutz_modal', 'is_open')],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Footer
footer = dbc.NavbarSimple(
    brand_href='#',
    color='light',
    children=[
        dbc.NavItem(impressum_modal),
        dbc.NavItem(datenschutz_modal),
    ]
)