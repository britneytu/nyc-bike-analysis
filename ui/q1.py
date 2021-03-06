import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

# get station dataset
top_2016 = pd.read_csv(r'data\q1_data\2016\top.csv').sort_values(by=['month'])
top_2015 = pd.read_csv(r'data\q1_data\2015\top.csv').sort_values(by=['month'])
top_2014 = pd.read_csv(r'data\q1_data\2014\top.csv').sort_values(by=['month'])
top_2013 = pd.read_csv(r'data\q1_data\2013\top.csv').sort_values(by=['month'])
top = pd.concat([top_2016,top_2015,top_2014,top_2013])
# get top 10 stations in each time frame
top_10_2016_morning = pd.read_csv(r'data\q1_data\2016\top10_morning.csv')
top_10_2016_afternoon = pd.read_csv(r'data\q1_data\2016\top10_afternoon.csv')
top_10_2016_evening = pd.read_csv(r'data\q1_data\2016\top10_evening.csv')
top_10_2016=[top_10_2016_morning,top_10_2016_afternoon,top_10_2016_evening]

top_10_2015_morning = pd.read_csv(r'data\q1_data\2015\top10_morning.csv')
top_10_2015_afternoon = pd.read_csv(r'data\q1_data\2015\top10_afternoon.csv')
top_10_2015_evening = pd.read_csv(r'data\q1_data\2015\top10_evening.csv')
top_10_2015=[top_10_2015_morning,top_10_2015_afternoon,top_10_2015_evening]

top_10_2014_morning = pd.read_csv(r'data\q1_data\2014\top10_morning.csv')
top_10_2014_afternoon = pd.read_csv(r'data\q1_data\2014\top10_afternoon.csv')
top_10_2014_evening = pd.read_csv(r'data\q1_data\2014\top10_evening.csv')
top_10_2014=[top_10_2014_morning,top_10_2014_afternoon,top_10_2014_evening]

top_10_2013_morning = pd.read_csv(r'data\q1_data\2013\top10_morning.csv')
top_10_2013_afternoon = pd.read_csv(r'data\q1_data\2013\top10_afternoon.csv')
top_10_2013_evening = pd.read_csv(r'data\q1_data\2013\top10_evening.csv')
top_10_2013=[top_10_2013_morning,top_10_2013_afternoon,top_10_2013_evening]

top_10_list = [top_10_2013,top_10_2014,top_10_2015,top_10_2016]

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("NYC Bike Stations Popularity"),
                        html.P(
                            """Select different time frame using the dropdown and check the popularity status"""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                            id="year",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in ['2013', '2014', '2015','2016']
                                            ],
                                            placeholder="Select a year",
                                        ),
                                html.Br(),
                                dcc.Dropdown(
                                            id="month",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                                            ],
                                            placeholder="Select a month",
                                        )
                            ],
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="time-frame",
                                            options=[
                                                {"label": i, "value": i}
                                                for i in ['Morning', 'Afternoon', 'Evening']
                                            ],
                                            placeholder="Select a time frame",
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map"),
                        dcc.Graph(id="popular"),
                    ],
                ),
            ],
        ),
    ],
)

# @app.callback(
#     Output("month", "options"),
#     [
#         Input("year", "value"),
#     ],
# )

# def update_month(year):
#     if 


# Update Map Graph based on date-picker, selected data on histogram and location dropdown
@app.callback(
    Output("map", "figure"),
    [
        Input("time-frame", "value"),
        Input("year", "value"),
        Input("month", "value"),
        Input('popular','clickData')
    ],
)
def update_map(timeFrame,year,month,data):
    zoom = 12.0
    latInitial = 40.7272
    lonInitial = -73.991251
    bearing = 0
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    if year in ['2013','2014','2015','2016'] and month is not None and timeFrame is not None:
        i = months.index(month) + 1
        return get_year_top_10_map(timeFrame,year,i,data)
    data_list = [
     # Data for all rides based on date and time
            Scattermapbox(
                name='2016',
                lat=top_2016['latitude'],
                lon=top_2016['longitude'],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=top_2016['name'],
                marker=dict(
                    opacity=1,
                    size=10,
                    color='#de3abd',
                ),
            ),
            # Data for all rides based on date and time
            Scattermapbox(
                name='2015',
                lat=top_2015['latitude'],
                lon=top_2015['longitude'],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=top_2015['name'],
                marker=dict(
                    opacity=1,
                    size=10,
                    color="#84d988",
                ),
            ),
            # Data for all rides based on date and time
            Scattermapbox(
                name='2014',
                lat=top_2014['latitude'],
                lon=top_2014['longitude'],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=top_2014['name'],
                marker=dict(
                    opacity=1,
                    size=10,
                    color="#78e1e3",
                ),
            ),
            # Data for all rides based on date and time
            Scattermapbox(
                name='2013' ,
                lat=top_2013['latitude'],
                lon=top_2013['longitude'],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=top_2013['name'],
                marker=dict(
                    opacity=1,
                    size=10,
                    color="#9b65e6",
                ),
            ),
    ]
    current_data = data_list
    if year is not None:
        current_data = [data_list[-(int(year)-2016)]]

    return go.Figure(
        data = current_data,
        
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=True,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
                style="dark",
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": 12,
                                        "mapbox.center.lon": "-73.991251",
                                        "mapbox.center.lat": "40.7272",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "dark",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )


@app.callback(
    Output('popular', 'figure'),
    [
        #Input('map', 'selectedData'),
        Input("time-frame", "value"),
        Input("year", "value"),
        Input("month", "value"),
    ],
)
def update_graph(timeFrame,year,month):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    if year in ['2013','2014','2015','2016'] and month is not None and timeFrame is not None:
        i = months.index(month) + 1
        return get_year_top_10(timeFrame,year,i)
    
    trace_2016 = dict(
        name='2016',
        type="scatter",
        hovertext=top_2016['name'],
        hoverinfo = 'text',
        x=top_2016['month'],
        y=top_2016['count'],
        line={"color": "#de3abd"},
        mode="lines+markers",
    )

    trace_2015 = dict(
        name='2015',
        type="scatter",
        hovertext=top_2015['name'],
        hoverinfo = 'text',
        x=top_2015['month'],
        y=top_2015['count'],
        line={"color": "#84d988"},
        mode="lines+markers",
    )

    trace_2014 = dict(
        name='2014',
        type="scatter",
        hovertext=top_2014['name'],
        hoverinfo = 'text',
        x=top_2014['month'],
        y=top_2014['count'],
        line={"color": "#78e1e3"},
        mode="lines+markers",
    )

    trace_2013 = dict(
        name='2013',
        type="scatter",
        hovertext=top_2013['name'],
        hoverinfo = 'text',
        x=top_2013['month'],
        y=top_2013['count'],
        line={"color": "#9b65e6"},
        mode="lines+markers",
    )

    layout = dict(
        title = 'Most popular station in each month',
        plot_bgcolor="#323130",
        paper_bgcolor="#323130",
        font={"color": "#fff"},
        height=400,
        xaxis={
            "range": [x for x in range(24)],
            "showline": True,
            "zeroline": False,
            "fixedrange": False,
            "title": "Month",
        },
        yaxis={
            "range": [
                min(0, min(min(top_2016['count']),min(top_2015['count']),min(top_2014['count']),min(top_2013['count']),)),
                max(0, max(max(top_2016['count']),max(top_2015['count']),max(top_2014['count']),max(top_2013['count']),)),
            ],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
        },
    )
    data_list = [trace_2013,trace_2014,trace_2015,trace_2016]
    if year is not None:
        data_list = [data_list[int(year)-2013]]

    return dict(data=data_list, layout=layout)

def get_year_top_10(time,year,month):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    frames = ['Morning','Afternoon','Evening']
    month = int(month)
    year = int(year)
    time = frames.index(time)
    df = top_10_list[year-2013]
    df = df[time]
    df = df.loc[df['month'] == month]
    return {
        'data': [
            {
                'x': [x for x in range(df.shape[0])],
                'y':df['count'],
                'nbins':10,
                #'customdata': df['storenum'],
                'type': 'bar',
                'autobinx': True,
                'xbins': {
                    'size':0.5
                },
                'hovertext':df['name'],
            }
        ],
        'layout': {
            'title': {
            'color':'#fafafa',
            'text':'Top 10 popular stations on {},{} {}'.format(months[int(month) - 1],frames[time],year),
            },
            'font':{"color": "#fff"},
            'plot_bgcolor':"#323130",
            'paper_bgcolor':"#323130",
            'xaxis':{
            'color':'#fafafa',
            "range": [x for x in range(10)],
            "showline": True,
            "zeroline": False,
            "fixedrange": False,
            "title": "Rank",
            },
            'yaxis':{
            'color':'#fafafa',
            "showline": True,
            "zeroline": False,
            "fixedrange": False,
            "title": "Count",
            },
            #'margin': {'l': 40, 'r': 20, 't': 0, 'b': 30}
        }
    }

def get_year_top_10_map(time,year,month,data):
    zoom = 12.0
    latInitial = 40.7272
    lonInitial = -73.991251
    bearing = 0
    frames = ['Morning','Afternoon','Evening']
    month = int(month)
    year = int(year)
    time = frames.index(time)
    df = top_10_list[year-2013]
    df = df[time]
    df = df.loc[df['month'] == month]
    d = df
    
    selectedDataLat = []
    selectedDataLong = []
    selectedMap = Scattermapbox()
    selected_station = ''
    if data is not None:
        selected_station = data['points'][0]['hovertext']
        is_selected = df['name'] == selected_station
        selectedData = df[is_selected]
        selectedDataLat = [selectedData['latitude'].tolist()[0]]
        selectedDataLong = [selectedData['longitude'].tolist()[0]]
       
    s_opacity = 1
    if data is not None:
        s_opacity = .5

    return go.Figure(
        data=[
            # Data for all rides based on date and time
            Scattermapbox(
                lat=df['latitude'],
                lon=df['longitude'],
                mode="markers",
                hoverinfo="lat+lon+text",
                text=df['name'],
                marker=dict(
                    opacity=s_opacity,
                    size=8,
                    color='#de3abd',
                ),
            ),

            #Another layer for selected station
            Scattermapbox(
                lat=selectedDataLat,
                lon=selectedDataLong,
                text = [selected_station],
                mode="markers",
                hoverinfo="lat+lon+text",
                marker=dict(
                    opacity=1,
                    size=20,
                    color='#9b65e6',
                ),
            ),
        ],
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial),  # 40.7272  # -73.991251
                style="dark",
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": 12,
                                        "mapbox.center.lon": "-73.991251",
                                        "mapbox.center.lat": "40.7272",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "dark",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )   

if __name__ == "__main__":
    app.run_server(debug=True)
