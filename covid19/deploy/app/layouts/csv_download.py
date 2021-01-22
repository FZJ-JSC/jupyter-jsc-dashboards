import dash_html_components as html


def create_csv_links(component_name):
    return html.Div(
        id=f"{component_name}_div",
        children=[
            html.A(
#                 html.Small("Rohdaten für Berlin Mitte SK vom 01.12.2020 als CSV Datei"),
                id=f"{component_name}_download",
                download="",
                href="",
                target="_blank",
            ),
            html.Br(),
            html.A(
                html.Span([
                    html.I(className="fa fa-external-link-alt fa-sm mr-2"),
                    html.Small("Erklärung der CSV Spalten"),
                ]),
                id=f"{component_name}_erklaerung",
                download="",
                href="",
                target="_blank",
#                 style={'color': 'var(--secondary)'}
            )
        ],
        style={'padding-top': '16px'}
    )


download_left = create_csv_links("download_left")
download_right = create_csv_links("download_right")