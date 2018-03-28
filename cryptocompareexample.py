import requests
import datetime
import pandas as pd
import numpy as np
from datetime import datetime


#get exchange list
def getexchangelist():
    req = requests.get('https://min-api.cryptocompare.com/data/all/exchanges').json()
    exchangelist = pd.DataFrame(req)
    #exchangelist.to_csv('exchangelist.csv')
    return exchangelist

exchangelist = getexchangelist()
#print(exchangelist)


#Get open, high, low, close, volumefrom and volumeto daily historical data. The values are based on 00:00 GMT time.
def daily_price(symbol, comparison_symbol,e):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit=5000'\
            .format(symbol.upper(), comparison_symbol.upper())
    if e:
        url += '&e={}'.format(e)
#    if all_data:
#        url += '&allData=true'
    print ("url = ", url)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)[1:]
    df['timestamp'] = [datetime.fromtimestamp(d) for d in df.time]
    return df

#df = daily_price(symbol='BTC',comparison_symbol='USD',e='Coinbase')
#print(df)


#for loop to get daily price for coins on different exchanges
dd = pd.DataFrame([])
for ex in exchangelist.keys():
    for coin in exchangelist.index:
        if isinstance(exchangelist[ex][coin],list) and 'USD' in exchangelist[ex][coin]:
            try:
                df = daily_price(symbol=coin, comparison_symbol='USD', e=ex)
                df['Exchange'] = ex
                df['Currency'] = coin
                dd = dd.append(df)
            except(Exception):
                print("error handled")
dd.to_csv('exchangedata2.csv')
print(dd)
