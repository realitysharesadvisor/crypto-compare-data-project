import csv
import requests
import datetime
import pandas as pd
import numpy as np
from datetime import datetime

dd = pd.DataFrame([])
count = 0

with open('urlspluserrors.csv', 'rt') as csvfile:
		reader = csv.reader(csvfile)
		for url in reader:
			str = url[0]
			if(str[0:5] == "url ="):
				try:
					# get cryptocurrency
					index_beg1 = str.find("fsym=") + 5
					index_end1 = str.find("&tsym=")

					# get the exchange platform
					index_beg2 = str.find("&e=") + 3
					index_end2 = len(str)

					# get url
					url = str[6:]
					page = requests.get(url)
					data = page.json()['Data']
					# print(data)
					df = pd.DataFrame(data)[1:]
					df['timestamp'] = [datetime.fromtimestamp(d) for d in df.time]
					# print(df['timestamp'])
					df['Exchange'] = str[index_beg1:index_end1]
					df['Currency'] = str[index_beg2:index_end2]
					print(df)
					dd = dd.append(df)
				except(Exception):
					print("error handled")

dd.to_csv('exchangedata2.csv')