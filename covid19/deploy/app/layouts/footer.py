import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import app
from dash.dependencies import Input, Output, State


def create_modal_footer_content(component, modal_title, markdown):
    return html.Div([
        dbc.Button(
            component.capitalize(),
            id='{}_modal_open'.format(component),
            outline=True, 
            color='secondary', 
            className='mr-1'
        ),
        dbc.Modal(
            id='{}_modal'.format(component),
            size='xl',
            children=[
                dbc.ModalHeader(modal_title),
                dbc.ModalBody(
                    dcc.Markdown(markdown)
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        'Schließen', 
                        id='{}_modal_close'.format(component),
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

# Datenschutzerklärung
with open('txt/datenschutzerklaerung.md') as md_file:
    datenschutz_md = md_file.read()
datenschutz_modal = create_modal_footer_content('datenschutz', "Datenschutzerklärung", datenschutz_md)

# Footer
footer = dbc.NavbarSimple(
    brand_href='#',
    color='light',
    children=[
        dbc.NavItem(impressum_modal),
        dbc.NavItem(datenschutz_modal),
    ]
)