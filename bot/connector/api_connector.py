import requests
# import time
# from io import BytesIO
from datetime import datetime
import pandas as pd
import json

tcbs_headers = {
  'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
  'DNT': '1',
  'Accept-language': 'vi',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Referer': 'https://tcinvest.tcbs.com.vn/',
  'sec-ch-ua-platform': '"Windows"'
}


def ohlc_data (symbol='REE', start_date='2023-01-01',
                        end_date='2023-10-31', resolution='D', bar_type='bars-long-term', headers=tcbs_headers):
    """
    Get longterm OHLC data from TCBS
    Parameters:
    """
    # convert date difference to number of days
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    delta = (end_date - start_date).days
    # convert end_date to timestamp
    end_date_stp = int(end_date.timestamp())
    start_date_stp = int(start_date.timestamp())

    if(resolution == '5') :
        bar_type = 'bars'

    print(f'Time range is {delta} days. Looping through {delta // 365 + 1} requests')
    url = f"https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/{bar_type}?ticker={symbol}&from={start_date_stp}&to={end_date_stp}&type=stock&resolution={resolution}"
    print(url)
    response = requests.request("GET", url, headers=headers)
    status_code = response.status_code
    print(status_code)
    if status_code == 200:
        data = response.json()
#         df is
        df = pd.DataFrame(data['data'])

        if df.size > 0:
        # convert tradingDate to time column
            df['time'] = pd.to_datetime(df['tradingDate']).dt.strftime('%Y-%m-%d')
        # drop tradingDate column
            df.drop('tradingDate', axis=1, inplace=True)
            df['ticker'] = symbol
            df = df[(df['time'] >= start_date.strftime('%Y-%m-%d')) & (df['time'] <= end_date.strftime('%Y-%m-%d'))]
            df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
            df['volume'] = df['volume'].astype(int)
            return df
#         return data
    return None


def get_token (payload = None):
    url = "https://apipub.tcbs.com.vn/authen/v1/login"
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload,verify=False)
    return response.json()['token']

def get_list_stock (token, url):
    # url = "https://apiext.tcbs.com.vn/hft-krema/v1/accounts/0001698153/se"    
    headers = {
    'Authorization': f'Bearer {token}' 
    }
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response)
    return response.json()