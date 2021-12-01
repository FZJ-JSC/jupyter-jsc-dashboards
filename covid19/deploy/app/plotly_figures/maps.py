### Daten
# **Landreis-Geometrie vom RKI:**  
# ShapeFile from https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0  
# **GEOJSON:**  
# https://mapshaper.org

import json
import logging
import os
import pandas as pd
import plotly.graph_objects as go

from numpy import nan


logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'WARNING'))
fh = logging.FileHandler('logs/log.out')
fh.setLevel(os.environ.get('LOGLEVEL', 'WARNING'))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def create_static_map_data(geojson_path):
    with open(geojson_path) as json_file:
        counties_geojson = json.load(json_file)

    # 'Id' must be a unique identifier of the shapes 
    # (required by plotly.Choroplethmapbox).
    for i, feat in enumerate(counties_geojson['features']):
        feat['id'] = i

    # Create pandas dataframe from geojson dictionary.
    counties_metadf = pd.DataFrame(data={
        # 'Geoids' has to match with the county-shape-ids of the map.csv files, 
        # so it must start with 0 and increase without skipping any values.
        'geoids': [feat['id'] for feat in counties_geojson['features']],
        'names': [feat['properties'].get('GEN') for feat in counties_geojson['features']],
        'cca': [feat['properties'].get('RS') for feat in counties_geojson['features']],
    })

    return (counties_geojson, counties_metadf)


def create_dynamic_map_data(counties_geojson, mapcsv_path, column):
    # Create (correctly sorted) dataframe from no. infections
    infections_array = []
    try:
        mapcsv = pd.read_csv(mapcsv_path)
        # Get no. infections for each county from mapcsv 
        for feat in counties_geojson['features']:
            # Need the county id to find the corresponding value in mapcsv
            cca_str = feat['properties'].get('RS')
            if cca_str is not None:
                cca_filtered_df = mapcsv.loc[mapcsv['countyID']==int(cca_str), column]
                cca_value = next(iter(cca_filtered_df), 0.0)
                infections_array.append(cca_value)
            else:
                infections_array.append(0.0)
    except IOError:
        logger.debug("File not found: " + mapcsv_path)
        for feat in counties_geojson['features']:
            infections_array.append(nan)

    counties_infectionsdf = pd.DataFrame(data={'infections': infections_array})
    return counties_infectionsdf


def create_map_figure(counties_geojson, counties_metadf, mapcsv_path,
                      column, n_people, zmax=None,
                      seven_days=False, incidence_values=False,
                      width=500, height=450):

    counties_infectionsdf = create_dynamic_map_data(
        counties_geojson, mapcsv_path, column)
    if zmax is None:
        zmax = counties_infectionsdf.max().tolist()[0]
    zmax = (zmax + 90) // 100 * 100

    if incidence_values:
        colorscale = 'YlOrRd'
        value_str = "Wert: %{z:.2f}<br>"
        if seven_days:
            colorbar_text = "7-Tage-Inzidenz pro 100.000 Einwohner"
        else:
            colorbar_text = "1-Tages-Inzidenz pro 100.000 Einwohner"
    elif not incidence_values:
        colorscale = 'deep'
        value_str = "Wert: %{z}<br>"
        if seven_days:
            colorbar_text = "Fallzahlen der letzten 7 Tage pro Landkreis"
        else:
            colorbar_text = "Fallzahlen des Tages pro Landkreises"

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=counties_geojson,
            # Set which features in geojson to plot using their feature id field.
            locations=counties_metadf.geoids,
            # Set text elements associated with each location.
            text=counties_metadf.names,
            # Set custom data to use in hovertemplate
            customdata=n_people,
            # Set data to be color-coded.
            # Round to int if we display number of new cases.
            z=counties_infectionsdf.infections if incidence_values \
            else counties_infectionsdf.infections.round().astype(int),
            # Set colorscale and bar
            colorscale=colorscale,
            colorbar=dict(
                thickness=20,
                ticklen=3,
                title=dict(
                    text=colorbar_text,
                    side='right'
                )
            ),
            zmin=0, zmax=zmax,
            # Set lines between features
            marker_opacity=0.75, marker_line_width=0.1,
            # Set data shown on hover
            hovertemplate="<b>%{text}</b><br>" +
                "Einwohner: %{customdata:.3s}<br>" +
                value_str +
                "<extra></extra>",
        )
    )

    # Set layout options.
    fig.update_layout(
#         width=width, 
#         height=height,
#         autosize=True,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # Preserve UI state when updating.
        uirevision=True,
        # Set mapbox.
        mapbox_style="carto-positron",  # https://plotly.com/python/mapbox-layers/
        mapbox_zoom=4.5,
        mapbox_center={"lat": 51.30, "lon": 10.45},
    )

    return fig
