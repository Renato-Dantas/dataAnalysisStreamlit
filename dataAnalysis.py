import streamlit as st
import pandas as pd
import plotly.graph_objects as go 
import pandas_datareader as web
from datetime import date, timedelta

def get_period():
    start = st.date_input('Select the period to start')
    if start == date.today():
        start = ('2020-01-01')
    else:
        pass
    return start

def upload_file(startDate):
    companies = {'Amazon': 'AMZN', 'Netflix': 'NFLX','Facebook':'FB','Apple':'AAPL'}
    company = st.selectbox('Select the Company:',list(companies.keys()))
    companyTag = companies[company]

    data = web.DataReader(companyTag, data_source= 'yahoo', start = startDate, end = date.today())
    data.reset_index(inplace=True)
    return data

def view_data(data):
    st.write(data)

def linechart_prices(data):
    high = go.Scatter(x = data.Date, y = data.High, name = 'High')
    low = go.Scatter(x = data.Date, y = data.Low, name = 'Low')
    close = go.Scatter(x = data.Date, y = data.Close, name = 'Close')

    trace = [high, low, close]
    layout = dict(title = 'High, Low and Close values', paper_bgcolor = 'aliceblue', plot_bgcolor = 'aliceblue')

    fig = dict(data = trace, layout = layout)
    st.plotly_chart(fig)

def candlestick(data):
    trace = go.Candlestick(x = data.Date, open = data.Open, high = data.High, low = data.Low, close = data.Close)
    layout = go.Layout(dict(title = 'Candlestick Stock Values'), xaxis = dict(rangeslider = dict(visible = False)), paper_bgcolor = 'aliceblue', plot_bgcolor = 'aliceblue')
    fig = go.Figure([trace], layout = layout)
    st.plotly_chart(fig)

def linechart_volume(data):
    layout = go.Layout(dict(title = 'Historic Volume Transitions'),paper_bgcolor = 'aliceblue', plot_bgcolor = 'aliceblue')
    trace = data = go.Scatter(x = data.Date, y = data.Volume, name = 'Volume' )
    fig = go.Figure([trace], layout = layout)
    st.plotly_chart(fig)    

def last_value(data):
    st.write('### Actual Stock Price')
    lastValue = round(float(data.Close.tail(1)),3)
    lastDay = data.Date.tail(1)

    day = []
    for i in lastDay:
        day.append(str(i))
    lastdate = day[0].split(' ')
    lastdate = lastdate[0]
    st.info(f'The last value found is $ {lastValue} on {lastdate}')

def percent(data):
    try:
        lastValue = list(data.Close.tail(2))
        percent = round(((lastValue[1]/lastValue[0])-1)*100,2)
        if percent >0:
            st.success(f'Stock Price increase {percent}%')
        else:
            st.error(f'Stock Price decrease {percent}%')
    except:
        st.error('No data in the selected period. Please choose another day to start the view') 
        
def avg_value(data):
    avg = round(data.Close.mean(),2)
    st.success(f'The average stock price is $ {avg} for the period')

def dataAnalysisText():
    st.markdown('This page is dedicated to show an **application of Data Science**, using the most popular libraries.\n\n First of all, We need to **analyse the tendencies of the Stock Price**. To this, We used here the ***Plotly*** libraries, that permit you to **create iterative plots and dashboards**. \n\n You can find more information about plotly on: ***https://plotly.com*** \n\n Also We used ***Pandas*** to manipulate the data and We get the data using ***pandas_datareader*** to upload all info from Yahoo')
    st.markdown('Please select a **date to start** to view the plots and the **interested company** \n\n ***If you do not select a new date, the plot will be created starting in January 2020***')