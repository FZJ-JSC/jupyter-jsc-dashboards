import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

table_header = html.Thead(html.Tr([html.Th("Spaltenname"), html.Th("Erklärung")]))

landkreis_csv = dbc.Card([
    dbc.CardHeader(html.H5("Erklärung zu den Landkreis CSV Dateien")),
    dbc.CardBody([
        html.Blockquote(
            html.P([
                html.Em("Beispieldateiname: "), "12345_Landkreis_2021-01-31.csv"
            ])
        ),
        dcc.Markdown("Jede Zeile stellt einen Tag dar. \
        Die Erklärung der Spalten folgt:"),
        # Table
        dbc.Table([
            table_header,
            html.Tbody([
                html.Tr([
                    html.Td("Raw Prediction (Mean/Q5/Q25/Q75/Q95)"),
                    html.Td("Direkte Modellwerte, mit Mittelwert und Quantilen")
                ]),
                html.Tr([
                    html.Td("Raw Prediction (Mean/Q5/Q25/Q75/Q95) 100k"),
                    html.Td("Direkte Modellwerte, normiert auf 100.000 Einwohner")
                ]),
                html.Tr([
                    html.Td("Trend Prediction (Mean/Q5/Q25/Q75/Q95)"),
                    html.Td("Modellwerte mit Korrektur für periodische Abweichungen in den Meldedaten")
                ]),
                html.Tr([
                    html.Td("Trend 7Week Prediction (Mean/Q5/Q25/Q75/Q95)"),
                    html.Td("Sieben-Tage-Inzidenz, berechnet aus 'Trend Predictions'")
                ]),
                html.Tr([
                    html.Td("Trend 7Week Prediction (Mean/Q5/Q25/Q75/Q95) 100k"),
                    html.Td("Sieben-Tage-Inzidenz, berechnet aus 'Trend Predictions', \
                    normiert auf 100.000 Einwohner")
                ]),
                html.Tr([
                    html.Td("RKI Meldedaten"),
                    html.Td("Meldedaten des RKI")
                ]),
                html.Tr([
                    html.Td("RKI 7Day Incidence"),
                    html.Td("Sieben-Tage-Inzidenz, berechnet aus Meldedaten des RKI")
                ]),
                html.Tr([
                    html.Td("is_nowcast"),
                    html.Td("Falls True wurden die Daten vorhergesagt, \
                    obwohl RKI-Meldedaten vorhanden waren")
                ]),
                html.Tr([
                    html.Td("is_high"),
                    html.Td("Falls True sind die RKI-Meldedaten höher als Q95 der Vorhersage")
                ]),
                html.Tr([
                    html.Td("is_prediction"),
                    html.Td("Falls True sind die Daten Vorhersagen für \
                    die Zukunft zum Zeitpunkt der Berechnung")
                ]),
            ])
        ], hover=True)
    ])
], className='mb-4')

karten_csv = dbc.Card([
    dbc.CardHeader(html.H5("Erklärung zu den Karten CSV Dateien")),
    dbc.CardBody([
        html.Blockquote(
            html.P([
                html.Em("Beispieldateiname"), ": map_2020_01_01.csv"
            ])
        ),
        dcc.Markdown("Jede Zeile stellt einen Lankreis dar. \
        Die Erklärung der Spalten folgt:"),
        # Table
        dbc.Table([
            table_header,
            html.Tbody([
                html.Tr([
                    html.Td("newInfRaw"),
                    html.Td("Vorhergesagter Absolutwert für Neuinfektionen")
                ]),
                html.Tr([
                    html.Td("newInf100k"),
                    html.Td("'newInfRaw' normiert auf 100.000 Einwohner")
                ]),
                html.Tr([
                    html.Td("7DayInfRaw"),
                    html.Td("Vorhergesagte Sieben-Tage-Inzidenz, \
                    mit Korrektur für periodische Abweichungen in den Meldedaten")
                ]),
                html.Tr([
                    html.Td("7DayInf100k"),
                    html.Td("'7DayInfRaw' normiert auf 100.000 Einwohner")
                ]),
                html.Tr([
                    html.Td("newInfRaw_RKI"),
                    html.Td("Vom RKI gemeldeter Absolutwert für Neuinfektionen")
                ]),
                html.Tr([
                    html.Td("newInf100k_RKI"),
                    html.Td("'newInfRaw_RKI' normiert auf 100.000 Einwohner")
                ]),
                html.Tr([
                    html.Td("7DayInfRaw_RKI"),
                    html.Td("Absolute Sieben-Tage-Inzidenz laut RKI-Meldedaten")
                ]),
                html.Tr([
                    html.Td("7DayInf100k_RKI"),
                    html.Td("'7DayInfRaw_RKI' normiert auf 100.000 Einwohner")
                ]),
            ])
        ], hover=True)
    ])
], className='my-4')

metadaten_csv = dbc.Card([
    dbc.CardHeader(html.H5("Erklärung zu den Metadaten CSV Dateien")),
    dbc.CardBody([
        html.Blockquote(
            html.P([
                html.Em("Beispieldateiname"), ": metadata_2020_01_01.csv"
            ])
        ),    dcc.Markdown("Jede Zeile stellt einen Landkreis dar. \
        Die Erklärung der Spalten folgt:"),
        # Table
        dbc.Table([
            table_header,
            html.Tbody([
                html.Tr([
                    html.Td("countyID"),
                    html.Td("einheitliche ID für Landkreis")
                ]),
                html.Tr([
                    html.Td("LKType"),
                    html.Td("Typ des Landkreises (LK/SK/Region)")
                ]),
                html.Tr([
                    html.Td("LKName"),
                    html.Td("Name des Landkreises")
                ]),
                html.Tr([
                    html.Td("probText"),
                    html.Td("Wahrscheinlichkeit für steigende/fallende Werte")
                ]),
                html.Tr([
                    html.Td("n_people"),
                    html.Td("Anzahl der gemeldeten Einwohner")
                ]),
            ])
        ], hover=True)
    ])
], className='my-4')