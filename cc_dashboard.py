import pandas as pd
import numpy as np
import datetime
import os

import plotly
from plotly import tools
from plotly.graph_objs import Scatter, Layout, Histogram
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=False)

#Function to plot dashboard
def crypto_dashboard(name):
    """This function creates dashboard with key metrics of a cryptocurrency: 
    Closing Price (USD), Trading Volume (Units), Daily Percentage Gain (%), 
    Total Market Cap (USD), Acum. Daily Return (Units), Volatility (%)"""
    
    #Read Coin data into dataframe
    df = pd.read_csv('Data/panda'+name+'.csv')
    #Conver Date column into timeseries
    df['date'] = pd.to_datetime(df['date'])
    #Set Date as index
    df.set_index(['date'],inplace=True)
    #Sort dataframe by date
    df.sort_index(axis=0, ascending=True,inplace=True)
    
    # Calculate acumulated daily return
    df['acumday'] = df['today'] + 1
    df['acumday'] = df['acumday'].cumprod()
    
    #Calculate Volatility of Price using 15 days period
    min_periods = 15
    cc_vol = (df['today'].rolling(min_periods).std() * np.sqrt(min_periods))
    cc_vol['volatility'] = cc_vol.values
    
    #Analyze past 12 months
    #Create scatter plot combined of each variable
    trace1 = go.Scatter(y=df.close, x=df.index, mode = 'lines', fill='tonexty')
    trace2 = go.Scatter(y=df.volume, x=df.index, mode = 'lines', fill='tonexty')
    trace3 = go.Histogram(x=df.today,opacity=0.75,histnorm='probability')
    trace4 = go.Scatter(y=df.marketcap, x=df.index, mode = 'lines', fill='tonexty')
    trace5 = go.Scatter(y=df.acumday, x=df.index, mode = 'lines', fill='tonexty')
    trace6 = go.Scatter(y=cc_vol.volatility, x=cc_vol.index, mode = 'lines', fill='tonexty')
    
    #Create layout for charts
    fig = tools.make_subplots(rows=3,
                            cols=2,
                            shared_xaxes=False,
                            print_grid=False, 
                            subplot_titles=('Closing Price (USD)',
                                            'Trading Volume (Units)',
                                            'Daily Percentage Gain (%)',
                                            'Total Market Cap (USD)',
                                            'Acum. Daily Return (Units)',
                                            'Volatility (%)'
                                         ))
    #Join all subplot into figure
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 2)
    fig.append_trace(trace5, 3, 1)
    fig.append_trace(trace6, 3, 2)
    
    
    #Print all subplots
    fig['layout'].update(height=700, 
                       width=1200,
                       showlegend=False, 
                       title=''+name+' Dashboard 12M',
                      ) 

    ###Create directory to store data
    if not os.path.exists('Reports'):
      os.makedirs('Reports')

    plotly.offline.plot(fig, filename=('Reports/'+name+'.html'))

    return

    # Hola esto es una prueba y borrame