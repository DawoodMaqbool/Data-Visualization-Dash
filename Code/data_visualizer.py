# importing all the necessary modules
import plotly_express as px
from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# importing public token for the dark theme
token = open('.mapbox_token').read()
# importing Dataset
df = pd.read_csv("crash_stat.csv", delimiter=',')
# Converting string based data into Datetime Formate
df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'])
# Setting Accident Date as Index
df.set_index('ACCIDENT_DATE', inplace=True)
app = dash.Dash(
    external_stylesheets=[dbc.themes.SOLAR]
)
server=app.server
# App layout sets the main layout of the app

app.layout = dbc.Container(fluid=True, children=[
    html.Br(),
    html.H5("Crash Statistics Victoria", id='heading', className='display-4 text-center', style={'textAlign': 'center'}),
    html.Br(),
    # Using the Bootstrap and HTML components of the DASH and creating the main layout
    dbc.Row([
        dbc.Col(md=6, children=[
            html.Label("Pick a Date : ", className='display-4', style={'font-size': '20px', 'margin': '15px'}),
            # DatePicker is a Module of Dash Core Components
            # this gives an interactive date and time module
            # this will allow the user to enter date and time
            dcc.DatePickerRange(
                id='my-date-picker-range_2',
                calendar_orientation='horizontal',
                day_size=35,
                end_date_placeholder_text="Return",
                with_portal=False,
                first_day_of_week=0,
                reopen_calendar_on_clear=True,
                is_RTL=False,
                clearable=True,
                number_of_months_shown=2,
                min_date_allowed=dt(2013, 7, 1),
                max_date_allowed=dt(2019, 2, 1),
                initial_visible_month=dt(2013, 7, 1),
                start_date=dt(2013, 7, 1).date(),
                end_date=dt(2014, 2, 1).date(),
                display_format='MMM Do, YY',
                month_format='MMMM, YYYY',
                minimum_nights=2,
                persistence=True,
                persisted_props=['start_date'],
                persistence_type='session',
                updatemode='singledate'
                ),
            html.Br(), html.Br(), html.Br(),
            dcc.Graph(id='bar_chart', style={})
            ]),
        dbc.Col(md=6, children=[
            html.Label("Pick a Date : ", className='display-4', style={'font-size': '20px', 'margin': '15px'}),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                calendar_orientation='horizontal',
                day_size=35,
                end_date_placeholder_text="Return",
                with_portal=False,
                first_day_of_week=0,
                reopen_calendar_on_clear=True,
                is_RTL=False,
                clearable=True,
                number_of_months_shown=2,
                min_date_allowed=dt(2013, 7, 1),
                max_date_allowed=dt(2019, 2, 1),
                initial_visible_month=dt(2013, 7, 1),
                start_date=dt(2013, 7, 1).date(),
                end_date=dt(2014, 2, 1).date(),
                display_format='MMM Do, YY',
                month_format='MMMM, YYYY',
                minimum_nights=2,
                persistence=True,
                persisted_props=['start_date'],
                persistence_type='session',
                updatemode='singledate'
                ),
            html.Br(), html.Br(), html.Br(),
            dcc.Graph(id='mymap')
            ])
        ]),
    dbc.Col(md=6, children=[
       html.Br(), html.Br(),
       html.H3("PieChart for Analyzing trend over Days", style={'textAlign': 'center'}),
       html.Br(), html.Br(),
       dcc.Dropdown(
           id='feature-dropdown',
           className='d-flex justify-content-center',
           options=[
               {'label': 'total_persons', 'value': 'TOTAL_PERSONS'},
               {'label': 'inj or fatal', 'value': 'INJ_OR_FATAL'},
               {'label': 'males', 'value': 'MALES'},
               {'label': 'females', 'value': 'FEMALES'},
           ],
           value='TOTAL_PERSONS'
       ),
    ]),
    dbc.Col(md=6, children=[
        html.Div([
            html.Br(), html.Br(),
            dcc.Graph(id='piechart')
            ])
        ])
    ])

# Callback functions are used to give output to the App
# Based on the Input provided
@app.callback(
    Output('mymap', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
# The output given to the callback are coming from here
def update_output(start_date, end_date):
    dff = df.loc[start_date:end_date]
    fig = px.scatter_mapbox(dff, lat='LATITUDE', lon='LONGITUDE', color='ACCIDENT_TYPE', template='plotly_dark', title='Crash MapBox', zoom=10, height=600, width=900,center=dict(lat=-37.98896, lon=145.1968), mapbox_style="carto-positron", hover_data={'ACCIDENT_TYPE': True, 'LATITUDE': False, 'LONGITUDE': False, 'TOTAL_PERSONS': True, 'SPEED_ZONE': True, 'SEVERITY': True, 'ROAD_GEOMETRY': True})
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@app.callback(
        Output('bar_chart', 'figure'),
        [Input('my-date-picker-range_2', 'start_date'),
         Input('my-date-picker-range_2', 'end_date')]
        )

def update_output(start_date, end_date):
    '''
    This Function is used to calculate average values
    for number of accidents
    '''
    dff = df.loc[start_date:end_date]
    time_data = dff['ACCIDENT_TIME']
    '''
    Creating temporary arrays for data modification
    '''
    tl1 = []
    tl2 = []
    tl3 = []
    # total variable holds the total number of accidents
    total = 0
    final_list = []
    x_axis = []
    # Generating 24 hours based lists
    for i in range(24):
        x_axis.append(i)
        tl3.append(0)
        final_list.append(0)

    for i in dff.index:
        temp = str(i)
        tl1.append(temp[0:10])

    for i in time_data:
        temp = str(i)
        tt = float(temp[0:5])
        if(tt % 1 < 0.3):
            val = tt-(tt % 1)
            tl2.append(val)
            tl3[(int(val) - 1)] += 1
        else:
            tl2.append(val + 1)
            tl3[int(val) - 1] += 1

    for i in tl3:
        total += i

    for i in range(len(tl3)):
        final_list[i] = ((tl3[i])/total) * 100

    dff['ACCIDENT_TIME'] = tl2
    fig = px.bar(dff, x=x_axis, y=final_list, height=600, width=900, template='plotly_dark', color=x_axis,title='Average Number of Accidents', labels={'x': 'Hours', 'y': 'Average'})
    return fig
@app.callback(
    dash.dependencies.Output('piechart', 'figure'),
    [dash.dependencies.Input('feature-dropdown', 'value')])
def update_output(value):
    fig = px.pie(df, names='DAY_OF_WEEK', values=value, title='Relation of Days of week with other attributes',template='plotly_dark', color_discrete_sequence=px.colors.sequential.RdBu, height=600,width=900)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
