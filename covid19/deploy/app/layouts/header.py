import dash_bootstrap_components as dbc
import dash_html_components as html


def create_header_nav_bar(button_text, href):
    return dbc.NavbarSimple(
        brand="Bayessches räumlich-zeitliches Interaktionsmodell für Covid-19",
        brand_href="#",
        color="dark",
        fixed="top",
        dark=True,
        children=[
            dbc.NavItem(
                dbc.Button(
                    button_text,
                    color='primary',
                    href=href  #"https://jupyter-jsc.fz-juelich.de/nbviewer/github/neuroinfo-os/BSTIM-Covid19/blob/master/notebooks/FragenAntworten.ipynb"
                )
            ),
            dbc.NavItem(
                dbc.NavLink(
                    html.Span([
                        html.I(className="fa fa-external-link-alt mx-1"),
                        "Quellcode"
                    ]),
                    href="https://github.com/neuroinfo-os/BSTIM-Covid19",
                    target="_blank"
                )
            ),
        ]
    )


navbar = create_header_nav_bar("Fragen & Antworten", "/faq")
faq_navbar = create_header_nav_bar("Dashboard", "/")