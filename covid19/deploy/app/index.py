import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import dashboard, faq
from layouts.header import navbar, faq_navbar
from layouts.footer import footer
import callbacks


main_page = html.Div([
    html.P('4.5', id='version', style={'display':'none'}),
    navbar, dashboard.body_layout, footer
])
faq_page = html.Div([
    faq_navbar, faq.faq_layout, footer
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# Change page depending on URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/faq':
        return faq_page
    else:
        return main_page


if __name__ == '__main__':
    app.run_server(debug=True)
