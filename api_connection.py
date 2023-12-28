""" This script store the function required to stream data from the API of your choice"""

import requests
import json
import pandas as pd
import numpy as np

# import plotting library
import matplotlib
import matplotlib.pyplot as plt 
from datetime import date, datetime, timedelta

# create GET request

def get_data_from_api():
    
    endpoint = 'https://apidatos.ree.es'

    get_archives = '/es/datos/mercados/precios-mercados-tiempo-real'

    headers = {'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Host': 'apidatos.ree.es'}

    start_date = '2023-11-23T00:00' # datetime.now() 
    end_date = '2023-11-23T23:59'   # start_date + timedelta(hours=24)

    params = {'start_date': start_date, 'end_date': end_date, 'time_trunc':'hour'}

    response = requests.get(endpoint+get_archives, headers=headers, params=params)
    outputs = response.json()

    
    if response.status_code >= 200 and response.status_code < 300:
        print('Connection is established')
    else :
        print('ERROR:')
        print(response.status_code)

    times2 = []
    pvpc_prices = []
    pvpc_data = outputs['included'][0]
    pvpc_values = pvpc_data['attributes']['values']

    # New vectors of price and time
    for data_point in pvpc_values:
        #print(time_period['value'])
        pvpc_prices.append(data_point['value'])
        times2.append(data_point['datetime'])

    # Convert each string to datetime object
    times2 = [datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z") for date_str in times2]
    times2_without_tz = [dt.replace(tzinfo=None) for dt in times2]
    
    return pvpc_prices, times2_without_tz
