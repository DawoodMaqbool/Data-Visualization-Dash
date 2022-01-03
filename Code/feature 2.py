from datetime import datetime as dt
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# importing Dataset
while True:
    dataset = input("Enter the name of the file"
    "\n \n Please type in the path to your file and press 'Enter': ")
    try:
        df = pd.read_csv(dataset, delimiter=',')
    except FileNotFoundError:
        print("Wrong file or file path")
    else:
        break

# The string data format is converted into datetime format.
df['ACCIDENT_DATE'] = pd.to_datetime(df['ACCIDENT_DATE'])
# Index date has been set with respect to Accident Date
df.set_index('ACCIDENT_DATE', inplace=True)

#the public token for dark theme is imported
token = open('.mapbox_token').read()

app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR])
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
    html.H2("Bar Chart of average number of Accidents in each hour of the day in the selected time period", style={'textAlign': 'center'}),
    html.Br(),
    dcc.Graph(id='bar_chart')
])


@app.callback(
    Output('bar_chart', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_output(start_date, end_date):
    average = []
    hours = []
    df2 = df.loc[start_date:end_date]
    time_data = df2['ACCIDENT_TIME']
    a1=[]
    a2=[]
    a3=[]
    total = 0
    for i in range(24):
        hours.append(i)
        a3.append(0)
        average.append(0)
    for i in df.index:
        temp = str(i)
        a1.append(temp[0:10])
    for i in time_data:
        temp = str(i)
        t = float(temp[0:5])
        if(t % 1 < 0.3):
            val = t-(t % 1)
            a2.append(val)
            a3[int(val) - 1] += 1
        else:
            a2.append(val+1)
            a3[int(val) -1] += 1
    for i in a3:
        total += i
    for i in range(len(a3)):
        average[i] = ((a3[i]/total) * 100)
    df2['ACCIDENT_TIME'] = a2
    fig = px.bar(df2, x = hours, y = average, height = 525, width = 1340, template = 'plotly_dark', color=hours,title='average number of Accidents in each hour of the day', labels={'x': 'Hours', 'y': 'Average'})
    return fig


if __name__ == '__main__':
    app.run_server()
