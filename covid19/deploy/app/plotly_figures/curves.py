import pandas as pd
import plotly.graph_objects as go
import locale
from datetime import datetime


locale.setlocale(locale.LC_TIME, "de_DE")

column_dict_raw = {
    'mean': {
        'column': 'Raw Prediction Mean',
        'color': 'rgb(213,94,0)',
    },
    'q5': {
        'column': 'Raw Prediction Q5',
        'color': 'rgb(230,212,173)',
    },
    'q25': {
        'column': 'Raw Prediction Q25',
        'color': 'rgb(230,185,84)',
    },
    'q75': {
        'column': 'Raw Prediction Q75',
        'color': 'rgb(230,185,84)',
    },
    'q95': {
        'column': 'Raw Prediction Q95',
        'color': 'rgb(230,212,173)',
    },
    'q5q95': {
        'fill_color': 'rgba(230,212,173,0.5)',
    },
    'q25q75': {
        'fill_color': 'rgba(230,185,84,0.5)',
    }
}

column_dict_trend = {
    'mean': {
        'column': 'Trend Prediction Mean',
        'color': 'rgb(0,100,80)',
    },
    'q5': {
        'column': 'Trend Prediction Q5',
        'color': 'rgb(214,221,198)',
    },
    'q25': {
        'column': 'Trend Prediction Q25',
        'color': 'rgb(190,208,150)',
    },
    'q75': {
        'column': 'Trend Prediction Q75',
        'color': 'rgb(190,208,150)',
    },
    'q95': {
        'column': 'Trend Prediction Q95',
        'color': 'rgb(214,221,198)',
    },
    'q5q95': {
        'fill_color': 'rgba(214,221,198,0.5)',
    },
    'q25q75': {
        'fill_color': 'rgba(190,208,150,0.5)',
    }
}

column_dict_7days = {
    'mean': {
        'column': 'Trend 7Week Prediction Mean100k',
        'color': 'rgb(0,100,80)',
    },
    'q5': {
        'column': 'Trend 7Week Prediction Q5',
        'color': 'rgb(214,221,198)',
    },
    'q25': {
        'column': 'Trend 7Week Prediction Q25',
        'color': 'rgb(190,208,150)',
    },
    'q75': {
        'column': 'Trend 7Week Prediction Q75',
        'color': 'rgb(190,208,150)',
    },
    'q95': {
        'column': 'Trend 7Week Prediction Q95',
        'color': 'rgb(214,221,198)',
    },
    'q5q95': {
        'fill_color': 'rgba(214,221,198,0.5)',
    },
    'q25q75': {
        'fill_color': 'rgba(190,208,150,0.5)',
    }
}


def create_figure_from_df(df, column_dict, rki=True):
    # Create figure
    fig = go.Figure()
    # Date column of df is the x data
    x_data = df['Unnamed: 0']

    # Filled quantils
    # Append reversed q95 column to q5 column
    y5_95 = df[column_dict['q5']['column']].append(df[column_dict['q95']['column']][::-1])
    fig.add_trace(go.Scatter(
        name='5%-95%-Quantil',    
        x=x_data.append(x_data[::-1]), 
        y=y5_95,
        fill='toself',
        fillcolor=column_dict['q5q95']['fill_color'],
        line_color='rgba(255,255,255,0)',
    ))
    # Append reversed q75 column to q25 column
    y25_75 = df[column_dict['q25']['column']].append(df[column_dict['q75']['column']][::-1])
    fig.add_trace(go.Scatter(
        name='25%-75%-Quantil',    
        x=x_data.append(x_data[::-1]),
        y=y25_75,
        fill='toself',
        fillcolor=column_dict['q25q75']['fill_color'],
        line_color='rgba(255,255,255,0)',
    ))

    # Dotted quantil lines
    for quantil in ['q5', 'q25', 'q75', 'q95']:
        fig.add_trace(go.Scatter(
            name='{}%-Quantil'.format(quantil[1:]),
            showlegend=False,
            x=x_data, y=df[column_dict[quantil]['column']],
            line=dict(
                color=column_dict[quantil]['color'],
                width=2,
                dash="dot",
            )
        ))

    # Model line
    fig.add_trace(go.Scatter(
        name='Modell',    
        x=x_data, y=df[column_dict['mean']['column']],
        line_color=column_dict['mean']['color'],
    ))

    if rki:
        # RKI scatter points
        fig.add_trace(go.Scatter(
            name='Daten RKI',
            x=x_data, y=df['RKI Meldedaten'],
            mode='markers',
            marker=dict(color="black", size=6)
        ))

    return fig


def update_layout(fig, fixedrange=False,
                  skip_first_7=False,
                  color_legend='rgb(229, 236, 246)', 
                  color_forecast='rgb(24, 145, 255)', 
                  color_nowcast='rgb(136, 207, 250)'):
    # Find y_max from q95 column data
    if skip_first_7:
        y_max = max(fig.data[5]['y'][7:])
    else:
        y_max = max(fig.data[5]['y'])
    x_data = fig.data[-1]['x']
    x_labels = []
    # Create x-axis labels
    for i, date in enumerate(x_data):
        if i % 5 == 0:
            date = datetime.strptime(date, '%Y-%m-%d')
            x_labels.append(date.strftime('%d.%m.%Y'))
        else:
            x_labels.append('')
    for i in [-10, -6, -1]:
        # Reformat date string
        date = datetime.strptime(x_data[i], '%Y-%m-%d').strftime('%d.%m.%Y<br>%A')
        if i == -6: # Day before forecast date: with weekday and red
            x_labels[i] = "<span style='color:red'><b>" + date + "</b></span>"
        else: # Nowcast and last date with weekday
            x_labels[i] = "<b>" + date + "</b>"

    # Update layout and legend
    fig.update_layout(
        margin=dict(l=0, r=0),  # Remove side margins
        legend=dict(
            x=0.01, y=0.99,
            yanchor="top",
            xanchor="left",
            bgcolor=color_legend,
            bordercolor="LightGrey",
            borderwidth=1
        ),
    )

    # Configure axes
    fig.update_xaxes(
        tickmode='array',
        tickvals=x_data,
        ticktext=x_labels,
        autorange=False,
        range=[x_data[0], x_data[-1]],
        ticks="outside",
        tickson="boundaries",
        tickangle=-45,
        ticklen=8,
        fixedrange=fixedrange # Disable panning
    )
    fig.update_yaxes(
        title="Fallzahlen/Tag nach Meldedatum",
        autorange=False,
        range=[-5, y_max],
        dtick=20, # 10
        fixedrange=fixedrange  # Disable zooming
    )

    # Vertical lines for nowcast and forecast
    fig.add_shape(
        type='line', 
        line=dict(
            color=color_nowcast,
            width=4,
            dash="dashdot",
        ),
        yref='paper', y0=0, y1=1,
        xref='x', x0=x_data[-10], x1=x_data[-10],
    )
    fig.add_shape(
        type='line', 
        line=dict(
            color=color_forecast,
            width=4,
        ),
        yref='paper', y0=0, y1=1,
        xref='x', x0=x_data[-5], x1=x_data[-5],
    )

    # Annotations for nowcast and forecast
    fig.add_annotation(xref="x", x=x_data[-10],
                       text="Nowcast", bgcolor=color_nowcast)
    fig.add_annotation(xref="x", x=x_data[-5], 
                       text="Forecast", bgcolor=color_forecast)
    fig.update_annotations(
        xanchor="left", yanchor="top",
        yref="y", y=y_max, 
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="White"
        ),
        align="left",
        borderpad=4,
        showarrow=False
    )

    return fig


def minimize(fig):
    font_size = 8
    fig.update_layout(
        legend=dict(
            font=dict(size=font_size),
            itemsizing='trace',
        ),
        font=dict(size=font_size),
        margin=dict(t=25)
    )
    fig.update_shapes(
        line=dict(width=2),
    )
    y_max = max(fig.data[5]['y'])
    fig.update_annotations(
        font=dict(size=font_size),
        borderwidth=0.5
    )
    fig.update_traces(
        marker=dict(size=3),
        line=dict(width=1),
    )


def plotit(df, column_dict, rki=True, 
           skip_first_7=False,
           fixedrange=False,
           color_legend='rgb(229, 236, 246)', 
           color_forecast='rgb(24, 145, 255)', 
           color_nowcast='rgb(136, 207, 250)'):
    fig = create_figure_from_df(df, column_dict)
    return update_layout(fig, 
                         skip_first_7=skip_first_7,
                         fixedrange=fixedrange,
                         color_legend=color_legend,
                         color_forecast=color_forecast,
                         color_nowcast=color_nowcast)