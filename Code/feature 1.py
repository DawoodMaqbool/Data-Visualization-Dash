from datetime import datetime as dt
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc


# importing Dataset
df = pd.read_csv("crash_stat.csv", delimiter=',')
# The string data format is converted into datetime format.
df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'])
# Index date has been set with respect to Accident Date
df.set_index('ACCIDENT_DATE', inplace=True)

#the public token for dark theme is imported
token = open('.mapbox_token').read()
app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR])
server=app.server()
app.layout = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',  # ID to be used in the callback section
        min_date_allowed=dt(2013, 7, 1),  # minimum date allowed on calendar
        max_date_allowed=dt(2019, 2, 1),  # maximum date allowed on calendar
        initial_visible_month=dt(2013, 7, 1),  # the fixed set date when user opens the page initially
        start_date=dt(2013, 7, 1).date(),
        end_date=dt(2014, 7, 1).date(),
        display_format='MMM Do, YY',  # how selected dates are displayed in the DatePickerRange component.
        month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
        calendar_orientation='horizontal',  
        day_size=30,  # size of image of calendar while choosing dates.
        start_date_placeholder_text="Start Date",   # text that appears inside the box when no start date chosen
        end_date_placeholder_text="End Date",  # text that appears inside the box when no end date chosen
        first_day_of_week=1,  # Display of starting week in calendar (1 = Monday)
        reopen_calendar_on_clear=True,
        clearable=True,  # user can clear the dropdown
        number_of_months_shown=2,  # number of months shown when calendar is open
        minimum_nights=2,  # minimum number of days between start and end date
        persistence=True, # user interactions in this component to be persisted when the component or the page is refreshed
        updatemode='singledate'  # singledate or bothdates. Determines when callback is triggered
    ),
    html.Br(),
    html.Br(),
    html.H2("Information of all Accidents happened in the selected time period", style={'textAlign': 'center'}),
    html.Br(),
    dcc.Graph(id='mymap')
])

@app.callback(
    Output('mymap', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_output(start_date, end_date):
    # print("Start date: " + start_date)
    # print("End date: " + end_date)
    dff = df.loc[start_date:end_date]
    # print(dff[:5])

    fig = px.scatter_mapbox(dff, lat='LATITUDE', lon='LONGITUDE', zoom=8, height=520, width=1365, template='plotly_dark', color='ACCIDENT_TYPE',center=dict(lat=-37.95557, lon=145.11385), mapbox_style="carto-positron", hover_data={'ACCIDENT_TYPE': True, 'ACCIDENT_TIME':True, 'LATITUDE': False, 'LONGITUDE': False, 'REGION_NAME': True, 'TOTAL_PERSONS': True, 'INJ_OR_FATAL': True, 'RMA': True})
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    fig.update_layout(margin={"r": 10, "t": 0, "l": 10, "b": 0})
    return fig


if __name__ == '__main__':
    app.run_server()
