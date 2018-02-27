##Used libraries
from downloader import crypto_dataset
from cc_dashboard import crypto_dashboard
import datetime

#Select Period to track
start_date = datetime.datetime(day=1,month=1,year=2017)
end_date = datetime.datetime(day=31,month=12,year=2017)

with open('coins.txt','r') as f:
    coins = f.read().splitlines()

for item in coins:
    crypto_dataset(item,start_date,end_date) 

for item in coins:
    crypto_dashboard(item) 
