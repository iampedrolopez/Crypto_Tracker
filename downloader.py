##Used libraries
import pandas as pd
import numpy as np
import os
import html5lib
import datetime

#Function to extract data
def crypto_dataset(name,start_date,end_date):
    """This function creates panel data with the percentage returns from a 
    cryptocurrency using the closing value obtained from www.coinmarketcap.com
    , along with various lagged returns from prior trading periods (Lags defaults
    to 5 days. Trading volume, Direction from previous day and market cap."""
    
    #Download the information from the web
    df = pd.read_html('https://coinmarketcap.com/currencies/'+name+
                       '/historical-data/?start='+
                      start_date.strftime('%Y%m%d')+
                      '&end='+end_date.strftime('%Y%m%d'))[0]
    
    ###Lowercase all column headers
    df.columns = df.columns.str.lower()
    
    #Set the 'Date' column as the index
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(['date'],inplace=True)
    
    
    ###Pre-Processing of the data
    
    #Create range Column: Variation betwwen the day
    df['range'] = ((df['close'] - df['open'])/df['open'])*100
    df['volume'] = pd.to_numeric(df['volume'],errors="coerce")
    df['market cap'] = pd.to_numeric(df['market cap'],errors="coerce")
    
    #Calculate Percentage return for various periods
    
    df['today'] = df['close'].pct_change(-1) #  
    df['dlag1'] = df['today'].shift(-1) # 1 DAY lookback
    df['dlag2'] = df['today'].shift(-2) # 2 DAY lookback
    df['dlag3'] = df['today'].shift(-3) # 3 DAY lookback
    df['dlag4'] = df['today'].shift(-4) # 4 DAY lookback
    df['dlag5'] = df['today'].shift(-5) # 5 DAY lookback
    
    ##Drop NA rows
    df.dropna(inplace=True)
    
    ###Create response variable
    df['todaydir'] = np.where(df['today']>=0.0000, 'Up', 'Down')
    
    ###Remove spaces in columns
    df.rename(columns={'market cap':'marketcap'},inplace=True)
    
    ###Create directory to store data
    if not os.path.exists('Data'):
        os.makedirs('Data')
    
    ###Store data into csv file
    df.to_csv('Data/panda'+name+'.csv',float_format='%.4f', encoding='utf-8', index=True)
    print(''+name+' Ok')
    return